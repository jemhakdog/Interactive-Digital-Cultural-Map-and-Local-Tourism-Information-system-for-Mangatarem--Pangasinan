import { notFound } from "next/navigation";
import Link from "next/link";
import { ArrowLeft, Building2, MapPin, Star } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { Separator } from "@/components/ui/separator";

async function getBusiness(id: string) {
  try {
    const res = await fetch(`http://localhost:8000/api/business/${id}`, { next: { revalidate: 60 } });
    if (!res.ok) return null;
    return res.json();
  } catch { return null; }
}

export default async function BusinessDetailPage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = await params;
  const business = await getBusiness(id);
  if (!business) notFound();

  return (
    <div className="container mx-auto px-4 py-8">
      <Link href="/business" className="inline-flex items-center gap-1 text-sm text-muted-foreground hover:text-foreground mb-6">
        <ArrowLeft className="h-4 w-4" /> Back to Business
      </Link>

      {business.image_url && (
        <div className="aspect-[21/9] bg-muted rounded-lg overflow-hidden mb-8">
          <img src={String(business.image_url)} alt={String(business.name)} className="w-full h-full object-cover" />
        </div>
      )}

      <div className="max-w-3xl">
        <div className="flex items-start justify-between gap-4">
          <div>
            <h1 className="text-3xl font-bold">{String(business.name)}</h1>
            <div className="flex flex-wrap gap-2 mt-2">
              {business.category && <Badge variant="secondary">{String(business.category)}</Badge>}
              {business.barangay_name && <Badge variant="outline">{String(business.barangay_name)}</Badge>}
            </div>
          </div>
          {business.average_rating != null && (
            <div className="flex items-center gap-1 text-sm">
              <Star className="h-4 w-4 fill-primary text-primary" />
              <span className="font-semibold">{Number(business.average_rating).toFixed(1)}</span>
            </div>
          )}
        </div>

        {business.description && (
          <p className="mt-6 text-muted-foreground leading-relaxed">{String(business.description)}</p>
        )}

        {business.address && (
          <div className="mt-4 flex items-center gap-2 text-sm text-muted-foreground">
            <MapPin className="h-4 w-4" />
            {String(business.address)}
          </div>
        )}

        {business.contact_phone && (
          <p className="mt-2 text-sm text-muted-foreground">📞 {String(business.contact_phone)}</p>
        )}

        {/* Rooms */}
        {business.rooms && business.rooms.length > 0 && (
          <>
            <Separator className="my-8" />
            <h2 className="text-xl font-bold mb-4">Rooms</h2>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              {(business.rooms as Record<string, unknown>[]).map((room, i) => (
                <div key={i} className="border rounded-lg p-4">
                  <h3 className="font-medium">{String(room.name)}</h3>
                  <p className="text-sm text-muted-foreground">{String(room.description ?? "")}</p>
                  {room.price != null && <p className="text-sm font-semibold mt-1">₱{Number(room.price).toLocaleString()}</p>}
                </div>
              ))}
            </div>
          </>
        )}

        {/* Menu */}
        {business.menu_items && business.menu_items.length > 0 && (
          <>
            <Separator className="my-8" />
            <h2 className="text-xl font-bold mb-4">Menu</h2>
            <div className="space-y-2">
              {(business.menu_items as Record<string, unknown>[]).map((item, i) => (
                <div key={i} className="flex justify-between border-b pb-2">
                  <span className="text-sm">{String(item.name)}</span>
                  {item.price != null && <span className="text-sm font-medium">₱{Number(item.price).toLocaleString()}</span>}
                </div>
              ))}
            </div>
          </>
        )}
      </div>
    </div>
  );
}
