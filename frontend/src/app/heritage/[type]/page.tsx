import { notFound } from "next/navigation";
import type { Metadata } from "next";
import { HeritageTypeView } from "./heritage-type-view";
import {
  HERITAGE_TYPES_CONFIG,
  HeritageItem,
} from "../heritage-types";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

interface TypeData {
  slug: string;
  label: string;
  count: number;
}

async function getHeritageItemsByType(type: string): Promise<HeritageItem[]> {
  try {
    const res = await fetch(`${API_BASE}/api/heritage/${type}?per_page=100`, {
      next: { revalidate: 60 },
    });
    if (!res.ok) return [];
    const data = await res.json();
    return (data.items ?? []) as HeritageItem[];
  } catch {
    return [];
  }
}

async function getAllHeritageTypes(): Promise<TypeData[]> {
  try {
    const res = await fetch(`${API_BASE}/api/heritage/types`, {
      next: { revalidate: 60 },
    });
    if (!res.ok) return [];
    const data = await res.json();
    return (data.types ?? []) as TypeData[];
  } catch {
    return [];
  }
}

export async function generateMetadata({
  params,
}: {
  params: Promise<{ type: string }>;
}): Promise<Metadata> {
  const { type } = await params;
  const config = HERITAGE_TYPES_CONFIG[type];

  if (!config) {
    return {
      title: "Heritage Classification Not Found",
    };
  }

  return {
    title: `${config.label_plural} | Mangatarem Heritage Registry`,
    description: `Official registry and documentation of ${config.label_plural.toLowerCase()} in Mangatarem, Pangasinan. ${config.description}`,
  };
}

export default async function HeritageTypePage({
  params,
}: {
  params: Promise<{ type: string }>;
}) {
  const { type } = await params;
  const config = HERITAGE_TYPES_CONFIG[type];

  if (!config) {
    notFound();
  }

  const [items, allTypes] = await Promise.all([
    getHeritageItemsByType(type),
    getAllHeritageTypes(),
  ]);

  return (
    <div className="container mx-auto px-4 py-8">
      <HeritageTypeView
        typeSlug={type}
        items={items}
        otherTypes={allTypes}
      />
    </div>
  );
}
