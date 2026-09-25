import Link from "next/link";

type CategoryCardProps = {
  title: string;
  description: string;
  href: string;
  icon: React.ReactNode;
  comingSoon?: boolean;
};

export default function CategoryCard({ title, description, href, icon, comingSoon = false }: CategoryCardProps) {
  return (
    <Link
      href={href}
      className="group relative block rounded-2xl border border-border-subtle bg-bg-card p-8 md:p-10 transition-all duration-300 hover:border-border-glow hover:bg-bg-card-hover card-glow"
      aria-label={comingSoon ? `${title} (Coming Soon)` : `Explore ${title}`}
    >
      <div className="absolute top-4 right-4 opacity-0 group-hover:opacity-100 transition-opacity duration-300">
        <svg
          className="w-6 h-6 text-accent-gold"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
          aria-hidden="true"
        >
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
        </svg>
      </div>

      <div className="relative z-10">
        <div className="mb-6 inline-flex items-center justify-center w-16 h-16 rounded-xl bg-accent-gold/10 text-accent-gold">
          {icon}
        </div>

        <h3 className="text-2xl md:text-3xl font-bold text-text-primary mb-3 group-hover:text-accent-gold transition-colors">
          {title}
          {comingSoon && (
            <span className="ml-3 inline-block px-2.5 py-0.5 text-xs font-medium uppercase tracking-wider rounded-full bg-accent-gold/20 text-accent-gold border border-accent-gold/30">
              Coming Soon
            </span>
          )}
        </h3>

        <p className="text-text-secondary leading-relaxed mb-6">{description}</p>

        <div className="flex items-center gap-2 text-sm font-medium text-accent-gold group-hover:gap-3 transition-all duration-200">
          <span>{comingSoon ? "Notify Me" : "Explore"}</span>
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
          </svg>
        </div>
      </div>
    </Link>
  );
}