import Link from "next/link";
import Image from "next/image";
import { Phone } from "@/lib/api";

type PhoneCardProps = {
  phone: Phone;
  image_url?: string | null;
};

export default function PhoneCard({ phone, image_url = null }: PhoneCardProps) {
  const formatINR = (v: number | null) => {
    if (v === null || v === undefined) return null;
    return new Intl.NumberFormat("en-IN", {
      style: "currency",
      currency: "INR",
      maximumFractionDigits: 0,
    }).format(v);
  };

  const priceLabel = formatINR(phone.price_inr);
  const displayImage = phone.enrichment?.official_image_url || image_url;

  return (
    <Link
      href={`/mobile/${phone.phone_id}`}
      className="group block rounded-xl border border-border-subtle bg-bg-card overflow-hidden transition-all duration-300 hover:border-border-glow hover:bg-bg-card-hover card-glow"
      aria-label={`View ${phone.brand} ${phone.model}`}
    >
      <div className="flex flex-col sm:flex-row">
        {/* Image area */}
        <div className="relative w-full sm:w-28 shrink-0 aspect-[3/4] sm:aspect-auto sm:h-full min-h-[140px] bg-gradient-to-b from-bg-deep to-bg-card border-b sm:border-b-0 sm:border-r border-border-subtle flex flex-col items-center justify-center p-3 text-center overflow-hidden">
          {displayImage ? (
            <div className="relative w-full h-28 sm:h-32 flex items-center justify-center">
              <Image
                src={displayImage}
                alt={`${phone.brand} ${phone.model}`}
                width={112}
                height={140}
                className="h-28 w-full object-contain transition-transform duration-300 group-hover:scale-105"
                sizes="(max-width: 640px) 100vw, 112px"
              />
            </div>
          ) : (
            <>
              <div className="relative">
                <svg className="w-10 h-10 text-accent-gold/80" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                  <path d="M17 1.01L7 1c-1.1 0-2 .9-2 2v18c0 1.1.9 2 2 2h10c1.1 0 2-.9 2-2V3c0-1.1-.9-1.99-2-1.99zM17 19H7V5h10v14z" />
                </svg>
                <div className="absolute inset-0 rounded-md bg-accent-gold/5 blur-lg -z-10" aria-hidden="true" />
              </div>
              <span className="text-[10px] uppercase tracking-wider text-text-muted font-medium">
                {phone.brand}
              </span>
            </>
          )}
        </div>

        {/* Content */}
        <div className="flex-1 p-4 min-w-0">
          <div className="flex items-start justify-between gap-2">
            <div className="min-w-0 flex-1">
              <p className="text-xs font-semibold uppercase tracking-wider text-text-muted">
                {phone.brand}
              </p>
              <h3 className="line-clamp-2 text-sm font-semibold text-text-primary group-hover:text-accent-gold transition-colors">
                {phone.model}
              </h3>
            </div>
            {Boolean(phone.has_5g) && (
              <span className="shrink-0 text-[10px] font-semibold px-2 py-0.5 rounded-full bg-accent-gold/15 border border-accent-gold/30 text-accent-gold">
                5G
              </span>
            )}
          </div>

          <div className="mt-3 flex flex-wrap items-center gap-x-4 gap-y-1 text-xs text-text-secondary">
            {phone.rating !== null && phone.rating !== undefined && (
              <span className="inline-flex items-center gap-1">
                <svg className="w-3 h-3 fill-current text-amber-400" viewBox="0 0 24 24" aria-hidden="true">
                  <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z" />
                </svg>
                {phone.rating.toFixed(1)}
              </span>
            )}
            {phone.ram_gb !== null && phone.ram_gb !== undefined && (
              <span>{phone.ram_gb} GB RAM</span>
            )}
            {phone.storage_gb !== null && phone.storage_gb !== undefined && (
              <span>{phone.storage_gb} GB</span>
            )}
            {phone.battery_mah !== null && phone.battery_mah !== undefined && (
              <span>{phone.battery_mah} mAh</span>
            )}
            {phone.refresh_rate_hz !== null && phone.refresh_rate_hz !== undefined && (
              <span>{phone.refresh_rate_hz} Hz</span>
            )}
          </div>

          <div className="mt-2 flex items-center justify-between gap-2">
            <div className="min-w-0">
              {phone.processor_brand && (
                <p className="truncate text-xs text-text-muted capitalize">
                  {phone.processor_brand}
                </p>
              )}
            </div>
            {priceLabel && (
              <span className="shrink-0 text-sm font-semibold text-accent-gold">
                {priceLabel}
              </span>
            )}
          </div>
        </div>
      </div>
    </Link>
  );
}