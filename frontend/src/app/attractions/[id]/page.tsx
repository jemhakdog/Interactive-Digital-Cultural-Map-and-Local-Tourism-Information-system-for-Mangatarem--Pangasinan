import type { Metadata } from "next";
import { notFound } from "next/navigation";
import { AttractionDetailView } from "./attraction-detail-view";
import { AttractionItem, AttractionReviewItem, AttractionReviewSummary } from "../attraction-types";
import { CURATED_ATTRACTION_METADATA, enrichAttraction } from "../attraction-data";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

async function getAttraction(id: string): Promise<AttractionItem | null> {
  const numericId = Number(id);
  try {
    const res = await fetch(`${API_BASE}/api/attractions/${id}`, {
      next: { revalidate: 60 },
    });
    if (res.ok) {
      return res.json();
    }
  } catch {
    // fallback
  }

  // Fallback to local curated data if available
  if (CURATED_ATTRACTION_METADATA[numericId]) {
    return CURATED_ATTRACTION_METADATA[numericId] as AttractionItem;
  }

  return null;
}

async function getReviews(id: string): Promise<{
  reviews: AttractionReviewItem[];
  summary: AttractionReviewSummary | null;
}> {
  try {
    const res = await fetch(`${API_BASE}/api/attractions/${id}/reviews`, {
      next: { revalidate: 60 },
    });
    if (!res.ok) return { reviews: [], summary: null };
    const data = await res.json();
    return {
      reviews: data.reviews ?? [],
      summary: data.summary ?? null,
    };
  } catch {
    return { reviews: [], summary: null };
  }
}

async function getRelatedAttractions(currentId: number, category?: string | null): Promise<AttractionItem[]> {
  try {
    const res = await fetch(`${API_BASE}/api/attractions/`, {
      next: { revalidate: 60 },
    });
    if (res.ok) {
      const data = await res.json();
      const all = (data.attractions ?? data.items ?? []) as AttractionItem[];
      return all
        .filter((a) => a.id !== currentId)
        .sort((a, b) => (a.category === category ? -1 : 1));
    }
  } catch {
    // fallback
  }

  const allCurated = Object.values(CURATED_ATTRACTION_METADATA) as AttractionItem[];
  return allCurated.filter((a) => a.id !== currentId);
}

export async function generateMetadata({
  params,
}: {
  params: Promise<{ id: string }>;
}): Promise<Metadata> {
  const { id } = await params;
  const attraction = await getAttraction(id);

  if (!attraction) {
    return {
      title: "Attraction Not Found | Mangatarem Tourism",
    };
  }

  const enriched = enrichAttraction(attraction);

  return {
    title: `${enriched.name} | Mangatarem Tourism`,
    description: enriched.description || `Discover ${enriched.name} in Mangatarem, Pangasinan.`,
    openGraph: {
      title: `${enriched.name} — Mangatarem Cultural Map`,
      description: enriched.description || "",
      images: enriched.image_url ? [{ url: enriched.image_url }] : [],
    },
  };
}

export default async function AttractionDetailPage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = await params;
  const attraction = await getAttraction(id);

  if (!attraction) {
    notFound();
  }

  const [reviewData, relatedAttractions] = await Promise.all([
    getReviews(id),
    getRelatedAttractions(attraction.id, attraction.category),
  ]);

  return (
    <div className="container mx-auto px-4 py-8 sm:py-10">
      <AttractionDetailView
        attraction={attraction}
        reviews={reviewData.reviews}
        reviewSummary={reviewData.summary}
        relatedAttractions={relatedAttractions}
      />
    </div>
  );
}
