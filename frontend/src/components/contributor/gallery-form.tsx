"use client";

import { useEffect, useState } from "react";
import { fetchAPI } from "@/lib/api";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Label } from "@/components/ui/label";
import { Loader2 } from "lucide-react";
import type { GalleryItem } from "./types";

interface FormState {
  type: string;
  url: string;
  caption: string;
}

const EMPTY: FormState = { type: "photo", url: "", caption: "" };

export function GalleryForm({ id }: { id?: string }) {
  const [form, setForm] = useState<FormState>(EMPTY);
  const [preview, setPreview] = useState<string | null>(null);
  const [loading, setLoading] = useState(Boolean(id));
  const [submitting, setSubmitting] = useState(false);
  const [message, setMessage] = useState<{ type: "success" | "error"; text: string } | null>(null);

  useEffect(() => {
    if (!id) return;
    let cancelled = false;
    (async () => {
      try {
        // TODO: FastAPI endpoint not implemented yet — using local placeholder state.
        const data = await fetchAPI<GalleryItem>(`/api/contributor/gallery/${id}`);
        if (!cancelled && data) {
          setForm({ type: data.type ?? "photo", url: data.url ?? "", caption: data.caption ?? "" });
          setPreview(data.url ?? null);
        }
      } catch {
        /* keep placeholder */
      } finally {
        if (!cancelled) setLoading(false);
      }
    })();
    return () => {
      cancelled = true;
    };
  }, [id]);

  function onFile(e: React.ChangeEvent<HTMLInputElement>) {
    const file = e.target.files?.[0];
    if (!file) return;
    const url = URL.createObjectURL(file);
    setPreview(url);
    setForm((f) => ({ ...f, url, type: file.type.startsWith("video") ? "video" : "photo" }));
  }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setSubmitting(true);
    setMessage(null);
    const payload = {
      type: form.type,
      url: form.url || undefined,
      caption: form.caption || undefined,
    };
    try {
      // TODO: FastAPI endpoint not implemented yet — contributor CRUD missing.
      if (id) {
        await fetchAPI(`/api/contributor/gallery/${id}`, {
          method: "PUT",
          body: JSON.stringify(payload),
        });
      } else {
        await fetchAPI(`/api/contributor/gallery`, {
          method: "POST",
          body: JSON.stringify(payload),
        });
      }
      setMessage({
        type: "success",
        text: id ? "Media item updated." : "Media item uploaded (pending review).",
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
      <div className="space-y-2 max-w-sm">
        <Label htmlFor="type">Media Type</Label>
        <select
          id="type"
          value={form.type}
          onChange={(e) => setForm((f) => ({ ...f, type: e.target.value }))}
          required
          className="h-8 w-full rounded-lg border border-input bg-transparent px-2.5 text-sm outline-none focus-visible:border-ring focus-visible:ring-3 focus-visible:ring-ring/50"
        >
          <option value="photo">Photo</option>
          <option value="video">Video</option>
        </select>
      </div>

      <div className="space-y-2">
        <Label htmlFor="media">Select Local Media File</Label>
        <Input
          id="media"
          type="file"
          accept="image/*,video/*"
          onChange={onFile}
          className="file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border file:border-border file:text-xs file:font-medium file:bg-muted file:text-foreground"
        />
        {preview && (
          <div className="mt-3 max-w-md rounded-xl overflow-hidden border border-border bg-muted p-2">
            {form.type === "video" ? (
              <video src={preview} className="w-full h-48 object-cover rounded-lg" controls />
            ) : (
              <img src={preview} alt="" className="w-full h-48 object-cover rounded-lg" />
            )}
          </div>
        )}
      </div>

      <div className="space-y-2">
        <Label htmlFor="url">Or Provide Remote URL</Label>
        <Input
          id="url"
          type="url"
          value={form.url}
          onChange={(e) => {
            setForm((f) => ({ ...f, url: e.target.value }));
            setPreview(e.target.value || null);
          }}
          placeholder="https://domain.com/asset.png"
        />
      </div>

      <div className="space-y-2">
        <Label htmlFor="caption">Caption (Optional)</Label>
        <Textarea
          id="caption"
          value={form.caption}
          onChange={(e) => setForm((f) => ({ ...f, caption: e.target.value }))}
          rows={3}
          placeholder="Write a short background description or capture credits..."
        />
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
          {id ? "Save Changes" : "Upload Media Item"}
        </Button>
      </div>
    </form>
  );
}
