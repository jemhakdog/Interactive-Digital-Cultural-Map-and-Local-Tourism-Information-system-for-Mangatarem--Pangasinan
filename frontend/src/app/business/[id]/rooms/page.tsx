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
import { BusinessLayout } from "@/components/business/business-layout";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import {
  Loader2,
  ArrowLeft,
  Hotel,
  Plus,
  Pencil,
  Trash2,
  Users,
  Bed,
} from "lucide-react";

interface RoomItem {
  id: number;
  name: string;
  price_per_night?: number | null;
  capacity?: number | null;
  is_available?: boolean;
}

const AMENITY_OPTIONS = ["wifi", "aircon", "tv", "hot_water", "mini_bar", "balcony", "bathroom"];

export default function ManageRoomsPage() {
  const params = useParams<{ id: string }>();
  const id = params.id;
  const { user, loading: authLoading } = useAuth();

  const [estName, setEstName] = useState("");
  const [rooms, setRooms] = useState<RoomItem[]>([]);
  const [loading, setLoading] = useState(true);

  const [name, setName] = useState("");
  const [price, setPrice] = useState("");
  const [capacity, setCapacity] = useState("2");
  const [description, setDescription] = useState("");
  const [amenities, setAmenities] = useState<string[]>([]);
  const [isAvailable, setIsAvailable] = useState(true);
  const [adding, setAdding] = useState(false);
  const [addError, setAddError] = useState("");

  const [editing, setEditing] = useState<RoomItem | null>(null);
  const [savingEdit, setSavingEdit] = useState(false);

  const load = async () => {
    try {
      const data = await fetchAPI<{ establishment?: { name?: string }; rooms?: RoomItem[] }>(
        `/api/business/${id}`
      );
      setEstName(data.establishment?.name ?? "");
      setRooms((data.rooms as RoomItem[]) ?? []);
    } catch {
      /* header optional */
    }
    try {
      const list = await fetchAPI<{ rooms?: RoomItem[] }>("/api/business/rooms/list");
      setRooms(list.rooms ?? []);
    } catch {
      setRooms([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (authLoading || !user) return;
    load();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [user, authLoading, id]);

  const toggleAmenity = (a: string) =>
    setAmenities((prev) => (prev.includes(a) ? prev.filter((x) => x !== a) : [...prev, a]));

  const handleAdd = async (e: React.FormEvent) => {
    e.preventDefault();
    setAdding(true);
    setAddError("");
    try {
      await fetchAPI("/api/business/rooms", {
        method: "POST",
        body: JSON.stringify({
          name,
          description,
          price_per_night: price ? parseFloat(price) : null,
          capacity: capacity ? parseInt(capacity, 10) : 2,
          is_available: isAvailable,
          amenities,
        }),
      });
      setName("");
      setPrice("");
      setCapacity("2");
      setDescription("");
      setAmenities([]);
      setIsAvailable(true);
      await load();
    } catch (err) {
      setAddError(err instanceof Error ? err.message : "Failed to add room.");
    } finally {
      setAdding(false);
    }
  };

  const handleDelete = async (roomId: number) => {
    if (!confirm("Delete this room from your listing?")) return;
    try {
      await fetchAPI(`/api/business/rooms/${roomId}`, { method: "DELETE" });
      setRooms((prev) => prev.filter((r) => r.id !== roomId));
    } catch {
      /* graceful */
    }
  };

  const handleEditSave = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!editing) return;
    setSavingEdit(true);
    try {
      await fetchAPI(`/api/business/rooms/${editing.id}`, {
        method: "PUT",
        body: JSON.stringify({
          name: editing.name,
          price_per_night: editing.price_per_night ?? null,
          capacity: editing.capacity ?? 2,
          is_available: editing.is_available ?? true,
        }),
      });
      setEditing(null);
      await load();
    } catch {
      /* graceful */
    } finally {
      setSavingEdit(false);
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center py-16">
        <Loader2 className="h-6 w-6 animate-spin text-muted-foreground" />
      </div>
    );
  }

  return (
    <BusinessLayout>
      <div className="container mx-auto px-4 py-8 max-w-5xl space-y-8">
      <div className="flex items-center justify-between pb-4 border-b border-border/50">
        <div className="space-y-1">
          <Link
            href="/business/dashboard"
            className="text-xs font-bold uppercase tracking-wider text-muted-foreground hover:text-foreground flex items-center gap-1.5 transition-colors"
          >
            <ArrowLeft className="h-3.5 w-3.5" /> Back to Dashboard
          </Link>
          <h1 className="text-xl font-bold tracking-tight text-foreground mt-2">
            Manage Room Inventory
          </h1>
          <p className="text-[11px] font-bold text-muted-foreground uppercase tracking-wider">
            {estName || "Your establishment"} — {rooms.length} active rooms listed
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Add form */}
        <Card className="h-fit border-border/60 p-6 space-y-4">
          <h2 className="text-xs font-bold uppercase text-muted-foreground tracking-wider border-b border-border/40 pb-3">
            Add New Room Unit
          </h2>
          <form onSubmit={handleAdd} className="space-y-4">
            <div className="space-y-1.5">
              <Label className="text-[11px] font-bold uppercase text-muted-foreground tracking-wider">Room Designation *</Label>
              <Input value={name} onChange={(e) => setName(e.target.value)} required placeholder="e.g. Deluxe Suite 101" className="rounded-xl" />
            </div>
            <div className="grid grid-cols-2 gap-3">
              <div className="space-y-1.5">
                <Label className="text-[11px] font-bold uppercase text-muted-foreground tracking-wider">Rate / Night (₱) *</Label>
                <Input value={price} onChange={(e) => setPrice(e.target.value)} required type="number" step="0.01" placeholder="1500" className="rounded-xl" />
              </div>
              <div className="space-y-1.5">
                <Label className="text-[11px] font-bold uppercase text-muted-foreground tracking-wider">Capacity *</Label>
                <Input value={capacity} onChange={(e) => setCapacity(e.target.value)} required type="number" min={1} className="rounded-xl" />
              </div>
            </div>
            <div className="space-y-1.5">
              <Label className="text-[11px] font-bold uppercase text-muted-foreground tracking-wider">Description</Label>
              <Textarea value={description} onChange={(e) => setDescription(e.target.value)} rows={2} placeholder="Beds, amenities, layout..." className="rounded-xl" />
            </div>
            <div className="space-y-2">
              <Label className="text-[11px] font-bold uppercase text-muted-foreground tracking-wider">Room Features</Label>
              <div className="grid grid-cols-2 gap-2">
                {AMENITY_OPTIONS.map((a) => (
                  <label key={a} className="flex items-center gap-2 text-xs font-semibold text-muted-foreground bg-muted/50 border border-border rounded-xl px-3 py-2 cursor-pointer capitalize">
                    <input type="checkbox" checked={amenities.includes(a)} onChange={() => toggleAmenity(a)} className="rounded border-border text-primary" />
                    {a.replace("_", " ")}
                  </label>
                ))}
              </div>
            </div>
            <label className="flex items-center gap-2.5 text-xs font-semibold text-muted-foreground cursor-pointer">
              <input type="checkbox" checked={isAvailable} onChange={(e) => setIsAvailable(e.target.checked)} className="rounded border-border text-primary" />
              Make available for booking immediately
            </label>
            {addError && <p className="text-xs font-semibold text-destructive">{addError}</p>}
            <Button type="submit" disabled={adding} className="w-full gap-2 rounded-xl">
              {adding ? <Loader2 className="h-4 w-4 animate-spin" /> : <Plus className="h-4 w-4" />}
              {adding ? "Adding..." : "Add Room Unit"}
            </Button>
          </form>
        </Card>

        {/* Catalog */}
        <div className="lg:col-span-2 space-y-4">
          <h2 className="text-xs font-bold uppercase text-muted-foreground tracking-wider border-b border-border/40 pb-3">
            Active Inventory Listing
          </h2>
          {rooms.length > 0 ? (
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              {rooms.map((room) => (
                <Card key={room.id} className="overflow-hidden border-border/60 flex flex-col justify-between">
                  <CardContent className="p-5 flex-grow flex flex-col justify-between space-y-4">
                    <div>
                      <div className="flex items-start justify-between gap-2">
                        <h3 className="font-bold text-sm text-foreground leading-snug">{room.name}</h3>
                        <span className={`inline-block px-2 py-0.5 text-[8px] font-bold uppercase rounded shrink-0 ${
                          room.is_available ? "bg-emerald-500/10 text-emerald-600" : "bg-destructive/10 text-destructive"
                        }`}>
                          {room.is_available ? "Available" : "Occupied"}
                        </span>
                      </div>
                      <div className="flex items-center gap-3 mt-1 text-[10px] font-bold text-muted-foreground uppercase tracking-wider">
                        {room.price_per_night != null && (
                          <span className="text-primary font-extrabold">₱{Number(room.price_per_night).toLocaleString()}/Night</span>
                        )}
                        <span>•</span>
                        <span className="flex items-center gap-1"><Users className="h-3 w-3" /> {room.capacity ?? 2} Guests</span>
                      </div>
                    </div>
                    <div className="pt-4 border-t border-border/40 flex justify-end gap-2">
                      <Dialog open={editing?.id === room.id} onOpenChange={(o) => !o && setEditing(null)}>
                        <DialogTrigger
                          render={
                            <Button
                              variant="ghost"
                              size="icon"
                              className="h-7 w-7 text-muted-foreground hover:text-foreground"
                              onClick={() => setEditing(room)}
                              aria-label="Edit room"
                            >
                              <Pencil className="h-3.5 w-3.5" />
                            </Button>
                          }
                        />
                        <DialogContent className="sm:max-w-md rounded-2xl">
                          <DialogHeader>
                            <DialogTitle className="text-lg font-bold">Edit Room</DialogTitle>
                            <DialogDescription className="text-xs">Update room details for your listing.</DialogDescription>
                          </DialogHeader>
                          {editing && (
                            <form onSubmit={handleEditSave} className="space-y-3 py-2">
                              <Input value={editing.name} onChange={(e) => setEditing({ ...editing, name: e.target.value })} required className="rounded-xl" />
                              <div className="grid grid-cols-2 gap-3">
                                <Input value={editing.price_per_night != null ? String(editing.price_per_night) : ""} onChange={(e) => setEditing({ ...editing, price_per_night: e.target.value ? parseFloat(e.target.value) : null })} type="number" step="0.01" placeholder="Rate / Night" className="rounded-xl" />
                                <Input value={editing.capacity != null ? String(editing.capacity) : "2"} onChange={(e) => setEditing({ ...editing, capacity: e.target.value ? parseInt(e.target.value, 10) : 2 })} type="number" min={1} placeholder="Capacity" className="rounded-xl" />
                              </div>
                              <label className="flex items-center gap-2 text-xs font-semibold text-muted-foreground cursor-pointer">
                                <input type="checkbox" checked={editing.is_available ?? true} onChange={(e) => setEditing({ ...editing, is_available: e.target.checked })} className="rounded border-border text-primary" />
                                Available for booking
                              </label>
                              <Button type="submit" disabled={savingEdit} className="w-full rounded-xl">
                                {savingEdit ? <Loader2 className="h-4 w-4 animate-spin" /> : "Save Changes"}
                              </Button>
                            </form>
                          )}
                        </DialogContent>
                      </Dialog>
                      <Button
                        variant="ghost"
                        size="icon"
                        className="h-7 w-7 text-destructive hover:bg-destructive/10"
                        onClick={() => handleDelete(room.id)}
                        aria-label="Delete room"
                      >
                        <Trash2 className="h-3.5 w-3.5" />
                      </Button>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          ) : (
            <div className="text-center py-20 bg-card border border-border/50 rounded-3xl">
              <div className="inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-muted text-muted-foreground mb-4">
                <Bed className="w-8 h-8" />
              </div>
              <h3 className="text-sm font-bold text-foreground">No room units listed</h3>
              <p className="text-xs font-medium text-muted-foreground mt-1 max-w-xs mx-auto">
                Use the creator panel to configure rooms for public booking details.
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
    </BusinessLayout>
  );
}
