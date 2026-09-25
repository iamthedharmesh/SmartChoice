import Link from "next/link";
import Image from "next/image";
import type { Movie, MovieMetadata, DiscoverMovie } from "@/lib/api";

type MovieCardProps = {
  movie: Movie | DiscoverMovie;
  metadata?: MovieMetadata | null;
  priority?: boolean;
};

function shortOverview(text: string, maxLength = 140): string {
  const clean = (text || "").trim();
  if (clean.length <= maxLength) {
    return clean || "No overview available.";
  }
  return `${clean.slice(0, maxLength).trim()}…`;
}

function formatRating(rating: number | null): string {
  if (rating === null || rating === undefined) return "";
  return rating.toFixed(1);
}

function getGenresDisplay(movie: Movie | DiscoverMovie): string {
  if ("genres" in movie && movie.genres) {
    return movie.genres;
  }
  if ("genre_ids" in movie && movie.genre_ids && movie.genre_ids.length > 0) {
    return movie.genre_ids.join(", ");
  }
  return "No genres listed";
}

export default function MovieCard({ movie, metadata, priority = false }: MovieCardProps) {
  const posterUrl = metadata?.poster_url ?? ("poster_url" in movie ? movie.poster_url : null);
  const releaseYear = metadata?.release_year ?? ("release_year" in movie ? movie.release_year : null);
  const rating = metadata?.rating ?? ("rating" in movie ? movie.rating : null);

  return (
    <Link
      href={`/movie/${movie.movie_id}`}
      className="group block rounded-xl border border-border-subtle bg-bg-card p-5 transition-all duration-300 hover:border-border-glow hover:bg-bg-card-hover card-glow"
      aria-label={`View details for ${movie.title}`}
    >
      <article className="h-full flex flex-col">
        {posterUrl && (
          <div className="relative mb-4 rounded-lg overflow-hidden aspect-[2/3] bg-bg-card-hover">
            <Image
              src={posterUrl}
              alt={`${movie.title} poster`}
              fill
              sizes="(max-width: 640px) 100vw, (max-width: 1024px) 50vw, 25vw"
              className="object-cover transition-transform duration-300 group-hover:scale-105"
              loading={priority ? "eager" : "lazy"}
            />
          </div>
        )}
        {!posterUrl && (
          <div className="mb-4 rounded-lg aspect-[2/3] bg-bg-deep flex flex-col items-center justify-center border border-border-subtle">
            <div className="p-3 rounded-full bg-bg-card-hover border border-border-subtle mb-2">
              <svg className="w-8 h-8 text-text-muted" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
            </div>
            <span className="text-[10px] uppercase tracking-wider text-text-muted font-medium">
              No Poster
            </span>
          </div>
        )}
        <div className="flex-1 flex flex-col">
          <h2 className="text-lg font-semibold text-text-primary group-hover:text-accent-gold transition-colors line-clamp-2">
            {movie.title}
          </h2>
          <div className="mt-2 flex flex-wrap items-center gap-2">
            {releaseYear && (
              <span className="inline-flex items-center gap-1 text-xs text-text-muted px-2 py-0.5 rounded bg-bg-deep/50">
                <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
                {releaseYear}
              </span>
            )}
            {rating !== null && rating !== undefined && (
              <span className="inline-flex items-center gap-1 text-xs font-medium text-amber-400 px-2 py-0.5 rounded bg-amber-400/10">
                <svg className="w-3 h-3 fill-current" viewBox="0 0 24 24" aria-hidden="true">
                  <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z" />
                </svg>
                {formatRating(rating)}
              </span>
            )}
          </div>
          <p className="mt-2 text-sm text-text-muted line-clamp-1">
            {getGenresDisplay(movie)}
          </p>
          <p className="mt-3 flex-1 text-sm leading-relaxed text-text-secondary">
            {shortOverview(movie.overview)}
          </p>
        </div>
        <div className="mt-4 pt-3 border-t border-border-subtle flex items-center justify-between">
          <span className="text-xs text-text-muted uppercase tracking-wider">
            Movie ID: {movie.movie_id}
          </span>
          <svg
            className="w-5 h-5 text-text-muted group-hover:text-accent-gold transition-colors"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
            aria-hidden="true"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M9 5l7 7-7 7"
            />
          </svg>
        </div>
      </article>
    </Link>
  );
}