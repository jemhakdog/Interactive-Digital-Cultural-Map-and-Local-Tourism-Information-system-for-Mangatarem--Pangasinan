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
import { Badge } from "@/components/ui/badge";
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
  Utensils,
  Plus,
  Pencil,
  Trash2,
  Star,
} from "lucide-react";

interface MenuItem {
  id: number;
  name: string;
  price?: number | null;
  category?: string | null;
  description?: string | null;
  is_available?: boolean;
  is_bestseller?: boolean;
}

const CATEGORIES = ["main", "appetizer", "dessert", "drinks", "snacks"];

export default function ManageMenuPage() {
  const params = useParams<{ id: string }>();
  const id = params.id;
  const { user, loading: authLoading } = useAuth();

  const [estName, setEstName] = useState("");
  const [items, setItems] = useState<MenuItem[]>([]);
  const [loading, setLoading] = useState(true);

  // Add form state
  const [name, setName] = useState("");
  const [price, setPrice] = useState("");
  const [category, setCategory] = useState("main");
  const [description, setDescription] = useState("");
  const [isBestseller, setIsBestseller] = useState(false);
  const [isAvailable, setIsAvailable] = useState(true);
  const [adding, setAdding] = useState(false);
  const [addError, setAddError] = useState("");

  // Edit dialog state
  const [editing, setEditing] = useState<MenuItem | null>(null);
  const [savingEdit, setSavingEdit] = useState(false);

  const load = async () => {
    try {
      const data = await fetchAPI<{ establishment?: { name?: string }; menu_items?: MenuItem[] }>(
        `/api/business/${id}`
      );
      setEstName(data.establishment?.name ?? "");
      setItems(data.menu_items ?? []);
    } catch {
      // Header optional — see owner menu list below for source of truth.
    }
    try {
      const list = await fetchAPI<{ menu_items?: MenuItem[] }>("/api/business/menu/list");
      setItems(list.menu_items ?? []);
    } catch {
      setItems([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (authLoading || !user) return;
    load();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [user, authLoading, id]);

  const handleAdd = async (e: React.FormEvent) => {
    e.preventDefault();
    setAdding(true);
    setAddError("");
    try {
      await fetchAPI("/api/business/menu", {
        method: "POST",
        body: JSON.stringify({
          name,
          description,
          price: price ? parseFloat(price) : null,
          category,
          is_bestseller: isBestseller,
          is_available: isAvailable,
        }),
      });
      setName("");
      setPrice("");
      setDescription("");
      setIsBestseller(false);
      setIsAvailable(true);
      await load();
    } catch (err) {
      setAddError(err instanceof Error ? err.message : "Failed to add menu item.");
    } finally {
      setAdding(false);
    }
  };

  const handleDelete = async (itemId: number) => {
    if (!confirm("Delete this menu item from your listing?")) return;
    try {
      await fetchAPI(`/api/business/menu/${itemId}`, { method: "DELETE" });
      setItems((prev) => prev.filter((m) => m.id !== itemId));
    } catch {
      /* graceful */
    }
  };

  const handleEditSave = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!editing) return;
    setSavingEdit(true);
    try {
      await fetchAPI(`/api/business/menu/${editing.id}`, {
        method: "PUT",
        body: JSON.stringify({
          name: editing.name,
          description: editing.description ?? "",
          price: editing.price ?? null,
          category: editing.category ?? "main",
          is_bestseller: editing.is_bestseller ?? false,
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
            Manage Menu &amp; Specialties
          </h1>
          <p className="text-[11px] font-bold text-muted-foreground uppercase tracking-wider">
            {estName || "Your establishment"} — {items.length} dishes listed
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Add form */}
        <Card className="h-fit border-border/60 p-6 space-y-4">
          <h2 className="text-xs font-bold uppercase text-muted-foreground tracking-wider border-b border-border/40 pb-3">
            Add New Dish
          </h2>
          <form onSubmit={handleAdd} className="space-y-4">
            <div className="space-y-1.5">
              <Label className="text-[11px] font-bold uppercase text-muted-foreground tracking-wider">Dish Name *</Label>
              <Input value={name} onChange={(e) => setName(e.target.value)} required placeholder="e.g. Pinakbet Platter" className="rounded-xl" />
            </div>
            <div className="grid grid-cols-2 gap-3">
              <div className="space-y-1.5">
                <Label className="text-[11px] font-bold uppercase text-muted-foreground tracking-wider">Price (₱)</Label>
                <Input value={price} onChange={(e) => setPrice(e.target.value)} type="number" step="0.01" placeholder="150" className="rounded-xl" />
              </div>
              <div className="space-y-1.5">
                <Label className="text-[11px] font-bold uppercase text-muted-foreground tracking-wider">Category *</Label>
                <select
                  value={category}
                  onChange={(e) => setCategory(e.target.value)}
                  className="h-10 w-full rounded-xl border border-border bg-card px-3 text-sm text-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary"
                >
                  {CATEGORIES.map((c) => (
                    <option key={c} value={c} className="capitalize">{c}</option>
                  ))}
                </select>
              </div>
            </div>
            <div className="space-y-1.5">
              <Label className="text-[11px] font-bold uppercase text-muted-foreground tracking-wider">Description</Label>
              <Textarea value={description} onChange={(e) => setDescription(e.target.value)} rows={2} placeholder="Signature flavors..." className="rounded-xl" />
            </div>
            <div className="flex flex-wrap gap-4 pt-1">
              <label className="flex items-center gap-2 text-xs font-semibold text-muted-foreground cursor-pointer">
                <input type="checkbox" checked={isBestseller} onChange={(e) => setIsBestseller(e.target.checked)} className="rounded border-border text-primary" />
                ⭐ Best Choice
              </label>
              <label className="flex items-center gap-2 text-xs font-semibold text-muted-foreground cursor-pointer">
                <input type="checkbox" checked={isAvailable} onChange={(e) => setIsAvailable(e.target.checked)} className="rounded border-border text-primary" />
                Available
              </label>
            </div>
            {addError && <p className="text-xs font-semibold text-destructive">{addError}</p>}
            <Button type="submit" disabled={adding} className="w-full gap-2 rounded-xl">
              {adding ? <Loader2 className="h-4 w-4 animate-spin" /> : <Plus className="h-4 w-4" />}
              {adding ? "Adding..." : "Add Menu Dish"}
            </Button>
          </form>
        </Card>

        {/* Catalog */}
        <div className="lg:col-span-2 space-y-4">
          <h2 className="text-xs font-bold uppercase text-muted-foreground tracking-wider border-b border-border/40 pb-3">
            Active Menu Catalog
          </h2>
          {items.length > 0 ? (
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              {items.map((item) => (
                <Card key={item.id} className="overflow-hidden border-border/60 flex flex-col justify-between">
                  <CardContent className="p-5 flex-grow flex flex-col justify-between space-y-3">
                    <div>
                      <div className="flex items-start justify-between gap-2">
                        <h3 className="font-bold text-sm text-foreground leading-snug">{item.name}</h3>
                        {item.price != null && (
                          <span className="text-sm font-extrabold text-primary whitespace-nowrap">₱{Number(item.price).toLocaleString()}</span>
                        )}
                      </div>
                      {item.category && (
                        <span className="inline-block mt-1 text-[10px] font-bold uppercase text-foreground/70 bg-muted px-2 py-0.5 rounded-md capitalize">
                          {item.category}
                        </span>
                      )}
                    </div>
                    <div className="pt-3 border-t border-border/40 flex items-center justify-between">
                      <span className={`inline-block px-2 py-0.5 text-[9px] font-bold uppercase rounded ${
                        item.is_available ? "bg-emerald-500/10 text-emerald-600" : "bg-destructive/10 text-destructive"
                      }`}>
                        {item.is_available ? "Available" : "Unavailable"}
                      </span>
                      {item.is_bestseller && (
                        <Badge className="bg-amber-500 text-white text-[9px] py-0 px-1.5">
                          <Star className="h-2.5 w-2.5 mr-0.5" /> Bestseller
                        </Badge>
                      )}
                      <div className="flex items-center gap-2">
                        <Dialog open={editing?.id === item.id} onOpenChange={(o) => !o && setEditing(null)}>
                          <DialogTrigger
                            render={
                              <Button
                                variant="ghost"
                                size="icon"
                                className="h-7 w-7 text-muted-foreground hover:text-foreground"
                                onClick={() => setEditing(item)}
                                aria-label="Edit menu item"
                              >
                                <Pencil className="h-3.5 w-3.5" />
                              </Button>
                            }
                          />
                          <DialogContent className="sm:max-w-md rounded-2xl">
                            <DialogHeader>
                              <DialogTitle className="text-lg font-bold">Edit Menu Item</DialogTitle>
                              <DialogDescription className="text-xs">Update dish details for your listing.</DialogDescription>
                            </DialogHeader>
                            {editing && (
                              <form onSubmit={handleEditSave} className="space-y-3 py-2">
                                <Input value={editing.name} onChange={(e) => setEditing({ ...editing, name: e.target.value })} required className="rounded-xl" />
                                <div className="grid grid-cols-2 gap-3">
                                  <Input value={editing.price != null ? String(editing.price) : ""} onChange={(e) => setEditing({ ...editing, price: e.target.value ? parseFloat(e.target.value) : null })} type="number" step="0.01" placeholder="Price" className="rounded-xl" />
                                  <select
                                    value={editing.category ?? "main"}
                                    onChange={(e) => setEditing({ ...editing, category: e.target.value })}
                                    className="h-10 w-full rounded-xl border border-border bg-card px-3 text-sm text-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary"
                                  >
                                    {CATEGORIES.map((c) => (
                                      <option key={c} value={c} className="capitalize">{c}</option>
                                    ))}
                                  </select>
                                </div>
                                <Textarea value={editing.description ?? ""} onChange={(e) => setEditing({ ...editing, description: e.target.value })} rows={2} className="rounded-xl" />
                                <div className="flex flex-wrap gap-4">
                                  <label className="flex items-center gap-2 text-xs font-semibold text-muted-foreground cursor-pointer">
                                    <input type="checkbox" checked={editing.is_bestseller ?? false} onChange={(e) => setEditing({ ...editing, is_bestseller: e.target.checked })} className="rounded border-border text-primary" />
                                    ⭐ Best Choice
                                  </label>
                                  <label className="flex items-center gap-2 text-xs font-semibold text-muted-foreground cursor-pointer">
                                    <input type="checkbox" checked={editing.is_available ?? true} onChange={(e) => setEditing({ ...editing, is_available: e.target.checked })} className="rounded border-border text-primary" />
                                    Available
                                  </label>
                                </div>
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
                          onClick={() => handleDelete(item.id)}
                          aria-label="Delete menu item"
                        >
                          <Trash2 className="h-3.5 w-3.5" />
                        </Button>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          ) : (
            <div className="text-center py-20 bg-card border border-border/50 rounded-3xl">
              <div className="inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-muted text-muted-foreground mb-4">
                <Utensils className="w-8 h-8" />
              </div>
              <h3 className="text-sm font-bold text-foreground">No menu items listed</h3>
              <p className="text-xs font-medium text-muted-foreground mt-1 max-w-xs mx-auto">
                Use the creator panel to add your signature dishes and beverages.
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
    </BusinessLayout>
  );
}
