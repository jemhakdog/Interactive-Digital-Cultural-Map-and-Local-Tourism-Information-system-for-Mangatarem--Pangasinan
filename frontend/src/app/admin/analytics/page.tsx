"use client";

import { useEffect, useState } from "react";
import { useAuth } from "@/lib/auth";
import { useRouter } from "next/navigation";
import { fetchAPI } from "@/lib/api";
import { Loader2, BarChart3, Users, Eye, CalendarClock } from "lucide-react";

interface AnalyticsSummary {
  visitors?: number;
  page_views?: number;
  visitors_7d?: number;
  [key: string]: unknown;
}

export default function AdminAnalyticsPage() {
  const { user, loading: authLoading } = useAuth();
  const router = useRouter();
  const [summary, setSummary] = useState<AnalyticsSummary | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!authLoading && (!user || user.role !== "admin")) router.push("/dashboard");
  }, [user, authLoading, router]);

  useEffect(() => {
    if (!user) return;
    // GET /api/analytics/summary is Admin-only and exists.
    fetchAPI<AnalyticsSummary>("/api/analytics/summary")
      .then((data) => setSummary(data))
      .catch(() => setError("Analytics summary is not available."))
      .finally(() => setLoading(false));
  }, [user]);

  if (authLoading || !user || loading) {
    return (
      <div className="flex justify-center py-16">
        <Loader2 className="h-6 w-6 animate-spin text-muted-foreground" />
      </div>
    );
  }

  const cards = [
    {
      label: "Total Visitors",
      value: summary?.visitors ?? 0,
      icon: Users,
      tint: "bg-primary/10 text-primary",
    },
    {
      label: "Page Views",
      value: summary?.page_views ?? 0,
      icon: Eye,
      tint: "bg-blue-50 text-blue-600",
    },
    {
      label: "Visitors (7d)",
      value: summary?.visitors_7d ?? 0,
      icon: CalendarClock,
      tint: "bg-amber-50 text-amber-600",
    },
  ];

  return (
    <div className="container mx-auto px-4 py-8 max-w-5xl space-y-6">
      <div className="flex items-center gap-3">
        <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-primary/10 text-primary">
          <BarChart3 className="h-5 w-5" />
        </div>
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Analytics Overview</h1>
          <p className="text-muted-foreground text-sm mt-0.5">
            Platform-wide visitor and engagement metrics
          </p>
        </div>
      </div>

      {error && (
        <div className="rounded-lg border border-border bg-muted px-4 py-3 text-sm text-muted-foreground">
          {error}
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {cards.map((c) => (
          <div key={c.label} className="border rounded-3xl border-border/50 p-6 flex flex-col justify-between">
            <div className={`p-3 rounded-2xl w-fit ${c.tint}`}>
              <c.icon className="h-6 w-6" />
            </div>
            <div className="mt-4">
              <p className="text-3xl font-black text-foreground tracking-tight leading-none">{c.value}</p>
              <h3 className="text-muted-foreground font-bold uppercase tracking-wider text-[10px] mt-1.5">
                {c.label}
              </h3>
            </div>
          </div>
        ))}
      </div>

      {summary && Object.keys(summary).length === 0 && (
        <div className="border border-dashed border-border rounded-2xl py-16 text-center">
          <BarChart3 className="h-10 w-10 mx-auto mb-3 text-muted-foreground/40" />
          <p className="font-bold text-foreground">No analytics data yet</p>
          <p className="text-xs text-muted-foreground mt-1">
            Metrics will populate as visitors interact with the platform.
          </p>
        </div>
      )}
    </div>
  );
}
