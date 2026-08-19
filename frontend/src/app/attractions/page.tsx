import Link from "next/link";
import { MapPin } from "lucide-react";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

async function getAttractions(category?: string, barangay?: string) {
  const params = new URLSearchParams();
  if (category && category !== "all") params.set("category", category);
  if (barangay && barangay !== "all") params.set("barangay", barangay);
  try {
    const res = await fetch(`http://localhost:8000/api/attractions?${params}`, { next: { revalidate: 60 } });
    if (!res.ok) return { items: [], categories: [], barangays: [] };
    return res.json();
  } catch { return { items: [], categories: [], barangays: [] }; }
}

export default async function AttractionsPage({
  searchParams,
}: {
  searchParams: Promise<{ category?: string; barangay?: string }>;
}) {
  const sp = await searchParams;
  const data = await getAttractions(sp.category, sp.barangay);
  const attractions = (data.attractions ?? data.items ?? []) as { id: number; name: string; category?: string; image_url?: string; barangay_name?: string; average_rating?: number }[];

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-2">Attractions</h1>
      <p className="text-muted-foreground mb-8">Discover the beauty and culture of Mangatarem</p>

      {attractions.length === 0 ? (
        <div className="text-center py-16 text-muted-foreground">
          <MapPin className="h-12 w-12 mx-auto mb-4 opacity-30" />
          <p>No attractions found.</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {attractions.map((a) => (
            <Link key={a.id} href={`/attractions/${a.id}`}>
              <Card className="overflow-hidden hover:shadow-md transition-shadow group h-full">
                <div className="aspect-[4/3] bg-muted relative overflow-hidden">
                  {a.image_url ? (
                    <img src={a.image_url} alt={a.name} className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300" />
                  ) : (
                    <div className="w-full h-full flex items-center justify-center">
                      <MapPin className="h-12 w-12 text-muted-foreground/30" />
                    </div>
                  )}
                </div>
                <CardContent className="p-4">
                  <h3 className="font-semibold line-clamp-1">{a.name}</h3>
                  {a.category && <Badge variant="secondary" className="mt-1 text-xs">{a.category}</Badge>}
                  {a.barangay_name && <p className="text-xs text-muted-foreground mt-1">{a.barangay_name}</p>}
                  {a.average_rating != null && (
                    <p className="text-xs text-muted-foreground mt-1">★ {a.average_rating.toFixed(1)}</p>
                  )}
                </CardContent>
              </Card>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}
