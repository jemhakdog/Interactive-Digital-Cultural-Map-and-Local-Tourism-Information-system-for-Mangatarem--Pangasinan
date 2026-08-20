"use client";

import { useEffect, useState } from "react";
import { useAuth } from "@/lib/auth";
import { useRouter } from "next/navigation";
import { Loader2, TrendingUp, CalendarDays, MapPin, Download } from "lucide-react";
import { Button } from "@/components/ui/button";

interface VisitStats {
  total?: number;
  month_total?: number;
  top_location?: string;
}

export default function AdminVisitsPage() {
  const { user, loading: authLoading } = useAuth();
  const router = useRouter();
  // TODO: FastAPI visitor analytics (per-establishment/attraction history) not implemented yet — using local placeholder state.
  const [stats] = useState<VisitStats>({});
  const [loading, setLoading] = useState(true);
  const [period, setPeriod] = useState({ start_date: "", end_date: "" });

  useEffect(() => {
    if (!authLoading && (!user || user.role !== "admin")) router.push("/dashboard");
  }, [user, authLoading, router]);

  useEffect(() => {
    if (!user) return;
    // No analytics read endpoint for the registry yet; placeholder stats stay empty.
    setLoading(false);
  }, [user]);

  if (authLoading || !user || loading) {
    return (
      <div className="flex justify-center py-16">
        <Loader2 className="h-6 w-6 animate-spin text-muted-foreground" />
      </div>
    );
  }

  const cards = [
    { label: "Period Visitors", value: stats.total ?? 0, icon: TrendingUp, tint: "bg-primary/10 text-primary" },
    { label: "Visitors This Month", value: stats.month_total ?? 0, icon: CalendarDays, tint: "bg-blue-50 text-blue-600" },
    {
      label: "Top Location",
      value: stats.top_location ?? "—",
      icon: MapPin,
      tint: "bg-amber-50 text-amber-600",
    },
  ];

  return (
    <div className="container mx-auto px-4 py-8 max-w-5xl space-y-6">
      <div className="flex items-center gap-3">
        <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-primary/10 text-primary">
          <TrendingUp className="h-5 w-5" />
        </div>
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Tourism Analytics</h1>
          <p className="text-muted-foreground text-sm mt-0.5">
            Monitoring visitor footprint and local momentum
          </p>
        </div>
      </div>

      <div className="border rounded-xl border-border/50 p-5 flex flex-col lg:flex-row justify-between items-start lg:items-center gap-4">
        <div>
          <h3 className="font-bold text-foreground">Filter Analytics Period</h3>
          <p className="text-[10px] font-bold uppercase tracking-wider text-muted-foreground mt-0.5">
            Set date boundaries to analyze metrics
          </p>
        </div>
        <div className="flex flex-wrap items-center gap-3">
          <input
            type="date"
            value={period.start_date}
            onChange={(e) => setPeriod((p) => ({ ...p, start_date: e.target.value }))}
            className="rounded-lg border border-border bg-background px-3 py-2.5 text-sm text-foreground outline-none focus:ring-2 focus:ring-primary/40"
          />
          <input
            type="date"
            value={period.end_date}
            onChange={(e) => setPeriod((p) => ({ ...p, end_date: e.target.value }))}
            className="rounded-lg border border-border bg-background px-3 py-2.5 text-sm text-foreground outline-none focus:ring-2 focus:ring-primary/40"
          />
          <Button variant="outline" className="rounded-xl" disabled title="Export not available yet">
            <Download className="h-4 w-4 mr-2" /> Export CSV
          </Button>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {cards.map((c) => (
          <div key={c.label} className="border rounded-3xl border-border/50 p-6 flex flex-col justify-between">
            <div className={`p-3 rounded-2xl w-fit ${c.tint}`}>
              <c.icon className="h-6 w-6" />
            </div>
            <div className="mt-4">
              <p className="text-3xl font-black text-foreground tracking-tight leading-none">
                {typeof c.value === "number" ? c.value : c.value}
              </p>
              <h3 className="text-muted-foreground font-bold uppercase tracking-wider text-[10px] mt-1.5">
                {c.label}
              </h3>
            </div>
          </div>
        ))}
      </div>

      <div className="border border-dashed border-border rounded-2xl py-16 text-center">
        <TrendingUp className="h-10 w-10 mx-auto mb-3 text-muted-foreground/40" />
        <p className="font-bold text-foreground">No analytics data available</p>
        <p className="text-xs text-muted-foreground mt-1">
          The visitor analytics export/report endpoints are not implemented on the backend yet.
        </p>
      </div>
    </div>
  );
}
