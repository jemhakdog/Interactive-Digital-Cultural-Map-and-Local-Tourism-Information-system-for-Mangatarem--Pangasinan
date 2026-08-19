import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Interactive Cultural Map",
  description: "Explore Mangatarem's attractions, heritage sites, natural springs, and curated tour routes on an interactive digital map.",
  openGraph: {
    title: "Interactive Cultural Map | Mangatarem Tourism",
    description: "Explore Mangatarem's attractions, heritage sites, natural springs, and curated tour routes on an interactive digital map.",
  },
};

export default function MapLayout({ children }: { children: React.ReactNode }) {
  return children;
}
