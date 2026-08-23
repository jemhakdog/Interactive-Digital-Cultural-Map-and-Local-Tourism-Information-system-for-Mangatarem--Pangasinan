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
import { BusinessLayout } from "@/components/business/business-layout";
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
  const { user } = useAuth();

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
    if (!user || user.role !== "business_owner") return;

    const load = async () => {
      try {
        const data = await fetchAPI<{ establishment?: OwnerEstablishment }>(
          `/api/business/${id}`
        );
        const item = data.establishment;
        if (item) {
          setEst(item);
          setName(item.name || "");
          setType(item.type || "restaurant");
          setDescription(item.description || "");
          setAddress(item.address || "");
          setBarangay(item.barangay_name || item.barangay || "");
          setPriceRange(item.price_range || "moderate");
          setContactNumber(item.contact_number || "");
          setEmail(item.email || "");
          setWebsite(item.website || "");
          setLatitude(item.latitude != null ? String(item.latitude) : "");
          setLongitude(item.longitude != null ? String(item.longitude) : "");
        } else {
          setNotFound(true);
        }
      } catch {
        setNotFound(true);
      } finally {
        setLoading(false);
      }

      // Barangay options
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
    load();
  }, [user, id]);

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

  return (
    <BusinessLayout>
      {loading ? (
        <div className="flex justify-center py-20">
          <Loader2 className="h-8 w-8 animate-spin text-primary" />
        </div>
      ) : notFound ? (
        <div className="container mx-auto px-4 py-12 max-w-2xl">
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
      ) : (
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
                Edit Establishment Profile
              </h1>
              <p className="text-xs text-muted-foreground">
                Update operational details, descriptions, contacts, and coordinates.
              </p>
            </div>
            {est?.status && (
              <Badge variant="secondary" className="uppercase text-[10px] font-bold">
                {est.status}
              </Badge>
            )}
          </div>

          <form onSubmit={handleSubmit} className="space-y-8 bg-card border border-border/60 rounded-3xl p-6 md:p-8">
            {/* Basic Info */}
            <div className="space-y-4">
              <h2 className="text-xs font-bold uppercase text-muted-foreground tracking-wider border-b border-border/40 pb-3">
                Core Information
              </h2>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="space-y-1.5">
                  <Label className="text-[11px] font-bold uppercase text-muted-foreground tracking-wider">
                    Business Name *
                  </Label>
                  <Input value={name} onChange={(e) => setName(e.target.value)} required className="rounded-xl" />
                </div>
                <div className="space-y-1.5">
                  <Label className="text-[11px] font-bold uppercase text-muted-foreground tracking-wider">
                    Establishment Type *
                  </Label>
                  <select
                    value={type}
                    onChange={(e) => setType(e.target.value)}
                    className="h-10 w-full rounded-xl border border-border bg-card px-3 text-sm text-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary"
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
                <Label className="text-[11px] font-bold uppercase text-muted-foreground tracking-wider">Description</Label>
                <Textarea
                  value={description}
                  onChange={(e) => setDescription(e.target.value)}
                  rows={4}
                  className="rounded-xl"
                  placeholder="Share a brief overview of your products, ambiance, specialties, and experience..."
                />
              </div>
            </div>

            {/* Location */}
            <div className="space-y-4">
              <h2 className="text-xs font-bold uppercase text-muted-foreground tracking-wider border-b border-border/40 pb-3">
                Location &amp; Coordinates
              </h2>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="space-y-1.5">
                  <Label className="text-[11px] font-bold uppercase text-muted-foreground tracking-wider">Street / Sitio Address</Label>
                  <Input value={address} onChange={(e) => setAddress(e.target.value)} className="rounded-xl" />
                </div>
                <div className="space-y-1.5">
                  <Label className="text-[11px] font-bold uppercase text-muted-foreground tracking-wider">Barangay</Label>
                  <select
                    value={barangay}
                    onChange={(e) => setBarangay(e.target.value)}
                    className="h-10 w-full rounded-xl border border-border bg-card px-3 text-sm text-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary"
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

              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="space-y-1.5">
                  <Label className="text-[11px] font-bold uppercase text-muted-foreground tracking-wider">Latitude (WGS84)</Label>
                  <Input value={latitude} onChange={(e) => setLatitude(e.target.value)} placeholder="15.789..." className="rounded-xl" />
                </div>
                <div className="space-y-1.5">
                  <Label className="text-[11px] font-bold uppercase text-muted-foreground tracking-wider">Longitude (WGS84)</Label>
                  <Input value={longitude} onChange={(e) => setLongitude(e.target.value)} placeholder="120.294..." className="rounded-xl" />
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
      )}
    </BusinessLayout>
  );
}
