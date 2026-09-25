"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import LaptopCard from "@/components/LaptopCard";
import {
  getLaptopRecommendations,
  getLaptopBrands,
  type Laptop,
} from "@/lib/api";

type BudgetPreset = {
  label: string;
  min: number | null;
  max: number | null;
};

const BUDGET_PRESETS: BudgetPreset[] = [
  { label: "Any Budget", min: null, max: null },
  { label: "Under ₹40,000", min: null, max: 40000 },
  { label: "₹40K – ₹65,000", min: 40000, max: 65000 },
  { label: "₹65K – ₹1,00,000", min: 65000, max: 100000 },
  { label: "₹1,00K – ₹1,50,000", min: 100000, max: 150000 },
  { label: "₹1,50,000+", min: 150000, max: null },
];

const PRIORITIES = [
  {
    id: "Coding",
    label: "Software Engineering & Coding",
    icon: "💻",
    description: "Multi-core CPUs, 16GB+ RAM, fast NVMe SSD, and high-DPI displays.",
  },
  {
    id: "Gaming",
    label: "Gaming & 3D Rendering",
    icon: "🎮",
    description: "Dedicated RTX graphics, high TGP wattage, and 120Hz+ displays.",
  },
  {
    id: "Student",
    label: "College & Portability",
    icon: "🎒",
    description: "Sub-1.5kg chassis, long battery life (50+ Whr), and all-day endurance.",
  },
  {
    id: "Everyday",
    label: "Office & Productivity",
    icon: "💼",
    description: "Quiet thermals, comfortable keyboards, and dependable day-to-day multitasking.",
  },
  {
    id: "Value",
    label: "Value for Money",
    icon: "💰",
    description: "Maximum hardware specifications and build quality per rupee spent.",
  },
];

export default function FindLaptopPage() {
  const [brands, setBrands] = useState<string[]>([]);
  const [selectedPresetIndex, setSelectedPresetIndex] = useState(0);
  const [priority, setPriority] = useState("Coding");
  const [selectedBrand, setSelectedBrand] = useState("Any Brand");
  const [minRam, setMinRam] = useState<number | undefined>(undefined);
  const [gpuType, setGpuType] = useState("All");

  const [recommendations, setRecommendations] = useState<Laptop[]>([]);
  const [loading, setLoading] = useState(false);
  const [hasSearched, setHasSearched] = useState(false);
  const [sortBy, setSortBy] = useState<"match" | "price-asc" | "price-desc" | "rating">("match");

  // Fetch unique brands
  useEffect(() => {
    getLaptopBrands()
      .then((res) => {
        if (res && res.brands) setBrands(["Any Brand", ...res.brands]);
      })
      .catch(() => {});
  }, []);

  const handleRecommend = async () => {
    setLoading(true);
    setHasSearched(true);

    const preset = BUDGET_PRESETS[selectedPresetIndex];
    try {
      const res = await getLaptopRecommendations({
        budget_min: preset.min,
        budget_max: preset.max,
        brand: selectedBrand === "Any Brand" ? null : selectedBrand,
        min_ram: minRam ?? null,
        gpu_type: gpuType === "All" ? null : gpuType,
        priority,
        limit: 9,
      });

      setRecommendations(res.recommendations || []);
    } catch {
      setRecommendations([]);
    } finally {
      setLoading(false);
    }
  };

  // Sort recommendations locally
  const sortedRecommendations = [...recommendations].sort((a, b) => {
    if (sortBy === "price-asc") return a.price_inr - b.price_inr;
    if (sortBy === "price-desc") return b.price_inr - a.price_inr;
    if (sortBy === "rating") return (b.rating ?? 0) - (a.rating ?? 0);
    return (b.match_percentage ?? 0) - (a.match_percentage ?? 0);
  });

  return (
    <main className="min-h-screen bg-bg-deep pb-20">
      {/* Hero Header */}
      <section className="border-b border-border-subtle bg-bg-card/40 backdrop-blur-md pt-10 pb-8">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          <nav className="flex items-center gap-2 text-xs text-text-muted mb-4">
            <Link href="/" className="hover:text-text-primary transition-colors">Home</Link>
            <span>/</span>
            <Link href="/laptops" className="hover:text-text-primary transition-colors">Laptops</Link>
            <span>/</span>
            <span className="text-accent-gold font-medium">Smart Finder</span>
          </nav>

          <span className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-accent-gold/15 border border-accent-gold/30 text-accent-gold text-xs font-bold uppercase tracking-wider mb-3">
            Hardware Persona Engine
          </span>
          <h1 className="text-3xl sm:text-4xl font-extrabold text-text-primary tracking-tight">
            Find Your Ideal Laptop
          </h1>
          <p className="mt-2 text-sm text-text-secondary max-w-2xl leading-relaxed">
            Specify your primary workflow and budget constraints. Our multi-attribute scoring
            engine ranks 105 machines with transparent match percentages.
          </p>
        </div>
      </section>

      {/* Main Configuration Card */}
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 pt-8 space-y-8">
        <div className="rounded-2xl border border-border-subtle bg-bg-card p-6 sm:p-8 space-y-8">
          {/* Step 1: Priority Persona */}
          <div>
            <div className="flex items-center justify-between mb-3">
              <label className="text-xs font-bold uppercase tracking-wider text-text-primary">
                1. What will you use this laptop for?
              </label>
              <span className="text-[11px] text-accent-gold font-semibold">Priority Persona</span>
            </div>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-3">
              {PRIORITIES.map((p) => {
                const active = priority === p.id;
                return (
                  <button
                    key={p.id}
                    type="button"
                    onClick={() => setPriority(p.id)}
                    className={`text-left rounded-xl p-4 border transition-all duration-200 flex flex-col justify-between ${
                      active
                        ? "border-accent-gold bg-accent-gold/10 shadow-lg shadow-accent-gold/5"
                        : "border-border-subtle bg-bg-deep hover:border-border-glow hover:bg-bg-card-hover"
                    }`}
                  >
                    <div>
                      <div className="text-2xl mb-2">{p.icon}</div>
                      <p className={`text-xs font-bold ${active ? "text-accent-gold" : "text-text-primary"}`}>
                        {p.label}
                      </p>
                      <p className="text-[11px] text-text-muted mt-1 leading-snug">
                        {p.description}
                      </p>
                    </div>
                  </button>
                );
              })}
            </div>
          </div>

          {/* Step 2: Budget Presets */}
          <div>
            <div className="flex items-center justify-between mb-3">
              <label className="text-xs font-bold uppercase tracking-wider text-text-primary">
                2. Select Your Budget Bracket
              </label>
              <span className="text-[11px] text-text-muted">Indian Rupee (INR)</span>
            </div>
            <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-2.5">
              {BUDGET_PRESETS.map((preset, idx) => {
                const active = selectedPresetIndex === idx;
                return (
                  <button
                    key={preset.label}
                    type="button"
                    onClick={() => setSelectedPresetIndex(idx)}
                    className={`px-3 py-2.5 rounded-xl border text-xs font-semibold text-center transition-all ${
                      active
                        ? "border-accent-gold bg-accent-gold text-bg-deep font-bold"
                        : "border-border-subtle bg-bg-deep text-text-secondary hover:text-text-primary hover:border-border-glow"
                    }`}
                  >
                    {preset.label}
                  </button>
                );
              })}
            </div>
          </div>

          {/* Step 3: Hardware Refinements */}
          <div>
            <label className="block text-xs font-bold uppercase tracking-wider text-text-primary mb-3">
              3. Hardware Preferences (Optional)
            </label>
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
              <div>
                <label htmlFor="pref-brand" className="block text-[10px] uppercase tracking-wider text-text-muted mb-1 font-semibold">
                  Preferred Brand
                </label>
                <select
                  id="pref-brand"
                  value={selectedBrand}
                  onChange={(e) => setSelectedBrand(e.target.value)}
                  className="w-full rounded-xl bg-bg-deep border border-border-subtle px-3 py-2 text-xs text-text-primary focus:border-accent-gold focus:outline-none"
                >
                  {brands.map((b) => (
                    <option key={b} value={b}>{b}</option>
                  ))}
                </select>
              </div>

              <div>
                <label htmlFor="pref-ram" className="block text-[10px] uppercase tracking-wider text-text-muted mb-1 font-semibold">
                  Minimum RAM
                </label>
                <select
                  id="pref-ram"
                  value={minRam ?? ""}
                  onChange={(e) => setMinRam(e.target.value ? Number(e.target.value) : undefined)}
                  className="w-full rounded-xl bg-bg-deep border border-border-subtle px-3 py-2 text-xs text-text-primary focus:border-accent-gold focus:outline-none"
                >
                  <option value="">Any Capacity</option>
                  <option value="8">At least 8 GB</option>
                  <option value="16">At least 16 GB (Recommended)</option>
                  <option value="32">At least 32 GB</option>
                </select>
              </div>

              <div>
                <label htmlFor="pref-gpu" className="block text-[10px] uppercase tracking-wider text-text-muted mb-1 font-semibold">
                  Graphics Card Type
                </label>
                <select
                  id="pref-gpu"
                  value={gpuType}
                  onChange={(e) => setGpuType(e.target.value)}
                  className="w-full rounded-xl bg-bg-deep border border-border-subtle px-3 py-2 text-xs text-text-primary focus:border-accent-gold focus:outline-none"
                >
                  <option value="All">All Graphics</option>
                  <option value="Dedicated">Dedicated GPU (NVIDIA RTX / AMD)</option>
                  <option value="Integrated">Integrated GPU (Iris Xe / Arc)</option>
                </select>
              </div>
            </div>
          </div>

          {/* Trigger Button */}
          <div className="pt-4 border-t border-border-subtle flex flex-col sm:flex-row items-center justify-between gap-4">
            <p className="text-xs text-text-muted">
              Evaluates multi-threaded CPU speed, GPU tiers, RAM, and weight.
            </p>
            <button
              type="button"
              onClick={handleRecommend}
              disabled={loading}
              className="w-full sm:w-auto inline-flex items-center justify-center gap-2 px-8 py-3 rounded-xl bg-accent-gold text-bg-deep font-bold text-sm hover:bg-accent-gold-dim transition-all disabled:opacity-50 shadow-lg shadow-accent-gold/10"
            >
              {loading ? (
                <>
                  <svg className="animate-spin h-4 w-4" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                  </svg>
                  <span>Scoring Laptops...</span>
                </>
              ) : (
                <>
                  <span>⚡ Get Ranked Recommendations</span>
                </>
              )}
            </button>
          </div>
        </div>

        {/* Results Showcase */}
        {hasSearched && (
          <section className="space-y-6 pt-4">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
              <div>
                <h2 className="text-xl sm:text-2xl font-bold text-text-primary">
                  Top Recommended Laptops
                </h2>
                <p className="text-xs text-text-muted mt-0.5">
                  Ranked by {priority} compatibility within your specified parameters
                </p>
              </div>

              {recommendations.length > 0 && (
                <div className="flex items-center gap-2 self-start sm:self-auto">
                  <label htmlFor="sort-select" className="text-xs text-text-muted">Sort by:</label>
                  <select
                    id="sort-select"
                    value={sortBy}
                    onChange={(e) => setSortBy(e.target.value as typeof sortBy)}
                    className="rounded-lg bg-bg-card border border-border-subtle px-2.5 py-1.5 text-xs text-text-primary focus:border-accent-gold focus:outline-none"
                  >
                    <option value="match">SmartChoice Match %</option>
                    <option value="price-asc">Price: Low to High</option>
                    <option value="price-desc">Price: High to Low</option>
                    <option value="rating">Expert Rating</option>
                  </select>
                </div>
              )}
            </div>

            {loading ? (
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
                {[1, 2, 3].map((i) => (
                  <div key={i} className="rounded-2xl border border-border-subtle bg-bg-card p-6 animate-pulse space-y-4">
                    <div className="h-4 bg-border-subtle rounded w-1/3" />
                    <div className="h-6 bg-border-subtle rounded w-3/4" />
                    <div className="grid grid-cols-2 gap-2">
                      <div className="h-14 bg-bg-deep rounded-lg" />
                      <div className="h-14 bg-bg-deep rounded-lg" />
                    </div>
                  </div>
                ))}
              </div>
            ) : recommendations.length === 0 ? (
              <div className="rounded-2xl border border-border-subtle bg-bg-card p-12 text-center max-w-md mx-auto">
                <p className="text-sm font-semibold text-text-primary">No laptops matched all constraints</p>
                <p className="text-xs text-text-muted mt-1 mb-4">
                  Try broadening your budget tier or switching preferred brands.
                </p>
                <button
                  type="button"
                  onClick={() => {
                    setSelectedPresetIndex(0);
                    setSelectedBrand("Any Brand");
                    setMinRam(undefined);
                    setGpuType("All");
                  }}
                  className="px-4 py-2 rounded-lg bg-accent-gold text-bg-deep text-xs font-bold"
                >
                  Reset Parameters
                </button>
              </div>
            ) : (
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
                {sortedRecommendations.map((laptop) => (
                  <LaptopCard key={laptop.laptop_id} laptop={laptop} />
                ))}
              </div>
            )}
          </section>
        )}
      </div>
    </main>
  );
}