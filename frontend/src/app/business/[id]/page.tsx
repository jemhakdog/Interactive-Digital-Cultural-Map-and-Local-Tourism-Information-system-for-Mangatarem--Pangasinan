import { notFound } from "next/navigation";
import type { Metadata } from "next";
import { BusinessDetailView, BusinessDetailData } from "./business-detail-view";
import { EstablishmentItem } from "../business-view";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

async function getBusiness(id: string): Promise<BusinessDetailData | null> {
  try {
    const res = await fetch(`${API_BASE}/api/business/${id}`, {
      next: { revalidate: 60 },
    });
    if (!res.ok) return null;
    const data = await res.json();
    if (!data || !data.establishment) return null;
    return data as BusinessDetailData;
  } catch {
    return null;
  }
}

async function getAllBusinesses(): Promise<EstablishmentItem[]> {
  try {
    const res = await fetch(`${API_BASE}/api/business/?per_page=50`, {
      next: { revalidate: 60 },
    });
    if (!res.ok) return [];
    const data = await res.json();
    return (data.establishments ?? data.businesses ?? data.items ?? []) as EstablishmentItem[];
  } catch {
    return [];
  }
}

export async function generateMetadata({
  params,
}: {
  params: Promise<{ id: string }>;
}): Promise<Metadata> {
  const { id } = await params;
  const data = await getBusiness(id);
  if (!data || !data.establishment) {
    return {
      title: "Business Not Found | Mangatarem Tourism",
    };
  }
  return {
    title: `${data.establishment.name} | Mangatarem Tourism`,
    description:
      data.establishment.description ||
      `Certified local business and hospitality establishment in Mangatarem, Pangasinan.`,
  };
}

export default async function BusinessDetailPage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = await params;
  const [data, allBusinesses] = await Promise.all([getBusiness(id), getAllBusinesses()]);

  if (!data || !data.establishment) notFound();

  // Filter out current business from related
  const relatedBusinesses = allBusinesses.filter(
    (b) => String(b.id) !== id
  );

  return (
    <div className="container mx-auto px-4 py-8">
      <BusinessDetailView data={data} relatedBusinesses={relatedBusinesses} />
    </div>
  );
}
