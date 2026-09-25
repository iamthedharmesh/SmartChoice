"use client";

import Link from "next/link";
import { type Laptop } from "@/lib/api";

interface LaptopCardProps {
  laptop: Laptop;
}

export default function LaptopCard({ laptop }: LaptopCardProps) {
  const formatINR = (val: number) =>
    new Intl.NumberFormat("en-IN", {
      style: "currency",
      currency: "INR",
      maximumFractionDigits: 0,
    }).format(val);

  const isDedicatedGPU = laptop.gpu_type?.toLowerCase() === "dedicated";
  const laptopHref = `/laptop/${laptop.laptop_id}`;

  const handleScrollTop = () => {
    if (typeof window !== "undefined") {
      window.scrollTo({ top: 0, behavior: "instant" });
    }
  };

  return (
    <Link
      href={laptopHref}
      onClick={handleScrollTop}
      className="group relative flex flex-col rounded-2xl border border-border-subtle bg-bg-card p-5 transition-all duration-300 hover:border-accent-gold/40 hover:shadow-gold cursor-pointer"
    >
      {/* Top Brand & Match/Rating Row */}
      <div className="flex items-center justify-between gap-2 mb-3">
        <span className="text-[11px] font-extrabold uppercase tracking-wider text-accent-gold">
          {laptop.brand}
        </span>
        {laptop.match_percentage !== undefined ? (
          <span className="px-2.5 py-0.5 rounded-full bg-accent-gold/15 text-accent-gold border border-accent-gold/30 text-xs font-bold">
            {laptop.match_percentage.toFixed(0)}% Match
          </span>
        ) : (
          <span className="inline-flex items-center gap-1 text-xs font-semibold text-text-muted">
            ★ {laptop.rating?.toFixed(1) || "85.0"}
          </span>
        )}
      </div>

      {/* Model Name */}
      <h3 className="text-base font-bold text-text-primary line-clamp-2 min-h-[48px] group-hover:text-accent-gold transition-colors">
        {laptop.model}
      </h3>

      {/* Key Hardware Tag Grid */}
      <div className="my-4 grid grid-cols-2 gap-2 text-xs">
        <div className="rounded-lg bg-bg-deep border border-border-subtle/60 p-2">
          <p className="text-[10px] uppercase tracking-wider text-text-muted">CPU</p>
          <p className="font-semibold text-text-primary truncate mt-0.5">
            {laptop.processor_model}
          </p>
          <p className="text-[10px] text-text-muted">{laptop.cpu_cores} Cores</p>
        </div>

        <div className="rounded-lg bg-bg-deep border border-border-subtle/60 p-2">
          <p className="text-[10px] uppercase tracking-wider text-text-muted">RAM & Storage</p>
          <p className="font-semibold text-text-primary mt-0.5">
            {laptop.ram_gb}GB {laptop.ram_type}
          </p>
          <p className="text-[10px] text-text-muted truncate">{laptop.storage_gb}GB SSD</p>
        </div>

        <div className="rounded-lg bg-bg-deep border border-border-subtle/60 p-2">
          <p className="text-[10px] uppercase tracking-wider text-text-muted">Graphics</p>
          <p className={`font-semibold truncate mt-0.5 ${isDedicatedGPU ? "text-emerald-400" : "text-text-primary"}`}>
            {laptop.gpu_model}
          </p>
          <p className="text-[10px] text-text-muted capitalize">{laptop.gpu_type}</p>
        </div>

        <div className="rounded-lg bg-bg-deep border border-border-subtle/60 p-2">
          <p className="text-[10px] uppercase tracking-wider text-text-muted">Display</p>
          <p className="font-semibold text-text-primary mt-0.5 truncate">
            {laptop.display_size_inch}&quot; {laptop.refresh_rate_hz}Hz
          </p>
          <p className="text-[10px] text-text-muted truncate">{laptop.resolution.split(" ")[0]}</p>
        </div>
      </div>

      {/* Recommendation Reasons (if present) */}
      {laptop.reasons && laptop.reasons.length > 0 && (
        <div className="mb-4 rounded-xl bg-accent-gold/5 border border-accent-gold/15 p-2.5 space-y-1">
          {laptop.reasons.slice(0, 2).map((r, i) => (
            <p key={i} className="text-[11px] text-text-secondary flex items-start gap-1.5 leading-snug">
              <span className="text-accent-gold font-bold">✓</span>
              <span>{r}</span>
            </p>
          ))}
        </div>
      )}

      {/* Footer: Price + Action Button */}
      <div className="mt-auto pt-3 border-t border-border-subtle flex items-center justify-between">
        <div>
          <p className="text-[10px] text-text-muted">Price</p>
          <p className="text-lg font-black text-accent-gold">
            {formatINR(laptop.price_inr)}
          </p>
        </div>

        <span className="inline-flex items-center gap-1 px-3 py-1.5 rounded-lg bg-bg-deep border border-border-subtle text-xs font-semibold text-text-primary group-hover:border-accent-gold group-hover:text-accent-gold transition-colors">
          View Specs →
        </span>
      </div>
    </Link>
  );
}