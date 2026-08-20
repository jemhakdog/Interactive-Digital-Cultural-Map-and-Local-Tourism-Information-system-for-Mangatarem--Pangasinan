"use client";

import { useEffect, useState } from "react";
import { fetchAPI } from "@/lib/api";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Label } from "@/components/ui/label";
import { Loader2 } from "lucide-react";
import type { Announcement } from "./types";

interface FormState {
  title: string;
  content: string;
}

export function AnnouncementForm({ id }: { id?: string }) {
  const [form, setForm] = useState<FormState>({ title: "", content: "" });
  const [loading, setLoading] = useState(Boolean(id));
  const [submitting, setSubmitting] = useState(false);
  const [message, setMessage] = useState<{ type: "success" | "error"; text: string } | null>(null);

  useEffect(() => {
    if (!id) return;
    let cancelled = false;
    (async () => {
      try {
        // TODO: FastAPI endpoint not implemented yet — using local placeholder state.
        const data = await fetchAPI<Announcement>(`/api/contributor/announcements/${id}`);
        if (!cancelled) setForm({ title: data.title ?? "", content: data.content ?? "" });
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

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setSubmitting(true);
    setMessage(null);
    const payload = { title: form.title, content: form.content };
    try {
      // TODO: FastAPI endpoint not implemented yet — announcements router missing.
      if (id) {
        await fetchAPI(`/api/contributor/announcements/${id}`, {
          method: "PUT",
          body: JSON.stringify(payload),
        });
      } else {
        await fetchAPI(`/api/contributor/announcements`, {
          method: "POST",
          body: JSON.stringify(payload),
        });
      }
      setMessage({
        type: "success",
        text: id ? "Announcement updated." : "Announcement submitted for approval.",
      });
    } catch {
      setMessage({
        type: "error",
        text: "Backend endpoint not available yet. Kept as a local draft.",
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
      <div className="space-y-2">
        <Label htmlFor="title">Announcement Title</Label>
        <Input
          id="title"
          value={form.title}
          onChange={(e) => setForm((f) => ({ ...f, title: e.target.value }))}
          required
          minLength={5}
          maxLength={200}
          placeholder="e.g. Road Closure Notice or Community Trade Fair"
        />
        <p className="text-[11px] text-muted-foreground">Minimum 5 characters, maximum 200 characters.</p>
      </div>
      <div className="space-y-2">
        <Label htmlFor="content">Announcement Content</Label>
        <Textarea
          id="content"
          value={form.content}
          onChange={(e) => setForm((f) => ({ ...f, content: e.target.value }))}
          rows={8}
          required
          minLength={10}
          maxLength={5000}
          placeholder="Provide complete details about this announcement..."
        />
        <p className="text-[11px] text-muted-foreground">Minimum 10 characters, maximum 5000 characters.</p>
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
          {id ? "Update Announcement" : "Submit for Approval"}
        </Button>
      </div>
    </form>
  );
}
