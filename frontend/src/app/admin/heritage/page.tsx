"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { useAuth } from "@/lib/auth";
import { useRouter } from "next/navigation";
import { fetchAPI } from "@/lib/api";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Loader2, Landmark, Plus } from "lucide-react";

interface TypeStat {
  slug?: string;
  type?: string;
  label?: string;
  form?: string;
  total?: number;
  approved?: number;
  pending?: number;
}

interface RegistryRow {
  type: string;
  label?: string;
  form?: string;
  has_coords?: boolean;
  name_field?: string;
}

export default function AdminHeritageDashboard() {
  const { user, loading: authLoading } = useAuth();
  const router = useRouter();
  const [stats, setStats] = useState<TypeStat[]>([]);
  const [registry, setRegistry] = useState<RegistryRow[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!authLoading && (!user || user.role !== "admin")) router.push("/dashboard");
  }, [user, authLoading, router]);

  useEffect(() => {
    if (!user) return;
    Promise.all([
      fetchAPI("/api/heritage/types").catch(() => null),
      fetchAPI("/api/heritage").catch(() => null),
    ]).then(([typesData, allData]) => {
      const t = (typesData as { types?: TypeStat[] } | TypeStat[] | null) ?? null;
      if (Array.isArray(t)) setStats(t);
      else if (t && Array.isArray((t as { types?: TypeStat[] }).types)) setStats((t as { types: TypeStat[] }).types);

      const a = (allData as { items?: unknown[] } | null) ?? null;
      // Derive a small registry overview from distinct types returned by /types.
      if (Array.isArray(t)) {
        setRegistry(
          t.map((s) => ({
            type: s.slug ?? s.type ?? "",
            label: s.label ?? s.type ?? "",
            form: s.form ?? "",
            has_coords: false,
            name_field: "name",
          }))
        );
      } else if (a && Array.isArray(a.items)) {
        const seen = new Map<string, RegistryRow>();
        (a.items as { type?: string }[]).forEach((it) => {
          const ty = it.type ?? "unknown";
          if (!seen.has(ty))
            seen.set(ty, { type: ty, label: ty, form: "", has_coords: false, name_field: "name" });
        });
        setRegistry(Array.from(seen.values()));
      }
    }).finally(() => setLoading(false));
  }, [user]);

  if (authLoading || !user || loading) {
    return (
      <div className="flex justify-center py-16">
        <Loader2 className="h-6 w-6 animate-spin text-muted-foreground" />
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8 max-w-5xl space-y-8">
      <div className="flex items-center gap-3">
        <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-primary/10 text-primary">
          <Landmark className="h-5 w-5" />
        </div>
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Heritage Archive</h1>
          <p className="text-muted-foreground text-sm mt-0.5">
            Manage Mangatarem&apos;s natural, cultural, built, and intangible heritage registries
          </p>
        </div>
      </div>

      {stats.length === 0 ? (
        <div className="border border-dashed border-border rounded-2xl py-16 text-center">
          <Landmark className="h-12 w-12 mx-auto mb-3 text-muted-foreground/40" />
          <p className="font-bold text-foreground">No heritage records yet</p>
          <p className="text-xs text-muted-foreground mt-1">
            Add your first entry to start populating the registry.
          </p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {stats.map((s, i) => {
            const type = s.slug ?? s.type ?? "";
            return (
              <Card key={i} className="flex flex-col justify-between gap-4">
                <CardContent className="p-6 space-y-4">
                  <div className="flex items-start justify-between">
                    <div>
                      {s.form && (
                        <Badge variant="secondary" className="mb-1 text-[10px]">
                          {s.form}
                        </Badge>
                      )}
                      <h3 className="text-sm font-bold text-foreground">{s.label ?? type}</h3>
                    </div>
                    <div className="p-2 bg-muted rounded-xl text-primary">
                      <Landmark className="h-5 w-5" />
                    </div>
                  </div>
                  <div className="grid grid-cols-3 gap-2 text-center">
                    <div className="bg-muted rounded-xl py-2.5">
                      <p className="text-base font-bold text-foreground">{s.total ?? 0}</p>
                      <p className="text-[9px] uppercase text-muted-foreground">Total</p>
                    </div>
                    <div className="bg-primary/5 rounded-xl py-2.5">
                      <p className="text-base font-bold text-primary">{s.approved ?? 0}</p>
                      <p className="text-[9px] uppercase text-muted-foreground">Approved</p>
                    </div>
                    <div className="bg-yellow-50 rounded-xl py-2.5">
                      <p className="text-base font-bold text-amber-600">{s.pending ?? 0}</p>
                      <p className="text-[9px] uppercase text-muted-foreground">Pending</p>
                    </div>
                  </div>
                </CardContent>
                <div className="flex gap-2 px-6 pb-6">
                  <Button render={<Link href={`/admin/heritage/${type}`} />} variant="outline" className="flex-1 rounded-xl">
                    Manage
                  </Button>
                  <Button render={<Link href={`/admin/heritage/new?type=${type}`} />} size="icon" className="rounded-xl" title="Add record">
                    <Plus className="h-4 w-4" />
                  </Button>
                </div>
              </Card>
            );
          })}
        </div>
      )}

      {registry.length > 0 && (
        <div className="border rounded-xl border-border/50 overflow-hidden">
          <div className="px-6 py-4 bg-muted/50 border-b">
            <h3 className="font-bold text-foreground">Master Registry Overview</h3>
          </div>
          <table className="w-full text-left">
            <thead>
              <tr className="bg-muted/40 text-[10px] uppercase text-muted-foreground">
                <th className="px-6 py-3">Registry Type</th>
                <th className="px-6 py-3">Form</th>
                <th className="px-6 py-3">Map Layer</th>
                <th className="px-6 py-3 text-right">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-border">
              {registry.map((r) => (
                <tr key={r.type} className="hover:bg-muted/30">
                  <td className="px-6 py-4 font-bold text-sm">{r.label ?? r.type}</td>
                  <td className="px-6 py-4 text-xs text-muted-foreground uppercase">{r.form || "—"}</td>
                  <td className="px-6 py-4 text-xs">
                    {r.has_coords ? (
                      <Badge variant="secondary" className="text-[9px]">Active Layer</Badge>
                    ) : (
                      <span className="text-[9px] uppercase text-muted-foreground">Spatial N/A</span>
                    )}
                  </td>
                  <td className="px-6 py-4 text-right">
                    <Button render={<Link href={`/admin/heritage/${r.type}`} />} variant="outline" size="sm" className="rounded-lg">
                      Manage Directory
                    </Button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
