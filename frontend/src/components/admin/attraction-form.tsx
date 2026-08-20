"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { fetchAPI } from "@/lib/api";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";
import { Loader2 } from "lucide-react";

export interface AttractionFormValues {
  name: string;
  description?: string;
  category?: string;
  latitude?: string;
  longitude?: string;
  barangay_name?: string;
}

export function AttractionForm({
  id,
  initial,
}: {
  id?: number;
  initial?: Partial<AttractionFormValues>;
}) {
  const router = useRouter();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [form, setForm] = useState({
    name: initial?.name ?? "",
    description: initial?.description ?? "",
    category: initial?.category ?? "",
    latitude: initial?.latitude ?? "",
    longitude: initial?.longitude ?? "",
    barangay_name: initial?.barangay_name ?? "",
  });

  const update = (key: keyof typeof form, value: string) =>
    setForm((f) => ({ ...f, [key]: value }));

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    const payload = {
      name: form.name,
      description: form.description,
      category: form.category,
      latitude: form.latitude ? parseFloat(form.latitude) : null,
      longitude: form.longitude ? parseFloat(form.longitude) : null,
      barangay_name: form.barangay_name || null,
    };
    try {
      if (id) {
        await fetchAPI(`/api/attractions/${id}`, {
          method: "PUT",
          body: JSON.stringify(payload),
        });
      } else {
        await fetchAPI("/api/attractions", {
          method: "POST",
          body: JSON.stringify(payload),
        });
      }
      router.push("/admin/attractions");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to save attraction");
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div className="space-y-2">
        <Label htmlFor="name">Name *</Label>
        <Input
          id="name"
          value={form.name}
          onChange={(e) => update("name", e.target.value)}
          required
        />
      </div>

      <div className="space-y-2">
        <Label htmlFor="description">Description</Label>
        <Textarea
          id="description"
          rows={4}
          value={form.description}
          onChange={(e) => update("description", e.target.value)}
        />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="space-y-2">
          <Label htmlFor="category">Category</Label>
          <Input
            id="category"
            value={form.category}
            onChange={(e) => update("category", e.target.value)}
            placeholder="e.g. Nature, Heritage, Religious"
          />
        </div>
        <div className="space-y-2">
          <Label htmlFor="barangay_name">Barangay</Label>
          <Input
            id="barangay_name"
            value={form.barangay_name}
            onChange={(e) => update("barangay_name", e.target.value)}
            placeholder="e.g. Poblacion"
          />
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="space-y-2">
          <Label htmlFor="latitude">Latitude</Label>
          <Input
            id="latitude"
            type="number"
            step="any"
            value={form.latitude}
            onChange={(e) => update("latitude", e.target.value)}
            placeholder="15.7890"
          />
        </div>
        <div className="space-y-2">
          <Label htmlFor="longitude">Longitude</Label>
          <Input
            id="longitude"
            type="number"
            step="any"
            value={form.longitude}
            onChange={(e) => update("longitude", e.target.value)}
            placeholder="120.2890"
          />
        </div>
      </div>

      {error && <p className="text-sm text-destructive">{error}</p>}

      <div className="flex justify-end gap-2 pt-2">
        <Button
          type="button"
          variant="outline"
          onClick={() => router.push("/admin/attractions")}
          disabled={loading}
        >
          Cancel
        </Button>
        <Button type="submit" disabled={loading}>
          {loading && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
          {id ? "Update Attraction" : "Save Attraction"}
        </Button>
      </div>
    </form>
  );
}
