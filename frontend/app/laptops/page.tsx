"use client";

import { useEffect, useState, useCallback, Suspense } from "react";
import { useSearchParams } from "next/navigation";
import Link from "next/link";
import LaptopCard from "@/components/LaptopCard";
import { getLaptops, getLaptopBrands, type Laptop } from "@/lib/api";

function LaptopsCatalogContent() {
  const searchParams = useSearchParams();
  const brandQuery = searchParams.get("brand") || "Any Brand";

  const [laptops, setLaptops] = useState<Laptop[]>([]);
  const [brands, setBrands] = useState<string[]>([]);
  const [total, setTotal] = useState(0);
  const [totalPages, setTotalPages] = useState(1);
  const [page, setPage] = useState(1);
  const [loading, setLoading] = useState(true);

  // Filter States
  const [search, setSearch] = useState("");
  const [selectedBrand, setSelectedBrand] = useState(brandQuery);
  const [selectedRam, setSelectedRam] = useState<number | undefined>(undefined);
  const [selectedGpu, setSelectedGpu] = useState("All");
  const [maxPrice, setMaxPrice] = useState<number | undefined>(undefined);

  // Sync selectedBrand whenever the URL query parameter changes
  useEffect(() => {
    const qBrand = searchParams.get("brand");
    if (qBrand) {
      setSelectedBrand(qBrand);
      setPage(1);
    }
  }, [searchParams]);

  // Fetch unique brands once
  useEffect(() => {
    getLaptopBrands()
      .then((res) => {
        if (res && res.brands) setBrands(["Any Brand", ...res.brands]);
      })
      .catch(() => {});
  }, []);

  // Fetch catalog
  const loadData = useCallback(() => {
    setLoading(true);
    getLaptops({
      page,
      limit: 12,
      brand: selectedBrand === "Any Brand" ? undefined : selectedBrand,
      min_ram: selectedRam,
      gpu_type: selectedGpu === "All" ? undefined : selectedGpu,
      max_price: maxPrice,
      q: search.trim() || undefined,
    })
      .then((res) => {
        setLaptops(res.laptops || []);
        setTotal(res.total || 0);
        setTotalPages(res.total_pages || 1);
      })
      .catch(() => {
        setLaptops([]);
      })
      .finally(() => setLoading(false));
  }, [page, selectedBrand, selectedRam, selectedGpu, maxPrice, search]);

  useEffect(() => {
    loadData();
  }, [loadData]);

  const handleReset = () => {
    setSearch("");
    setSelectedBrand("Any Brand");
    setSelectedRam(undefined);
    setSelectedGpu("All");
    setMaxPrice(undefined);
    setPage(1);
  };

  return (
    <main className="min-h-screen bg-bg-deep pb-16">
      {/* Header Banner */}
      <section className="border-b border-border-subtle bg-bg-card/40 backdrop-blur-md pt-10 pb-8">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
            <div>
              <span className="text-xs font-bold uppercase tracking-wider text-accent-gold">
                Hardware Catalog
              </span>
              <h1 className="text-3xl sm:text-4xl font-extrabold text-text-primary mt-1">
                Laptops Explorer
              </h1>
              <p className="text-xs sm:text-sm text-text-muted mt-1.5">
                Browse 105 curated laptops across Apple, ASUS, Lenovo, HP, Dell, and Acer with verified benchmarks.
              </p>
            </div>

            <Link
              href="/laptops/find"
              className="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl bg-accent-gold text-bg-deep font-bold text-xs sm:text-sm hover:bg-accent-gold-dim transition-colors self-start md:self-auto shadow-lg shadow-accent-gold/10"
            >
              ⚡ Find My Laptop
            </Link>
          </div>

          {/* Search & Filter Controls */}
          <div className="mt-8 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-3">
            {/* Search Input */}
            <div className="lg:col-span-2">
              <label htmlFor="search-input" className="block text-[10px] uppercase tracking-wider text-text-muted mb-1 font-semibold">
                Search Model or Processor
              </label>
              <input
                id="search-input"
                type="text"
                placeholder="e.g. RTX 4060, M3, i5-13500H, OLED..."
                value={search}
                onChange={(e) => {
                  setSearch(e.target.value);
                  setPage(1);
                }}
                className="w-full rounded-xl bg-bg-deep border border-border-subtle px-3.5 py-2 text-xs text-text-primary placeholder:text-text-muted focus:border-accent-gold focus:outline-none transition-colors"
              />
            </div>

            {/* Brand Filter */}
            <div>
              <label htmlFor="brand-select" className="block text-[10px] uppercase tracking-wider text-text-muted mb-1 font-semibold">
                Brand
              </label>
              <select
                id="brand-select"
                value={selectedBrand}
                onChange={(e) => {
                  setSelectedBrand(e.target.value);
                  setPage(1);
                }}
                className="w-full rounded-xl bg-bg-deep border border-border-subtle px-3 py-2 text-xs text-text-primary focus:border-accent-gold focus:outline-none transition-colors"
              >
                {brands.map((b) => (
                  <option key={b} value={b}>{b}</option>
                ))}
              </select>
            </div>

            {/* RAM Filter */}
            <div>
              <label htmlFor="ram-select" className="block text-[10px] uppercase tracking-wider text-text-muted mb-1 font-semibold">
                Min RAM
              </label>
              <select
                id="ram-select"
                value={selectedRam ?? ""}
                onChange={(e) => {
                  setSelectedRam(e.target.value ? Number(e.target.value) : undefined);
                  setPage(1);
                }}
                className="w-full rounded-xl bg-bg-deep border border-border-subtle px-3 py-2 text-xs text-text-primary focus:border-accent-gold focus:outline-none transition-colors"
              >
                <option value="">Any RAM</option>
                <option value="8">8 GB or more</option>
                <option value="16">16 GB or more</option>
                <option value="32">32 GB or more</option>
              </select>
            </div>

            {/* GPU Type */}
            <div>
              <label htmlFor="gpu-select" className="block text-[10px] uppercase tracking-wider text-text-muted mb-1 font-semibold">
                GPU Type
              </label>
              <select
                id="gpu-select"
                value={selectedGpu}
                onChange={(e) => {
                  setSelectedGpu(e.target.value);
                  setPage(1);
                }}
                className="w-full rounded-xl bg-bg-deep border border-border-subtle px-3 py-2 text-xs text-text-primary focus:border-accent-gold focus:outline-none transition-colors"
              >
                <option value="All">All Graphics</option>
                <option value="Dedicated">Dedicated (RTX/Radeon)</option>
                <option value="Integrated">Integrated (Iris Xe/Arc)</option>
              </select>
            </div>
          </div>

          {/* Filter Status & Reset */}
          <div className="mt-4 flex items-center justify-between text-xs text-text-muted">
            <span>
              Showing {laptops.length} of {total} laptops {selectedBrand !== "Any Brand" ? `for ${selectedBrand}` : ""}
            </span>
            {(search || selectedBrand !== "Any Brand" || selectedRam || selectedGpu !== "All") && (
              <button
                type="button"
                onClick={handleReset}
                className="text-accent-gold hover:underline font-semibold"
              >
                Reset All Filters
              </button>
            )}
          </div>
        </div>
      </section>

      {/* Catalog Grid */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-8">
        {loading ? (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {[1, 2, 3, 4, 5, 6].map((i) => (
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
        ) : laptops.length === 0 ? (
          <div className="rounded-2xl border border-border-subtle bg-bg-card p-12 text-center max-w-md mx-auto">
            <p className="text-sm font-semibold text-text-primary">No laptops match your criteria</p>
            <p className="text-xs text-text-muted mt-1 mb-4">Try clearing filters or adjusting your search term.</p>
            <button
              type="button"
              onClick={handleReset}
              className="px-4 py-2 rounded-lg bg-accent-gold text-bg-deep text-xs font-bold"
            >
              Reset Filters
            </button>
          </div>
        ) : (
          <>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
              {laptops.map((l) => (
                <LaptopCard key={l.laptop_id} laptop={l} />
              ))}
            </div>

            {/* Pagination */}
            {totalPages > 1 && (
              <div className="mt-10 flex items-center justify-center gap-2">
                <button
                  type="button"
                  disabled={page <= 1}
                  onClick={() => setPage((p) => Math.max(1, p - 1))}
                  className="px-4 py-2 rounded-lg bg-bg-card border border-border-subtle text-xs font-medium text-text-primary disabled:opacity-40 disabled:cursor-not-allowed hover:border-accent-gold"
                >
                  ← Previous
                </button>
                <span className="text-xs text-text-muted px-3">
                  Page {page} of {totalPages}
                </span>
                <button
                  type="button"
                  disabled={page >= totalPages}
                  onClick={() => setPage((p) => Math.min(totalPages, p + 1))}
                  className="px-4 py-2 rounded-lg bg-bg-card border border-border-subtle text-xs font-medium text-text-primary disabled:opacity-40 disabled:cursor-not-allowed hover:border-accent-gold"
                >
                  Next →
                </button>
              </div>
            )}
          </>
        )}
      </section>
    </main>
  );
}

export default function LaptopsCatalogPage() {
  return (
    <Suspense
      fallback={
        <div className="min-h-screen bg-bg-deep flex items-center justify-center p-8">
          <div className="animate-pulse text-sm text-text-muted">Loading laptops catalog...</div>
        </div>
      }
    >
      <LaptopsCatalogContent />
    </Suspense>
  );
}