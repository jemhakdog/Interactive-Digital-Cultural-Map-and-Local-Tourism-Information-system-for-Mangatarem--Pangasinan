"use client";

import { useEffect, useState, useCallback } from "react";
import Link from "next/link";
import { useAuth } from "@/lib/auth";
import { useRouter, useParams } from "next/navigation";
import { fetchAPI } from "@/lib/api";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Loader2, Plus, Pencil, Trash2 } from "lucide-react";

interface HeritageItem {
  id: number;
  name?: string;
  municipality?: string;
  status?: string;
  subcategory?: string;
  type?: string;
  location?: string;
}

export default function AdminHeritageTypeList() {
  const { user, loading: authLoading } = useAuth();
  const router = useRouter();
  const params = useParams();
  const type = String(params.type);

  const [items, setItems] = useState<HeritageItem[]>([]);
  const [loading, setLoading] = useState(true);

  const load = useCallback(() => {
    return fetchAPI<{ items?: HeritageItem[] }>(`/api/heritage/${type}`)
      .then((data) => setItems(data.items ?? []))
      .catch(() => setItems([]));
  }, [type]);

  useEffect(() => {
    if (!authLoading && (!user || user.role !== "admin")) router.push("/dashboard");
  }, [user, authLoading, router]);

  useEffect(() => {
    if (!user) return;
    load().finally(() => setLoading(false));
  }, [user, load]);

  const handleDelete = async (item: HeritageItem) => {
    if (!window.confirm(`Delete "${item.name ?? item.municipality ?? item.id}"?`)) return;
    try {
      await fetchAPI(`/api/heritage/${type}/${item.id}`, { method: "DELETE" });
      setItems((prev) => prev.filter((i) => i.id !== item.id));
    } catch {
      /* ignore */
    }
  };

  const title = type.charAt(0).toUpperCase() + type.slice(1);

  if (authLoading || !user || loading) {
    return (
      <div className="flex justify-center py-16">
        <Loader2 className="h-6 w-6 animate-spin text-muted-foreground" />
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8 max-w-5xl">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-3xl font-bold tracking-tight capitalize">{title} Heritage</h1>
          <p className="text-muted-foreground text-sm mt-0.5">{items.length} records</p>
        </div>
        <Button render={<Link href={`/admin/heritage/new?type=${type}`} />} className="gap-2 rounded-xl">
          <Plus className="h-4 w-4" /> Add New Entry
        </Button>
      </div>

      <div className="border rounded-xl border-border/50 overflow-hidden">
        <Table>
          <TableHeader>
            <TableRow className="bg-muted/50">
              <TableHead>ID</TableHead>
              <TableHead>Name</TableHead>
              <TableHead>Subcategory</TableHead>
              <TableHead>Status</TableHead>
              <TableHead className="text-right">Actions</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {items.map((item) => (
              <TableRow key={item.id}>
                <TableCell className="font-mono text-xs">{item.id}</TableCell>
                <TableCell className="font-medium">{item.name ?? item.municipality ?? "—"}</TableCell>
                <TableCell className="text-muted-foreground text-sm">
                  {item.subcategory ?? item.type ?? "—"}
                </TableCell>
                <TableCell>
                  <Badge
                    variant={item.status === "approved" ? "default" : "outline"}
                    className="text-xs capitalize"
                  >
                    {item.status ?? "pending"}
                  </Badge>
                </TableCell>
                <TableCell className="text-right">
                  <div className="flex justify-end gap-1">
                    <Button render={<Link href={`/admin/heritage/${type}/${item.id}/edit`} />} variant="ghost" size="icon" className="h-8 w-8">
                      <Pencil className="h-3.5 w-3.5" />
                    </Button>
                    <Button
                      variant="ghost"
                      size="icon"
                      className="h-8 w-8 text-destructive"
                      onClick={() => handleDelete(item)}
                    >
                      <Trash2 className="h-3.5 w-3.5" />
                    </Button>
                  </div>
                </TableCell>
              </TableRow>
            ))}
            {items.length === 0 && (
              <TableRow>
                <TableCell colSpan={5} className="text-center text-muted-foreground py-8">
                  No {type} heritage records yet.
                </TableCell>
              </TableRow>
            )}
          </TableBody>
        </Table>
      </div>
    </div>
  );
}
