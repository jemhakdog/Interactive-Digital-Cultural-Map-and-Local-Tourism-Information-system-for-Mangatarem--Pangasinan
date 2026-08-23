import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Allow dev asset requests from these origins (Next blocks cross-origin
  // /_next/* requests by default; 127.0.0.1 differs from localhost).
  allowedDevOrigins: ["127.0.0.1"],
};

export default nextConfig;
