import Link from "next/link";
import { MapPin, Calendar, Search, ArrowRight } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

// Server Component — fetches directly
async function getHomeData() {
  try {
    const res = await fetch("http://localhost:8000/api/", { next: { revalidate: 60 } });
    if (!res.ok) return null;
    return res.json();
  } catch { return null; }
}

function AttractionCard({ item }: { item: { id: number; name: string; category?: string; image_url?: string; barangay_name?: string } }) {
  return (
    <Link href={`/attractions/${item.id}`}>
      <Card className="overflow-hidden hover:shadow-md transition-shadow group cursor-pointer h-full">
        <div className="aspect-[4/3] bg-muted relative overflow-hidden">
          {item.image_url ? (
            <img
              src={item.image_url}
              alt={item.name}
              className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
            />
          ) : (
            <div className="w-full h-full flex items-center justify-center">
              <MapPin className="h-12 w-12 text-muted-foreground/30" />
            </div>
          )}
        </div>
        <CardContent className="p-4">
          <h3 className="font-semibold text-base line-clamp-1">{item.name}</h3>
          {item.category && (
            <Badge variant="secondary" className="mt-1 text-xs">{item.category}</Badge>
          )}
          {item.barangay_name && (
            <p className="text-xs text-muted-foreground mt-1">{item.barangay_name}</p>
          )}
        </CardContent>
      </Card>
    </Link>
  );
}

function EventCard({ item }: { item: { id: number; name: string; category?: string; date?: string; image_url?: string; barangay_name?: string } }) {
  return (
    <Link href={`/events/${item.id}`}>
      <Card className="overflow-hidden hover:shadow-md transition-shadow group cursor-pointer h-full">
        <div className="aspect-[4/3] bg-muted relative overflow-hidden">
          {item.image_url ? (
            <img
              src={item.image_url}
              alt={item.name}
              className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
            />
          ) : (
            <div className="w-full h-full flex items-center justify-center">
              <Calendar className="h-12 w-12 text-muted-foreground/30" />
            </div>
          )}
        </div>
        <CardContent className="p-4">
          <h3 className="font-semibold text-base line-clamp-1">{item.name}</h3>
          {item.date && (
            <p className="text-xs text-muted-foreground mt-1">
              {new Date(item.date).toLocaleDateString("en-PH", { month: "short", day: "numeric", year: "numeric" })}
            </p>
          )}
          {item.barangay_name && (
            <p className="text-xs text-muted-foreground">{item.barangay_name}</p>
          )}
        </CardContent>
      </Card>
    </Link>
  );
}

export default async function HomePage() {
  const data = await getHomeData();
  const attractions = (data?.featured_attractions ?? []) as { id: number; name: string; category?: string; image_url?: string; barangay_name?: string }[];
  const events = (data?.featured_events ?? []) as { id: number; name: string; category?: string; date?: string; image_url?: string; barangay_name?: string }[];

  return (
    <div>
      {/* Hero */}
      <section className="relative bg-primary text-primary-foreground">
        <div className="container mx-auto px-4 py-20 md:py-32 text-center">
          <h1 className="text-3xl md:text-5xl font-bold mb-4">
            Discover Mangatarem
          </h1>
          <p className="text-lg md:text-xl opacity-90 max-w-2xl mx-auto mb-8">
            Explore the cultural heritage, natural wonders, and vibrant community
            of Mangatarem, Pangasinan.
          </p>
          <div className="flex flex-col sm:flex-row gap-3 justify-center">
            <Link href="/attractions">
              <Button size="lg" variant="secondary" className="gap-2">
                <MapPin className="h-5 w-5" /> Explore Attractions
              </Button>
            </Link>
            <Link href="/search">
              <Button size="lg" variant="outline" className="gap-2 border-white/30 text-white hover:bg-white/10">
                <Search className="h-5 w-5" /> Search
              </Button>
            </Link>
          </div>
        </div>
      </section>

      {/* Featured Attractions */}
      {attractions.length > 0 && (
        <section className="container mx-auto px-4 py-12">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-2xl font-bold">Featured Attractions</h2>
            <Link href="/attractions" className="text-sm text-primary hover:underline flex items-center gap-1">
              View all <ArrowRight className="h-4 w-4" />
            </Link>
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {attractions.map((a) => (
              <AttractionCard key={a.id} item={a} />
            ))}
          </div>
        </section>
      )}

      {/* Featured Events */}
      {events.length > 0 && (
        <section className="container mx-auto px-4 py-12 bg-muted/30">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-2xl font-bold">Upcoming Events</h2>
            <Link href="/events" className="text-sm text-primary hover:underline flex items-center gap-1">
              View all <ArrowRight className="h-4 w-4" />
            </Link>
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {events.map((e) => (
              <EventCard key={e.id} item={e} />
            ))}
          </div>
        </section>
      )}

      {/* CTA */}
      <section className="container mx-auto px-4 py-16 text-center">
        <h2 className="text-2xl font-bold mb-3">Plan Your Visit</h2>
        <p className="text-muted-foreground max-w-lg mx-auto mb-6">
          Use our interactive map to find the best attractions, restaurants, and
          accommodations in Mangatarem.
        </p>
        <Link href="/map">
          <Button size="lg" className="gap-2">
            <MapPin className="h-5 w-5" /> Open Map
          </Button>
        </Link>
      </section>
    </div>
  );
}
