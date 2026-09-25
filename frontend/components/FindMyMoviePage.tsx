"use client";

import { useState } from "react";
import Link from "next/link";
import Image from "next/image";
import { getPreferenceRecommendations, getMovieMetadataBatch, type PreferenceRecommendation, type MovieMetadata } from "@/lib/api";

const GENRES = [
  "Action", "Adventure", "Animation", "Comedy", "Crime", "Documentary",
  "Drama", "Family", "Fantasy", "History", "Horror", "Music",
  "Mystery", "Romance", "Science Fiction", "Thriller", "War", "Western",
];

const LANGUAGES = [
  { code: "", label: "Any Language" },
  { code: "hi", label: "Hindi" },
  { code: "en", label: "English" },
  { code: "ta", label: "Tamil" },
  { code: "te", label: "Telugu" },
  { code: "ml", label: "Malayalam" },
  { code: "kn", label: "Kannada" },
  { code: "bn", label: "Bengali" },
  { code: "mr", label: "Marathi" },
  { code: "pa", label: "Punjabi" },
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

const RATINGS = [
  { value: null, label: "Any" },
  { value: 6, label: "6+" },
  { value: 7, label: "7+" },
  { value: 8, label: "8+" },
];

const ERAS = [
  { value: null, label: "Any Era", from: null, to: null },
  { value: 2020, label: "2020s", from: 2020, to: 2029 },
  { value: 2010, label: "2010s", from: 2010, to: 2019 },
  { value: 2000, label: "2000s", from: 2000, to: 2009 },
  { value: 1900, label: "1990s & Earlier", from: null, to: 1999 },
];

const PRIORITIES = [
  { value: "story", label: "Story" },
  { value: "rating", label: "Rating" },
  { value: "popularity", label: "Popularity" },
  { value: "recency", label: "Recency" },
];

export default function FindMyMoviePage() {
  const [selectedGenres, setSelectedGenres] = useState<string[]>([]);
  const [language, setLanguage] = useState("");
  const [minRating, setMinRating] = useState<number | null>(null);
  const [era, setEra] = useState<number | null>(null);
  const [priority, setPriority] = useState("story");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [results, setResults] = useState<PreferenceRecommendation[]>([]);
  const [metadataMap, setMetadataMap] = useState<Map<number, MovieMetadata | null>>(new Map());
  const [metadataLoading, setMetadataLoading] = useState(false);
  const [searched, setSearched] = useState(false);

  const toggleGenre = (genre: string) => {
    setSelectedGenres((prev) =>
      prev.includes(genre) ? prev.filter((g) => g !== genre) : [...prev, genre]
    );
  };

  const eraObj = ERAS.find((e) => e.value === era);

  const handleFind = async () => {
    if (selectedGenres.length === 0) {
      setError("Please select at least one genre.");
      return;
    }
    setLoading(true);
    setError(null);
    setSearched(true);
    try {
      const res = await getPreferenceRecommendations({
        genres: selectedGenres,
        language: language || null,
        min_rating: minRating,
        year_from: eraObj?.from ?? null,
        year_to: eraObj?.to ?? null,
        priority,
        limit: 10,
      });
      setResults(res.recommendations);
      const movieIds = res.recommendations.map((r) => r.movie_id);
      if (movieIds.length > 0) {
        setMetadataLoading(true);
        try {
          const metadata = await getMovieMetadataBatch(movieIds);
          setMetadataMap(metadata);
        } finally {
          setMetadataLoading(false);
        }
      } else {
        setMetadataMap(new Map());
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load recommendations");
      setResults([]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="mx-auto max-w-6xl px-4 py-10">
      <header className="mb-10">
        <div className="hero-gradient rounded-2xl border border-border-subtle px-6 py-8 sm:px-8 sm:py-10">
          <div className="max-w-2xl">
            <h1 className="animate-fade-in-up text-3xl sm:text-4xl font-bold tracking-tight text-gradient-gold">
              Find Your Perfect Movie
            </h1>
            <p className="mt-3 text-base sm:text-lg text-text-secondary">
              Tell SmartChoice what you are in the mood for, and we will find movies that match your taste.
            </p>
            <p className="mt-2 text-xs sm:text-sm text-text-muted">
              Powered by TF-IDF story similarity + hybrid preference scoring
            </p>
          </div>
        </div>
      </header>

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
        <div className="lg:col-span-1">
          <FindForm selectedGenres={selectedGenres} language={language} minRating={minRating} era={era} priority={priority} loading={loading} toggleGenre={toggleGenre} setLanguage={setLanguage} setMinRating={setMinRating} setEra={setEra} setPriority={setPriority} handleFind={handleFind} />
        </div>
        <div className="lg:col-span-2">
          <ResultsSection results={results} loading={loading} error={error} searched={searched} metadataMap={metadataMap} metadataLoading={metadataLoading} selectedGenres={selectedGenres} language={language} minRating={minRating} era={era} priority={priority} />
        </div>
      </div>
    </div>
  );
}interface FindFormProps {
  selectedGenres: string[];
  language: string;
  minRating: number | null;
  era: number | null;
  priority: string;
  loading: boolean;
  toggleGenre: (genre: string) => void;
  setLanguage: (value: string) => void;
  setMinRating: (value: number | null) => void;
  setEra: (value: number | null) => void;
  setPriority: (value: string) => void;
  handleFind: () => void;
}

interface ResultsSectionProps {
  results: PreferenceRecommendation[];
  loading: boolean;
  error: string | null;
  searched: boolean;
  metadataMap: Map<number, MovieMetadata | null>;
  metadataLoading: boolean;
  selectedGenres: string[];
  language: string;
  minRating: number | null;
  era: number | null;
  priority: string;
}

function FindForm({ selectedGenres, language, minRating, era, priority, loading, toggleGenre, setLanguage, setMinRating, setEra, setPriority, handleFind }: FindFormProps) {
  const eraObj = ERAS.find((e) => e.value === era);
  return (
    <div className="rounded-xl border border-border-subtle bg-bg-card p-6">
      <h2 className="text-lg font-semibold text-text-primary mb-4">Preferences</h2>

      <div className="mb-5">
        <label className="block text-xs font-medium text-text-muted uppercase tracking-wider mb-2">Genres</label>
        <div className="flex flex-wrap gap-2">
          {GENRES.map((g) => {
            const active = selectedGenres.includes(g);
            return (
              <button key={g} type="button" onClick={() => toggleGenre(g)} className={"px-3 py-1.5 rounded-full text-xs font-medium border transition-colors " + (active ? "bg-accent-gold/20 border-accent-gold text-accent-gold" : "border-border-subtle bg-bg-deep text-text-secondary hover:border-border-glow")}>
                {g}
              </button>
            );
          })}
        </div>
      </div>

      <div className="mb-5">
        <label className="block text-xs font-medium text-text-muted uppercase tracking-wider mb-2">Language</label>
        <select value={language} onChange={(e) => setLanguage(e.target.value)} className="w-full rounded-lg border border-border-subtle bg-bg-deep px-3 py-2 text-sm text-text-primary focus:outline-none focus:border-accent-gold">
          {LANGUAGES.map((l) => (
            <option key={l.code} value={l.code}>{l.label}</option>
          ))}
        </select>
      </div>

      <div className="mb-5">
        <label className="block text-xs font-medium text-text-muted uppercase tracking-wider mb-2">Minimum Rating</label>
        <div className="flex flex-wrap gap-2">
          {RATINGS.map((r) => {
            const active = minRating === r.value;
            return (
              <button key={r.label} type="button" onClick={() => setMinRating(r.value)} className={"px-3 py-1.5 rounded-full text-xs font-medium border transition-colors " + (active ? "bg-accent-gold/20 border-accent-gold text-accent-gold" : "border-border-subtle bg-bg-deep text-text-secondary hover:border-border-glow")}>
                {r.label}
              </button>
            );
          })}
        </div>
      </div>

      <div className="mb-5">
        <label className="block text-xs font-medium text-text-muted uppercase tracking-wider mb-2">Era</label>
        <div className="flex flex-wrap gap-2">
          {ERAS.map((e) => {
            const active = era === e.value;
            return (
              <button key={e.label} type="button" onClick={() => setEra(e.value)} className={"px-3 py-1.5 rounded-full text-xs font-medium border transition-colors " + (active ? "bg-accent-gold/20 border-accent-gold text-accent-gold" : "border-border-subtle bg-bg-deep text-text-secondary hover:border-border-glow")}>
                {e.label}
              </button>
            );
          })}
        </div>
      </div>

      <div className="mb-6">
        <label className="block text-xs font-medium text-text-muted uppercase tracking-wider mb-2">Priority</label>
        <select value={priority} onChange={(e) => setPriority(e.target.value)} className="w-full rounded-lg border border-border-subtle bg-bg-deep px-3 py-2 text-sm text-text-primary focus:outline-none focus:border-accent-gold">
          {PRIORITIES.map((p) => (
            <option key={p.value} value={p.value}>{p.label}</option>
          ))}
        </select>
      </div>

      <button type="button" onClick={handleFind} disabled={loading} className="w-full rounded-lg bg-accent-gold px-4 py-2.5 text-sm font-semibold text-bg-deep transition-opacity hover:opacity-90 disabled:opacity-50 disabled:cursor-not-allowed">
        {loading ? "Finding..." : "Find My Movie"}
      </button>
    </div>
  );
}
function PreferenceSummary({ selectedGenres, language, minRating, era, priority }: {
  selectedGenres: string[];
  language: string;
  minRating: number | null;
  era: number | null;
  priority: string;
}) {
  const eraLabel = ERAS.find((e) => e.value === era)?.label;
  const priorityLabel = PRIORITIES.find((p) => p.value === priority)?.label ?? priority;

  const chips: { key: string; label: string }[] = [];
  selectedGenres.forEach((g) => chips.push({ key: "genre-" + g, label: g }));
  if (language) {
    const lang = LANGUAGES.find((l) => l.code === language);
    if (lang) chips.push({ key: "lang-" + language, label: lang.label });
  }
  if (minRating !== null) chips.push({ key: "rating", label: minRating + "+" });
  if (eraLabel) chips.push({ key: "era", label: eraLabel });
  chips.push({ key: "priority", label: priorityLabel + " focused" });

  if (chips.length === 0) return null;

  return (
    <div className="mb-4 rounded-xl border border-border-subtle bg-bg-card px-4 py-3">
      <p className="text-xs font-semibold uppercase tracking-wider text-text-muted mb-2">
        Based on your preferences
      </p>
      <div className="flex flex-wrap gap-2">
        {chips.map((chip) => (
          <span key={chip.key} className="inline-flex items-center rounded-full border border-accent-gold/30 bg-accent-gold/10 px-2.5 py-1 text-xs font-medium text-accent-gold">
            {chip.label}
          </span>
        ))}
      </div>
    </div>
  );
}

function HowItWorks() {
  return (
    <div className="mt-6 rounded-xl border border-border-subtle bg-bg-card p-5">
      <h3 className="text-sm font-semibold text-text-primary">How SmartChoice recommends</h3>
      <p className="mt-1 text-sm text-text-secondary">
        Your recommendations combine multiple signals instead of relying on a single rating.
      </p>
      <div className="mt-4 space-y-3">
        <div>
          <p className="text-xs font-semibold text-accent-gold">Story similarity</p>
          <p className="text-xs text-text-muted">
            TF-IDF analyzes movie text such as plot, genres, keywords, cast and director to find movies with similar content.
          </p>
        </div>
        <div className="border-t border-border-subtle" />
        <div>
          <p className="text-xs font-semibold text-accent-gold">Preference scoring</p>
          <p className="text-xs text-text-muted">
            SmartChoice combines story similarity with your selected genre preferences, ratings, popularity and release recency.
          </p>
        </div>
        <div className="border-t border-border-subtle" />
        <div>
          <p className="text-xs font-semibold text-accent-gold">SmartChoice Match</p>
          <p className="text-xs text-text-muted">
            The match percentage represents the weighted preference score used to rank these recommendations.
          </p>
        </div>
      </div>
    </div>
  );
}

function ResultsSection({ results, loading, error, searched, metadataMap, metadataLoading, selectedGenres, language, minRating, era, priority }: ResultsSectionProps) {
  if (loading) {
    return (
      <div className="rounded-xl border border-border-subtle bg-bg-card p-8 text-center">
        <div className="inline-block h-8 w-8 animate-spin rounded-full border-2 border-border-subtle border-t-accent-gold" />
        <p className="mt-3 text-sm text-text-muted">Finding your perfect movie...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="rounded-xl border border-red-500/30 bg-red-500/10 p-6 text-center">
        <p className="text-sm text-red-400">{error}</p>
      </div>
    );
  }

  if (searched && results.length === 0) {
    return (
      <div className="rounded-xl border border-border-subtle bg-bg-card p-8 text-center">
        <p className="text-sm text-text-muted">No recommendations found. Try adjusting your filters.</p>
      </div>
    );
  }

  if (results.length === 0) {
    return (
      <div className="rounded-xl border border-border-subtle bg-bg-card p-8 text-center">
        <p className="text-sm text-text-muted">Select at least one genre and click Find My Movie.</p>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      <div>
        <h2 className="text-lg font-semibold text-text-primary">
          {results.length === 1 ? "1 match for you" : `${results.length} matches for you`}
        </h2>
        <p className="mt-1 text-sm text-text-muted">Ranked using your selected preferences</p>
      </div>
      <PreferenceSummary selectedGenres={selectedGenres} language={language} minRating={minRating} era={era} priority={priority} />
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        {results.map((movie, index) => (
          <div key={movie.movie_id} style={{ animationDelay: `${Math.min(index, 5) * 60}ms` }}>
            <RecommendationCard movie={movie} metadata={metadataMap.get(movie.movie_id) ?? null} metadataLoading={metadataLoading} />
          </div>
        ))}
      </div>
      <HowItWorks />
    </div>
  );
}
function RecommendationCard({ movie, metadata, metadataLoading }: { movie: PreferenceRecommendation; metadata: MovieMetadata | null; metadataLoading: boolean }) {
  const releaseYear = movie.release_date ? movie.release_date.slice(0, 4) : null;
  const matchPct = movie.match_percentage;
  const posterUrl = metadata?.poster_url ?? null;

  return (
    <Link href={"/movie/" + movie.movie_id} className="group block animate-fade-in-up rounded-xl border border-border-subtle bg-bg-card overflow-hidden transition-all duration-300 hover:border-border-glow hover:bg-bg-card-hover card-glow" aria-label={"View details for " + movie.title}>
      <div className="flex gap-4 p-4">
        <div className="relative w-20 shrink-0 aspect-[2/3] rounded-lg overflow-hidden bg-bg-deep border border-border-subtle">
          {metadataLoading ? (
            <div className="animate-shimmer absolute inset-0 bg-gradient-to-r from-bg-card via-bg-card-hover to-bg-card" />
          ) : posterUrl ? (
            <Image src={posterUrl} alt={movie.title + " poster"} fill sizes="80px" className="object-cover" />
          ) : (
            <div className="flex h-full w-full flex-col items-center justify-center gap-1 px-2 text-center">
              <svg className="w-6 h-6 text-text-muted" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
              <span className="text-[9px] uppercase tracking-wider text-text-muted font-medium">No Poster</span>
            </div>
          )}
        </div>
        <div className="min-w-0 flex-1 flex flex-col">
          <div className="flex items-center justify-between gap-2">
            <span className="text-[10px] font-semibold uppercase tracking-[0.15em] text-text-muted">
              SmartChoice Match
            </span>
            <span className="text-lg font-bold text-accent-gold">
              {Math.round(matchPct)}%
            </span>
          </div>
          <div className="mt-1.5 h-1.5 w-full rounded-full bg-border-subtle overflow-hidden">
            <div
              className="h-full bg-gradient-to-r from-accent-gold to-accent-gold-dim transition-all duration-500"
              style={{ width: `${Math.min(Math.max(matchPct, 0), 100)}%` }}
            />
          </div>
          <h3 className="mt-2 truncate text-sm font-semibold text-text-primary group-hover:text-accent-gold transition-colors">
            {movie.title}
          </h3>
          <div className="mt-1 flex flex-wrap items-center gap-2">
            {releaseYear && (
              <span className="text-xs text-text-muted">{releaseYear}</span>
            )}
            {movie.rating !== null && movie.rating !== undefined && (
              <span className="inline-flex items-center gap-1 text-xs font-medium text-amber-400">
                <svg className="w-3 h-3 fill-current" viewBox="0 0 24 24" aria-hidden="true">
                  <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z" />
                </svg>
                {movie.rating.toFixed(1)}
              </span>
            )}
          </div>
          {movie.reasons && movie.reasons.length > 0 && (
            <div className="mt-2 flex flex-wrap gap-1">
              {movie.reasons.slice(0, 3).map((reason, idx) => (
                <span key={idx} className="text-[10px] px-2 py-0.5 rounded-full bg-bg-deep text-text-muted border border-border-subtle">
                  {reason}
                </span>
              ))}
            </div>
          )}
        </div>
      </div>
    </Link>
  );
}
