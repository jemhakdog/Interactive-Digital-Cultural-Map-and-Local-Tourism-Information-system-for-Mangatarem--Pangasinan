import type { Metadata } from "next";
import { BusinessView, EstablishmentItem } from "./business-view";
import { AdminManageBar } from "@/components/layout/admin-manage-bar";

export const metadata: Metadata = {
  title: "Business Directory",
  description:
    "Explore local inns, authentic Pangasinan dining, cafes, and agro-tourism destinations in Mangatarem, Pangasinan.",
};

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

async function getBusinesses(): Promise<EstablishmentItem[]> {
  try {
    const res = await fetch(`${API_BASE}/api/business/?per_page=100`, {
      next: { revalidate: 60 },
    });
    if (!res.ok) return [];
    const data = await res.json();
    return (data.establishments ?? data.businesses ?? data.items ?? []) as EstablishmentItem[];
  } catch {
    return [];
  }
}

export default async function BusinessPage() {
  const establishments = await getBusinesses();

  return (
    <div className="container mx-auto px-4 py-8">
      <AdminManageBar label="Businesses & Establishments" href="/admin/establishments" />
      {/* ── Page Header ── */}
      <div className="mb-8 space-y-1">
        <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-primary/10 text-primary text-xs font-semibold mb-2">
          <span>Local Commerce & Hospitality</span>
        </div>
        <h1 className="text-3xl md:text-4xl font-bold tracking-tight text-foreground">
          Business Directory
        </h1>
        <p className="text-muted-foreground text-sm md:text-base max-w-2xl">
          Discover certified accommodations, traditional Pangasinan dining, specialty coffee shops,
          and organic farms across the Municipality of Mangatarem.
        </p>
      </div>

      {/* ── Interactive Business Directory ── */}
      <BusinessView establishments={establishments} />
    </div>
  );
}
