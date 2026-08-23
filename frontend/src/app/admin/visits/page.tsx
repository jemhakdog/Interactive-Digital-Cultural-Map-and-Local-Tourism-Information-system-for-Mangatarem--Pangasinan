"use client";

import { useCallback, useEffect, useState, useMemo } from "react";
import { useAuth } from "@/lib/auth";
import { useRouter } from "next/navigation";
import Link from "next/link";
import {
  Loader2,
  TrendingUp,
  CalendarDays,
  MapPin,
  Users,
  Calendar,
  Layers,
  ArrowRight,
  Search,
  Filter,
  CheckCircle2,
  Building2,
  Compass,
  FileSpreadsheet,
  RefreshCw,
  BarChart3,
  Map as MapIcon,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent } from "@/components/ui/card";
import { fetchAPI } from "@/lib/api";

interface VisitStats {
  total?: number;
  month_total?: number;
  top_location?: string;
}

interface VisitLogEntry {
  id: number;
  visitor_name?: string | null;
  visitor_age?: number | null;
  visitor_address?: string | null;
  target_type: string;
  target_id: number;
  target_name?: string | null;
  visit_date?: string | null;
  steward?: string | null;
  visitor_count: number;
  is_system_user: boolean;
  created_at?: string | null;
}

interface VisitorRegistryResponse {
  visitors: VisitLogEntry[];
  total: number;
}

interface LocationSummary {
  name: string;
  type: string;
  count: number;
}

interface DailyTrendPoint {
  day: string;
  count: number;
}

type PresetKey = "today" | "7d" | "30d" | "month" | "ytd" | "all";

export default function AdminVisitsPage() {
  const { user, loading: authLoading } = useAuth();
  const router = useRouter();

  const [stats, setStats] = useState<VisitStats>({});
  const [logs, setLogs] = useState<VisitLogEntry[]>([]);
  const [totalLogsCount, setTotalLogsCount] = useState<number>(0);
  const [loading, setLoading] = useState(true);
  const [exporting, setExporting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const [activePreset, setActivePreset] = useState<PresetKey>("30d");
  const [period, setPeriod] = useState({ start_date: "", end_date: "" });
  const [searchQuery, setSearchQuery] = useState("");
  const [selectedType, setSelectedType] = useState<"all" | "attraction" | "establishment">("all");

  useEffect(() => {
    if (!authLoading && (!user || user.role !== "admin")) {
      router.push("/dashboard");
    }
  }, [user, authLoading, router]);

  // Helper to compute date range strings
  const computePresetDates = useCallback((preset: PresetKey) => {
    const today = new Date();
    const formatDate = (d: Date) => d.toISOString().split("T")[0];
    const todayStr = formatDate(today);

    switch (preset) {
      case "today":
        return { start_date: todayStr, end_date: todayStr };
      case "7d": {
        const d = new Date();
        d.setDate(d.getDate() - 7);
        return { start_date: formatDate(d), end_date: todayStr };
      }
      case "30d": {
        const d = new Date();
        d.setDate(d.getDate() - 30);
        return { start_date: formatDate(d), end_date: todayStr };
      }
      case "month": {
        const startOfMonth = new Date(today.getFullYear(), today.getMonth(), 1);
        return { start_date: formatDate(startOfMonth), end_date: todayStr };
      }
      case "ytd": {
        const startOfYear = new Date(today.getFullYear(), 0, 1);
        return { start_date: formatDate(startOfYear), end_date: todayStr };
      }
      case "all":
        return { start_date: "", end_date: "" };
    }
  }, []);

  // Initialize with 30d preset on first load
  useEffect(() => {
    const initial = computePresetDates("30d");
    setPeriod(initial);
  }, [computePresetDates]);

  const loadData = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const params = new URLSearchParams();
      if (period.start_date) params.set("start_date", period.start_date);
      if (period.end_date) params.set("end_date", period.end_date);
      const qs = params.toString();

      const [statsData, registryData] = await Promise.allSettled([
        fetchAPI<VisitStats>(`/api/visits${qs ? `?${qs}` : ""}`),
        fetchAPI<VisitorRegistryResponse>(`/api/visitor-registry?per_page=100${qs ? `&${qs}` : ""}`),
      ]);

      if (statsData.status === "fulfilled") {
        setStats(statsData.value);
      }
      if (registryData.status === "fulfilled") {
        setLogs(registryData.value.visitors || []);
        setTotalLogsCount(registryData.value.total || 0);
      }
    } catch {
      setError("Failed to load visitor traffic analytics. Please try again.");
    } finally {
      setLoading(false);
    }
  }, [period.start_date, period.end_date]);

  useEffect(() => {
    if (!user || user.role !== "admin") return;
    loadData();
  }, [user, loadData]);

  const handleSelectPreset = (preset: PresetKey) => {
    setActivePreset(preset);
    setPeriod(computePresetDates(preset));
  };

  const handleCustomDateChange = (type: "start_date" | "end_date", value: string) => {
    setActivePreset("all");
    setPeriod((p) => ({ ...p, [type]: value }));
  };

  // Client-Side CSV Export Function
  const exportToCSV = () => {
    if (!logs.length) return;
    setExporting(true);

    try {
      const headers = [
        "Log ID",
        "Visitor Name",
        "Group Size",
        "Destination Type",
        "Destination Name",
        "Visit Date",
        "Visitor Address / Origin",
        "Visitor Age",
        "Registered By Steward",
        "Platform User",
        "Created At",
      ];

      const csvRows = logs.map((log) => [
        log.id,
        `"${(log.visitor_name || "Anonymous").replace(/"/g, '""')}"`,
        log.visitor_count || 1,
        log.target_type === "establishment" ? "Business" : "Attraction",
        `"${(log.target_name || "Unspecified").replace(/"/g, '""')}"`,
        log.visit_date || "",
        `"${(log.visitor_address || "N/A").replace(/"/g, '""')}"`,
        log.visitor_age ?? "N/A",
        `"${(log.steward || "Self / Kiosk").replace(/"/g, '""')}"`,
        log.is_system_user ? "Yes" : "No",
        log.created_at || "",
      ]);

      const csvContent = "\uFEFF" + [headers.join(","), ...csvRows.map((r) => r.join(","))].join("\n");
      const blob = new Blob([csvContent], { type: "text/csv;charset=utf-8;" });
      const url = URL.createObjectURL(blob);
      const link = document.createElement("a");
      const dateTag = period.start_date ? `${period.start_date}_to_${period.end_date || "present"}` : "all_time";
      link.setAttribute("href", url);
      link.setAttribute("download", `Mangatarem_Visitor_Footprint_Report_${dateTag}.csv`);
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      URL.revokeObjectURL(url);
    } catch {
      // ignore
    } finally {
      setExporting(false);
    }
  };

  // Derived Analytics Metrics
  const totalVisitorsCount = stats.total ?? logs.reduce((acc, curr) => acc + (curr.visitor_count || 1), 0);
  const avgGroupSize = logs.length > 0 ? (totalVisitorsCount / logs.length).toFixed(1) : "1.0";

  // Location share calculations
  const locationBreakdown: LocationSummary[] = useMemo(() => {
    const map = new globalThis.Map<string, LocationSummary>();
    logs.forEach((log) => {
      const name = log.target_name || "Unknown";
      const current = map.get(name) || { name, type: log.target_type, count: 0 };
      current.count += log.visitor_count || 1;
      map.set(name, current);
    });

    const sorted = Array.from(map.values()).sort((a, b) => b.count - a.count);
    return sorted.slice(0, 5);
  }, [logs]);

  // Attraction vs Business Breakdown
  const typeStats = useMemo(() => {
    let attractionVisitors = 0;
    let businessVisitors = 0;

    logs.forEach((l) => {
      if (l.target_type === "establishment" || l.target_type === "business") {
        businessVisitors += l.visitor_count || 1;
      } else {
        attractionVisitors += l.visitor_count || 1;
      }
    });

    const total = attractionVisitors + businessVisitors || 1;
    return {
      attractionVisitors,
      businessVisitors,
      attractionPct: Math.round((attractionVisitors / total) * 100),
      businessPct: Math.round((businessVisitors / total) * 100),
    };
  }, [logs]);

  // Daily Trend aggregation for SVG Line Chart
  const dailyTrend: DailyTrendPoint[] = useMemo(() => {
    const dayMap = new globalThis.Map<string, number>();
    logs.forEach((log) => {
      const dateKey = log.visit_date || (log.created_at ? log.created_at.split("T")[0] : "");
      if (!dateKey) return;
      dayMap.set(dateKey, (dayMap.get(dateKey) || 0) + (log.visitor_count || 1));
    });

    return Array.from(dayMap.entries())
      .map(([day, count]) => ({ day, count }))
      .sort((a, b) => a.day.localeCompare(b.day))
      .slice(-14);
  }, [logs]);

  // Filtered log entries for preview
  const filteredLogs = useMemo(() => {
    return logs.filter((log) => {
      const matchesSearch =
        !searchQuery ||
        (log.visitor_name?.toLowerCase().includes(searchQuery.toLowerCase()) ?? false) ||
        (log.target_name?.toLowerCase().includes(searchQuery.toLowerCase()) ?? false) ||
        (log.visitor_address?.toLowerCase().includes(searchQuery.toLowerCase()) ?? false);

      const matchesType =
        selectedType === "all" ||
        (selectedType === "establishment"
          ? log.target_type === "establishment" || log.target_type === "business"
          : log.target_type === "attraction");

      return matchesSearch && matchesType;
    });
  }, [logs, searchQuery, selectedType]);

  if (authLoading || !user) {
    return (
      <div className="flex min-h-[60vh] items-center justify-center py-16">
        <div className="flex flex-col items-center gap-3">
          <Loader2 className="h-8 w-8 animate-spin text-primary" />
          <p className="text-sm text-muted-foreground animate-pulse">Loading Visitor Traffic...</p>
        </div>
      </div>
    );
  }

  const kpiCards = [
    {
      label: "Period Visitors",
      value: totalVisitorsCount.toLocaleString(),
      subtitle: activePreset !== "all" ? `Filtered in ${activePreset.toUpperCase()}` : "Selected Period",
      icon: TrendingUp,
      color: "text-emerald-600 dark:text-emerald-400 bg-emerald-500/10",
    },
    {
      label: "Visitors This Month",
      value: (stats.month_total ?? 0).toLocaleString(),
      subtitle: "Current calendar month",
      icon: CalendarDays,
      color: "text-blue-600 dark:text-blue-400 bg-blue-500/10",
    },
    {
      label: "Top Destination",
      value: stats.top_location || (locationBreakdown[0]?.name ?? "—"),
      subtitle: locationBreakdown[0] ? `${locationBreakdown[0].count} total visits` : "No visits recorded",
      icon: MapPin,
      color: "text-amber-600 dark:text-amber-400 bg-amber-500/10",
      truncate: true,
    },
    {
      label: "Average Group Size",
      value: `${avgGroupSize} pers.`,
      subtitle: `Based on ${logs.length} registry records`,
      icon: Users,
      color: "text-indigo-600 dark:text-indigo-400 bg-indigo-500/10",
    },
  ];

  return (
    <div className="container mx-auto px-4 py-8 max-w-6xl space-y-8">
      {/* Header Banner */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-2 border-b border-border/60">
        <div className="space-y-1">
          <div className="flex items-center gap-2">
            <Badge variant="outline" className="bg-primary/5 text-primary border-primary/20 px-2.5 py-0.5 text-xs font-semibold rounded-full">
              <MapIcon className="h-3.5 w-3.5 mr-1" /> Tourism Footprint & Analytics
            </Badge>
          </div>
          <h1 className="text-3xl font-extrabold tracking-tight text-foreground">
            Visitor Traffic & Momentum
          </h1>
          <p className="text-sm text-muted-foreground">
            Real-time monitoring of on-site foot traffic, destination popularity, and steward log streams.
          </p>
        </div>

        <div className="flex flex-wrap items-center gap-2.5">
          <Button
            onClick={loadData}
            variant="outline"
            size="sm"
            disabled={loading}
            className="rounded-xl gap-2 font-medium cursor-pointer"
          >
            <RefreshCw className={`h-4 w-4 ${loading ? "animate-spin" : ""}`} /> Refresh
          </Button>

          <Button
            onClick={exportToCSV}
            size="sm"
            disabled={exporting || logs.length === 0}
            className="rounded-xl shadow-sm gap-2 font-semibold cursor-pointer bg-emerald-600 hover:bg-emerald-700 text-white"
          >
            <FileSpreadsheet className="h-4 w-4" /> {exporting ? "Generating CSV..." : "Export CSV Report"}
          </Button>

          <Link href="/admin/visitor-registry">
            <Button size="sm" variant="secondary" className="rounded-xl gap-2 font-medium cursor-pointer">
              <Layers className="h-4 w-4" /> Full Registry <ArrowRight className="h-3.5 w-3.5" />
            </Button>
          </Link>
        </div>
      </div>

      {/* Date Filter & Preset Controls */}
      <Card className="border-border/60 shadow-sm bg-card/60 backdrop-blur">
        <CardContent className="p-5 space-y-4">
          <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-4">
            {/* Quick Preset Buttons */}
            <div className="flex items-center gap-1.5 flex-wrap">
              <span className="text-xs font-semibold text-muted-foreground mr-1 flex items-center gap-1">
                <Filter className="h-3.5 w-3.5" /> Presets:
              </span>
              {(
                [
                  { id: "today", label: "Today" },
                  { id: "7d", label: "7 Days" },
                  { id: "30d", label: "30 Days" },
                  { id: "month", label: "This Month" },
                  { id: "ytd", label: "Year to Date" },
                  { id: "all", label: "All Time" },
                ] as const
              ).map((preset) => (
                <button
                  key={preset.id}
                  type="button"
                  onClick={() => handleSelectPreset(preset.id)}
                  className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-all cursor-pointer ${
                    activePreset === preset.id
                      ? "bg-primary text-primary-foreground shadow-sm"
                      : "bg-muted hover:bg-accent text-muted-foreground hover:text-foreground"
                  }`}
                >
                  {preset.label}
                </button>
              ))}
            </div>

            {/* Custom Date Pickers */}
            <div className="flex items-center gap-2 flex-wrap sm:flex-nowrap">
              <div className="flex items-center gap-1.5 bg-background border border-border rounded-xl px-3 py-1.5 shadow-sm">
                <Calendar className="h-3.5 w-3.5 text-muted-foreground shrink-0" />
                <span className="text-[11px] font-medium text-muted-foreground">From:</span>
                <input
                  type="date"
                  value={period.start_date}
                  onChange={(e) => handleCustomDateChange("start_date", e.target.value)}
                  className="text-xs bg-transparent border-0 outline-none text-foreground cursor-pointer focus:ring-0"
                />
              </div>

              <div className="flex items-center gap-1.5 bg-background border border-border rounded-xl px-3 py-1.5 shadow-sm">
                <Calendar className="h-3.5 w-3.5 text-muted-foreground shrink-0" />
                <span className="text-[11px] font-medium text-muted-foreground">To:</span>
                <input
                  type="date"
                  value={period.end_date}
                  onChange={(e) => handleCustomDateChange("end_date", e.target.value)}
                  className="text-xs bg-transparent border-0 outline-none text-foreground cursor-pointer focus:ring-0"
                />
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      {error && (
        <div className="p-4 rounded-2xl border border-destructive/30 bg-destructive/10 text-destructive text-sm font-medium">
          {error}
        </div>
      )}

      {/* KPI Cards Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {kpiCards.map((c) => (
          <Card key={c.label} className="border-border/60 shadow-sm bg-card hover:border-primary/30 transition-colors">
            <CardContent className="p-5 flex flex-col justify-between h-full space-y-4">
              <div className="flex items-center justify-between">
                <p className="text-xs font-semibold text-muted-foreground uppercase tracking-wider">{c.label}</p>
                <div className={`flex h-9 w-9 shrink-0 items-center justify-center rounded-xl ${c.color}`}>
                  <c.icon className="h-4 w-4" />
                </div>
              </div>
              <div>
                <p className={`text-2xl md:text-3xl font-extrabold tracking-tight text-foreground ${c.truncate ? "truncate" : ""}`}>
                  {c.value}
                </p>
                <p className="text-xs text-muted-foreground mt-1">{c.subtitle}</p>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Data Visualization Grid: Trend & Leaderboard */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Visitor Trend Chart (2 columns on lg) */}
        <Card className="lg:col-span-2 border-border/60 shadow-sm">
          <CardContent className="p-6 space-y-6">
            <div className="flex items-center justify-between">
              <div>
                <h3 className="text-lg font-bold tracking-tight text-foreground flex items-center gap-2">
                  <BarChart3 className="h-5 w-5 text-primary" /> Daily Foot Traffic Activity
                </h3>
                <p className="text-xs text-muted-foreground">
                  Visitor volume fluctuation in the selected period
                </p>
              </div>
              <Badge variant="secondary" className="text-xs font-semibold">
                {dailyTrend.length > 0 ? `${dailyTrend.length} Data Points` : "No Activity"}
              </Badge>
            </div>

            {/* SVG Visualizer */}
            {dailyTrend.length > 0 ? (
              <div className="space-y-4 pt-2">
                <div className="h-44 w-full flex items-end gap-2 sm:gap-3 px-2 pt-6 pb-2 border-b border-border/60">
                  {(() => {
                    const maxVal = Math.max(...dailyTrend.map((d) => d.count), 1);
                    return dailyTrend.map((point) => {
                      const heightPct = Math.max(12, Math.round((point.count / maxVal) * 100));
                      const label = point.day.slice(5); // MM-DD
                      return (
                        <div key={point.day} className="flex-1 flex flex-col items-center gap-1.5 group relative h-full justify-end">
                          {/* Tooltip on hover */}
                          <div className="absolute -top-9 hidden group-hover:flex flex-col items-center z-20 pointer-events-none">
                            <span className="bg-foreground text-background text-[10px] font-bold px-2 py-1 rounded shadow-lg whitespace-nowrap">
                              {point.day}: {point.count} {point.count === 1 ? "visitor" : "visitors"}
                            </span>
                            <div className="w-1.5 h-1.5 bg-foreground rotate-45 -mt-0.5" />
                          </div>

                          <div
                            style={{ height: `${heightPct}%` }}
                            className="w-full max-w-[36px] bg-gradient-to-t from-primary/80 to-primary rounded-t-lg group-hover:brightness-110 transition-all duration-200"
                          />
                          <span className="text-[10px] font-medium text-muted-foreground group-hover:text-foreground transition-colors truncate">
                            {label}
                          </span>
                        </div>
                      );
                    });
                  })()}
                </div>

                <div className="flex items-center justify-between text-xs text-muted-foreground pt-1">
                  <span>Start of Period: <strong className="text-foreground">{dailyTrend[0]?.day}</strong></span>
                  <span>Latest Activity: <strong className="text-foreground">{dailyTrend[dailyTrend.length - 1]?.day}</strong></span>
                </div>
              </div>
            ) : (
              <div className="py-14 text-center border border-dashed border-border rounded-2xl">
                <TrendingUp className="h-8 w-8 mx-auto mb-2 text-muted-foreground/40" />
                <p className="text-sm font-semibold text-foreground">No traffic logs in this date range</p>
                <p className="text-xs text-muted-foreground mt-0.5">Try widening your date filters or registering a visitor.</p>
              </div>
            )}

            {/* Type Distribution Split Bar */}
            <div className="pt-4 border-t border-border/40 space-y-2.5">
              <div className="flex items-center justify-between text-xs font-semibold">
                <span className="flex items-center gap-1.5 text-emerald-600 dark:text-emerald-400">
                  <Compass className="h-4 w-4" /> Attractions ({typeStats.attractionPct}%)
                </span>
                <span className="flex items-center gap-1.5 text-teal-600 dark:text-teal-400">
                  <Building2 className="h-4 w-4" /> Local Businesses ({typeStats.businessPct}%)
                </span>
              </div>
              <div className="h-3 w-full rounded-full bg-muted overflow-hidden flex">
                <div
                  style={{ width: `${typeStats.attractionPct}%` }}
                  className="bg-emerald-500 transition-all duration-300"
                />
                <div
                  style={{ width: `${typeStats.businessPct}%` }}
                  className="bg-teal-500 transition-all duration-300"
                />
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Top Locations Leaderboard */}
        <Card className="border-border/60 shadow-sm flex flex-col justify-between">
          <CardContent className="p-6 space-y-5">
            <div>
              <h3 className="text-lg font-bold tracking-tight text-foreground flex items-center gap-2">
                <MapPin className="h-5 w-5 text-amber-500" /> Top Visited Venues
              </h3>
              <p className="text-xs text-muted-foreground">
                Ranked by cumulative visitor check-in volume
              </p>
            </div>

            {locationBreakdown.length > 0 ? (
              <div className="space-y-3.5">
                {locationBreakdown.map((item, index) => {
                  const maxLoc = locationBreakdown[0]?.count || 1;
                  const pct = Math.round((item.count / maxLoc) * 100);
                  return (
                    <div key={item.name} className="space-y-1.5">
                      <div className="flex items-center justify-between text-xs">
                        <span className="font-semibold text-foreground flex items-center gap-1.5 truncate max-w-[190px]">
                          <span className="flex h-5 w-5 shrink-0 items-center justify-center rounded-full bg-muted font-bold text-[10px]">
                            {index + 1}
                          </span>
                          {item.name}
                        </span>
                        <span className="font-bold text-foreground shrink-0">
                          {item.count} <span className="text-[10px] font-normal text-muted-foreground">visits</span>
                        </span>
                      </div>
                      <div className="h-2 w-full rounded-full bg-muted overflow-hidden">
                        <div
                          style={{ width: `${pct}%` }}
                          className={`h-full rounded-full transition-all duration-300 ${
                            index === 0 ? "bg-amber-500" : index === 1 ? "bg-primary" : "bg-muted-foreground/60"
                          }`}
                        />
                      </div>
                    </div>
                  );
                })}
              </div>
            ) : (
              <div className="py-12 text-center border border-dashed border-border rounded-2xl">
                <p className="text-xs text-muted-foreground">No destinations recorded yet.</p>
              </div>
            )}

            <div className="pt-2">
              <Link href="/admin/attractions">
                <Button variant="outline" size="sm" className="w-full rounded-xl text-xs font-semibold cursor-pointer">
                  Manage Tourism Locations <ArrowRight className="h-3.5 w-3.5 ml-1.5" />
                </Button>
              </Link>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Recent Visitor Logs Stream Preview */}
      <Card className="border-border/60 shadow-sm">
        <CardContent className="p-6 space-y-5">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
            <div>
              <h3 className="text-lg font-bold tracking-tight text-foreground flex items-center gap-2">
                <Users className="h-5 w-5 text-primary" /> Recent Visitor Registry Logs
              </h3>
              <p className="text-xs text-muted-foreground">
                Displaying {filteredLogs.length} of {totalLogsCount} recorded visitor entries
              </p>
            </div>

            {/* Table Filters */}
            <div className="flex flex-wrap items-center gap-2.5">
              <div className="relative min-w-[200px]">
                <Search className="h-3.5 w-3.5 absolute left-3 top-1/2 -translate-y-1/2 text-muted-foreground" />
                <input
                  type="text"
                  placeholder="Search visitor or venue..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="w-full rounded-xl border border-border bg-background pl-8 pr-3 py-1.5 text-xs text-foreground outline-none focus:ring-2 focus:ring-primary/40"
                />
              </div>

              <div className="flex items-center gap-1 bg-muted p-1 rounded-xl">
                <button
                  type="button"
                  onClick={() => setSelectedType("all")}
                  className={`px-2.5 py-1 rounded-lg text-xs font-semibold transition-all cursor-pointer ${
                    selectedType === "all" ? "bg-background text-foreground shadow-sm" : "text-muted-foreground"
                  }`}
                >
                  All
                </button>
                <button
                  type="button"
                  onClick={() => setSelectedType("attraction")}
                  className={`px-2.5 py-1 rounded-lg text-xs font-semibold transition-all cursor-pointer ${
                    selectedType === "attraction" ? "bg-background text-foreground shadow-sm" : "text-muted-foreground"
                  }`}
                >
                  Attractions
                </button>
                <button
                  type="button"
                  onClick={() => setSelectedType("establishment")}
                  className={`px-2.5 py-1 rounded-lg text-xs font-semibold transition-all cursor-pointer ${
                    selectedType === "establishment" ? "bg-background text-foreground shadow-sm" : "text-muted-foreground"
                  }`}
                >
                  Businesses
                </button>
              </div>
            </div>
          </div>

          {/* Table Container */}
          <div className="rounded-2xl border border-border/60 overflow-hidden">
            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs">
                <thead className="bg-muted/60 text-muted-foreground font-semibold border-b border-border/60">
                  <tr>
                    <th className="py-3 px-4">Visitor</th>
                    <th className="py-3 px-4">Group Size</th>
                    <th className="py-3 px-4">Destination</th>
                    <th className="py-3 px-4">Origin / Address</th>
                    <th className="py-3 px-4">Visit Date</th>
                    <th className="py-3 px-4">Steward</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-border/40">
                  {filteredLogs.slice(0, 10).map((log) => (
                    <tr key={log.id} className="hover:bg-muted/30 transition-colors">
                      <td className="py-3 px-4">
                        <div className="font-semibold text-foreground">
                          {log.visitor_name || "Anonymous Visitor"}
                        </div>
                        {log.is_system_user && (
                          <span className="text-[10px] text-primary flex items-center gap-1 font-medium">
                            <CheckCircle2 className="h-3 w-3 inline" /> Verified User
                          </span>
                        )}
                      </td>
                      <td className="py-3 px-4">
                        <span className="font-bold text-foreground bg-primary/10 text-primary px-2.5 py-0.5 rounded-full text-[11px]">
                          {log.visitor_count} {log.visitor_count === 1 ? "person" : "pax"}
                        </span>
                      </td>
                      <td className="py-3 px-4">
                        <div className="font-medium text-foreground">{log.target_name || "Unspecified"}</div>
                        <span className="text-[10px] text-muted-foreground uppercase tracking-wider font-semibold">
                          {log.target_type === "establishment" ? "Business" : "Attraction"}
                        </span>
                      </td>
                      <td className="py-3 px-4 text-muted-foreground">
                        {log.visitor_address || "—"}
                      </td>
                      <td className="py-3 px-4 font-medium text-foreground">
                        {log.visit_date || (log.created_at ? log.created_at.split("T")[0] : "—")}
                      </td>
                      <td className="py-3 px-4 text-muted-foreground">
                        {log.steward || "Self / Online"}
                      </td>
                    </tr>
                  ))}

                  {filteredLogs.length === 0 && (
                    <tr>
                      <td colSpan={6} className="py-10 text-center text-muted-foreground">
                        No visitor logs matching the search criteria.
                      </td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>
          </div>

          <div className="flex items-center justify-between pt-2">
            <span className="text-xs text-muted-foreground">
              Showing top {Math.min(10, filteredLogs.length)} recent entries
            </span>
            <Link href="/admin/visitor-registry">
              <Button variant="ghost" size="sm" className="rounded-xl text-xs font-semibold gap-1.5 cursor-pointer">
                View All in Visitor Registry <ArrowRight className="h-3.5 w-3.5" />
              </Button>
            </Link>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}

