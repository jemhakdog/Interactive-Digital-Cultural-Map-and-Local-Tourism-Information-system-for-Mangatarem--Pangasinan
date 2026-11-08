import Link from "next/link";
import Image from "next/image";
import {
  MapPin,
  Calendar,
  Search,
  ArrowRight,
  Compass,
  Star,
  Landmark,
  Building2,
  Navigation,
  Bell,
  Map as MapIcon,
  BookOpen,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { HeroSearch } from "@/components/public/hero-search";
import { NewsletterSubscribe } from "@/components/public/newsletter-subscribe";
import { CURATED_ATTRACTION_METADATA } from "@/app/attractions/attraction-data";
import { resolvePlaceImage } from "@/components/map/data";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

const FALLBACK_EVENTS = [
  {
    id: 101,
    name: "Mangatarem Mango & Agri-Tourism Fair",
    category: "Festival",
    date: "2026-04-18T08:00:00",
    image_url: "/img/attractions/san_raymundo_de_penafort_parish_church/image_1.jpg",
    barangay_name: "Poblacion",
    description:
      "Annual cultural festival showcasing Mangatarem's sweet carabao mango harvests, local artisans, folk dance exhibitions, and agri-tourism innovations.",
  },
  {
    id: 102,
    name: "Feast of San Raymundo de Peñafort",
    category: "Religious",
    date: "2026-01-23T06:00:00",
    image_url: "/img/attractions/san_raymundo_de_penafort_parish_church/image_2.jpg",
    barangay_name: "Poblacion",
    description:
      "Centuries-old parish fiesta tradition featuring solemn mass processions, historical church tours, and evening community band performances.",
  },
  {
    id: 103,
    name: "Manleluag Eco-Trail & Tree Planting Walk",
    category: "Eco-Tour",
    date: "2026-06-05T06:30:00",
    image_url: "/img/manleluag_spring.webp",
    barangay_name: "Malabobo",
    description:
      "Guided morning biodiversity hike along the national protected landscape, including sulfuric spring baths and endemic birdwatching.",
  },
];

async function getHome() {
  try {
    const res = await fetch(`${API_BASE}/api/`, { next: { revalidate: 60 } });
    if (!res.ok) return { featured_attractions: [], featured_events: [] };
    return res.json();
  } catch {
    return { featured_attractions: [], featured_events: [] };
  }
}

function AttractionCard({
  item,
}: {
  item: {
    id: number;
    name: string;
    category?: string | null;
    image_url?: string | null;
    barangay_name?: string | null;
    average_rating?: number | null;
  };
}) {
  return (
    <Link
      href={`/attractions/${item.id}`}
      className="block h-full focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary rounded-xl"
    >
      <Card className="group overflow-hidden border-border/70 hover:shadow-lg hover:shadow-primary/5 transition-all duration-300 hover:-translate-y-0.5 h-full bg-card">
        <div className="aspect-[4/3] bg-muted relative overflow-hidden">
          {item.image_url ? (
            <Image
              src={item.image_url}
              alt={item.name}
              fill
              sizes="(max-width: 640px) 100vw, (max-width: 1024px) 50vw, 33vw"
              className="object-cover group-hover:scale-105 transition-transform duration-500"
            />
          ) : (
            <div className="w-full h-full flex items-center justify-center">
              <MapPin className="h-10 w-10 text-muted-foreground/30" />
            </div>
          )}
          {item.category && (
            <Badge
              variant="secondary"
              className="absolute top-3 left-3 text-xs bg-background/90 text-foreground font-sans font-medium backdrop-blur-sm border border-border/50 shadow-sm"
            >
              {item.category}
            </Badge>
          )}
        </div>
        <CardContent className="p-4">
          <h3 className="font-heading font-semibold text-lg line-clamp-1 group-hover:text-primary transition-colors text-foreground">
            {item.name}
          </h3>
          <div className="flex items-center gap-2 mt-1">
            {item.barangay_name && (
              <p className="text-xs font-sans text-muted-foreground">{item.barangay_name}</p>
            )}
            {item.average_rating != null && (
              <p className="text-xs font-sans text-muted-foreground flex items-center gap-0.5">
                <Star className="h-3 w-3 fill-amber-500 text-amber-500" />
                {item.average_rating.toFixed(1)}
              </p>
            )}
          </div>
        </CardContent>
      </Card>
    </Link>
  );
}

function EventCard({
  item,
}: {
  item: {
    id: number;
    name: string;
    category?: string | null;
    date?: string | null;
    image_url?: string | null;
    barangay_name?: string | null;
  };
}) {
  return (
    <Link
      href={`/events/${item.id}`}
      className="block h-full focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary rounded-xl"
    >
      <Card className="group overflow-hidden border-border/70 hover:shadow-lg hover:shadow-primary/5 transition-all duration-300 hover:-translate-y-0.5 h-full bg-card">
        <div className="aspect-[4/3] bg-muted relative overflow-hidden">
          {item.image_url ? (
            <Image
              src={item.image_url}
              alt={item.name}
              fill
              sizes="(max-width: 640px) 100vw, (max-width: 1024px) 50vw, 33vw"
              className="object-cover group-hover:scale-105 transition-transform duration-500"
            />
          ) : (
            <div className="w-full h-full flex items-center justify-center">
              <Calendar className="h-10 w-10 text-muted-foreground/30" />
            </div>
          )}
          {item.category && (
            <Badge
              variant="secondary"
              className="absolute top-3 left-3 text-xs bg-background/90 text-foreground font-sans font-medium backdrop-blur-sm border border-border/50 shadow-sm"
            >
              {item.category}
            </Badge>
          )}
          {item.date && (
            <div className="absolute top-3 right-3 bg-background/90 text-foreground border border-border/50 backdrop-blur-sm rounded-lg px-2.5 py-1 text-center font-sans shadow-sm">
              <p className="text-[10px] font-semibold text-muted-foreground uppercase leading-none">
                {new Date(item.date).toLocaleDateString("en-PH", { month: "short" })}
              </p>
              <p className="text-sm font-bold text-foreground leading-tight">
                {new Date(item.date).getDate()}
              </p>
            </div>
          )}
        </div>
        <CardContent className="p-4">
          <h3 className="font-heading font-semibold text-lg line-clamp-1 group-hover:text-primary transition-colors text-foreground">
            {item.name}
          </h3>
          {item.barangay_name && (
            <p className="text-xs font-sans text-muted-foreground mt-1">{item.barangay_name}</p>
          )}
        </CardContent>
      </Card>
    </Link>
  );
}

export default async function HomePage() {
  const data = await getHome();
  const apiAttractions = (data.featured_attractions ?? []) as {
    id: number;
    name: string;
    category?: string;
    image_url?: string;
    barangay_name?: string;
    average_rating?: number;
  }[];
  const apiEvents = (data.featured_events ?? []) as {
    id: number;
    name: string;
    category?: string;
    date?: string;
    image_url?: string;
    barangay_name?: string;
  }[];

  // Fallback to rich curated local entries if backend API is cold or unseeded
  const curatedFallbackAttractions = Object.values(CURATED_ATTRACTION_METADATA)
    .slice(0, 3)
    .map((item) => ({
      id: item.id!,
      name: item.name!,
      category: item.category ?? "Nature",
      image_url: resolvePlaceImage(item.gallery?.[0], item.name || "Mangatarem Attraction"),
      barangay_name: item.barangay_name ?? "Mangatarem",
      average_rating: item.rating ?? 4.9,
    }));

  const attractions = apiAttractions.length > 0 ? apiAttractions : curatedFallbackAttractions;
  const events = apiEvents.length > 0 ? apiEvents : FALLBACK_EVENTS;

  return (
    <div className="public-theme min-h-screen bg-background text-foreground transition-colors duration-200">
      {/* Editorial Hero */}
      <section className="relative border-b border-border/60 bg-gradient-to-b from-primary/10 via-background to-background pt-16 pb-20 md:pt-24 md:pb-28">
        <div className="container relative mx-auto px-4 text-center max-w-4xl">
          <div className="inline-flex items-center gap-2 bg-primary/10 border border-primary/20 text-primary rounded-full px-4 py-1.5 text-xs sm:text-sm font-sans font-medium mb-6">
            <Compass className="h-4 w-4" />
            Municipal Cultural Heritage Portal • Pangasinan
          </div>
          <h1 className="font-heading font-medium tracking-tight text-4xl sm:text-5xl lg:text-6xl text-foreground mb-4">
            Explore Mangatarem
          </h1>
          <p className="font-sans text-base sm:text-lg md:text-xl text-muted-foreground max-w-2xl mx-auto mb-8 leading-relaxed">
            Discover the centuries-old Spanish masonry of San Raymundo de Peñafort, the protected rainforest
            canopy of Manleluag Spring, and the scenic mountain corridors of Daang Kalikasan.
          </p>

          {/* Interactive Search */}
          <div className="max-w-2xl mx-auto">
            <HeroSearch />
          </div>

          <div className="flex flex-wrap justify-center gap-3 mt-8">
            <Link href="/attractions">
              <Button size="lg" className="gap-2 rounded-xl shadow-md font-sans">
                <MapPin className="h-5 w-5" /> Explore Attractions
              </Button>
            </Link>
            <Link href="/map">
              <Button size="lg" variant="outline" className="gap-2 rounded-xl border-border/80 font-sans">
                <Search className="h-5 w-5" /> Open Interactive Map
              </Button>
            </Link>
          </div>
        </div>
      </section>

      {/* Dual Conversion Gateway */}
      <section className="container mx-auto px-4 -mt-10 md:-mt-12 relative z-10 mb-12">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 max-w-5xl mx-auto">
          {/* Section 1: Interactive Map Portal */}
          <Link href="/map" className="group block focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary rounded-2xl">
            <Card className="h-full bg-card/95 backdrop-blur-sm border-2 border-primary/20 hover:border-primary/50 transition-all duration-300 hover:shadow-xl hover:shadow-primary/5 hover:-translate-y-1 overflow-hidden p-6">
              <div className="flex items-start justify-between gap-4">
                <div className="space-y-3 flex-1">
                  <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-primary/10 text-primary text-xs font-semibold font-sans">
                    <MapIcon className="h-3.5 w-3.5" /> Geospatial Discovery
                  </div>
                  <h2 className="font-heading font-semibold text-2xl text-foreground group-hover:text-primary transition-colors">
                    Explore Interactive Cultural Map
                  </h2>
                  <p className="text-sm font-sans text-muted-foreground leading-relaxed">
                    Navigate the 82 barangays with GPS coordinates, elevation profiles, and verified boundary surveys.
                  </p>
                  <div className="flex flex-wrap gap-2 pt-2">
                    <Badge variant="outline" className="font-sans text-xs border-primary/30 text-foreground bg-primary/5">
                      15 Cultural Sites
                    </Badge>
                    <Badge variant="outline" className="font-sans text-xs border-primary/30 text-foreground bg-primary/5">
                      8 Natural Attractions
                    </Badge>
                  </div>
                </div>
                <div className="hidden sm:flex h-14 w-14 shrink-0 items-center justify-center rounded-2xl bg-primary text-primary-foreground shadow-lg shadow-primary/20 group-hover:scale-105 transition-transform">
                  <Navigation className="h-6 w-6" />
                </div>
              </div>
            </Card>
          </Link>

          {/* Section 2: Cultural Heritage Portal */}
          <div className="rounded-2xl border-2 border-accent/20 bg-card/95 backdrop-blur-sm p-6 shadow-sm hover:border-accent/50 transition-all duration-300 flex flex-col justify-between">
            <div className="space-y-3">
              <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-accent/10 text-accent text-xs font-semibold font-sans">
                <BookOpen className="h-3.5 w-3.5" /> Curated Heritage Archives
              </div>
              <h2 className="font-heading font-semibold text-2xl text-foreground">
                Living Traditions & Heritage
              </h2>
              <p className="text-sm font-sans text-muted-foreground leading-relaxed">
                Filter and study the municipal cultural properties registered under the National Cultural Heritage Act.
              </p>
              <div className="flex flex-wrap gap-2 pt-2">
                <Link href="/heritage?type=built-heritage">
                  <Badge variant="secondary" className="font-sans text-xs hover:bg-accent hover:text-accent-foreground transition-colors cursor-pointer">
                    Built Heritage
                  </Badge>
                </Link>
                <Link href="/heritage?type=natural-heritage">
                  <Badge variant="secondary" className="font-sans text-xs hover:bg-accent hover:text-accent-foreground transition-colors cursor-pointer">
                    Natural Landscapes
                  </Badge>
                </Link>
                <Link href="/heritage?type=intangible-heritage">
                  <Badge variant="secondary" className="font-sans text-xs hover:bg-accent hover:text-accent-foreground transition-colors cursor-pointer">
                    Living Traditions
                  </Badge>
                </Link>
              </div>
            </div>
            <div className="pt-4 mt-auto">
              <Link href="/heritage" className="text-sm font-sans font-medium text-accent hover:underline inline-flex items-center gap-1.5">
                Browse Full Registry <ArrowRight className="h-4 w-4" />
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Quick Category Navigation Bar */}
      <section className="container mx-auto px-4 mb-16">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 max-w-5xl mx-auto">
          {[
            { href: "/attractions", icon: MapPin, label: "Attractions", count: "Natural springs & hills" },
            { href: "/events", icon: Calendar, label: "Events", count: "Fiestas & eco-tours" },
            { href: "/heritage", icon: Landmark, label: "Heritage", count: "Built & intangible sites" },
            { href: "/business", icon: Building2, label: "Business", count: "Dining & stay spots" },
          ].map(({ href, icon: Icon, label, count }) => (
            <Link key={href} href={href}>
              <Card className="bg-card border border-border/80 shadow-sm hover:shadow-md hover:border-primary/40 hover:-translate-y-0.5 transition-all duration-200 cursor-pointer h-full">
                <CardContent className="p-4 flex items-center gap-3">
                  <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-primary/10 text-primary">
                    <Icon className="h-5 w-5" />
                  </div>
                  <div>
                    <p className="font-heading font-medium text-base text-foreground">{label}</p>
                    <p className="text-xs font-sans text-muted-foreground">{count}</p>
                  </div>
                </CardContent>
              </Card>
            </Link>
          ))}
        </div>
      </section>

      {/* Featured Attractions */}
      {attractions.length > 0 && (
        <section className="container mx-auto px-4 py-12 border-t border-border/40">
          <div className="flex items-center justify-between mb-8 max-w-6xl mx-auto">
            <div>
              <h2 className="font-heading font-medium text-3xl tracking-tight text-foreground">Featured Attractions</h2>
              <p className="font-sans text-muted-foreground text-sm mt-1">Curated municipal destinations and eco-tourism sites</p>
            </div>
            <Link href="/attractions" className="font-sans text-sm text-primary hover:underline flex items-center gap-1 font-medium">
              View all <ArrowRight className="h-4 w-4" />
            </Link>
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 max-w-6xl mx-auto">
            {attractions.map((a) => (
              <AttractionCard key={a.id} item={a} />
            ))}
          </div>
        </section>
      )}

      {/* Featured Events */}
      {events.length > 0 && (
        <section className="bg-muted/30 border-t border-border/40 py-16">
          <div className="container mx-auto px-4 max-w-6xl">
            <div className="flex items-center justify-between mb-8">
              <div>
                <h2 className="font-heading font-medium text-3xl tracking-tight text-foreground">Seasonal Events & Announcements</h2>
                <p className="font-sans text-muted-foreground text-sm mt-1">Fiestas, agro-tourism festivals, and eco-walks</p>
              </div>
              <Link href="/events" className="font-sans text-sm text-primary hover:underline flex items-center gap-1 font-medium">
                View all <ArrowRight className="h-4 w-4" />
              </Link>
            </div>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
              {events.map((e) => (
                <EventCard key={e.id} item={e} />
              ))}
            </div>
          </div>
        </section>
      )}

      {/* Community Newsletter & Updates */}
      <section className="container mx-auto px-4 py-16">
        <div className="max-w-4xl mx-auto rounded-3xl bg-gradient-to-r from-primary/10 via-background to-accent/10 border border-border p-8 md:p-12">
          <div className="max-w-2xl mx-auto text-center space-y-4">
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-primary/15 text-primary text-xs font-semibold font-sans">
              <Bell className="h-3.5 w-3.5" /> Stay Updated
            </div>
            <h2 className="font-heading font-medium text-3xl tracking-tight text-foreground">
              Never Miss Mangatarem Tourism Announcements
            </h2>
            <p className="font-sans text-muted-foreground text-sm sm:text-base leading-relaxed">
              Get notified of upcoming town celebrations, protected landscape advisories, cultural heritage stories, and travel updates.
            </p>
            <div className="pt-2">
              <NewsletterSubscribe />
            </div>
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="bg-muted/20 border-t border-border/40 py-16 text-center">
        <div className="container mx-auto px-4 max-w-lg">
          <h2 className="font-heading font-medium text-3xl mb-3 tracking-tight text-foreground">Plan Your Visit</h2>
          <p className="font-sans text-muted-foreground mb-6 text-sm sm:text-base">
            Use our interactive digital map to discover attractions, restaurants, and historical landmarks in Mangatarem.
          </p>
          <Link href="/map">
            <Button size="lg" className="gap-2 rounded-xl font-sans shadow-md">
              <MapPin className="h-5 w-5" /> Open Interactive Map
            </Button>
          </Link>
        </div>
      </section>
    </div>
  );
}
