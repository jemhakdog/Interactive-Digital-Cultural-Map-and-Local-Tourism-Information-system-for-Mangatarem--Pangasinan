import type { Metadata } from "next";
import Link from "next/link";
import { MapPin, ArrowLeft, Navigation, Landmark, Sparkles, Share2 } from "lucide-react";
import {
  BarangayProfile,
  type BarangayInfo,
  type SimpleItem,
} from "@/components/public/barangay-profile";

export async function generateMetadata({
  params,
}: {
  params: Promise<{ id: string }> | { id: string };
}): Promise<Metadata> {
  const resolvedParams = await params;
  const name = decodeURIComponent(resolvedParams.id);
  return {
    title: `${name} | Barangay Cultural Profile — Mangatarem`,
    description: `Explore the cultural heritage, community history, attractions, and local traditions of Barangay ${name} in Mangatarem, Pangasinan.`,
  };
}

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

interface BarangayProfileData {
  info: BarangayInfo | null;
  attractions: SimpleItem[];
  events: SimpleItem[];
  gallery: SimpleItem[];
}

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
  params: Promise<{ id: string }> | { id: string };
}) {
  const resolvedParams = await params;
  const barangayName = decodeURIComponent(resolvedParams.id);
  const data = await getBarangayProfile(barangayName);

  return (
    <div className="min-h-screen bg-gradient-to-b from-background via-muted/20 to-background pb-16">
      <div className="container mx-auto px-4 py-8 sm:py-12 space-y-8 max-w-6xl">
        {/* ── Breadcrumbs & Back Navigation ── */}
        <div className="flex items-center justify-between">
          <Link
            href="/barangays"
            className="inline-flex items-center gap-2 text-xs font-semibold text-muted-foreground hover:text-primary transition-colors bg-card border border-border/80 px-3 py-1.5 rounded-xl shadow-xs"
          >
            <ArrowLeft className="h-3.5 w-3.5" /> Back to All 82 Barangays
          </Link>

          <Link
            href={`/map?barangay=${encodeURIComponent(barangayName)}`}
            className="inline-flex items-center gap-1.5 text-xs font-semibold text-primary hover:underline"
          >
            <Navigation className="h-3.5 w-3.5" />
            <span>Locate on Map</span>
          </Link>
        </div>

        {/* ── Cultural Hero Card ── */}
        <div className="relative overflow-hidden rounded-3xl border border-border/70 bg-card/80 backdrop-blur-md p-6 sm:p-10 shadow-xs">
          <div
            aria-hidden="true"
            className="pointer-events-none absolute -top-24 -right-24 h-72 w-72 rounded-full bg-primary/10 blur-3xl"
          />
          <div
            aria-hidden="true"
            className="pointer-events-none absolute -bottom-24 -left-24 h-72 w-72 rounded-full bg-amber-500/10 blur-3xl"
          />

          <div className="relative z-10 space-y-4">
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-primary/10 border border-primary/20 text-primary text-xs font-semibold">
              <MapPin className="h-3.5 w-3.5" />
              <span>Mangatarem, Pangasinan, Philippines</span>
            </div>

            <h1 className="text-3xl sm:text-4xl md:text-5xl font-extrabold tracking-tight text-foreground">
              {barangayName}
            </h1>

            <p className="text-muted-foreground text-sm sm:text-base max-w-2xl leading-relaxed">
              Official cultural heritage profile, municipal records, local community assets, and registered tourist destinations in {barangayName}.
            </p>

            <div className="flex flex-wrap items-center gap-3 pt-2">
              <div className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-background border border-border/80 text-xs font-semibold text-foreground">
                <Sparkles className="h-3.5 w-3.5 text-amber-500" />
                <span>{data.attractions.length} Cultural Assets</span>
              </div>
              <div className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-background border border-border/80 text-xs font-semibold text-foreground">
                <Landmark className="h-3.5 w-3.5 text-primary" />
                <span>Local Heritage Register</span>
              </div>
            </div>
          </div>
        </div>

        {/* ── Detailed Profile Tabs ── */}
        <BarangayProfile
          barangayName={barangayName}
          info={data.info}
          attractions={data.attractions}
          events={data.events}
          gallery={data.gallery}
        />
      </div>
    </div>
  );
}
