"use client";

import { useEffect, useState, useCallback } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/lib/auth";
import { fetchAPI } from "@/lib/api";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Loader2, Plus, Pencil, Trash2, MapPin } from "lucide-react";
import { DeleteDialog, AttractionFormDialog } from "@/components/admin-dialogs";

interface Attraction {
  id: number;
  name: string;
  category: string;
  status: string;
  is_featured: boolean;
  barangay_name: string | null;
}

export default function AdminAttractionsPage() {
  const { user, loading: authLoading } = useAuth();
  const router = useRouter();
  const [attractions, setAttractions] = useState<Attraction[]>([]);
  const [loading, setLoading] = useState(true);
  const [deleteTarget, setDeleteTarget] = useState<Attraction | null>(null);
  const [editTarget, setEditTarget] = useState<Attraction | null>(null);
  const [addOpen, setAddOpen] = useState(false);

  const loadAttractions = useCallback(() => {
    return fetchAPI("/api/attractions")
      .then((data) => setAttractions((data as { items: Attraction[] }).items ?? []))
      .catch(() => {});
  }, []);

  useEffect(() => {
    if (!authLoading && (!user || user.role !== "admin")) router.push("/dashboard");
  }, [user, authLoading, router]);

  useEffect(() => {
    if (!user) return;
    loadAttractions().finally(() => setLoading(false));
  }, [user, loadAttractions]);

  const handleDelete = async () => {
    if (!deleteTarget) return;
    await fetchAPI(`/api/attractions/${deleteTarget.id}`, { method: "DELETE" });
    setAttractions((prev) => prev.filter((a) => a.id !== deleteTarget.id));
    setDeleteTarget(null);
  };

  const handleEdit = async (data: { name: string; description?: string; category?: string; latitude?: string; longitude?: string }) => {
    if (!editTarget) return;
    await fetchAPI(`/api/attractions/${editTarget.id}`, {
      method: "PUT",
      body: JSON.stringify({
        name: data.name,
        description: data.description ?? "",
        category: data.category ?? "",
        latitude: data.latitude ? parseFloat(data.latitude) : null,
        longitude: data.longitude ? parseFloat(data.longitude) : null,
      }),
    });
    loadAttractions();
    setEditTarget(null);
  };

  const handleAdd = async (data: { name: string; description?: string; category?: string; latitude?: string; longitude?: string }) => {
    await fetchAPI("/api/attractions", {
      method: "POST",
      body: JSON.stringify({
        name: data.name,
        description: data.description ?? "",
        category: data.category ?? "",
        latitude: data.latitude ? parseFloat(data.latitude) : null,
        longitude: data.longitude ? parseFloat(data.longitude) : null,
      }),
    });
    loadAttractions();
    setAddOpen(false);
  };

  if (authLoading || !user || loading) {
    return <div className="flex justify-center py-16"><Loader2 className="h-6 w-6 animate-spin text-muted-foreground" /></div>;
  }

  return (
    <div className="container mx-auto px-4 py-8 max-w-5xl">
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center gap-3">
          <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-primary/10 text-primary">
            <MapPin className="h-5 w-5" />
          </div>
          <div>
            <h1 className="text-3xl font-bold tracking-tight">Manage Attractions</h1>
            <p className="text-muted-foreground text-sm mt-0.5">{attractions.length} total attractions</p>
          </div>
        </div>
        <Button onClick={() => setAddOpen(true)} className="gap-2 rounded-xl">
          <Plus className="h-4 w-4" /> Add Attraction
        </Button>
      </div>

      <div className="border rounded-xl border-border/50 overflow-hidden">
        <Table>
          <TableHeader>
            <TableRow className="bg-muted/50">
              <TableHead>Name</TableHead>
              <TableHead>Category</TableHead>
              <TableHead>Barangay</TableHead>
              <TableHead>Status</TableHead>
              <TableHead className="text-right">Actions</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {attractions.map((a) => (
              <TableRow key={a.id}>
                <TableCell className="font-medium">{a.name}</TableCell>
                <TableCell><Badge variant="secondary" className="text-xs">{a.category || "—"}</Badge></TableCell>
                <TableCell className="text-muted-foreground text-sm">{a.barangay_name || "—"}</TableCell>
                <TableCell>
                  <Badge variant={a.status === "published" ? "default" : "outline"} className="text-xs capitalize">
                    {a.status}
                  </Badge>
                </TableCell>
                <TableCell className="text-right">
                  <div className="flex justify-end gap-1">
                    <Button variant="ghost" size="icon" className="h-8 w-8" onClick={() => setEditTarget(a)}>
                      <Pencil className="h-3.5 w-3.5" />
                    </Button>
                    <Button variant="ghost" size="icon" className="h-8 w-8 text-destructive" onClick={() => setDeleteTarget(a)}>
                      <Trash2 className="h-3.5 w-3.5" />
                    </Button>
                  </div>
                </TableCell>
              </TableRow>
            ))}
            {attractions.length === 0 && (
              <TableRow>
                <TableCell colSpan={5} className="text-center text-muted-foreground py-8">
                  No attractions yet.
                </TableCell>
              </TableRow>
            )}
          </TableBody>
        </Table>
      </div>

      <DeleteDialog open={!!deleteTarget} onOpenChange={() => setDeleteTarget(null)} onConfirm={handleDelete} title="Delete Attraction" description={`Are you sure you want to delete "${deleteTarget?.name ?? ""}"?`} />
      <AttractionFormDialog open={!!editTarget} onOpenChange={() => setEditTarget(null)} onSubmit={handleEdit} title="Edit Attraction" initialData={editTarget ? { name: editTarget.name, category: editTarget.category } : undefined} />
      <AttractionFormDialog open={addOpen} onOpenChange={setAddOpen} onSubmit={handleAdd} title="Add Attraction" />
    </div>
  );
}
