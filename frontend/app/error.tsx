"use client";

type ErrorProps = {
  error: Error & { digest?: string };
  reset: () => void;
};

export default function Error({ error, reset }: ErrorProps) {
  return (
    <main className="mx-auto max-w-6xl px-4 py-10">
      <h1 className="text-4xl font-bold text-zinc-900">SmartChoice</h1>
      <p className="mt-4 text-zinc-700">
        Could not load movies from the FastAPI backend.
      </p>
      <p className="mt-2 text-sm text-zinc-500">{error.message}</p>
      <p className="mt-2 text-sm text-zinc-500">
        Make sure the API is running at http://127.0.0.1:8000
      </p>
      <button
        type="button"
        onClick={() => reset()}
        className="mt-4 rounded-lg bg-zinc-900 px-4 py-2 text-sm text-white"
      >
        Try again
      </button>
    </main>
  );
}
