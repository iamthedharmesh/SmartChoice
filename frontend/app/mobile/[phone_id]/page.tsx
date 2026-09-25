"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import Link from "next/link";
import Image from "next/image";
import PhoneCard from "@/components/PhoneCard";
import { getMobile, searchMobiles, type Phone } from "@/lib/api";

export default function MobileDetailPage() {
  const params = useParams();
  const phoneId = params?.phone_id ? Number(params.phone_id) : null;

  const [phone, setPhone] = useState<Phone | null>(null);
  const [similarPhones, setSimilarPhones] = useState<Phone[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [copied, setCopied] = useState(false);

  useEffect(() => {
    if (!phoneId || Number.isNaN(phoneId)) {
      setError("Invalid phone ID");
      setLoading(false);
      return;
    }

    setLoading(true);
    getMobile(phoneId)
      .then((data) => {
        setPhone(data);
        setError(null);

        // Fetch similar phones in the same price range
        const price = data.price_inr || 20000;
        const minP = Math.max(0, Math.floor(price * 0.75));
        const maxP = Math.ceil(price * 1.3);

        searchMobiles({
          min_price: minP,
          max_price: maxP,
          limit: 6,
          page: 1,
        })
          .then((res) => {
            if (res && Array.isArray(res.mobiles)) {
              setSimilarPhones(res.mobiles.filter((m) => m.phone_id !== data.phone_id).slice(0, 4));
            }
          })
          .catch(() => {});
      })
      .catch(() => {
        setError("Smartphone details could not be loaded.");
      })
      .finally(() => setLoading(false));
  }, [phoneId]);

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
          <p className="text-sm text-text-muted">Loading smartphone specifications...</p>
        </div>
      </div>
    );
  }

  if (error || !phone) {
    return (
      <div className="min-h-screen bg-bg-deep flex items-center justify-center p-8">
        <div className="max-w-md w-full rounded-xl border border-red-500/30 bg-red-500/10 p-6 text-center">
          <p className="text-sm text-red-400 mb-4">{error || "Phone not found"}</p>
          <Link
            href="/mobiles"
            className="inline-flex items-center gap-2 px-4 py-2 rounded-lg bg-accent-gold text-bg-deep font-semibold text-sm hover:bg-accent-gold-dim transition-colors"
          >
            ← Back to Mobile Catalog
          </Link>
        </div>
      </div>
    );
  }

  const e = phone.enrichment;
  const displayImage = e?.official_image_url;

  // Safely parse numeric hardware metrics for scores
  const chargingWatts = Number(e?.wired_charging_w) || phone.charging_watt || 25;
  const rearMp = Number(e?.rear_main_mp) || phone.rear_camera_mp || 48;
  const frontMp = Number(e?.front_camera_mp) || phone.front_camera_mp || 16;
  const clockSpeed = Number(phone.clock_speed_ghz) || 2.0;
  const ramGb = Number(phone.ram_gb) || 6;
  const refreshRate = Number(phone.refresh_rate_hz) || 60;
  const batteryMah = Number(phone.battery_mah) || 5000;
  const rating = Number(phone.rating) || 80;
  const price = Number(phone.price_inr) || 25000;

  const gamingScore = Math.min(
    98,
    Math.round(
      (clockSpeed / 3.2) * 40 +
        (ramGb / 16) * 30 +
        (refreshRate >= 120 ? 30 : 15)
    )
  );

  const cameraScore = Math.min(
    96,
    Math.round(
      Math.min(1, rearMp / 108) * 45 +
        (e?.rear_main_ois ? 25 : 10) +
        (frontMp / 32) * 20 +
        ((phone.rear_camera_count ?? 2) >= 3 ? 10 : 5)
    )
  );

  const batteryScore = Math.min(
    99,
    Math.round(
      Math.min(1, batteryMah / 5500) * 55 +
        Math.min(1, chargingWatts / 100) * 45
    )
  );

  const displayScore = Math.min(
    97,
    Math.round(
      (refreshRate >= 120 ? 45 : 25) +
        (e?.display_type?.toLowerCase().includes("amoled") || e?.display_type?.toLowerCase().includes("oled") ? 35 : 20) +
        (e?.display_hdr_support ? 15 : 5)
    )
  );

  const valueScore = Math.min(
    95,
    Math.round(
      Math.max(60, rating * 1.1 - (price > 60000 ? 10 : 0))
    )
  );

  return (
    <main className="min-h-screen bg-bg-deep pb-16">
      {/* Top Header / Breadcrumb Bar */}
      <div className="border-b border-border-subtle bg-bg-card/40 backdrop-blur-md sticky top-0 z-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-3 flex items-center justify-between gap-4">
          <nav className="flex items-center gap-2 text-xs text-text-muted truncate">
            <Link href="/" className="hover:text-text-primary transition-colors">Home</Link>
            <span>/</span>
            <Link href="/mobiles" className="hover:text-text-primary transition-colors">Mobiles</Link>
            <span>/</span>
            <span className="text-text-secondary">{phone.brand}</span>
            <span>/</span>
            <span className="text-accent-gold font-medium truncate">{phone.model}</span>
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
              href="/mobiles/find"
              className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-accent-gold text-bg-deep text-xs font-bold hover:bg-accent-gold-dim transition-colors"
            >
              Find My Phone
            </Link>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-8 space-y-8">
        {/* Main Showcase Hero */}
        <div className="rounded-2xl border border-border-subtle bg-bg-card p-6 sm:p-8">
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
            {/* Left: Device Image Showcase */}
            <div className="lg:col-span-5 flex flex-col items-center justify-center bg-gradient-to-b from-bg-deep to-bg-card rounded-xl border border-border-subtle p-8 min-h-[380px] relative overflow-hidden group">
              <div className="absolute inset-0 bg-accent-gold/5 blur-3xl rounded-full -z-0 pointer-events-none" />

              {displayImage ? (
                <div className="relative w-full h-72 sm:h-80 flex items-center justify-center z-10">
                  <Image
                    src={displayImage}
                    alt={`${phone.brand} ${phone.model}`}
                    width={280}
                    height={340}
                    className="max-h-72 sm:max-h-80 w-auto object-contain transition-transform duration-500 group-hover:scale-105 drop-shadow-[0_15px_25px_rgba(0,0,0,0.6)]"
                    priority
                  />
                </div>
              ) : (
                <div className="flex flex-col items-center justify-center py-12 z-10">
                  <svg className="w-24 h-24 text-accent-gold/80 mb-3" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                    <path d="M17 1.01L7 1c-1.1 0-2 .9-2 2v18c0 1.1.9 2 2 2h10c1.1 0 2-.9 2-2V3c0-1.1-.9-1.99-2-1.99zM17 19H7V5h10v14z" />
                  </svg>
                  <span className="text-sm uppercase tracking-wider text-accent-gold font-bold">
                    {phone.brand}
                  </span>
                </div>
              )}

              <div className="mt-4 flex items-center gap-2 z-10">
                <span className="px-2.5 py-1 rounded-md bg-bg-deep text-[11px] font-medium text-text-muted border border-border-subtle">
                  {e?.model_id ? `Model: ${e.model_id}` : phone.brand}
                </span>
                <span className="px-2.5 py-1 rounded-md bg-emerald-500/10 text-emerald-400 text-[11px] font-medium border border-emerald-500/30">
                  {e?.availability_status_india || "Available in India"}
                </span>
              </div>
            </div>

            {/* Right: Key Specs & Pricing Overview */}
            <div className="lg:col-span-7 flex flex-col justify-between">
              <div>
                <div className="flex items-center gap-2 mb-2">
                  <span className="text-xs font-bold uppercase tracking-wider text-accent-gold">
                    {phone.brand}
                  </span>
                  <span className="text-text-muted">•</span>
                  <span className="text-xs text-text-muted">
                    SmartChoice Verified Specs
                  </span>
                </div>

                <h1 className="text-3xl sm:text-4xl font-extrabold text-text-primary tracking-tight">
                  {phone.model}
                </h1>

                {/* Price & Rating Badges */}
                <div className="mt-4 flex flex-wrap items-baseline gap-4">
                  <span className="text-3xl sm:text-4xl font-black text-accent-gold">
                    {formatINR(phone.price_inr)}
                  </span>
                  <span className="text-xs text-text-muted">
                    (Approximate Indian Retail Price)
                  </span>
                </div>

                <div className="mt-4 flex flex-wrap items-center gap-2.5">
                  {phone.rating !== null && phone.rating !== undefined && (
                    <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-accent-gold/15 border border-accent-gold/30 text-accent-gold text-xs font-bold">
                      ★ {phone.rating.toFixed(1)} / 100 Spec Rating
                    </span>
                  )}
                  {Boolean(phone.has_5g) && (
                    <span className="inline-flex items-center px-3 py-1 rounded-full bg-accent-gold/15 border border-accent-gold/30 text-accent-gold text-xs font-semibold">
                      5G Connectivity
                    </span>
                  )}
                  {Boolean(phone.has_nfc) && (
                    <span className="inline-flex items-center px-3 py-1 rounded-full bg-blue-400/15 border border-blue-400/30 text-blue-400 text-xs font-semibold">
                      NFC Enabled
                    </span>
                  )}
                  {(e?.wired_charging_w || phone.charging_watt) && (
                    <span className="inline-flex items-center px-3 py-1 rounded-full bg-emerald-500/15 border border-emerald-500/30 text-emerald-400 text-xs font-semibold">
                      ⚡ {chargingWatts}W Fast Charging
                    </span>
                  )}
                </div>

                {/* Key Spec Highlight Grid */}
                <div className="mt-6 pt-6 border-t border-border-subtle">
                  <h3 className="text-xs font-bold uppercase tracking-wider text-text-muted mb-3">
                    At a Glance
                  </h3>
                  <div className="grid grid-cols-2 sm:grid-cols-3 gap-3">
                    <div className="rounded-xl bg-bg-deep border border-border-subtle p-3.5">
                      <p className="text-[10px] uppercase tracking-wider text-text-muted">Display</p>
                      <p className="text-sm font-bold text-text-primary mt-1">
                        {e?.display_size_inch ? `${e.display_size_inch}" ` : ""}
                        {phone.refresh_rate_hz ? `${phone.refresh_rate_hz} Hz` : "60 Hz"}
                      </p>
                      <p className="text-[11px] text-text-secondary truncate mt-0.5">
                        {e?.display_type || "IPS LCD / AMOLED"}
                      </p>
                    </div>

                    <div className="rounded-xl bg-bg-deep border border-border-subtle p-3.5">
                      <p className="text-[10px] uppercase tracking-wider text-text-muted">Processor</p>
                      <p className="text-sm font-bold text-text-primary mt-1 capitalize truncate">
                        {phone.processor_brand || "Octa-Core"}
                      </p>
                      <p className="text-[11px] text-text-secondary mt-0.5">
                        {phone.clock_speed_ghz ? `${phone.clock_speed_ghz} GHz` : "8 Cores"}
                      </p>
                    </div>

                    <div className="rounded-xl bg-bg-deep border border-border-subtle p-3.5">
                      <p className="text-[10px] uppercase tracking-wider text-text-muted">RAM & Storage</p>
                      <p className="text-sm font-bold text-text-primary mt-1">
                        {phone.ram_gb ? `${phone.ram_gb} GB` : "6 GB"} / {phone.storage_gb ? `${phone.storage_gb} GB` : "128 GB"}
                      </p>
                      <p className="text-[11px] text-text-secondary mt-0.5">Fast UFS Storage</p>
                    </div>

                    <div className="rounded-xl bg-bg-deep border border-border-subtle p-3.5">
                      <p className="text-[10px] uppercase tracking-wider text-text-muted">Battery</p>
                      <p className="text-sm font-bold text-text-primary mt-1">
                        {phone.battery_mah ? `${phone.battery_mah} mAh` : "5000 mAh"}
                      </p>
                      <p className="text-[11px] text-emerald-400 mt-0.5 font-medium">
                        {chargingWatts}W Charging
                      </p>
                    </div>

                    <div className="rounded-xl bg-bg-deep border border-border-subtle p-3.5">
                      <p className="text-[10px] uppercase tracking-wider text-text-muted">Main Camera</p>
                      <p className="text-sm font-bold text-text-primary mt-1">
                        {rearMp} MP
                      </p>
                      <p className="text-[11px] text-text-secondary mt-0.5">
                        {e?.rear_main_ois ? "OIS Supported" : `${phone.rear_camera_count ?? 2} Rear Lenses`}
                      </p>
                    </div>

                    <div className="rounded-xl bg-bg-deep border border-border-subtle p-3.5">
                      <p className="text-[10px] uppercase tracking-wider text-text-muted">Selfie Camera</p>
                      <p className="text-sm font-bold text-text-primary mt-1">
                        {frontMp} MP
                      </p>
                      <p className="text-[11px] text-text-secondary mt-0.5">Front HDR / AI</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* SmartChoice Spec Breakdown Meters */}
        <section className="rounded-2xl border border-border-subtle bg-bg-card p-6 sm:p-8">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 mb-6">
            <div>
              <h2 className="text-lg font-bold text-text-primary">
                SmartChoice Benchmark Scores
              </h2>
              <p className="text-xs text-text-muted">
                Calculated hardware index based on synthetic performance, camera optics, and battery metrics.
              </p>
            </div>
            <span className="text-xs font-semibold px-3 py-1 rounded-full bg-accent-gold/10 text-accent-gold border border-accent-gold/30 self-start sm:self-auto">
              Spec Rating Index
            </span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
            <div className="rounded-xl bg-bg-deep border border-border-subtle p-4">
              <div className="flex justify-between items-center text-xs mb-1.5">
                <span className="font-semibold text-text-secondary">🎮 Gaming</span>
                <span className="font-bold text-accent-gold">{gamingScore}/100</span>
              </div>
              <div className="h-2 rounded-full bg-border-subtle overflow-hidden">
                <div className="h-full bg-accent-gold rounded-full" style={{ width: `${gamingScore}%` }} />
              </div>
              <p className="text-[10px] text-text-muted mt-2">GPU & fluid frame rates</p>
            </div>

            <div className="rounded-xl bg-bg-deep border border-border-subtle p-4">
              <div className="flex justify-between items-center text-xs mb-1.5">
                <span className="font-semibold text-text-secondary">📸 Camera</span>
                <span className="font-bold text-accent-gold">{cameraScore}/100</span>
              </div>
              <div className="h-2 rounded-full bg-border-subtle overflow-hidden">
                <div className="h-full bg-accent-gold rounded-full" style={{ width: `${cameraScore}%` }} />
              </div>
              <p className="text-[10px] text-text-muted mt-2">Optics & sensor resolution</p>
            </div>

            <div className="rounded-xl bg-bg-deep border border-border-subtle p-4">
              <div className="flex justify-between items-center text-xs mb-1.5">
                <span className="font-semibold text-text-secondary">🔋 Battery</span>
                <span className="font-bold text-accent-gold">{batteryScore}/100</span>
              </div>
              <div className="h-2 rounded-full bg-border-subtle overflow-hidden">
                <div className="h-full bg-accent-gold rounded-full" style={{ width: `${batteryScore}%` }} />
              </div>
              <p className="text-[10px] text-text-muted mt-2">Capacity & recharge speed</p>
            </div>

            <div className="rounded-xl bg-bg-deep border border-border-subtle p-4">
              <div className="flex justify-between items-center text-xs mb-1.5">
                <span className="font-semibold text-text-secondary">📱 Display</span>
                <span className="font-bold text-accent-gold">{displayScore}/100</span>
              </div>
              <div className="h-2 rounded-full bg-border-subtle overflow-hidden">
                <div className="h-full bg-accent-gold rounded-full" style={{ width: `${displayScore}%` }} />
              </div>
              <p className="text-[10px] text-text-muted mt-2">Panel clarity & refresh rate</p>
            </div>

            <div className="rounded-xl bg-bg-deep border border-border-subtle p-4">
              <div className="flex justify-between items-center text-xs mb-1.5">
                <span className="font-semibold text-text-secondary">💰 Value</span>
                <span className="font-bold text-accent-gold">{valueScore}/100</span>
              </div>
              <div className="h-2 rounded-full bg-border-subtle overflow-hidden">
                <div className="h-full bg-accent-gold rounded-full" style={{ width: `${valueScore}%` }} />
              </div>
              <p className="text-[10px] text-text-muted mt-2">Feature-to-price ratio</p>
            </div>
          </div>
        </section>

        {/* Full Specifications Section */}
        <section className="rounded-2xl border border-border-subtle bg-bg-card p-6 sm:p-8">
          <h2 className="text-xl font-bold text-text-primary mb-6">
            Detailed Specifications
          </h2>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Display Specs */}
            <div className="rounded-xl bg-bg-deep border border-border-subtle p-5">
              <h3 className="text-xs font-bold uppercase tracking-wider text-accent-gold mb-4 flex items-center gap-2">
                <span>📱</span> Display & Screen
              </h3>
              <dl className="space-y-3 text-xs">
                <div className="flex justify-between py-1 border-b border-border-subtle/50">
                  <dt className="text-text-muted">Screen Size</dt>
                  <dd className="font-semibold text-text-primary">{e?.display_size_inch ? `${e.display_size_inch} inches` : "6.72 inches"}</dd>
                </div>
                <div className="flex justify-between py-1 border-b border-border-subtle/50">
                  <dt className="text-text-muted">Panel Technology</dt>
                  <dd className="font-semibold text-text-primary">{e?.display_type || "IPS LCD / AMOLED"}</dd>
                </div>
                <div className="flex justify-between py-1 border-b border-border-subtle/50">
                  <dt className="text-text-muted">Resolution</dt>
                  <dd className="font-semibold text-text-primary">{e?.display_resolution || "1080 x 2400 (FHD+)"}</dd>
                </div>
                <div className="flex justify-between py-1 border-b border-border-subtle/50">
                  <dt className="text-text-muted">Refresh Rate</dt>
                  <dd className="font-semibold text-text-primary">{phone.refresh_rate_hz ? `${phone.refresh_rate_hz} Hz` : "60 Hz"}</dd>
                </div>
                <div className="flex justify-between py-1 border-b border-border-subtle/50">
                  <dt className="text-text-muted">Peak Brightness</dt>
                  <dd className="font-semibold text-text-primary">{e?.display_peak_brightness_nits ? `${e.display_peak_brightness_nits} nits` : "680 nits"}</dd>
                </div>
                <div className="flex justify-between py-1">
                  <dt className="text-text-muted">Protection</dt>
                  <dd className="font-semibold text-text-primary">{e?.display_protection || "Scratch-resistant glass"}</dd>
                </div>
              </dl>
            </div>

            {/* Camera System Specs */}
            <div className="rounded-xl bg-bg-deep border border-border-subtle p-5">
              <h3 className="text-xs font-bold uppercase tracking-wider text-accent-gold mb-4 flex items-center gap-2">
                <span>📸</span> Camera System
              </h3>
              <dl className="space-y-3 text-xs">
                <div className="flex justify-between py-1 border-b border-border-subtle/50">
                  <dt className="text-text-muted">Rear Main Sensor</dt>
                  <dd className="font-semibold text-text-primary">
                    {rearMp} MP
                  </dd>
                </div>
                <div className="flex justify-between py-1 border-b border-border-subtle/50">
                  <dt className="text-text-muted">Optical Stabilization (OIS)</dt>
                  <dd className="font-semibold text-text-primary">{e?.rear_main_ois ? "Supported (OIS)" : "Electronic (EIS)"}</dd>
                </div>
                <div className="flex justify-between py-1 border-b border-border-subtle/50">
                  <dt className="text-text-muted">Rear Lenses Count</dt>
                  <dd className="font-semibold text-text-primary">{phone.rear_camera_count ?? 2} Cameras</dd>
                </div>
                <div className="flex justify-between py-1 border-b border-border-subtle/50">
                  <dt className="text-text-muted">Front Selfie Camera</dt>
                  <dd className="font-semibold text-text-primary">
                    {frontMp} MP
                  </dd>
                </div>
                <div className="flex justify-between py-1 border-b border-border-subtle/50">
                  <dt className="text-text-muted">Video Recording Max</dt>
                  <dd className="font-semibold text-text-primary">{e?.rear_video_max || "1080p @ 60fps / 4K @ 30fps"}</dd>
                </div>
                <div className="flex justify-between py-1">
                  <dt className="text-text-muted">Main Lens Aperture</dt>
                  <dd className="font-semibold text-text-primary">{e?.rear_main_aperture || "f/1.8"}</dd>
                </div>
              </dl>
            </div>

            {/* Processor & Memory */}
            <div className="rounded-xl bg-bg-deep border border-border-subtle p-5">
              <h3 className="text-xs font-bold uppercase tracking-wider text-accent-gold mb-4 flex items-center gap-2">
                <span>⚡</span> Performance & Platform
              </h3>
              <dl className="space-y-3 text-xs">
                <div className="flex justify-between py-1 border-b border-border-subtle/50">
                  <dt className="text-text-muted">Chipset / Processor</dt>
                  <dd className="font-semibold text-text-primary capitalize">{phone.processor_brand || "Octa-Core"}</dd>
                </div>
                <div className="flex justify-between py-1 border-b border-border-subtle/50">
                  <dt className="text-text-muted">CPU Architecture</dt>
                  <dd className="font-semibold text-text-primary">{phone.core_count ?? 8} Cores</dd>
                </div>
                <div className="flex justify-between py-1 border-b border-border-subtle/50">
                  <dt className="text-text-muted">Clock Speed</dt>
                  <dd className="font-semibold text-text-primary">{phone.clock_speed_ghz ? `${phone.clock_speed_ghz} GHz` : "2.2 GHz"}</dd>
                </div>
                <div className="flex justify-between py-1 border-b border-border-subtle/50">
                  <dt className="text-text-muted">RAM Capacity</dt>
                  <dd className="font-semibold text-text-primary">{phone.ram_gb ? `${phone.ram_gb} GB LPDDR4X` : "6 GB"}</dd>
                </div>
                <div className="flex justify-between py-1 border-b border-border-subtle/50">
                  <dt className="text-text-muted">Storage Capacity</dt>
                  <dd className="font-semibold text-text-primary">{phone.storage_gb ? `${phone.storage_gb} GB UFS 2.2` : "128 GB"}</dd>
                </div>
                <div className="flex justify-between py-1">
                  <dt className="text-text-muted">Operating System</dt>
                  <dd className="font-semibold text-text-primary capitalize">{phone.os || "Android"}</dd>
                </div>
              </dl>
            </div>

            {/* Battery, Charging & Connectivity */}
            <div className="rounded-xl bg-bg-deep border border-border-subtle p-5">
              <h3 className="text-xs font-bold uppercase tracking-wider text-accent-gold mb-4 flex items-center gap-2">
                <span>🔋</span> Battery & Connectivity
              </h3>
              <dl className="space-y-3 text-xs">
                <div className="flex justify-between py-1 border-b border-border-subtle/50">
                  <dt className="text-text-muted">Battery Capacity</dt>
                  <dd className="font-semibold text-text-primary">{phone.battery_mah ? `${phone.battery_mah} mAh` : "5000 mAh"}</dd>
                </div>
                <div className="flex justify-between py-1 border-b border-border-subtle/50">
                  <dt className="text-text-muted">Charging Speed</dt>
                  <dd className="font-semibold text-emerald-400">
                    {chargingWatts}W Fast Charge
                  </dd>
                </div>
                <div className="flex justify-between py-1 border-b border-border-subtle/50">
                  <dt className="text-text-muted">5G Cellular</dt>
                  <dd className="font-semibold text-text-primary">{phone.has_5g ? "Supported (Dual 5G)" : "4G LTE"}</dd>
                </div>
                <div className="flex justify-between py-1 border-b border-border-subtle/50">
                  <dt className="text-text-muted">NFC Contactless</dt>
                  <dd className="font-semibold text-text-primary">{phone.has_nfc ? "Yes (Google Wallet Ready)" : "Not Supported"}</dd>
                </div>
                <div className="flex justify-between py-1 border-b border-border-subtle/50">
                  <dt className="text-text-muted">Port Standard</dt>
                  <dd className="font-semibold text-text-primary">{e?.usb_version ? `USB ${e.usb_version} Type-C` : "USB Type-C"}</dd>
                </div>
                <div className="flex justify-between py-1">
                  <dt className="text-text-muted">Weight</dt>
                  <dd className="font-semibold text-text-primary">{e?.weight_g ? `${e.weight_g} g` : "190 g"}</dd>
                </div>
              </dl>
            </div>
          </div>
        </section>

        {/* SmartChoice Recommendation Summary & Buying Advice */}
        <section className="rounded-2xl border border-border-subtle bg-gradient-to-r from-bg-card via-bg-deep to-bg-card p-6 sm:p-8">
          <div className="max-w-3xl">
            <span className="text-xs font-bold uppercase tracking-wider text-accent-gold">
              SmartChoice Verdict
            </span>
            <h2 className="text-xl font-bold text-text-primary mt-1">
            Who is the {phone.model.toLowerCase().startsWith(phone.brand.toLowerCase()) ? phone.model : `${phone.brand} ${phone.model}`} for?
            </h2>
            <p className="mt-3 text-sm text-text-secondary leading-relaxed">
              The {phone.model} is a strong contender in the {formatINR(phone.price_inr)} price segment.
              With a {phone.refresh_rate_hz ?? 120}Hz smooth display, {phone.ram_gb ?? 6}GB of RAM, and a {phone.battery_mah ?? 5000}mAh battery backed by fast charging,
              it delivers solid day-to-day multitasking and fluid multimedia streaming. It is recommended for users seeking long battery endurance, modern 5G connectivity, and dependable daily speed.
            </p>
            <div className="mt-5 flex flex-wrap gap-3">
              <Link
                href="/mobiles/find"
                className="inline-flex items-center gap-2 px-4 py-2 rounded-lg bg-accent-gold text-bg-deep text-xs font-bold hover:bg-accent-gold-dim transition-colors"
              >
                Compare with Other Budget Picks →
              </Link>
              <Link
                href="/mobiles"
                className="inline-flex items-center gap-2 px-4 py-2 rounded-lg border border-border-subtle bg-bg-deep text-xs font-semibold text-text-secondary hover:text-text-primary hover:border-border-glow transition-colors"
              >
                Browse All {phone.brand} Phones
              </Link>
            </div>
          </div>
        </section>

        {/* Similar Phones Carousel / Grid */}
        {similarPhones.length > 0 && (
          <section className="rounded-2xl border border-border-subtle bg-bg-card p-6 sm:p-8">
            <div className="flex items-center justify-between mb-6">
              <div>
                <h2 className="text-xl font-bold text-text-primary">
                  Similar Phones in this Price Segment
                </h2>
                <p className="text-xs text-text-muted mt-0.5">
                  Alternative smartphones close to {formatINR(phone.price_inr)}
                </p>
              </div>
              <Link
                href="/mobiles"
                className="text-xs font-semibold text-accent-gold hover:underline"
              >
                View Catalog →
              </Link>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
              {similarPhones.map((item) => (
                <PhoneCard key={item.phone_id} phone={item} />
              ))}
            </div>
          </section>
        )}
      </div>
    </main>
  );
}