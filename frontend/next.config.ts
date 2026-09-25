import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  images: {
    remotePatterns: [
      // TMDB movie images
      {
        protocol: "https",
        hostname: "image.tmdb.org",
        pathname: "/t/p/**",
      },

      // Apple
      {
        protocol: "https",
        hostname: "www.apple.com",
        pathname: "/**",
      },

      // Samsung
      {
        protocol: "https",
        hostname: "images.samsung.com",
        pathname: "/**",
      },
      {
        protocol: "https",
        hostname: "img.global.news.samsung.com",
        pathname: "/**",
      },

      // OnePlus
      {
        protocol: "https",
        hostname: "image01-in.oneplus.net",
        pathname: "/**",
      },
      {
        protocol: "https",
        hostname: "www.oneplus.com",
        pathname: "/**",
      },
      {
        protocol: "https",
        hostname: "cdn.opstatics.com",
        pathname: "/**",
      },
      {
        protocol: "https",
        hostname: "oasis.opstatics.com",
        pathname: "/**",
      },

      // OPPO
      {
        protocol: "https",
        hostname: "www.oppo.com",
        pathname: "/**",
      },

      // vivo
      {
        protocol: "https",
        hostname: "in-exstatic-vivofs.vivo.com",
        pathname: "/**",
      },
      {
        protocol: "https",
        hostname: "asia-exstatic-vivofs.vivo.com",
        pathname: "/**",
      },

      // Xiaomi / Redmi / POCO
      {
        protocol: "https",
        hostname: "i01.appmifile.com",
        pathname: "/**",
      },
      {
        protocol: "https",
        hostname: "i02.appmifile.com",
        pathname: "/**",
      },

      // Realme
      {
        protocol: "https",
        hostname: "static.realme.net",
        pathname: "/**",
      },

      // Motorola & Lenovo
      {
        protocol: "https",
        hostname: "motorolain.vtexassets.com",
        pathname: "/**",
      },
      {
        protocol: "https",
        hostname: "p3-ofp.static.pub",
        pathname: "/**",
      },

      // Nothing & ZTE
      {
        protocol: "https",
        hostname: "cdn.shopify.com",
        pathname: "/**",
      },

      // TECNO
      {
        protocol: "https",
        hostname: "d13pvy8xd75yde.cloudfront.net",
        pathname: "/**",
      },

      // Honor
      {
        protocol: "https",
        hostname: "www.honor.com",
        pathname: "/**",
      },

      // LG
      {
        protocol: "https",
        hostname: "www.lg.com",
        pathname: "/**",
      },
    ],
  },
};

export default nextConfig;