"""
Content-based movie recommendation engine (TF-IDF + cosine similarity).

Viva summary:
  1. Each movie already has a "tags" string (plot + genres + keywords + cast + director).
  2. TF-IDF turns that text into a numeric feature vector.
  3. Cosine similarity measures how close two movie vectors are (angle, not raw distance).
  4. For a chosen movie we score it against every other movie and return the top 10.

We do NOT build a 4800 x 4800 similarity matrix. That would use a lot of RAM.
We keep the TF-IDF matrix (sparse) and compute one row of similarities on demand.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# backend/app/ml/recommender.py -> parents[2] is backend/
BACKEND_ROOT = Path(__file__).resolve().parents[2]
ARTIFACTS_DIR = BACKEND_ROOT / "artifacts"
PROCESSED_CSV = ARTIFACTS_DIR / "processed_movies.csv"

VECTORIZER_PATH = ARTIFACTS_DIR / "tfidf_vectorizer.joblib"
MATRIX_PATH = ARTIFACTS_DIR / "tfidf_matrix.joblib"
MOVIES_PATH = ARTIFACTS_DIR / "movies_index.joblib"

TOP_N = 10


def normalize_title(title: str) -> str:
    """Case-insensitive match; extra spaces are ignored."""
    return " ".join(str(title).lower().split())


def load_processed_movies() -> pd.DataFrame:
    if not PROCESSED_CSV.exists():
        raise FileNotFoundError(
            "processed_movies.csv is missing. Run: python -m app.ml.preprocess"
        )
    df = pd.read_csv(PROCESSED_CSV)
    df["tags"] = df["tags"].fillna("")
    df["title"] = df["title"].fillna("").astype(str)
    df = df[df["tags"].str.len() > 0].reset_index(drop=True)
    return df


def train_model(df: pd.DataFrame) -> tuple[TfidfVectorizer, object]:
    """
    Fit TF-IDF on all movie tags.

    What TF-IDF does:
      TF  (term frequency)  = how often a word appears in THIS movie's tags.
      IDF (inverse document frequency) = words that appear in almost every
          movie (like "film") get a SMALL weight. Rare, distinctive words
          (like "inception" or a director's name) get a LARGE weight.

    What a feature vector is:
      After vectorization, each movie is a long list of numbers — one number
      per vocabulary term. Most values are 0 because a movie only uses a
      small subset of all words. scikit-learn stores this as a SPARSE matrix
      so those zeros do not waste memory.

    stop_words="english" drops very common English words (the, and, of)
    that do not help us tell movies apart.
    """
    vectorizer = TfidfVectorizer(
        stop_words="english",
        min_df=2,
        max_features=50000,
    )
    tfidf_matrix = vectorizer.fit_transform(df["tags"])
    return vectorizer, tfidf_matrix


def save_artifacts(
    vectorizer: TfidfVectorizer,
    tfidf_matrix,
    df: pd.DataFrame,
) -> None:
    """Save the trained vectorizer, sparse TF-IDF matrix, and a slim movie table."""
    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(vectorizer, VECTORIZER_PATH)
    joblib.dump(tfidf_matrix, MATRIX_PATH)
    movies_index = df[["movie_id", "title"]].copy()
    joblib.dump(movies_index, MOVIES_PATH)


def load_artifacts():
    """Load previously trained files. Raises if you have not built the model yet."""
    missing = [
        path.name
        for path in (VECTORIZER_PATH, MATRIX_PATH, MOVIES_PATH)
        if not path.exists()
    ]
    if missing:
        raise FileNotFoundError(
            "Missing model files: "
            + ", ".join(missing)
            + ". Run: python -m app.ml.recommender --build"
        )

    vectorizer = joblib.load(VECTORIZER_PATH)
    tfidf_matrix = joblib.load(MATRIX_PATH)
    movies_index = joblib.load(MOVIES_PATH)
    return vectorizer, tfidf_matrix, movies_index


def find_movie_index(movies_index: pd.DataFrame, title: str) -> int:
    """Return the row number of a movie title, or raise ValueError."""
    query = normalize_title(title)
    if not query:
        raise ValueError("Please enter a movie title.")

    normalized = movies_index["title"].map(normalize_title)
    matches = movies_index.index[normalized == query].tolist()

    if not matches:
        # Practical hint: show a few titles that contain the typed words.
        contains = movies_index.index[normalized.str.contains(query, regex=False)].tolist()
        hint = ""
        if contains:
            examples = ", ".join(movies_index.loc[contains[:5], "title"].tolist())
            hint = f" Did you mean: {examples}?"
        raise ValueError(f'Movie not found: "{title}".{hint}')

    return int(matches[0])


def find_movie_index_by_id(movies_index: pd.DataFrame, movie_id: int) -> int:
    """Return the TF-IDF row number for a TMDB movie_id, or raise ValueError."""
    matches = movies_index.index[movies_index["movie_id"] == int(movie_id)].tolist()
    if not matches:
        raise ValueError(f"Movie not found: {movie_id}")
    return int(matches[0])


def recommend_from_row_index(
    movie_idx: int,
    movies_index: pd.DataFrame,
    tfidf_matrix,
    top_n: int = TOP_N,
    processed: pd.DataFrame | None = None,
) -> pd.DataFrame:
    """
    Shared scoring used by title search and by the FastAPI movie_id endpoint.

    This is the SAME cosine-similarity ranking as before. We only look up the
    movie by a different key (row index), then:
      1. Take that movie's TF-IDF vector (already trained, never refit here).
      2. Compute cosine similarity against all movie vectors.
      3. Sort high -> low, skip the movie itself, return top_n.

    How cosine similarity works:
      Imagine each movie vector as an arrow in high-dimensional space.
      Cosine similarity looks at the ANGLE between two arrows:
        1.0 -> same direction -> very similar tags
        0.0 -> at a right angle -> unrelated tags
    """
    movie_vector = tfidf_matrix[movie_idx]
    scores = cosine_similarity(movie_vector, tfidf_matrix).flatten()
    ranked_indices = scores.argsort()[::-1]

    recommendations = []
    for idx in ranked_indices:
        if idx == movie_idx:
            continue
        rec = {
            "rank": len(recommendations) + 1,
            "movie_id": int(movies_index.loc[idx, "movie_id"]),
            "title": str(movies_index.loc[idx, "title"]),
            "similarity": float(scores[idx]),
            "match_percentage": round(float(scores[idx]) * 100, 1),
        }
        if processed is not None:
            rec["reasons"] = _build_reasons(movie_idx, idx, processed)
        recommendations.append(rec)
        if len(recommendations) >= top_n:
            break

    return pd.DataFrame(recommendations)


def _build_reasons(movie_idx: int, other_idx: int, processed: pd.DataFrame) -> list[str]:
    """Build concise human-readable reasons for a recommendation match."""
    reasons: list[str] = []
    seed_row = processed.iloc[movie_idx]
    other_row = processed.iloc[other_idx]

    def _to_set(value) -> set:
        if not value or (isinstance(value, float) and pd.isna(value)):
            return set()
        return {w.strip().lower() for w in str(value).split() if w.strip()}

    seed_genres = _to_set(seed_row.get("genres"))
    other_genres = _to_set(other_row.get("genres"))
    shared_genres = seed_genres & other_genres
    if shared_genres:
        reasons.append(f"Shared genre: {', '.join(sorted(shared_genres))}")

    seed_keywords = _to_set(seed_row.get("keywords"))
    other_keywords = _to_set(other_row.get("keywords"))
    shared_keywords = seed_keywords & other_keywords
    if shared_keywords:
        reasons.append(f"Shared keyword: {', '.join(sorted(shared_keywords))}")

    seed_director = _to_set(seed_row.get("director"))
    other_director = _to_set(other_row.get("director"))
    shared_director = seed_director & other_director
    if shared_director:
        reasons.append(f"Shared director: {', '.join(sorted(shared_director))}")

    seed_cast = _to_set(seed_row.get("cast"))
    other_cast = _to_set(other_row.get("cast"))
    shared_cast = seed_cast & other_cast
    if shared_cast:
        reasons.append(f"Shared cast: {', '.join(sorted(shared_cast))}")

    return reasons


def recommend_by_title(
    title: str,
    movies_index: pd.DataFrame,
    tfidf_matrix,
    top_n: int = TOP_N,
) -> pd.DataFrame:
    """Recommend movies similar to a title (CLI). Same model as recommend_by_movie_id."""
    movie_idx = find_movie_index(movies_index, title)
    return recommend_from_row_index(movie_idx, movies_index, tfidf_matrix, top_n)


def recommend_by_movie_id(
    movie_id: int,
    movies_index: pd.DataFrame,
    tfidf_matrix,
    processed: pd.DataFrame | None = None,
    top_n: int = TOP_N,
) -> pd.DataFrame:
    """Recommend movies similar to a TMDB movie_id (FastAPI). Same model as CLI."""
    movie_idx = find_movie_index_by_id(movies_index, movie_id)
    return recommend_from_row_index(
        movie_idx, movies_index, tfidf_matrix, top_n=top_n, processed=processed
    )


def build_and_save() -> None:
    print("Loading processed_movies.csv ...")
    df = load_processed_movies()
    print(f"Training TF-IDF on {len(df)} movies ...")
    vectorizer, tfidf_matrix = train_model(df)
    save_artifacts(vectorizer, tfidf_matrix, df)
    print(f"Vocabulary size: {len(vectorizer.get_feature_names_out())}")
    print(f"TF-IDF matrix shape: {tfidf_matrix.shape} (movies x terms)")
    print(f"Saved: {VECTORIZER_PATH.name}, {MATRIX_PATH.name}, {MOVIES_PATH.name}")


def print_recommendations(title: str, recs: pd.DataFrame) -> None:
    print()
    print(f"Recommended movies similar to: {title}")
    print("-" * 40)
    for _, row in recs.iterrows():
        print(f"{int(row['rank'])}. {row['title']}  (score: {row['similarity']:.3f})")
    print()


def run_cli() -> None:
    """Ask for a movie title in the terminal. Type quit to exit."""
    _vectorizer, tfidf_matrix, movies_index = load_artifacts()
    print("SmartChoice recommender is ready.")
    print("Type a movie title, or 'quit' to exit.")

    while True:
        try:
            title = input("\nEnter a movie title: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye.")
            break

        if title.lower() in {"quit", "exit", "q"}:
            print("Goodbye.")
            break

        try:
            recs = recommend_by_title(title, movies_index, tfidf_matrix)
        except ValueError as error:
            print(error)
            continue

        print_recommendations(title, recs)


def run_batch_titles(titles: list[str]) -> None:
    """Non-interactive test: print recommendations for each title."""
    _vectorizer, tfidf_matrix, movies_index = load_artifacts()
    for title in titles:
        try:
            recs = recommend_by_title(title, movies_index, tfidf_matrix)
        except ValueError as error:
            print(error)
            print()
            continue
        print_recommendations(title, recs)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="SmartChoice content-based movie recommender"
    )
    parser.add_argument(
        "--build",
        action="store_true",
        help="Train TF-IDF and save joblib artifacts, then exit",
    )
    parser.add_argument(
        "--movie",
        action="append",
        dest="movies",
        help="Recommend for this title (can be repeated). Skips the interactive prompt.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)

    if args.build:
        build_and_save()
        return 0

    if not VECTORIZER_PATH.exists():
        print("No saved model found. Training once before recommendations ...")
        build_and_save()
        print()

    if args.movies:
        run_batch_titles(args.movies)
        return 0

    run_cli()
    return 0


if __name__ == "__main__":
    sys.exit(main())
