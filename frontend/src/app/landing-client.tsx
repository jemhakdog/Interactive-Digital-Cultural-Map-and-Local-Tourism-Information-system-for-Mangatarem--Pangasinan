"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import { useAuth } from "@/lib/auth";
import {
  Compass,
  MapPin,
  Calendar,
  Sparkles,
  Mountain,
  TreePine,
  ShieldCheck,
  Eye,
  Camera,
  ArrowRight,
  ChevronLeft,
  ChevronRight,
  BarChart2,
  FileText,
  Users,
  TrendingUp,
  User,
  Map,
  Landmark,
  Building2,
  Church,
  Search,
  Star,
  Layers,
  ArrowUpRight
} from "lucide-react";
import { NewsletterSubscribe } from "@/components/public/newsletter-subscribe";
import { resolvePlaceImage } from "@/components/map/data";

export interface AttractionItem {
  id: number;
  name: string;
  category?: string;
  image_url?: string;
  barangay_name?: string;
  average_rating?: number;
}

export interface EventItem {
  id: number;
  name: string;
  category?: string;
  date?: string;
  image_url?: string;
  barangay_name?: string;
}

interface LandingClientProps {
  attractions: AttractionItem[];
  events: EventItem[];
}

// Ecosystem Satellite Nodes with radiant coordinates and distinct delay for refresh entry
const satellites = [
  {
    id: "nature",
    icon: TreePine,
    label: "Eco-Tourism",
    color: "bg-emerald-500/15 text-emerald-700 dark:text-emerald-400",
    ring: "border-emerald-500/30",
    leftPct: 22,
    topPct: 18,
    delay: 150,
    href: "/attractions?category=Nature",
  },
  {
    id: "festivals",
    icon: ShieldCheck,
    label: "Cultural Pride",
    color: "bg-primary/20 text-primary",
    ring: "border-primary/40",
    leftPct: 78,
    topPct: 18,
    delay: 250,
    href: "/events",
  },
  {
    id: "heritage",
    icon: Landmark,
    label: "Heritage Sites",
    color: "bg-amber-500/15 text-amber-700 dark:text-amber-400",
    ring: "border-amber-500/30",
    leftPct: 10,
    topPct: 50,
    delay: 350,
    href: "/heritage",
  },
  {
    id: "map-node",
    icon: Eye,
    label: "GIS Cultural Map",
    color: "bg-card text-foreground border border-border",
    ring: "border-border",
    leftPct: 90,
    topPct: 50,
    delay: 450,
    href: "/map",
  },
  {
    id: "photo1",
    img: "/img/manleluag_spring.webp",
    label: "Manleluag Hot Spring",
    color: "bg-primary/10",
    ring: "border-primary/30",
    leftPct: 24,
    topPct: 82,
    delay: 550,
    href: "/attractions",
  },
  {
    id: "photo2",
    img: "/img/daang_kalikasan.webp",
    label: "Daang Kalikasan",
    color: "bg-primary/10",
    ring: "border-primary/30",
    leftPct: 76,
    topPct: 82,
    delay: 650,
    href: "/attractions",
  },
];

// Floating Staggered Cards (Left & Right Flanks)
const galleryLeft = [
  {
    id: "gl-1",
    name: "Manleluag Hot Spring",
    category: "Protected Landscape",
    img: "/img/manleluag_spring.webp",
    speed: 0.6,
    blur: "backdrop-blur-none",
    margin: "mt-0 sm:mt-4 ml-0",
  },
  {
    id: "gl-2",
    name: "Saint Raymund Parish",
    category: "18th-Century Baroque",
    img: "/img/st_raymund_church.webp",
    speed: 1.2,
    blur: "blur-[0.5px] opacity-90",
    margin: "mt-8 sm:mt-16 ml-4 sm:ml-12",
  },
  {
    id: "gl-3",
    name: "Canding Falls",
    category: "Natural Eco Cascade",
    img: "/img/attractions/canding_falls/image_1.jpg",
    speed: 0.8,
    blur: "backdrop-blur-none",
    margin: "mt-6 sm:mt-12 -ml-2 sm:ml-2",
  },
  {
    id: "gl-4",
    name: "Ventenilla Residence",
    category: "Ancestral Heritage",
    img: "/img/attractions/don_ramon_ventenilla_residence/image_1.jpg",
    speed: 1.4,
    blur: "blur-[0.8px] opacity-80",
    margin: "mt-10 sm:mt-20 ml-6 sm:ml-16",
  },
];

const galleryRight = [
  {
    id: "gr-1",
    name: "Daang Kalikasan",
    category: "Scenic Mountain Ridgeline",
    img: "/img/daang_kalikasan.webp",
    speed: 0.7,
    blur: "backdrop-blur-none",
    margin: "mt-2 sm:mt-6 mr-0",
  },
  {
    id: "gr-2",
    name: "Timmanguyob Falls",
    category: "Pristine Highland Springs",
    img: "/img/attractions/timmanguyob_falls/image_1.jpg",
    speed: 1.3,
    blur: "blur-[0.6px] opacity-85",
    margin: "mt-6 sm:mt-14 mr-4 sm:mr-10",
  },
  {
    id: "gr-3",
    name: "Pacalat River Escapes",
    category: "Riverine Eco Spot",
    img: "/img/attractions/pacalat_river/image_1.jpg",
    speed: 0.9,
    blur: "backdrop-blur-none",
    margin: "mt-8 sm:mt-12 -mr-2 sm:mr-4",
  },
  {
    id: "gr-4",
    name: "Corleto Ancestral Estate",
    category: "Spanish Era Architecture",
    img: "/img/attractions/corleto_residence/image_1.jpg",
    speed: 1.5,
    blur: "blur-[0.8px] opacity-75",
    margin: "mt-10 sm:mt-20 mr-6 sm:mr-14",
  },
];

const rotatingTextPills = [
  "Access Real-Time Tourism Insights",
  "Explore 82 Barangays Digitally",
  "Preserve Pangasinan Cultural Treasures",
];

// 3D Arched Tool/Module Integrations
const tourismModules = [
  {
    id: "gis-map",
    name: "Interactive GIS Map",
    summary: "Geospatial vector mapping, elevation layers, and GPS-guided trail coordinates for travelers.",
    brandBg: "bg-primary/10 text-primary border-primary/20",
    icon: Map,
    href: "/map",
  },
  {
    id: "heritage-vault",
    name: "Cultural Registry",
    summary: "Historical documentation, oral histories, and verified cultural properties catalogued across towns.",
    brandBg: "bg-amber-500/10 text-amber-700 dark:text-amber-300 border-amber-500/20",
    icon: Landmark,
    href: "/heritage",
  },
  {
    id: "attractions-hub",
    name: "Eco Destinations",
    summary: "Curated national parks, scenic ridges, and natural spring resorts complete with visit guides.",
    brandBg: "bg-primary/10 text-primary border-primary/20",
    icon: Mountain,
    href: "/attractions",
  },
  {
    id: "festivals-hub",
    name: "Community Events",
    summary: "Annual Mango Festival schedules, barangay patronal fiestas, and local cultural celebrations.",
    brandBg: "bg-destructive/10 text-destructive border-destructive/20",
    icon: Calendar,
    href: "/events",
  },
  {
    id: "business-hub",
    name: "Local Enterprises",
    summary: "Verified homestays, native Pangasinan delicacies, agrarian markets, and artisan shops.",
    brandBg: "bg-secondary text-secondary-foreground border-border",
    icon: Building2,
    href: "/business",
  },
];

// Exact integer-px positions for each wheel offset (0=center, ±1, ±2).
// Precomputed from the 42° spacing & radii, rounded once, so server and
// client emit byte-identical inline styles (float-trig strings would
// round differently and break hydration). Keys 0-4 = offsets -2..+2.
const WHEEL_OFFSETS = [
  { x: -388, y: 62, tilt: -44, scale: 0.82, opacity: 0.44, z: 19 },
  { x: -261, y: -78, tilt: -22, scale: 0.9, opacity: 0.72, z: 22 },
  { x: 0, y: -135, tilt: 0, scale: 1.15, opacity: 1, z: 25 },
  { x: 261, y: -78, tilt: 22, scale: 0.9, opacity: 0.72, z: 22 },
  { x: 388, y: 62, tilt: 44, scale: 0.82, opacity: 0.44, z: 19 },
];

// Testimonials / Words of Appreciation
const visitorTestimonials = [
  {
    id: "t1",
    name: "Maria Teresa Santos",
    title: "Cultural Heritage Researcher, Pangasinan State Univ.",
    rating: "5.0",
    avatar: "https://images.unsplash.com/photo-1544005313-94ddf0286df2?w=200&auto=format&fit=crop&q=80",
    quote:
      "The Interactive Digital Cultural Map is an extraordinary breakthrough for Pangasinan. It preserves historical ancestral homes and natural treasures with meticulous geospatial accuracy.",
  },
  {
    id: "t2",
    name: "Engr. Rafael Mendoza",
    title: "Adventure Tourist & Eco-Cyclist",
    rating: "5.0",
    avatar: "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=200&auto=format&fit=crop&q=80",
    quote:
      "Navigating from Daang Kalikasan to Manleluag Hot Springs was effortless using the live GIS routing. The digital information system makes discovering hidden gems seamless.",
  },
  {
    id: "t3",
    name: "Beatriz Villanueva",
    title: "Mangatarem Hospitality & MSME Association Lead",
    rating: "5.0",
    avatar: "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=200&auto=format&fit=crop&q=80",
    quote:
      "Our community businesses, agri-tourism hubs, and local weavers now receive direct recognition from eco-travelers across Luzon. It truly elevates our hometown.",
  },
];

export function LandingClient({ attractions, events }: LandingClientProps) {
  const { user } = useAuth();
  const [scrollY, setScrollY] = useState(0);
  const [mounted, setMounted] = useState(false);
  const [reportView, setReportView] = useState<"daily" | "monthly">("daily");
  const [activePillIndex, setActivePillIndex] = useState(0);
  const [isWheelPaused, setIsWheelPaused] = useState(false);
  const [activeTestimonial, setActiveTestimonial] = useState(0);
  const [wheelElapsed, setWheelElapsed] = useState(0); // ticks since mount; SSR never fires wheel changes

  useEffect(() => {
    setMounted(true);
    const handleScroll = () => {
      setScrollY(window.scrollY);
    };
    window.addEventListener("scroll", handleScroll, { passive: true });
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  useEffect(() => {
    const timer = setInterval(() => {
      setActivePillIndex((prev) => (prev + 1) % rotatingTextPills.length);
    }, 2800);
    return () => clearInterval(timer);
  }, []);

  // Auto-rotating wheel effect (like a revolving carousel). The rotation is
  // derived from a tick counter that only ever advances in effects, so the
  // server-rendered (hydrated) markup stays identical to first client paint.
  // The interval is suspended until the post-hydration mount render so the
  // first client render (compared against server HTML) can never see a tick.
  useEffect(() => {
    if (!mounted || isWheelPaused) return;
    const interval = setInterval(() => {
      setWheelElapsed((t) => t + 1);
    }, 3200);
    return () => clearInterval(interval);
  }, [isWheelPaused, mounted]);

  const activeModule = wheelElapsed % tourismModules.length;

  const hero1Prog = Math.min(1, Math.max(0, scrollY / 450));
  const hubTranslationY = -hero1Prog * 80;
  const hubOpacity = 1 - hero1Prog * 0.45;
  const satelliteSpread = 1 + hero1Prog * 1.6;
  const satelliteOpacity = Math.max(0, 1 - hero1Prog * 1.8);

  const prevTestimonial = () => {
    setActiveTestimonial((prev) => (prev === 0 ? visitorTestimonials.length - 1 : prev - 1));
  };
  const nextTestimonial = () => {
    setActiveTestimonial((prev) => (prev + 1) % visitorTestimonials.length);
  };

  return (
    <div className="min-h-screen bg-background text-foreground font-sans antialiased overflow-x-hidden selection:bg-primary selection:text-primary-foreground">
      {/* Floating Pill Navigation Bar with entrance animation */}
      <header
        className={
          "fixed top-5 left-0 right-0 z-50 flex justify-center px-4 pointer-events-none transition-all duration-700 ease-out " +
          (mounted ? "translate-y-0 opacity-100" : "-translate-y-8 opacity-0")
        }
      >
        <nav className="pointer-events-auto flex items-center justify-between gap-4 md:gap-8 px-6 py-2.5 bg-background/80 backdrop-blur-xl border border-border shadow-lg shadow-primary/5 rounded-full max-w-5xl w-full transition-all duration-300 hover:bg-background/95 hover:border-primary/40">
          {/* Brand Logo */}
          <Link href="/" className="flex items-center gap-2.5 group shrink-0">
            <div className="w-8 h-8 rounded-xl bg-primary flex items-center justify-center text-primary-foreground shadow-sm transition-transform group-hover:scale-105">
              <Compass className="w-4.5 h-4.5" />
            </div>
            <span className="font-bold text-base md:text-lg tracking-tight text-foreground whitespace-nowrap">
              Mangatarem<span className="text-primary">Tourism</span>
            </span>
          </Link>

          {/* Clean One-Line Nav Links */}
          <div className="hidden lg:flex items-center gap-5 xl:gap-7 text-sm font-medium text-muted-foreground whitespace-nowrap">
            <Link href="/attractions" className="hover:text-foreground transition-colors">
              Attractions
            </Link>
            <Link href="/map" className="hover:text-foreground transition-colors">
              Map
            </Link>
            <Link href="/events" className="hover:text-foreground transition-colors">
              Events
            </Link>
            <Link href="/heritage" className="hover:text-foreground transition-colors">
              Heritage
            </Link>
            <Link href="/business" className="hover:text-foreground transition-colors">
              Business
            </Link>
          </div>

          {/* Right side: auth actions (login-aware) */}
          <div className="flex items-center gap-2 sm:gap-3 shrink-0">
            {user ? (
              <Link
                href={
                  user.role === "admin"
                    ? "/admin"
                    : user.role === "business_owner"
                    ? "/business/dashboard"
                    : user.role === "contributor"
                    ? "/contributor/dashboard"
                    : "/dashboard"
                }
                className="inline-flex items-center justify-center gap-2 h-9 px-3.5 text-xs md:text-sm font-medium text-foreground rounded-full hover:bg-muted/50 transition-colors whitespace-nowrap"
              >
                <span className="flex h-5 w-5 items-center justify-center rounded-full bg-primary/10 text-primary">
                  <User className="h-3 w-3" />
                </span>
                {user.name}
              </Link>
            ) : (
              <>
                <Link
                  href="/auth/login"
                  className="inline-flex items-center justify-center h-9 px-3.5 text-xs md:text-sm font-medium text-muted-foreground hover:text-foreground rounded-full hover:bg-muted/50 transition-colors whitespace-nowrap"
                >
                  Log in
                </Link>
                <Link
                  href="/auth/register"
                  className="inline-flex items-center justify-center h-9 px-3.5 text-xs md:text-sm font-medium text-foreground rounded-full hover:bg-muted/50 transition-colors whitespace-nowrap"
                >
                  Sign up
                </Link>
              </>
            )}
            <Link
              href="/map"
              className="inline-flex items-center justify-center h-9 px-4 sm:px-5 bg-primary text-primary-foreground hover:bg-primary/90 text-xs md:text-sm font-medium rounded-full shadow-sm transition-all hover:scale-[1.02] active:scale-[0.98] whitespace-nowrap"
            >
              Explore Map
            </Link>
          </div>
        </nav>
      </header>

      {/* Hero Section 1: The App Node Hub with staggered reveal */}
      <section className="relative pt-32 sm:pt-40 pb-20 sm:pb-28 overflow-hidden flex flex-col items-center justify-center text-center px-4">
        {/* Ambient background glow using project primary green */}
        <div
          className={
            "absolute top-1/4 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[380px] bg-primary/10 blur-3xl pointer-events-none rounded-full -z-10 transition-opacity duration-1000 " +
            (mounted ? "opacity-100 scale-100" : "opacity-0 scale-75")
          }
        />

        {/* Interactive Ecosystem Diagram Hub */}
        <div
          className={
            "relative w-80 h-80 sm:w-96 sm:h-96 md:w-[420px] md:h-[420px] flex items-center justify-center my-4 transition-all duration-700 ease-out " +
            (mounted ? "opacity-100 scale-100" : "opacity-0 scale-90")
          }
          style={{
            transform: "translateY(" + hubTranslationY + "px)",
            opacity: hubOpacity,
          }}
        >
          {/* Radar Guides & Orbit Rings */}
          <div className="absolute inset-2 sm:inset-4 rounded-full border border-dashed border-border/80 animate-[spin_60s_linear_infinite] pointer-events-none" />
          <div className="absolute inset-14 sm:inset-16 rounded-full border border-border/60 pointer-events-none" />

          {/* Radiating Circuit Lines to each satellite */}
          <svg className="absolute inset-0 w-full h-full pointer-events-none stroke-border/70" fill="none" strokeWidth="1.5">
            {satellites.map((sat) => (
              <line
                key={sat.id}
                x1="50%"
                y1="50%"
                x2={sat.leftPct + "%"}
                y2={sat.topPct + "%"}
                strokeDasharray="4 4"
                className="transition-opacity duration-500"
              />
            ))}
          </svg>

          {/* Radiating Satellite Nodes with Pop/Fade-in Stagger */}
          {satellites.map((sat) => {
            const isReady = mounted;
            return (
              <div
                key={sat.id}
                className="absolute -translate-x-1/2 -translate-y-1/2 transition-all duration-700 cubic-bezier(0.34, 1.56, 0.64, 1)"
                style={{
                  left: sat.leftPct + "%",
                  top: sat.topPct + "%",
                  transform: "translate(-50%, -50%) scale(" + (isReady ? satelliteSpread : 0.4) + ")",
                  opacity: isReady ? satelliteOpacity : 0,
                  transitionDelay: sat.delay + "ms",
                }}
              >
                <Link href={sat.href} className="relative group cursor-pointer block">
                  {sat.img ? (
                    <div className="w-13 h-13 sm:w-16 sm:h-16 rounded-2xl overflow-hidden p-0.5 bg-card border border-border shadow-md transition-all duration-300 group-hover:scale-110 group-hover:shadow-lg group-hover:border-primary/50">
                      <img src={sat.img} alt={sat.label} className="w-full h-full object-cover rounded-[14px]" />
                    </div>
                  ) : (
                    <div
                      className={
                        "w-12 h-12 sm:w-14 sm:h-14 rounded-2xl flex items-center justify-center shadow-md transition-all duration-300 group-hover:scale-110 group-hover:shadow-lg " +
                        sat.color + " " + sat.ring + " border"
                      }
                    >
                      {sat.icon && <sat.icon className="w-5 h-5 sm:w-6 sm:h-6" />}
                    </div>
                  )}
                  <span className="absolute -bottom-6 left-1/2 -translate-x-1/2 text-[10px] font-semibold text-muted-foreground bg-card px-2 py-0.5 rounded-full shadow-xs whitespace-nowrap opacity-0 group-hover:opacity-100 transition-opacity border border-border pointer-events-none">
                    {sat.label}
                  </span>
                </Link>
              </div>
            );
          })}

          {/* Central Squircle with primary theme color + Pulse effect */}
          <Link
            href="/map"
            className={
              "relative z-10 w-24 h-24 sm:w-28 sm:h-28 rounded-[28px] bg-primary text-primary-foreground flex items-center justify-center shadow-xl shadow-primary/25 border-2 border-background transition-all duration-700 hover:scale-105 cursor-pointer " +
              (mounted ? "scale-100 opacity-100" : "scale-50 opacity-0")
            }
            style={{ transitionDelay: "100ms" }}
          >
            <div className="relative w-14 h-14 rounded-full border-2 border-primary-foreground/40 flex items-center justify-center">
              <div className="absolute w-1 h-3 bg-primary-foreground top-1 rounded-full" />
              <div className="absolute w-2.5 h-2.5 bg-primary-foreground rounded-full shadow-sm" />
              <div className="absolute w-0.5 h-4 bg-primary-foreground/90 origin-bottom transform rotate-45 -translate-y-2 rounded-full" />
              <div className="absolute inset-0 rounded-full border border-dashed border-primary-foreground/60 animate-[spin_16s_linear_infinite]" />
            </div>
          </Link>
        </div>

        {/* Hero 1 Headline, Subtitle, and CTA Button with staggered reveal */}
        <div
          className={
            "max-w-3xl mx-auto mt-6 transition-all duration-700 ease-out " +
            (mounted ? "translate-y-0 opacity-100" : "translate-y-8 opacity-0")
          }
          style={{ transitionDelay: "300ms" }}
        >
          <h1 className="text-4xl sm:text-6xl md:text-7xl font-black text-foreground tracking-tight leading-[1.08] font-sans">
            All-in-one Tourism platform
          </h1>
          <p className="mt-5 text-base sm:text-xl text-muted-foreground max-w-2xl mx-auto leading-relaxed font-normal">
            An interactive digital cultural map and local tourism information system for Mangatarem, Pangasinan.
            Discover eco-destinations, local heritage, and 82 connected barangays.
          </p>

          <div className="mt-8 flex justify-center gap-3">
            <Link
              href="/map"
              className="bg-primary hover:bg-primary/90 text-primary-foreground text-base font-semibold px-8 py-3.5 rounded-full shadow-lg shadow-primary/20 transition-all hover:scale-105 active:scale-95 flex items-center gap-2"
            >
              Explore Interactive Map
              <ArrowRight className="w-4 h-4" />
            </Link>
          </div>
        </div>
      </section>

      {/* Hero Section 2: Floating Portrait Gallery */}
      <section className="relative py-24 sm:py-32 overflow-hidden border-t border-border/50 bg-muted/20">
        <div className="max-w-7xl mx-auto px-4 relative">
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-center min-h-[520px]">
            {/* Left 4 Portrait Cards */}
            <div className="hidden lg:grid grid-cols-2 gap-4 col-span-3">
              {galleryLeft.map((p) => {
                const translateY = (scrollY - 700) * (p.speed * 0.12);
                return (
                  <div
                    key={p.id}
                    className={"transition-transform duration-75 ease-out " + p.margin}
                    style={{ transform: "translateY(" + translateY + "px)" }}
                  >
                    <div
                      className={"group bg-card border border-border/80 rounded-2xl p-2 shadow-sm transition-all duration-300 hover:scale-105 hover:shadow-lg hover:border-primary/40 " + p.blur}
                    >
                      <div className="aspect-[4/5] rounded-xl overflow-hidden relative">
                        <img src={p.img} alt={p.name} className="w-full h-full object-cover" />
                        <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity flex items-end p-2.5">
                          <div>
                            <p className="text-white text-xs font-semibold">{p.name}</p>
                            <p className="text-primary-foreground/80 text-[10px]">{p.category}</p>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>

            {/* Center Content: Squircle + Core Cultural solutions */}
            <div className="col-span-1 lg:col-span-6 flex flex-col items-center text-center px-4 z-20">
              <div className="w-12 h-12 rounded-2xl bg-primary/15 text-primary border border-primary/20 flex items-center justify-center shadow-sm mb-5">
                <Users className="w-6 h-6" />
              </div>

              <h2 className="text-3xl sm:text-5xl font-black tracking-tight text-foreground mb-4 font-sans">
                Core Cultural solutions
              </h2>

              <p className="text-muted-foreground text-base sm:text-lg max-w-lg mb-8 leading-relaxed">
                Empower local communities, preservation leaders, and travelers with unified maps, verified records, and live tourism indices.
              </p>

              <Link
                href="/attractions"
                className="bg-primary/10 hover:bg-primary/20 text-primary font-semibold text-sm sm:text-base px-7 py-3 rounded-full shadow-sm transition-all hover:scale-105 active:scale-95 flex items-center gap-2"
              >
                Learn more
                <ArrowRight className="w-4 h-4 text-primary" />
              </Link>
            </div>

            {/* Right 4 Portrait Cards */}
            <div className="hidden lg:grid grid-cols-2 gap-4 col-span-3">
              {galleryRight.map((p) => {
                const translateY = -(scrollY - 700) * (p.speed * 0.12);
                return (
                  <div
                    key={p.id}
                    className={"transition-transform duration-75 ease-out " + p.margin}
                    style={{ transform: "translateY(" + translateY + "px)" }}
                  >
                    <div
                      className={"group bg-card border border-border/80 rounded-2xl p-2 shadow-sm transition-all duration-300 hover:scale-105 hover:shadow-lg hover:border-primary/40 " + p.blur}
                    >
                      <div className="aspect-[4/5] rounded-xl overflow-hidden relative">
                        <img src={p.img} alt={p.name} className="w-full h-full object-cover" />
                        <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity flex items-end p-2.5">
                          <div>
                            <p className="text-white text-xs font-semibold">{p.name}</p>
                            <p className="text-primary-foreground/80 text-[10px]">{p.category}</p>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        </div>
      </section>

      {/* Section 3: "Built for Everyone" Bento Grid */}
      <section id="features" className="py-24 max-w-7xl mx-auto px-4 sm:px-6">
        <div className="text-center max-w-3xl mx-auto mb-16">
          <h2 className="text-3xl sm:text-5xl font-black text-foreground tracking-tight font-sans">
            Built for everyone
          </h2>
          <p className="mt-4 text-muted-foreground text-base sm:text-lg">
            Manage travelers, local heritage properties, community businesses, and tourism data in one unified architecture.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {/* Card 1: Attendance Report bar chart */}
          <div className="bg-card border border-border/80 rounded-3xl p-6 shadow-sm hover:shadow-lg hover:-translate-y-1 transition-all duration-300 flex flex-col justify-between">
            <div>
              <div className="flex items-center justify-between mb-4">
                <div className="flex items-center gap-2">
                  <div className="w-8 h-8 rounded-xl bg-primary/10 text-primary flex items-center justify-center">
                    <BarChart2 className="w-4 h-4" />
                  </div>
                  <h3 className="font-bold text-foreground text-base">Attendance Report</h3>
                </div>
                <div className="flex bg-muted p-0.5 rounded-lg text-xs font-semibold">
                  <button
                    onClick={() => setReportView("daily")}
                    className={"px-2.5 py-1 rounded-md transition-all " + (reportView === "daily" ? "bg-card text-foreground shadow-xs" : "text-muted-foreground")}
                  >
                    Daily
                  </button>
                  <button
                    onClick={() => setReportView("monthly")}
                    className={"px-2.5 py-1 rounded-md transition-all " + (reportView === "monthly" ? "bg-card text-foreground shadow-xs" : "text-muted-foreground")}
                  >
                    Monthly
                  </button>
                </div>
              </div>
              <p className="text-xs text-muted-foreground mb-6">
                Eco-trail and cultural spot visitor traffic across Mangatarem tourism nodes.
              </p>

              <div className="h-36 flex items-end justify-between gap-2 px-2 pt-4 border-b border-border/50">
                {(reportView === "daily"
                  ? [65, 88, 94, 76, 98, 85, 92]
                  : [78, 82, 89, 93, 86, 91, 95]
                ).map((val, idx) => (
                  <div key={idx} className="flex-1 flex flex-col items-center gap-1.5 h-full justify-end group">
                    <span className="text-[10px] font-semibold text-primary opacity-0 group-hover:opacity-100 transition-opacity">
                      {val}%
                    </span>
                    <div
                      className="w-full bg-primary rounded-t-md transition-all duration-500"
                      style={{ height: val + "%" }}
                    />
                    <span className="text-[10px] text-muted-foreground font-medium">
                      {["M", "T", "W", "T", "F", "S", "S"][idx]}
                    </span>
                  </div>
                ))}
              </div>
            </div>

            <div className="mt-4 flex items-center justify-between text-xs text-muted-foreground">
              <span className="flex items-center gap-1 text-primary font-semibold">
                <TrendingUp className="w-3.5 h-3.5" /> +18.4% seasonal surge
              </span>
              <span className="font-mono text-muted-foreground">94.2% satisfaction</span>
            </div>
          </div>

          {/* Card 2: Rotating Text Pill Badge */}
          <div className="bg-primary text-primary-foreground rounded-3xl p-6 shadow-sm hover:shadow-lg hover:-translate-y-1 transition-all duration-300 flex flex-col justify-between overflow-hidden relative min-h-[280px]">
            <div className="absolute top-0 right-0 w-48 h-48 bg-white/10 rounded-full blur-2xl pointer-events-none" />

            <div className="relative z-10">
              <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-white/15 border border-white/20 text-white text-xs font-medium mb-6">
                <Sparkles className="w-3.5 h-3.5 text-white" />
                Live Tourism Feed
              </div>

              <h3 className="text-xl font-bold tracking-tight mb-2">Intelligent Digital Heritage Network</h3>
              <p className="text-xs text-primary-foreground/80 leading-relaxed mb-6">
                Live synchronization between GIS spatial data, tourist visits, and barangay cultural logs.
              </p>
            </div>

            <div className="relative z-10 my-4 bg-white/10 backdrop-blur-md border border-white/20 p-4 rounded-2xl overflow-hidden">
              <div className="h-8 relative overflow-hidden flex items-center">
                {rotatingTextPills.map((text, idx) => (
                  <div
                    key={text}
                    className={"absolute inset-0 flex items-center font-bold text-xs sm:text-sm text-white tracking-wide transition-all duration-700 ease-in-out " + (idx === activePillIndex ? "opacity-100 translate-x-0" : idx < activePillIndex ? "opacity-0 -translate-x-full" : "opacity-0 translate-x-full")}
                  >
                    <div className="w-2 h-2 rounded-full bg-white mr-2 shrink-0 animate-ping" />
                    <span className="truncate">{text}</span>
                  </div>
                ))}
              </div>
            </div>

            <div className="relative z-10 flex items-center justify-between text-[11px] text-primary-foreground/80 pt-2">
              <span>Updated live</span>
              <span className="text-white font-semibold">82 Barangays Synced</span>
            </div>
          </div>

          {/* Card 3: Legal Document Previews */}
          <div className="bg-card border border-border/80 rounded-3xl p-6 shadow-sm hover:shadow-lg hover:-translate-y-1 transition-all duration-300 flex flex-col justify-between">
            <div>
              <div className="flex items-center justify-between mb-4">
                <div className="flex items-center gap-2">
                  <div className="w-8 h-8 rounded-xl bg-primary/10 text-primary flex items-center justify-center">
                    <FileText className="w-4 h-4" />
                  </div>
                  <h3 className="font-bold text-foreground text-base">Registry & Ordinances</h3>
                </div>
                <span className="px-2.5 py-0.5 rounded-full bg-primary/15 text-primary text-xs font-semibold">
                  Verified
                </span>
              </div>
              <p className="text-xs text-muted-foreground mb-4">
                Municipal tourism guidelines and cultural heritage ordinances.
              </p>

              <div className="space-y-2.5">
                {[
                  { name: "Mangatarem Eco-Tourism Charter v2.pdf", status: "Digitally Signed" },
                  { name: "Historical Landmark Resolution No. 14.pdf", status: "Audit Cleared" },
                  { name: "Pangasinan Cultural Inventory Form.pdf", status: "In Vault" },
                ].map((doc, idx) => (
                  <div
                    key={idx}
                    className="p-2.5 rounded-xl border border-border/60 bg-muted/30 hover:bg-muted/60 transition-colors flex items-center justify-between"
                  >
                    <div className="flex items-center gap-2 overflow-hidden">
                      <FileText className="w-4 h-4 text-primary shrink-0" />
                      <span className="text-xs font-semibold text-foreground truncate">{doc.name}</span>
                    </div>
                    <span className="text-[10px] text-primary font-medium shrink-0 ml-2 bg-primary/10 px-2 py-0.5 rounded-md">
                      {doc.status}
                    </span>
                  </div>
                ))}
              </div>
            </div>

            <div className="mt-4 pt-3 border-t border-border/50 flex items-center justify-between text-xs text-muted-foreground">
              <span>Official municipal records</span>
              <span className="font-semibold text-primary">Verified LGU Archive</span>
            </div>
          </div>

          {/* Card 4 (Bottom Left - Spans 2 cols): Data Table with Featured Spots */}
          <div className="md:col-span-2 bg-card border border-border/80 rounded-3xl p-6 shadow-sm hover:shadow-lg hover:-translate-y-1 transition-all duration-300">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 mb-4">
              <div>
                <h3 className="font-bold text-foreground text-base">Featured Attractions & Eco-Cultural Sites</h3>
                <p className="text-xs text-muted-foreground">
                  Real-time tourist participation and visitor satisfaction scores.
                </p>
              </div>
              <Link
                href="/attractions"
                className="text-xs font-semibold text-primary bg-primary/10 hover:bg-primary/20 px-3 py-1 rounded-full self-start sm:self-auto transition-colors flex items-center gap-1"
              >
                View all attractions <ArrowUpRight className="w-3 h-3" />
              </Link>
            </div>

            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs">
                <thead>
                  <tr className="border-b border-border/60 text-muted-foreground font-semibold uppercase tracking-wider text-[10px]">
                    <th className="py-2.5 px-2">Destination</th>
                    <th className="py-2.5 px-2">Barangay</th>
                    <th className="py-2.5 px-2">Category</th>
                    <th className="py-2.5 px-2">Popularity Index</th>
                    <th className="py-2.5 px-2 text-right">Rating</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-border/40">
                  {(attractions.length > 0
                    ? attractions.slice(0, 3)
                    : [
                        {
                          id: 1,
                          name: "Manleluag Spring Protected Landscape",
                          barangay_name: "Malabobo",
                          category: "Nature & Hot Spring",
                          average_rating: 4.9,
                        },
                        {
                          id: 2,
                          name: "Saint Raymund de Peñafort Church",
                          barangay_name: "Poblacion",
                          category: "Historical & Religious",
                          average_rating: 4.8,
                        },
                        {
                          id: 3,
                          name: "Daang Kalikasan Highway",
                          barangay_name: "Highland Corridor",
                          category: "Scenic Eco Trail",
                          average_rating: 5.0,
                        },
                      ]
                  ).map((item) => {
                    const ratingScore = item.average_rating || 4.8;
                    const pct = Math.round((ratingScore / 5) * 100);
                    return (
                      <tr key={item.id} className="hover:bg-muted/40 transition-colors">
                        <td className="py-3 px-2 flex items-center gap-2.5">
                          <div className="w-8 h-8 rounded-lg overflow-hidden bg-muted shrink-0 border border-border">
                            <img
                              src={resolvePlaceImage(item.image_url, item.name)}
                              alt={item.name}
                              className="w-full h-full object-cover"
                            />
                          </div>
                          <Link href={"/attractions/" + item.id} className="font-semibold text-foreground hover:text-primary transition-colors">
                            {item.name}
                          </Link>
                        </td>
                        <td className="py-3 px-2 text-foreground font-medium">{item.barangay_name || "Mangatarem"}</td>
                        <td className="py-3 px-2 text-muted-foreground">{item.category || "Heritage"}</td>
                        <td className="py-3 px-2">
                          <div className="flex items-center gap-2">
                            <div className="w-24 h-2 bg-muted rounded-full overflow-hidden">
                              <div
                                className="h-full bg-primary rounded-full"
                                style={{ width: pct + "%" }}
                              />
                            </div>
                            <span className="font-mono text-[10px] text-muted-foreground">
                              {pct}%
                            </span>
                          </div>
                        </td>
                        <td className="py-3 px-2 text-right">
                          <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[10px] font-semibold bg-amber-500/10 text-amber-700 dark:text-amber-300 border border-amber-500/20">
                            <Star className="w-3 h-3 fill-amber-400 text-amber-400" />
                            {ratingScore.toFixed(1)}
                          </span>
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
          </div>

          {/* Card 5: Circular Avatar Wheel showing Active Tour Guides */}
          <div className="bg-card border border-border/80 rounded-3xl p-6 shadow-sm hover:shadow-lg hover:-translate-y-1 transition-all duration-300 flex flex-col items-center justify-between text-center">
            <div className="w-full flex items-center justify-between mb-2">
              <h3 className="font-bold text-foreground text-base">Active Tour Guides</h3>
              <span className="text-xs font-semibold px-2 py-0.5 rounded-md bg-primary/10 text-primary border border-primary/20">
                6 on Trail
              </span>
            </div>
            <p className="text-xs text-muted-foreground mb-4 text-left w-full">
              Accredited community eco-guides currently guiding mountain expeditions.
            </p>

            <div className="relative w-40 h-40 my-2 flex items-center justify-center">
              <div className="w-16 h-16 rounded-full bg-primary text-primary-foreground flex flex-col items-center justify-center shadow-md shadow-primary/20">
                <span className="font-bold text-base">6</span>
                <span className="text-[9px] uppercase font-semibold tracking-wider text-primary-foreground/80">Active</span>
              </div>

              <div className="absolute inset-0 rounded-full border border-dashed border-primary/30 animate-[spin_40s_linear_infinite]" />

              {[
                { img: "https://images.unsplash.com/photo-1544005313-94ddf0286df2?w=100&auto=format&fit=crop&q=80", pos: "top-0 left-1/2 -translate-x-1/2" },
                { img: "https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?w=100&auto=format&fit=crop&q=80", pos: "bottom-0 left-1/2 -translate-x-1/2" },
                { img: "https://images.unsplash.com/photo-1517841905240-472988babdf9?w=100&auto=format&fit=crop&q=80", pos: "left-0 top-1/2 -translate-y-1/2" },
                { img: "https://images.unsplash.com/photo-1492562080023-ab3db95bfbce?w=100&auto=format&fit=crop&q=80", pos: "right-0 top-1/2 -translate-y-1/2" },
              ].map((av, i) => (
                <div key={i} className={"absolute " + av.pos + " p-1 bg-card rounded-full shadow-md border border-border"}>
                  <img src={av.img} alt="Accredited Guide" className="w-8 h-8 rounded-full object-cover" />
                </div>
              ))}
            </div>

            <div className="w-full pt-3 border-t border-border/50 flex items-center justify-between text-xs text-muted-foreground">
              <span>Next trail briefing</span>
              <span className="font-semibold text-foreground">Today, 2:00 PM</span>
            </div>
          </div>
        </div>
      </section>

      {/* Section 4: The 3D Revolving Wheel Carousel */}
      <section
        className="py-24 bg-muted/20 overflow-hidden border-y border-border/50 select-none"
        onMouseEnter={() => setIsWheelPaused(true)}
        onMouseLeave={() => setIsWheelPaused(false)}
      >
        <div className="max-w-6xl mx-auto px-4 text-center">
          <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-primary/10 border border-primary/20 text-primary text-xs font-semibold mb-4">
            <div className="flex -space-x-1">
              <div className="w-2.5 h-2.5 rounded-full bg-primary" />
              <div className="w-2.5 h-2.5 rounded-full bg-primary/60" />
            </div>
            Connected Tourism Network
          </div>

          <h2 className="text-3xl sm:text-5xl font-black text-foreground tracking-tight max-w-2xl mx-auto font-sans">
            Integrate with your existing tools in seconds
          </h2>
          <p className="text-sm text-muted-foreground mt-3">
            Continuously rotating circular carousel • Hover to pause or click any module
          </p>

          {/* Semicircular Half-Wheel Stage: guiding lines hidden, lower boundary cleanly clipped */}
          <div className="relative mt-6 mb-8 h-[360px] sm:h-[400px] flex flex-col items-center justify-end">
            {/* Left & Right Arc Spin Buttons */}
            <button
              onClick={() => setWheelElapsed((prev) => prev - 1)}
              aria-label="Previous Module"
              className="absolute left-2 sm:left-4 md:left-8 top-1/2 -translate-y-1/2 z-30 w-11 h-11 rounded-full bg-background/90 hover:bg-background border border-border flex items-center justify-center text-muted-foreground hover:text-foreground shadow-md hover:scale-105 active:scale-95 transition-all cursor-pointer backdrop-blur-md"
            >
              <ChevronLeft className="w-5 h-5" />
            </button>
            <button
              onClick={() => setWheelElapsed((prev) => prev + 1)}
              aria-label="Next Module"
              className="absolute right-2 sm:right-4 md:right-8 top-1/2 -translate-y-1/2 z-30 w-11 h-11 rounded-full bg-background/90 hover:bg-background border border-border flex items-center justify-center text-muted-foreground hover:text-foreground shadow-md hover:scale-105 active:scale-95 transition-all cursor-pointer backdrop-blur-md"
            >
              <ChevronRight className="w-5 h-5" />
            </button>

            {/* Clipped Semicircular Viewport: Only the upper half of the circle is visible.
                Anything dipping below the baseline / equator is cleanly masked out. */}
            <div
              className="relative w-full max-w-6xl h-full flex items-end justify-center pb-6 overflow-hidden [mask-image:linear-gradient(to_bottom,black_0%,black_88%,transparent_100%)] [-webkit-mask-image:linear-gradient(to_bottom,black_0%,black_88%,transparent_100%)]"
            >
              {tourismModules.map((app, index) => {
                const total = tourismModules.length;
                let offset = (index - activeModule) % total;
                if (offset > total / 2) offset -= total;
                if (offset < -total / 2) offset += total;

                const isCenter = offset === 0;
                // Position from the exact integer table (index 2 = centered).
                // Math.cos/sin would emit long float strings that mismatch
                // between server (float serialize) and client (style parse).
                const spot = WHEEL_OFFSETS[offset + 2];
                const xPos = spot.x;
                const yPos = spot.y; // arch up to apex
                const tiltAngle = spot.tilt; // tilts card proportionally
                const scale = spot.scale;
                const opacity = spot.opacity;
                const zIndex = spot.z;

                return (
                  <button
                    key={app.id}
                    onClick={() => setWheelElapsed(index)}
                    style={{
                      transform:
                        "translateX(" +
                        xPos +
                        "px) translateY(" +
                        yPos +
                        "px) rotate(" +
                        tiltAngle +
                        "deg) scale(" +
                        scale +
                        ")",
                      opacity: opacity,
                      zIndex: zIndex,
                      transition: "all 0.65s cubic-bezier(0.25, 1, 0.5, 1)",
                    }}
                    className={
                      "absolute w-32 sm:w-40 h-40 sm:h-48 rounded-3xl p-4 sm:p-5 flex flex-col items-center justify-center bg-card border-2 shadow-md transition-all cursor-pointer " +
                      (isCenter
                        ? "border-primary shadow-xl shadow-primary/20 ring-4 ring-primary/10"
                        : "border-border/80 hover:border-primary/50")
                    }
                  >
                    <div
                      className={
                        "w-13 h-13 sm:w-16 sm:h-16 rounded-2xl flex items-center justify-center mb-3 shadow-inner transition-transform " +
                        app.brandBg +
                        (isCenter ? " scale-110" : "")
                      }
                    >
                      <app.icon className="w-7 h-7 sm:w-8 sm:h-8" />
                    </div>
                    <span className="font-bold text-xs sm:text-sm text-foreground tracking-tight text-center line-clamp-1">
                      {app.name}
                    </span>
                  </button>
                );
              })}
            </div>
          </div>

          {/* Active Module Details & Direct Link */}
          <div className="max-w-xl mx-auto min-h-[90px] transition-all duration-300">
            <h4 className="text-xl font-extrabold text-foreground tracking-tight flex items-center justify-center gap-2">
              {tourismModules[activeModule].name}
              <Link
                href={tourismModules[activeModule].href}
                className="text-primary hover:underline text-xs font-semibold inline-flex items-center gap-0.5"
              >
                Open <ArrowRight className="w-3 h-3" />
              </Link>
            </h4>
            <p className="text-sm text-muted-foreground mt-1 leading-relaxed">
              {tourismModules[activeModule].summary}
            </p>

            {/* Interactive Carousel Pill Dots */}
            <div className="flex justify-center gap-2 mt-5">
              {tourismModules.map((_, i) => (
                <button
                  key={i}
                  onClick={() => setWheelElapsed(i)}
                  className={
                    "h-2 rounded-full transition-all duration-300 cursor-pointer " +
                    (i === activeModule ? "w-7 bg-primary" : "w-2 bg-muted hover:bg-muted-foreground/40")
                  }
                />
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* Section 5: "Words of Appreciation" Testimonials */}
      <section className="py-24 max-w-6xl mx-auto px-4">
        <div className="text-center max-w-2xl mx-auto mb-16">
          <h2 className="text-3xl sm:text-5xl font-black text-foreground tracking-tight font-sans">
            Words of Appreciation
          </h2>
          <p className="mt-3 text-muted-foreground text-base sm:text-lg">
            Trusted by travelers, historians, and local communities exploring the heart of Pangasinan.
          </p>
        </div>

        <div className="relative overflow-hidden py-4">
          <div className="flex items-center justify-center gap-4 sm:gap-8">
            {visitorTestimonials.map((t, idx) => {
              const isCenter = idx === activeTestimonial;
              const isLeft = idx === (activeTestimonial - 1 + visitorTestimonials.length) % visitorTestimonials.length;
              const isRight = idx === (activeTestimonial + 1) % visitorTestimonials.length;

              if (!isCenter && !isLeft && !isRight) return null;

              return (
                <div
                  key={t.id}
                  className={"transition-all duration-500 ease-out transform " + (isCenter ? "scale-100 opacity-100 z-20 w-full max-w-2xl" : "hidden md:block scale-90 opacity-30 z-10 w-80 shrink-0 pointer-events-none")}
                >
                  <div className="bg-card border border-border/80 rounded-3xl p-7 sm:p-10 shadow-lg shadow-primary/5 flex flex-col justify-between">
                    <div className="flex items-center justify-between border-b border-border/50 pb-5 mb-5">
                      <div className="flex items-center gap-3.5">
                        <div className="w-14 h-14 rounded-2xl overflow-hidden border border-border shadow-sm p-0.5 bg-muted">
                          <img src={t.avatar} alt={t.name} className="w-full h-full object-cover rounded-[14px]" />
                        </div>
                        <div>
                          <h4 className="font-bold text-foreground text-base">{t.name}</h4>
                          <p className="text-xs text-muted-foreground">{t.title}</p>
                        </div>
                      </div>

                      <div className="flex items-center gap-1.5 bg-amber-500/10 px-3 py-1.5 rounded-full border border-amber-500/20">
                        <div className="flex text-amber-400">
                          {[...Array(5)].map((_, i) => (
                            <Star key={i} className="w-3.5 h-3.5 fill-amber-400" />
                          ))}
                        </div>
                        <span className="font-bold text-xs text-amber-700 dark:text-amber-300 ml-1">{t.rating}</span>
                      </div>
                    </div>

                    <p className="text-foreground/90 text-sm sm:text-base leading-relaxed italic">
                      \"{t.quote}\"
                    </p>
                  </div>
                </div>
              );
            })}
          </div>

          <div className="flex justify-center items-center gap-4 mt-10">
            <button
              onClick={prevTestimonial}
              aria-label="Previous testimonial"
              className="w-12 h-12 rounded-full border border-border hover:border-foreground bg-card flex items-center justify-center text-muted-foreground hover:text-foreground shadow-sm hover:scale-105 active:scale-95 transition-all cursor-pointer"
            >
              <ChevronLeft className="w-5 h-5" />
            </button>
            <button
              onClick={nextTestimonial}
              aria-label="Next testimonial"
              className="w-12 h-12 rounded-full border border-border hover:border-foreground bg-card flex items-center justify-center text-muted-foreground hover:text-foreground shadow-sm hover:scale-105 active:scale-95 transition-all cursor-pointer"
            >
              <ChevronRight className="w-5 h-5" />
            </button>
          </div>
        </div>
      </section>

      {/* Section 6: The Footer and Kinetic Watermark */}
      <footer className="relative bg-card pt-20 pb-12 border-t border-border/80 overflow-hidden">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 relative z-10">
          <div className="grid grid-cols-1 md:grid-cols-12 gap-10 pb-16">
            {/* Column 1: Mission Statement */}
            <div className="md:col-span-4 space-y-4">
              <Link href="/" className="flex items-center gap-2">
                <div className="w-8 h-8 rounded-xl bg-primary flex items-center justify-center text-primary-foreground shadow-sm">
                  <Compass className="w-4 h-4" />
                </div>
                <span className="font-extrabold text-xl tracking-tight text-foreground">
                  Mangatarem<span className="text-primary">Tourism</span>
                </span>
              </Link>
              <p className="text-muted-foreground text-sm leading-relaxed max-w-sm">
                Interactive Digital Cultural Map and Local Tourism Information System for Mangatarem, Pangasinan.
                Documenting historical monuments, protected landscapes, and community heritage.
              </p>
            </div>

            {/* Column 2: Navigation Links 1 */}
            <div className="md:col-span-2 space-y-3">
              <h5 className="font-bold text-foreground text-sm">Explore</h5>
              <ul className="space-y-2 text-sm text-muted-foreground">
                <li><Link href="/attractions" className="hover:text-foreground transition-colors">Attractions</Link></li>
                <li><Link href="/map" className="hover:text-foreground transition-colors">Interactive Map</Link></li>
                <li><Link href="/events" className="hover:text-foreground transition-colors">Events & Fiestas</Link></li>
                <li><Link href="/heritage" className="hover:text-foreground transition-colors">Cultural Heritage</Link></li>
                <li><Link href="/barangays" className="hover:text-foreground transition-colors">82 Barangays</Link></li>
              </ul>
            </div>

            {/* Column 3: Navigation Links 2 */}
            <div className="md:col-span-2 space-y-3">
              <h5 className="font-bold text-foreground text-sm">Community</h5>
              <ul className="space-y-2 text-sm text-muted-foreground">
                <li><Link href="/gallery" className="hover:text-foreground transition-colors">Photo Gallery</Link></li>
                <li><Link href="/business" className="hover:text-foreground transition-colors">Local Businesses</Link></li>
                <li><Link href="/announcements" className="hover:text-foreground transition-colors">Announcements</Link></li>
                <li><Link href="/passport" className="hover:text-foreground transition-colors">Tourist Passport</Link></li>
              </ul>
            </div>

            {/* Column 4: Newsletter & Socials */}
            <div className="md:col-span-4 space-y-4">
              <h5 className="font-bold text-foreground text-sm">Stay in the Loop</h5>
              <p className="text-xs text-muted-foreground">
                Subscribe for local festivals, conservation updates, and tourism advisories.
              </p>
              <div className="max-w-md">
                <NewsletterSubscribe />
              </div>

              <div className="pt-2">
                <h6 className="text-xs font-semibold text-muted-foreground uppercase tracking-wider mb-2">Connect With Us</h6>
                <div className="flex items-center gap-3">
                  <a
                    href="https://instagram.com"
                    target="_blank"
                    rel="noreferrer"
                    aria-label="Instagram"
                    className="w-11 h-11 rounded-2xl bg-card border border-border shadow-xs hover:border-primary flex items-center justify-center text-muted-foreground hover:text-primary transition-all"
                  >
                    <svg className="w-5 h-5 fill-current" viewBox="0 0 24 24">
                      <path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-.059-1.69-.073-4.949-.073zm0 5.838c-3.403 0-6.162 2.759-6.162 6.162s2.759 6.163 6.162 6.163 6.162-2.759 6.162-6.163c0-3.403-2.759-6.162-6.162-6.162zm0 10.162c-2.209 0-4-1.79-4-4 0-2.209 1.791-4 4-4s4 1.791 4 4c0 2.21-1.791 4-4 4zm6.406-11.845c-.796 0-1.441.645-1.441 1.44s.645 1.44 1.441 1.44c.795 0 1.439-.645 1.439-1.44s-.644-1.44-1.439-1.44z" />
                    </svg>
                  </a>
                  <a
                    href="https://x.com"
                    target="_blank"
                    rel="noreferrer"
                    aria-label="X"
                    className="w-11 h-11 rounded-2xl bg-card border border-border shadow-xs hover:border-primary flex items-center justify-center text-muted-foreground hover:text-foreground transition-all"
                  >
                    <svg className="w-4 h-4 fill-current" viewBox="0 0 24 24">
                      <path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z" />
                    </svg>
                  </a>
                  <a
                    href="https://tiktok.com"
                    target="_blank"
                    rel="noreferrer"
                    aria-label="TikTok"
                    className="w-11 h-11 rounded-2xl bg-card border border-border shadow-xs hover:border-primary flex items-center justify-center text-muted-foreground hover:text-foreground transition-all"
                  >
                    <svg className="w-4 h-4 fill-current" viewBox="0 0 24 24">
                      <path d="M12.525.02c1.31-.02 2.61-.01 3.91-.02.08 1.53.63 3.09 1.75 4.17 1.12 1.11 2.7 1.62 4.24 1.79v4.03c-1.44-.05-2.89-.35-4.2-.97-.57-.26-1.1-.59-1.62-.93-.01 2.92.01 5.84-.02 8.75-.08 1.4-.54 2.79-1.35 3.94-1.31 1.92-3.58 3.17-5.91 3.21-1.43.08-2.86-.31-4.08-1.03-2.02-1.19-3.44-3.37-3.65-5.71-.02-.5-.03-1-.01-1.49.18-1.9 1.12-3.72 2.58-4.96 1.66-1.44 3.98-2.13 6.15-1.72.02 1.48-.04 2.96-.04 4.44-.99-.32-2.15-.23-3.02.37-.63.41-1.11 1.04-1.36 1.75-.21.51-.24 1.07-.14 1.61.24 1.64 1.82 3.02 3.5 2.87 1.12-.01 2.19-.66 2.77-1.61.19-.33.4-.67.41-1.06.1-1.79.06-3.57.07-5.36.01-4.03-.01-8.05.02-12.07z" />
                    </svg>
                  </a>
                </div>
              </div>
            </div>
          </div>

          <div className="flex flex-col sm:flex-row items-center justify-between border-t border-border/50 pt-6 text-xs text-muted-foreground">
            <p>© {new Date().getFullYear()} Municipality of Mangatarem, Pangasinan. All rights reserved.</p>
            <div className="flex gap-6 mt-4 sm:mt-0">
              <Link href="/privacy" className="hover:text-foreground">Privacy Notice</Link>
              <Link href="/terms" className="hover:text-foreground">Terms of Service</Link>
              <Link href="/map" className="hover:text-foreground">Interactive Map</Link>
            </div>
          </div>
        </div>

        {/* Bottom Half: Massive Kinetic Logotype Watermark with project primary color */}
        <div className="relative w-full overflow-hidden select-none pointer-events-none mt-12 flex justify-center items-center">
          <div className="absolute inset-x-0 bottom-0 h-40 bg-gradient-to-t from-primary/20 to-transparent blur-3xl" />
          
          <h1
            className="text-[18vw] font-black tracking-tighter text-primary opacity-30 leading-none whitespace-nowrap translate-y-1/3 blur-2xl sm:blur-3xl filter transition-all duration-700"
            style={{
              textShadow: "0 0 100px var(--primary)",
            }}
          >
            Mangatarem
          </h1>
        </div>
      </footer>
    </div>
  );
}
