"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import PhoneCard from "@/components/PhoneCard";
import {
  getMobiles,
  searchMobiles,
  type MobileCatalogResponse,
} from "@/lib/api";

const PAGE_SIZE = 20;

function sortMobiles(mobiles: any[], sort: string) {
  const list = [...mobiles];
  const num = (v: any) => (v === null || v === undefined ? -Infinity : Number(v));
  switch (sort) {
    case "price_asc":
      return list.sort((a, b) => num(a.price_inr) - num(b.price_inr));
    case "price_desc":
      return list.sort((a, b) => num(b.price_inr) - num(a.price_inr));
    case "rating":
      return list.sort((a, b) => num(b.rating) - num(a.rating));
    case "ram":
      return list.sort((a, b) => num(b.ram_gb) - num(a.ram_gb));
    case "storage":
      return list.sort((a, b) => num(b.storage_gb) - num(a.storage_gb));
    default:
      return list;
  }
}

export default function MobilesPage() {
  const [data, setData] = useState<MobileCatalogResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const [searchQuery, setSearchQuery] = useState("");
  const [brand, setBrand] = useState("All");
  const [minPrice, setMinPrice] = useState("");
  const [maxPrice, setMaxPrice] = useState("");
  const [minRam, setMinRam] = useState(0);
  const [minStorage, setMinStorage] = useState(0);
  const [only5G, setOnly5G] = useState(false);
  const [sort, setSort] = useState("default");
  const [page, setPage] = useState(1);
  const [brands, setBrands] = useState<string[]>([]);

  const fetchCatalog = async (targetPage: number, query: string) => {
    try {
      setLoading(true);
      setError(null);
      const params: Parameters<typeof searchMobiles>[0] = {
        page: targetPage,
        limit: PAGE_SIZE,
      };
      const q = query.trim();
      if (q) params.q = q;
      if (brand !== "All") params.brand = brand;
      if (minPrice) {
        const n = Number(minPrice);
        if (!Number.isNaN(n) && n > 0) params.min_price = n;
      }
      if (maxPrice) {
        const n = Number(maxPrice);
        if (!Number.isNaN(n) && n >= 0) params.max_price = n;
      }
      if (minRam > 0) params.min_ram = minRam;
      if (minStorage > 0) params.min_storage = minStorage;
      if (only5G) params.has_5g = true;

      const res =
        q || brand !== "All" || minPrice || maxPrice || minRam > 0 || minStorage > 0 || only5G
          ? await searchMobiles(params)
          : await getMobiles(targetPage, PAGE_SIZE);
      setData(res);
    } catch {
      setError("Unable to load smartphones. Make sure the SmartChoice backend is running.");
    } finally {
      setLoading(false);
    }
  };

  // Debounced search — wait 350ms after the user stops typing before fetching
  useEffect(() => {
    const timer = setTimeout(() => {
      fetchCatalog(1, searchQuery);
    }, 350);
    return () => clearTimeout(timer);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [searchQuery, brand, minPrice, maxPrice, minRam, minStorage, only5G]);

  // Initial load
  useEffect(() => {
    fetchCatalog(1, searchQuery);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  // Discover available brands from the catalog
  useEffect(() => {
    if (!data) return;
    const unique = Array.from(
      new Set(data.mobiles.map((m) => m.brand).filter(Boolean))
    ).sort();
    setBrands(unique);
  }, [data]);

  const RAM_OPTIONS = [
    { label: "Any", value: 0 },
    { label: "4 GB+", value: 4 },
    { label: "6 GB+", value: 6 },
    { label: "8 GB+", value: 8 },
    { label: "12 GB+", value: 12 },
    { label: "16 GB+", value: 16 },
  ];

  const STORAGE_OPTIONS = [
    { label: "Any", value: 0 },
    { label: "64 GB+", value: 64 },
    { label: "128 GB+", value: 128 },
    { label: "256 GB+", value: 256 },
    { label: "512 GB+", value: 512 },
  ];

  const SORT_OPTIONS = [
    { label: "Recommended", value: "default" },
    { label: "Price: Low to High", value: "price_asc" },
    { label: "Price: High to Low", value: "price_desc" },
    { label: "Rating", value: "rating" },
    { label: "RAM", value: "ram" },
    { label: "Storage", value: "storage" },
  ];

  const sorted = data ? sortMobiles(data.mobiles, sort) : [];

  return (
    <div className="min-h-screen bg-bg-deep">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <header className="mb-8">
          <div className="hero-gradient rounded-2xl border border-border-subtle px-6 py-8 sm:px-8 sm:py-10">
            <div className="max-w-2xl">
              <h1 className="text-3xl sm:text-4xl font-bold tracking-tight text-gradient-gold">
                Choose Your Next Smartphone
              </h1>
              <p className="mt-3 text-base sm:text-lg text-text-secondary">
                Compare phones based on specifications, budget, and priorities.
                SmartChoice helps you find the right device for your needs.
              </p>
              <div className="mt-5">
                <Link
                  href="/mobiles/find"
                  className="inline-flex items-center gap-2 px-5 py-2.5 rounded-lg bg-accent-gold text-bg-deep font-semibold hover:bg-accent-gold-dim transition-colors"
                >
                  Find My Phone
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                  </svg>
                </Link>
              </div>
            </div>
          </div>
        </header>

        {/* Search + filters */}
        <div className="mb-6 rounded-xl border border-border-subtle bg-bg-card p-4 sm:p-5">
          <div className="flex flex-col lg:flex-row gap-4">
            <div className="flex-1">
              <label htmlFor="phone-search" className="sr-only">Search phones</label>
              <div className="relative">
                <svg className="w-4 h-4 text-text-muted absolute left-3 top-1/2 -translate-y-1/2" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
                <input
                  id="phone-search"
                  type="search"
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  placeholder="Search phones, brands, processors..."
                  className="w-full rounded-lg border border-border-subtle bg-bg-deep pl-9 pr-3 py-2 text-sm text-text-primary placeholder-text-muted focus:outline-none focus:border-accent-gold"
                />
              </div>
            </div>
            <div className="flex flex-wrap items-center gap-2">
              <label htmlFor="brand-filter" className="sr-only">Brand</label>
              <select
                id="brand-filter"
                value={brand}
                onChange={(e) => setBrand(e.target.value)}
                className="rounded-lg border border-border-subtle bg-bg-deep px-3 py-2 text-sm text-text-primary focus:outline-none focus:border-accent-gold"
              >
                <option value="All">All Brands</option>
                {brands.map((b) => (
                  <option key={b} value={b}>{b}</option>
                ))}
              </select>
              <label htmlFor="sort-filter" className="sr-only">Sort</label>
              <select
                id="sort-filter"
                value={sort}
                onChange={(e) => setSort(e.target.value)}
                className="rounded-lg border border-border-subtle bg-bg-deep px-3 py-2 text-sm text-text-primary focus:outline-none focus:border-accent-gold"
              >
                {SORT_OPTIONS.map((o) => (
                  <option key={o.value} value={o.value}>{o.label}</option>
                ))}
              </select>
            </div>
          </div>

          <div className="mt-4 grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
            <div>
              <label htmlFor="min-price" className="block text-xs text-text-muted mb-1">Min Price (INR)</label>
              <input
                id="min-price"
                type="number"
                value={minPrice}
                onChange={(e) => setMinPrice(e.target.value)}
                placeholder="e.g. 10000"
                className="w-full rounded-lg border border-border-subtle bg-bg-deep px-3 py-2 text-sm text-text-primary focus:outline-none focus:border-accent-gold"
              />
            </div>
            <div>
              <label htmlFor="max-price" className="block text-xs text-text-muted mb-1">Max Price (INR)</label>
              <input
                id="max-price"
                type="number"
                value={maxPrice}
                onChange={(e) => setMaxPrice(e.target.value)}
                placeholder="Any"
                className="w-full rounded-lg border border-border-subtle bg-bg-deep px-3 py-2 text-sm text-text-primary focus:outline-none focus:border-accent-gold"
              />
            </div>
            <div>
              <label htmlFor="min-ram" className="block text-xs text-text-muted mb-1">RAM</label>
              <select
                id="min-ram"
                value={minRam}
                onChange={(e) => setMinRam(Number(e.target.value))}
                className="w-full rounded-lg border border-border-subtle bg-bg-deep px-3 py-2 text-sm text-text-primary focus:outline-none focus:border-accent-gold"
              >
                {RAM_OPTIONS.map((o) => (
                  <option key={o.value} value={o.value}>{o.label}</option>
                ))}
              </select>
            </div>
            <div>
              <label htmlFor="min-storage" className="block text-xs text-text-muted mb-1">Storage</label>
              <select
                id="min-storage"
                value={minStorage}
                onChange={(e) => setMinStorage(Number(e.target.value))}
                className="w-full rounded-lg border border-border-subtle bg-bg-deep px-3 py-2 text-sm text-text-primary focus:outline-none focus:border-accent-gold"
              >
                {STORAGE_OPTIONS.map((o) => (
                  <option key={o.value} value={o.value}>{o.label}</option>
                ))}
              </select>
            </div>
            <div>
              <label htmlFor="5g-filter" className="block text-xs text-text-muted mb-1">Connectivity</label>
              <select
                id="5g-filter"
                value={only5G ? "yes" : "all"}
                onChange={(e) => setOnly5G(e.target.value === "yes")}
                className="w-full rounded-lg border border-border-subtle bg-bg-deep px-3 py-2 text-sm text-text-primary focus:outline-none focus:border-accent-gold"
              >
                <option value="all">All</option>
                <option value="yes">5G Only</option>
              </select>
            </div>
            <div className="flex items-end">
              <button
                type="button"
                onClick={() => {
                  setSearchQuery("");
                  setBrand("All");
                  setMinPrice("");
                  setMaxPrice("");
                  setMinRam(0);
                  setMinStorage(0);
                  setOnly5G(false);
                }}
                className="w-full rounded-lg border border-border-subtle bg-bg-deep px-3 py-2 text-sm text-text-secondary hover:bg-bg-card-hover hover:border-border-glow transition-colors"
              >
                Clear Filters
              </button>
            </div>
          </div>
        </div>

        {/* Results */}
        <div>
          <div className="flex items-center justify-between mb-4">
            <p className="text-sm text-text-muted">
              {loading ? "Loading..." : data ? `${data.total} smartphone${data.total === 1 ? "" : "s"}` : ""}
            </p>
          </div>

          {error && (
            <div className="mb-4 rounded-xl border border-red-500/30 bg-red-500/10 p-6 text-center">
              <p className="text-sm text-red-400">{error}</p>
              <button
                type="button"
                onClick={() => fetchCatalog(page, searchQuery)}
                className="mt-3 inline-flex items-center gap-2 px-4 py-2 rounded-lg bg-accent-gold/10 text-accent-gold font-medium hover:bg-accent-gold/20 transition-colors border border-accent-gold/30"
              >
                Retry
              </button>
            </div>
          )}

          {loading && !data && (
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
              {Array.from({ length: 8 }).map((_, i) => (
                <div key={i} className="rounded-xl border border-border-subtle bg-bg-card p-4 animate-pulse">
                  <div className="flex gap-3">
                    <div className="w-20 h-28 shrink-0 rounded-lg bg-bg-deep" />
                    <div className="flex-1 space-y-2">
                      <div className="h-3 w-16 rounded bg-bg-deep" />
                      <div className="h-4 w-32 rounded bg-bg-deep" />
                      <div className="h-3 w-24 rounded bg-bg-deep mt-2" />
                      <div className="h-3 w-20 rounded bg-bg-deep" />
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}

          {!loading && data && sorted.length === 0 && (
            <div className="rounded-xl border border-border-subtle bg-bg-card p-10 text-center">
              <svg className="w-10 h-10 text-text-muted mx-auto mb-3" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <p className="text-text-primary font-medium">No phones found</p>
              <p className="text-sm text-text-muted mt-1">Try changing your filters or search terms.</p>
              <button
                type="button"
                onClick={() => {
                  setSearchQuery("");
                  setBrand("All");
                  setMinPrice("");
                  setMaxPrice("");
                  setMinRam(0);
                  setMinStorage(0);
                  setOnly5G(false);
                }}
                className="mt-4 inline-flex items-center gap-2 px-4 py-2 rounded-lg bg-accent-gold/10 text-accent-gold font-medium hover:bg-accent-gold/20 transition-colors border border-accent-gold/30"
              >
                Clear Filters
              </button>
            </div>
          )}

          {!loading && data && sorted.length > 0 && (
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
              {sorted.map((phone) => (
                <PhoneCard key={phone.phone_id} phone={phone} />
              ))}
            </div>
          )}

          {!loading && data && data.total_pages > 1 && (
            <div className="flex items-center justify-center gap-3 mt-8">
              <button
                type="button"
                disabled={page === 1}
                onClick={() => {
                  const p = page - 1;
                  setPage(p);
                  fetchCatalog(p, searchQuery);
                }}
                className="inline-flex items-center gap-1 px-3 py-2 rounded-lg border border-border-subtle bg-bg-deep text-sm text-text-secondary disabled:opacity-40 disabled:cursor-not-allowed hover:bg-bg-card-hover hover:border-border-glow transition-colors"
              >
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
                </svg>
                Previous
              </button>
              <span className="text-sm text-text-muted">
                Page {page} of {data.total_pages}
              </span>
              <button
                type="button"
                disabled={page >= data.total_pages}
                onClick={() => {
                  const p = page + 1;
                  setPage(p);
                  fetchCatalog(p, searchQuery);
                }}
                className="inline-flex items-center gap-1 px-3 py-2 rounded-lg border border-border-subtle bg-bg-deep text-sm text-text-secondary disabled:opacity-40 disabled:cursor-not-allowed hover:bg-bg-card-hover hover:border-border-glow transition-colors"
              >
                Next
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                </svg>
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}