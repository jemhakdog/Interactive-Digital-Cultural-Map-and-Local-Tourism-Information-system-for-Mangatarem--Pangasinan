import Link from "next/link";
import { Building2 } from "lucide-react";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

async function getBusiness() {
  try {
    const res = await fetch("http://localhost:8000/api/business", { next: { revalidate: 60 } });
    if (!res.ok) return { items: [] };
    return res.json();
  } catch { return { items: [] }; }
}

export default async function BusinessPage() {
  const data = await getBusiness();
  const businesses = (data.items ?? []) as { id: number; name: string; category?: string; image_url?: string; barangay_name?: string; average_rating?: number }[];

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-2">Business Directory</h1>
      <p className="text-muted-foreground mb-8">Restaurants, hotels, and local establishments</p>

      {businesses.length === 0 ? (
        <div className="text-center py-16 text-muted-foreground">
          <Building2 className="h-12 w-12 mx-auto mb-4 opacity-30" />
          <p>No businesses found.</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {businesses.map((b) => (
            <Link key={b.id} href={`/business/${b.id}`}>
              <Card className="overflow-hidden hover:shadow-md transition-shadow group h-full">
                <div className="aspect-[4/3] bg-muted relative overflow-hidden">
                  {b.image_url ? (
                    <img src={b.image_url} alt={b.name} className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300" />
                  ) : (
                    <div className="w-full h-full flex items-center justify-center">
                      <Building2 className="h-12 w-12 text-muted-foreground/30" />
                    </div>
                  )}
                </div>
                <CardContent className="p-4">
                  <h3 className="font-semibold line-clamp-1">{b.name}</h3>
                  {b.category && <Badge variant="secondary" className="mt-1 text-xs">{b.category}</Badge>}
                  {b.barangay_name && <p className="text-xs text-muted-foreground mt-1">{b.barangay_name}</p>}
                  {b.average_rating != null && (
                    <p className="text-xs text-muted-foreground mt-1">★ {Number(b.average_rating).toFixed(1)}</p>
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
