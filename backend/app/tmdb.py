"""
TMDB Metadata Service for SmartChoice.

Fetches visual metadata (poster, backdrop, rating, release date, runtime)
from The Movie Database API using existing TMDB movie IDs.

This module is independent of the TF-IDF recommendation engine.
"""

import asyncio
import os
import datetime
from pathlib import Path
from typing import Optional
import httpx
from dotenv import load_dotenv

# Load .env from backend directory (parent of app/)
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

TMDB_API_KEY = os.getenv("TMDB_API_KEY")
TMDB_BASE_URL = "https://api.themoviedb.org/3"
TMDB_IMAGE_BASE_URL = "https://image.tmdb.org/t/p"


class TMDBError(Exception):
    """Custom exception for TMDB API errors."""
    pass


import logging
logger = logging.getLogger(__name__)

# Shared HTTP client with connection pooling
_shared_client: httpx.AsyncClient | None = None
# Semaphore to limit concurrent TMDB requests (prevent connection exhaustion)
_tmdb_semaphore = asyncio.Semaphore(5)

async def _get_client() -> httpx.AsyncClient:
    """Get or create the shared HTTP client."""
    global _shared_client
    if _shared_client is None or _shared_client.is_closed:
        _shared_client = httpx.AsyncClient(
            timeout=15.0,
            limits=httpx.Limits(max_connections=10, max_keepalive_connections=5),
        )
    return _shared_client

async def close_client() -> None:
    """Close the shared HTTP client (for app shutdown)."""
    global _shared_client
    if _shared_client and not _shared_client.is_closed:
        await _shared_client.aclose()
        _shared_client = None


async def fetch_movie_metadata(movie_id: int) -> Optional[dict]:
    """
    Fetch movie metadata from TMDB API.

    Args:
        movie_id: TMDB movie ID (matches existing movie_id in dataset)

    Returns:
        Dict with poster_url, backdrop_url, release_date, release_year, rating, runtime
        Returns None if movie not found or API key not configured.
    """
    if not TMDB_API_KEY:
        logger.warning("TMDB_API_KEY not configured, returning None for movie_id=%s", movie_id)
        return None

    url = f"{TMDB_BASE_URL}/movie/{movie_id}"
    params = {"api_key": TMDB_API_KEY, "language": "en-US"}

    try:
        client = await _get_client()
        async with _tmdb_semaphore:
            response = await client.get(url, params=params)

            if response.status_code == 404:
                logger.info("TMDB movie not found: movie_id=%s", movie_id)
                return None

            if response.status_code == 401:
                logger.error("TMDB authentication failed (invalid API key) for movie_id=%s", movie_id)
                return None

            response.raise_for_status()
            data = response.json()

    except httpx.HTTPStatusError as e:
        logger.warning("TMDB HTTP error for movie_id=%s: %s", movie_id, e.response.status_code)
        return None
    except httpx.RequestError as e:
        logger.warning("TMDB request error for movie_id=%s: type=%s repr=%r", movie_id, type(e).__name__, e)
        return None
    except Exception as e:
        logger.warning("TMDB unexpected error for movie_id=%s: type=%s repr=%r", movie_id, type(e).__name__, e)
        return None

    poster_path = data.get("poster_path")
    backdrop_path = data.get("backdrop_path")

    return {
        "movie_id": movie_id,
        "poster_url": f"{TMDB_IMAGE_BASE_URL}/w500{poster_path}" if poster_path else None,
        "backdrop_url": f"{TMDB_IMAGE_BASE_URL}/w1280{backdrop_path}" if backdrop_path else None,
        "release_date": data.get("release_date"),
        "release_year": int(data["release_date"][:4]) if data.get("release_date") else None,
        "rating": data.get("vote_average"),
        "runtime": data.get("runtime"),
    }


async def fetch_multiple_metadata(movie_ids: list[int]) -> dict[int, Optional[dict]]:
    """
    Fetch metadata for multiple movies concurrently with limited concurrency.

    Args:
        movie_ids: List of TMDB movie IDs

    Returns:
        Dict mapping movie_id to metadata dict (or None if not found)
    """
    if not TMDB_API_KEY:
        return {mid: None for mid in movie_ids}

    async def fetch_one(movie_id: int) -> tuple[int, Optional[dict]]:
        url = f"{TMDB_BASE_URL}/movie/{movie_id}"
        params = {"api_key": TMDB_API_KEY, "language": "en-US"}
        try:
            client = await _get_client()
            async with _tmdb_semaphore:
                response = await client.get(url, params=params)
            if response.status_code == 404:
                return movie_id, None
            response.raise_for_status()
            data = response.json()

            poster_path = data.get("poster_path")
            backdrop_path = data.get("backdrop_path")

            return movie_id, {
                "movie_id": movie_id,
                "poster_url": f"{TMDB_IMAGE_BASE_URL}/w500{poster_path}" if poster_path else None,
                "backdrop_url": f"{TMDB_IMAGE_BASE_URL}/w1280{backdrop_path}" if backdrop_path else None,
                "release_date": data.get("release_date"),
                "release_year": int(data["release_date"][:4]) if data.get("release_date") else None,
                "rating": data.get("vote_average"),
                "runtime": data.get("runtime"),
            }
        except Exception as e:
            logger.warning("TMDB metadata error for movie_id=%s: type=%s repr=%r", movie_id, type(e).__name__, e)
            return movie_id, None

    tasks = [fetch_one(mid) for mid in movie_ids]
    results = await asyncio.gather(*tasks)

    return dict(results)


def _map_tmdb_movie(data: dict) -> dict:
    """Map TMDB movie result to clean frontend-friendly structure."""
    poster_path = data.get("poster_path")
    backdrop_path = data.get("backdrop_path")
    release_date = data.get("release_date")
    
    return {
        "movie_id": data.get("id"),
        "title": data.get("title") or data.get("name") or "Unknown",
        "overview": data.get("overview") or "",
        "poster_url": f"{TMDB_IMAGE_BASE_URL}/w500{poster_path}" if poster_path else None,
        "backdrop_url": f"{TMDB_IMAGE_BASE_URL}/w1280{backdrop_path}" if backdrop_path else None,
        "release_date": release_date,
        "release_year": int(release_date[:4]) if release_date else None,
        "rating": data.get("vote_average"),
        "language": data.get("original_language"),
        "genre_ids": data.get("genre_ids", []),
    }


async def _tmdb_get(endpoint: str, **params: dict) -> Optional[dict]:
    """Internal helper to make TMDB API requests with retry for 5xx/429 errors."""

    if not TMDB_API_KEY:
        logger.warning("TMDB_API_KEY not configured")
        return None

    url = f"{TMDB_BASE_URL}{endpoint}"
    # Log the actual request being made (without API key)
    log_params = {k: v for k, v in params.items() if k != "api_key"}
    logger.info("TMDB request: %s params=%s", endpoint, log_params)
    params = {**params, "api_key": TMDB_API_KEY}

    for attempt in range(3):
        try:
            async with _tmdb_semaphore:
                response = await asyncio.to_thread(
                    httpx.get,
                    url,
                    params=params,
                    timeout=20.0,
                )

                if response.status_code == 401:
                    logger.error("TMDB authentication failed (invalid API key)")
                    return None

                # Don't retry 4xx errors (except 429 rate limit)
                if 400 <= response.status_code < 500 and response.status_code != 429:
                    logger.warning(
                        "TMDB HTTP error for %s: %s - %s",
                        endpoint,
                        response.status_code,
                        response.text[:200],
                    )
                    return None

                response.raise_for_status()
                return response.json()

        except httpx.TimeoutException as e:
            logger.warning(
                "TMDB timeout for %s (attempt %d/3): type=%s repr=%r",
                endpoint,
                attempt + 1,
                type(e).__name__,
                e,
            )
            if attempt < 2:
                delay = 1 if attempt == 0 else 2
                await asyncio.sleep(delay)
                continue
            logger.error("TMDB timeout for %s after 3 attempts - returning 503 to caller", endpoint)
            return None

        except httpx.HTTPStatusError as e:
            status = e.response.status_code

            # Retry on 5xx errors AND 429 (rate limit)
            if (status >= 500 or status == 429) and attempt < 2:
                delay = 1 if attempt == 0 else 2

                logger.warning(
                    "TMDB HTTP %s for %s, retrying in %ds (attempt %d/3): type=%s repr=%r body=%s",
                    status,
                    endpoint,
                    delay,
                    attempt + 1,
                    type(e).__name__,
                    e,
                    e.response.text[:200] if e.response.text else "no response body",
                )

                await asyncio.sleep(delay)
                continue

            logger.warning(
                "TMDB HTTP error for %s: %s - %s (type=%s repr=%r)",
                endpoint,
                status,
                e.response.text[:200] if e.response.text else "no response body",
                type(e).__name__,
                e,
            )
            return None

        except httpx.ConnectError as e:
            # Specific: connection failed (DNS, refused, etc.)
            if attempt < 2:
                delay = 1 if attempt == 0 else 2
                logger.warning(
                    "TMDB ConnectError for %s (attempt %d/3): type=%s repr=%r",
                    endpoint,
                    attempt + 1,
                    type(e).__name__,
                    e,
                )
                await asyncio.sleep(delay)
                continue
            logger.error(
                "TMDB ConnectError for %s after 3 attempts: type=%s repr=%r",
                endpoint,
                type(e).__name__,
                e,
            )
            return None

        except httpx.ReadError as e:
            # Specific: read timeout / incomplete response
            if attempt < 2:
                delay = 1 if attempt == 0 else 2
                logger.warning(
                    "TMDB ReadError for %s (attempt %d/3): type=%s repr=%r",
                    endpoint,
                    attempt + 1,
                    type(e).__name__,
                    e,
                )
                await asyncio.sleep(delay)
                continue
            logger.error(
                "TMDB ReadError for %s after 3 attempts: type=%s repr=%r",
                endpoint,
                type(e).__name__,
                e,
            )
            return None

        except httpx.RequestError as e:
            # Generic httpx request error (covers others not caught above)
            if attempt < 2:
                delay = 1 if attempt == 0 else 2
                logger.warning(
                    "TMDB RequestError for %s (attempt %d/3): type=%s repr=%r",
                    endpoint,
                    attempt + 1,
                    type(e).__name__,
                    e,
                )
                await asyncio.sleep(delay)
                continue
            logger.error(
                "TMDB RequestError for %s after 3 attempts: type=%s repr=%r",
                endpoint,
                type(e).__name__,
                e,
            )
            return None

        except Exception as e:
            logger.exception(
                "TMDB unexpected error for %s: type=%s repr=%r",
                endpoint,
                type(e).__name__,
                e,
            )
            return None

    return None


async def fetch_popular_movies(page: int = 1, language: str = "en-US", region: Optional[str] = None) -> Optional[dict]:
    """Fetch popular movies from TMDB."""
    params = {"page": page, "language": language}
    if region:
        params["region"] = region
    return await _tmdb_get("/discover/movie", **params)


async def fetch_trending_movies(time_window: str = "week", language: str = "en-US") -> Optional[dict]:
    """Fetch trending movies from TMDB. time_window: 'day' or 'week'."""
    params = {"language": language}
    return await _tmdb_get(f"/trending/movie/{time_window}", **params)


async def fetch_upcoming_movies(page: int = 1, language: str = "en-US", region: Optional[str] = None,
                                with_original_language: Optional[str] = None,
                                with_genres: Optional[str] = None,
                                vote_average_gte: Optional[float] = None,
                                year: Optional[int] = None,
                                with_origin_country: Optional[str] = None) -> Optional[dict]:
    """Fetch upcoming movies from TMDB using /discover/movie with primary_release_date filter."""
    today = datetime.date.today().isoformat()
    params = {
        "page": page,
        "sort_by": "primary_release_date.asc",
        "primary_release_date.gte": today,
        "language": language,
    }
    if region:
        params["region"] = region
    if with_original_language:
        params["with_original_language"] = with_original_language
    if with_genres:
        params["with_genres"] = with_genres
    if vote_average_gte is not None:
        params["vote_average.gte"] = vote_average_gte
    if year:
        params["year"] = year
    if with_origin_country:
        params["with_origin_country"] = with_origin_country
    return await _tmdb_get("/discover/movie", **params)


async def fetch_now_playing_movies(page: int = 1, language: str = "en-US", region: Optional[str] = None,
                                   with_original_language: Optional[str] = None,
                                   with_genres: Optional[str] = None,
                                   vote_average_gte: Optional[float] = None,
                                   year: Optional[int] = None,
                                   with_origin_country: Optional[str] = None) -> Optional[dict]:
    """Fetch now playing movies from TMDB using /discover/movie with primary_release_date filter."""
    today = datetime.date.today().isoformat()
    thirty_days_ago = (datetime.date.today() - datetime.timedelta(days=30)).isoformat()
    params = {
        "page": page,
        "sort_by": "primary_release_date.desc",
        "primary_release_date.lte": today,
        "primary_release_date.gte": thirty_days_ago,
        "language": language,
    }
    if region:
        params["region"] = region
    if with_original_language:
        params["with_original_language"] = with_original_language
    if with_genres:
        params["with_genres"] = with_genres
    if vote_average_gte is not None:
        params["vote_average.gte"] = vote_average_gte
    if year:
        params["year"] = year
    if with_origin_country:
        params["with_origin_country"] = with_origin_country
    return await _tmdb_get("/discover/movie", **params)


async def discover_movies(
    page: int = 1,
    sort_by: str = "popularity.desc",
    year: Optional[int] = None,
    primary_release_year: Optional[int] = None,
    release_date_gte: Optional[str] = None,
    release_date_lte: Optional[str] = None,
    primary_release_date_gte: Optional[str] = None,
    primary_release_date_lte: Optional[str] = None,
    language: Optional[str] = None,
    region: Optional[str] = None,
    with_original_language: Optional[str] = None,
    with_genres: Optional[str] = None,
    vote_average_gte: Optional[float] = None,
    include_adult: bool = False,
    include_video: bool = False,
    with_watch_providers: Optional[str] = None,
    watch_region: Optional[str] = None,
    with_origin_country: Optional[str] = None,
) -> Optional[dict]:
    """
    Discover movies with TMDB's /discover/movie endpoint.
    
    Args:
        page: Page number (1-500)
        sort_by: Sort order (e.g., 'popularity.desc', 'release_date.desc', 'vote_average.desc', 'vote_count.desc')
        year: Filter by release year
        primary_release_year: Filter by primary release year
        release_date_gte: Release date greater than or equal (YYYY-MM-DD)
        release_date_lte: Release date less than or equal (YYYY-MM-DD)
        primary_release_date_gte: Primary release date greater than or equal (YYYY-MM-DD)
        primary_release_date_lte: Primary release date less than or equal (YYYY-MM-DD)
        language: Language code (e.g., 'en', 'hi', 'ta', 'te', 'ml', 'kn', 'bn', 'ko', 'ja')
        region: Region code (e.g., 'US', 'IN')
        with_original_language: Filter by original language (ISO 639-1)
        with_genres: Comma-separated genre IDs
        vote_average_gte: Minimum vote average (0-10)
        include_adult: Include adult movies
        include_video: Include videos
        with_watch_providers: Watch provider IDs
        watch_region: Region for watch providers
        with_origin_country: Filter by origin country (ISO 3166-1, e.g., 'IN' for India)
    """
    params = {
        "page": page,
        "sort_by": sort_by,
        "include_adult": str(include_adult).lower(),
        "include_video": str(include_video).lower(),
    }
    
    if year:
        params["year"] = year
    if primary_release_year:
        params["primary_release_year"] = primary_release_year
    if release_date_gte:
        params["release_date.gte"] = release_date_gte
    if release_date_lte:
        params["release_date.lte"] = release_date_lte
    if primary_release_date_gte:
        params["primary_release_date.gte"] = primary_release_date_gte
    if primary_release_date_lte:
        params["primary_release_date.lte"] = primary_release_date_lte
    if language:
        params["language"] = language
    if region:
        params["region"] = region
    if with_original_language:
        params["with_original_language"] = with_original_language
    if with_genres:
        params["with_genres"] = with_genres
    if vote_average_gte is not None:
        params["vote_average.gte"] = vote_average_gte
    if with_watch_providers:
        params["with_watch_providers"] = with_watch_providers
    if watch_region:
        params["watch_region"] = watch_region
    if with_origin_country:
        params["with_origin_country"] = with_origin_country

    return await _tmdb_get("/discover/movie", **params)


async def fetch_tmdb_movie_details(movie_id: int) -> Optional[dict]:
    """
    Fetch full movie details from TMDB including credits (cast, crew).
    
    Args:
        movie_id: TMDB movie ID
        
    Returns:
        Dict with full movie details or None if not found
    """
    if not TMDB_API_KEY:
        logger.warning("TMDB_API_KEY not configured")
        return None

       # Fetch movie details with append_to_response for credits
    data: Optional[dict] = None

    data = await _tmdb_get(
        f"/movie/{movie_id}",
        language="en-US",
        append_to_response="credits,similar",
    )

    if data is None:
        logger.info("TMDB movie not found: movie_id=%s", movie_id)
        return None

# Extract basic movie info
    # Extract basic movie info
    poster_path = data.get("poster_path")
    backdrop_path = data.get("backdrop_path")
    release_date = data.get("release_date")
    genres = data.get("genres", [])
    production_countries = data.get("production_countries", [])
    
    # Extract credits
    credits = data.get("credits", {})
    cast = credits.get("cast", [])
    crew = credits.get("crew", [])
    
    # Get top billed cast (first 10)
    main_cast = [
        {
            "name": member.get("name"),
            "character": member.get("character"),
            "profile_path": member.get("profile_path"),
            "order": member.get("order"),
        }
        for member in cast[:10]
    ]
    
    # Get director(s)
    directors = [
        {"name": member.get("name"), "job": member.get("job")}
        for member in crew
        if member.get("job") == "Director"
    ]
    
    # Get writers (screenplay, writer, etc.)
    writers = [
        {"name": member.get("name"), "job": member.get("job")}
        for member in crew
        if member.get("job") in ("Screenplay", "Writer", "Novel", "Characters")
    ]
    
    # Get key crew
    key_crew = [
        {"name": member.get("name"), "job": member.get("job")}
        for member in crew
        if member.get("job") in (
            "Producer", "Executive Producer", "Co-Producer",
            "Director of Photography", "Editor", "Original Music Composer",
            "Production Designer", "Costume Designer"
        )
    ]

    # Extract similar movies from TMDB response
    similar_raw = data.get("similar", {})
    similar_movies_raw = similar_raw.get("results", [])

    # Get the current movie's language and origin for filtering
    current_language = data.get("original_language") or ""
    current_country_codes = {
        c.get("iso_3166_1") for c in production_countries
        if c.get("iso_3166_1")
    }

    # Try TMDB Discover with explicit language + origin country filtering.
    # The /similar endpoint returns globally-similar movies regardless of
    # the source movie's language, so Discover gives us proper same-language
    # + same-country results for TMDB-only movies.
    discover_params = {
        "page": 1,
        "sort_by": "popularity.desc",
        "language": "en-US",
    }
    if current_language:
        discover_params["with_original_language"] = current_language
    if current_country_codes:
        discover_params["with_origin_country"] = ",".join(sorted(current_country_codes))

    discover_result = await _tmdb_get("/discover/movie", **discover_params)
    discover_results = (discover_result or {}).get("results", [])

    # Use Discover results when available; otherwise fall back to /similar
    source_results = discover_results if discover_results else similar_movies_raw

    # Exclude the currently viewed movie and remove duplicates
    seen_ids: set = set()
    seen_ids.add(movie_id)
    unique_results = []
    for sm in source_results:
        sid = sm.get("id")
        if sid is None or sid in seen_ids:
            continue
        seen_ids.add(sid)
        unique_results.append(sm)
        if len(unique_results) >= 10:
            break

    similar_movies = []
    for sm in unique_results:
        similar_movies.append({
            "movie_id": sm.get("id"),
            "title": sm.get("title") or sm.get("name") or "Unknown",
            "overview": sm.get("overview") or "",
            "poster_url": f"{TMDB_IMAGE_BASE_URL}/w500{sm.get('poster_path')}" if sm.get("poster_path") else None,
            "backdrop_url": f"{TMDB_IMAGE_BASE_URL}/w1280{sm.get('backdrop_path')}" if sm.get("backdrop_path") else None,
            "release_date": sm.get("release_date"),
            "release_year": int(sm["release_date"][:4]) if sm.get("release_date") else None,
            "rating": sm.get("vote_average"),
            "runtime": sm.get("runtime"),
            "genres": [g.get("name") for g in sm.get("genres", []) if g.get("name")],
            "original_language": sm.get("original_language"),
            "production_countries": [c.get("name") for c in sm.get("production_countries", []) if c.get("name")],
        })

    return {
        "movie_id": movie_id,
        "title": data.get("title") or data.get("name") or "Unknown",
        "overview": data.get("overview") or "",
        "poster_url": f"{TMDB_IMAGE_BASE_URL}/w500{poster_path}" if poster_path else None,
        "backdrop_url": f"{TMDB_IMAGE_BASE_URL}/w1280{backdrop_path}" if backdrop_path else None,
        "release_date": release_date,
        "release_year": int(release_date[:4]) if release_date else None,
        "rating": data.get("vote_average"),
        "runtime": data.get("runtime"),
        "genres": [g.get("name") for g in genres if g.get("name")],
        "original_language": data.get("original_language"),
        "production_countries": [c.get("name") for c in production_countries if c.get("name")],
        "cast": main_cast,
        "directors": directors,
        "writers": writers,
        "key_crew": key_crew,
        "similar_movies": similar_movies,
    }