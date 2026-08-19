"use client";

import { useEffect, useState, useCallback } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/lib/auth";
import { fetchAPI } from "@/lib/api";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Loader2, Plus, Pencil, Trash2 } from "lucide-react";
import { DeleteDialog, EventFormDialog } from "@/components/admin-dialogs";

interface Event {
  id: number;
  name: string;
  category: string;
  status: string;
  date: string | null;
  barangay_name: string | null;
}

export default function AdminEventsPage() {
  const { user, loading: authLoading } = useAuth();
  const router = useRouter();
  const [events, setEvents] = useState<Event[]>([]);
  const [loading, setLoading] = useState(true);
  const [deleteTarget, setDeleteTarget] = useState<Event | null>(null);
  const [editTarget, setEditTarget] = useState<Event | null>(null);
  const [addOpen, setAddOpen] = useState(false);

  const loadEvents = useCallback(() => {
    return fetchAPI("/api/events")
      .then((data) => setEvents((data as { items: Event[] }).items ?? []))
      .catch(() => {});
  }, []);

  useEffect(() => {
    if (!authLoading && (!user || user.role !== "admin")) router.push("/dashboard");
  }, [user, authLoading, router]);

  useEffect(() => {
    if (!user) return;
    loadEvents().finally(() => setLoading(false));
  }, [user, loadEvents]);

  const handleDelete = async () => {
    if (!deleteTarget) return;
    await fetchAPI(`/api/events/${deleteTarget.id}`, { method: "DELETE" });
    setEvents((prev) => prev.filter((e) => e.id !== deleteTarget.id));
    setDeleteTarget(null);
  };

  const handleEdit = async (data: { name: string; description?: string; category?: string; date?: string; location?: string }) => {
    if (!editTarget) return;
    await fetchAPI(`/api/events/${editTarget.id}`, {
      method: "PUT",
      body: JSON.stringify({
        name: data.name,
        description: data.description ?? "",
        category: data.category ?? "",
        date: data.date || null,
        location: data.location ?? "",
      }),
    });
    loadEvents();
    setEditTarget(null);
  };

  const handleAdd = async (data: { name: string; description?: string; category?: string; date?: string; location?: string }) => {
    await fetchAPI("/api/events", {
      method: "POST",
      body: JSON.stringify({
        name: data.name,
        description: data.description ?? "",
        category: data.category ?? "",
        date: data.date || null,
        location: data.location ?? "",
      }),
    });
    loadEvents();
    setAddOpen(false);
  };

  if (authLoading || !user || loading) {
    return <div className="flex justify-center py-16"><Loader2 className="h-6 w-6 animate-spin text-muted-foreground" /></div>;
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-3xl font-bold">Manage Events</h1>
          <p className="text-muted-foreground text-sm mt-1">{events.length} total events</p>
        </div>
        <Button onClick={() => setAddOpen(true)} className="gap-2">
          <Plus className="h-4 w-4" /> Add Event
        </Button>
      </div>

      <div className="border rounded-lg">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Name</TableHead>
              <TableHead>Category</TableHead>
              <TableHead>Date</TableHead>
              <TableHead>Barangay</TableHead>
              <TableHead>Status</TableHead>
              <TableHead className="text-right">Actions</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {events.map((e) => (
              <TableRow key={e.id}>
                <TableCell className="font-medium">{e.name}</TableCell>
                <TableCell>{e.category || "—"}</TableCell>
                <TableCell>{e.date ? new Date(e.date).toLocaleDateString() : "—"}</TableCell>
                <TableCell>{e.barangay_name || "—"}</TableCell>
                <TableCell>
                  <Badge variant={e.status === "approved" ? "default" : "secondary"}>
                    {e.status}
                  </Badge>
                </TableCell>
                <TableCell className="text-right">
                  <Button variant="ghost" size="icon" className="h-8 w-8" onClick={() => setEditTarget(e)}>
                    <Pencil className="h-4 w-4" />
                  </Button>
                  <Button variant="ghost" size="icon" className="h-8 w-8 text-destructive" onClick={() => setDeleteTarget(e)}>
                    <Trash2 className="h-4 w-4" />
                  </Button>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </div>

      <DeleteDialog
        open={!!deleteTarget}
        onOpenChange={(open) => { if (!open) setDeleteTarget(null); }}
        title="Delete Event"
        description={`Are you sure you want to delete "${deleteTarget?.name}"? This action cannot be undone.`}
        onConfirm={handleDelete}
      />

      <EventFormDialog
        open={!!editTarget}
        onOpenChange={(open) => { if (!open) setEditTarget(null); }}
        initialData={editTarget ? {
          name: editTarget.name,
          category: editTarget.category,
          date: editTarget.date ?? "",
        } : undefined}
        title="Edit Event"
        onSubmit={handleEdit}
      />

      <EventFormDialog
        open={addOpen}
        onOpenChange={setAddOpen}
        title="Add Event"
        onSubmit={handleAdd}
      />
    </div>
  );
}
