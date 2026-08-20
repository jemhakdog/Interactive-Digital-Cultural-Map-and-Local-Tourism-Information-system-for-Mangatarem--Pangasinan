"use client";

import { useEffect, useState } from "react";
import { fetchAPI } from "@/lib/api";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Label } from "@/components/ui/label";
import { Loader2 } from "lucide-react";

interface ProfileState {
  mission: string;
  vision: string;
  history: string;
  cultural_assets: string;
  traditions: string;
  local_practices: string;
  unique_features: string;
}

const FIELDS: { key: keyof ProfileState; label: string; hint: string; rows: number }[] = [
  { key: "mission", label: "Mission Statement", hint: "Enter the official barangay mission statement.", rows: 4 },
  { key: "vision", label: "Vision Statement", hint: "Enter the official barangay vision statement.", rows: 4 },
  { key: "history", label: "History & Origin Description", hint: "Provide an academic summary of historical roots and local folklore.", rows: 6 },
  { key: "cultural_assets", label: "Cultural Assets Inventory", hint: "List significant local landmarks, structures, or artifacts.", rows: 4 },
  { key: "traditions", label: "Local Traditions & Customary Observances", hint: "Describe festivals, rituals, or annual celebrations.", rows: 4 },
  { key: "local_practices", label: "Livelihoods & Practices", hint: "Detail agricultural practices, crafts, or micro-businesses.", rows: 4 },
  { key: "unique_features", label: "Unique Community Characteristics", hint: "Detail landscapes, springs, or outstanding features.", rows: 4 },
];

const EMPTY: ProfileState = {
  mission: "",
  vision: "",
  history: "",
  cultural_assets: "",
  traditions: "",
  local_practices: "",
  unique_features: "",
};

export default function ContributorProfilePage() {
  const [form, setForm] = useState<ProfileState>(EMPTY);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [message, setMessage] = useState<{ type: "success" | "error"; text: string } | null>(null);

  useEffect(() => {
    let cancelled = false;
    (async () => {
      try {
        // TODO: FastAPI endpoint not implemented yet — barangay profile endpoint missing.
        const data = await fetchAPI<ProfileState>("/api/barangay");
        if (!cancelled && data) setForm({ ...EMPTY, ...data });
      } catch {
        /* keep placeholder */
      } finally {
        if (!cancelled) setLoading(false);
      }
    })();
    return () => {
      cancelled = true;
    };
  }, []);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setSubmitting(true);
    setMessage(null);
    try {
      // TODO: FastAPI endpoint not implemented yet — barangay profile endpoint missing.
      await fetchAPI("/api/barangay", { method: "PUT", body: JSON.stringify(form) });
      setMessage({ type: "success", text: "Barangay profile saved." });
    } catch {
      setMessage({ type: "error", text: "Backend endpoint not available yet. Kept as a local draft." });
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
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold tracking-tight">Manage Barangay Profile</h1>
        <p className="text-sm text-muted-foreground">CBIS Registry Profile</p>
      </div>
      <form onSubmit={handleSubmit} className="space-y-6 bg-card border border-border rounded-2xl p-6 lg:p-8">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {FIELDS.slice(0, 2).map((f) => (
            <div key={f.key} className="space-y-2">
              <Label htmlFor={f.key}>{f.label}</Label>
              <Textarea
                id={f.key}
                value={form[f.key]}
                onChange={(e) => setForm((s) => ({ ...s, [f.key]: e.target.value }))}
                rows={f.rows}
                placeholder={f.hint}
              />
            </div>
          ))}
        </div>
        {FIELDS.slice(2).map((f) => (
          <div key={f.key} className="space-y-2">
            <Label htmlFor={f.key}>{f.label}</Label>
            <p className="text-[11px] text-muted-foreground">{f.hint}</p>
            <Textarea
              id={f.key}
              value={form[f.key]}
              onChange={(e) => setForm((s) => ({ ...s, [f.key]: e.target.value }))}
              rows={f.rows}
              placeholder={f.hint}
            />
          </div>
        ))}

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
            Save Profile Settings
          </Button>
        </div>
      </form>
    </div>
  );
}
