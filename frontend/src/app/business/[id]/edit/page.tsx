"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { useParams } from "next/navigation";
import { useAuth } from "@/lib/auth";
import { fetchAPI } from "@/lib/api";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Label } from "@/components/ui/label";
import { Badge } from "@/components/ui/badge";
import { Loader2, ArrowLeft, Save, CheckCircle2 } from "lucide-react";

interface OwnerEstablishment {
  id: number;
  name?: string;
  type?: string;
  description?: string | null;
  address?: string | null;
  latitude?: number | null;
  longitude?: number | null;
  contact_number?: string | null;
  email?: string | null;
  website?: string | null;
  price_range?: string | null;
  barangay?: string | null;
  barangay_name?: string | null;
  status?: string;
}

export default function EditEstablishmentPage() {
  const params = useParams<{ id: string }>();
  const id = params.id;
  const { user, loading: authLoading } = useAuth();

  const [est, setEst] = useState<OwnerEstablishment | null>(null);
  const [loading, setLoading] = useState(true);
  const [notFound, setNotFound] = useState(false);
  const [barangays, setBarangays] = useState<string[]>([]);
  const [saving, setSaving] = useState(false);
  const [saved, setSaved] = useState(false);
  const [error, setError] = useState("");

  // Local form state
  const [name, setName] = useState("");
  const [type, setType] = useState("restaurant");
  const [description, setDescription] = useState("");
  const [address, setAddress] = useState("");
  const [barangay, setBarangay] = useState("");
  const [priceRange, setPriceRange] = useState("moderate");
  const [contactNumber, setContactNumber] = useState("");
  const [email, setEmail] = useState("");
  const [website, setWebsite] = useState("");
  const [latitude, setLatitude] = useState("");
  const [longitude, setLongitude] = useState("");

  useEffect(() => {
    if (authLoading || !user) return;
    const load = async () => {
      try {
        const data = await fetchAPI<{ establishment: OwnerEstablishment }>(
          `/api/business/${id}`
        );
        const e = data.establishment;
        setEst(e);
        setName(e.name ?? "");
        setType(e.type ?? "restaurant");
        setDescription(e.description ?? "");
        setAddress(e.address ?? "");
        setBarangay(e.barangay_name ?? e.barangay ?? "");
        setPriceRange(e.price_range ?? "moderate");
        setContactNumber(e.contact_number ?? "");
        setEmail(e.email ?? "");
        setWebsite(e.website ?? "");
        setLatitude(e.latitude != null ? String(e.latitude) : "");
        setLongitude(e.longitude != null ? String(e.longitude) : "");
      } catch {
        // TODO: owner detail fetch only returns approved establishments; pending
        // owners cannot load their draft yet.
        setNotFound(true);
      } finally {
        setLoading(false);
      }

      // Barangay options (no dedicated /api/barangay endpoint yet).
      try {
        const list = await fetchAPI<{ establishments?: { barangay_name?: string | null }[] }>(
          "/api/business?per_page=200"
        );
        const names = Array.from(
          new Set((list.establishments ?? []).map((e) => e.barangay_name).filter(Boolean) as string[])
        );
        setBarangays(names);
      } catch {
        setBarangays([]);
      }
    };
    load();
  }, [user, authLoading, id]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSaving(true);
    setError("");
    setSaved(false);
    try {
      const body: Record<string, unknown> = {
        name,
        type,
        description,
        address,
        barangay_name: barangay || null,
        price_range: priceRange,
        contact_number: contactNumber || null,
        email: email || null,
        website: website || null,
      };
      if (latitude) body.latitude = parseFloat(latitude);
      if (longitude) body.longitude = parseFloat(longitude);
      await fetchAPI(`/api/business/${id}`, { method: "PUT", body: JSON.stringify(body) });
      setSaved(true);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to save changes.");
    } finally {
      setSaving(false);
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center py-16">
        <Loader2 className="h-6 w-6 animate-spin text-muted-foreground" />
      </div>
    );
  }

  if (notFound) {
    return (
      <div className="container mx-auto px-4 py-8 max-w-2xl">
        <div className="text-center bg-card border border-border/60 rounded-3xl p-10 space-y-3">
          <h1 className="text-xl font-bold text-foreground">Establishment not available</h1>
          <p className="text-sm text-muted-foreground">
            This listing could not be loaded. It may still be pending administrative verification.
          </p>
          <Link href="/business/dashboard">
            <Button variant="outline" className="rounded-xl mt-2">Back to Dashboard</Button>
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8 max-w-4xl space-y-8">
      <div className="flex items-center justify-between pb-4 border-b border-border/50">
        <div className="space-y-1">
          <Link
            href="/business/dashboard"
            className="text-xs font-bold uppercase tracking-wider text-muted-foreground hover:text-foreground flex items-center gap-1.5 transition-colors"
          >
            <ArrowLeft className="h-3.5 w-3.5" /> Back to Dashboard
          </Link>
          <h1 className="text-xl font-bold tracking-tight text-foreground mt-2">
            Modify Establishment Listing
          </h1>
        </div>
        {est?.status && (
          <Badge variant="secondary" className="text-[10px] font-bold uppercase">
            Status: {est.status}
          </Badge>
        )}
      </div>

      <form onSubmit={handleSubmit} className="bg-card border border-border/60 rounded-3xl p-8 shadow-xs space-y-8">
        {/* Classification */}
        <div className="space-y-4">
          <h2 className="text-xs font-bold uppercase text-muted-foreground tracking-wider border-b border-border/40 pb-3">
            Classification &amp; Overview
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="space-y-1.5">
              <Label className="text-[11px] font-bold uppercase text-muted-foreground tracking-wider">Establishment Name *</Label>
              <Input value={name} onChange={(e) => setName(e.target.value)} required placeholder="e.g. Mangatarem Forest View Lodge" className="rounded-xl" />
            </div>
            <div className="space-y-1.5">
              <Label className="text-[11px] font-bold uppercase text-muted-foreground tracking-wider">Business Type *</Label>
              <select
                value={type}
                onChange={(e) => setType(e.target.value)}
                className="h-10 w-full rounded-xl border border-border bg-card px-3 text-sm text-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary"
              >
                <option value="inn">🏨 Inn / Accommodation Lodge</option>
                <option value="restaurant">🍽️ Restaurant &amp; Dining</option>
                <option value="cafe">☕ Local Brew Café</option>
                <option value="fastfood">🍔 Bistro Fastfood</option>
              </select>
            </div>
          </div>
          <div className="space-y-1.5">
            <Label className="text-[11px] font-bold uppercase text-muted-foreground tracking-wider">Public Description *</Label>
            <Textarea value={description} onChange={(e) => setDescription(e.target.value)} required rows={4} placeholder="Share the unique narrative of your establishment..." className="rounded-xl" />
          </div>
        </div>

        {/* Location */}
        <div className="space-y-4">
          <h2 className="text-xs font-bold uppercase text-muted-foreground tracking-wider border-b border-border/40 pb-3">
            Address &amp; Coordinates
          </h2>
          <div className="space-y-1.5">
            <Label className="text-[11px] font-bold uppercase text-muted-foreground tracking-wider">Street Address *</Label>
            <Input value={address} onChange={(e) => setAddress(e.target.value)} required placeholder="Brgy. Cabaran, Romulo Highway, Mangatarem, Pangasinan" className="rounded-xl" />
          </div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="space-y-1.5">
              <Label className="text-[11px] font-bold uppercase text-muted-foreground tracking-wider">Barangay</Label>
              <Input
                list="barangay-options"
                value={barangay}
                onChange={(e) => setBarangay(e.target.value)}
                placeholder="Select or type"
                className="rounded-xl"
              />
              <datalist id="barangay-options">
                {barangays.map((b) => (
                  <option key={b} value={b} />
                ))}
              </datalist>
            </div>
            <div className="space-y-1.5">
              <Label className="text-[11px] font-bold uppercase text-muted-foreground tracking-wider">Latitude</Label>
              <Input value={latitude} onChange={(e) => setLatitude(e.target.value)} placeholder="15.7000" className="rounded-xl" />
            </div>
            <div className="space-y-1.5">
              <Label className="text-[11px] font-bold uppercase text-muted-foreground tracking-wider">Longitude</Label>
              <Input value={longitude} onChange={(e) => setLongitude(e.target.value)} placeholder="120.4000" className="rounded-xl" />
            </div>
          </div>
        </div>

        {/* Contact */}
        <div className="space-y-4">
          <h2 className="text-xs font-bold uppercase text-muted-foreground tracking-wider border-b border-border/40 pb-3">
            Contact &amp; Pricing
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="space-y-1.5">
              <Label className="text-[11px] font-bold uppercase text-muted-foreground tracking-wider">Contact Number</Label>
              <Input value={contactNumber} onChange={(e) => setContactNumber(e.target.value)} className="rounded-xl" />
            </div>
            <div className="space-y-1.5">
              <Label className="text-[11px] font-bold uppercase text-muted-foreground tracking-wider">Email</Label>
              <Input value={email} onChange={(e) => setEmail(e.target.value)} type="email" className="rounded-xl" />
            </div>
            <div className="space-y-1.5">
              <Label className="text-[11px] font-bold uppercase text-muted-foreground tracking-wider">Website</Label>
              <Input value={website} onChange={(e) => setWebsite(e.target.value)} className="rounded-xl" />
            </div>
            <div className="space-y-1.5">
              <Label className="text-[11px] font-bold uppercase text-muted-foreground tracking-wider">Price Range</Label>
              <select
                value={priceRange}
                onChange={(e) => setPriceRange(e.target.value)}
                className="h-10 w-full rounded-xl border border-border bg-card px-3 text-sm text-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary"
              >
                <option value="budget">₱ Budget</option>
                <option value="moderate">₱₱ Moderate</option>
                <option value="luxury">₱₱₱ Luxury</option>
              </select>
            </div>
          </div>
        </div>

        {saved && (
          <div className="flex items-center gap-2 text-xs font-semibold text-emerald-600 bg-emerald-500/10 border border-emerald-500/20 rounded-xl p-3">
            <CheckCircle2 className="h-4 w-4" /> Changes saved successfully.
          </div>
        )}
        {error && <p className="text-xs font-semibold text-destructive">{error}</p>}

        <Button type="submit" disabled={saving} className="w-full gap-2 rounded-xl">
          {saving ? <Loader2 className="h-4 w-4 animate-spin" /> : <Save className="h-4 w-4" />}
          {saving ? "Saving..." : "Save Changes"}
        </Button>
      </form>
    </div>
  );
}
