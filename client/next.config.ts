import type { NextConfig } from "next";

//http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4
const nextConfig: NextConfig = {
  images: {
    remotePatterns: [
      {
        protocol: "https",
        hostname: "upload.wikimedia.org",
        port: "",
        pathname: "/wikipedia/commons/thumb/**",
      },
      {
        protocol: "https",
        hostname: "i.ytimg.com",
        port: "",
        pathname: "/vi_webp/**",
      },
      {
        protocol: "https",
        hostname: "i.ytimg.com",
        port: "",
        pathname: "/vi/**",
      },
      {
        protocol: "https",
        hostname: "img.jakpost.net",
        port: "",
        pathname: "/c/**",
      },
      // {
      //   protocol: "http",
      //   hostname: "commondatastorage.googleapis.com",
      //   port: "",
      //   pathname: "/gtv-videos-bucket/**",
      //   search: "",
      // },
    ],
  },
  /* config options here */
};

export default nextConfig;
