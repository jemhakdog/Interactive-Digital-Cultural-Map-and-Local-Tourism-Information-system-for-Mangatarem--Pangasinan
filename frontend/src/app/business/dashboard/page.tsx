"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useAuth } from "@/lib/auth";
import { fetchAPI } from "@/lib/api";
import { EstablishmentItem } from "@/app/business/business-view";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import {
  Loader2,
  Store,
  Hotel,
  Utensils,
  Star,
  MessageSquare,
  ShieldCheck,
  ArrowRight,
  Users,
  PlusCircle,
  MapPin,
} from "lucide-react";

export default function BusinessDashboardPage() {
  const { user, loading: authLoading } = useAuth();
  const router = useRouter();

  const [establishment, setEstablishment] = useState<(EstablishmentItem & { status?: string }) | null>(null);
  const [roomCount, setRoomCount] = useState<number | null>(null);
  const [menuCount, setMenuCount] = useState<number | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!authLoading && (!user || user.role !== "business_owner")) {
      router.push("/dashboard");
    }
  }, [user, authLoading, router]);

  useEffect(() => {
    if (!user || user.role !== "business_owner") return;

    // TODO: FastAPI has no "my establishment" endpoint — best-effort locate the
    // owner's establishment via the public list (works once approved).
    const load = async () => {
      try {
        const data = await fetchAPI<{ establishments?: EstablishmentItem[] }>(
          "/api/business?per_page=200"
        );
        const mine =
          (data.establishments ?? []).find(
            (e) => (e as EstablishmentItem & { owner_id?: number }).owner_id === user.id
          ) ?? null;
        setEstablishment(mine);
      } catch {
        setEstablishment(null);
      }

      // Owner-scoped inventory (works regardless of approval status).
      try {
        const rooms = await fetchAPI<{ rooms?: unknown[] }>("/api/business/rooms/list");
        setRoomCount((rooms.rooms ?? []).length);
      } catch {
        setRoomCount(0);
      }
      try {
        const menu = await fetchAPI<{ menu_items?: unknown[] }>("/api/business/menu/list");
        setMenuCount((menu.menu_items ?? []).length);
      } catch {
        setMenuCount(0);
      } finally {
        setLoading(false);
      }
    };

    load();
  }, [user]);

  if (authLoading || !user || user.role !== "business_owner") {
    return (
      <div className="flex justify-center py-16">
        <Loader2 className="h-6 w-6 animate-spin text-muted-foreground" />
      </div>
    );
  }

  const isDining = establishment?.type && ["restaurant", "cafe", "fastfood"].includes(establishment.type);
  const primaryText = isDining ? "text-orange-600 dark:text-orange-400" : "text-primary";

  // ── Onboarding empty state (no establishment yet) ──
  if (!establishment) {
    return (
      <div className="container mx-auto px-4 py-8 max-w-3xl">
        <div className="text-center bg-card border border-border/60 rounded-3xl shadow-xs p-10 space-y-5">
          <div className="inline-flex items-center justify-center w-20 h-20 rounded-2xl bg-primary/10 text-primary">
            <Store className="h-10 w-10" />
          </div>
          <h1 className="text-2xl font-bold tracking-tight text-foreground">
            Set up your Mangatarem business profile
          </h1>
          <p className="text-sm text-muted-foreground max-w-md mx-auto leading-relaxed">
            Publish your rooms, menu specials, or agro-tourism activities to visiting tourists.
            Once your listing is created and approved it will appear here.
          </p>
          <div className="pt-2 flex flex-col sm:flex-row items-center justify-center gap-3">
            <Link href="/business">
              <Button className="gap-2 rounded-xl">
                <PlusCircle className="h-4 w-4" /> Browse Business Directory
              </Button>
            </Link>
            <Link href="/dashboard">
              <Button variant="outline" className="rounded-xl">
                Back to Dashboard
              </Button>
            </Link>
          </div>
        </div>
      </div>
    );
  }

  const e = establishment;
  const statusBadge =
    e.status === "approved"
      ? "bg-emerald-500/10 text-emerald-600 dark:text-emerald-400"
      : e.status === "pending"
      ? "bg-amber-500/10 text-amber-600"
      : "bg-destructive/10 text-destructive";

  const stats = [
    {
      label: "Average Rating",
      value: e.rating_avg && e.rating_avg > 0 ? e.rating_avg.toFixed(1) : "0.0",
      sub: e.rating_avg && e.rating_avg > 0 ? "★ Rating" : "No reviews yet",
      icon: Star,
      color: "text-amber-500 bg-amber-500/10",
    },
    {
      label: isDining ? "Active Menu Dishes" : "Rooms / Lodgings",
      value: String(isDining ? menuCount ?? 0 : roomCount ?? 0),
      sub: "Managed items",
      icon: isDining ? Utensils : Hotel,
      color: "text-primary bg-primary/10",
    },
    {
      label: "Total Reviews",
      value: String(e.review_count ?? 0),
      sub: "Visitor feedbacks",
      icon: MessageSquare,
      color: "text-blue-500 bg-blue-500/10",
    },
    {
      label: "Verification",
      value: e.status === "approved" ? "Approved" : "Pending",
      sub: "Active state",
      icon: ShieldCheck,
      color: "text-emerald-500 bg-emerald-500/10",
    },
  ];

  return (
    <div className="container mx-auto px-4 py-8 max-w-6xl space-y-8">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-6 border-b border-border/50">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-foreground">
            {isDining ? "🍽️ Culinary Management Hub" : e.type === "inn" ? "🏨 Hospitality Partner Command" : "💼 Business Partner Portal"}
          </h1>
          <p className="text-xs font-medium text-muted-foreground mt-1 uppercase tracking-wider">
            {isDining
              ? "Promote menu listings, hours, and customer reviews"
              : "Steward accommodation listings and visitor metrics"}
          </p>
        </div>
        <div className="flex items-center gap-2">
          <Badge variant="secondary" className="text-[10px] font-bold uppercase">
            Type: {e.type}
          </Badge>
          <Badge className={`text-[10px] font-bold uppercase ${statusBadge}`}>
            Status: {e.status}
          </Badge>
        </div>
      </div>

      {/* Pending banners */}
      {e.status === "pending" && (
        <div className="bg-amber-500/10 border-l-4 border-amber-500 p-4 rounded-r-xl flex items-start gap-3">
          <ShieldCheck className="w-5 h-5 text-amber-600 shrink-0 mt-0.5" />
          <div>
            <h3 className="text-xs font-bold uppercase text-amber-800 dark:text-amber-300 tracking-wider">
              Listing awaiting administrative verification
            </h3>
            <p className="text-xs text-amber-700 dark:text-amber-400/80 mt-1">
              Your listing is under review by Mangatarem tourism administrators. Once verified it
              will appear on the interactive cultural map.
            </p>
          </div>
        </div>
      )}

      {/* Stats grid */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        {stats.map((s) => (
          <Card key={s.label} className="border-border/50">
            <CardContent className="p-5 flex flex-col justify-between">
              <span className="text-[10px] font-bold uppercase tracking-wider text-muted-foreground">
                {s.label}
              </span>
              <div className="flex items-baseline gap-2 mt-4">
                <span className="text-3xl font-bold text-foreground">{s.value}</span>
                <span className="text-xs font-semibold text-muted-foreground">{s.sub}</span>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Profile summary + actions */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <Card className="lg:col-span-2 border-border/60 overflow-hidden">
          <div className="h-32 bg-primary/10 flex items-end p-5">
            <span className="px-2.5 py-1 text-[9px] font-bold bg-background/80 text-foreground rounded border border-border/40 uppercase tracking-wider">
              Cover
            </span>
          </div>
          <div className="p-6">
            <div className="flex items-start justify-between gap-4">
              <div>
                <span className={`text-[10px] font-bold uppercase ${primaryText} tracking-widest`}>
                  {e.type === "inn" ? "🏨 Lodging" : "🍽️ Dining"} Establishment
                </span>
                <h2 className="text-lg font-bold text-foreground mt-1">{e.name}</h2>
                {e.address && (
                  <p className="text-xs font-medium text-muted-foreground mt-1 flex items-center gap-1">
                    <MapPin className="h-3.5 w-3.5 text-primary" /> {e.address}
                  </p>
                )}
              </div>
              <Link href={`/business/${e.id}/edit`}>
                <Button variant="outline" size="sm" className="gap-1.5 rounded-xl shrink-0">
                  Edit Profile
                </Button>
              </Link>
            </div>
            {e.description && (
              <p className="text-xs font-medium text-muted-foreground mt-4 leading-relaxed border-t border-border/40 pt-4">
                {e.description}
              </p>
            )}
          </div>
          <div className="bg-muted/40 border-t border-border/40 p-6 grid grid-cols-2 sm:grid-cols-4 gap-4 text-center">
            <div>
              <p className="text-[9px] font-bold text-muted-foreground uppercase tracking-widest">Phone</p>
              <p className="text-xs font-semibold text-foreground mt-1 truncate">{e.contact_number || "—"}</p>
            </div>
            <div>
              <p className="text-[9px] font-bold text-muted-foreground uppercase tracking-widest">Email</p>
              <p className="text-xs font-semibold text-foreground mt-1 truncate">{e.email || "—"}</p>
            </div>
            <div>
              <p className="text-[9px] font-bold text-muted-foreground uppercase tracking-widest">Price</p>
              <p className="text-xs font-semibold text-foreground mt-1 uppercase">{e.price_range || "₱₱"}</p>
            </div>
            <div>
              <p className="text-[9px] font-bold text-muted-foreground uppercase tracking-widest">Barangay</p>
              <p className="text-xs font-semibold text-foreground mt-1 truncate">{e.barangay_name || e.barangay || "—"}</p>
            </div>
          </div>
        </Card>

        <div className="space-y-4">
          {e.type === "inn" ? (
            <Link href={`/business/${e.id}/rooms`}>
              <ActionCard icon={Hotel} title="Manage Rooms" desc={`${roomCount ?? 0} rooms configured`} />
            </Link>
          ) : (
            <Link href={`/business/${e.id}/menu`}>
              <ActionCard icon={Utensils} title="Manage Menu" desc={`${menuCount ?? 0} dishes configured`} />
            </Link>
          )}
          <Link href={`/business/${e.id}/reviews`}>
            <ActionCard icon={MessageSquare} title="Customer Feedbacks" desc={`${e.review_count ?? 0} active reviews`} />
          </Link>
          <Link href={`/business/${e.id}/verify`}>
            <ActionCard icon={ShieldCheck} title="Verification" desc="Submit business permits" />
          </Link>
          <Link href="/business/peers">
            <ActionCard icon={Users} title="Market Overview" desc="Browse local peers" />
          </Link>
        </div>
      </div>
    </div>
  );
}

function ActionCard({
  icon: Icon,
  title,
  desc,
}: {
  icon: typeof Store;
  title: string;
  desc: string;
}) {
  return (
    <div className="group bg-card border border-border/50 rounded-2xl p-5 shadow-xs hover:border-primary/30 hover:shadow-md transition-all flex items-center justify-between">
      <div className="flex items-center gap-4">
        <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-primary/10 text-primary">
          <Icon className="h-5 w-5" />
        </div>
        <div>
          <h3 className="text-sm font-bold text-foreground group-hover:text-primary transition-colors">
            {title}
          </h3>
          <p className="text-xs font-medium text-muted-foreground mt-0.5">{desc}</p>
        </div>
      </div>
      <ArrowRight className="h-4 w-4 text-muted-foreground group-hover:translate-x-1 transition-transform" />
    </div>
  );
}
