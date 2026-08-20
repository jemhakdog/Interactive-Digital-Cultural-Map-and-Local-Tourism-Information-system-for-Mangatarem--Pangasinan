import type { Metadata } from "next";
import Link from "next/link";
import { MapPin, ArrowLeft } from "lucide-react";
import {
  BarangayProfile,
  type BarangayInfo,
  type SimpleItem,
} from "@/components/public/barangay-profile";

export const metadata: Metadata = {
  title: "Barangay Profile — Mangatarem",
};

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

interface BarangayProfileData {
  info: BarangayInfo | null;
  attractions: SimpleItem[];
  events: SimpleItem[];
  gallery: SimpleItem[];
}

// TODO: FastAPI endpoint not implemented yet (no GET /api/barangay/{name}).
// All related queries fall back to local placeholder state.
async function getBarangayProfile(name: string): Promise<BarangayProfileData> {
  const fallback: BarangayProfileData = {
    info: null,
    attractions: [],
    events: [],
    gallery: [],
  };
  try {
    const res = await fetch(`${API_BASE}/api/barangay/${encodeURIComponent(name)}`, {
      next: { revalidate: 300 },
    });
    if (!res.ok) return fallback;
    const data = await res.json();
    return {
      info: (data.barangay_info ?? data.info ?? null) as BarangayInfo | null,
      attractions: (data.attractions ?? []) as SimpleItem[],
      events: (data.events ?? []) as SimpleItem[],
      gallery: (data.gallery ?? []) as SimpleItem[],
    };
  } catch {
    return fallback;
  }
}

export default async function BarangayProfilePage({
  params,
}: {
  params: { id: string };
}) {
  const barangayName = decodeURIComponent(params.id);
  const data = await getBarangayProfile(barangayName);

  return (
    <div className="container mx-auto px-4 py-8 sm:py-10 space-y-8">
      {/* ── Header ── */}
      <div className="space-y-3 max-w-3xl">
        <Link
          href="/barangays"
          className="inline-flex items-center gap-1.5 text-xs text-muted-foreground hover:text-foreground transition-colors"
        >
          <ArrowLeft className="h-3.5 w-3.5" /> All Barangays
        </Link>
        <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-primary/10 text-primary text-xs font-semibold">
          <MapPin className="h-3.5 w-3.5" />
          <span>Pangasinan, Philippines</span>
        </div>
        <h1 className="text-3xl sm:text-4xl font-extrabold tracking-tight text-foreground">
          {barangayName}
        </h1>
        {data.attractions.length > 0 && (
          <p className="text-sm text-muted-foreground">
            {data.attractions.length} Attractions
          </p>
        )}
      </div>

      <BarangayProfile
        barangayName={barangayName}
        info={data.info}
        attractions={data.attractions}
        events={data.events}
        gallery={data.gallery}
      />
    </div>
  );
}
