"use client";

import { useState, useCallback, useEffect, useRef } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import MovieCard from "@/components/MovieCard";
import {
  getMovies,
  getMoviesSearch,
  getMovieMetadataBatch,
  getPopularMovies,
  getTrendingMovies,
  getUpcomingMovies,
  getNowPlayingMovies,
  getDiscoverMovies,
  type Movie,
  type MovieListResponse,
  type MovieMetadata,
  type DiscoverMovie,
  type DiscoverResponse,
} from "@/lib/api";

function HeroSection({ onSearch }: { onSearch: (query: string) => void }) {
  return (
    <section className="relative min-h-[50vh] flex items-center justify-center hero-gradient overflow-hidden">
      <div className="absolute inset-0 bg-gradient-to-b from-transparent via-bg-deep to-bg-deep" />
      <div className="relative z-10 px-4 text-center max-w-4xl mx-auto">
        <div className="animate-fade-in-up">
          <span className="inline-block px-4 py-1.5 rounded-full border border-border-glow/30 bg-border-glow/10 text-accent-gold text-sm font-medium tracking-wider uppercase mb-6">
            Movie Discovery
          </span>
        </div>
        <h1 className="animate-fade-in-up text-5xl md:text-7xl lg:text-8xl font-bold tracking-tight text-text-primary mb-6" style={{ animationDelay: "100ms" }}>
          Movies
        </h1>
        <p className="animate-fade-in-up text-lg md:text-xl lg:text-2xl text-text-secondary max-w-2xl mx-auto mb-10" style={{ animationDelay: "200ms" }}>
          Discover movies tailored to your taste with TF-IDF + cosine similarity recommendations
        </p>
        <div className="animate-fade-in-up flex flex-col sm:flex-row gap-4 justify-center items-center max-w-xl mx-auto" style={{ animationDelay: "300ms" }}>
          <form onSubmit={(e) => { e.preventDefault(); }} className="w-full sm:max-w-md">
            <label htmlFor="hero-search" className="sr-only">Search movies</label>
            <div className="relative search-glow rounded-full bg-bg-card/80 backdrop-blur-sm border border-border-subtle transition-all duration-300 overflow-hidden">
              <input
                id="hero-search"
                type="search"
                placeholder="Search for a movie…"
                className="w-full px-6 py-4 pl-14 text-lg text-text-primary placeholder-text-muted bg-transparent outline-none"
                onKeyDown={(e) => {
                  if (e.key === "Enter") {
                    const target = e.currentTarget as HTMLInputElement;
                    if (target.value.trim()) {
                      onSearch(target.value.trim());
                    }
                  }
                }}
              />
              <svg
                className="absolute left-5 top-1/2 -translate-y-1/2 w-6 h-6 text-text-muted pointer-events-none"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
                aria-hidden="true"
              >
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
            </div>
          </form>
        </div>
        <div className="animate-fade-in-up mt-16 flex items-center justify-center gap-8 text-text-muted" style={{ animationDelay: "400ms" }}>
          <div className="flex items-center gap-2">
            <svg className="w-5 h-5 text-accent-gold" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/></svg>
            <span className="text-sm">TF-IDF + Cosine Similarity</span>
          </div>
          <div className="flex items-center gap-2">
            <svg className="w-5 h-5 text-accent-gold" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8zm-1-13h2v6h-2zm0 8h2v2h-2z"/></svg>
            <span className="text-sm">5000+ Movies</span>
          </div>
          <div className="flex items-center gap-2">
            <svg className="w-5 h-5 text-accent-gold" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true"><path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zM9 17H7v-7h2v7zm4 0h-2V7h2v10zm4 0h-2v-4h2v4z"/></svg>
            <span className="text-sm">Instant Results</span>
          </div>
        </div>
      </div>
    </section>
  );
}

function SearchBar({ onSearch, initialQuery = "" }: { onSearch: (query: string) => void; initialQuery?: string }) {
  const [query, setQuery] = useState(initialQuery);
  const debounceTimer = useRef<NodeJS.Timeout | null>(null);

  const handleChange = useCallback((value: string) => {
    setQuery(value);
    if (debounceTimer.current) clearTimeout(debounceTimer.current);
    debounceTimer.current = setTimeout(() => {
      if (value.trim()) onSearch(value.trim());
    }, 300);
  }, []);

  return (
    <div className="max-w-2xl mx-auto">
      <label htmlFor="search-input" className="sr-only">Search movies</label>
      <div className="relative search-glow rounded-full bg-bg-card/80 backdrop-blur-sm border border-border-subtle transition-all duration-300 overflow-hidden">
        <input
          id="search-input"
          type="search"
          value={query}
          onChange={(e) => handleChange(e.target.value)}
          placeholder="Search movies by title…"
          className="w-full px-6 py-3.5 pl-12 text-base text-text-primary placeholder-text-muted bg-transparent outline-none"
        />
        <svg
          className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-text-muted pointer-events-none"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
          aria-hidden="true"
        >
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
        </svg>
        {query && (
          <button
            type="button"
            onClick={() => { setQuery(""); handleChange(""); }}
            className="absolute right-4 top-1/2 -translate-y-1/2 p-1 text-text-muted hover:text-text-primary transition-colors"
            aria-label="Clear search"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        )}
      </div>
    </div>
  );
}

function MovieGrid({ movies, metadataMap, loading, error, retry }: { movies: (Movie | DiscoverMovie)[]; metadataMap: Map<number, MovieMetadata | null>; loading: boolean; error: string | null; retry: () => void }) {
  if (loading) {
    return (
      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4" role="status" aria-label="Loading movies">
        {Array.from({ length: 8 }).map((_, i) => (
          <div key={i} className="rounded-xl border border-border-subtle bg-bg-card p-5 animate-shimmer">
            <div className="h-6 w-3/4 bg-bg-card-hover rounded mb-2" />
            <div className="h-4 w-1/2 bg-bg-card-hover rounded mb-3" />
            <div className="h-4 w-full bg-bg-card-hover rounded" />
            <div className="h-4 w-5/6 bg-bg-card-hover rounded mt-2" />
          </div>
        ))}
      </div>
    );
  }

  if (error) {
    return (
      <div className="text-center py-12 px-4">
        <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-red-500/20 mb-4">
          <svg className="w-8 h-8 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
          </svg>
        </div>
        <h3 className="text-lg font-semibold text-text-primary mb-2">Failed to load movies</h3>
        <p className="text-text-muted mb-4">{error}</p>
        <button
          onClick={retry}
          className="inline-flex items-center gap-2 px-4 py-2 rounded-lg bg-accent-gold text-bg-deep font-medium hover:bg-accent-gold-dim transition-colors"
        >
          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
          </svg>
          Try Again
        </button>
      </div>
    );
  }

  if (movies.length === 0) {
    return (
      <div className="text-center py-12 px-4">
        <svg className="mx-auto w-16 h-16 text-text-muted/50 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        <h3 className="text-lg font-semibold text-text-primary mb-2">No movies found</h3>
        <p className="text-text-muted">Try adjusting your search or browse popular movies below.</p>
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4" role="list" aria-label="Movie results">
      {movies.map((movie, index) => (
        <div key={movie.movie_id} style={{ animationDelay: `${index * 50}ms` }} className="animate-fade-in-up">
          <MovieCard movie={movie} metadata={metadataMap.get(movie.movie_id) ?? null} priority={index < 4} />
        </div>
      ))}
    </div>
  );
}

const MAX_DISCOVERY_PAGES = 20;

export default function MoviesPage() {
  const router = useRouter();
  const searchParams = useSearchParams();
  
  // Local search state
  const [movies, setMovies] = useState<(Movie | DiscoverMovie)[]>([]);
  const [metadataMap, setMetadataMap] = useState<Map<number, MovieMetadata | null>>(new Map());
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [searchQuery, setSearchQuery] = useState("");
  const [isSearching, setIsSearching] = useState(false);
  
  // Discovery state
  const [discoveryMode, setDiscoveryMode] = useState<"local" | "trending" | "popular" | "upcoming" | "now-playing" | "discover" | "popular-india" | "latest">("local");
  const [discoveryPage, setDiscoveryPage] = useState(1);
  const [totalPages, setTotalPages] = useState(0);
  const [totalResults, setTotalResults] = useState(0);
  
  // Filter state
  const [filters, setFilters] = useState({
    year: "",
    language: "",
    region: "",
    cinema: "",
    with_genres: "",
    vote_average_gte: "",
    sort_by: "popularity.desc",
  });

  const initialQuery = searchParams.get("q") || "";

  const fetchMovies = useCallback(async (page = 1, limit = 20, query?: string) => {
    setLoading(true);
    setError(null);
    try {
      let data: MovieListResponse;
      if (query && query.trim()) {
        data = await getMoviesSearch(query.trim(), limit);
      } else {
        data = await getMovies(page, limit);
      }
      setMovies(data.results);
      
      // Fetch metadata for displayed movies
      const movieIds = data.results.map((m) => m.movie_id);
      const metadata = await getMovieMetadataBatch(movieIds);
      setMetadataMap(metadata);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load movies");
    } finally {
      setLoading(false);
    }
  }, []);

const fetchDiscovery = useCallback(async (
    mode: typeof discoveryMode,
    page: number,
    currentFilters: typeof filters
  ) => {
    const requestId = ++discoveryRequestIdRef.current;

    // Cancel any previous in-flight discovery request
    if (discoveryAbortControllerRef.current) {
      discoveryAbortControllerRef.current.abort();
    }
    const controller = new AbortController();
    discoveryAbortControllerRef.current = controller;
    const signal = controller.signal;

    setLoading(true);
    setError(null);

    try {
      let data: DiscoverResponse;

      const userLanguage = currentFilters.language || "";
      const cinemaParams = getCinemaParams(currentFilters.cinema, userLanguage);

      switch (mode) {
        case "trending":
          data = await getTrendingMovies("week", "en-US", signal);
          break;

        case "popular-india":
          data = await getDiscoverMovies({
            page,
            sort_by: "popularity.desc",
            with_origin_country: "IN",
            region: "IN",
          }, signal);
          break;

        case "latest": {
          const today = new Date();
          const sixMonthsAgo = new Date();
          sixMonthsAgo.setMonth(today.getMonth() - 6);
          const formatDate = (d: Date) => d.toISOString().split("T")[0];
          data = await getDiscoverMovies({
            page,
            sort_by: "primary_release_date.desc",
            primary_release_date_gte: formatDate(sixMonthsAgo),
            primary_release_date_lte: formatDate(today),
            region: "IN",
            with_original_language: currentFilters.language || undefined,
            with_genres: currentFilters.with_genres || undefined,
            vote_average_gte: currentFilters.vote_average_gte
              ? parseFloat(currentFilters.vote_average_gte)
              : undefined,
            ...cinemaParams,
          }, signal);
          break;
        }

        case "popular":
          data = await getPopularMovies(page, {
            sort_by: currentFilters.sort_by || "popularity.desc",
            year: currentFilters.year ? parseInt(currentFilters.year) : undefined,
            with_original_language: currentFilters.language || undefined,
            region: currentFilters.region || undefined,
            with_genres: currentFilters.with_genres || undefined,
            vote_average_gte: currentFilters.vote_average_gte
              ? parseFloat(currentFilters.vote_average_gte)
              : undefined,
            ...cinemaParams,
          }, signal);
          break;

        case "upcoming":
          data = await getUpcomingMovies(page, {
            sort_by: currentFilters.sort_by || "release_date.asc",
            year: currentFilters.year ? parseInt(currentFilters.year) : undefined,
            with_original_language: currentFilters.language || undefined,
            region: currentFilters.region || undefined,
            with_genres: currentFilters.with_genres || undefined,
            vote_average_gte: currentFilters.vote_average_gte
              ? parseFloat(currentFilters.vote_average_gte)
              : undefined,
            ...cinemaParams,
          }, signal);
          break;

        case "now-playing":
          data = await getNowPlayingMovies(page, {
            sort_by: currentFilters.sort_by || "release_date.desc",
            year: currentFilters.year ? parseInt(currentFilters.year) : undefined,
            with_original_language: currentFilters.language || undefined,
            region: currentFilters.region || undefined,
            with_genres: currentFilters.with_genres || undefined,
            vote_average_gte: currentFilters.vote_average_gte
              ? parseFloat(currentFilters.vote_average_gte)
              : undefined,
            ...cinemaParams,
          }, signal);
          break;

        case "discover":
          data = await getDiscoverMovies({
            page,
            sort_by: currentFilters.sort_by,
            year: currentFilters.year
              ? parseInt(currentFilters.year)
              : undefined,
            with_original_language: currentFilters.language || undefined,
            region: currentFilters.region || undefined,
            with_genres: currentFilters.with_genres || undefined,
            vote_average_gte: currentFilters.vote_average_gte
              ? parseFloat(currentFilters.vote_average_gte)
              : undefined,
            ...cinemaParams,
          }, signal);
          break;

        default:
          throw new Error("Invalid discovery mode");
      }

      if (requestId !== discoveryRequestIdRef.current) return;

      setError(null);
      setMovies(data.results);
      setTotalPages(data.total_pages);
      setTotalResults(data.total_results);
      setDiscoveryPage(page);

      // Fetch metadata for discovered movies (non-blocking)
      const movieIds = data.results.map((m) => m.movie_id);
      try {
        const metadata = await getMovieMetadataBatch(movieIds);
        if (requestId !== discoveryRequestIdRef.current) return;
        setMetadataMap(metadata);
      } catch {
        if (requestId !== discoveryRequestIdRef.current) return;
        setMetadataMap(new Map(movieIds.map(id => [id, null])));
      }

    } catch (err) {
      if (err instanceof DOMException && err.name === "AbortError") return;
      if (requestId !== discoveryRequestIdRef.current) return;
      setError(
        err instanceof Error
          ? err.message
          : "Failed to load movies"
      );
    } finally {
      if (requestId === discoveryRequestIdRef.current) {
        setLoading(false);
      }
    }
  }, []);

  const handleSearch = useCallback((query: string) => {
    setSearchQuery(query);
    setIsSearching(true);
    setDiscoveryMode("local");
    router.push(`/movies?q=${encodeURIComponent(query)}`, { scroll: false });
    fetchMovies(1, 20, query);
  }, [router, fetchMovies]);

  const handleDiscoveryModeChange = useCallback((mode: typeof discoveryMode) => {
    setDiscoveryMode(mode);
    setDiscoveryPage(1);
    setSearchQuery("");
    setIsSearching(false);
    router.push("/movies", { scroll: false });
    // Use setTimeout to get latest filters state
    setTimeout(() => {
      // We need to read current filters - use a ref or just call with current
      // Since we can't easily get current state here, we'll rely on the fetchDiscovery
      // being called from handleFilterSubmit which has current filters
    }, 0);
    // Actually fetch with current filters by using a ref or just calling
    // The fetchDiscovery will be called from handleFilterSubmit with fresh filters
    // For tab change, we need to fetch with current filters
  }, [router]);

  // We need a way to fetch with current filters - use a ref for filters
  const filtersRef = useRef(filters);
  filtersRef.current = filters;

  // Request generation guard to prevent stale responses overwriting newer requests
  const discoveryRequestIdRef = useRef(0);
  // AbortController to cancel in-flight discovery requests when a new one starts
  const discoveryAbortControllerRef = useRef<AbortController | null>(null);

  const handleDiscoveryModeChangeWithFilters = useCallback((mode: typeof discoveryMode) => {
    setDiscoveryMode(mode);
    setDiscoveryPage(1);
    setSearchQuery("");
    setIsSearching(false);
    router.push("/movies", { scroll: false });
    fetchDiscovery(mode, 1, filtersRef.current);
  }, [router, fetchDiscovery]);

  const handleFilterChange = useCallback((key: keyof typeof filters, value: string) => {
    setFilters(prev => ({ ...prev, [key]: value }));
  }, []);

  // Convert cinema filter to TMDB parameters
  // Only applies cinema's language restriction if user hasn't explicitly selected a language
  const getCinemaParams = useCallback((cinema: string, userLanguage: string) => {
    const baseParams: Record<string, string> = {};
    switch (cinema) {
      case "bollywood":
        baseParams.with_origin_country = "IN";
        if (!userLanguage) baseParams.with_original_language = "hi";
        break;
      case "south-indian":
        baseParams.with_origin_country = "IN";
        if (!userLanguage) baseParams.with_original_language = "ta|te|ml|kn";
        break;
      case "hollywood":
        baseParams.with_origin_country = "US";
        if (!userLanguage) baseParams.with_original_language = "en";
        break;
      case "korean":
        baseParams.with_origin_country = "KR";
        if (!userLanguage) baseParams.with_original_language = "ko";
        break;
      case "japanese":
        baseParams.with_origin_country = "JP";
        if (!userLanguage) baseParams.with_original_language = "ja";
        break;
      case "chinese":
        baseParams.with_origin_country = "CN";
        if (!userLanguage) baseParams.with_original_language = "zh";
        break;
      default:
        break;
    }
    return baseParams;
  }, []);

  const handleFilterSubmit = useCallback(() => {
    setDiscoveryPage(1);
    if (discoveryMode !== "local") {
      fetchDiscovery(discoveryMode, 1, filters);
    }
  }, [discoveryMode, fetchDiscovery, filters]);

  const handlePageChange = useCallback((page: number) => {
    if (page < 1 || page > totalPages) return;
    if (discoveryMode === "local") {
      fetchMovies(page, 20, searchQuery || undefined);
    } else {
      fetchDiscovery(discoveryMode, page, filters);
    }
  }, [discoveryMode, totalPages, searchQuery, fetchMovies, fetchDiscovery, filters]);

  const handleRetry = useCallback(() => {
    if (discoveryMode === "local") {
      fetchMovies(1, 20, searchQuery || undefined);
    } else {
      fetchDiscovery(discoveryMode, 1, filters);
    }
  }, [discoveryMode, fetchMovies, fetchDiscovery, searchQuery, filters]);

  useEffect(() => {
    if (initialQuery) {
      setSearchQuery(initialQuery);
      setIsSearching(true);
      setDiscoveryMode("local");
      fetchMovies(1, 20, initialQuery);
    } else {
      // Default: load local popular movies
      fetchMovies();
    }
  }, [initialQuery, fetchMovies]);

  // Language options for filter
  const languageOptions = [
    { code: "", label: "All Languages" },
  
    // 🇮🇳 Indian Languages
    { code: "hi", label: "Hindi" },
    { code: "ta", label: "Tamil" },
    { code: "te", label: "Telugu" },
    { code: "ml", label: "Malayalam" },
    { code: "kn", label: "Kannada" },
    { code: "bn", label: "Bengali" },
    { code: "mr", label: "Marathi" },
    { code: "pa", label: "Punjabi" },
  
    // 🌎 International Languages
    { code: "en", label: "English" },
    { code: "ko", label: "Korean" },
    { code: "ja", label: "Japanese" },
    { code: "zh", label: "Chinese" },
    { code: "fr", label: "French" },
    { code: "de", label: "German" },
    { code: "es", label: "Spanish" },
    { code: "it", label: "Italian" },
    { code: "pt", label: "Portuguese" },
    { code: "ru", label: "Russian" },
  ];
  const regionOptions = [
    { code: "", label: "All Regions" },
    { code: "US", label: "United States" },
    { code: "IN", label: "India" },
    { code: "GB", label: "United Kingdom" },
    { code: "CA", label: "Canada" },
    { code: "AU", label: "Australia" },
    { code: "DE", label: "Germany" },
    { code: "FR", label: "France" },
    { code: "JP", label: "Japan" },
    { code: "KR", label: "South Korea" },
    { code: "BR", label: "Brazil" },
    { code: "MX", label: "Mexico" },
  ];

  const cinemaOptions = [
    { code: "", label: "All Cinema" },
    { code: "bollywood", label: "Bollywood" },
    { code: "south-indian", label: "South Indian" },
    { code: "hollywood", label: "Hollywood" },
    { code: "korean", label: "Korean" },
    { code: "japanese", label: "Japanese" },
    { code: "chinese", label: "Chinese" },
  ];

  const sortOptions = [
    { value: "popularity.desc", label: "Popularity (High to Low)" },
    { value: "popularity.asc", label: "Popularity (Low to High)" },
    { value: "release_date.desc", label: "Release Date (Newest First)" },
    { value: "release_date.asc", label: "Release Date (Oldest First)" },
    { value: "vote_average.desc", label: "Rating (Highest First)" },
    { value: "vote_average.asc", label: "Rating (Lowest First)" },
    { value: "vote_count.desc", label: "Vote Count (Most Voted)" },
  ];

  const discoveryTabs = [
    {
      id: "trending",
      label: "Trending Now",
      icon: "M13 2L3 14h9l-1 8 10-12h-9l1-8z",
    },
    {
      id: "popular-india",
      label: "Popular in India",
      icon: "M12 2a10 10 0 100 20 10 10 0 000-20zm0 2c1.3 0 2.5.4 3.5 1.1-.7.4-1.6.7-2.5.8-.3-.8-.6-1.4-1-1.9zM8.5 5.1c-.4.6-.7 1.3-.9 2.1-1-.2-1.9-.5-2.7-1A8 8 0 018.5 5.1zM4 10h3.3c0 .7.1 1.4.3 2H4.2c-.1-.6-.2-1.3-.2-2zm.7 4h3.6c.3.8.7 1.5 1.2 2.1A8 8 0 014.7 14zM12 20c-1.2-.8-2.2-2.1-2.8-4h5.6c-.6 1.9-1.6 3.2-2.8 4zm3.5-4c.5-.6.9-1.3 1.2-2.1h3.6a8 8 0 01-4.8 2.1zM20 12h-3.4c.2-.6.3-1.3.3-2H20c0 .7-.1 1.4-.2 2zm-3.1-4c-.2-.8-.5-1.5-.9-2.1A8 8 0 0119.2 8h-2.3z",
    },
    {
      id: "latest",
      label: "Latest Movies",
      icon: "M12 2a10 10 0 100 20 10 10 0 000-20zm1 5h-2v6l5 3 1-1.7-4-2.3V7z",
    },
    {
      id: "popular",
      label: "Popular Movies",
      icon: "M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5",
    },
    {
      id: "upcoming",
      label: "Upcoming",
      icon: "M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8zm-1-13h2v6h-2zm0 8h2v2h-2z",
    },
    {
      id: "now-playing",
      label: "Now Playing",
      icon: "M4 4h16a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2zm0 2v12h16V6H4zm5 6l4 4-4 4V8z",
    },
    {
      id: "discover",
      label: "Discover",
      icon: "M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z",
    },
  ];

  return (
    <div className="min-h-screen bg-bg-deep">
      <HeroSection onSearch={handleSearch} />

      <main className="px-4 py-12 md:py-16">
        <SearchBar onSearch={handleSearch} initialQuery={searchQuery} />

        {/* Discovery Tabs */}
        <nav className="mt-8 mb-6" aria-label="Movie discovery sections">
          <div className="overflow-x-auto pb-2">
            <div className="flex gap-2 min-w-max">
              <button
                onClick={() => handleDiscoveryModeChangeWithFilters("local")}
                className={`whitespace-nowrap px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                  discoveryMode === "local"
                    ? "bg-accent-gold text-bg-deep"
                    : "bg-bg-card text-text-primary hover:bg-bg-card-hover"
                }`}
              >
                Local Catalog
              </button>
              {discoveryTabs.map((tab) => (
                <button
                  key={tab.id}
                  onClick={() => handleDiscoveryModeChangeWithFilters(tab.id as typeof discoveryMode)}
                  className={`whitespace-nowrap px-4 py-2 rounded-lg text-sm font-medium transition-colors flex items-center gap-2 ${
                    discoveryMode === tab.id
                      ? "bg-accent-gold text-bg-deep"
                      : "bg-bg-card text-text-primary hover:bg-bg-card-hover"
                  }`}
                >
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d={tab.icon} />
                  </svg>
                  {tab.label}
                </button>
              ))}
            </div>
          </div>
        </nav>

        {/* Filter Bar (for Discover mode) */}
        {(discoveryMode === "discover" || discoveryMode === "popular" || discoveryMode === "upcoming" || discoveryMode === "now-playing" || discoveryMode === "latest") && (
          <div className="mb-6 p-4 rounded-xl bg-bg-card border border-border-subtle">
            <div className="flex flex-wrap gap-4 items-end">
              <div className="flex-1 min-w-[150px]">
                <label htmlFor="sort-by" className="block text-xs font-medium text-text-muted mb-1">Sort By</label>
                <select
                  id="sort-by"
                  value={filters.sort_by}
                  onChange={(e) => handleFilterChange("sort_by", e.target.value)}
                  className="w-full px-3 py-2 rounded-lg bg-bg-deep border border-border-subtle text-text-primary text-sm focus:outline-none focus:ring-2 focus:ring-accent-gold"
                >
                  {sortOptions.map((opt) => (
                    <option key={opt.value} value={opt.value}>{opt.label}</option>
                  ))}
                </select>
              </div>
              <div className="flex-1 min-w-[150px]">
                <label htmlFor="language" className="block text-xs font-medium text-text-muted mb-1">Language</label>
                <select
                  id="language"
                  value={filters.language}
                  onChange={(e) => handleFilterChange("language", e.target.value)}
                  className="w-full px-3 py-2 rounded-lg bg-bg-deep border border-border-subtle text-text-primary text-sm focus:outline-none focus:ring-2 focus:ring-accent-gold"
                >
                  {languageOptions.map((opt) => (
                    <option key={opt.code} value={opt.code}>{opt.label}</option>
                  ))}
                </select>
              </div>
              <div className="flex-1 min-w-[150px]">
                <label htmlFor="region" className="block text-xs font-medium text-text-muted mb-1">Region</label>
                <select
                  id="region"
                  value={filters.region}
                  onChange={(e) => handleFilterChange("region", e.target.value)}
                  className="w-full px-3 py-2 rounded-lg bg-bg-deep border border-border-subtle text-text-primary text-sm focus:outline-none focus:ring-2 focus:ring-accent-gold"
                >
                  {regionOptions.map((opt) => (
                    <option key={opt.code} value={opt.code}>{opt.label}</option>
                  ))}
                </select>
              </div>
              <div className="flex-1 min-w-[150px]">
                <label htmlFor="cinema" className="block text-xs font-medium text-text-muted mb-1">Cinema</label>
                <select
                  id="cinema"
                  value={filters.cinema}
                  onChange={(e) => handleFilterChange("cinema", e.target.value)}
                  className="w-full px-3 py-2 rounded-lg bg-bg-deep border border-border-subtle text-text-primary text-sm focus:outline-none focus:ring-2 focus:ring-accent-gold"
                >
                  {cinemaOptions.map((opt) => (
                    <option key={opt.code} value={opt.code}>{opt.label}</option>
                  ))}
                </select>
              </div>
              <div className="flex-1 min-w-[120px]">
                <label htmlFor="year" className="block text-xs font-medium text-text-muted mb-1">Year</label>
                <input
                  id="year"
                  type="number"
                  placeholder="e.g. 2024"
                  value={filters.year}
                  onChange={(e) => handleFilterChange("year", e.target.value)}
                  className="w-full px-3 py-2 rounded-lg bg-bg-deep border border-border-subtle text-text-primary text-sm focus:outline-none focus:ring-2 focus:ring-accent-gold"
                  min="1900"
                  max={new Date().getFullYear() + 2}
                />
              </div>
              <div className="flex-1 min-w-[120px]">
                <label htmlFor="rating" className="block text-xs font-medium text-text-muted mb-1">Min Rating</label>
                <input
                  id="rating"
                  type="number"
                  step="0.1"
                  placeholder="e.g. 7.0"
                  value={filters.vote_average_gte}
                  onChange={(e) => handleFilterChange("vote_average_gte", e.target.value)}
                  className="w-full px-3 py-2 rounded-lg bg-bg-deep border border-border-subtle text-text-primary text-sm focus:outline-none focus:ring-2 focus:ring-accent-gold"
                  min="0"
                  max="10"
                />
              </div>
              <div className="flex-1 min-w-[150px]">
                <label htmlFor="genres" className="block text-xs font-medium text-text-muted mb-1">Genre IDs</label>
                <input
                  id="genres"
                  type="text"
                  placeholder="e.g. 28,12,16"
                  value={filters.with_genres}
                  onChange={(e) => handleFilterChange("with_genres", e.target.value)}
                  className="w-full px-3 py-2 rounded-lg bg-bg-deep border border-border-subtle text-text-primary text-sm focus:outline-none focus:ring-2 focus:ring-accent-gold"
                />
              </div>
              <button
                onClick={handleFilterSubmit}
                disabled={loading}
                className="whitespace-nowrap px-4 py-2 rounded-lg bg-accent-gold text-bg-deep font-medium text-sm hover:bg-accent-gold-dim transition-colors disabled:opacity-50 disabled:cursor-not-allowed self-end"
              >
                Apply Filters
              </button>
            </div>
            <p className="mt-3 text-xs text-text-muted">
              <strong>Genre IDs:</strong> 28=Action, 12=Adventure, 16=Animation, 35=Comedy, 80=Crime, 99=Documentary, 18=Drama, 10751=Family, 14=Fantasy, 36=History, 27=Horror, 10402=Music, 9648=Mystery, 10749=Romance, 878=Sci-Fi, 10770=TV Movie, 53=Thriller, 10752=War, 37=Western
            </p>
          </div>
        )}

        <section className="mt-12" aria-labelledby="movies-heading">
          <div className="flex items-center justify-between mb-8">
            <h2 id="movies-heading" className="text-2xl md:text-3xl font-bold text-text-primary">
              {isSearching && searchQuery ? (
                <>
                  Search results for "<span className="text-accent-gold">{searchQuery}</span>"
                </>
              ) : discoveryMode === "local" ? (
                "Popular Movies (Local Catalog)"
              ) : discoveryMode === "trending" ? (
                "Trending Now"
              ) : discoveryMode === "popular" ? (
                "Popular Movies"
              ) : discoveryMode === "upcoming" ? (
                "Upcoming Movies"
              ) : discoveryMode === "now-playing" ? (
                "Now Playing"
              ) : (
                "Discover Movies"
              )}
            </h2>
            <div className="flex items-center gap-4">
              {totalResults > 0 && (
                <span className="text-sm text-text-muted">~{totalResults.toLocaleString()} results</span>
              )}
              {!isSearching && discoveryMode === "local" && (
                <span className="text-sm text-text-muted">Showing {movies.length} movies</span>
              )}
            </div>
          </div>

          <MovieGrid
            movies={movies}
            metadataMap={metadataMap}
            loading={loading}
            error={error}
            retry={handleRetry}
          />

          {/* Helpful hint for unfiltered Discover */}
          {discoveryMode === "discover" && !loading && !error && totalResults > 20000 && (
            <div className="mt-6 p-4 rounded-xl bg-bg-card/60 border border-border-subtle text-center">
              <p className="text-sm text-text-muted">
                Showing the most popular results. Narrow down your search using the filters above —
                <span className="text-text-secondary"> Cinema</span>,{" "}
                <span className="text-text-secondary">Language</span>,{" "}
                <span className="text-text-secondary">Genre</span>,{" "}
                <span className="text-text-secondary">Year</span>, or{" "}
                <span className="text-text-secondary">Minimum Rating</span>.
              </p>
            </div>
          )}

          {/* Pagination for discovery modes */}
          {(discoveryMode !== "local" || isSearching) && totalPages > 1 && (
            <nav className="mt-8 flex items-center justify-center gap-2" aria-label="Pagination">
              <button
                onClick={() => handlePageChange(discoveryPage - 1)}
                disabled={discoveryPage <= 1 || loading}
                className="px-4 py-2 rounded-lg bg-bg-card border border-border-subtle text-text-primary hover:bg-bg-card-hover disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                aria-label="Previous page"
              >
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
                </svg>
              </button>
              <span className="px-4 py-2 text-text-primary">
                Page {discoveryPage} of {Math.min(totalPages, MAX_DISCOVERY_PAGES)}
              </span>
              <button
                onClick={() => handlePageChange(discoveryPage + 1)}
                disabled={discoveryPage >= Math.min(totalPages, MAX_DISCOVERY_PAGES) || loading}
                className="px-4 py-2 rounded-lg bg-bg-card border border-border-subtle text-text-primary hover:bg-bg-card-hover disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                aria-label="Next page"
              >
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                </svg>
              </button>
            </nav>
          )}

          {isSearching && totalPages > 1 && !loading && !error && (
            <nav className="mt-8 flex items-center justify-center gap-2" aria-label="Pagination">
              <button
                onClick={() => handlePageChange(discoveryPage - 1)}
                disabled={discoveryPage <= 1}
                className="px-4 py-2 rounded-lg bg-bg-card border border-border-subtle text-text-primary hover:bg-bg-card-hover disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                aria-label="Previous page"
              >
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
                </svg>
              </button>
              <span className="px-4 py-2 text-text-primary">
                Page {discoveryPage} of {totalPages}
              </span>
              <button
                onClick={() => handlePageChange(discoveryPage + 1)}
                disabled={discoveryPage >= totalPages}
                className="px-4 py-2 rounded-lg bg-bg-card border border-border-subtle text-text-primary hover:bg-bg-card-hover disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                aria-label="Next page"
              >
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                </svg>
              </button>
            </nav>
          )}

          <div className="mt-8">
            {loading && (
              <div className="text-center py-8">
                <div className="inline-flex items-center gap-2 text-text-muted">
                  <svg className="animate-spin h-6 w-6" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                  </svg>
                  <span>Loading movies...</span>
                </div>
              </div>
            )}
          </div>
        </section>

        {!isSearching && discoveryMode === "local" && (
          <section className="mt-20 text-center" aria-labelledby="cta-heading">
            <h3 id="cta-heading" className="text-2xl font-bold text-text-primary mb-4">
              Looking for something specific?
            </h3>
            <p className="text-text-secondary mb-6 max-w-md mx-auto">
              Click any movie to see details and find similar movies powered by our ML recommendation engine.
            </p>
            <div className="flex items-center justify-center gap-4 text-sm text-text-muted">
              <span className="flex items-center gap-1">
                <svg className="w-4 h-4 text-accent-gold" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/></svg>
                TF-IDF Vectorization
              </span>
              <span className="flex items-center gap-1">
                <svg className="w-4 h-4 text-accent-gold" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8zm-1-13h2v6h-2zm0 8h2v2h-2z"/></svg>
                Cosine Similarity
              </span>
              <span className="flex items-center gap-1">
                <svg className="w-4 h-4 text-accent-gold" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true"><path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zM9 17H7v-7h2v7zm4 0h-2V7h2v10zm4 0h-2v-4h2v4z"/></svg>
                Top 10 Recommendations
              </span>
            </div>
          </section>
        )}
      </main>

      <footer className="border-t border-border-subtle py-8 px-4">
        <div className="mx-auto max-w-6xl text-center text-text-muted text-sm">
          <p>SmartChoice — Movie Recommendation System</p>
          <p className="mt-1">Powered by FastAPI + TF-IDF + Cosine Similarity</p>
          <p className="mt-2">TMDB Data © The Movie Database (themoviedb.org)</p>
        </div>
      </footer>
    </div>
  );
}