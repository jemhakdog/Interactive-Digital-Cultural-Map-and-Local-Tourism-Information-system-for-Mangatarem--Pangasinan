"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { useAuth } from "@/lib/auth";
import { fetchAPI } from "@/lib/api";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import {
  Loader2,
  MapPin,
  Calendar,
  Building2,
  Users,
  ArrowRight,
  Shield,
  CalendarCheck,
  Star,
  BadgeCheck,
  Landmark,
  FileText,
  Mail,
  ClipboardList,
  BarChart3,
  Megaphone,
  Images,
  PlusCircle,
  AlertTriangle,
  ExternalLink,
  Map,
  Compass,
  CheckCircle2,
  Layers,
} from "lucide-react";

interface AdminStats {
  attractions: number;
  events: number;
  businesses: number;
  users: number;
  pendingMerchants: number;
  pendingReviews: number;
}

export default function AdminPage() {
  const { user, loading: authLoading } = useAuth();
  const router = useRouter();
  const [stats, setStats] = useState<AdminStats | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!authLoading && (!user || user.role !== "admin")) {
      router.push("/dashboard");
    }
  }, [user, authLoading, router]);

  useEffect(() => {
    if (!user || user.role !== "admin") return;

    Promise.allSettled([
      fetchAPI("/api/attractions").then((d) => (d as { items?: unknown[] }).items?.length ?? 0),
      fetchAPI("/api/events").then((d) => (d as { items?: unknown[] }).items?.length ?? 0),
      fetchAPI("/api/business").then((d) => (d as { items?: unknown[] }).items?.length ?? 0),
      fetchAPI<{ total: number }>("/api/admin/users?per_page=1").then((d) => d.total).catch(() => 0),
      fetchAPI<{ merchants?: unknown[] }>("/api/admin/merchants/pending").then((d) => d.merchants?.length ?? 0).catch(() => 0),
      fetchAPI<{ reviews?: Array<{ status?: string }> }>("/api/admin/reviews")
        .then((d) => d.reviews?.filter((r) => r.status === "pending").length ?? 0)
        .catch(() => 0),
    ])
      .then(([attractionsRes, eventsRes, businessRes, usersRes, merchantsRes, reviewsRes]) => {
        setStats({
          attractions: attractionsRes.status === "fulfilled" ? attractionsRes.value : 0,
          events: eventsRes.status === "fulfilled" ? eventsRes.value : 0,
          businesses: businessRes.status === "fulfilled" ? businessRes.value : 0,
          users: usersRes.status === "fulfilled" ? usersRes.value : 0,
          pendingMerchants: merchantsRes.status === "fulfilled" ? merchantsRes.value : 0,
          pendingReviews: reviewsRes.status === "fulfilled" ? reviewsRes.value : 0,
        });
      })
      .catch(() => {})
      .finally(() => setLoading(false));
  }, [user]);

  if (authLoading || !user || loading) {
    return (
      <div className="flex min-h-[60vh] items-center justify-center py-16">
        <div className="flex flex-col items-center gap-3">
          <Loader2 className="h-8 w-8 animate-spin text-primary" />
          <p className="text-sm text-muted-foreground animate-pulse">Loading Admin Command Center...</p>
        </div>
      </div>
    );
  }

  const currentDateFormatted = new Intl.DateTimeFormat("en-US", {
    weekday: "long",
    year: "numeric",
    month: "long",
    day: "numeric",
  }).format(new Date());

  const kpiCards = [
    {
      label: "Attractions",
      value: stats?.attractions ?? 0,
      icon: MapPin,
      href: "/admin/attractions",
      color: "text-emerald-600 dark:text-emerald-400",
      bgColor: "bg-emerald-500/10 border-emerald-500/20",
      description: "Cultural & eco-tourism sites",
      tag: "Active Sites",
    },
    {
      label: "Events & Festivals",
      value: stats?.events ?? 0,
      icon: Calendar,
      href: "/admin/events",
      color: "text-blue-600 dark:text-blue-400",
      bgColor: "bg-blue-500/10 border-blue-500/20",
      description: "Town activities & schedules",
      tag: "Calendar",
    },
    {
      label: "Local Businesses",
      value: stats?.businesses ?? 0,
      icon: Building2,
      href: "/admin/establishments",
      color: "text-amber-600 dark:text-amber-400",
      bgColor: "bg-amber-500/10 border-amber-500/20",
      description: "Merchants & accommodations",
      tag: "Directory",
    },
    {
      label: "Platform Users",
      value: stats?.users ?? 0,
      icon: Users,
      href: "/admin/users",
      color: "text-indigo-600 dark:text-indigo-400",
      bgColor: "bg-indigo-500/10 border-indigo-500/20",
      description: "Stewards, tourists & admins",
      tag: "Accounts",
    },
  ];

  const adminCategories = [
    {
      title: "Core Tourism & Heritage",
      description: "Manage destinations, cultural heritage, town events, and media assets",
      items: [
        {
          href: "/admin/attractions",
          label: "Attractions Management",
          description: "Eco-parks, springs, waterfalls & viewpoints",
          icon: MapPin,
          badge: `${stats?.attractions ?? 0} sites`,
          color: "text-emerald-600 dark:text-emerald-400 bg-emerald-500/10",
        },
        {
          href: "/admin/events",
          label: "Events & Festivals",
          description: "Schedules, town fiestas, & community gatherings",
          icon: Calendar,
          badge: `${stats?.events ?? 0} events`,
          color: "text-blue-600 dark:text-blue-400 bg-blue-500/10",
        },
        {
          href: "/admin/heritage",
          label: "Heritage & Culture",
          description: "Historical landmarks, churches, & culinary traditions",
          icon: Landmark,
          color: "text-amber-600 dark:text-amber-400 bg-amber-500/10",
        },
        {
          href: "/admin/establishments",
          label: "Establishments & Dining",
          description: "Local restaurants, homestays, & craft shops",
          icon: Building2,
          badge: `${stats?.businesses ?? 0} venues`,
          color: "text-teal-600 dark:text-teal-400 bg-teal-500/10",
        },
        {
          href: "/admin/barangays",
          label: "Barangay Profiles",
          description: "Local sector information and boundary details",
          icon: Layers,
          color: "text-cyan-600 dark:text-cyan-400 bg-cyan-500/10",
        },
        {
          href: "/admin/gallery",
          label: "Media Gallery",
          description: "High-resolution curated photos and media banners",
          icon: Images,
          color: "text-pink-600 dark:text-pink-400 bg-pink-500/10",
        },
      ],
    },
    {
      title: "Content & Moderation",
      description: "Review visitor feedback, publish announcements, and manage municipal documents",
      items: [
        {
          href: "/admin/reviews",
          label: "Review Moderation",
          description: "Approve or flag visitor ratings and feedback",
          icon: Star,
          alert: (stats?.pendingReviews ?? 0) > 0 ? `${stats?.pendingReviews} Pending` : undefined,
          color: "text-amber-600 dark:text-amber-400 bg-amber-500/10",
        },
        {
          href: "/admin/announcements",
          label: "Public Announcements",
          description: "Town advisories, road updates, and tourism news",
          icon: Megaphone,
          color: "text-orange-600 dark:text-orange-400 bg-orange-500/10",
        },
        {
          href: "/admin/documents",
          label: "Documents & Ordinances",
          description: "Official tourism policies, permits, and guides",
          icon: FileText,
          color: "text-slate-600 dark:text-slate-400 bg-slate-500/10",
        },
        {
          href: "/admin/newsletter",
          label: "Newsletter Subscribers",
          description: "Mailing lists and promotional bulletin digests",
          icon: Mail,
          color: "text-blue-600 dark:text-blue-400 bg-blue-500/10",
        },
      ],
    },
    {
      title: "Operations & Governance",
      description: "Merchant credentials, steward check-ins, bookings, and user roles",
      items: [
        {
          href: "/admin/verify-merchants",
          label: "Verify Merchants",
          description: "Review business permits and merchant accreditation",
          icon: BadgeCheck,
          alert: (stats?.pendingMerchants ?? 0) > 0 ? `${stats?.pendingMerchants} Pending` : undefined,
          color: "text-emerald-600 dark:text-emerald-400 bg-emerald-500/10",
        },
        {
          href: "/admin/bookings",
          label: "Manage Bookings",
          description: "Facility reservations, tour packages & slots",
          icon: CalendarCheck,
          color: "text-indigo-600 dark:text-indigo-400 bg-indigo-500/10",
        },
        {
          href: "/admin/visitor-registry",
          label: "Visitor Registry Log",
          description: "On-site logs registered by site stewards and kiosks",
          icon: ClipboardList,
          color: "text-teal-600 dark:text-teal-400 bg-teal-500/10",
        },
        {
          href: "/admin/users",
          label: "User Management",
          description: "Manage accounts, roles, and administrative privileges",
          icon: Users,
          badge: `${stats?.users ?? 0} users`,
          color: "text-violet-600 dark:text-violet-400 bg-violet-500/10",
        },
      ],
    },
    {
      title: "Analytics & Footprint",
      description: "Data-driven tourism metrics, crowd monitoring, and reports",
      items: [
        {
          href: "/admin/visits",
          label: "Visitor Traffic & Footprint",
          description: "Location popularity, date trends, and CSV data export",
          icon: Map,
          color: "text-emerald-600 dark:text-emerald-400 bg-emerald-500/10",
        },
        {
          href: "/admin/analytics",
          label: "Comprehensive Analytics",
          description: "In-depth telemetry, check-in conversion, and charts",
          icon: BarChart3,
          color: "text-blue-600 dark:text-blue-400 bg-blue-500/10",
        },
      ],
    },
  ];

  const hasPendingItems = (stats?.pendingMerchants ?? 0) > 0 || (stats?.pendingReviews ?? 0) > 0;

  return (
    <div className="container mx-auto px-4 py-8 max-w-6xl space-y-8">
      {/* Hero Welcome & Command Center Header */}
      <div className="relative overflow-hidden rounded-3xl border border-border/60 bg-gradient-to-br from-primary/10 via-background to-secondary/20 p-6 md:p-8 shadow-sm">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-6 relative z-10">
          <div className="space-y-2">
            <div className="flex flex-wrap items-center gap-2">
              <Badge variant="outline" className="bg-background/80 backdrop-blur border-primary/30 text-primary px-3 py-1 font-semibold text-xs rounded-full">
                <Shield className="h-3.5 w-3.5 mr-1.5 inline" /> Admin Command Center
              </Badge>
              <span className="text-xs text-muted-foreground font-medium hidden sm:inline-block">
                • {currentDateFormatted}
              </span>
            </div>
            <h1 className="text-3xl md:text-4xl font-extrabold tracking-tight text-foreground">
              Mangatarem Tourism Admin
            </h1>
            <p className="text-muted-foreground text-sm md:text-base max-w-2xl">
              Welcome back, <span className="font-semibold text-foreground">{user.name || user.email}</span>. Manage destinations, review merchant submissions, and monitor tourist traffic across all barangays.
            </p>
          </div>

          {/* Header Quick Actions */}
          <div className="flex flex-wrap items-center gap-2.5">
            <Link href="/admin/attractions/new">
              <Button size="sm" className="rounded-xl shadow-sm gap-2 font-medium cursor-pointer">
                <PlusCircle className="h-4 w-4" /> Add Attraction
              </Button>
            </Link>
            <Link href="/admin/events/new">
              <Button size="sm" variant="secondary" className="rounded-xl shadow-sm gap-2 font-medium cursor-pointer">
                <Calendar className="h-4 w-4" /> New Event
              </Button>
            </Link>
            <Link href="/map" target="_blank">
              <Button size="sm" variant="outline" className="rounded-xl gap-2 font-medium cursor-pointer">
                <Compass className="h-4 w-4" /> Live Map <ExternalLink className="h-3 w-3 opacity-60" />
              </Button>
            </Link>
          </div>
        </div>

        {/* Subtle background decoration */}
        <div className="absolute -right-12 -bottom-12 w-64 h-64 bg-primary/5 rounded-full blur-3xl pointer-events-none" />
      </div>

      {/* Pending Items Attention Banner */}
      {hasPendingItems && (
        <div className="rounded-2xl border border-amber-500/30 bg-amber-500/10 p-4 md:p-5 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
          <div className="flex items-center gap-3.5">
            <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-amber-500/20 text-amber-600 dark:text-amber-400">
              <AlertTriangle className="h-5 w-5" />
            </div>
            <div>
              <h3 className="text-sm font-bold text-foreground">Items Awaiting Admin Action</h3>
              <p className="text-xs text-muted-foreground">
                {(stats?.pendingMerchants ?? 0) > 0 && `${stats?.pendingMerchants} merchant application(s) pending review. `}
                {(stats?.pendingReviews ?? 0) > 0 && `${stats?.pendingReviews} visitor review(s) pending moderation.`}
              </p>
            </div>
          </div>
          <div className="flex items-center gap-2">
            {(stats?.pendingMerchants ?? 0) > 0 && (
              <Link href="/admin/verify-merchants">
                <Button size="sm" variant="outline" className="rounded-xl border-amber-500/30 bg-background text-xs font-semibold cursor-pointer">
                  Verify Merchants ({stats?.pendingMerchants})
                </Button>
              </Link>
            )}
            {(stats?.pendingReviews ?? 0) > 0 && (
              <Link href="/admin/reviews">
                <Button size="sm" variant="outline" className="rounded-xl border-amber-500/30 bg-background text-xs font-semibold cursor-pointer">
                  Moderate Reviews ({stats?.pendingReviews})
                </Button>
              </Link>
            )}
          </div>
        </div>
      )}

      {/* Key Metric KPI Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {kpiCards.map((c) => (
          <Link key={c.label} href={c.href}>
            <Card className="group border-border/60 hover:shadow-md hover:border-primary/30 transition-all duration-200 cursor-pointer h-full">
              <CardContent className="p-5 flex flex-col justify-between h-full space-y-4">
                <div className="flex items-center justify-between">
                  <div className={`flex h-11 w-11 shrink-0 items-center justify-center rounded-2xl ${c.bgColor} ${c.color} group-hover:scale-105 transition-transform`}>
                    <c.icon className="h-5 w-5" />
                  </div>
                  <Badge variant="secondary" className="text-[11px] font-semibold px-2 py-0.5 rounded-md">
                    {c.tag}
                  </Badge>
                </div>
                <div>
                  <p className="text-3xl font-extrabold tracking-tight text-foreground">{c.value}</p>
                  <p className="text-sm font-semibold text-foreground/90 mt-0.5">{c.label}</p>
                  <p className="text-xs text-muted-foreground mt-0.5">{c.description}</p>
                </div>
              </CardContent>
            </Card>
          </Link>
        ))}
      </div>

      {/* Structured Category Sections */}
      <div className="space-y-8">
        {adminCategories.map((category) => (
          <div key={category.title} className="space-y-3.5">
            <div className="border-b border-border/50 pb-2">
              <h2 className="text-xl font-bold tracking-tight text-foreground">{category.title}</h2>
              <p className="text-xs text-muted-foreground">{category.description}</p>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3.5">
              {category.items.map((item) => (
                <Link key={item.href} href={item.href} className="group">
                  <div className="h-full rounded-2xl border border-border/50 bg-card p-4 transition-all duration-200 hover:border-primary/30 hover:bg-accent/40 hover:shadow-sm cursor-pointer flex flex-col justify-between space-y-3">
                    <div className="flex items-start justify-between gap-3">
                      <div className="flex items-center gap-3">
                        <div className={`flex h-10 w-10 shrink-0 items-center justify-center rounded-xl ${item.color} group-hover:scale-105 transition-transform`}>
                          <item.icon className="h-5 w-5" />
                        </div>
                        <div>
                          <div className="flex items-center gap-2">
                            <h3 className="text-sm font-bold text-foreground group-hover:text-primary transition-colors">
                              {item.label}
                            </h3>
                          </div>
                          <p className="text-xs text-muted-foreground line-clamp-1 mt-0.5">
                            {item.description}
                          </p>
                        </div>
                      </div>
                    </div>

                    <div className="flex items-center justify-between pt-1 border-t border-border/30">
                      <div className="flex items-center gap-2">
                        {item.badge && (
                          <span className="text-[11px] font-medium text-muted-foreground bg-muted px-2 py-0.5 rounded-md">
                            {item.badge}
                          </span>
                        )}
                        {item.alert && (
                          <Badge variant="destructive" className="text-[10px] font-bold px-2 py-0.5 rounded-full animate-pulse">
                            {item.alert}
                          </Badge>
                        )}
                      </div>
                      <span className="text-xs font-semibold text-muted-foreground group-hover:text-primary flex items-center gap-1 transition-colors">
                        Manage <ArrowRight className="h-3.5 w-3.5 transition-transform group-hover:translate-x-1" />
                      </span>
                    </div>
                  </div>
                </Link>
              ))}
            </div>
          </div>
        ))}
      </div>

      {/* Quick Portal Health & Footer Info */}
      <div className="rounded-2xl border border-border/50 bg-muted/30 p-5 flex flex-col md:flex-row items-center justify-between gap-4 text-xs text-muted-foreground">
        <div className="flex items-center gap-3">
          <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-emerald-500/10 text-emerald-600 dark:text-emerald-400">
            <CheckCircle2 className="h-4 w-4" />
          </div>
          <div>
            <p className="font-semibold text-foreground">Interactive Digital Cultural Map Platform</p>
            <p>Municipality of Mangatarem, Pangasinan • Tourism & Cultural Office</p>
          </div>
        </div>
        <div className="flex items-center gap-4">
          <Link href="/explore" className="hover:text-foreground underline-offset-4 hover:underline">
            Public Tourism Portal
          </Link>
          <span>•</span>
          <Link href="/map" className="hover:text-foreground underline-offset-4 hover:underline">
            Interactive Map
          </Link>
          <span>•</span>
          <Link href="/admin/documents" className="hover:text-foreground underline-offset-4 hover:underline">
            Tourism Registry Guides
          </Link>
        </div>
      </div>
    </div>
  );
}

