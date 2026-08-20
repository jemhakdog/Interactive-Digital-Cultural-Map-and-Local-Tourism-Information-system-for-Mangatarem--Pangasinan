"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { fetchAPI } from "@/lib/api";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";
import { Loader2 } from "lucide-react";

export interface HeritageFormValues {
  name: string;
  description?: string;
  status?: string;
  category?: string;
  location?: string;
}

export function HeritageForm({
  type,
  id,
  initial,
}: {
  type: string;
  id?: number;
  initial?: Partial<HeritageFormValues>;
}) {
  const router = useRouter();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [form, setForm] = useState({
    name: initial?.name ?? "",
    description: initial?.description ?? "",
    status: initial?.status ?? "pending",
    category: initial?.category ?? "",
    location: initial?.location ?? "",
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
      status: form.status,
      category: form.category || undefined,
      location: form.location || undefined,
    };
    try {
      if (id) {
        await fetchAPI(`/api/heritage/${type}/${id}`, {
          method: "PUT",
          body: JSON.stringify(payload),
        });
      } else {
        await fetchAPI(`/api/heritage/${type}`, {
          method: "POST",
          body: JSON.stringify(payload),
        });
      }
      router.push("/admin/heritage");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to save heritage record");
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div className="space-y-2">
        <Label htmlFor="name">Name / Title *</Label>
        <Input
          id="name"
          value={form.name}
          onChange={(e) => update("name", e.target.value)}
          required
        />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="space-y-2">
          <Label htmlFor="category">Category / Subcategory</Label>
          <Input
            id="category"
            value={form.category}
            onChange={(e) => update("category", e.target.value)}
            placeholder="e.g. Natural, Built, Intangible"
          />
        </div>
        <div className="space-y-2">
          <Label htmlFor="location">Location</Label>
          <Input
            id="location"
            value={form.location}
            onChange={(e) => update("location", e.target.value)}
            placeholder="e.g. Brgy. Bogsongan"
          />
        </div>
      </div>

      <div className="space-y-2">
        <Label htmlFor="status">Status</Label>
        <select
          id="status"
          value={form.status}
          onChange={(e) => update("status", e.target.value)}
          className="w-full rounded-lg border border-border bg-background px-3 py-2 text-sm text-foreground outline-none focus:ring-2 focus:ring-primary/40"
        >
          <option value="pending">Pending</option>
          <option value="approved">Approved</option>
        </select>
      </div>

      <div className="space-y-2">
        <Label htmlFor="description">Description</Label>
        <Textarea
          id="description"
          rows={5}
          value={form.description}
          onChange={(e) => update("description", e.target.value)}
        />
      </div>

      {error && <p className="text-sm text-destructive">{error}</p>}

      <div className="flex justify-end gap-2 pt-2">
        <Button
          type="button"
          variant="outline"
          onClick={() => router.push("/admin/heritage")}
          disabled={loading}
        >
          Cancel
        </Button>
        <Button type="submit" disabled={loading}>
          {loading && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
          {id ? "Update Record" : "Save to Archive"}
        </Button>
      </div>
    </form>
  );
}
