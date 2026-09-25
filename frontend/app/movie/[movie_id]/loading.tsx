export default function MovieDetailsLoading() {
  return (
    <main className="mx-auto max-w-6xl px-4 py-10 space-y-6">
      <div className="h-10 w-3/12 animate-pulse rounded bg-zinc-200" />
      <div className="h-4 w-2/12 animate-pulse rounded bg-zinc-200" />
      <div className="space-y-3">
        <div className="h-4 w-full animate-pulse rounded bg-zinc-200" />
        <div className="h-4 w-5/6 animate-pulse rounded bg-zinc-200" />
        <div className="h-4 w-4/6 animate-pulse rounded bg-zinc-200" />
      </div>
      <div className="border-t border-zinc-200 pt-6">
        <div className="h-8 w-2/12 animate-pulse rounded bg-zinc-200 mb-4" />
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {Array.from({ length: 6 }).map((_, i) => (
            <div key={i} className="rounded-xl border border-zinc-200 bg-white p-4 animate-pulse space-y-3">
              <div className="h-6 w-3/4 bg-zinc-200 rounded" />
              <div className="h-4 w-1/2 bg-zinc-200 rounded" />
              <div className="h-4 w-full bg-zinc-200 rounded" />
              <div className="h-4 w-5/6 bg-zinc-200 rounded" />
            </div>
          ))}
        </div>
      </div>
    </main>
  );
}