"use client";

import { useEffect, useRef, useState } from "react";
import Link from "next/link";
import PhoneRecommendationCard from "@/components/PhoneRecommendationCard";
import {
  getPhoneRecommendations,
  getMobileBrands,
  type PhoneRecommendation,
  type PhoneRecommendationResponse,
} from "@/lib/api";

type BudgetPreset = {
  label: string;
  min: number | null;
  max: number | null;
};

const BUDGET_PRESETS: BudgetPreset[] = [
  { label: "₹10K", min: null, max: 10000 },
  { label: "₹15K", min: 10000, max: 15000 },
  { label: "₹20K", min: 15000, max: 20000 },
  { label: "₹30K", min: 20000, max: 30000 },
  { label: "₹40K", min: 28000, max: 40000 },
  { label: "₹50K", min: 35000, max: 50000 },
  { label: "₹75K", min: 50000, max: 75000 },
  { label: "₹1L+", min: 75000, max: null },
];

const RAM_OPTIONS = [
  { label: "Any", value: null },
  { label: "4 GB+", value: 4 },
  { label: "6 GB+", value: 6 },
  { label: "8 GB+", value: 8 },
  { label: "12 GB+", value: 12 },
  { label: "16 GB+", value: 16 },
];

const STORAGE_OPTIONS = [
  { label: "Any", value: null },
  { label: "64 GB+", value: 64 },
  { label: "128 GB+", value: 128 },
  { label: "256 GB+", value: 256 },
  { label: "512 GB+", value: 512 },
];

const REFRESH_RATE_OPTIONS = [
  { label: "Any", value: null },
  { label: "90 Hz+", value: 90 },
  { label: "120 Hz+", value: 120 },
];

const PRIORITIES = [
  { value: "Gaming", label: "Gaming", icon: "🎮", desc: "Top graphics, 120Hz+ refresh rate, fast cooling" },
  { value: "Camera", label: "Camera", icon: "📸", desc: "High megapixel sensor, OIS, crisp low-light photos" },
  { value: "Performance", label: "Performance", icon: "⚡", desc: "Fast processor and smooth multitasking" },
  { value: "Battery", label: "Battery", icon: "🔋", desc: "Long battery life and fast charging" },
  { value: "Value", label: "Value", icon: "💰", desc: "Maximum features for your budget" },
  { value: "Student", label: "Student", icon: "🎓", desc: "Balanced, practical, and affordable" },
  { value: "Everyday", label: "Everyday", icon: "📱", desc: "Dependable everyday smartphone" },
];

function sortRecommendations(list: PhoneRecommendation[], sortKey: string): PhoneRecommendation[] {
  const copy = [...list];
  switch (sortKey) {
    case "price_desc":
      return copy.sort((a, b) => (b.price_inr ?? 0) - (a.price_inr ?? 0));
    case "price_asc":
      return copy.sort((a, b) => (a.price_inr ?? Infinity) - (b.price_inr ?? Infinity));
    case "rating":
      return copy.sort((a, b) => (b.rating ?? 0) - (a.rating ?? 0));
    case "match":
    default:
      return copy.sort((a, b) => (b.match_percentage ?? 0) - (a.match_percentage ?? 0));
  }
}

export default function FindMyPhonePage() {
  const [selectedPreset, setSelectedPreset] = useState<string | null>("₹75K");
  const [customMin, setCustomMin] = useState("");
  const [customMax, setCustomMax] = useState("");
  const [brand, setBrand] = useState("Any Brand");
  const [brands, setBrands] = useState<string[]>([]);
  const [brandsLoading, setBrandsLoading] = useState(true);
  const [minRam, setMinRam] = useState<number | null>(null);
  const [minStorage, setMinStorage] = useState<number | null>(null);
  const [only5G, setOnly5G] = useState(false);
  const [refreshRate, setRefreshRate] = useState<number | null>(null);
  const [priority, setPriority] = useState("Performance");
  const [sortKey, setSortKey] = useState("match");

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [validationError, setValidationError] = useState<string | null>(null);
  const [result, setResult] = useState<PhoneRecommendationResponse | null>(null);

  const resultsRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    getMobileBrands()
      .then((data) => {
        if (data && Array.isArray(data.brands)) {
          setBrands(data.brands);
        }
      })
      .catch(() => {})
      .finally(() => setBrandsLoading(false));
  }, []);

  const formatINR = (v: number) =>
    new Intl.NumberFormat("en-IN", {
      style: "currency",
      currency: "INR",
      maximumFractionDigits: 0,
    }).format(v);

  const handlePresetSelect = (preset: BudgetPreset) => {
    setSelectedPreset(preset.label);
    setCustomMin("");
    setCustomMax("");
    setValidationError(null);
  };

  const handleCustomChange = (minVal: string, maxVal: string) => {
    setSelectedPreset(null);
    setCustomMin(minVal);
    setCustomMax(maxVal);
    setValidationError(null);
  };

  const getEffectiveBounds = (): { min: number | null; max: number | null } => {
    if (selectedPreset) {
      const found = BUDGET_PRESETS.find((p) => p.label === selectedPreset);
      if (found) return { min: found.min, max: found.max };
    }
    const minN = customMin ? Number(customMin) : null;
    const maxN = customMax ? Number(customMax) : null;
    return {
      min: minN && !Number.isNaN(minN) && minN > 0 ? minN : null,
      max: maxN && !Number.isNaN(maxN) && maxN > 0 ? maxN : null,
    };
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setValidationError(null);
    setError(null);

    const { min, max } = getEffectiveBounds();
    if (min !== null && max !== null && min > max) {
      setValidationError("Minimum budget cannot exceed maximum budget.");
      return;
    }

    setLoading(true);
    try {
      const res = await getPhoneRecommendations({
        budget_min: min,
        budget_max: max,
        brand: brand === "Any Brand" ? null : brand,
        min_ram: minRam,
        min_storage: minStorage,
        has_5g: only5G ? true : null,
        refresh_rate_min: refreshRate,
        priority,
      });
      setResult(res);
      setTimeout(() => {
        resultsRef.current?.scrollIntoView({ behavior: "smooth", block: "start" });
      }, 100);
    } catch {
      setError("Unable to calculate recommendations. Make sure the SmartChoice backend is running.");
    } finally {
      setLoading(false);
    }
  };

  const { min: activeMin, max: activeMax } = getEffectiveBounds();
  const sortedList = result ? sortRecommendations(result.recommendations, sortKey) : [];

  return (
    <main className="min-h-screen bg-bg-deep">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <header className="mb-8">
          <div className="hero-gradient rounded-2xl border border-border-subtle px-6 py-8 sm:px-8 sm:py-10">
            <span className="inline-block px-3 py-1 rounded-full bg-accent-gold/15 border border-accent-gold/30 text-accent-gold text-xs font-semibold uppercase tracking-wider mb-3">
              SmartChoice Recommender
            </span>
            <h1 className="text-3xl sm:text-4xl font-bold tracking-tight text-gradient-gold">
              Find Your Perfect Phone
            </h1>
            <p className="mt-3 text-base sm:text-lg text-text-secondary max-w-2xl">
              Tell SmartChoice what matters to you. Our recommendation engine compares
              smartphone specifications and ranks phones based on your priorities.
            </p>
          </div>
        </header>

        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
          {/* Filter Form Sidebar */}
          <form onSubmit={handleSubmit} className="lg:col-span-5 space-y-6">
            <div className="rounded-xl border border-border-subtle bg-bg-card p-5 space-y-6">
              {/* Budget Section */}
              <section>
                <div className="flex items-center justify-between mb-3">
                  <h2 className="text-xs font-semibold uppercase tracking-wider text-text-muted">
                    Your Budget Bracket
                  </h2>
                  {(activeMin || activeMax) && (
                    <span className="text-xs text-accent-gold font-medium">
                      {activeMin ? formatINR(activeMin) : "₹0"} – {activeMax ? formatINR(activeMax) : "Above"}
                    </span>
                  )}
                </div>

                <div className="grid grid-cols-4 gap-2">
                  {BUDGET_PRESETS.map((p) => {
                    const isSelected = selectedPreset === p.label;
                    return (
                      <button
                        key={p.label}
                        type="button"
                        onClick={() => handlePresetSelect(p)}
                        className={`px-3 py-2 rounded-lg text-xs font-semibold border transition-all text-center ${
                          isSelected
                            ? "bg-accent-gold text-bg-deep border-accent-gold shadow-md"
                            : "border-border-subtle bg-bg-deep text-text-secondary hover:border-border-glow hover:text-text-primary"
                        }`}
                      >
                        {p.label}
                      </button>
                    );
                  })}
                </div>

                {/* Custom Budget Range */}
                <div className="mt-4 pt-3 border-t border-border-subtle">
                  <p className="text-[11px] text-text-muted mb-2">Or enter custom price range (INR):</p>
                  <div className="grid grid-cols-2 gap-2">
                    <input
                      type="number"
                      placeholder="Min (e.g. 50000)"
                      value={customMin}
                      onChange={(e) => handleCustomChange(e.target.value, customMax)}
                      className="w-full rounded-lg border border-border-subtle bg-bg-deep px-3 py-2 text-xs text-text-primary placeholder-text-muted focus:outline-none focus:border-accent-gold"
                    />
                    <input
                      type="number"
                      placeholder="Max (e.g. 75000)"
                      value={customMax}
                      onChange={(e) => handleCustomChange(customMin, e.target.value)}
                      className="w-full rounded-lg border border-border-subtle bg-bg-deep px-3 py-2 text-xs text-text-primary placeholder-text-muted focus:outline-none focus:border-accent-gold"
                    />
                  </div>
                </div>
              </section>

              {/* Priority Section */}
              <section>
                <h2 className="text-xs font-semibold uppercase tracking-wider text-text-muted mb-3">
                  Primary Priority
                </h2>
                <div className="grid grid-cols-2 gap-2">
                  {PRIORITIES.map((item) => (
                    <button
                      key={item.value}
                      type="button"
                      onClick={() => setPriority(item.value)}
                      className={`p-2.5 rounded-lg border text-left transition-all ${
                        priority === item.value
                          ? "bg-accent-gold/15 border-accent-gold text-accent-gold"
                          : "border-border-subtle bg-bg-deep text-text-secondary hover:border-border-glow"
                      }`}
                    >
                      <div className="flex items-center gap-1.5 font-medium text-xs">
                        <span>{item.icon}</span>
                        <span>{item.label}</span>
                      </div>
                    </button>
                  ))}
                </div>
              </section>

              {/* Hardware Specifications */}
              <section className="space-y-4">
                <h2 className="text-xs font-semibold uppercase tracking-wider text-text-muted">
                  Minimum Requirements
                </h2>

                <div>
                  <label htmlFor="pref-brand" className="block text-xs text-text-muted mb-1">
                    Preferred Brand
                  </label>
                  <select
                    id="pref-brand"
                    value={brand}
                    onChange={(e) => setBrand(e.target.value)}
                    disabled={brandsLoading}
                    className="w-full rounded-lg border border-border-subtle bg-bg-deep px-3 py-2 text-sm text-text-primary focus:outline-none focus:border-accent-gold"
                  >
                    <option value="Any Brand">Any Brand</option>
                    {brands.map((b) => (
                      <option key={b} value={b}>{b}</option>
                    ))}
                  </select>
                </div>

                <div className="grid grid-cols-2 gap-3">
                  <div>
                    <label htmlFor="pref-ram" className="block text-xs text-text-muted mb-1">RAM</label>
                    <select
                      id="pref-ram"
                      value={minRam ?? ""}
                      onChange={(e) => setMinRam(e.target.value ? Number(e.target.value) : null)}
                      className="w-full rounded-lg border border-border-subtle bg-bg-deep px-3 py-2 text-sm text-text-primary focus:outline-none focus:border-accent-gold"
                    >
                      {RAM_OPTIONS.map((o) => (
                        <option key={o.label} value={o.value ?? ""}>{o.label}</option>
                      ))}
                    </select>
                  </div>
                  <div>
                    <label htmlFor="pref-storage" className="block text-xs text-text-muted mb-1">Storage</label>
                    <select
                      id="pref-storage"
                      value={minStorage ?? ""}
                      onChange={(e) => setMinStorage(e.target.value ? Number(e.target.value) : null)}
                      className="w-full rounded-lg border border-border-subtle bg-bg-deep px-3 py-2 text-sm text-text-primary focus:outline-none focus:border-accent-gold"
                    >
                      {STORAGE_OPTIONS.map((o) => (
                        <option key={o.label} value={o.value ?? ""}>{o.label}</option>
                      ))}
                    </select>
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-3">
                  <div>
                    <label htmlFor="pref-refresh" className="block text-xs text-text-muted mb-1">Refresh Rate</label>
                    <select
                      id="pref-refresh"
                      value={refreshRate ?? ""}
                      onChange={(e) => setRefreshRate(e.target.value ? Number(e.target.value) : null)}
                      className="w-full rounded-lg border border-border-subtle bg-bg-deep px-3 py-2 text-sm text-text-primary focus:outline-none focus:border-accent-gold"
                    >
                      {REFRESH_RATE_OPTIONS.map((o) => (
                        <option key={o.label} value={o.value ?? ""}>{o.label}</option>
                      ))}
                    </select>
                  </div>
                  <div>
                    <label htmlFor="pref-5g" className="block text-xs text-text-muted mb-1">Connectivity</label>
                    <select
                      id="pref-5g"
                      value={only5G ? "yes" : "all"}
                      onChange={(e) => setOnly5G(e.target.value === "yes")}
                      className="w-full rounded-lg border border-border-subtle bg-bg-deep px-3 py-2 text-sm text-text-primary focus:outline-none focus:border-accent-gold"
                    >
                      <option value="all">Any Network</option>
                      <option value="yes">5G Only</option>
                    </select>
                  </div>
                </div>
              </section>

              {validationError && (
                <div className="rounded-lg bg-red-500/10 border border-red-500/30 p-3 text-xs text-red-400">
                  {validationError}
                </div>
              )}

              {/* Submit CTA */}
              <button
                type="submit"
                disabled={loading}
                className="w-full py-3 rounded-lg bg-accent-gold text-bg-deep font-bold text-sm hover:bg-accent-gold-dim transition-colors disabled:opacity-50 flex items-center justify-center gap-2"
              >
                {loading ? (
                  <>
                    <svg className="animate-spin h-4 w-4" viewBox="0 0 24 24" fill="none">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
                    </svg>
                    Matching Handsets...
                  </>
                ) : (
                  <>
                    Find My Phone
                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M14 5l7 7m0 0l-7 7m7-7H3" />
                    </svg>
                  </>
                )}
              </button>
            </div>
          </form>

          {/* Results Area */}
          <div ref={resultsRef} className="lg:col-span-7">
            {error && (
              <div className="rounded-xl border border-red-500/30 bg-red-500/10 p-6 text-center mb-6">
                <p className="text-sm text-red-400">{error}</p>
              </div>
            )}

            {!result && !loading && (
              <div className="rounded-xl border border-border-subtle bg-bg-card p-8 text-center text-text-muted">
                <div className="w-14 h-14 rounded-full bg-accent-gold/10 text-accent-gold flex items-center justify-center mx-auto mb-3 text-2xl">
                  📱
                </div>
                <h3 className="text-base font-semibold text-text-primary mb-1">
                  Ready to Compare
                </h3>
                <p className="text-xs text-text-muted max-w-sm mx-auto">
                  Select your budget bracket, brand, and hardware priorities on the left, then click Find My Phone.
                </p>
              </div>
            )}

            {result && result.total === 0 && !loading && (
              <div className="rounded-xl border border-border-subtle bg-bg-card p-8 text-center">
                <p className="text-base font-medium text-text-primary">No matching phones found</p>
                <p className="text-xs text-text-muted mt-1">
                  Try broadening your budget range or lowering minimum RAM/storage requirements.
                </p>
              </div>
            )}

            {result && result.total > 0 && (
              <div className="space-y-4">
                {/* Result Controls Header */}
                <div className="rounded-xl border border-border-subtle bg-bg-card p-4 flex flex-col sm:flex-row sm:items-center justify-between gap-3">
                  <div>
                    <h2 className="text-sm font-bold text-text-primary">
                      SmartChoice Recommendations
                    </h2>
                    <p className="text-xs text-text-muted">
                      {result.total} models matched in {activeMin ? formatINR(activeMin) : "₹0"} – {activeMax ? formatINR(activeMax) : "Above"}
                    </p>
                  </div>

                  {/* Interactive Sort Dropdown */}
                  <div className="flex items-center gap-2">
                    <label htmlFor="sort-control" className="text-xs text-text-muted shrink-0">
                      Sort by:
                    </label>
                    <select
                      id="sort-control"
                      value={sortKey}
                      onChange={(e) => setSortKey(e.target.value)}
                      className="rounded-lg border border-border-subtle bg-bg-deep px-3 py-1.5 text-xs text-text-primary focus:outline-none focus:border-accent-gold font-medium"
                    >
                      <option value="match">SmartChoice Match (Highest)</option>
                      <option value="price_desc">Price: High to Low</option>
                      <option value="price_asc">Price: Low to High</option>
                      <option value="rating">Rating: High to Low</option>
                    </select>
                  </div>
                </div>

                {/* Recommendations Grid */}
                <div className="grid grid-cols-1 gap-4">
                  {sortedList.map((phone) => (
                    <PhoneRecommendationCard key={phone.phone_id} phone={phone} />
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </main>
  );
}