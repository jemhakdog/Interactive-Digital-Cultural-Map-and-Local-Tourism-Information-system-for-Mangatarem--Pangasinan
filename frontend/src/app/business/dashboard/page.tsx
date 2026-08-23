"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { useAuth } from "@/lib/auth";
import { fetchAPI } from "@/lib/api";
import { EstablishmentItem } from "@/app/business/business-view";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Label } from "@/components/ui/label";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { BusinessLayout } from "@/components/business/business-layout";
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
  Pencil,
  CheckCircle2,
} from "lucide-react";

export default function BusinessDashboardPage() {
  const { user } = useAuth();

  const [establishment, setEstablishment] = useState<(EstablishmentItem & { status?: string }) | null>(null);
  const [roomCount, setRoomCount] = useState<number | null>(null);
  const [menuCount, setMenuCount] = useState<number | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!user || user.role !== "business_owner") return;

    // Locate the owner's establishment via the public list
    const load = async () => {
      try {
        const data = await fetchAPI<{ establishments?: EstablishmentItem[] }>(
          "/api/business?per_page=100"
        );
        const mine =
          (data.establishments ?? []).find(
            (e) => (e as EstablishmentItem & { owner_id?: number }).owner_id === user.id
          ) ?? null;
        setEstablishment(mine);
      } catch {
        setEstablishment(null);
      }

      // Owner-scoped inventory
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

  const isDining = establishment?.type && ["restaurant", "cafe", "fastfood"].includes(establishment.type);
  const primaryText = isDining ? "text-orange-600 dark:text-orange-400" : "text-primary";

  return (
    <BusinessLayout>
      {loading ? (
        <div className="flex justify-center py-20">
          <Loader2 className="h-8 w-8 animate-spin text-primary" />
        </div>
      ) : !establishment ? (
        /* ── Onboarding empty state (no establishment yet) ── */
        <div className="container mx-auto px-4 py-12 max-w-3xl">
          <div className="text-center bg-card border border-border/60 rounded-3xl shadow-xs p-10 space-y-5">
            <div className="inline-flex items-center justify-center w-20 h-20 rounded-2xl bg-primary/10 text-primary">
              <Store className="h-10 w-10" />
            </div>
            <h1 className="text-2xl font-bold tracking-tight text-foreground">
              Set up your Mangatarem business profile
            </h1>
            <p className="text-sm text-muted-foreground max-w-md mx-auto leading-relaxed">
              Register your inn, restaurant, café, or shop details. Once submitted, your profile
              will be sent to the Mangatarem municipal administrator for review and approval.
            </p>
            <div className="pt-2 flex flex-col sm:flex-row items-center justify-center gap-3">
              <CreateEstablishmentModal onCreated={() => window.location.reload()} />
              <Link href="/business">
                <Button variant="outline" className="gap-2 rounded-xl">
                  Browse Directory
                </Button>
              </Link>
            </div>
          </div>
        </div>
      ) : (
        <div className="container mx-auto px-4 py-8 max-w-6xl space-y-8">
          {/* Header */}
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-6 border-b border-border/50">
            <div>
              <div className="flex items-center gap-2">
                <h1 className="text-2xl font-bold tracking-tight text-foreground">
                  {isDining ? "🍽️ Culinary Management Hub" : establishment.type === "inn" ? "🏨 Hospitality Partner Command" : "💼 Business Partner Portal"}
                </h1>
              </div>
              <p className="text-xs font-medium text-muted-foreground mt-1 uppercase tracking-wider">
                {isDining
                  ? "Promote menu listings, hours, and customer reviews"
                  : "Steward accommodation listings and visitor metrics"}
              </p>
            </div>
            <div className="flex items-center gap-2">
              <Badge variant="secondary" className="text-[10px] font-bold uppercase">
                Type: {establishment.type}
              </Badge>
              <Badge
                className={`text-[10px] font-bold uppercase ${
                  establishment.status === "approved"
                    ? "bg-emerald-500/10 text-emerald-600 dark:text-emerald-400"
                    : establishment.status === "pending"
                    ? "bg-amber-500/10 text-amber-600"
                    : "bg-destructive/10 text-destructive"
                }`}
              >
                Status: {establishment.status || "active"}
              </Badge>
            </div>
          </div>

          {/* Pending banners */}
          {establishment.status === "pending" && (
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
            <Card className="border-border/50">
              <CardContent className="p-5 flex flex-col justify-between">
                <span className="text-[10px] font-bold uppercase tracking-wider text-muted-foreground">
                  Average Rating
                </span>
                <div className="flex items-baseline gap-2 mt-4">
                  <span className="text-3xl font-bold text-foreground">
                    {establishment.rating_avg && establishment.rating_avg > 0 ? establishment.rating_avg.toFixed(1) : "0.0"}
                  </span>
                  <span className="text-xs font-semibold text-muted-foreground">
                    {establishment.rating_avg && establishment.rating_avg > 0 ? "★ Rating" : "No reviews"}
                  </span>
                </div>
              </CardContent>
            </Card>

            <Card className="border-border/50">
              <CardContent className="p-5 flex flex-col justify-between">
                <span className="text-[10px] font-bold uppercase tracking-wider text-muted-foreground">
                  {isDining ? "Active Menu Dishes" : "Rooms / Lodgings"}
                </span>
                <div className="flex items-baseline gap-2 mt-4">
                  <span className="text-3xl font-bold text-foreground">
                    {String(isDining ? menuCount ?? 0 : roomCount ?? 0)}
                  </span>
                  <span className="text-xs font-semibold text-muted-foreground">Managed items</span>
                </div>
              </CardContent>
            </Card>

            <Card className="border-border/50">
              <CardContent className="p-5 flex flex-col justify-between">
                <span className="text-[10px] font-bold uppercase tracking-wider text-muted-foreground">
                  Total Reviews
                </span>
                <div className="flex items-baseline gap-2 mt-4">
                  <span className="text-3xl font-bold text-foreground">
                    {String(establishment.review_count ?? 0)}
                  </span>
                  <span className="text-xs font-semibold text-muted-foreground">Visitor feedbacks</span>
                </div>
              </CardContent>
            </Card>

            <Card className="border-border/50">
              <CardContent className="p-5 flex flex-col justify-between">
                <span className="text-[10px] font-bold uppercase tracking-wider text-muted-foreground">
                  Verification
                </span>
                <div className="flex items-baseline gap-2 mt-4">
                  <span className="text-3xl font-bold text-foreground">
                    {establishment.status === "approved" ? "Approved" : "Pending"}
                  </span>
                  <span className="text-xs font-semibold text-muted-foreground">Active state</span>
                </div>
              </CardContent>
            </Card>
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
                      {establishment.type === "inn" ? "🏨 Lodging" : "🍽️ Dining"} Establishment
                    </span>
                    <h2 className="text-lg font-bold text-foreground mt-1">{establishment.name}</h2>
                    {establishment.address && (
                      <p className="text-xs font-medium text-muted-foreground mt-1 flex items-center gap-1">
                        <MapPin className="h-3.5 w-3.5 text-primary" /> {establishment.address}
                      </p>
                    )}
                  </div>
                  <Link href={`/business/${establishment.id}/edit`}>
                    <Button variant="outline" size="sm" className="gap-1.5 rounded-xl shrink-0">
                      <Pencil className="h-3.5 w-3.5" /> Edit Profile
                    </Button>
                  </Link>
                </div>
                {establishment.description && (
                  <p className="text-xs font-medium text-muted-foreground mt-4 leading-relaxed border-t border-border/40 pt-4">
                    {establishment.description}
                  </p>
                )}
              </div>
              <div className="bg-muted/40 border-t border-border/40 p-6 grid grid-cols-2 sm:grid-cols-4 gap-4 text-center">
                <div>
                  <p className="text-[9px] font-bold text-muted-foreground uppercase tracking-widest">Phone</p>
                  <p className="text-xs font-semibold text-foreground mt-1 truncate">{establishment.contact_number || "—"}</p>
                </div>
                <div>
                  <p className="text-[9px] font-bold text-muted-foreground uppercase tracking-widest">Email</p>
                  <p className="text-xs font-semibold text-foreground mt-1 truncate">{establishment.email || "—"}</p>
                </div>
                <div>
                  <p className="text-[9px] font-bold text-muted-foreground uppercase tracking-widest">Price</p>
                  <p className="text-xs font-semibold text-foreground mt-1 uppercase">{establishment.price_range || "₱₱"}</p>
                </div>
                <div>
                  <p className="text-[9px] font-bold text-muted-foreground uppercase tracking-widest">Barangay</p>
                  <p className="text-xs font-semibold text-foreground mt-1 truncate">{establishment.barangay_name || establishment.barangay || "—"}</p>
                </div>
              </div>
            </Card>

            <div className="space-y-4">
              {establishment.type === "inn" ? (
                <Link href={`/business/${establishment.id}/rooms`}>
                  <ActionCard icon={Hotel} title="Manage Rooms" desc={`${roomCount ?? 0} rooms configured`} />
                </Link>
              ) : (
                <Link href={`/business/${establishment.id}/menu`}>
                  <ActionCard icon={Utensils} title="Manage Menu" desc={`${menuCount ?? 0} dishes configured`} />
                </Link>
              )}
              <Link href={`/business/${establishment.id}/reviews`}>
                <ActionCard icon={MessageSquare} title="Customer Feedbacks" desc={`${establishment.review_count ?? 0} active reviews`} />
              </Link>
              <Link href={`/business/${establishment.id}/verify`}>
                <ActionCard icon={ShieldCheck} title="Verification" desc="Submit business permits" />
              </Link>
              <Link href="/business/peers">
                <ActionCard icon={Users} title="Market Overview" desc="Browse local peers" />
              </Link>
            </div>
          </div>
        </div>
      )}
    </BusinessLayout>
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

function CreateEstablishmentModal({ onCreated }: { onCreated: () => void }) {
  const [open, setOpen] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState(false);

  const [name, setName] = useState("");
  const [type, setType] = useState("restaurant");
  const [description, setDescription] = useState("");
  const [address, setAddress] = useState("");
  const [barangayName, setBarangayName] = useState("");
  const [priceRange, setPriceRange] = useState("moderate");
  const [contactNumber, setContactNumber] = useState("");
  const [email, setEmail] = useState("");
  const [website, setWebsite] = useState("");
  const [barangays, setBarangays] = useState<string[]>([]);

  useEffect(() => {
    const loadBarangays = async () => {
      try {
        const list = await fetchAPI<{ establishments?: { barangay_name?: string | null }[] }>(
          "/api/business?per_page=100"
        );
        const names = Array.from(
          new Set((list.establishments ?? []).map((e) => e.barangay_name).filter(Boolean) as string[])
        );
        setBarangays(names);
      } catch {
        setBarangays([]);
      }
    };
    loadBarangays();
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError("");

    try {
      await fetchAPI("/api/business", {
        method: "POST",
        body: JSON.stringify({
          name,
          type,
          description: description || undefined,
          address: address || undefined,
          barangay_name: barangayName || undefined,
          price_range: priceRange || undefined,
          contact_number: contactNumber || undefined,
          email: email || undefined,
          website: website || undefined,
        }),
      });

      setSuccess(true);
      setTimeout(() => {
        setOpen(false);
        onCreated();
      }, 1500);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to create establishment profile.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger
        render={
          <Button className="gap-2 rounded-xl">
            <PlusCircle className="h-4 w-4" /> Setup Business Profile
          </Button>
        }
      />
      <DialogContent className="sm:max-w-lg max-h-[90vh] overflow-y-auto rounded-3xl">
        <DialogHeader>
          <DialogTitle className="text-xl font-bold">Setup Business Profile</DialogTitle>
          <DialogDescription className="text-xs">
            Submit your establishment details to the Mangatarem Tourism Office for admin approval.
          </DialogDescription>
        </DialogHeader>

        {success ? (
          <div className="py-8 text-center space-y-3">
            <CheckCircle2 className="h-12 w-12 text-primary mx-auto" />
            <h4 className="text-base font-bold">Profile Submitted!</h4>
            <p className="text-xs text-muted-foreground max-w-xs mx-auto">
              Your establishment profile is pending approval. You can now manage your details.
            </p>
          </div>
        ) : (
          <form onSubmit={handleSubmit} className="space-y-4 py-2">
            {error && (
              <div className="bg-destructive/10 border border-destructive/20 text-destructive text-xs p-3 rounded-xl">
                {error}
              </div>
            )}

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div className="space-y-1.5">
                <Label htmlFor="biz-name" className="text-xs font-semibold">
                  Business Name *
                </Label>
                <Input
                  id="biz-name"
                  placeholder="e.g. Mangatarem Bistro"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  required
                  className="rounded-xl h-9 text-xs"
                />
              </div>

              <div className="space-y-1.5">
                <Label htmlFor="biz-type" className="text-xs font-semibold">
                  Category *
                </Label>
                <select
                  id="biz-type"
                  value={type}
                  onChange={(e) => setType(e.target.value)}
                  className="h-9 w-full rounded-xl border border-border bg-card px-3 text-xs text-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary"
                >
                  <option value="restaurant">Restaurant</option>
                  <option value="cafe">Cafe / Coffee Shop</option>
                  <option value="fastfood">Fast Food</option>
                  <option value="inn">Inn / Lodging</option>
                  <option value="resort">Resort / Eco-Park</option>
                  <option value="shop">Retail / Souvenir Shop</option>
                  <option value="other">Other Service</option>
                </select>
              </div>
            </div>

            <div className="space-y-1.5">
              <Label htmlFor="biz-desc" className="text-xs font-semibold">
                Overview & Description
              </Label>
              <Textarea
                id="biz-desc"
                placeholder="Describe your hospitality services, specialty dishes, ambiance, or amenities..."
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                rows={3}
                className="rounded-xl text-xs"
              />
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div className="space-y-1.5">
                <Label htmlFor="biz-addr" className="text-xs font-semibold">
                  Street Address
                </Label>
                <Input
                  id="biz-addr"
                  placeholder="e.g. National Highway, Poblacion"
                  value={address}
                  onChange={(e) => setAddress(e.target.value)}
                  className="rounded-xl h-9 text-xs"
                />
              </div>

              <div className="space-y-1.5">
                <Label htmlFor="biz-brgy" className="text-xs font-semibold">
                  Barangay
                </Label>
                <select
                  id="biz-brgy"
                  value={barangayName}
                  onChange={(e) => setBarangayName(e.target.value)}
                  className="h-9 w-full rounded-xl border border-border bg-card px-3 text-xs text-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary"
                >
                  <option value="">Select Barangay</option>
                  {barangays.map((b) => (
                    <option key={b} value={b}>
                      {b}
                    </option>
                  ))}
                </select>
              </div>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div className="space-y-1.5">
                <Label htmlFor="biz-phone" className="text-xs font-semibold">
                  Contact Number
                </Label>
                <Input
                  id="biz-phone"
                  placeholder="0917-123-4567"
                  value={contactNumber}
                  onChange={(e) => setContactNumber(e.target.value)}
                  className="rounded-xl h-9 text-xs"
                />
              </div>

              <div className="space-y-1.5">
                <Label htmlFor="biz-price" className="text-xs font-semibold">
                  Price Tier
                </Label>
                <select
                  id="biz-price"
                  value={priceRange}
                  onChange={(e) => setPriceRange(e.target.value)}
                  className="h-9 w-full rounded-xl border border-border bg-card px-3 text-xs text-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary"
                >
                  <option value="budget">₱ Budget Friendly</option>
                  <option value="moderate">₱₱ Moderate Range</option>
                  <option value="luxury">₱₱₱ Premium / Luxury</option>
                </select>
              </div>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div className="space-y-1.5">
                <Label htmlFor="biz-email" className="text-xs font-semibold">
                  Business Email
                </Label>
                <Input
                  id="biz-email"
                  type="email"
                  placeholder="contact@business.com"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="rounded-xl h-9 text-xs"
                />
              </div>

              <div className="space-y-1.5">
                <Label htmlFor="biz-website" className="text-xs font-semibold">
                  Website / Social Page
                </Label>
                <Input
                  id="biz-website"
                  placeholder="https://facebook.com/mybusiness"
                  value={website}
                  onChange={(e) => setWebsite(e.target.value)}
                  className="rounded-xl h-9 text-xs"
                />
              </div>
            </div>

            <Button type="submit" disabled={loading} className="w-full rounded-xl mt-4">
              {loading ? <Loader2 className="h-4 w-4 animate-spin mr-2" /> : <PlusCircle className="h-4 w-4 mr-2" />}
              {loading ? "Submitting for Approval..." : "Submit Establishment Profile"}
            </Button>
          </form>
        )}
      </DialogContent>
    </Dialog>
  );
}
