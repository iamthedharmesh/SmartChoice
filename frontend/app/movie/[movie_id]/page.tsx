import { Metadata } from "next";
import { notFound } from "next/navigation";
import Link from "next/link";
import Image from "next/image";
import {
  getMovie,
  getMovieMetadata,
  getTmdbMovie,
  type MovieDetail,
  type MovieMetadata,
  type TmdbMovieDetail,
  type TmdbCastMember,
} from "@/lib/api";
import SimilarMoviesContent from "@/components/SimilarMoviesContent";

interface PageProps {
  params: Promise<{ movie_id: string }>;
}

async function isLocalMovie(movieId: number): Promise<boolean> {
  try {
    await getMovie(movieId);
    return true;
  } catch {
    return false;
  }
}

async function getMovieData(movieId: number): Promise<{
  movie: MovieDetail | TmdbMovieDetail;
  metadata: MovieMetadata | null;
  tmdbDetail: TmdbMovieDetail | null;
  source: "local" | "tmdb";
  inLocalDataset: boolean;
}> {
  const localExists = await isLocalMovie(movieId);

  if (localExists) {
    try {
      const [movie, metadata, tmdbDetail] = await Promise.all([
        getMovie(movieId),
        getMovieMetadata(movieId).catch(() => null),
        getTmdbMovie(movieId).catch(() => null),
      ]);
      return { movie, metadata, tmdbDetail, source: "local", inLocalDataset: true };
    } catch {
      // Fall through to TMDB
    }
  }

  try {
    const tmdbMovie = await getTmdbMovie(movieId);
    return { movie: tmdbMovie, metadata: null, tmdbDetail: tmdbMovie, source: "tmdb", inLocalDataset: false };
  } catch {
    notFound();
  }
}

export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
  const { movie_id } = await params;
  const movieId = Number(movie_id);

  const localExists = await isLocalMovie(movieId);
  let title = "Movie";
  let description = "";

  if (localExists) {
    try {
      const movie = await getMovie(movieId);
      title = movie.title;
      description = movie.overview.slice(0, 160);
    } catch {
      const tmdbMovie = await getTmdbMovie(movieId).catch(() => null);
      if (tmdbMovie) {
        title = tmdbMovie.title;
        description = tmdbMovie.overview.slice(0, 160);
      }
    }
  } else {
    const tmdbMovie = await getTmdbMovie(movieId).catch(() => null);
    if (tmdbMovie) {
      title = tmdbMovie.title;
      description = tmdbMovie.overview.slice(0, 160);
    }
  }

  return {
    title: `${title} | SmartChoice`,
    description,
  };
}

export default async function MovieDetailsPage({ params }: PageProps) {
  const { movie_id } = await params;
  const movieId = Number(movie_id);
  const { movie, metadata, tmdbDetail, source, inLocalDataset } = await getMovieData(movieId);

  const isTmdbMovie = source === "tmdb";
  const tmdbMovie = isTmdbMovie ? (movie as TmdbMovieDetail) : null;
  const localMovie = !isTmdbMovie ? (movie as MovieDetail) : null;

  // Use tmdbDetail first so we get high-quality capitalized overview with punctuation
  const backdropUrl = tmdbDetail?.backdrop_url ?? tmdbMovie?.backdrop_url ?? metadata?.backdrop_url;
  const posterUrl = tmdbDetail?.poster_url ?? tmdbMovie?.poster_url ?? metadata?.poster_url;
  const releaseYear = tmdbDetail?.release_year ?? tmdbMovie?.release_year ?? metadata?.release_year;
  const rating = tmdbDetail?.rating ?? tmdbMovie?.rating ?? metadata?.rating;
  const runtime = tmdbDetail?.runtime ?? tmdbMovie?.runtime ?? metadata?.runtime;
  const genres = tmdbDetail?.genres?.join(", ") ?? tmdbMovie?.genres?.join(", ") ?? localMovie?.genres ?? "No genres listed";
  const overview = tmdbDetail?.overview || tmdbMovie?.overview || localMovie?.overview || "No overview available.";
  const originalLanguage = tmdbDetail?.original_language ?? tmdbMovie?.original_language ?? null;
  const productionCountries = tmdbDetail?.production_countries ?? tmdbMovie?.production_countries ?? [];

  const cast = tmdbDetail?.cast ?? [];
  const directors = tmdbDetail?.directors ?? [];
  const writers = tmdbDetail?.writers ?? [];
  const similarMovies = tmdbDetail?.similar_movies ?? [];

  return (
    <main className="mx-auto max-w-6xl px-4 py-8">
      {/* Top Breadcrumb Navigation */}
      <div className="mb-6 flex items-center justify-between">
        <nav className="flex items-center gap-2 text-xs text-text-muted truncate">
          <Link href="/" className="hover:text-text-primary transition-colors">Home</Link>
          <span>/</span>
          <Link href="/movies" className="hover:text-text-primary transition-colors">Movies</Link>
          <span>/</span>
          <span className="text-accent-gold font-medium truncate">{movie.title}</span>
        </nav>

        <div className="flex items-center gap-2">
          <Link
            href="/movies"
            className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg border border-border-subtle bg-bg-deep text-xs font-semibold text-text-secondary hover:text-text-primary hover:border-border-glow transition-all"
          >
            ← Back to Catalog
          </Link>
          <Link
            href="/movies/find"
            className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-accent-gold text-bg-deep text-xs font-bold hover:bg-accent-gold-dim transition-colors"
          >
            Find My Movie
          </Link>
        </div>
      </div>

      {/* Cinematic Hero Backdrop */}
      {backdropUrl && (
        <div className="mb-8 rounded-2xl overflow-hidden aspect-video md:aspect-[21/9] relative border border-border-subtle shadow-2xl">
          <Image
            src={backdropUrl}
            alt={`${movie.title} backdrop`}
            fill
            priority
            className="object-cover brightness-40"
            sizes="100vw"
          />
          <div className="absolute inset-0 bg-gradient-to-t from-bg-deep via-bg-deep/50 to-transparent" />
          <div className="absolute bottom-0 left-0 right-0 p-6 md:p-8">
            <div className="flex flex-col md:flex-row md:items-end gap-6">
              {posterUrl && (
                <div className="relative shrink-0 shadow-2xl rounded-lg overflow-hidden border border-border-subtle">
                  <Image
                    src={posterUrl}
                    alt={`${movie.title} poster`}
                    width={160}
                    height={240}
                    className="object-cover rounded-lg"
                    priority
                  />
                </div>
              )}
              <div className="flex-1">
                <div className="flex flex-wrap items-center gap-2.5 mb-3">
                  <h1 className="text-3xl md:text-4xl font-extrabold text-white tracking-tight">
                    {movie.title}
                  </h1>
                  {releaseYear && (
                    <span className="inline-flex items-center gap-1 px-3 py-1 rounded-full bg-white/10 backdrop-blur text-white text-xs font-semibold border border-white/15">
                      {releaseYear}
                    </span>
                  )}
                  {rating !== null && rating !== undefined && (
                    <span className="inline-flex items-center gap-1 px-3 py-1 rounded-full bg-accent-gold/20 backdrop-blur text-accent-gold text-xs font-bold border border-accent-gold/30">
                      ★ {typeof rating === "number" ? rating.toFixed(1) : rating}
                    </span>
                  )}
                  {runtime && (
                    <span className="inline-flex items-center gap-1 px-3 py-1 rounded-full bg-white/10 backdrop-blur text-white text-xs font-semibold border border-white/15">
                      {runtime} min
                    </span>
                  )}
                </div>
                <p className="text-white/80 text-sm md:text-base max-w-3xl">
                  {genres || "No genres listed"}
                </p>
                {originalLanguage && (
                  <p className="text-white/60 text-xs mt-1">
                    Language: <span className="uppercase font-semibold text-white/80">{originalLanguage}</span>
                  </p>
                )}
              </div>
            </div>
          </div>
        </div>
      )}

      {!backdropUrl && (
        <header className="mb-8 rounded-2xl border border-border-subtle bg-bg-card p-6">
          <div className="flex flex-col md:flex-row gap-6">
            {posterUrl && (
              <Image
                src={posterUrl}
                alt={`${movie.title} poster`}
                width={160}
                height={240}
                className="rounded-lg shadow-xl object-cover shrink-0"
              />
            )}
            <div className="flex-1">
              <h1 className="text-3xl font-bold text-text-primary">{movie.title}</h1>
              <div className="mt-3 flex flex-wrap items-center gap-3">
                {releaseYear && (
                  <span className="text-xs px-2.5 py-1 rounded-full bg-bg-deep border border-border-subtle text-text-secondary">
                    {releaseYear}
                  </span>
                )}
                {rating !== null && rating !== undefined && (
                  <span className="text-xs px-2.5 py-1 rounded-full bg-accent-gold/15 text-accent-gold font-bold border border-accent-gold/30">
                    ★ {typeof rating === "number" ? rating.toFixed(1) : rating}
                  </span>
                )}
                {runtime && (
                  <span className="text-xs px-2.5 py-1 rounded-full bg-bg-deep border border-border-subtle text-text-secondary">
                    {runtime} min
                  </span>
                )}
              </div>
              <p className="mt-3 text-sm text-text-secondary">{genres || "No genres listed"}</p>
            </div>
          </div>
        </header>
      )}

      <article className="space-y-10">
        {/* Overview + Movie Information Grid */}
        <section className="grid grid-cols-1 lg:grid-cols-[1.5fr_1fr] gap-6">
          {/* Overview with Pristine Formatting */}
          <div className="rounded-2xl border border-border-subtle bg-bg-card p-6 md:p-8">
            <div className="flex items-center gap-3 mb-5">
              <div className="w-1 h-7 rounded-full bg-accent-gold" />
              <h2 className="text-2xl font-bold text-text-primary">
                Overview
              </h2>
            </div>
            <p className="text-base text-text-secondary leading-relaxed whitespace-pre-wrap">
              {overview || "No overview available."}
            </p>
          </div>

          {/* Balanced Movie Information Card */}
          <div className="rounded-2xl border border-border-subtle bg-bg-card p-6 md:p-8">
            <div className="flex items-center gap-3 mb-6">
              <div className="w-1 h-7 rounded-full bg-accent-gold" />
              <h2 className="text-2xl font-bold text-text-primary">
                Movie Information
              </h2>
            </div>

            <div className="grid grid-cols-2 gap-3">
              {releaseYear && (
                <div className="rounded-xl bg-bg-deep border border-border-subtle p-3.5">
                  <p className="text-[10px] uppercase tracking-wider text-text-muted mb-0.5">
                    Release Year
                  </p>
                  <p className="text-text-primary font-bold text-base">
                    {releaseYear}
                  </p>
                </div>
              )}

              {runtime && (
                <div className="rounded-xl bg-bg-deep border border-border-subtle p-3.5">
                  <p className="text-[10px] uppercase tracking-wider text-text-muted mb-0.5">
                    Runtime
                  </p>
                  <p className="text-text-primary font-bold text-base">
                    {runtime} min
                  </p>
                </div>
              )}

              {rating !== null && rating !== undefined && (
                <div className="rounded-xl bg-accent-gold/10 border border-accent-gold/20 p-3.5">
                  <p className="text-[10px] uppercase tracking-wider text-accent-gold mb-0.5 font-semibold">
                    Rating
                  </p>
                  <p className="text-accent-gold font-bold text-base">
                    ★ {typeof rating === "number" ? rating.toFixed(1) : rating} / 10
                  </p>
                </div>
              )}

              {originalLanguage && (
                <div className="rounded-xl bg-bg-deep border border-border-subtle p-3.5">
                  <p className="text-[10px] uppercase tracking-wider text-text-muted mb-0.5">
                    Language
                  </p>
                  <p className="text-text-primary font-bold text-base uppercase">
                    {originalLanguage}
                  </p>
                </div>
              )}
            </div>

            {/* Genres */}
            <div className="mt-5 pt-4 border-t border-border-subtle">
              <p className="text-[10px] uppercase tracking-wider text-text-muted mb-2 font-semibold">
                Genres
              </p>
              <div className="flex flex-wrap gap-1.5">
                {genres
                  .split(",")
                  .map((genre) => genre.trim())
                  .filter(Boolean)
                  .map((genre, idx) => (
                    <span
                      key={`${genre}-${idx}`}
                      className="px-2.5 py-1 rounded-full bg-bg-deep border border-border-subtle text-xs text-text-secondary"
                    >
                      {genre}
                    </span>
                  ))}
              </div>
            </div>

            {/* Production Countries */}
            {productionCountries.length > 0 && (
              <div className="mt-4 pt-3 border-t border-border-subtle">
                <p className="text-[10px] uppercase tracking-wider text-text-muted mb-1 font-semibold">
                  Production Countries
                </p>
                <p className="text-xs text-text-secondary">
                  {productionCountries.join(" • ")}
                </p>
              </div>
            )}
          </div>
        </section>

        {/* Cast Carousel with Invisible Scrollbar */}
        {cast.length > 0 && (
          <section>
            <div className="flex items-end justify-between mb-5">
              <div>
                <p className="text-xs font-bold uppercase tracking-wider text-accent-gold mb-1">
                  The Cast
                </p>
                <h2 className="text-2xl md:text-3xl font-bold text-text-primary">
                  Top Billed Cast
                </h2>
              </div>
              <span className="text-xs text-text-muted">
                Showing top {Math.min(cast.length, 12)}
              </span>
            </div>

            <div className="flex gap-4 overflow-x-auto pb-4 [&::-webkit-scrollbar]:hidden [-ms-overflow-style:none] [scrollbar-width:none]">
              {cast.slice(0, 12).map((member: TmdbCastMember, idx: number) => (
                <div
                  key={`${member.name}-${idx}`}
                  className="group shrink-0 w-36 md:w-40"
                >
                  <div className="relative overflow-hidden rounded-xl bg-bg-deep border border-border-subtle">
                    {member.profile_path ? (
                      <Image
                        src={`https://image.tmdb.org/t/p/w185${member.profile_path}`}
                        alt={member.name}
                        width={185}
                        height={278}
                        className="w-full aspect-[2/3] object-cover transition-transform duration-300 group-hover:scale-105"
                        loading="lazy"
                      />
                    ) : (
                      <div className="w-full aspect-[2/3] bg-bg-deep flex items-center justify-center">
                        <svg className="w-12 h-12 text-text-muted" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                        </svg>
                      </div>
                    )}
                  </div>
                  <p className="mt-2.5 text-xs font-semibold text-text-primary truncate">
                    {member.name}
                  </p>
                  {member.character && (
                    <p className="text-[11px] text-text-muted truncate">
                      {member.character}
                    </p>
                  )}
                </div>
              ))}
            </div>
          </section>
        )}

        {/* Crew */}
        {(directors.length > 0 || writers.length > 0) && (
          <section>
            <div className="flex items-center gap-3 mb-5">
              <div className="w-1 h-7 rounded-full bg-accent-gold" />
              <h2 className="text-2xl font-bold text-text-primary">
                Crew
              </h2>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {directors.length > 0 && (
                <div className="rounded-2xl border border-border-subtle bg-bg-card p-5">
                  <p className="text-xs uppercase tracking-wider text-accent-gold font-bold mb-3">
                    Director
                  </p>
                  <div className="space-y-2.5">
                    {directors.map((dir, idx) => (
                      <div key={`${dir.name}-${idx}`} className="flex items-center gap-3">
                        <div className="w-9 h-9 rounded-full bg-accent-gold/15 flex items-center justify-center text-accent-gold text-xs font-bold">
                          🎬
                        </div>
                        <div>
                          <p className="text-sm font-semibold text-text-primary">{dir.name}</p>
                          <p className="text-xs text-text-muted">Director</p>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {writers.length > 0 && (
                <div className="rounded-2xl border border-border-subtle bg-bg-card p-5">
                  <p className="text-xs uppercase tracking-wider text-accent-gold font-bold mb-3">
                    Writers & Screenplay
                  </p>
                  <div className="space-y-2.5">
                    {writers.map((writer, idx) => (
                      <div key={`${writer.name}-${idx}`} className="flex items-center gap-3">
                        <div className="w-9 h-9 rounded-full bg-bg-deep border border-border-subtle flex items-center justify-center text-text-muted text-xs">
                          ✍️
                        </div>
                        <div>
                          <p className="text-sm font-semibold text-text-primary">{writer.name}</p>
                          <p className="text-xs text-text-muted">{writer.job || "Screenplay"}</p>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </section>
        )}

        {/* Similar Movies (Auto-Loaded) */}
        {inLocalDataset && (
          <section className="border-t border-border-subtle pt-8">
            <SimilarMoviesContent movieId={movieId} movieTitle={movie.title} />
          </section>
        )}

        {/* TMDB-only movie fallback */}
        {isTmdbMovie && !inLocalDataset && (
          <section className="border-t border-border-subtle pt-8">
            <div className="flex items-center gap-3 mb-6">
              <div className="w-1 h-7 rounded-full bg-accent-gold" />
              <h2 className="text-2xl font-bold text-text-primary">
                You May Also Like
              </h2>
              <span className="text-xs font-semibold uppercase tracking-wider text-text-muted ml-2">
                TMDB Recommendations
              </span>
            </div>

            {similarMovies.length > 0 ? (
              <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-3">
                {similarMovies.map((rec) => (
                  <Link
                    key={rec.movie_id ?? rec.title}
                    href={`/movie/${rec.movie_id}`}
                    className="rounded-xl border border-border-subtle bg-bg-card overflow-hidden transition-all duration-300 hover:border-accent-gold/40 hover:shadow-gold block"
                  >
                    {rec.poster_url ? (
                      <div className="relative aspect-[2/3] bg-bg-deep">
                        <Image
                          src={rec.poster_url}
                          alt={rec.title}
                          fill
                          sizes="(max-width: 640px) 100vw, (max-width: 1024px) 50vw, 25vw"
                          className="object-cover"
                          loading="lazy"
                        />
                      </div>
                    ) : (
                      <div className="aspect-[2/3] bg-bg-deep flex flex-col items-center justify-center border-b border-border-subtle">
                        <span className="text-xs uppercase tracking-wider text-text-muted font-medium">No Poster</span>
                      </div>
                    )}
                    <div className="p-4">
                      <h3 className="text-base font-semibold text-text-primary line-clamp-2 mb-2">
                        {rec.title}
                      </h3>
                      <div className="flex flex-wrap items-center gap-2 text-xs text-text-muted">
                        {rec.release_year && <span>{rec.release_year}</span>}
                        {rec.rating !== null && rec.rating !== undefined && (
                          <span className="inline-flex items-center gap-1 text-accent-gold font-medium">
                            ★ {rec.rating.toFixed(1)}
                          </span>
                        )}
                        {rec.genres.length > 0 && <span>• {rec.genres.slice(0, 2).join(", ")}</span>}
                      </div>
                    </div>
                  </Link>
                ))}
              </div>
            ) : (
              <div className="rounded-2xl border border-border-subtle bg-bg-card text-center py-10 px-6">
                <h3 className="text-xl font-semibold text-text-primary mb-2">
                  No Similar Movies Found
                </h3>
                <p className="text-xs text-text-muted max-w-md mx-auto">
                  TMDB currently has no similar recommendations for this title.
                </p>
              </div>
            )}
          </section>
        )}
      </article>
    </main>
  );
}