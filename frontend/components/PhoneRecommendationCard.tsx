import Image from "next/image";
import Link from "next/link";
import { PhoneRecommendation } from "@/lib/api";

type Props = {
  phone: PhoneRecommendation;
};

export default function PhoneRecommendationCard({ phone }: Props) {
  const formatINR = (v: number | null) => {
    if (v === null || v === undefined) return null;
    return new Intl.NumberFormat("en-IN", {
      style: "currency",
      currency: "INR",
      maximumFractionDigits: 0,
    }).format(v);
  };

  const priceLabel = formatINR(phone.price_inr);
  const match = Number(phone.match_percentage) || 0;
  const enrichment = phone.enrichment;

  return (
    <Link
      href={`/mobile/${phone.phone_id}`}
      target="_blank"
      rel="noopener noreferrer"
      className="group block rounded-xl border border-border-subtle bg-bg-card overflow-hidden transition-all duration-300 hover:border-border-glow hover:bg-bg-card-hover card-glow cursor-pointer"
      aria-label={`View ${phone.brand} ${phone.model} details (opens in new tab)`}
    >
      <div className="flex flex-col sm:flex-row">
        {/* Product Image / Icon Area */}
        <div className="relative w-full sm:w-36 shrink-0 aspect-[3/4] sm:aspect-auto sm:h-full min-h-[170px] bg-gradient-to-b from-bg-deep to-bg-card border-b sm:border-b-0 sm:border-r border-border-subtle flex flex-col items-center justify-center p-3 text-center overflow-hidden">
          {enrichment?.official_image_url ? (
            <div className="relative w-full h-32 flex items-center justify-center">
              <Image
                src={enrichment.official_image_url}
                alt={`${phone.brand} ${phone.model}`}
                width={128}
                height={160}
                className="h-32 w-full object-contain transition-transform duration-300 group-hover:scale-105"
                sizes="(max-width: 640px) 100vw, 128px"
              />
            </div>
          ) : (
            <div className="flex flex-col items-center gap-2">
              <div className="relative">
                <svg
                  className="w-10 h-10 text-accent-gold/80"
                  fill="currentColor"
                  viewBox="0 0 24 24"
                  aria-hidden="true"
                >
                  <path d="M17 1.01L7 1c-1.1 0-2 .9-2 2v18c0 1.1.9 2 2 2h10c1.1 0 2-.9 2-2V3c0-1.1-.9-1.99-2-1.99zM17 19H7V5h10v14z" />
                </svg>
                <div className="absolute inset-0 rounded-md bg-accent-gold/5 blur-lg -z-10" aria-hidden="true" />
              </div>
              <span className="text-[10px] uppercase tracking-wider text-text-muted font-medium">
                {phone.brand}
              </span>
            </div>
          )}
        </div>

        {/* Card Content */}
        <div className="flex-1 p-5 flex flex-col justify-between">
          <div>
            <div className="flex items-start justify-between gap-3">
              <div className="min-w-0">
                <p className="text-xs font-semibold uppercase tracking-wider text-text-muted">
                  {phone.brand}
                </p>
                <h3 className="text-base font-semibold text-text-primary group-hover:text-accent-gold transition-colors">
                  {phone.model}
                </h3>
              </div>
              {Boolean(phone.has_5g) && (
                <span className="shrink-0 text-[10px] font-semibold px-2.5 py-0.5 rounded-full bg-accent-gold/15 border border-accent-gold/30 text-accent-gold">
                  5G
                </span>
              )}
            </div>

            {/* SmartChoice Match Bar */}
            <div className="mt-3">
              <div className="flex items-center justify-between gap-2">
                <span className="text-[10px] font-semibold uppercase tracking-[0.15em] text-text-muted">
                  SmartChoice Match
                </span>
                <span className="text-base font-bold text-accent-gold">
                  {match.toFixed(1)}%
                </span>
              </div>
              <div className="mt-1 h-1.5 w-full rounded-full bg-border-subtle overflow-hidden">
                <div
                  className="h-full bg-gradient-to-r from-accent-gold to-accent-gold-dim transition-all duration-500"
                  style={{ width: `${Math.min(Math.max(match, 0), 100)}%` }}
                />
              </div>
            </div>

            {/* Core Specifications */}
            <div className="mt-3 flex flex-wrap items-center gap-x-4 gap-y-1.5 text-xs text-text-secondary">
              {phone.rating !== null && phone.rating !== undefined && (
                <span className="inline-flex items-center gap-1 text-amber-400 font-medium">
                  ★ {phone.rating.toFixed(1)}
                </span>
              )}
              {phone.ram_gb !== null && phone.ram_gb !== undefined && (
                <span>{phone.ram_gb} GB RAM</span>
              )}
              {phone.storage_gb !== null && phone.storage_gb !== undefined && (
                <span>{phone.storage_gb} GB Storage</span>
              )}
              {phone.battery_mah !== null && phone.battery_mah !== undefined && (
                <span>{phone.battery_mah} mAh</span>
              )}
              {phone.refresh_rate_hz !== null && phone.refresh_rate_hz !== undefined && (
                <span>{phone.refresh_rate_hz} Hz</span>
              )}
            </div>

            {/* Why This Phone Reasons */}
            {phone.reasons && phone.reasons.length > 0 && (
              <div className="mt-3 flex flex-wrap gap-1.5">
                {phone.reasons.slice(0, 3).map((reason, idx) => (
                  <span
                    key={idx}
                    className="text-[10px] px-2 py-0.5 rounded-md bg-bg-deep text-text-secondary border border-border-subtle"
                  >
                    ✓ {reason}
                  </span>
                ))}
              </div>
            )}
          </div>

          {/* Card Footer: Price & Clear Call to Action */}
          <div className="mt-4 pt-3 border-t border-border-subtle flex items-center justify-between">
            <div>
              {priceLabel && (
                <span className="text-lg font-bold text-accent-gold">
                  {priceLabel}
                </span>
              )}
            </div>
            <span className="inline-flex items-center gap-1.5 text-xs font-semibold text-accent-gold group-hover:underline">
              View Full Details
              <svg className="w-3.5 h-3.5 transition-transform group-hover:translate-x-1" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
              </svg>
            </span>
          </div>
        </div>
      </div>
    </Link>
  );
}