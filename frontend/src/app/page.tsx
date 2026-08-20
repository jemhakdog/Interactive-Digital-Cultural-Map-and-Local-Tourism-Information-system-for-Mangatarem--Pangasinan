import Link from "next/link";
import { MapPin, Calendar, Search, ArrowRight, Compass, Star, Landmark, Building2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

async function getHome() {
  try {
    const res = await fetch(`${API_BASE}/api/`, { next: { revalidate: 60 } });
    if (!res.ok) return { featured_attractions: [], featured_events: [] };
    return res.json();
  } catch {
    return { featured_attractions: [], featured_events: [] };
  }
}

function AttractionCard({ item }: { item: { id: number; name: string; category?: string; image_url?: string; barangay_name?: string; average_rating?: number } }) {
  return (
    <Link href={`/attractions/${item.id}`}>
      <Card className="group overflow-hidden border-border/50 hover:shadow-lg hover:shadow-primary/5 transition-all duration-300 hover:-translate-y-0.5 h-full">
        <div className="aspect-[4/3] bg-muted relative overflow-hidden">
          {item.image_url ? (
            <img src={item.image_url} alt={item.name} className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500" />
          ) : (
            <div className="w-full h-full flex items-center justify-center">
              <MapPin className="h-10 w-10 text-muted-foreground/20" />
            </div>
          )}
          {item.category && (
            <Badge variant="secondary" className="absolute top-3 left-3 text-xs bg-background/80 backdrop-blur-sm">
              {item.category}
            </Badge>
          )}
        </div>
        <CardContent className="p-4">
          <h3 className="font-semibold text-sm line-clamp-1 group-hover:text-primary transition-colors">{item.name}</h3>
          <div className="flex items-center gap-2 mt-1">
            {item.barangay_name && <p className="text-xs text-muted-foreground">{item.barangay_name}</p>}
            {item.average_rating != null && (
              <p className="text-xs text-muted-foreground flex items-center gap-0.5">
                <Star className="h-3 w-3 fill-amber-400 text-amber-400" />
                {item.average_rating.toFixed(1)}
              </p>
            )}
          </div>
        </CardContent>
      </Card>
    </Link>
  );
}

function EventCard({ item }: { item: { id: number; name: string; category?: string; date?: string; image_url?: string; barangay_name?: string } }) {
  return (
    <Link href={`/events/${item.id}`}>
      <Card className="group overflow-hidden border-border/50 hover:shadow-lg hover:shadow-primary/5 transition-all duration-300 hover:-translate-y-0.5 h-full">
        <div className="aspect-[4/3] bg-muted relative overflow-hidden">
          {item.image_url ? (
            <img src={item.image_url} alt={item.name} className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500" />
          ) : (
            <div className="w-full h-full flex items-center justify-center">
              <Calendar className="h-10 w-10 text-muted-foreground/20" />
            </div>
          )}
          {item.category && (
            <Badge variant="secondary" className="absolute top-3 left-3 text-xs bg-background/80 backdrop-blur-sm">
              {item.category}
            </Badge>
          )}
          {item.date && (
            <div className="absolute top-3 right-3 bg-background/80 backdrop-blur-sm rounded-lg px-2 py-1 text-center">
              <p className="text-[10px] font-medium text-muted-foreground leading-none">
                {new Date(item.date).toLocaleDateString("en-PH", { month: "short" })}
              </p>
              <p className="text-sm font-bold leading-tight">
                {new Date(item.date).getDate()}
              </p>
            </div>
          )}
        </div>
        <CardContent className="p-4">
          <h3 className="font-semibold text-sm line-clamp-1 group-hover:text-primary transition-colors">{item.name}</h3>
          {item.barangay_name && <p className="text-xs text-muted-foreground mt-1">{item.barangay_name}</p>}
        </CardContent>
      </Card>
    </Link>
  );
}

export default async function HomePage() {
  const data = await getHome();
  const attractions = (data.featured_attractions ?? []) as { id: number; name: string; category?: string; image_url?: string; barangay_name?: string; average_rating?: number }[];
  const events = (data.featured_events ?? []) as { id: number; name: string; category?: string; date?: string; image_url?: string; barangay_name?: string }[];

  return (
    <div>
      {/* Hero */}
      <section className="relative overflow-hidden bg-gradient-to-br from-primary via-primary to-primary/80 text-primary-foreground">
        <div className="absolute inset-0 opacity-10">
          <div className="absolute top-0 left-0 w-96 h-96 bg-white/20 rounded-full -translate-x-1/2 -translate-y-1/2 blur-3xl" />
          <div className="absolute bottom-0 right-0 w-80 h-80 bg-white/15 rounded-full translate-x-1/3 translate-y-1/3 blur-3xl" />
        </div>
        <div className="container relative mx-auto px-4 py-20 md:py-32 text-center">
          <div className="inline-flex items-center gap-2 bg-white/10 backdrop-blur-sm rounded-full px-4 py-1.5 text-sm mb-6">
            <Compass className="h-4 w-4" />
            Discover Pangasinan
          </div>
          <h1 className="text-4xl md:text-6xl font-bold mb-4 tracking-tight">
            Explore Mangatarem
          </h1>
          <p className="text-lg md:text-xl text-primary-foreground/80 max-w-2xl mx-auto mb-8">
            An interactive digital cultural map and local tourism information system
            for Mangatarem, Pangasinan.
          </p>
          <div className="flex flex-wrap justify-center gap-3">
            <Link href="/attractions">
              <Button size="lg" className="gap-2 bg-white text-primary hover:bg-white/90 rounded-xl shadow-lg shadow-black/10">
                <MapPin className="h-5 w-5" /> Explore Attractions
              </Button>
            </Link>
            <Link href="/map">
              <Button size="lg" className="gap-2 bg-white/15 hover:bg-white/25 text-white border border-white/30 backdrop-blur-sm rounded-xl shadow-sm">
                <Search className="h-5 w-5" /> Open Map
              </Button>
            </Link>
          </div>
        </div>
      </section>

      {/* Quick links */}
      <section className="container mx-auto px-4 -mt-8 md:-mt-10 relative z-10">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {[
            { href: "/attractions", icon: MapPin, label: "Attractions", count: "Places to visit" },
            { href: "/events", icon: Calendar, label: "Events", count: "What's happening" },
            { href: "/heritage", icon: Landmark, label: "Heritage", count: "Cultural sites" },
            { href: "/business", icon: Building2, label: "Business", count: "Local spots" },
          ].map(({ href, icon: Icon, label, count }) => (
            <Link key={href} href={href}>
              <Card className="bg-card border border-border shadow-md shadow-black/5 hover:shadow-lg hover:border-primary/30 hover:-translate-y-0.5 transition-all duration-200 cursor-pointer">
                <CardContent className="p-4 flex items-center gap-3">
                  <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-primary/10 text-primary">
                    <Icon className="h-5 w-5" />
                  </div>
                  <div>
                    <p className="font-semibold text-sm">{label}</p>
                    <p className="text-xs text-muted-foreground">{count}</p>
                  </div>
                </CardContent>
              </Card>
            </Link>
          ))}
        </div>
      </section>

      {/* Featured Attractions */}
      {attractions.length > 0 && (
        <section className="container mx-auto px-4 py-16">
          <div className="flex items-center justify-between mb-6">
            <div>
              <h2 className="text-2xl font-bold tracking-tight">Featured Attractions</h2>
              <p className="text-muted-foreground text-sm mt-1">Must-visit spots in Mangatarem</p>
            </div>
            <Link href="/attractions" className="text-sm text-primary hover:underline flex items-center gap-1 font-medium">
              View all <ArrowRight className="h-4 w-4" />
            </Link>
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
            {attractions.map((a) => (
              <AttractionCard key={a.id} item={a} />
            ))}
          </div>
        </section>
      )}

      {/* Featured Events */}
      {events.length > 0 && (
        <section className="bg-muted/30">
          <div className="container mx-auto px-4 py-16">
            <div className="flex items-center justify-between mb-6">
              <div>
                <h2 className="text-2xl font-bold tracking-tight">Upcoming Events</h2>
                <p className="text-muted-foreground text-sm mt-1">Festivals and happenings</p>
              </div>
              <Link href="/events" className="text-sm text-primary hover:underline flex items-center gap-1 font-medium">
                View all <ArrowRight className="h-4 w-4" />
              </Link>
            </div>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
              {events.map((e) => (
                <EventCard key={e.id} item={e} />
              ))}
            </div>
          </div>
        </section>
      )}

      {/* CTA */}
      <section className="container mx-auto px-4 py-16 text-center">
        <div className="max-w-lg mx-auto">
          <h2 className="text-2xl font-bold mb-3 tracking-tight">Plan Your Visit</h2>
          <p className="text-muted-foreground mb-6">
            Use our interactive map to find the best attractions, restaurants, and
            accommodations in Mangatarem.
          </p>
          <Link href="/map">
            <Button size="lg" className="gap-2 rounded-xl">
              <MapPin className="h-5 w-5" /> Open Interactive Map
            </Button>
          </Link>
        </div>
      </section>
    </div>
  );
}
