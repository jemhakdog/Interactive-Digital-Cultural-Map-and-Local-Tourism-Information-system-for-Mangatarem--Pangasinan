"use client";

import { useEffect, useState } from "react";
import { useAuth } from "@/lib/auth";
import { fetchAPI } from "@/lib/api";
import { useRouter } from "next/navigation";
import { Loader2, MapPin, Pencil, Check, X, Landmark } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";

interface Barangay {
  id: number;
  name: string;
  mission?: string | null;
  vision?: string | null;
  history?: string | null;
  attractions_count: number;
  has_geo: boolean;
}

const FIELDS = [
  { key: "mission", label: "Mission" },
  { key: "vision", label: "Vision" },
  { key: "history", label: "History" },
] as const;

export default function AdminBarangaysPage() {
  const { user, loading: authLoading } = useAuth();
  const router = useRouter();
  const [items, setItems] = useState<Barangay[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [editing, setEditing] = useState<Barangay | null>(null);
  const [form, setForm] = useState({ mission: "", vision: "", history: "" });
  const [saving, setSaving] = useState(false);

  const load = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await fetchAPI<{ barangays: Barangay[] }>("/api/admin/barangays");
      setItems(data.barangays);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load barangays.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (!authLoading && (!user || user.role !== "admin")) router.push("/dashboard");
  }, [user, authLoading, router]);

  useEffect(() => {
    if (!user || user.role !== "admin") return;
    load();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [user]);

  const openEdit = (b: Barangay) => {
    setEditing(b);
    setForm({
      mission: b.mission ?? "",
      vision: b.vision ?? "",
      history: b.history ?? "",
    });
  };

  const save = async () => {
    if (!editing) return;
    setSaving(true);
    try {
      await fetchAPI(`/api/admin/barangays/${editing.id}`, {
        method: "PUT",
        body: JSON.stringify(form),
      });
      setEditing(null);
      await load();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to save barangay.");
    } finally {
      setSaving(false);
    }
  };

  if (authLoading || !user || loading) {
    return (
      <div className="flex justify-center py-16">
        <Loader2 className="h-6 w-6 animate-spin text-muted-foreground" />
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8 max-w-5xl space-y-6">
      <div className="flex items-center gap-3">
        <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-primary/10 text-primary">
          <Landmark className="h-5 w-5" />
        </div>
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Barangays</h1>
          <p className="text-muted-foreground text-sm mt-0.5">
            Edit mission, vision, and history profiles for each barangay
          </p>
        </div>
      </div>

      {error && <p className="text-sm text-destructive">{error}</p>}

      {items.length === 0 ? (
        <div className="border border-dashed border-border rounded-2xl py-20 text-center">
          <MapPin className="h-12 w-12 mx-auto mb-3 text-muted-foreground/40" />
          <p className="font-bold text-foreground">No barangays</p>
          <p className="text-xs text-muted-foreground mt-1">No barangay records exist yet.</p>
        </div>
      ) : (
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Name</TableHead>
              <TableHead>Attractions</TableHead>
              <TableHead>Profile completeness</TableHead>
              <TableHead className="text-right">Actions</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {items.map((b) => {
              const filled = FIELDS.filter((f) => (b[f.key] ?? "").trim()).length;
              return (
                <TableRow key={b.id}>
                  <TableCell className="font-bold">{b.name}</TableCell>
                  <TableCell>{b.attractions_count}</TableCell>
                  <TableCell>
                    <Badge variant="outline" className="text-[8px] font-black uppercase tracking-wider">
                      {filled}/{FIELDS.length} sections
                    </Badge>
                    {b.has_geo && (
                      <Badge variant="outline" className="ml-1.5 text-[8px] font-black uppercase tracking-wider">
                        geo
                      </Badge>
                    )}
                  </TableCell>
                  <TableCell className="text-right">
                    <Button size="sm" variant="outline" className="gap-1 rounded-lg" onClick={() => openEdit(b)}>
                      <Pencil className="h-3.5 w-3.5" /> Edit
                    </Button>
                  </TableCell>
                </TableRow>
              );
            })}
          </TableBody>
        </Table>
      )}

      <Dialog open={editing !== null} onOpenChange={(open) => !open && setEditing(null)}>
        <DialogContent className="max-w-lg">
          <DialogHeader>
            <DialogTitle>Edit {editing?.name}</DialogTitle>
          </DialogHeader>
          <div className="space-y-4">
            {FIELDS.map((f) => (
              <div key={f.key} className="space-y-2">
                <Label htmlFor={`brgy-${f.key}`}>{f.label}</Label>
                <Textarea
                  id={`brgy-${f.key}`}
                  rows={4}
                  value={form[f.key]}
                  onChange={(e) => setForm({ ...form, [f.key]: e.target.value })}
                />
              </div>
            ))}
            <div className="flex justify-end gap-2 pt-2">
              <Button variant="outline" onClick={() => setEditing(null)}><X className="h-4 w-4" /> Cancel</Button>
              <Button onClick={save} disabled={saving} className="gap-1.5">
                {saving ? <Loader2 className="h-4 w-4 animate-spin" /> : <Check className="h-4 w-4" />}
                Save changes
              </Button>
            </div>
          </div>
        </DialogContent>
      </Dialog>
    </div>
  );
}
