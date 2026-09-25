"use client";

import { useEffect, useState, useCallback } from "react";
import {
  getRecommendations,
  getMovieMetadataBatch,
  type RecommendationMovie,
  type MovieMetadata,
} from "@/lib/api";
import MovieCard from "@/components/MovieCard";

interface SimilarMoviesContentProps {
  movieId: number;
  movieTitle: string;
}

interface ParsedReason {
  label: string;
  value: string;
}

function parseReason(reason: string): ParsedReason | null {
  const idx = reason.indexOf(": ");
  if (idx === -1) return null;
  return {
    label: reason.slice(0, idx),
    value: reason.slice(idx + 2),
  };
}

export default function SimilarMoviesContent({
  movieId,
  movieTitle,
}: SimilarMoviesContentProps) {
  const [recommendations, setRecommendations] = useState<RecommendationMovie[]>([]);
  const [metadataMap, setMetadataMap] = useState<Map<number, MovieMetadata | null>>(new Map());
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchSimilar = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const recs = await getRecommendations(movieId);
      setRecommendations(recs);

      const movieIds = recs.map((r) => r.movie_id);
      const metadata = await getMovieMetadataBatch(movieIds);
      setMetadataMap(metadata);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load recommendations");
    } finally {
      setLoading(false);
    }
  }, [movieId]);

  // Automatically fetch recommendations when page loads
  useEffect(() => {
    fetchSimilar();
  }, [fetchSimilar]);

  return (
    <div>
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 mb-6">
        <div>
          <div className="flex items-center gap-3">
            <div className="w-1 h-7 rounded-full bg-accent-gold" />
            <h2 className="text-2xl font-bold text-text-primary">
              Similar Movies
            </h2>
          </div>
          <p className="text-xs text-text-muted mt-1 ml-4">
            AI recommendations matched by plot keywords and themes for &ldquo;{movieTitle}&rdquo;
          </p>
        </div>

        <span className="text-[10px] font-bold uppercase tracking-wider text-accent-gold px-3 py-1 rounded-full bg-accent-gold/15 border border-accent-gold/30 self-start sm:self-auto">
          TF-IDF + Cosine Similarity
        </span>
      </div>

      {/* Loading Skeleton */}
      {loading && (
        <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-3">
          {[1, 2, 3].map((n) => (
            <div
              key={n}
              className="rounded-xl border border-border-subtle bg-bg-card p-5 animate-pulse space-y-4"
            >
              <div className="aspect-[2/3] w-full rounded-lg bg-bg-deep" />
              <div className="h-4 bg-border-subtle rounded w-3/4" />
              <div className="h-3 bg-border-subtle rounded w-1/2" />
            </div>
          ))}
        </div>
      )}

      {/* Error state */}
      {error && (
        <div className="rounded-xl border border-red-500/30 bg-red-500/10 p-6 text-center">
          <p className="text-sm text-red-400 mb-3">{error}</p>
          <button
            type="button"
            onClick={fetchSimilar}
            className="inline-flex items-center gap-2 rounded-lg bg-accent-gold px-4 py-2 text-xs font-bold text-bg-deep hover:bg-accent-gold-dim transition-colors"
          >
            Retry Recommendation
          </button>
        </div>
      )}

      {/* Empty State */}
      {!loading && !error && recommendations.length === 0 && (
        <div className="rounded-xl border border-border-subtle bg-bg-card p-8 text-center text-text-muted">
          <p className="text-sm font-medium text-text-primary">No similar movies found</p>
          <p className="text-xs text-text-muted mt-1">Try exploring other titles from the catalog.</p>
        </div>
      )}

      {/* Auto-Loaded Recommendations */}
      {!loading && !error && recommendations.length > 0 && (
        <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-3">
          {recommendations.map((rec) => {
            const parsedReasons = (rec.reasons ?? [])
              .map(parseReason)
              .filter((r): r is ParsedReason => r !== null);

            return (
              <div
                key={rec.movie_id}
                className="group relative flex flex-col rounded-xl border border-border-subtle bg-bg-card transition-all duration-300 hover:border-accent-gold/40 hover:shadow-gold overflow-hidden"
              >
                <div className="p-5 pb-0">
                  <MovieCard movie={rec} metadata={metadataMap.get(rec.movie_id) ?? null} />
                </div>

                <div className="mt-auto border-t border-border-subtle bg-bg-deep/60 px-5 py-4">
                  {rec.match_percentage !== undefined && (
                    <div className="flex items-center justify-between mb-2">
                      <span className="text-[10px] font-semibold uppercase tracking-[0.15em] text-text-muted">
                        SmartChoice Match
                      </span>
                      <span className="text-lg font-bold text-accent-gold">
                        {rec.match_percentage.toFixed(1)}%
                      </span>
                    </div>
                  )}

                  {rec.match_percentage !== undefined && (
                    <div className="h-1.5 w-full rounded-full bg-border-subtle overflow-hidden mb-3">
                      <div
                        className="h-full bg-gradient-to-r from-accent-gold to-accent-gold-dim transition-all duration-500"
                        style={{ width: `${Math.min(rec.match_percentage, 100)}%` }}
                      />
                    </div>
                  )}

                  {parsedReasons.length > 0 && (
                    <div>
                      <p className="text-[10px] font-semibold uppercase tracking-[0.15em] text-text-muted mb-2">
                        Why this movie?
                      </p>
                      <div className="space-y-2">
                        {parsedReasons.map((r, i) => (
                          <div key={i}>
                            <span className="text-[11px] font-semibold uppercase tracking-wide text-accent-gold">
                              {r.label}
                            </span>
                            <p className="text-sm text-text-secondary leading-snug">
                              {r.value}
                            </p>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}