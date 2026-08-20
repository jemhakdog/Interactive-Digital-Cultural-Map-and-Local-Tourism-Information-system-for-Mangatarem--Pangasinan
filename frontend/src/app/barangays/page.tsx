import type { Metadata } from "next";
import { MapPin } from "lucide-react";
import { BarangayExplorer, type BarangayItem } from "@/components/public/barangay-explorer";
import { MANGATAREM_BARANGAYS } from "@/app/auth/auth-constants";

export const metadata: Metadata = {
  title: "Barangays of Mangatarem",
  description:
    "Explore the 82 barangays of Mangatarem, Pangasinan. Discover local history, cultural heritage, and hidden gems in every corner of our town.",
};

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

const CATEGORIES = ["Nature", "History", "Food", "Festivals"];

// TODO: FastAPI endpoint not implemented yet (no GET /api/barangays).
// Using a curated local fallback derived from the official barangay list.
function buildCuratedBarangays(): BarangayItem[] {
  return MANGATAREM_BARANGAYS.map((name, i) => ({
    name,
    category: CATEGORIES[i % CATEGORIES.length],
    tags: [CATEGORIES[i % CATEGORIES.length]],
    attraction_count: 0,
  }));
}

async function getBarangays(): Promise<BarangayItem[]> {
  try {
    const res = await fetch(`${API_BASE}/api/barangays`, { next: { revalidate: 300 } });
    if (!res.ok) return buildCuratedBarangays();
    const data = await res.json();
    const items = (data.barangays ?? data.items ?? []) as BarangayItem[];
    return items.length ? items : buildCuratedBarangays();
  } catch {
    return buildCuratedBarangays();
  }
}

export default async function BarangaysPage() {
  const barangays = await getBarangays();

  return (
    <div className="container mx-auto px-4 py-8 sm:py-10 space-y-8">
      {/* ── Page Header ── */}
      <div className="space-y-2 max-w-2xl">
        <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-primary/10 text-primary text-xs font-semibold">
          <MapPin className="h-3.5 w-3.5" />
          <span>The Heart of Pangasinan</span>
        </div>
        <h1 className="text-3xl sm:text-4xl font-extrabold tracking-tight text-foreground">
          82 Barangays
        </h1>
        <p className="text-muted-foreground text-sm sm:text-base leading-relaxed">
          Every corner tells a story. Journey through the diverse landscapes and rich
          traditions that weave the tapestry of Mangatarem.
        </p>
      </div>

      <BarangayExplorer barangays={barangays} />
    </div>
  );
}
