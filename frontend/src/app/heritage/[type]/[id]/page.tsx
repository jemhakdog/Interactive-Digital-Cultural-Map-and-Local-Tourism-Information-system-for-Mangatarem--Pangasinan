import { notFound } from "next/navigation";
import type { Metadata } from "next";
import { HeritageDetailView } from "./heritage-detail-view";
import {
  HERITAGE_TYPES_CONFIG,
  HeritageItem,
} from "../../heritage-types";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

async function getHeritageItem(type: string, id: string): Promise<HeritageItem | null> {
  try {
    const res = await fetch(`${API_BASE}/api/heritage/${type}/${id}`, {
      next: { revalidate: 60 },
    });
    if (!res.ok) return null;
    return res.json();
  } catch {
    return null;
  }
}

async function getRelatedHeritage(type: string): Promise<HeritageItem[]> {
  try {
    const res = await fetch(`${API_BASE}/api/heritage/${type}?per_page=10`, {
      next: { revalidate: 60 },
    });
    if (!res.ok) return [];
    const data = await res.json();
    return (data.items ?? []) as HeritageItem[];
  } catch {
    return [];
  }
}

export async function generateMetadata({
  params,
}: {
  params: Promise<{ type: string; id: string }>;
}): Promise<Metadata> {
  const { type, id } = await params;
  const item = await getHeritageItem(type, id);

  if (!item) {
    return {
      title: "Heritage Item Not Found",
    };
  }

  const typeConfig = HERITAGE_TYPES_CONFIG[type];
  const typeLabel = typeConfig ? typeConfig.label : "Heritage";

  return {
    title: `${item.name_of_asset} — ${typeLabel} | Mangatarem Tourism`,
    description:
      item.significance ||
      `Official registry profile for ${item.name_of_asset} in Mangatarem, Pangasinan.`,
  };
}

export default async function HeritageDetailPage({
  params,
}: {
  params: Promise<{ type: string; id: string }>;
}) {
  const { type, id } = await params;
  const [item, relatedList] = await Promise.all([
    getHeritageItem(type, id),
    getRelatedHeritage(type),
  ]);

  if (!item) {
    notFound();
  }

  const relatedItems = relatedList.filter((r) => String(r.id) !== id);

  return (
    <div className="container mx-auto px-4 py-8">
      <HeritageDetailView item={item} relatedItems={relatedItems} />
    </div>
  );
}
