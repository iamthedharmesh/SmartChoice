"""
Preprocess the TMDB 5000 dataset for a content-based recommender.

Viva idea:
  We do not recommend from raw CSV columns. We turn each movie into one
  cleaned text string called "tags" (plot + genres + keywords + cast + director).
  Later, TF-IDF will turn those tags into numbers.

This file only prepares data. It does not train TF-IDF or cosine similarity.
"""

from __future__ import annotations

import ast
import json
import re
from pathlib import Path

import pandas as pd

# backend/app/ml/preprocess.py -> parents[2] is the backend/ folder
BACKEND_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = BACKEND_ROOT / "data"
ARTIFACTS_DIR = BACKEND_ROOT / "artifacts"

MOVIES_CSV = DATA_DIR / "tmdb_5000_movies.csv"
CREDITS_CSV = DATA_DIR / "tmdb_5000_credits.csv"
PROCESSED_CSV = ARTIFACTS_DIR / "processed_movies.csv"

# Using the first 3 billed actors is a common academic choice:
# they usually define the "feel" of the movie without filling tags with extras.
TOP_CAST_COUNT = 3


def load_raw_datasets() -> tuple[pd.DataFrame, pd.DataFrame]:
    """Read the two Kaggle TMDB 5000 CSV files."""
    if not MOVIES_CSV.exists() or not CREDITS_CSV.exists():
        raise FileNotFoundError(
            "Put tmdb_5000_movies.csv and tmdb_5000_credits.csv in backend/data/"
        )

    movies = pd.read_csv(MOVIES_CSV)
    credits = pd.read_csv(CREDITS_CSV)
    return movies, credits


def merge_movies_and_credits(movies: pd.DataFrame, credits: pd.DataFrame) -> pd.DataFrame:
    """
    Join plot/genre data with cast/crew data.

    movies.id and credits.movie_id are the same TMDB movie id.
    Both files also have a title column, so after the merge pandas names them
    title_x and title_y. We keep one title and drop the duplicate.
    """
    merged = movies.merge(
        credits,
        left_on="id",
        right_on="movie_id",
        how="inner",
        suffixes=("_movies", "_credits"),
    )

    # Prefer the movies-table title; fall back if it is somehow empty.
    if "title_movies" in merged.columns:
        merged["title"] = merged["title_movies"].fillna(merged.get("title_credits"))
    elif "title" not in merged.columns:
        raise KeyError("Merged data has no title column.")

    return merged


def parse_json_list(value) -> list:
    """
    The CSV stores lists as text that looks like JSON, for example:
      [{"id": 28, "name": "Action"}, {"id": 12, "name": "Adventure"}]

    Missing cells (NaN) or broken text become an empty list so later steps
    never crash.
    """
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return []

    text = str(value).strip()
    if text == "" or text == "[]":
        return []

    for parser in (json.loads, ast.literal_eval):
        try:
            parsed = parser(text)
            return parsed if isinstance(parsed, list) else []
        except (json.JSONDecodeError, ValueError, SyntaxError, TypeError, MemoryError):
            continue

    return []


def names_from_objects(value, limit: int | None = None) -> list[str]:
    """Pull the 'name' field from a list of dicts (genres, keywords, cast)."""
    items = parse_json_list(value)
    names: list[str] = []
    for item in items:
        if isinstance(item, dict) and item.get("name"):
            names.append(str(item["name"]))
        if limit is not None and len(names) >= limit:
            break
    return names


def director_from_crew(value) -> str:
    """
    Crew is a list of jobs (Director, Editor, Producer, ...).
    Content-based recommenders usually keep only the Director.
    If there is more than one Director, we keep the first.
    """
    for person in parse_json_list(value):
        if isinstance(person, dict) and person.get("job") == "Director":
            name = person.get("name")
            if name:
                return str(name)
    return ""


def collapse_token(text: str) -> str:
    """
    Turn 'Sam Worthington' into 'samworthington'.

    Why: TF-IDF splits on spaces. If we keep the space, 'sam' and 'worthington'
    are two unrelated words. Removing spaces makes the whole name one token,
    so two movies that share an actor match more strongly.
    The same idea applies to 'Science Fiction' -> 'sciencefiction'.
    """
    cleaned = re.sub(r"[^a-z0-9]+", "", text.lower())
    return cleaned


def clean_overview(text) -> str:
    """Lowercase the plot and keep letters/numbers/spaces only."""
    if text is None or (isinstance(text, float) and pd.isna(text)):
        return ""
    cleaned = re.sub(r"[^a-z0-9\s]+", " ", str(text).lower())
    return re.sub(r"\s+", " ", cleaned).strip()


def build_tags(
    overview: str,
    genres: list[str],
    keywords: list[str],
    cast: list[str],
    director: str,
) -> str:
    """
    One document per movie for TF-IDF.

    Overview stays as normal words (story meaning).
    Genres, keywords, cast, and director are collapsed into single tokens.
    """
    parts: list[str] = []

    if overview:
        parts.append(overview)

    # Repeat high-signal tokens so TF-IDF is not dominated by generic plot words
    # such as "heist" or "mission". Director/cast/genres tell us the movie's identity.
    genre_tokens = [collapse_token(name) for name in genres if name]
    keyword_tokens = [collapse_token(name) for name in keywords if name]
    cast_tokens = [collapse_token(name) for name in cast if name]
    director_token = collapse_token(director) if director else ""

    parts.extend(genre_tokens * 2)
    parts.extend(keyword_tokens * 2)
    parts.extend(cast_tokens * 2)
    if director_token:
        parts.extend([director_token] * 3)

    return " ".join(part for part in parts if part)


def preprocess_movies() -> pd.DataFrame:
    """Full pipeline: load -> merge -> extract -> tags -> save-ready table."""
    movies, credits = load_raw_datasets()
    df = merge_movies_and_credits(movies, credits)

    # Keep only the columns we actually need for recommendations.
    df = df[
        [
            "id",
            "title",
            "overview",
            "genres",
            "keywords",
            "cast",
            "crew",
            "original_language",
            "vote_average",
            "release_date",
            "popularity",
            "runtime",
            "production_countries",
        ]
    ].copy()

    df["overview"] = df["overview"].fillna("")
    df["title"] = df["title"].fillna("").astype(str).str.strip()

    # Drop rows that cannot be shown or searched (no id / no title).
    df = df[df["title"] != ""]
    df = df.dropna(subset=["id"])
    df["movie_id"] = df["id"].astype(int)

    # Preserve metadata columns for preference-based recommendations
    df["original_language"] = df["original_language"].fillna("").astype(str).str.strip()
    df["vote_average"] = pd.to_numeric(df["vote_average"], errors="coerce")
    df["release_date"] = df["release_date"].fillna("").astype(str).str.strip()
    df["popularity"] = pd.to_numeric(df["popularity"], errors="coerce")
    df["runtime"] = pd.to_numeric(df["runtime"], errors="coerce")

    # Extract production country names (ISO codes + names)
    def country_names(value) -> list[str]:
        items = parse_json_list(value)
        names = []
        for item in items:
            if isinstance(item, dict):
                code = item.get("iso_3166_1")
                name = item.get("name")
                if code:
                    names.append(code)
                elif name:
                    names.append(str(name))
        return names

    df["production_countries"] = df["production_countries"].apply(country_names)

    df["genres"] = df["genres"].apply(lambda value: names_from_objects(value))
    df["keywords"] = df["keywords"].apply(lambda value: names_from_objects(value))
    df["cast"] = df["cast"].apply(
        lambda value: names_from_objects(value, limit=TOP_CAST_COUNT)
    )
    df["director"] = df["crew"].apply(director_from_crew)

    cleaned_overview = df["overview"].apply(clean_overview)

    df["tags"] = [
        build_tags(overview, genres, keywords, cast, director)
        for overview, genres, keywords, cast, director in zip(
            cleaned_overview,
            df["genres"],
            df["keywords"],
            df["cast"],
            df["director"],
        )
    ]

    # Movies with empty tags would become empty vectors later — drop them now.
    df = df[df["tags"].str.len() > 0].copy()

    processed = pd.DataFrame(
        {
            "movie_id": df["movie_id"],
            "title": df["title"],
            "overview": cleaned_overview.loc[df.index],
            "genres": df["genres"].apply(lambda names: " ".join(names)),
            "keywords": df["keywords"].apply(lambda names: " ".join(names)),
            "cast": df["cast"].apply(lambda names: " ".join(names)),
            "director": df["director"],
            "tags": df["tags"],
            "original_language": df["original_language"],
            "vote_average": df["vote_average"],
            "release_date": df["release_date"],
            "popularity": df["popularity"],
            "runtime": df["runtime"],
            "production_countries": df["production_countries"].apply(lambda names: " ".join(names)),
        }
    )

    processed = processed.drop_duplicates(subset=["movie_id"]).reset_index(drop=True)
    return processed


def save_processed_movies(processed: pd.DataFrame) -> Path:
    """Save a CSV the next ML step can load with pandas.read_csv."""
    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
    processed.to_csv(PROCESSED_CSV, index=False)
    return PROCESSED_CSV


def print_preprocessing_report(processed: pd.DataFrame) -> None:
    """Proof for you (and viva): counts, columns, and one example movie."""
    sample = processed.iloc[0]

    print("=== SmartChoice preprocessing report ===")
    print(f"Movies processed: {len(processed)}")
    print(f"Columns: {list(processed.columns)}")
    print(f"Saved to: {PROCESSED_CSV}")
    print()
    print("--- Sample movie ---")
    print(f"movie_id : {sample['movie_id']}")
    print(f"title    : {sample['title']}")
    print(f"genres   : {sample['genres']}")
    print(f"keywords : {sample['keywords']}")
    print(f"cast     : {sample['cast']}")
    print(f"director : {sample['director']}")
    tags = str(sample["tags"])
    preview = tags if len(tags) <= 400 else tags[:400] + "..."
    print(f"tags     : {preview}")


def main() -> None:
    processed = preprocess_movies()
    save_processed_movies(processed)
    print_preprocessing_report(processed)


if __name__ == "__main__":
    main()
