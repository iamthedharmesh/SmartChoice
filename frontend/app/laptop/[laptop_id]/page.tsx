"use client";

import { useEffect, useState } from "react";
import { useParams, usePathname } from "next/navigation";
import Link from "next/link";
import LaptopCard from "@/components/LaptopCard";
import { getLaptop, getLaptops, type Laptop } from "@/lib/api";

export default function LaptopDetailPage() {
  const params = useParams();
  const pathname = usePathname();
  const laptopId = params?.laptop_id ? Number(params.laptop_id) : null;

  const [laptop, setLaptop] = useState<Laptop | null>(null);
  const [similarLaptops, setSimilarLaptops] = useState<Laptop[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [copied, setCopied] = useState(false);

  useEffect(() => {
    // Immediately scroll viewport to top when route changes
    if (typeof window !== "undefined") {
      window.scrollTo({ top: 0, behavior: "instant" });
    }

    if (!laptopId || Number.isNaN(laptopId)) {
      setError("Invalid laptop ID");
      setLoading(false);
      return;
    }

    setLoading(true);
    setLaptop(null);

    getLaptop(laptopId)
      .then((data) => {
        setLaptop(data);
        setError(null);

        // Fetch similar laptops within ±25% price range
        const price = data.price_inr || 60000;
        const minP = Math.max(0, Math.floor(price * 0.75));
        const maxP = Math.ceil(price * 1.25);

        getLaptops({
          min_price: minP,
          max_price: maxP,
          limit: 6,
          page: 1,
        })
          .then((res) => {
            if (res && Array.isArray(res.laptops)) {
              setSimilarLaptops(
                res.laptops.filter((l) => l.laptop_id !== data.laptop_id).slice(0, 3)
              );
            }
          })
          .catch(() => {});
      })
      .catch(() => {
        setError("Laptop specifications could not be loaded.");
      })
      .finally(() => setLoading(false));
  }, [laptopId, pathname]);

  const formatINR = (v: number | null | undefined) => {
    if (v === null || v === undefined) return "Price not available";
    return new Intl.NumberFormat("en-IN", {
      style: "currency",
      currency: "INR",
      maximumFractionDigits: 0,
    }).format(v);
  };

  const handleCopyLink = () => {
    if (typeof window !== "undefined") {
      navigator.clipboard.writeText(window.location.href);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-bg-deep flex items-center justify-center p-8">
        <div className="animate-pulse space-y-4 text-center">
          <div className="w-16 h-16 rounded-full bg-accent-gold/20 mx-auto" />
          <p className="text-sm text-text-muted">Loading hardware specifications...</p>
        </div>
      </div>
    );
  }

  if (error || !laptop) {
    return (
      <div className="min-h-screen bg-bg-deep flex items-center justify-center p-8">
        <div className="max-w-md w-full rounded-xl border border-red-500/30 bg-red-500/10 p-6 text-center">
          <p className="text-sm text-red-400 mb-4">{error || "Laptop not found"}</p>
          <Link
            href="/laptops"
            className="inline-flex items-center gap-2 px-4 py-2 rounded-lg bg-accent-gold text-bg-deep font-semibold text-sm hover:bg-accent-gold-dim transition-colors"
          >
            ← Back to Laptop Catalog
          </Link>
        </div>
      </div>
    );
  }

  const isDedicatedGPU = laptop.gpu_type?.toLowerCase() === "dedicated";
  const codingScore = laptop.coding_score ?? 85;
  const gamingScore = laptop.gaming_score ?? 60;
  const studentScore = laptop.student_score ?? 80;
  const prodScore = laptop.productivity_score ?? 82;
  const valueScore = laptop.value_score ?? 88;

  return (
    <main className="min-h-screen bg-bg-deep pb-16">
      {/* Breadcrumb Bar */}
      <div className="border-b border-border-subtle bg-bg-card/40 backdrop-blur-md sticky top-0 z-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-3 flex items-center justify-between gap-4">
          <nav className="flex items-center gap-2 text-xs text-text-muted truncate">
            <Link href="/" className="hover:text-text-primary transition-colors">Home</Link>
            <span>/</span>
            <Link href="/laptops" className="hover:text-text-primary transition-colors">Laptops</Link>
            <span>/</span>
            <span className="text-text-secondary">{laptop.brand}</span>
            <span>/</span>
            <span className="text-accent-gold font-medium truncate">{laptop.model}</span>
          </nav>

          <div className="flex items-center gap-2 shrink-0">
            <button
              type="button"
              onClick={handleCopyLink}
              className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg border border-border-subtle bg-bg-deep text-xs font-medium text-text-secondary hover:text-text-primary hover:border-border-glow transition-all"
            >
              {copied ? (
                <>
                  <svg className="w-3.5 h-3.5 text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                  </svg>
                  <span className="text-emerald-400">Link Copied!</span>
                </>
              ) : (
                <>
                  <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8.684 13.342C8.886 12.938 9 12.482 9 12c0-.482-.114-.938-.316-1.342m0 2.684a3 3 0 110-2.684m0 2.684l6.632 3.316m-6.632-6l6.632-3.316m0 0a3 3 0 105.367-2.684 3 3 0 00-5.367 2.684zm0 9.316a3 3 0 105.368 2.684 3 3 0 00-5.368-2.684z" />
                  </svg>
                  <span>Share</span>
                </>
              )}
            </button>
            <Link
              href="/laptops/find"
              className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-accent-gold text-bg-deep text-xs font-bold hover:bg-accent-gold-dim transition-colors"
            >
              Find My Laptop
            </Link>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-8 space-y-8">
        {/* Main Showcase Hero */}
        <div className="rounded-2xl border border-border-subtle bg-bg-card p-6 sm:p-8">
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
            {/* Visual Hardware Box */}
            <div className="lg:col-span-4 flex flex-col items-center justify-center bg-gradient-to-b from-bg-deep to-bg-card rounded-xl border border-border-subtle p-8 min-h-[320px] relative overflow-hidden group">
              <div className="absolute inset-0 bg-accent-gold/5 blur-3xl rounded-full -z-0 pointer-events-none" />
              <div className="text-6xl sm:text-7xl mb-4 group-hover:scale-110 transition-transform duration-300">
                💻
              </div>
              <span className="text-lg font-black uppercase tracking-wider text-accent-gold">
                {laptop.brand}
              </span>
              <span className="text-xs text-text-muted mt-1">
                {laptop.operating_system}
              </span>

              <div className="mt-6 flex flex-wrap gap-2 justify-center">
                <span className="px-2.5 py-1 rounded-md bg-bg-deep text-[11px] font-medium text-text-secondary border border-border-subtle">
                  ⚖️ {laptop.weight_kg} kg
                </span>
                <span className="px-2.5 py-1 rounded-md bg-bg-deep text-[11px] font-medium text-text-secondary border border-border-subtle">
                  🔋 {laptop.battery_whr} Whr
                </span>
              </div>
            </div>

            {/* Specifications & Overview */}
            <div className="lg:col-span-8 flex flex-col justify-between">
              <div>
                <div className="flex items-center gap-2 mb-2">
                  <span className="text-xs font-bold uppercase tracking-wider text-accent-gold">
                    {laptop.brand}
                  </span>
                  <span className="text-text-muted">•</span>
                  <span className="text-xs text-text-muted">
                    SmartChoice Verified Hardware
                  </span>
                </div>

                <h1 className="text-2xl sm:text-3xl lg:text-4xl font-extrabold text-text-primary tracking-tight">
                  {laptop.model}
                </h1>

                {/* Price & Rating Badges */}
                <div className="mt-4 flex flex-wrap items-baseline gap-4">
                  <span className="text-3xl sm:text-4xl font-black text-accent-gold">
                    {formatINR(laptop.price_inr)}
                  </span>
                  <span className="text-xs text-text-muted">
                    (Approximate Indian Retail Price)
                  </span>
                </div>

                <div className="mt-4 flex flex-wrap items-center gap-2.5">
                  <span className="inline-flex items-center gap-1 px-3 py-1 rounded-full bg-accent-gold/15 border border-accent-gold/30 text-accent-gold text-xs font-bold">
                    ★ {laptop.rating.toFixed(1)} / 100 Index
                  </span>
                  <span className="inline-flex items-center px-3 py-1 rounded-full bg-bg-deep border border-border-subtle text-text-primary text-xs font-semibold">
                    {laptop.processor_model} ({laptop.cpu_cores} Cores)
                  </span>
                  <span className={`inline-flex items-center px-3 py-1 rounded-full text-xs font-semibold ${
                    isDedicatedGPU
                      ? "bg-emerald-500/15 border border-emerald-500/30 text-emerald-400"
                      : "bg-blue-400/15 border border-blue-400/30 text-blue-400"
                  }`}>
                    {laptop.gpu_model} ({laptop.gpu_type})
                  </span>
                  <span className="inline-flex items-center px-3 py-1 rounded-full bg-bg-deep border border-border-subtle text-text-secondary text-xs font-medium">
                    ⚡ {laptop.refresh_rate_hz} Hz
                  </span>
                </div>

                {/* At a Glance Grid */}
                <div className="mt-6 pt-6 border-t border-border-subtle">
                  <h3 className="text-xs font-bold uppercase tracking-wider text-text-muted mb-3">
                    At a Glance
                  </h3>
                  <div className="grid grid-cols-2 sm:grid-cols-3 gap-3">
                    <div className="rounded-xl bg-bg-deep border border-border-subtle p-3.5">
                      <p className="text-[10px] uppercase tracking-wider text-text-muted">Display</p>
                      <p className="text-sm font-bold text-text-primary mt-1">
                        {laptop.display_size_inch}&quot; {laptop.refresh_rate_hz}Hz
                      </p>
                      <p className="text-[11px] text-text-secondary truncate mt-0.5">
                        {laptop.resolution}
                      </p>
                    </div>

                    <div className="rounded-xl bg-bg-deep border border-border-subtle p-3.5">
                      <p className="text-[10px] uppercase tracking-wider text-text-muted">Processor</p>
                      <p className="text-sm font-bold text-text-primary mt-1 truncate">
                        {laptop.processor_model}
                      </p>
                      <p className="text-[11px] text-text-secondary mt-0.5">
                        {laptop.cpu_cores} Cores • {laptop.processor_brand}
                      </p>
                    </div>

                    <div className="rounded-xl bg-bg-deep border border-border-subtle p-3.5">
                      <p className="text-[10px] uppercase tracking-wider text-text-muted">Memory</p>
                      <p className="text-sm font-bold text-text-primary mt-1">
                        {laptop.ram_gb} GB RAM
                      </p>
                      <p className="text-[11px] text-text-secondary mt-0.5">{laptop.ram_type}</p>
                    </div>

                    <div className="rounded-xl bg-bg-deep border border-border-subtle p-3.5">
                      <p className="text-[10px] uppercase tracking-wider text-text-muted">Storage</p>
                      <p className="text-sm font-bold text-text-primary mt-1">
                        {laptop.storage_gb} GB
                      </p>
                      <p className="text-[11px] text-text-secondary mt-0.5">{laptop.storage_type}</p>
                    </div>

                    <div className="rounded-xl bg-bg-deep border border-border-subtle p-3.5">
                      <p className="text-[10px] uppercase tracking-wider text-text-muted">Graphics</p>
                      <p className={`text-sm font-bold truncate mt-1 ${isDedicatedGPU ? "text-emerald-400" : "text-text-primary"}`}>
                        {laptop.gpu_model}
                      </p>
                      <p className="text-[11px] text-text-secondary mt-0.5 capitalize">{laptop.gpu_type} GPU</p>
                    </div>

                    <div className="rounded-xl bg-bg-deep border border-border-subtle p-3.5">
                      <p className="text-[10px] uppercase tracking-wider text-text-muted">Portability</p>
                      <p className="text-sm font-bold text-text-primary mt-1">
                        {laptop.weight_kg} kg
                      </p>
                      <p className="text-[11px] text-text-secondary mt-0.5">{laptop.battery_whr} Whr Battery</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Persona Breakdown Meters */}
        <section className="rounded-2xl border border-border-subtle bg-bg-card p-6 sm:p-8">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 mb-6">
            <div>
              <h2 className="text-lg font-bold text-text-primary">
                SmartChoice Persona Capability Scores
              </h2>
              <p className="text-xs text-text-muted">
                Calculated hardware index based on synthetic benchmarks, GPU power tiers, RAM, and weight.
              </p>
            </div>
            <span className="text-xs font-semibold px-3 py-1 rounded-full bg-accent-gold/10 text-accent-gold border border-accent-gold/30 self-start sm:self-auto">
              Hardware Index
            </span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
            <div className="rounded-xl bg-bg-deep border border-border-subtle p-4">
              <div className="flex justify-between items-center text-xs mb-1.5">
                <span className="font-semibold text-text-secondary">💻 Coding</span>
                <span className="font-bold text-accent-gold">{codingScore}/100</span>
              </div>
              <div className="h-2 rounded-full bg-border-subtle overflow-hidden">
                <div className="h-full bg-accent-gold rounded-full" style={{ width: `${codingScore}%` }} />
              </div>
              <p className="text-[10px] text-text-muted mt-2">RAM, compilation cores & storage</p>
            </div>

            <div className="rounded-xl bg-bg-deep border border-border-subtle p-4">
              <div className="flex justify-between items-center text-xs mb-1.5">
                <span className="font-semibold text-text-secondary">🎮 Gaming</span>
                <span className="font-bold text-accent-gold">{gamingScore}/100</span>
              </div>
              <div className="h-2 rounded-full bg-border-subtle overflow-hidden">
                <div className="h-full bg-accent-gold rounded-full" style={{ width: `${gamingScore}%` }} />
              </div>
              <p className="text-[10px] text-text-muted mt-2">Dedicated GPU & refresh rate</p>
            </div>

            <div className="rounded-xl bg-bg-deep border border-border-subtle p-4">
              <div className="flex justify-between items-center text-xs mb-1.5">
                <span className="font-semibold text-text-secondary">🎒 Student</span>
                <span className="font-bold text-accent-gold">{studentScore}/100</span>
              </div>
              <div className="h-2 rounded-full bg-border-subtle overflow-hidden">
                <div className="h-full bg-accent-gold rounded-full" style={{ width: `${studentScore}%` }} />
              </div>
              <p className="text-[10px] text-text-muted mt-2">Battery Whr & lightweight chassis</p>
            </div>

            <div className="rounded-xl bg-bg-deep border border-border-subtle p-4">
              <div className="flex justify-between items-center text-xs mb-1.5">
                <span className="font-semibold text-text-secondary">💼 Productivity</span>
                <span className="font-bold text-accent-gold">{prodScore}/100</span>
              </div>
              <div className="h-2 rounded-full bg-border-subtle overflow-hidden">
                <div className="h-full bg-accent-gold rounded-full" style={{ width: `${prodScore}%` }} />
              </div>
              <p className="text-[10px] text-text-muted mt-2">Ergonomics & everyday stability</p>
            </div>

            <div className="rounded-xl bg-bg-deep border border-border-subtle p-4">
              <div className="flex justify-between items-center text-xs mb-1.5">
                <span className="font-semibold text-text-secondary">💰 Value</span>
                <span className="font-bold text-accent-gold">{valueScore}/100</span>
              </div>
              <div className="h-2 rounded-full bg-border-subtle overflow-hidden">
                <div className="h-full bg-accent-gold rounded-full" style={{ width: `${valueScore}%` }} />
              </div>
              <p className="text-[10px] text-text-muted mt-2">Hardware-to-price efficiency</p>
            </div>
          </div>
        </section>

        {/* Technical Specifications */}
        <section className="rounded-2xl border border-border-subtle bg-bg-card p-6 sm:p-8">
          <h2 className="text-xl font-bold text-text-primary mb-6">
            Detailed Technical Specifications
          </h2>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="rounded-xl bg-bg-deep border border-border-subtle p-5">
              <h3 className="text-xs font-bold uppercase tracking-wider text-accent-gold mb-4 flex items-center gap-2">
                <span>🖥️</span> Display & Visuals
              </h3>
              <dl className="space-y-3 text-xs">
                <div className="flex justify-between py-1 border-b border-border-subtle/50">
                  <dt className="text-text-muted">Screen Size</dt>
                  <dd className="font-semibold text-text-primary">{laptop.display_size_inch} inches</dd>
                </div>
                <div className="flex justify-between py-1 border-b border-border-subtle/50">
                  <dt className="text-text-muted">Resolution</dt>
                  <dd className="font-semibold text-text-primary">{laptop.resolution}</dd>
                </div>
                <div className="flex justify-between py-1 border-b border-border-subtle/50">
                  <dt className="text-text-muted">Refresh Rate</dt>
                  <dd className="font-semibold text-text-primary">{laptop.refresh_rate_hz} Hz</dd>
                </div>
                <div className="flex justify-between py-1">
                  <dt className="text-text-muted">Panel Quality</dt>
                  <dd className="font-semibold text-text-primary">
                    {laptop.resolution.toLowerCase().includes("oled") ? "OLED High-Contrast" : "Anti-Glare IPS"}
                  </dd>
                </div>
              </dl>
            </div>

            <div className="rounded-xl bg-bg-deep border border-border-subtle p-5">
              <h3 className="text-xs font-bold uppercase tracking-wider text-accent-gold mb-4 flex items-center gap-2">
                <span>⚡</span> Processor & Architecture
              </h3>
              <dl className="space-y-3 text-xs">
                <div className="flex justify-between py-1 border-b border-border-subtle/50">
                  <dt className="text-text-muted">Processor Model</dt>
                  <dd className="font-semibold text-text-primary">{laptop.processor_model}</dd>
                </div>
                <div className="flex justify-between py-1 border-b border-border-subtle/50">
                  <dt className="text-text-muted">Processor Brand</dt>
                  <dd className="font-semibold text-text-primary">{laptop.processor_brand}</dd>
                </div>
                <div className="flex justify-between py-1 border-b border-border-subtle/50">
                  <dt className="text-text-muted">CPU Core Count</dt>
                  <dd className="font-semibold text-text-primary">{laptop.cpu_cores} Cores</dd>
                </div>
                <div className="flex justify-between py-1">
                  <dt className="text-text-muted">Operating System</dt>
                  <dd className="font-semibold text-text-primary">{laptop.operating_system}</dd>
                </div>
              </dl>
            </div>

            <div className="rounded-xl bg-bg-deep border border-border-subtle p-5">
              <h3 className="text-xs font-bold uppercase tracking-wider text-accent-gold mb-4 flex items-center gap-2">
                <span>💾</span> Memory & Storage
              </h3>
              <dl className="space-y-3 text-xs">
                <div className="flex justify-between py-1 border-b border-border-subtle/50">
                  <dt className="text-text-muted">RAM Capacity</dt>
                  <dd className="font-semibold text-text-primary">{laptop.ram_gb} GB</dd>
                </div>
                <div className="flex justify-between py-1 border-b border-border-subtle/50">
                  <dt className="text-text-muted">RAM Architecture</dt>
                  <dd className="font-semibold text-text-primary">{laptop.ram_type}</dd>
                </div>
                <div className="flex justify-between py-1 border-b border-border-subtle/50">
                  <dt className="text-text-muted">Storage Capacity</dt>
                  <dd className="font-semibold text-text-primary">{laptop.storage_gb} GB</dd>
                </div>
                <div className="flex justify-between py-1">
                  <dt className="text-text-muted">Storage Standard</dt>
                  <dd className="font-semibold text-text-primary">{laptop.storage_type}</dd>
                </div>
              </dl>
            </div>

            <div className="rounded-xl bg-bg-deep border border-border-subtle p-5">
              <h3 className="text-xs font-bold uppercase tracking-wider text-accent-gold mb-4 flex items-center gap-2">
                <span>🎮</span> Graphics & Battery
              </h3>
              <dl className="space-y-3 text-xs">
                <div className="flex justify-between py-1 border-b border-border-subtle/50">
                  <dt className="text-text-muted">Graphics Card</dt>
                  <dd className="font-semibold text-text-primary">{laptop.gpu_model}</dd>
                </div>
                <div className="flex justify-between py-1 border-b border-border-subtle/50">
                  <dt className="text-text-muted">GPU Type</dt>
                  <dd className="font-semibold text-text-primary capitalize">{laptop.gpu_type}</dd>
                </div>
                <div className="flex justify-between py-1 border-b border-border-subtle/50">
                  <dt className="text-text-muted">Battery Capacity</dt>
                  <dd className="font-semibold text-text-primary">{laptop.battery_whr} Whr</dd>
                </div>
                <div className="flex justify-between py-1">
                  <dt className="text-text-muted">Weight</dt>
                  <dd className="font-semibold text-text-primary">{laptop.weight_kg} kg</dd>
                </div>
              </dl>
            </div>
          </div>
        </section>

        {/* Verdict */}
        <section className="rounded-2xl border border-border-subtle bg-gradient-to-r from-bg-card via-bg-deep to-bg-card p-6 sm:p-8">
          <div className="max-w-3xl">
            <span className="text-xs font-bold uppercase tracking-wider text-accent-gold">
              SmartChoice Verdict
            </span>
            <h2 className="text-xl font-bold text-text-primary mt-1">
              Who is the {laptop.brand} {laptop.model} for?
            </h2>
            <p className="mt-3 text-sm text-text-secondary leading-relaxed">
              The {laptop.model} is a well-rounded machine in the {formatINR(laptop.price_inr)} price bracket.
              Equipped with an {laptop.processor_model} ({laptop.cpu_cores} Cores), {laptop.ram_gb}GB of {laptop.ram_type} memory, and {laptop.storage_gb}GB fast NVMe SSD,
              it is ideal for {codingScore >= 88 ? "software developers compiling complex codebases and running VMs" : "everyday multitasking and intensive university coursework"}.
              {isDedicatedGPU ? ` Its ${laptop.gpu_model} dedicated graphics also unlocks full support for 3D modeling, game development, and modern gaming.` : " The integrated graphics deliver cool and quiet power efficiency."}
            </p>
            <div className="mt-5 flex flex-wrap gap-3">
              <Link
                href="/laptops/find"
                className="inline-flex items-center gap-2 px-4 py-2 rounded-lg bg-accent-gold text-bg-deep text-xs font-bold hover:bg-accent-gold-dim transition-colors"
              >
                Compare with Other Laptops →
              </Link>
              <Link
                href={`/laptops?brand=${encodeURIComponent(laptop.brand)}`}
                className="inline-flex items-center gap-2 px-4 py-2 rounded-lg border border-border-subtle bg-bg-deep text-xs font-semibold text-text-secondary hover:text-text-primary hover:border-border-glow transition-colors"
              >
                Browse All {laptop.brand} Laptops
              </Link>
            </div>
          </div>
        </section>

        {/* Similar Laptops in this Price Range */}
        {similarLaptops.length > 0 && (
          <section className="rounded-2xl border border-border-subtle bg-bg-card p-6 sm:p-8">
            <div className="flex items-center justify-between mb-6">
              <div>
                <h2 className="text-xl font-bold text-text-primary">
                  Similar Laptops in this Price Segment
                </h2>
                <p className="text-xs text-text-muted mt-0.5">
                  Alternative laptops close to {formatINR(laptop.price_inr)}
                </p>
              </div>
              <Link
                href="/laptops"
                className="text-xs font-semibold text-accent-gold hover:underline"
              >
                View Catalog →
              </Link>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
              {similarLaptops.map((item) => (
                <LaptopCard key={item.laptop_id} laptop={item} />
              ))}
            </div>
          </section>
        )}
      </div>
    </main>
  );
}