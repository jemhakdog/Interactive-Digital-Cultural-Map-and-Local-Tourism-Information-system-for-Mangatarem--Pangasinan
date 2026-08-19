import type { Metadata } from "next";
import { GalleryView, GalleryItem } from "./gallery-view";

export const metadata: Metadata = {
  title: "Visions of Mangatarem — Multimedia Cultural Gallery",
  description:
    "Explore high-resolution photography, scenic landscapes, Spanish colonial heritage, and community cultural stories from Mangatarem, Pangasinan.",
};

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

async function getGalleryData() {
  try {
    const res = await fetch(`${API_BASE}/api/gallery?per_page=48`, {
      next: { revalidate: 60 },
    });
    if (!res.ok) {
      return { items: [], barangays: [] };
    }
    return res.json();
  } catch {
    return { items: [], barangays: [] };
  }
}

export default async function GalleryPage() {
  const data = await getGalleryData();
  const rawItems = (data.items ?? []) as GalleryItem[];
  const availableBarangays = (data.barangays ?? []) as string[];

  return (
    <div className="container mx-auto px-4 py-8 sm:py-10">
      {/* ── Standard Page Header for Consistency & Test Compatibility ── */}
      <div className="mb-8 space-y-1">
        <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-primary/10 text-primary text-xs font-semibold mb-2">
          <span>Visual Heritage & Media Showcase</span>
        </div>
        <h1 className="text-3xl md:text-4xl font-bold tracking-tight text-foreground">
          Gallery
        </h1>
        <p className="text-muted-foreground text-sm md:text-base max-w-2xl">
          Photos from Mangatarem — explore cultural heritage, natural landscapes, festivals, and community stories.
        </p>
      </div>

      {/* ── Interactive Multimedia Gallery Showcase ── */}
      <GalleryView
        initialItems={rawItems}
        availableBarangays={availableBarangays}
      />
    </div>
  );
}
