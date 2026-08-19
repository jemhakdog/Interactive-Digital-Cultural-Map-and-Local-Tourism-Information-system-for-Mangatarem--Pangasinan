import type { Metadata } from "next";
import { HeritageHubView } from "./heritage-hub-view";
import { HeritageItem } from "./heritage-types";

export const metadata: Metadata = {
  title: "Heritage Registry | Mangatarem Tourism",
  description:
    "Explore the formal Heritage Registry of Mangatarem, Pangasinan. Browse natural heritage, built heritage, intangible cultural traditions, and historical artifacts across 82 barangays.",
};

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

interface HeritageTypeData {
  slug: string;
  label: string;
  label_plural: string;
  count: number;
}

async function getHeritageTypes(): Promise<HeritageTypeData[]> {
  try {
    const res = await fetch(`${API_BASE}/api/heritage/types`, {
      next: { revalidate: 60 },
    });
    if (!res.ok) return [];
    const data = await res.json();
    return (data.types ?? []) as HeritageTypeData[];
  } catch {
    return [];
  }
}

async function getAllHeritageItems(): Promise<HeritageItem[]> {
  try {
    const res = await fetch(`${API_BASE}/api/heritage/?per_page=100`, {
      next: { revalidate: 60 },
    });
    if (!res.ok) return [];
    const data = await res.json();
    return (data.items ?? []) as HeritageItem[];
  } catch {
    return [];
  }
}

export default async function HeritagePage() {
  const [types, items] = await Promise.all([
    getHeritageTypes(),
    getAllHeritageItems(),
  ]);

  const typeCounts: Record<string, number> = {};
  types.forEach((t) => {
    typeCounts[t.slug] = t.count;
  });

  return (
    <div className="container mx-auto px-4 py-8">
      {/* ── Editorial Header ── */}
      <div className="mb-8 space-y-2">
        <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-primary/10 text-primary text-xs font-semibold">
          <span>Living History & Cultural Memory</span>
        </div>
        <h1 className="text-3xl md:text-4xl lg:text-5xl font-bold tracking-tight text-foreground">
          Heritage Registry
        </h1>
        <p className="text-muted-foreground text-sm md:text-base max-w-2xl">
          Explore the formal archive of Mangatarem&apos;s cultural landmarks, natural wonders,
          living traditions, and sacred artifacts across all 82 barangays.
        </p>
      </div>

      {/* ── Interactive Heritage Hub ── */}
      <HeritageHubView initialItems={items} typeCounts={typeCounts} />
    </div>
  );
}
