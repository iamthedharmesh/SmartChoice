import Link from "next/link";

export default function HomePage() {
  return (
    <main className="min-h-screen bg-bg-deep">
      {/* Hero Section */}
      <section className="relative overflow-hidden pt-16 pb-20 sm:pt-24 sm:pb-28">
        <div className="absolute inset-0 bg-gradient-to-b from-accent-gold/5 via-transparent to-transparent pointer-events-none" />

        <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 text-center relative z-10">
          <span className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-accent-gold/15 border border-accent-gold/30 text-accent-gold text-xs font-bold uppercase tracking-wider mb-6">
            Intelligent Recommendation Platform
          </span>

          <h1 className="text-4xl sm:text-6xl lg:text-7xl font-extrabold tracking-tight text-text-primary">
            Make <span className="text-gradient-gold">Better Choices.</span>
          </h1>

          <p className="mt-5 text-base sm:text-xl text-text-secondary max-w-2xl mx-auto leading-relaxed">
            SmartChoice helps you discover movies, smartphones, and laptops tailored
            to your priorities. Powered by dual NLP content filtering and multi-criteria
            hardware scoring engines.
          </p>

          {/* Tri-Category Quick Navigation */}
          <div className="mt-8 flex flex-wrap items-center justify-center gap-3">
            <Link
              href="/laptops"
              className="inline-flex items-center gap-2 px-5 py-3 rounded-xl bg-accent-gold text-bg-deep font-bold text-sm hover:bg-accent-gold-dim transition-all shadow-lg shadow-accent-gold/10"
            >
              💻 Explore Laptops
            </Link>

            <Link
              href="/mobiles"
              className="inline-flex items-center gap-2 px-5 py-3 rounded-xl border border-border-subtle bg-bg-card text-text-primary font-semibold text-sm hover:border-border-glow hover:bg-bg-card-hover transition-all"
            >
              📱 Explore Mobiles
            </Link>

            <Link
              href="/movies"
              className="inline-flex items-center gap-2 px-5 py-3 rounded-xl border border-border-subtle bg-bg-card text-text-primary font-semibold text-sm hover:border-border-glow hover:bg-bg-card-hover transition-all"
            >
              🎬 Explore Movies
            </Link>
          </div>

          {/* Platform Metrics */}
          <div className="mt-12 flex flex-wrap items-center justify-center gap-6 text-xs text-text-muted">
            <div className="flex items-center gap-2">
              <span className="text-accent-gold font-bold">🎬</span>
              <span>5,000+ Movies</span>
            </div>
            <span className="text-border-subtle">•</span>
            <div className="flex items-center gap-2">
              <span className="text-accent-gold font-bold">📱</span>
              <span>980+ Smartphones</span>
            </div>
            <span className="text-border-subtle">•</span>
            <div className="flex items-center gap-2">
              <span className="text-accent-gold font-bold">💻</span>
              <span>105+ Laptops</span>
            </div>
            <span className="text-border-subtle">•</span>
            <div className="flex items-center gap-2">
              <span className="text-accent-gold font-bold">⚡</span>
              <span>Sub-50ms Inference</span>
            </div>
          </div>
        </div>
      </section>

      {/* Explore Categories Section */}
      <section className="py-16 border-t border-border-subtle/50 bg-bg-card/30">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center max-w-2xl mx-auto mb-12">
            <h2 className="text-2xl sm:text-3xl font-extrabold text-text-primary">
              Explore Categories
            </h2>
            <p className="mt-2 text-sm text-text-muted">
              Choose a category to discover data-driven personalized recommendations
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {/* Category: Movies */}
            <div className="rounded-2xl border border-border-subtle bg-bg-card p-6 flex flex-col justify-between hover:border-border-glow transition-all card-glow">
              <div>
                <div className="w-12 h-12 rounded-xl bg-accent-gold/15 text-accent-gold flex items-center justify-center text-xl mb-4">
                  🎬
                </div>
                <div className="flex items-center justify-between">
                  <h3 className="text-xl font-bold text-text-primary">Movies</h3>
                  <span className="text-[10px] font-bold px-2.5 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                    5,000+ Titles
                  </span>
                </div>
                <p className="mt-3 text-xs sm:text-sm text-text-secondary leading-relaxed">
                  Discover your next film with TF-IDF content-based NLP plot recommendations.
                  Search, browse by genre, and explore director and cast networks.
                </p>
              </div>

              <div className="mt-6 pt-4 border-t border-border-subtle flex items-center justify-between">
                <Link
                  href="/movies"
                  className="text-xs font-bold text-accent-gold hover:underline inline-flex items-center gap-1"
                >
                  Browse Catalog →
                </Link>
                <Link
                  href="/movies/find"
                  className="text-xs font-medium text-text-secondary hover:text-text-primary"
                >
                  Find My Movie
                </Link>
              </div>
            </div>

            {/* Category: Mobiles */}
            <div className="rounded-2xl border border-border-subtle bg-bg-card p-6 flex flex-col justify-between hover:border-border-glow transition-all card-glow">
              <div>
                <div className="w-12 h-12 rounded-xl bg-accent-gold/15 text-accent-gold flex items-center justify-center text-xl mb-4">
                  📱
                </div>
                <div className="flex items-center justify-between">
                  <h3 className="text-xl font-bold text-text-primary">Mobiles</h3>
                  <span className="text-[10px] font-bold px-2.5 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                    980 Devices
                  </span>
                </div>
                <p className="mt-3 text-xs sm:text-sm text-text-secondary leading-relaxed">
                  Compare specifications, verified benchmark ratings, and find your ideal device.
                  Custom budget brackets, hardware filtering, and camera scoring.
                </p>
              </div>

              <div className="mt-6 pt-4 border-t border-border-subtle flex items-center justify-between">
                <Link
                  href="/mobiles"
                  className="text-xs font-bold text-accent-gold hover:underline inline-flex items-center gap-1"
                >
                  Browse Phones →
                </Link>
                <Link
                  href="/mobiles/find"
                  className="text-xs font-medium text-text-secondary hover:text-text-primary"
                >
                  Find My Phone
                </Link>
              </div>
            </div>

            {/* Category: Laptops (ACTIVATED) */}
            <div className="rounded-2xl border border-accent-gold/40 bg-bg-card p-6 flex flex-col justify-between hover:border-accent-gold transition-all card-glow relative overflow-hidden">
              <div className="absolute top-0 right-0 bg-accent-gold text-bg-deep text-[10px] font-extrabold px-3 py-1 rounded-bl-lg uppercase tracking-wider">
                Full Specs & Persona Scoring
              </div>

              <div>
                <div className="w-12 h-12 rounded-xl bg-accent-gold/15 text-accent-gold flex items-center justify-center text-xl mb-4">
                  💻
                </div>
                <div className="flex items-center justify-between">
                  <h3 className="text-xl font-bold text-text-primary">Laptops</h3>
                  <span className="text-[10px] font-bold px-2.5 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                    105 Models
                  </span>
                </div>
                <p className="mt-3 text-xs sm:text-sm text-text-secondary leading-relaxed">
                  Find the ideal laptop for Coding, Gaming, University, or Value.
                  Evaluated on multi-core CPUs, GPU tiers, RAM, and weight.
                </p>
              </div>

              <div className="mt-6 pt-4 border-t border-border-subtle flex items-center justify-between">
                <Link
                  href="/laptops"
                  className="text-xs font-bold text-accent-gold hover:underline inline-flex items-center gap-1"
                >
                  Browse 105 Laptops →
                </Link>
                <Link
                  href="/laptops/find"
                  className="px-3 py-1.5 rounded-lg bg-accent-gold text-bg-deep font-bold text-xs hover:bg-accent-gold-dim transition-colors"
                >
                  Find My Laptop
                </Link>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* How SmartChoice Works */}
      <section className="py-20 border-t border-border-subtle/50">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center max-w-2xl mx-auto mb-16">
            <h2 className="text-2xl sm:text-3xl font-extrabold text-text-primary">
              How SmartChoice Works
            </h2>
            <p className="mt-2 text-sm text-text-muted">
              Three simple steps to transparent, explainable recommendations
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="rounded-2xl border border-border-subtle bg-bg-card p-6 text-center">
              <div className="w-12 h-12 rounded-full bg-accent-gold/15 text-accent-gold font-black text-sm flex items-center justify-center mx-auto mb-4 border border-accent-gold/30">
                01
              </div>
              <h3 className="text-base font-bold text-text-primary mb-2">
                Define Your Constraints
              </h3>
              <p className="text-xs sm:text-sm text-text-secondary leading-relaxed">
                Set budget brackets, preferred brands, RAM minimums, or movie themes.
                Hard filters eliminate unviable options first.
              </p>
            </div>

            <div className="rounded-2xl border border-border-subtle bg-bg-card p-6 text-center">
              <div className="w-12 h-12 rounded-full bg-accent-gold/15 text-accent-gold font-black text-sm flex items-center justify-center mx-auto mb-4 border border-accent-gold/30">
                02
              </div>
              <h3 className="text-base font-bold text-text-primary mb-2">
                Hybrid Scoring Algorithms
              </h3>
              <p className="text-xs sm:text-sm text-text-secondary leading-relaxed">
                Movies use TF-IDF vectorization and cosine similarity over plot keywords.
                Hardware uses multi-criteria persona scoring for Coding, Gaming, Battery, and Value.
              </p>
            </div>

            <div className="rounded-2xl border border-border-subtle bg-bg-card p-6 text-center">
              <div className="w-12 h-12 rounded-full bg-accent-gold/15 text-accent-gold font-black text-sm flex items-center justify-center mx-auto mb-4 border border-accent-gold/30">
                03
              </div>
              <h3 className="text-base font-bold text-text-primary mb-2">
                Explainable Match %
              </h3>
              <p className="text-xs sm:text-sm text-text-secondary leading-relaxed">
                Receive ranked recommendations with transparent match percentages,
                highlighted feature chips, and detailed hardware benchmark breakdowns.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-border-subtle bg-bg-card/60 pt-12 pb-8">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-10">
            <div>
              <div className="flex items-center gap-2 mb-3">
                <span className="text-accent-gold text-xl font-bold">☵</span>
                <span className="text-lg font-bold text-text-primary tracking-tight">SmartChoice</span>
              </div>
              <p className="text-xs text-text-muted leading-relaxed">
                Intelligent, data-driven recommendation engine for movies and consumer electronics.
                Built with FastAPI and Next.js.
              </p>
            </div>

            <div>
              <p className="text-xs font-bold uppercase tracking-wider text-text-primary mb-3">Categories</p>
              <ul className="space-y-2 text-xs text-text-secondary">
                <li><Link href="/movies" className="hover:text-accent-gold transition-colors">Movies Catalog</Link></li>
                <li><Link href="/movies/find" className="hover:text-accent-gold transition-colors">Find My Movie</Link></li>
                <li><Link href="/mobiles" className="hover:text-accent-gold transition-colors">Mobiles Catalog (980)</Link></li>
                <li><Link href="/mobiles/find" className="hover:text-accent-gold transition-colors">Find My Phone</Link></li>
                <li><Link href="/laptops" className="hover:text-accent-gold transition-colors">Laptops Catalog (105)</Link></li>
                <li><Link href="/laptops/find" className="hover:text-accent-gold transition-colors">Find My Laptop</Link></li>
              </ul>
            </div>

            <div>
              <p className="text-xs font-bold uppercase tracking-wider text-text-primary mb-3">Technology</p>
              <ul className="space-y-2 text-xs text-text-secondary">
                <li>TF-IDF NLP Vectorization</li>
                <li>Cosine Similarity Engine</li>
                <li>Multi-Attribute Persona Scoring</li>
                <li>FastAPI Backend & Next.js 16</li>
              </ul>
            </div>

            <div>
              <p className="text-xs font-bold uppercase tracking-wider text-text-primary mb-3">Data Sources</p>
              <ul className="space-y-2 text-xs text-text-secondary">
                <li>TMDB 5000 Movies Dataset</li>
                <li>Indian Smartphone Specs Catalog</li>
                <li>Indian Laptop Hardware Specs</li>
              </ul>
            </div>
          </div>

          <div className="pt-6 border-t border-border-subtle/50 text-center text-xs text-text-muted">
            SmartChoice — Intelligent Recommendation Platform • Powered by FastAPI & Next.js
          </div>
        </div>
      </footer>
    </main>
  );
}