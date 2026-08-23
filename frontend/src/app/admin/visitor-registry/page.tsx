"use client";

import { useEffect, useState } from "react";
import { useAuth } from "@/lib/auth";
import { fetchAPI } from "@/lib/api";
import { useRouter } from "next/navigation";
import { Loader2, Users, Download } from "lucide-react";
import { Button } from "@/components/ui/button";

interface VisitLog {
  id: number;
  visitor_name: string;
  visitor_age?: number | null;
  visitor_address?: string | null;
  target_name?: string;
  target_type?: string;
  visit_date?: string;
  steward?: string;
  visitor_count?: number;
  is_system_user?: boolean;
}

export default function AdminVisitorRegistryPage() {
  const { user, loading: authLoading } = useAuth();
  const router = useRouter();
  const [logs, setLogs] = useState<VisitLog[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [filters, setFilters] = useState({
    target_type: "",
    target_id: "",
    start_date: "",
    end_date: "",
    search: "",
  });

  useEffect(() => {
    if (!authLoading && (!user || user.role !== "admin")) router.push("/dashboard");
  }, [user, authLoading, router]);

  useEffect(() => {
    if (!user || user.role !== "admin") return;
    let cancelled = false;
    const load = async () => {
      setLoading(true);
      setError(null);
      try {
        const params = new URLSearchParams();
        if (filters.target_type) params.set("target_type", filters.target_type);
        if (filters.target_id) params.set("target_id", filters.target_id);
        if (filters.start_date) params.set("start_date", filters.start_date);
        if (filters.end_date) params.set("end_date", filters.end_date);
        if (filters.search) params.set("search", filters.search);
        const data = await fetchAPI<{ visitors: VisitLog[]; total: number }>(
          `/api/visitor-registry?${params.toString()}`
        );
        if (!cancelled) setLogs(data.visitors ?? []);
      } catch (err) {
        if (!cancelled) {
          setLogs([]);
          setError(err instanceof Error ? err.message : "Failed to load visitor registry.");
        }
      } finally {
        if (!cancelled) setLoading(false);
      }
    };
    load();
    return () => {
      cancelled = true;
    };
  }, [user, filters]);

  if (authLoading || !user || loading) {
    return (
      <div className="flex justify-center py-16">
        <Loader2 className="h-6 w-6 animate-spin text-muted-foreground" />
      </div>
    );
  }

  const update = (key: keyof typeof filters, value: string) =>
    setFilters((f) => ({ ...f, [key]: value }));

  return (
    <div className="container mx-auto px-4 py-8 max-w-5xl space-y-6">
      <div className="flex items-center justify-between gap-4">
        <div className="flex items-center gap-3">
          <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-primary/10 text-primary">
            <Users className="h-5 w-5" />
          </div>
          <div>
            <h1 className="text-3xl font-bold tracking-tight">Visitor Registry</h1>
            <p className="text-muted-foreground text-sm mt-0.5">
              Master database of all identified tourism momentum
            </p>
          </div>
        </div>
        {/* TODO: backend has no export endpoint — add GET /api/visitor-registry/export (CSV) before enabling. */}
        <Button variant="outline" className="gap-2 rounded-xl" disabled title="Export not available yet">
          <Download className="h-4 w-4" /> Export Dataset
        </Button>
      </div>

      <div className="border rounded-xl border-border/50 p-5 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
        <div className="space-y-1.5">
          <label className="block text-[10px] font-black uppercase tracking-wider text-muted-foreground">
            Target Type
          </label>
          <select
            value={filters.target_type}
            onChange={(e) => update("target_type", e.target.value)}
            className="w-full rounded-lg border border-border bg-background px-3 py-2 text-sm text-foreground outline-none focus:ring-2 focus:ring-primary/40"
          >
            <option value="">All Types</option>
            <option value="attraction">Attractions</option>
            <option value="business">Businesses</option>
          </select>
        </div>
        <div className="space-y-1.5">
          <label className="block text-[10px] font-black uppercase tracking-wider text-muted-foreground">
            Date From
          </label>
          <input
            type="date"
            value={filters.start_date}
            onChange={(e) => update("start_date", e.target.value)}
            className="w-full rounded-lg border border-border bg-background px-3 py-2 text-sm text-foreground outline-none focus:ring-2 focus:ring-primary/40"
          />
        </div>
        <div className="space-y-1.5">
          <label className="block text-[10px] font-black uppercase tracking-wider text-muted-foreground">
            Date To
          </label>
          <input
            type="date"
            value={filters.end_date}
            onChange={(e) => update("end_date", e.target.value)}
            className="w-full rounded-lg border border-border bg-background px-3 py-2 text-sm text-foreground outline-none focus:ring-2 focus:ring-primary/40"
          />
        </div>
        <div className="space-y-1.5 sm:col-span-2 lg:col-span-1">
          <label className="block text-[10px] font-black uppercase tracking-wider text-muted-foreground">
            Visitor Name
          </label>
          <input
            type="text"
            value={filters.search}
            onChange={(e) => update("search", e.target.value)}
            placeholder="Search name..."
            className="w-full rounded-lg border border-border bg-background px-3 py-2 text-sm text-foreground outline-none focus:ring-2 focus:ring-primary/40"
          />
        </div>
      </div>

      <div className="border rounded-xl border-border/50 overflow-hidden">
        <table className="w-full text-left">
          <thead>
            <tr className="bg-muted/50 text-[10px] uppercase text-muted-foreground">
              <th className="px-6 py-4">Visitor Identity</th>
              <th className="px-6 py-4">Age</th>
              <th className="px-6 py-4">Origin</th>
              <th className="px-6 py-4">Location Visited</th>
              <th className="px-6 py-4">Date</th>
              <th className="px-6 py-4">Logged By</th>
            </tr>
          </thead>
          <tbody>
            {logs.length === 0 ? (
              <tr>
                <td colSpan={6} className="text-center text-muted-foreground py-16">
                  <Users className="h-10 w-10 mx-auto mb-3 text-muted-foreground/40" />
                  {error ? (
                    <>
                      <p className="font-bold text-destructive">Failed to load visitor registry</p>
                      <p className="text-xs text-muted-foreground mt-1">{error}</p>
                    </>
                  ) : (
                    <>
                      <p className="font-bold text-foreground">No detailed records found</p>
                      <p className="text-xs text-muted-foreground mt-1">
                        Detailed logs will appear here as check-ins are recorded.
                      </p>
                    </>
                  )}
                </td>
              </tr>
            ) : (
              logs.map((log) => (
                <tr key={log.id} className="border-t border-border">
                  <td className="px-6 py-4">{log.visitor_name}</td>
                  <td className="px-6 py-4 text-sm">{log.visitor_age ?? "—"}</td>
                  <td className="px-6 py-4 text-sm">{log.visitor_address ?? "Not provided"}</td>
                  <td className="px-6 py-4 text-sm">
                    {log.target_name}
                    <span className="block text-[9px] uppercase text-blue-600">{log.target_type}</span>
                  </td>
                  <td className="px-6 py-4 text-sm">{log.visit_date ?? "—"}</td>
                  <td className="px-6 py-4 text-sm">{log.steward ?? "—"}</td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
