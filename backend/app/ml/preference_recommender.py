"""SmartChoice "Find My Movie" preference-based recommender.

Reuses the existing TF-IDF matrix for content/story similarity and adds
hybrid scoring on top of genre match, rating, popularity, and recency.

This module does NOT modify recommend_from_row_index() or any existing
recommendation behavior.
"""

from __future__ import annotations

import math
from typing import Optional

import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity


# Default hybrid weights (story/content similarity is the foundation)
DEFAULT_WEIGHTS = {
    "story": 0.40,
    "genre": 0.25,
    "rating": 0.15,
    "popularity": 0.10,
    "recency": 0.10,
}

# Priority -> weight overrides (which factor becomes most important)
PRIORITY_WEIGHTS = {
    "story": {
        "story": 0.55, "genre": 0.20, "rating": 0.10, "popularity": 0.10, "recency": 0.05,
    },
    "rating": {
        "story": 0.25, "genre": 0.15, "rating": 0.40, "popularity": 0.10, "recency": 0.10,
    },
    "popularity": {
        "story": 0.25, "genre": 0.15, "rating": 0.10, "popularity": 0.40, "recency": 0.10,
    },
    "recency": {
        "story": 0.25, "genre": 0.15, "rating": 0.10, "popularity": 0.10, "recency": 0.40,
    },
}


def _normalize_series(values: pd.Series, invert: bool = False) -> pd.Series:
    """Min-max normalize a Series to [0, 1]. Returns 0.5 if all values are equal."""
    vmin, vmax = values.min(), values.max()
    if vmax == vmin:
        return pd.Series(0.5, index=values.index)
    norm = (values - vmin) / (vmax - vmin)
    if invert:
        norm = 1.0 - norm
    return norm


def _extract_release_year(release_date) -> Optional[int]:
    """Parse YYYY-MM-DD release date into an integer year."""
    if not release_date or (isinstance(release_date, float) and pd.isna(release_date)):
        return None
    text = str(release_date).strip()
    if not text:
        return None
    try:
        return int(text[:4])
    except (ValueError, TypeError):
        return None


def _graded_genre_match(genres_field, genre_set: set) -> float:
    """Fraction of selected genres present in a movie's genres (0.0 to 1.0)."""
    if not genre_set:
        return 0.0
    row_genres = {w.strip().lower() for w in str(genres_field or "").split() if w.strip()}
    if not row_genres:
        return 0.0
    matched = genre_set & row_genres
    return len(matched) / len(genre_set)


def _log_pop_norm(popularity_series: pd.Series, pop_min: float, pop_max: float) -> pd.Series:
    """Normalize popularity using log1p and the full dataset's popularity range.

    Result is constrained to [0, 1]. Missing/zero popularity maps to 0.0.
    """
    log_vals = np.log1p(popularity_series.fillna(0.0))
    if pop_max == pop_min:
        return pd.Series(0.0, index=popularity_series.index)
    return (log_vals - np.log1p(pop_min)) / (np.log1p(pop_max) - np.log1p(pop_min))


def _year_recency_norm(year_series: pd.Series, year_min: float, year_max: float) -> pd.Series:
    """Normalize release year so newer years score higher (0.0 to 1.0).

    Missing years map to 0.5. Uses the full dataset's year range, not the
    filtered candidate pool.
    """
    filled = year_series.fillna((year_min + year_max) / 2.0 if year_max > year_min else year_min)
    if year_max == year_min:
        return pd.Series(0.5, index=year_series.index)
    return (filled - year_min) / (year_max - year_min)


def _build_user_vector(
    tfidf_matrix,
    movies_index: pd.DataFrame,
    processed: pd.DataFrame,
    genres: list[str],
    language: Optional[str] = None,
) -> Optional[np.ndarray]:
    """
    Build a user preference TF-IDF vector by averaging the TF-IDF vectors of
    seed movies that match the requested genres (and optional language).

    Returns None when no seed movies can be found.
    """
    genre_set = {g.strip().lower() for g in genres if g and g.strip()}
    if not genre_set:
        return None

    def _row_genres(row) -> set:
        raw = row.get("genres") if hasattr(row, "get") else None
        if raw is None or (isinstance(raw, float) and pd.isna(raw)):
            return set()
        return {w.strip().lower() for w in str(raw).split() if w.strip()}

    genre_col = processed["genres"] if "genres" in processed.columns else None
    lang_col = processed["original_language"] if "original_language" in processed.columns and language else None

    mask = pd.Series(False, index=processed.index)
    for i, row in processed.iterrows():
        row_genres = _row_genres(row)
        if not row_genres:
            continue
        if genre_set & row_genres:
            if lang_col is not None:
                row_lang = str(row.get("original_language") or "").strip().lower()
                if row_lang and row_lang == language.strip().lower():
                    mask[i] = True
            else:
                mask[i] = True

    seed_indices = processed.index[mask].tolist()
    if not seed_indices:
        return None

    seed_vectors = tfidf_matrix[seed_indices]
    user_vector = np.asarray(seed_vectors.mean(axis=0)).flatten()
    return user_vector


def recommend_from_preferences(
    movies: pd.DataFrame,
    tfidf_matrix,
    genres: list[str],
    language: Optional[str] = None,
    min_rating: Optional[float] = None,
    year_from: Optional[int] = None,
    year_to: Optional[int] = None,
    priority: str = "story",
    limit: int = 10,
    exclude_movie_ids: Optional[list] = None,
) -> pd.DataFrame:
    """
    Build a user preference vector from seed movies matching the requested
    genres, then rank all movies by hybrid weighted score.

    Returns a DataFrame with one row per recommendation.
    """
    weights = PRIORITY_WEIGHTS.get(priority, DEFAULT_WEIGHTS)
    exclude_set = set(exclude_movie_ids or [])
    genre_set = {g.strip().lower() for g in genres if g and g.strip()}

    # --- Step 1: build user preference vector from seed movies ---
    user_vector = _build_user_vector(tfidf_matrix, movies, movies, genres, language)

    if user_vector is None:
        return pd.DataFrame()

    # --- Step 2: compute story similarity for all movies ---
    story_scores = cosine_similarity(user_vector.reshape(1, -1), tfidf_matrix).flatten()

    # --- Step 3: apply hard filters ---
    df = movies.copy()
    df["_story"] = story_scores

    if language and "original_language" in df.columns:
        df = df[df["original_language"].fillna("").str.lower() == language.strip().lower()]

    if min_rating is not None and "vote_average" in df.columns:
        df = df[df["vote_average"].fillna(0) >= float(min_rating)]

    if "release_date" in df.columns:
        df["_year"] = df["release_date"].apply(_extract_release_year)
        if year_from is not None:
            df = df[df["_year"].fillna(0) >= int(year_from)]
        if year_to is not None:
            df = df[df["_year"].fillna(9999) <= int(year_to)]

    if exclude_set and "movie_id" in df.columns:
        df = df[~df["movie_id"].isin(exclude_set)]

    if df.empty:
        return pd.DataFrame()

    # --- Step 4: compute normalized scoring components ---
    # Genre match: fraction of selected genres present (graded, not binary).
    df["_genre_match"] = df["genres"].apply(
        lambda g: _graded_genre_match(g, genre_set)
    )

    # Rating: use the TMDB 0-10 scale directly, clamped to [0, 1].
    df["_rating_norm"] = (df["vote_average"].fillna(0.0) / 10.0).clip(lower=0.0, upper=1.0) if "vote_average" in df.columns else 0.5

    # Popularity: log1p then normalize using the FULL local dataset's range.
    if "popularity" in movies.columns:
        pop_all = movies["popularity"].fillna(0.0)
        pop_min = float(pop_all.min())
        pop_max = float(pop_all.max())
        df["_pop_norm"] = _log_pop_norm(df["popularity"].fillna(0.0), pop_min, pop_max)
    else:
        df["_pop_norm"] = 0.5

    # Recency: newer years score higher. Missing years map to 0.5.
    # Year range is taken from the full local dataset, not the filtered pool.
    if "release_date" in movies.columns:
        year_all = movies["release_date"].apply(_extract_release_year)
        year_valid = year_all.dropna()
        year_min = float(year_valid.min()) if not year_valid.empty else 2000.0
        year_max = float(year_valid.max()) if not year_valid.empty else 2024.0
        df["_recency_norm"] = _year_recency_norm(df["_year"], year_min, year_max)
    else:
        df["_recency_norm"] = 0.5

    # --- Step 5: weighted hybrid score ---
    df["_score"] = (
        weights["story"] * df["_story"]
        + weights["genre"] * df["_genre_match"]
        + weights["rating"] * df["_rating_norm"]
        + weights["popularity"] * df["_pop_norm"]
        + weights["recency"] * df["_recency_norm"]
    )

    df = df.sort_values("_score", ascending=False).head(limit)

    # --- Step 6: build explanation ---
    genre_set = {g.strip().lower() for g in genres if g and g.strip()}
    results = []
    for _, row in df.iterrows():
        reasons = _build_preference_reasons(row, genre_set, min_rating, year_from, year_to, priority)
        results.append({
            "movie_id": int(row["movie_id"]),
            "title": str(row["title"]),
            "match_percentage": round(float(row["_score"]) * 100, 1),
            "story_similarity": round(float(row["_story"]), 4),
            "genre_match": round(float(row["_genre_match"]), 4),
            "rating": float(row["vote_average"]) if "vote_average" in row and not pd.isna(row["vote_average"]) else None,
            "popularity": float(row["popularity"]) if "popularity" in row and not pd.isna(row["popularity"]) else None,
            "release_date": str(row["release_date"]) if "release_date" in row and not pd.isna(row.get("release_date")) else None,
            "reasons": reasons,
        })

    return pd.DataFrame(results)


def _build_preference_reasons(
    row: pd.Series,
    genre_set: set,
    min_rating: Optional[float],
    year_from: Optional[int],
    year_to: Optional[int],
    priority: str,
) -> list[str]:
    """Build human-readable explanation strings from actual movie data."""
    reasons = []
    row_genres = {
        w.strip().lower()
        for w in str(row.get("genres") or "").split()
        if w.strip()
    }
    shared = genre_set & row_genres
    if shared:
        reasons.append(
            "Matches your " + " and ".join(sorted(shared)) + " preferences"
        )

    story = float(row.get("_story") or 0)
    if story > 0.3:
        reasons.append("Strong story similarity to your selected preferences")

    rating = row.get("vote_average")
    if rating is not None and not pd.isna(rating) and min_rating is not None:
        if float(rating) >= float(min_rating):
            reasons.append(
                f"Rated {float(rating):.1f}, above your {min_rating:.1f} minimum"
            )

    year = _extract_release_year(row.get("release_date"))
    if year is not None and year_from is not None and year_to is not None:
        if year_from <= year <= year_to:
            reasons.append(f"Released in your preferred era ({year})")
    elif year is not None and year_from is not None and year_to is None:
        if year >= year_from:
            reasons.append(f"Released in or after {year_from}")

    if priority == "rating" and rating is not None and not pd.isna(rating):
        reasons.append(f"Priority: rating ({float(rating):.1f})")
    elif priority == "popularity":
        pop = row.get("popularity")
        if pop is not None and not pd.isna(pop):
            reasons.append(f"Priority: popularity ({float(pop):.0f})")
    elif priority == "recency" and year is not None:
        reasons.append(f"Priority: recency ({year})")
    elif priority == "story" and story > 0.2:
        reasons.append("Priority: story similarity")

    return reasons