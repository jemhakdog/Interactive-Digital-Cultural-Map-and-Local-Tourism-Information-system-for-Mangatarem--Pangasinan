import type { Metadata } from "next";
import { TreePine } from "lucide-react";
import { AttractionsView } from "./attractions-view";
import { AttractionItem } from "./attraction-types";
import { CURATED_ATTRACTION_METADATA } from "./attraction-data";

export const metadata: Metadata = {
  title: "Attractions & Natural Wonders",
  description:
    "Explore protected natural landscapes, scenic mountain roads, serene waterfalls, and centuries-old cultural landmarks in Mangatarem, Pangasinan.",
};

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

async function getAttractions(): Promise<AttractionItem[]> {
  try {
    const res = await fetch(`${API_BASE}/api/attractions/`, {
      next: { revalidate: 60 },
    });
    if (!res.ok) {
      // Fallback to rich curated list
      return Object.values(CURATED_ATTRACTION_METADATA) as AttractionItem[];
    }
    const data = await res.json();
    const items = (data.attractions ?? data.items ?? []) as AttractionItem[];
    if (items.length === 0) {
      return Object.values(CURATED_ATTRACTION_METADATA) as AttractionItem[];
    }
    return items;
  } catch {
    return Object.values(CURATED_ATTRACTION_METADATA) as AttractionItem[];
  }
}

export default async function AttractionsPage() {
  const attractions = await getAttractions();

  return (
    <div className="container mx-auto px-4 py-8 sm:py-10 space-y-8">
      {/* ── Page Header ── */}
      <div className="space-y-2 max-w-2xl">
        <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-primary/10 text-primary text-xs font-semibold">
          <TreePine className="h-3.5 w-3.5" />
          <span>Eco-Tourism & Cultural Wonders</span>
        </div>
        <h1 className="text-3xl sm:text-4xl font-extrabold tracking-tight text-foreground">
          Attractions of Mangatarem
        </h1>
        <p className="text-muted-foreground text-sm sm:text-base leading-relaxed">
          Discover protected national landscapes, thermal hot springs, scenic mountain passes, cascading falls, and centuries-old colonial architecture in Pangasinan.
        </p>
      </div>

      {/* ── Interactive Hub ── */}
      <AttractionsView initialAttractions={attractions} />
    </div>
  );
}
