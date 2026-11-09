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
  MessageSquare,
  Award,
  Route,
  ShieldCheck,
  Globe2,
  Layers,
  Sparkles,
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
    barangay_name: "Poblacion Central",
    coordinates: "15.7911° N, 120.2939° E",
    description:
      "Annual municipal cultural fair celebrating sweet carabao mango harvests, local handloom crafts, folk music, and agri-tourism innovations.",
  },
  {
    id: 102,
    name: "Feast of San Raymundo de Peñafort",
    category: "Religious Heritage",
    date: "2026-01-23T06:00:00",
    image_url: "/img/st_raymund_church.webp",
    barangay_name: "Poblacion Central",
    coordinates: "15.7915° N, 120.2942° E",
    description:
      "Centuries-old parish feast featuring solemn historical processions, Spanish brick masonry tours, and evening community brass band performances.",
  },
  {
    id: 103,
    name: "Manleluag Eco-Trail & Canopy Walk",
    category: "Eco-Tour",
    date: "2026-06-05T06:30:00",
    image_url: "/img/manleluag_spring.webp",
    barangay_name: "Malabobo Sector",
    coordinates: "15.7061° N, 120.2811° E",
    description:
      "Guided morning biodiversity hike along the national protected landscape, featuring natural sulfuric spring pools and endemic bird observation.",
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
  const isWaterFeature =
    item.category?.toLowerCase().includes("spring") ||
    item.category?.toLowerCase().includes("water") ||
    item.category?.toLowerCase().includes("river");

  return (
    <Link
      href={`/attractions/${item.id}`}
      className="group block h-full focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary rounded-xl transition-all duration-200 ease-out hover:-translate-y-1.5 active:scale-[0.98]"
    >
      <Card className="h-full overflow-hidden bg-card border-[0.5px] border-border/90 shadow-sm hover:shadow-lg hover:border-primary/40 transition-all duration-200">
        <div className="aspect-[4/3] bg-muted/60 relative overflow-hidden">
          {item.image_url ? (
            <Image
              src={item.image_url}
              alt={item.name}
              fill
              sizes="(max-width: 640px) 100vw, (max-width: 1024px) 50vw, 33vw"
              className="object-cover group-hover:scale-105 transition-transform duration-500 ease-out"
            />
          ) : (
            <div className="w-full h-full flex flex-col items-center justify-center bg-muted/40 text-muted-foreground/50">
              <MapPin className="h-10 w-10 stroke-[1.5]" />
              <span className="text-xs font-sans mt-2">Field Archive Entry</span>
            </div>
          )}
          {item.category && (
            <Badge
              variant="secondary"
              className={`absolute top-3 left-3 text-xs font-sans font-medium backdrop-blur-md border shadow-sm transition-transform duration-200 group-hover:scale-105 ${
                isWaterFeature
                  ? "bg-[oklch(0.45_0.12_240)]/90 text-white border-[oklch(0.45_0.12_240)]/30"
                  : "bg-accent/90 text-accent-foreground border-accent/40"
              }`}
            >
              {item.category}
            </Badge>
          )}
        </div>
        <CardContent className="p-5">
          <div className="flex items-center justify-between text-xs font-sans text-muted-foreground mb-1.5">
            <span className="truncate">{item.barangay_name || "Mangatarem Sector"}</span>
            {item.average_rating != null && (
              <span className="flex items-center gap-1 font-semibold text-foreground">
                <Star className="h-3.5 w-3.5 fill-[oklch(0.75_0.15_75)] text-[oklch(0.75_0.15_75)] group-hover:rotate-12 group-hover:scale-110 transition-transform duration-300" />
                {item.average_rating.toFixed(1)}
              </span>
            )}
          </div>
          <h3 className="font-heading font-medium text-xl line-clamp-1 group-hover:text-primary transition-colors duration-200 text-foreground">
            {item.name}
          </h3>
          <p className="font-sans text-xs text-muted-foreground mt-2 inline-flex items-center gap-1 group-hover:text-primary transition-colors duration-200 font-medium">
            Inspect Field Dossier <ArrowRight className="h-3.5 w-3.5 group-hover:translate-x-1 transition-transform duration-200" />
          </p>
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
    coordinates?: string | null;
    description?: string | null;
  };
}) {
  return (
    <Link
      href={`/events/${item.id}`}
      className="group block h-full focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary rounded-xl transition-all duration-200 ease-out hover:-translate-y-1.5 active:scale-[0.98]"
    >
      <Card className="h-full overflow-hidden bg-card border-[0.5px] border-border/90 shadow-sm hover:shadow-lg hover:border-primary/40 transition-all duration-200 flex flex-col justify-between">
        <div>
          <div className="aspect-[16/9] bg-muted/60 relative overflow-hidden">
            {item.image_url ? (
              <Image
                src={item.image_url}
                alt={item.name}
                fill
                sizes="(max-width: 640px) 100vw, (max-width: 1024px) 50vw, 33vw"
                className="object-cover group-hover:scale-105 transition-transform duration-500 ease-out"
              />
            ) : (
              <div className="w-full h-full flex items-center justify-center bg-muted/40 text-muted-foreground/50">
                <Calendar className="h-10 w-10 stroke-[1.5]" />
              </div>
            )}
            {item.category && (
              <Badge
                variant="secondary"
                className="absolute top-3 left-3 text-xs bg-background/95 text-foreground font-sans font-medium backdrop-blur-md border border-border/80 shadow-sm transition-transform duration-200 group-hover:scale-105"
              >
                {item.category}
              </Badge>
            )}
            {item.date && (
              <div className="absolute top-3 right-3 bg-background/95 text-foreground border border-border/80 backdrop-blur-md rounded-lg px-2.5 py-1 text-center font-sans shadow-sm transition-all duration-200 group-hover:scale-105 group-hover:border-primary/50">
                <p className="text-[10px] font-semibold text-muted-foreground uppercase leading-none">
                  {new Date(item.date).toLocaleDateString("en-PH", { month: "short" })}
                </p>
                <p className="text-sm font-bold text-foreground leading-tight">
                  {new Date(item.date).getDate()}
                </p>
              </div>
            )}
          </div>
          <CardContent className="p-5 space-y-2">
            <div className="flex items-center gap-2 text-xs font-mono text-muted-foreground">
              <span>{item.coordinates || "Mangatarem, Pangasinan"}</span>
            </div>
            <h3 className="font-heading font-medium text-xl leading-snug line-clamp-1 group-hover:text-primary transition-colors duration-200 text-foreground">
              {item.name}
            </h3>
            {item.description && (
              <p className="font-sans text-xs sm:text-sm text-muted-foreground line-clamp-2 leading-relaxed">
                {item.description}
              </p>
            )}
          </CardContent>
        </div>
        <div className="px-5 pb-5 pt-0">
          <div className="pt-3 border-t border-border/60 flex items-center justify-between text-xs font-sans font-medium text-primary">
            <span>{item.barangay_name || "Municipal Sector"}</span>
            <span className="inline-flex items-center gap-1 group-hover:translate-x-1 transition-transform duration-200">
              Event Details <ArrowRight className="h-3.5 w-3.5" />
            </span>
          </div>
        </div>
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
      category: item.category ?? "Nature Sanctuary",
      image_url: resolvePlaceImage(item.gallery?.[0], item.name || "Mangatarem Attraction"),
      barangay_name: item.barangay_name ?? "Mangatarem",
      average_rating: item.rating ?? 4.9,
    }));

  const attractions = apiAttractions.length > 0 ? apiAttractions : curatedFallbackAttractions;
  const events = apiEvents.length > 0 ? apiEvents : FALLBACK_EVENTS;

  return (
    <div className="public-theme min-h-screen bg-background text-foreground transition-colors duration-200">
      {/* ── SECTION 1: Cartographic Orientation & Hero Gateway ── */}
      <section className="relative topo-grid border-b border-border/80 pt-10 pb-16 md:pt-16 md:pb-20 overflow-hidden">
        <div className="container mx-auto px-4 max-w-6xl">
          {/* Cartographer Coordinate Header Strip with Radar Ping */}
          <div className="flex flex-wrap items-center justify-between gap-3 text-xs font-mono text-muted-foreground border-b border-border/70 pb-3 mb-8">
            <div className="flex items-center gap-2.5">
              <span className="relative flex h-2.5 w-2.5">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-primary opacity-75" />
                <span className="relative inline-flex rounded-full h-2.5 w-2.5 bg-primary" />
              </span>
              <span className="font-medium text-foreground">15°47′28″N • 120°17′38″E</span>
              <span className="hidden sm:inline">• Elevation: 62m – 1,180m MASL</span>
            </div>
            <div className="flex items-center gap-3">
              <span className="hidden md:inline">Agno River Basin & Daang Kalikasan Corridor</span>
              <Badge variant="outline" className="text-[10px] uppercase tracking-wider font-mono border-primary/40 text-primary bg-primary/5">
                Official Municipal Register
              </Badge>
            </div>
          </div>

          {/* Editorial Headline & Mission with Entrance Fade */}
          <div className="max-w-4xl mx-auto text-center space-y-4 mb-8 animate-editorial-fade">
            <h1 className="font-heading font-medium tracking-tight text-4xl sm:text-5xl lg:text-6xl text-foreground leading-[1.08]">
              The Mangatarem Field Guide & Cultural Cartography
            </h1>
            <p className="font-sans text-base sm:text-lg text-muted-foreground max-w-3xl mx-auto leading-relaxed">
              A sunlit municipal archive and geospatial gateway. Orient yourself across 82 barangays, trace the
              centuries-old Spanish brickwork of San Raymundo de Peñafort, and explore the protected rainforest
              canopy of Manleluag Spring along the scenic mountain corridors of Daang Kalikasan.
            </p>
          </div>

          {/* Immediate Traveler Search Utility with Staggered Entrance */}
          <div className="max-w-2xl mx-auto mb-10 animate-editorial-delay-1">
            <HeroSearch />
          </div>

          {/* Orientation-First Dual Gateway Cards with Hover & Staggered Animations */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 max-w-5xl mx-auto animate-editorial-delay-2">
            {/* Gateway 1: Geospatial Interactive Map */}
            <Link
              href="/map"
              className="group block focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary rounded-2xl transition-all duration-300 ease-out hover:-translate-y-1.5 active:scale-[0.98]"
            >
              <Card className="h-full bg-card/95 border-[0.5px] border-primary/30 hover:border-primary/70 transition-all duration-300 shadow-sm hover:shadow-xl hover:shadow-primary/5 p-6 relative overflow-hidden">
                <div className="flex items-start justify-between gap-4">
                  <div className="space-y-3 flex-1">
                    <div className="flex items-center gap-2">
                      <span className="px-2.5 py-0.5 rounded-sm bg-primary/10 text-primary text-xs font-mono font-medium">
                        SECTOR 01 • GEOSPATIAL
                      </span>
                      <span className="text-xs font-mono text-muted-foreground">GIS v1.2</span>
                    </div>
                    <h2 className="font-heading font-medium text-2xl text-foreground group-hover:text-primary transition-colors duration-200">
                      Interactive Cultural Map
                    </h2>
                    <p className="font-sans text-sm text-muted-foreground leading-relaxed">
                      Survey 82 barangays with GPS coordinates, elevation profiles, and verified municipal boundary routes.
                    </p>
                    <div className="flex flex-wrap gap-2 pt-2">
                      <Badge variant="outline" className="font-sans text-xs border-primary/40 text-foreground bg-primary/5 group-hover:border-primary/60 transition-colors">
                        82 Verified Barangays
                      </Badge>
                      <Badge variant="outline" className="font-sans text-xs border-primary/40 text-foreground bg-primary/5 group-hover:border-primary/60 transition-colors">
                        15 Cultural Sites
                      </Badge>
                      <Badge variant="outline" className="font-sans text-xs border-[oklch(0.45_0.12_240)]/40 text-foreground bg-[oklch(0.45_0.12_240)]/5">
                        8 Natural Sanctuaries
                      </Badge>
                    </div>
                  </div>
                  <div className="hidden sm:flex h-13 w-13 shrink-0 items-center justify-center rounded-xl bg-primary text-primary-foreground shadow-md shadow-primary/20 group-hover:scale-110 group-hover:-rotate-6 transition-all duration-300 ease-out">
                    <Navigation className="h-6 w-6" />
                  </div>
                </div>
                <div className="mt-5 pt-3 border-t border-border/70 flex items-center justify-between text-xs font-sans font-medium text-primary">
                  <span>Open Interactive Map Canvas</span>
                  <ArrowRight className="h-4 w-4 group-hover:translate-x-1.5 transition-transform duration-200" />
                </div>
              </Card>
            </Link>

            {/* Gateway 2: Curated Cultural Archives */}
            <div className="group rounded-2xl border-[0.5px] border-accent/40 bg-card/95 p-6 shadow-sm hover:border-accent/80 transition-all duration-300 flex flex-col justify-between hover:shadow-xl hover:shadow-accent/5 hover:-translate-y-1.5">
              <div className="space-y-3">
                <div className="flex items-center justify-between">
                  <span className="px-2.5 py-0.5 rounded-sm bg-accent/10 text-accent text-xs font-mono font-medium">
                    SECTOR 02 • ARCHIVES
                  </span>
                  <span className="text-[11px] font-mono text-muted-foreground">RA 10066 Registered</span>
                </div>
                <h2 className="font-heading font-medium text-2xl text-foreground group-hover:text-accent transition-colors duration-200">
                  Living Traditions & Heritage
                </h2>
                <p className="font-sans text-sm text-muted-foreground leading-relaxed">
                  Study municipal cultural properties cataloged under the National Cultural Heritage Act registry.
                </p>
                <div className="flex flex-wrap gap-2 pt-2">
                  <Link href="/heritage?type=built-heritage">
                    <Badge variant="secondary" className="font-sans text-xs hover:bg-accent hover:text-accent-foreground transition-all duration-200 cursor-pointer border border-border/60 hover:scale-105">
                      Built Heritage (1827–Present)
                    </Badge>
                  </Link>
                  <Link href="/heritage?type=natural-heritage">
                    <Badge variant="secondary" className="font-sans text-xs hover:bg-accent hover:text-accent-foreground transition-all duration-200 cursor-pointer border border-border/60 hover:scale-105">
                      Natural Landscapes
                    </Badge>
                  </Link>
                  <Link href="/heritage?type=intangible-heritage">
                    <Badge variant="secondary" className="font-sans text-xs hover:bg-accent hover:text-accent-foreground transition-all duration-200 cursor-pointer border border-border/60 hover:scale-105">
                      Living Traditions
                    </Badge>
                  </Link>
                </div>
              </div>
              <div className="mt-5 pt-3 border-t border-border/70 flex items-center justify-between">
                <Link
                  href="/heritage"
                  className="text-xs font-sans font-medium text-accent hover:underline inline-flex items-center gap-1.5"
                >
                  Browse Full Heritage Registry <ArrowRight className="h-4 w-4 group-hover:translate-x-1.5 transition-transform duration-200" />
                </Link>
                <span className="text-[11px] font-mono text-muted-foreground">Historical Dossiers</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* ── SECTION 2: Neo-Geo Field Almanac & Category Matrix ── */}
      <section className="container mx-auto px-4 py-12 max-w-6xl">
        <div className="flex items-center justify-between mb-6 pb-2 border-b-[0.5px] border-border/80">
          <div>
            <h2 className="font-heading font-medium text-2xl text-foreground">Municipal Sector Matrix</h2>
            <p className="font-sans text-xs text-muted-foreground">Primary exploration domains across the 82 territorial barangays</p>
          </div>
          <span className="font-mono text-xs text-muted-foreground hidden sm:inline">GRID 04-DIV</span>
        </div>

        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
          {[
            {
              href: "/attractions",
              icon: MapPin,
              code: "SEC-01",
              title: "Natural Sanctuaries",
              desc: "Manleluag Hot Springs & Mountain Corridors",
              tag: "8 Sites",
            },
            {
              href: "/heritage",
              icon: Landmark,
              code: "SEC-02",
              title: "Historic Monuments",
              desc: "Spanish brick masonry & centuries-old plazas",
              tag: "15 Registered",
            },
            {
              href: "/events",
              icon: Calendar,
              code: "SEC-03",
              title: "Fiestas & Fairs",
              desc: "Mango harvests, eco-treks & patronal days",
              tag: "Seasonal",
            },
            {
              href: "/business",
              icon: Building2,
              code: "SEC-04",
              title: "Local Sustenance",
              desc: "Pangasinan tupig, mango stalls & homestays",
              tag: "Verified",
            },
          ].map(({ href, icon: Icon, code, title, desc, tag }) => (
            <Link key={href} href={href} className="group focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary rounded-xl transition-all duration-200 hover:-translate-y-1.5 active:scale-[0.98]">
              <Card className="bg-card border-[0.5px] border-border/90 p-5 h-full flex flex-col justify-between hover:border-primary/50 hover:shadow-lg transition-all duration-200">
                <div className="space-y-3">
                  <div className="flex items-center justify-between">
                    <span className="text-[10px] font-mono text-muted-foreground">{code}</span>
                    <Badge variant="outline" className="text-[10px] font-mono border-border/80 text-muted-foreground">
                      {tag}
                    </Badge>
                  </div>
                  <div className="h-10 w-10 rounded-lg bg-primary/10 text-primary flex items-center justify-center group-hover:scale-110 group-hover:bg-primary group-hover:text-primary-foreground group-hover:shadow-md group-hover:shadow-primary/20 transition-all duration-300 ease-out">
                    <Icon className="h-5 w-5" />
                  </div>
                  <div>
                    <h3 className="font-heading font-medium text-lg text-foreground group-hover:text-primary transition-colors duration-200">
                      {title}
                    </h3>
                    <p className="font-sans text-xs text-muted-foreground mt-1 leading-relaxed">
                      {desc}
                    </p>
                  </div>
                </div>
                <div className="pt-3 mt-3 border-t border-border/60 flex items-center justify-between text-[11px] font-sans font-medium text-primary">
                  <span>Explore Sector</span>
                  <ArrowRight className="h-3.5 w-3.5 group-hover:translate-x-1 transition-transform duration-200" />
                </div>
              </Card>
            </Link>
          ))}
        </div>
      </section>

      {/* ── SECTION 3: Deep Heritage Chronicles (Spanish Masonry & Rainforest Canopy) ── */}
      <section className="bg-muted/30 border-y-[0.5px] border-border/80 py-16">
        <div className="container mx-auto px-4 max-w-6xl">
          <div className="text-center max-w-2xl mx-auto mb-12">
            <span className="font-mono text-xs text-primary uppercase tracking-wider">Historical Field Records</span>
            <h2 className="font-heading font-medium text-3xl sm:text-4xl text-foreground mt-1">
              Chronicles of Brick, Canopy & Water
            </h2>
            <p className="font-sans text-sm sm:text-base text-muted-foreground mt-2 leading-relaxed">
              Mangatarem’s character was forged where the fertile Agno River floodplains meet the rugged Zambales mountain range.
            </p>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            {/* Story A: San Raymundo de Peñafort */}
            <div className="group bg-card rounded-2xl border-[0.5px] border-border/90 overflow-hidden shadow-sm hover:shadow-xl hover:border-accent/50 hover:-translate-y-1.5 transition-all duration-300 ease-out flex flex-col justify-between">
              <div>
                <div className="relative aspect-[16/10] overflow-hidden bg-muted">
                  <Image
                    src="/img/st_raymund_church.webp"
                    alt="San Raymundo de Peñafort Parish Church Spanish Brick Masonry"
                    fill
                    sizes="(max-width: 1024px) 100vw, 50vw"
                    className="object-cover group-hover:scale-105 transition-transform duration-700 ease-out"
                  />
                  <div className="absolute bottom-3 left-3 bg-background/95 backdrop-blur-md px-3 py-1 rounded text-xs font-mono border border-border/60 text-foreground transition-all duration-200 group-hover:border-accent/40">
                    15.7911° N, 120.2939° E • Poblacion Central
                  </div>
                </div>
                <div className="p-6 space-y-3">
                  <div className="flex items-center gap-2">
                    <Badge variant="outline" className="text-xs font-sans text-accent border-accent/40 bg-accent/5 transition-transform duration-200 group-hover:scale-105">
                      Terracotta Masonry • Circa 1835–1882
                    </Badge>
                  </div>
                  <h3 className="font-heading font-medium text-2xl text-foreground group-hover:text-accent transition-colors duration-200">
                    The Colonial Brickwork of San Raymundo de Peñafort
                  </h3>
                  <p className="font-sans text-sm text-muted-foreground leading-relaxed">
                    Constructed under the supervision of Dominican friars starting in 1835, the church stands as one of the
                    finest examples of hand-fired terracotta masonry in western Pangasinan. Built with thick brick buttresses and
                    hand-hewn molave timber trusses, it has weathered earthquakes, typhoons, and centuries of municipal history.
                  </p>
                </div>
              </div>
              <div className="p-6 pt-0">
                <Link href="/heritage?type=built-heritage">
                  <Button variant="outline" className="w-full gap-2 rounded-xl border-accent/40 text-accent hover:bg-accent hover:text-accent-foreground font-sans text-xs transition-all duration-200">
                    <BookOpen className="h-4 w-4" /> Study Architectural Dossier
                  </Button>
                </Link>
              </div>
            </div>

            {/* Story B: Manleluag Spring & Daang Kalikasan */}
            <div className="group bg-card rounded-2xl border-[0.5px] border-border/90 overflow-hidden shadow-sm hover:shadow-xl hover:border-[oklch(0.45_0.12_240)]/50 hover:-translate-y-1.5 transition-all duration-300 ease-out flex flex-col justify-between">
              <div>
                <div className="relative aspect-[16/10] overflow-hidden bg-muted">
                  <Image
                    src="/img/manleluag_spring.webp"
                    alt="Manleluag Spring Protected Landscape Rainforest Canopy"
                    fill
                    sizes="(max-width: 1024px) 100vw, 50vw"
                    className="object-cover group-hover:scale-105 transition-transform duration-700 ease-out"
                  />
                  <div className="absolute bottom-3 left-3 bg-background/95 backdrop-blur-md px-3 py-1 rounded text-xs font-mono border border-border/60 text-foreground transition-all duration-200 group-hover:border-[oklch(0.45_0.12_240)]/40">
                    15.7061° N, 120.2811° E • Malabobo Sector
                  </div>
                </div>
                <div className="p-6 space-y-3">
                  <div className="flex items-center gap-2">
                    <Badge variant="outline" className="text-xs font-sans text-[oklch(0.45_0.12_240)] border-[oklch(0.45_0.12_240)]/40 bg-[oklch(0.45_0.12_240)]/5 transition-transform duration-200 group-hover:scale-105">
                      Protected Landscape • Thermal Sulfuric Spring
                    </Badge>
                  </div>
                  <h3 className="font-heading font-medium text-2xl text-foreground group-hover:text-[oklch(0.45_0.12_240)] transition-colors duration-200">
                    Manleluag Protected Canopy & Mountain Ridges
                  </h3>
                  <p className="font-sans text-sm text-muted-foreground leading-relaxed">
                    Nestled in 1,065 hectares of virgin dipterocarp rainforest, Manleluag Spring Protected Landscape is a vital
                    biodiversity sanctuary. Natural warm mineral springs emerge from geothermal fissures beneath the mountain,
                    while the high-altitude Daang Kalikasan corridor winds along the ridgeline offering panoramic views.
                  </p>
                </div>
              </div>
              <div className="p-6 pt-0">
                <Link href="/attractions">
                  <Button variant="outline" className="w-full gap-2 rounded-xl border-[oklch(0.45_0.12_240)]/40 text-[oklch(0.45_0.12_240)] hover:bg-[oklch(0.45_0.12_240)] hover:text-white font-sans text-xs transition-all duration-200">
                    <MapPin className="h-4 w-4" /> View Protected Sanctuary Routes
                  </Button>
                </Link>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* ── SECTION 4: Featured Attractions & Field Register ── */}
      {attractions.length > 0 && (
        <section className="container mx-auto px-4 py-16 max-w-6xl">
          <div className="flex flex-col sm:flex-row sm:items-end justify-between mb-8 gap-4 pb-2 border-b-[0.5px] border-border/80">
            <div>
              <span className="font-mono text-xs text-primary uppercase">Curated Catalog</span>
              <h2 className="font-heading font-medium text-3xl text-foreground">Featured Field Attractions</h2>
              <p className="font-sans text-xs sm:text-sm text-muted-foreground mt-1">
                Verified eco-tourism destinations, mountain passes, and cultural landmarks
              </p>
            </div>
            <Link
              href="/attractions"
              className="font-sans text-xs sm:text-sm text-primary hover:underline inline-flex items-center gap-1 font-medium group"
            >
              Inspect Complete Directory ({attractions.length}+){" "}
              <ArrowRight className="h-4 w-4 group-hover:translate-x-1 transition-transform duration-200" />
            </Link>
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {attractions.map((a) => (
              <AttractionCard key={a.id} item={a} />
            ))}
          </div>
        </section>
      )}

      {/* ── SECTION 5: Seasonal Almanac & Field Events ── */}
      {events.length > 0 && (
        <section className="bg-muted/20 border-t-[0.5px] border-border/80 py-16">
          <div className="container mx-auto px-4 max-w-6xl">
            <div className="flex flex-col sm:flex-row sm:items-end justify-between mb-8 gap-4 pb-2 border-b-[0.5px] border-border/80">
              <div>
                <span className="font-mono text-xs text-primary uppercase">Calendar of Events</span>
                <h2 className="font-heading font-medium text-3xl text-foreground">Municipal Almanac & Fiestas</h2>
                <p className="font-sans text-xs sm:text-sm text-muted-foreground mt-1">
                  Agri-tourism fairs, patronal celebrations, and guided eco-tours
                </p>
              </div>
              <Link
                href="/events"
                className="font-sans text-xs sm:text-sm text-primary hover:underline inline-flex items-center gap-1 font-medium group"
              >
                View Full Event Schedule{" "}
                <ArrowRight className="h-4 w-4 group-hover:translate-x-1 transition-transform duration-200" />
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

      {/* ── SECTION 6: Static Ecosystem Teasers (Zero-JS SSR, Lightweight Navigation) ── */}
      <section className="container mx-auto px-4 py-16 max-w-6xl">
        <div className="text-center max-w-2xl mx-auto mb-10">
          <span className="font-mono text-xs text-primary uppercase tracking-wider">Connected Systems</span>
          <h2 className="font-heading font-medium text-3xl text-foreground mt-1">
            Tools for the Field Explorer
          </h2>
          <p className="font-sans text-sm text-muted-foreground mt-2 leading-relaxed">
            Navigate routes, consult fellow travelers, and collect municipal verification stamps as you explore.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {/* Card 1: Geospatial Smart Routes */}
          <Link
            href="/map"
            className="group block focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary rounded-xl transition-all duration-200 hover:-translate-y-1.5 active:scale-[0.98]"
          >
            <Card className="h-full bg-card border-[0.5px] border-border/90 p-6 flex flex-col justify-between hover:border-primary/60 hover:shadow-lg transition-all duration-200">
              <div className="space-y-3">
                <div className="flex items-center justify-between">
                  <span className="h-9 w-9 rounded-lg bg-primary/10 text-primary flex items-center justify-center group-hover:scale-110 group-hover:rotate-3 transition-transform duration-300">
                    <Route className="h-5 w-5" />
                  </span>
                  <Badge variant="outline" className="text-[10px] font-mono border-primary/30 text-primary">
                    Geospatial
                  </Badge>
                </div>
                <h3 className="font-heading font-medium text-xl text-foreground group-hover:text-primary transition-colors duration-200">
                  Corridor & Ridge Routes
                </h3>
                <p className="font-sans text-xs sm:text-sm text-muted-foreground leading-relaxed">
                  Turn-by-turn coordinate navigation, elevation gradients, and cycling corridors through Daang Kalikasan and outer barangays.
                </p>
              </div>
              <div className="pt-4 mt-4 border-t border-border/60 flex items-center justify-between text-xs font-sans font-medium text-primary">
                <span>Launch Route Navigator</span>
                <ArrowRight className="h-4 w-4 group-hover:translate-x-1.5 transition-transform duration-200" />
              </div>
            </Card>
          </Link>

          {/* Card 2: Community Field Notes */}
          <Link
            href="/chat"
            className="group block focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary rounded-xl transition-all duration-200 hover:-translate-y-1.5 active:scale-[0.98]"
          >
            <Card className="h-full bg-card border-[0.5px] border-border/90 p-6 flex flex-col justify-between hover:border-primary/60 hover:shadow-lg transition-all duration-200">
              <div className="space-y-3">
                <div className="flex items-center justify-between">
                  <span className="h-9 w-9 rounded-lg bg-accent/10 text-accent flex items-center justify-center group-hover:scale-110 group-hover:rotate-3 transition-transform duration-300">
                    <MessageSquare className="h-5 w-5" />
                  </span>
                  <Badge variant="outline" className="text-[10px] font-mono border-accent/30 text-accent">
                    Discussions
                  </Badge>
                </div>
                <h3 className="font-heading font-medium text-xl text-foreground group-hover:text-accent transition-colors duration-200">
                  Traveler Field Notes
                </h3>
                <p className="font-sans text-xs sm:text-sm text-muted-foreground leading-relaxed">
                  Direct dispatches from locals and visitors: road conditions, mango harvest schedules, and dining recommendations.
                </p>
              </div>
              <div className="pt-4 mt-4 border-t border-border/60 flex items-center justify-between text-xs font-sans font-medium text-accent">
                <span>Open Community Channels</span>
                <ArrowRight className="h-4 w-4 group-hover:translate-x-1.5 transition-transform duration-200" />
              </div>
            </Card>
          </Link>

          {/* Card 3: Cultural Passport */}
          <Link
            href="/passport"
            className="group block focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary rounded-xl transition-all duration-200 hover:-translate-y-1.5 active:scale-[0.98]"
          >
            <Card className="h-full bg-card border-[0.5px] border-border/90 p-6 flex flex-col justify-between hover:border-[oklch(0.75_0.15_75)]/60 hover:shadow-lg transition-all duration-200">
              <div className="space-y-3">
                <div className="flex items-center justify-between">
                  <span className="h-9 w-9 rounded-lg bg-[oklch(0.75_0.15_75)]/15 text-[oklch(0.75_0.15_75)] flex items-center justify-center group-hover:scale-110 group-hover:rotate-3 transition-transform duration-300">
                    <Award className="h-5 w-5" />
                  </span>
                  <Badge variant="outline" className="text-[10px] font-mono border-[oklch(0.75_0.15_75)]/40 text-[oklch(0.75_0.15_75)]">
                    Stamp Ledger
                  </Badge>
                </div>
                <h3 className="font-heading font-medium text-xl text-foreground group-hover:text-primary transition-colors duration-200">
                  Heritage Passport
                </h3>
                <p className="font-sans text-xs sm:text-sm text-muted-foreground leading-relaxed">
                  Check in at historical sites, collect verified digital municipal stamps, and earn tourism badges across all 82 barangays.
                </p>
              </div>
              <div className="pt-4 mt-4 border-t border-border/60 flex items-center justify-between text-xs font-sans font-medium text-[oklch(0.75_0.15_75)]">
                <span>View Stamp Register</span>
                <ArrowRight className="h-4 w-4 group-hover:translate-x-1.5 transition-transform duration-200" />
              </div>
            </Card>
          </Link>
        </div>
      </section>

      {/* ── SECTION 7: Township Dispatch & Field Guide Call-to-Action ── */}
      <section className="container mx-auto px-4 py-16 max-w-6xl">
        <div className="rounded-3xl bg-card border-[0.5px] border-border/90 p-8 sm:p-12 shadow-sm relative overflow-hidden transition-all duration-300 hover:shadow-md">
          <div className="max-w-2xl mx-auto text-center space-y-4">
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-primary/10 text-primary text-xs font-mono font-medium">
              <Bell className="h-3.5 w-3.5" /> MUNICIPAL DISPATCH SERVICE
            </div>
            <h2 className="font-heading font-medium text-3xl sm:text-4xl text-foreground">
              Subscribe to Mangatarem Heritage Bulletins
            </h2>
            <p className="font-sans text-sm sm:text-base text-muted-foreground leading-relaxed">
              Receive official notices regarding Manleluag protected landscape access, festival dates, municipal historical research, and tourism advisories.
            </p>
            <div className="pt-2">
              <NewsletterSubscribe />
            </div>
          </div>
        </div>

        {/* Closing Cartographic Stamp & Direct Call to Explore */}
        <div className="mt-12 text-center border-t-[0.5px] border-border/80 pt-10">
          <div className="inline-flex items-center justify-center p-3 rounded-full bg-primary/5 text-primary mb-3 transition-transform duration-500 hover:rotate-45">
            <Compass className="h-6 w-6 stroke-[1.5]" />
          </div>
          <h3 className="font-heading font-medium text-2xl text-foreground">
            Begin Your Field Survey of Mangatarem
          </h3>
          <p className="font-sans text-xs sm:text-sm text-muted-foreground max-w-md mx-auto mt-1 mb-6">
            Access the interactive GIS map with all 82 barangay boundaries and cultural POIs.
          </p>
          <div className="flex flex-wrap justify-center gap-3">
            <Link href="/map">
              <Button size="lg" className="rounded-xl px-6 font-sans text-xs sm:text-sm shadow-sm gap-2 transition-all duration-200 hover:-translate-y-0.5 active:scale-95">
                <MapPin className="h-4 w-4" /> Open Full Interactive Map
              </Button>
            </Link>
            <Link href="/heritage">
              <Button size="lg" variant="outline" className="rounded-xl px-6 font-sans text-xs sm:text-sm border-border/90 gap-2 transition-all duration-200 hover:-translate-y-0.5 active:scale-95">
                <BookOpen className="h-4 w-4" /> Read Heritage Archives
              </Button>
            </Link>
          </div>
          <p className="font-mono text-[11px] text-muted-foreground/60 mt-6">
            Mangatarem Local Tourism & Cultural Mapping System • Coordinates 15.7911° N, 120.2939° E
          </p>
        </div>
      </section>
    </div>
  );
}
