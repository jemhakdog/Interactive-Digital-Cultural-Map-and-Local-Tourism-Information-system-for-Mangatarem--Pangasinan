import Link from "next/link";
import { Calendar } from "lucide-react";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

async function getEvents() {
  try {
    const res = await fetch("http://localhost:8000/api/events", { next: { revalidate: 60 } });
    if (!res.ok) return { items: [] };
    return res.json();
  } catch { return { items: [] }; }
}

export default async function EventsPage() {
  const data = await getEvents();
  const events = (data.items ?? []) as { id: number; name: string; category?: string; date?: string; image_url?: string; barangay_name?: string }[];

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-2">Events</h1>
      <p className="text-muted-foreground mb-8">What&apos;s happening in Mangatarem</p>

      {events.length === 0 ? (
        <div className="text-center py-16 text-muted-foreground">
          <Calendar className="h-12 w-12 mx-auto mb-4 opacity-30" />
          <p>No events found.</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {events.map((e) => (
            <Link key={e.id} href={`/events/${e.id}`}>
              <Card className="overflow-hidden hover:shadow-md transition-shadow group h-full">
                <div className="aspect-[4/3] bg-muted relative overflow-hidden">
                  {e.image_url ? (
                    <img src={e.image_url} alt={e.name} className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300" />
                  ) : (
                    <div className="w-full h-full flex items-center justify-center">
                      <Calendar className="h-12 w-12 text-muted-foreground/30" />
                    </div>
                  )}
                </div>
                <CardContent className="p-4">
                  <h3 className="font-semibold line-clamp-1">{e.name}</h3>
                  {e.date && (
                    <p className="text-xs text-muted-foreground mt-1">
                      {new Date(e.date).toLocaleDateString("en-PH", { month: "short", day: "numeric", year: "numeric" })}
                    </p>
                  )}
                  {e.category && <Badge variant="secondary" className="mt-1 text-xs">{e.category}</Badge>}
                  {e.barangay_name && <p className="text-xs text-muted-foreground mt-1">{e.barangay_name}</p>}
                </CardContent>
              </Card>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}
