"use client";

import { useEffect, useState } from "react";
import { fetchAPI } from "@/lib/api";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Label } from "@/components/ui/label";
import { Loader2, Crosshair } from "lucide-react";
import type { Attraction } from "./types";

const CATEGORIES = ["Nature", "Historical", "Religious", "Adventure", "Culture"];
const CATEGORY_LABELS: Record<string, string> = {
  Nature: "Nature & Parks",
  Historical: "Historical Landmark",
  Religious: "Religious Site",
  Adventure: "Adventure & Recreation",
  Culture: "Cultural Center",
};

interface FormState {
  name: string;
  category: string;
  description: string;
  directions: string;
  image_url: string;
  latitude: string;
  longitude: string;
}

const EMPTY: FormState = {
  name: "",
  category: "Nature",
  description: "",
  directions: "",
  image_url: "",
  latitude: "",
  longitude: "",
};

export function AttractionForm({ id }: { id?: string }) {
  const [form, setForm] = useState<FormState>(EMPTY);
  const [loading, setLoading] = useState(Boolean(id));
  const [submitting, setSubmitting] = useState(false);
  const [message, setMessage] = useState<{ type: "success" | "error"; text: string } | null>(null);

  useEffect(() => {
    if (!id) return;
    let cancelled = false;
    (async () => {
      try {
        const data = await fetchAPI<Attraction>(`/api/attractions/${id}`);
        if (!cancelled && data) {
          setForm({
            name: data.name ?? "",
            category: data.category ?? "Nature",
            description: data.description ?? "",
            directions: data.directions ?? "",
            image_url: data.image_url ?? "",
            latitude: data.latitude != null ? String(data.latitude) : "",
            longitude: data.longitude != null ? String(data.longitude) : "",
          });
        }
      } catch {
        // TODO: FastAPI endpoint not implemented yet — using local placeholder state.
      } finally {
        if (!cancelled) setLoading(false);
      }
    })();
    return () => {
      cancelled = true;
    };
  }, [id]);

  function update(key: keyof FormState, value: string) {
    setForm((f) => ({ ...f, [key]: value }));
  }

  function useMyLocation() {
    if (typeof navigator === "undefined" || !navigator.geolocation) return;
    navigator.geolocation.getCurrentPosition(
      (pos) =>
        setForm((f) => ({
          ...f,
          latitude: pos.coords.latitude.toFixed(6),
          longitude: pos.coords.longitude.toFixed(6),
        })),
      () => {}
    );
  }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setSubmitting(true);
    setMessage(null);
    const payload = {
      name: form.name,
      category: form.category,
      description: form.description,
      directions: form.directions,
      image_url: form.image_url || undefined,
      latitude: form.latitude ? Number(form.latitude) : null,
      longitude: form.longitude ? Number(form.longitude) : null,
    };
    try {
      // TODO: FastAPI endpoint not implemented yet — contributor CRUD missing.
      if (id) {
        await fetchAPI(`/api/contributor/attractions/${id}`, {
          method: "PUT",
          body: JSON.stringify(payload),
        });
      } else {
        await fetchAPI(`/api/contributor/attractions`, {
          method: "POST",
          body: JSON.stringify(payload),
        });
      }
      setMessage({
        type: "success",
        text: id ? "Landmark updated and queued for review." : "Landmark submitted for review.",
      });
    } catch {
      setMessage({
        type: "error",
        text: "Backend submission endpoint not available yet. Kept as a local draft.",
      });
    } finally {
      setSubmitting(false);
    }
  }

  if (loading)
    return (
      <div className="flex justify-center py-12">
        <Loader2 className="h-6 w-6 animate-spin text-muted-foreground" />
      </div>
    );

  return (
    <form onSubmit={handleSubmit} className="space-y-6 bg-card border border-border rounded-2xl p-6 lg:p-8">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="space-y-2">
          <Label htmlFor="name">Landmark Name</Label>
          <Input
            id="name"
            value={form.name}
            onChange={(e) => update("name", e.target.value)}
            required
            placeholder="e.g. Mangatarem Historic Plaza"
          />
        </div>
        <div className="space-y-2">
          <Label htmlFor="category">Category</Label>
          <select
            id="category"
            value={form.category}
            onChange={(e) => update("category", e.target.value)}
            required
            className="h-8 w-full rounded-lg border border-input bg-transparent px-2.5 text-sm outline-none focus-visible:border-ring focus-visible:ring-3 focus-visible:ring-ring/50"
          >
            {CATEGORIES.map((c) => (
              <option key={c} value={c}>
                {CATEGORY_LABELS[c]}
              </option>
            ))}
          </select>
        </div>
        <div className="md:col-span-2 space-y-2">
          <Label htmlFor="description">Narrative Description</Label>
          <Textarea
            id="description"
            value={form.description}
            onChange={(e) => update("description", e.target.value)}
            rows={5}
            required
            placeholder="Detail the historical values, folklores, and characteristics of this asset..."
          />
        </div>
        <div className="md:col-span-2 space-y-2">
          <Label htmlFor="directions">Directions &amp; Travel Guide</Label>
          <Textarea
            id="directions"
            value={form.directions}
            onChange={(e) => update("directions", e.target.value)}
            rows={3}
            placeholder="Provide transit instructions, road markers, or local reference landmarks..."
          />
        </div>
        <div className="space-y-2">
          <Label htmlFor="latitude">Latitude</Label>
          <Input
            id="latitude"
            type="number"
            step="any"
            value={form.latitude}
            onChange={(e) => update("latitude", e.target.value)}
            required
            placeholder="15.7xxx"
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
            required
            placeholder="120.2xxx"
          />
        </div>
        <div className="md:col-span-2 flex justify-end">
          <Button type="button" variant="outline" size="sm" onClick={useMyLocation} className="gap-1.5 rounded-lg">
            <Crosshair className="h-4 w-4" /> Pinpoint My Location
          </Button>
        </div>
        <div className="md:col-span-2 space-y-2">
          <Label htmlFor="image_url">Image URL</Label>
          <Input
            id="image_url"
            type="url"
            value={form.image_url}
            onChange={(e) => update("image_url", e.target.value)}
            placeholder="https://domain.com/image.jpg"
          />
        </div>
      </div>

      {message && (
        <div
          className={`rounded-lg px-4 py-3 text-sm ${
            message.type === "success" ? "bg-primary/10 text-primary" : "bg-destructive/10 text-destructive"
          }`}
        >
          {message.text}
        </div>
      )}

      <div className="flex justify-end gap-3 pt-2">
        <Button type="submit" disabled={submitting} className="gap-1.5">
          {submitting && <Loader2 className="h-4 w-4 animate-spin" />}
          {id ? "Save Changes" : "Submit Landmark"}
        </Button>
      </div>
    </form>
  );
}
