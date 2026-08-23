"use client";

import { useEffect, useState, useCallback, useMemo } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { useAuth } from "@/lib/auth";
import { fetchAPI, APIError } from "@/lib/api";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent } from "@/components/ui/card";
import {
  Sheet,
  SheetContent,
} from "@/components/ui/sheet";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import {
  Loader2,
  Plus,
  Pencil,
  Trash2,
  Calendar,
  Search,
  Eye,
  LayoutGrid,
  List,
  ExternalLink,
  Clock,
  MapPin,
  ShieldAlert,
  CheckCircle2,
  X,
  Sparkles,
  CalendarDays,
  RefreshCw,
  ArrowUpDown,
  Tag,
  Share2,
} from "lucide-react";
import { DeleteDialog } from "@/components/admin-dialogs";

interface Event {
  id: number;
  name: string;
  description?: string | null;
  category: string;
  status: string;
  date: string | null;
  location?: string | null;
  latitude?: number | null;
  longitude?: number | null;
  barangay_name?: string | null;
  barangay_id?: number | null;
  image_url?: string | null;
  created_at?: string | null;
}

const CATEGORY_COLORS: Record<string, string> = {
  Festival: "bg-amber-500/10 text-amber-600 dark:text-amber-400 border-amber-500/20",
  Cultural: "bg-indigo-500/10 text-indigo-600 dark:text-indigo-400 border-indigo-500/20",
  Religious: "bg-sky-500/10 text-sky-600 dark:text-sky-400 border-sky-500/20",
  Sports: "bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 border-emerald-500/20",
  Agricultural: "bg-lime-500/10 text-lime-600 dark:text-lime-400 border-lime-500/20",
  Civic: "bg-rose-500/10 text-rose-600 dark:text-rose-400 border-rose-500/20",
  Community: "bg-teal-500/10 text-teal-600 dark:text-teal-400 border-teal-500/20",
  Tourism: "bg-cyan-500/10 text-cyan-600 dark:text-cyan-400 border-cyan-500/20",
};

export default function AdminEventsPage() {
  const { user, loading: authLoading } = useAuth();
  const router = useRouter();

  const [events, setEvents] = useState<Event[]>([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [actionError, setActionError] = useState<string | null>(null);
  const [successNotice, setSuccessNotice] = useState<string | null>(null);

  // Filters & Controls
  const [searchQuery, setSearchQuery] = useState("");
  const [selectedCategory, setSelectedCategory] = useState<string>("all");
  const [selectedStatus, setSelectedStatus] = useState<string>("all");
  const [timeFilter, setTimeFilter] = useState<"all" | "upcoming" | "past" | "today">("all");
  const [selectedBarangay, setSelectedBarangay] = useState<string>("all");
  const [sortBy, setSortBy] = useState<"date-asc" | "date-desc" | "name" | "newest">("date-desc");
  const [viewMode, setViewMode] = useState<"grid" | "table">("grid");

  // Selection & Modals
  const [inspectTarget, setInspectTarget] = useState<Event | null>(null);
  const [deleteTarget, setDeleteTarget] = useState<Event | null>(null);
  const [editModalTarget, setEditModalTarget] = useState<Event | null>(null);
  const [addModalOpen, setAddModalOpen] = useState(false);
  const [submittingModal, setSubmittingModal] = useState(false);

  // Modal Form State
  const [formData, setFormData] = useState<{
    name: string;
    description: string;
    category: string;
    date: string;
    location: string;
    image_url: string;
  }>({
    name: "",
    description: "",
    category: "Festival",
    date: "",
    location: "",
    image_url: "",
  });

  const loadEvents = useCallback(async () => {
    try {
      const data = await fetchAPI<{ events: Event[] }>("/api/events?status=all");
      setEvents(data?.events ?? []);
    } catch {
      // Fallback if status=all not supported, try base endpoint
      try {
        const data = await fetchAPI<{ events: Event[] }>("/api/events");
        setEvents(data?.events ?? []);
      } catch (err) {
        setActionError(err instanceof APIError ? err.detail : "Failed to load events.");
      }
    }
  }, []);

  useEffect(() => {
    if (!authLoading && (!user || user.role !== "admin")) {
      router.push("/dashboard");
    }
  }, [user, authLoading, router]);

  useEffect(() => {
    if (!user) return;
    loadEvents().finally(() => setLoading(false));
  }, [user, loadEvents]);

  const handleRefresh = async () => {
    setRefreshing(true);
    await loadEvents();
    setRefreshing(false);
  };

  // 1-Click Status Toggle (Approved/Published vs Pending/Draft)
  const handleToggleStatus = async (event: Event) => {
    const current = (event.status || "draft").toLowerCase();
    const nextStatus = current === "approved" || current === "published" ? "draft" : "approved";

    // Optimistic update
    setEvents((prev) =>
      prev.map((e) => (e.id === event.id ? { ...e, status: nextStatus } : e))
    );
    if (inspectTarget?.id === event.id) {
      setInspectTarget({ ...inspectTarget, status: nextStatus });
    }

    try {
      await fetchAPI(`/api/events/${event.id}`, {
        method: "PUT",
        body: JSON.stringify({ status: nextStatus }),
      });
      setSuccessNotice(`"${event.name}" marked as ${nextStatus}.`);
      setTimeout(() => setSuccessNotice(null), 3000);
    } catch (err) {
      // Revert
      setEvents((prev) =>
        prev.map((e) => (e.id === event.id ? { ...e, status: current } : e))
      );
      setActionError(err instanceof APIError ? err.detail : "Failed to update event status.");
    }
  };

  // Delete Action
  const handleDelete = async () => {
    if (!deleteTarget) return;
    try {
      await fetchAPI(`/api/events/${deleteTarget.id}`, { method: "DELETE" });
      setEvents((prev) => prev.filter((e) => e.id !== deleteTarget.id));
      if (inspectTarget?.id === deleteTarget.id) {
        setInspectTarget(null);
      }
      setDeleteTarget(null);
      setSuccessNotice(`Deleted "${deleteTarget.name}".`);
      setTimeout(() => setSuccessNotice(null), 3000);
    } catch (err) {
      setActionError(err instanceof APIError ? err.detail : "Failed to delete event.");
    }
  };

  // Open Edit Modal
  const handleOpenEditModal = (event: Event) => {
    setEditModalTarget(event);
    setFormData({
      name: event.name || "",
      description: event.description || "",
      category: event.category || "Festival",
      date: event.date ? event.date.split("T")[0] : "",
      location: event.location || "",
      image_url: event.image_url || "",
    });
  };

  // Open Add Modal
  const handleOpenAddModal = () => {
    setFormData({
      name: "",
      description: "",
      category: "Festival",
      date: new Date().toISOString().split("T")[0],
      location: "",
      image_url: "",
    });
    setAddModalOpen(true);
  };

  // Submit Edit Form
  const handleSaveEdit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!editModalTarget) return;
    setSubmittingModal(true);
    try {
      await fetchAPI(`/api/events/${editModalTarget.id}`, {
        method: "PUT",
        body: JSON.stringify(formData),
      });
      setSuccessNotice(`Updated "${formData.name}".`);
      setTimeout(() => setSuccessNotice(null), 3000);
      setEditModalTarget(null);
      await loadEvents();
    } catch (err) {
      setActionError(err instanceof APIError ? err.detail : "Failed to update event.");
    } finally {
      setSubmittingModal(false);
    }
  };

  // Submit Add Form
  const handleSaveAdd = async (e: React.FormEvent) => {
    e.preventDefault();
    setSubmittingModal(true);
    try {
      await fetchAPI("/api/events", {
        method: "POST",
        body: JSON.stringify(formData),
      });
      setSuccessNotice(`Created event "${formData.name}".`);
      setTimeout(() => setSuccessNotice(null), 3000);
      setAddModalOpen(false);
      await loadEvents();
    } catch (err) {
      setActionError(err instanceof APIError ? err.detail : "Failed to create event.");
    } finally {
      setSubmittingModal(false);
    }
  };

  // Unique Lists
  const categories = useMemo(() => {
    const set = new Set<string>();
    events.forEach((e) => {
      if (e.category) set.add(e.category);
    });
    return Array.from(set).sort();
  }, [events]);

  const barangays = useMemo(() => {
    const set = new Set<string>();
    events.forEach((e) => {
      if (e.barangay_name) set.add(e.barangay_name);
    });
    return Array.from(set).sort();
  }, [events]);

  // Date Calculations for KPIs
  const now = new Date();
  now.setHours(0, 0, 0, 0);

  const totalCount = events.length;
  const upcomingCount = events.filter((e) => {
    if (!e.date) return false;
    const d = new Date(e.date);
    d.setHours(0, 0, 0, 0);
    return d >= now;
  }).length;

  const pastCount = events.filter((e) => {
    if (!e.date) return false;
    const d = new Date(e.date);
    d.setHours(0, 0, 0, 0);
    return d < now;
  }).length;

  const publishedCount = events.filter(
    (e) => (e.status || "").toLowerCase() === "approved" || (e.status || "").toLowerCase() === "published"
  ).length;

  // Filtered & Sorted Events
  const filteredEvents = useMemo(() => {
    return events
      .filter((e) => {
        // Search query
        if (searchQuery.trim()) {
          const q = searchQuery.toLowerCase();
          const matchName = e.name?.toLowerCase().includes(q);
          const matchDesc = e.description?.toLowerCase().includes(q);
          const matchLoc = e.location?.toLowerCase().includes(q);
          const matchBarangay = e.barangay_name?.toLowerCase().includes(q);
          const matchCat = e.category?.toLowerCase().includes(q);
          if (!matchName && !matchDesc && !matchLoc && !matchBarangay && !matchCat) return false;
        }

        // Category
        if (selectedCategory !== "all" && e.category !== selectedCategory) {
          return false;
        }

        // Status
        if (selectedStatus !== "all") {
          const st = (e.status || "draft").toLowerCase();
          if (selectedStatus === "approved" && st !== "approved" && st !== "published") return false;
          if (selectedStatus === "draft" && st !== "draft" && st !== "pending") return false;
        }

        // Timeframe
        if (timeFilter !== "all") {
          if (!e.date) return false;
          const d = new Date(e.date);
          d.setHours(0, 0, 0, 0);

          if (timeFilter === "upcoming" && d < now) return false;
          if (timeFilter === "past" && d >= now) return false;
          if (timeFilter === "today" && d.getTime() !== now.getTime()) return false;
        }

        // Barangay
        if (selectedBarangay !== "all" && e.barangay_name !== selectedBarangay) {
          return false;
        }

        return true;
      })
      .sort((a, b) => {
        if (sortBy === "date-asc") {
          const da = a.date ? new Date(a.date).getTime() : 0;
          const db = b.date ? new Date(b.date).getTime() : 0;
          return da - db;
        }
        if (sortBy === "date-desc") {
          const da = a.date ? new Date(a.date).getTime() : 0;
          const db = b.date ? new Date(b.date).getTime() : 0;
          return db - da;
        }
        if (sortBy === "name") return a.name.localeCompare(b.name);
        if (sortBy === "newest") return (b.id || 0) - (a.id || 0);
        return 0;
      });
  }, [events, searchQuery, selectedCategory, selectedStatus, timeFilter, selectedBarangay, sortBy, now]);

  // Helper date formatters
  const formatEventDate = (dateStr?: string | null) => {
    if (!dateStr) return { month: "TBD", day: "--", full: "Date to be announced", relative: "" };
    const d = new Date(dateStr);
    const month = d.toLocaleDateString("en-US", { month: "short" }).toUpperCase();
    const day = d.getDate();
    const full = d.toLocaleDateString("en-US", {
      weekday: "short",
      month: "short",
      day: "numeric",
      year: "numeric",
    });

    // Relative countdown
    const eventTime = new Date(dateStr);
    eventTime.setHours(0, 0, 0, 0);
    const diffTime = eventTime.getTime() - now.getTime();
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

    let relative = "";
    if (diffDays === 0) relative = "Happening Today";
    else if (diffDays === 1) relative = "Tomorrow";
    else if (diffDays > 1 && diffDays <= 30) relative = `In ${diffDays} days`;
    else if (diffDays > 30) relative = `In ${Math.round(diffDays / 30)} months`;
    else if (diffDays === -1) relative = "Yesterday";
    else relative = `${Math.abs(diffDays)} days ago`;

    return { month, day, full, relative, diffDays };
  };

  if (authLoading || !user || loading) {
    return (
      <div className="container mx-auto px-4 py-16 max-w-7xl">
        <div className="flex flex-col items-center justify-center gap-3">
          <Loader2 className="h-8 w-8 animate-spin text-primary" />
          <p className="text-sm text-muted-foreground animate-pulse">Loading event schedules & festivities...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8 max-w-7xl space-y-8">
      {/* Header Area */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-border/60 pb-6">
        <div className="flex items-center gap-4">
          <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-primary/10 text-primary border border-primary/20 shadow-sm">
            <Calendar className="h-6 w-6" />
          </div>
          <div>
            <div className="flex items-center gap-2.5">
              <h1 className="text-2xl sm:text-3xl font-extrabold tracking-tight text-foreground">
                Event Management
              </h1>
              <Badge variant="outline" className="font-mono text-xs px-2.5 py-0.5 rounded-full border-border bg-muted/50">
                {totalCount} Total
              </Badge>
            </div>
            <p className="text-sm text-muted-foreground mt-1">
              Curate municipal festivals, cultural activities, and tourism gatherings in Mangatarem
            </p>
          </div>
        </div>

        <div className="flex items-center gap-2.5">
          <Button
            variant="outline"
            size="sm"
            onClick={handleRefresh}
            disabled={refreshing}
            className="rounded-xl h-10 gap-2 text-muted-foreground hover:text-foreground"
          >
            <RefreshCw className={`h-4 w-4 ${refreshing ? "animate-spin" : ""}`} />
            <span className="hidden sm:inline">Refresh</span>
          </Button>

          <Button
            onClick={handleOpenAddModal}
            className="rounded-xl h-10 gap-2 bg-primary text-primary-foreground hover:bg-primary/90 shadow-sm transition-all"
          >
            <Plus className="h-4 w-4" />
            <span>Add Event</span>
          </Button>
        </div>
      </div>

      {/* Notifications / Alerts */}
      {actionError && (
        <div className="rounded-xl border border-destructive/30 bg-destructive/10 px-4 py-3 text-sm text-destructive flex items-center justify-between gap-2 shadow-xs">
          <div className="flex items-center gap-2">
            <ShieldAlert className="h-4 w-4 flex-shrink-0" />
            <span>{actionError}</span>
          </div>
          <Button
            variant="ghost"
            size="icon"
            className="h-6 w-6 text-destructive hover:bg-destructive/20 rounded-md"
            onClick={() => setActionError(null)}
          >
            <X className="h-3.5 w-3.5" />
          </Button>
        </div>
      )}

      {successNotice && (
        <div className="rounded-xl border border-emerald-500/30 bg-emerald-500/10 px-4 py-3 text-sm text-emerald-600 dark:text-emerald-400 flex items-center justify-between gap-2 shadow-xs animate-in fade-in slide-in-from-top-1">
          <div className="flex items-center gap-2">
            <CheckCircle2 className="h-4 w-4 flex-shrink-0" />
            <span>{successNotice}</span>
          </div>
          <Button
            variant="ghost"
            size="icon"
            className="h-6 w-6 text-emerald-600 hover:bg-emerald-500/20 rounded-md"
            onClick={() => setSuccessNotice(null)}
          >
            <X className="h-3.5 w-3.5" />
          </Button>
        </div>
      )}

      {/* KPI Metric Cards */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <Card className="rounded-2xl border-border/60 shadow-xs bg-card/60 backdrop-blur-xs">
          <CardContent className="p-4 sm:p-5 flex items-center justify-between">
            <div>
              <p className="text-xs font-medium text-muted-foreground uppercase tracking-wider">Total Events</p>
              <h3 className="text-2xl font-bold mt-1 text-foreground">{totalCount}</h3>
              <p className="text-xs text-muted-foreground mt-0.5">{categories.length} distinct categories</p>
            </div>
            <div className="h-11 w-11 rounded-xl bg-primary/10 text-primary flex items-center justify-center">
              <CalendarDays className="h-5 w-5" />
            </div>
          </CardContent>
        </Card>

        <Card className="rounded-2xl border-border/60 shadow-xs bg-card/60 backdrop-blur-xs">
          <CardContent className="p-4 sm:p-5 flex items-center justify-between">
            <div>
              <p className="text-xs font-medium text-muted-foreground uppercase tracking-wider">Upcoming</p>
              <h3 className="text-2xl font-bold mt-1 text-emerald-600 dark:text-emerald-400">{upcomingCount}</h3>
              <p className="text-xs text-muted-foreground mt-0.5 flex items-center gap-1">
                <Sparkles className="h-3 w-3 text-emerald-500" /> Active itineraries
              </p>
            </div>
            <div className="h-11 w-11 rounded-xl bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 flex items-center justify-center">
              <Clock className="h-5 w-5" />
            </div>
          </CardContent>
        </Card>

        <Card className="rounded-2xl border-border/60 shadow-xs bg-card/60 backdrop-blur-xs">
          <CardContent className="p-4 sm:p-5 flex items-center justify-between">
            <div>
              <p className="text-xs font-medium text-muted-foreground uppercase tracking-wider">Past / Completed</p>
              <h3 className="text-2xl font-bold mt-1 text-foreground">{pastCount}</h3>
              <p className="text-xs text-muted-foreground mt-0.5">Archived gatherings</p>
            </div>
            <div className="h-11 w-11 rounded-xl bg-muted text-muted-foreground flex items-center justify-center">
              <Calendar className="h-5 w-5" />
            </div>
          </CardContent>
        </Card>

        <Card className="rounded-2xl border-border/60 shadow-xs bg-card/60 backdrop-blur-xs">
          <CardContent className="p-4 sm:p-5 flex items-center justify-between">
            <div>
              <p className="text-xs font-medium text-muted-foreground uppercase tracking-wider">Published / Live</p>
              <h3 className="text-2xl font-bold mt-1 text-foreground">{publishedCount}</h3>
              <p className="text-xs text-sky-600 dark:text-sky-400 mt-0.5 flex items-center gap-1">
                <CheckCircle2 className="h-3 w-3 inline" />
                {totalCount > 0 ? `${Math.round((publishedCount / totalCount) * 100)}% approved` : "0%"}
              </p>
            </div>
            <div className="h-11 w-11 rounded-xl bg-sky-500/10 text-sky-600 dark:text-sky-400 flex items-center justify-center">
              <CheckCircle2 className="h-5 w-5" />
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Filter & Controls Toolbar */}
      <div className="flex flex-col gap-4 bg-muted/40 p-4 rounded-2xl border border-border/50">
        <div className="flex flex-col lg:flex-row items-stretch lg:items-center justify-between gap-3">
          {/* Search bar */}
          <div className="relative flex-1">
            <Search className="absolute left-3.5 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
            <Input
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Search events by name, description, venue, barangay..."
              className="pl-10 pr-9 h-10 rounded-xl bg-background border-border/80 focus-visible:ring-1"
            />
            {searchQuery && (
              <button
                onClick={() => setSearchQuery("")}
                className="absolute right-3 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground cursor-pointer p-0.5"
              >
                <X className="h-3.5 w-3.5" />
              </button>
            )}
          </div>

          {/* Quick Toolbar items */}
          <div className="flex flex-wrap items-center gap-2">
            {/* Timeframe Quick Filter Buttons */}
            <div className="flex items-center rounded-xl bg-background border border-border/80 p-1 h-10">
              <button
                onClick={() => setTimeFilter("all")}
                className={`px-3 py-1 text-xs font-semibold rounded-lg transition-colors cursor-pointer ${
                  timeFilter === "all" ? "bg-primary text-primary-foreground" : "text-muted-foreground hover:text-foreground"
                }`}
              >
                All
              </button>
              <button
                onClick={() => setTimeFilter("upcoming")}
                className={`px-3 py-1 text-xs font-semibold rounded-lg transition-colors cursor-pointer ${
                  timeFilter === "upcoming" ? "bg-primary text-primary-foreground" : "text-muted-foreground hover:text-foreground"
                }`}
              >
                Upcoming
              </button>
              <button
                onClick={() => setTimeFilter("past")}
                className={`px-3 py-1 text-xs font-semibold rounded-lg transition-colors cursor-pointer ${
                  timeFilter === "past" ? "bg-primary text-primary-foreground" : "text-muted-foreground hover:text-foreground"
                }`}
              >
                Past
              </button>
            </div>

            {/* Category Select */}
            <select
              value={selectedCategory}
              onChange={(e) => setSelectedCategory(e.target.value)}
              className="h-10 px-3 rounded-xl bg-background border border-border/80 text-sm font-medium text-foreground focus:outline-none focus:ring-1 focus:ring-primary cursor-pointer"
            >
              <option value="all">All Categories</option>
              {categories.map((c) => (
                <option key={c} value={c}>
                  {c}
                </option>
              ))}
            </select>

            {/* Status Select */}
            <select
              value={selectedStatus}
              onChange={(e) => setSelectedStatus(e.target.value)}
              className="h-10 px-3 rounded-xl bg-background border border-border/80 text-sm font-medium text-foreground focus:outline-none focus:ring-1 focus:ring-primary cursor-pointer"
            >
              <option value="all">All Status</option>
              <option value="approved">Approved / Live</option>
              <option value="draft">Pending / Draft</option>
            </select>

            {/* Barangay Select */}
            {barangays.length > 0 && (
              <select
                value={selectedBarangay}
                onChange={(e) => setSelectedBarangay(e.target.value)}
                className="h-10 px-3 rounded-xl bg-background border border-border/80 text-sm font-medium text-foreground focus:outline-none focus:ring-1 focus:ring-primary cursor-pointer max-w-[150px] truncate"
              >
                <option value="all">All Barangays</option>
                {barangays.map((b) => (
                  <option key={b} value={b}>
                    {b}
                  </option>
                ))}
              </select>
            )}

            {/* Sort options */}
            <div className="flex items-center rounded-xl bg-background border border-border/80 h-10 px-2 gap-1 text-muted-foreground">
              <ArrowUpDown className="h-3.5 w-3.5 ml-1 text-muted-foreground/80" />
              <select
                value={sortBy}
                onChange={(e) => setSortBy(e.target.value as "date-asc" | "date-desc" | "name" | "newest")}
                className="bg-transparent border-0 text-xs font-medium text-foreground focus:outline-none cursor-pointer pr-2"
              >
                <option value="date-desc">Date (Latest First)</option>
                <option value="date-asc">Date (Earliest First)</option>
                <option value="name">Name (A-Z)</option>
                <option value="newest">Recently Added</option>
              </select>
            </div>

            {/* View Mode Switcher */}
            <div className="flex items-center rounded-xl bg-background border border-border/80 p-1 h-10">
              <Button
                variant={viewMode === "grid" ? "secondary" : "ghost"}
                size="icon"
                onClick={() => setViewMode("grid")}
                className="h-8 w-8 rounded-lg"
                title="Grid View"
              >
                <LayoutGrid className="h-4 w-4" />
              </Button>
              <Button
                variant={viewMode === "table" ? "secondary" : "ghost"}
                size="icon"
                onClick={() => setViewMode("table")}
                className="h-8 w-8 rounded-lg"
                title="Table View"
              >
                <List className="h-4 w-4" />
              </Button>
            </div>
          </div>
        </div>

        {/* Active filter tags */}
        {(searchQuery || selectedCategory !== "all" || selectedStatus !== "all" || timeFilter !== "all" || selectedBarangay !== "all") && (
          <div className="flex flex-wrap items-center gap-2 pt-2 border-t border-border/50 text-xs text-muted-foreground">
            <span className="font-medium">Active filters:</span>
            {searchQuery && (
              <Badge variant="secondary" className="gap-1 rounded-md text-xs py-0.5">
                Query: {searchQuery}
                <button onClick={() => setSearchQuery("")} className="hover:text-foreground cursor-pointer">
                  <X className="h-3 w-3" />
                </button>
              </Badge>
            )}
            {timeFilter !== "all" && (
              <Badge variant="secondary" className="gap-1 rounded-md text-xs py-0.5 capitalize">
                Time: {timeFilter}
                <button onClick={() => setTimeFilter("all")} className="hover:text-foreground cursor-pointer">
                  <X className="h-3 w-3" />
                </button>
              </Badge>
            )}
            {selectedCategory !== "all" && (
              <Badge variant="secondary" className="gap-1 rounded-md text-xs py-0.5">
                Category: {selectedCategory}
                <button onClick={() => setSelectedCategory("all")} className="hover:text-foreground cursor-pointer">
                  <X className="h-3 w-3" />
                </button>
              </Badge>
            )}
            {selectedStatus !== "all" && (
              <Badge variant="secondary" className="gap-1 rounded-md text-xs py-0.5 capitalize">
                Status: {selectedStatus}
                <button onClick={() => setSelectedStatus("all")} className="hover:text-foreground cursor-pointer">
                  <X className="h-3 w-3" />
                </button>
              </Badge>
            )}
            {selectedBarangay !== "all" && (
              <Badge variant="secondary" className="gap-1 rounded-md text-xs py-0.5">
                Barangay: {selectedBarangay}
                <button onClick={() => setSelectedBarangay("all")} className="hover:text-foreground cursor-pointer">
                  <X className="h-3 w-3" />
                </button>
              </Badge>
            )}
            <Button
              variant="ghost"
              size="sm"
              onClick={() => {
                setSearchQuery("");
                setSelectedCategory("all");
                setSelectedStatus("all");
                setTimeFilter("all");
                setSelectedBarangay("all");
              }}
              className="h-6 px-2 text-xs text-primary hover:underline hover:bg-transparent"
            >
              Reset all
            </Button>
            <span className="ml-auto text-xs font-medium text-foreground">
              Showing {filteredEvents.length} of {totalCount}
            </span>
          </div>
        )}
      </div>

      {/* Content Rendering: Grid vs Table */}
      {filteredEvents.length === 0 ? (
        <div className="border border-dashed border-border/80 rounded-2xl py-20 text-center bg-card/40">
          <div className="h-14 w-14 rounded-2xl bg-muted/80 text-muted-foreground/60 flex items-center justify-center mx-auto mb-4 border border-border/60">
            <CalendarDays className="h-7 w-7" />
          </div>
          <h3 className="text-base font-bold text-foreground">No events found</h3>
          <p className="text-sm text-muted-foreground mt-1 max-w-sm mx-auto">
            We couldn&apos;t find any events matching your current search or timeframe filter criteria.
          </p>
          <div className="mt-5 flex justify-center gap-3">
            <Button
              variant="outline"
              size="sm"
              onClick={() => {
                setSearchQuery("");
                setSelectedCategory("all");
                setSelectedStatus("all");
                setTimeFilter("all");
                setSelectedBarangay("all");
              }}
              className="rounded-xl"
            >
              Clear Filters
            </Button>
            <Button
              size="sm"
              onClick={handleOpenAddModal}
              className="rounded-xl gap-1.5"
            >
              <Plus className="h-4 w-4" /> Add Event
            </Button>
          </div>
        </div>
      ) : viewMode === "grid" ? (
        /* Visual Card Grid Mode */
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
          {filteredEvents.map((event) => {
            const isLive =
              (event.status || "").toLowerCase() === "approved" ||
              (event.status || "").toLowerCase() === "published";
            const categoryStyle =
              CATEGORY_COLORS[event.category] ??
              "bg-primary/10 text-primary border-primary/20";
            const dateInfo = formatEventDate(event.date);

            return (
              <Card
                key={event.id}
                className="group relative overflow-hidden rounded-2xl border-border/60 hover:border-border transition-all duration-200 hover:shadow-md bg-card flex flex-col justify-between"
              >
                <div>
                  {/* Banner Image & Date Box Overlay */}
                  <div className="relative aspect-video w-full overflow-hidden bg-muted">
                    {event.image_url ? (
                      // eslint-disable-next-line @next/next/no-img-element
                      <img
                        src={event.image_url}
                        alt={event.name}
                        className="h-full w-full object-cover transition-transform duration-300 group-hover:scale-105"
                      />
                    ) : (
                      <div className="flex h-full w-full items-center justify-center bg-gradient-to-br from-primary/10 via-muted to-muted/60 text-muted-foreground/40">
                        <Calendar className="h-12 w-12" />
                      </div>
                    )}

                    {/* Gradient Overlay */}
                    <div className="absolute inset-0 bg-gradient-to-t from-black/75 via-black/20 to-transparent" />

                    {/* Calendar Date Badge (Top Left) */}
                    <div className="absolute top-3 left-3 bg-background/95 dark:bg-card/95 backdrop-blur-md rounded-xl p-2 text-center shadow-md border border-border/60 min-w-[48px]">
                      <span className="block text-[10px] font-black uppercase text-primary tracking-wider leading-none">
                        {dateInfo.month}
                      </span>
                      <span className="block text-lg font-black text-foreground leading-tight mt-0.5">
                        {dateInfo.day}
                      </span>
                    </div>

                    {/* Category Tag (Top Right) */}
                    <div className="absolute top-3 right-3">
                      <span
                        className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-semibold backdrop-blur-md border ${categoryStyle}`}
                      >
                        {event.category || "General"}
                      </span>
                    </div>

                    {/* Bottom overlay: Location & Relative countdown */}
                    <div className="absolute bottom-3 left-3 right-3 flex items-center justify-between text-white text-xs">
                      <div className="flex items-center gap-1 truncate font-medium drop-shadow-xs">
                        <MapPin className="h-3.5 w-3.5 flex-shrink-0 text-primary" />
                        <span className="truncate">
                          {event.location || (event.barangay_name ? `Brgy. ${event.barangay_name}` : "Mangatarem")}
                        </span>
                      </div>
                      {dateInfo.relative && (
                        <div className="flex items-center gap-1 bg-black/50 backdrop-blur-md px-2 py-0.5 rounded-md font-semibold text-white/90 text-[11px]">
                          <Clock className="h-3 w-3" />
                          <span>{dateInfo.relative}</span>
                        </div>
                      )}
                    </div>
                  </div>

                  {/* Event Details */}
                  <div className="p-4 sm:p-5 space-y-3">
                    <div>
                      <div className="flex items-start justify-between gap-2">
                        <h3 className="font-bold text-base text-foreground line-clamp-1 group-hover:text-primary transition-colors">
                          {event.name}
                        </h3>
                        <button
                          onClick={() => handleToggleStatus(event)}
                          className="cursor-pointer flex-shrink-0"
                          title={`Click to mark as ${isLive ? "draft" : "approved"}`}
                        >
                          <Badge
                            variant="outline"
                            className={`text-[10px] font-bold uppercase tracking-wider px-2 py-0.5 rounded-full border transition-colors ${
                              isLive
                                ? "bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 border-emerald-500/20 hover:bg-emerald-500/20"
                                : "bg-amber-500/10 text-amber-600 dark:text-amber-400 border-amber-500/20 hover:bg-amber-500/20"
                            }`}
                          >
                            {isLive ? "Approved" : "Draft"}
                          </Badge>
                        </button>
                      </div>

                      <p className="text-xs text-muted-foreground line-clamp-2 mt-1.5 leading-relaxed">
                        {event.description || "No narrative details provided for this event yet."}
                      </p>
                    </div>

                    {/* Schedule Snippet */}
                    <div className="flex items-center justify-between text-[11px] text-muted-foreground bg-muted/40 rounded-lg px-2.5 py-1.5">
                      <span className="flex items-center gap-1.5 font-medium">
                        <Calendar className="h-3.5 w-3.5 text-primary" />
                        {dateInfo.full}
                      </span>
                      {event.barangay_name && (
                        <span className="text-[10px] font-semibold bg-background px-1.5 py-0.5 rounded border border-border/50">
                          Brgy. {event.barangay_name}
                        </span>
                      )}
                    </div>
                  </div>
                </div>

                {/* Card Actions Footer */}
                <div className="p-4 pt-0 sm:p-5 sm:pt-0 flex items-center justify-between gap-2 border-t border-border/40 mt-2">
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => setInspectTarget(event)}
                    className="rounded-xl h-8 text-xs gap-1.5 flex-1 hover:bg-muted"
                  >
                    <Eye className="h-3.5 w-3.5 text-muted-foreground" />
                    Quick View
                  </Button>

                  <div className="flex items-center gap-1">
                    <Button
                      variant="ghost"
                      size="icon"
                      onClick={() => handleOpenEditModal(event)}
                      className="h-8 w-8 rounded-lg text-muted-foreground hover:text-foreground hover:bg-muted"
                      title="Edit Event"
                    >
                      <Pencil className="h-3.5 w-3.5" />
                    </Button>
                    <Button
                      variant="ghost"
                      size="icon"
                      onClick={() => setDeleteTarget(event)}
                      className="h-8 w-8 rounded-lg text-muted-foreground hover:text-destructive hover:bg-destructive/10"
                      title="Delete Event"
                    >
                      <Trash2 className="h-3.5 w-3.5" />
                    </Button>
                  </div>
                </div>
              </Card>
            );
          })}
        </div>
      ) : (
        /* Dense Data Table Mode */
        <div className="border rounded-2xl border-border/60 overflow-hidden bg-card shadow-xs">
          <Table>
            <TableHeader>
              <TableRow className="bg-muted/50 hover:bg-muted/50 border-b border-border/60">
                <TableHead className="w-[100px]">Date</TableHead>
                <TableHead>Event Title</TableHead>
                <TableHead>Category</TableHead>
                <TableHead>Location & Barangay</TableHead>
                <TableHead>Status</TableHead>
                <TableHead className="text-right">Actions</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {filteredEvents.map((event) => {
                const isLive =
                  (event.status || "").toLowerCase() === "approved" ||
                  (event.status || "").toLowerCase() === "published";
                const categoryStyle =
                  CATEGORY_COLORS[event.category] ??
                  "bg-primary/10 text-primary border-primary/20";
                const dateInfo = formatEventDate(event.date);

                return (
                  <TableRow key={event.id} className="hover:bg-muted/30 transition-colors">
                    {/* Date Block */}
                    <TableCell className="py-3">
                      <div className="font-mono text-xs">
                        <span className="font-bold block text-foreground">{dateInfo.month} {dateInfo.day}</span>
                        <span className="text-[10px] text-muted-foreground">{dateInfo.relative || "—"}</span>
                      </div>
                    </TableCell>

                    {/* Title & Desc */}
                    <TableCell className="py-3 max-w-xs">
                      <div
                        className="font-bold text-sm text-foreground hover:text-primary cursor-pointer transition-colors"
                        onClick={() => setInspectTarget(event)}
                      >
                        {event.name}
                      </div>
                      <p className="text-xs text-muted-foreground line-clamp-1 mt-0.5">
                        {event.description || "No description"}
                      </p>
                    </TableCell>

                    {/* Category */}
                    <TableCell className="py-3">
                      <Badge
                        variant="outline"
                        className={`text-xs font-semibold border ${categoryStyle}`}
                      >
                        {event.category || "General"}
                      </Badge>
                    </TableCell>

                    {/* Location */}
                    <TableCell className="py-3 text-sm text-muted-foreground">
                      <div className="flex items-center gap-1 text-xs">
                        <MapPin className="h-3.5 w-3.5 text-muted-foreground/70" />
                        <span className="truncate max-w-[200px]">
                          {event.location || (event.barangay_name ? `Brgy. ${event.barangay_name}` : "Mangatarem")}
                        </span>
                      </div>
                    </TableCell>

                    {/* Status */}
                    <TableCell className="py-3">
                      <button
                        onClick={() => handleToggleStatus(event)}
                        className="cursor-pointer"
                        title={`Click to mark as ${isLive ? "draft" : "approved"}`}
                      >
                        <Badge
                          variant="outline"
                          className={`text-[11px] font-semibold capitalize px-2.5 py-0.5 rounded-full border transition-colors ${
                            isLive
                              ? "bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 border-emerald-500/20 hover:bg-emerald-500/20"
                              : "bg-amber-500/10 text-amber-600 dark:text-amber-400 border-amber-500/20 hover:bg-amber-500/20"
                          }`}
                        >
                          {isLive ? "Approved" : "Draft"}
                        </Badge>
                      </button>
                    </TableCell>

                    {/* Actions */}
                    <TableCell className="py-3 text-right">
                      <div className="flex justify-end items-center gap-1">
                        <Button
                          variant="ghost"
                          size="icon"
                          className="h-8 w-8 rounded-lg text-muted-foreground hover:text-foreground"
                          onClick={() => setInspectTarget(event)}
                          title="Quick View"
                        >
                          <Eye className="h-3.5 w-3.5" />
                        </Button>
                        <Button
                          variant="ghost"
                          size="icon"
                          className="h-8 w-8 rounded-lg text-muted-foreground hover:text-foreground"
                          onClick={() => handleOpenEditModal(event)}
                          title="Edit Event"
                        >
                          <Pencil className="h-3.5 w-3.5" />
                        </Button>
                        <Button
                          variant="ghost"
                          size="icon"
                          className="h-8 w-8 rounded-lg text-muted-foreground hover:text-destructive hover:bg-destructive/10"
                          onClick={() => setDeleteTarget(event)}
                          title="Delete Event"
                        >
                          <Trash2 className="h-3.5 w-3.5" />
                        </Button>
                      </div>
                    </TableCell>
                  </TableRow>
                );
              })}
            </TableBody>
          </Table>
        </div>
      )}

      {/* Quick View Inspection Sheet / Drawer */}
      <Sheet open={!!inspectTarget} onOpenChange={(open) => !open && setInspectTarget(null)}>
        <SheetContent className="w-full sm:max-w-lg p-0 flex flex-col justify-between overflow-y-auto bg-background">
          {inspectTarget && (
            <div className="space-y-6 pb-6">
              {/* Header Image */}
              <div className="relative aspect-video w-full bg-muted overflow-hidden">
                {inspectTarget.image_url ? (
                  // eslint-disable-next-line @next/next/no-img-element
                  <img
                    src={inspectTarget.image_url}
                    alt={inspectTarget.name}
                    className="h-full w-full object-cover"
                  />
                ) : (
                  <div className="flex h-full w-full items-center justify-center text-muted-foreground/40 bg-muted">
                    <Calendar className="h-16 w-16" />
                  </div>
                )}
                <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-black/30 to-transparent" />
                <div className="absolute bottom-4 left-5 right-5 text-white">
                  <div className="flex items-center gap-2 mb-1.5">
                    <Badge variant="outline" className="text-xs bg-white/20 text-white backdrop-blur-md border-white/30">
                      {inspectTarget.category}
                    </Badge>
                    <Badge className="text-xs bg-primary text-primary-foreground border-0">
                      {inspectTarget.status || "Draft"}
                    </Badge>
                  </div>
                  <h2 className="text-xl font-bold">{inspectTarget.name}</h2>
                  <p className="text-xs text-white/80 flex items-center gap-1 mt-1">
                    <Calendar className="h-3.5 w-3.5 text-primary" />
                    {formatEventDate(inspectTarget.date).full}
                  </p>
                </div>
              </div>

              {/* Sheet Body Details */}
              <div className="px-6 space-y-5">
                {/* Description */}
                <div>
                  <h4 className="text-xs font-bold uppercase tracking-wider text-muted-foreground mb-1.5">
                    Event Overview
                  </h4>
                  <p className="text-sm text-foreground leading-relaxed">
                    {inspectTarget.description || "No description provided."}
                  </p>
                </div>

                {/* Key Attributes Grid */}
                <div className="grid grid-cols-2 gap-3 pt-2">
                  <div className="p-3 rounded-xl bg-muted/40 border border-border/50">
                    <span className="text-[11px] font-medium text-muted-foreground flex items-center gap-1 mb-1">
                      <Calendar className="h-3 w-3" /> Event Date
                    </span>
                    <p className="text-xs font-semibold text-foreground">
                      {formatEventDate(inspectTarget.date).full}
                    </p>
                  </div>

                  <div className="p-3 rounded-xl bg-muted/40 border border-border/50">
                    <span className="text-[11px] font-medium text-muted-foreground flex items-center gap-1 mb-1">
                      <Clock className="h-3 w-3" /> Time Status
                    </span>
                    <p className="text-xs font-semibold text-foreground">
                      {formatEventDate(inspectTarget.date).relative || "Scheduled"}
                    </p>
                  </div>

                  <div className="p-3 rounded-xl bg-muted/40 border border-border/50">
                    <span className="text-[11px] font-medium text-muted-foreground flex items-center gap-1 mb-1">
                      <MapPin className="h-3 w-3" /> Venue / Location
                    </span>
                    <p className="text-xs font-semibold text-foreground truncate">
                      {inspectTarget.location || "Mangatarem Center"}
                    </p>
                  </div>

                  <div className="p-3 rounded-xl bg-muted/40 border border-border/50">
                    <span className="text-[11px] font-medium text-muted-foreground flex items-center gap-1 mb-1">
                      <Tag className="h-3 w-3" /> Barangay Jurisdiction
                    </span>
                    <p className="text-xs font-semibold text-foreground">
                      {inspectTarget.barangay_name ? `Brgy. ${inspectTarget.barangay_name}` : "Municipal-wide"}
                    </p>
                  </div>
                </div>
              </div>

              {/* Action Buttons in Sheet */}
              <div className="px-6 pt-4 border-t border-border/60 flex flex-col gap-2.5">
                <div className="grid grid-cols-2 gap-2">
                  <Button
                    variant="outline"
                    onClick={() => handleToggleStatus(inspectTarget)}
                    className="rounded-xl h-10 text-xs gap-1.5"
                  >
                    <CheckCircle2 className="h-3.5 w-3.5" />
                    {(inspectTarget.status || "").toLowerCase() === "approved" ? "Set to Draft" : "Approve & Live"}
                  </Button>

                  <Button
                    variant="outline"
                    onClick={() => {
                      setInspectTarget(null);
                      handleOpenEditModal(inspectTarget);
                    }}
                    className="rounded-xl h-10 text-xs gap-1.5"
                  >
                    <Pencil className="h-3.5 w-3.5" /> Edit Modal
                  </Button>
                </div>

                <div className="flex items-center gap-2">
                  <Link
                    href="/events"
                    target="_blank"
                    className="flex-1 inline-flex items-center justify-center h-10 rounded-xl bg-muted hover:bg-muted/80 text-foreground font-medium text-xs gap-1.5 border border-border/60 transition-colors"
                  >
                    <ExternalLink className="h-3.5 w-3.5" /> Public Calendar
                  </Link>

                  <Button
                    onClick={() => router.push(`/admin/events/${inspectTarget.id}/edit`)}
                    className="flex-1 rounded-xl h-10 text-xs gap-1.5 bg-primary text-primary-foreground"
                  >
                    <Pencil className="h-3.5 w-3.5" /> Full Page Edit
                  </Button>
                </div>
              </div>
            </div>
          )}
        </SheetContent>
      </Sheet>

      {/* Inline Fast Edit Modal */}
      <Dialog open={!!editModalTarget} onOpenChange={(open) => !open && setEditModalTarget(null)}>
        <DialogContent className="max-w-xl rounded-2xl bg-card border-border/80">
          <DialogHeader>
            <DialogTitle className="text-xl font-bold">Edit Event Details</DialogTitle>
            <DialogDescription className="text-xs text-muted-foreground">
              Update schedule, venue, narrative, and imagery for &quot;{editModalTarget?.name}&quot;
            </DialogDescription>
          </DialogHeader>

          <form onSubmit={handleSaveEdit} className="space-y-4 pt-2">
            <div className="space-y-1.5">
              <Label htmlFor="edit-name" className="text-xs font-semibold">Event Name *</Label>
              <Input
                id="edit-name"
                required
                value={formData.name}
                onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                className="rounded-xl"
              />
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
              <div className="space-y-1.5">
                <Label htmlFor="edit-date" className="text-xs font-semibold">Event Date *</Label>
                <Input
                  id="edit-date"
                  type="date"
                  required
                  value={formData.date}
                  onChange={(e) => setFormData({ ...formData, date: e.target.value })}
                  className="rounded-xl"
                />
              </div>

              <div className="space-y-1.5">
                <Label htmlFor="edit-category" className="text-xs font-semibold">Category *</Label>
                <select
                  id="edit-category"
                  value={formData.category}
                  onChange={(e) => setFormData({ ...formData, category: e.target.value })}
                  className="w-full h-9 px-3 rounded-xl bg-background border border-border/80 text-sm font-medium text-foreground focus:outline-none focus:ring-1 focus:ring-primary cursor-pointer"
                >
                  <option value="Festival">Festival</option>
                  <option value="Cultural">Cultural</option>
                  <option value="Religious">Religious</option>
                  <option value="Sports">Sports</option>
                  <option value="Agricultural">Agricultural</option>
                  <option value="Civic">Civic</option>
                  <option value="Community">Community</option>
                  <option value="Tourism">Tourism</option>
                </select>
              </div>
            </div>

            <div className="space-y-1.5">
              <Label htmlFor="edit-location" className="text-xs font-semibold">Venue / Location</Label>
              <Input
                id="edit-location"
                placeholder="e.g. Mangatarem Town Plaza, Municipal Auditorium"
                value={formData.location}
                onChange={(e) => setFormData({ ...formData, location: e.target.value })}
                className="rounded-xl"
              />
            </div>

            <div className="space-y-1.5">
              <Label htmlFor="edit-image" className="text-xs font-semibold">Image URL (Optional)</Label>
              <Input
                id="edit-image"
                placeholder="https://..."
                value={formData.image_url}
                onChange={(e) => setFormData({ ...formData, image_url: e.target.value })}
                className="rounded-xl"
              />
            </div>

            <div className="space-y-1.5">
              <Label htmlFor="edit-description" className="text-xs font-semibold">Event Description</Label>
              <Textarea
                id="edit-description"
                rows={3}
                placeholder="Details, schedule, or program highlights..."
                value={formData.description}
                onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                className="rounded-xl resize-none text-xs"
              />
            </div>

            <DialogFooter className="pt-3 border-t border-border/60">
              <Button
                type="button"
                variant="outline"
                onClick={() => setEditModalTarget(null)}
                className="rounded-xl"
              >
                Cancel
              </Button>
              <Button
                type="submit"
                disabled={submittingModal}
                className="rounded-xl bg-primary text-primary-foreground"
              >
                {submittingModal ? <Loader2 className="h-4 w-4 animate-spin mr-1.5" /> : null}
                Save Changes
              </Button>
            </DialogFooter>
          </form>
        </DialogContent>
      </Dialog>

      {/* Inline Fast Add Modal */}
      <Dialog open={addModalOpen} onOpenChange={setAddModalOpen}>
        <DialogContent className="max-w-xl rounded-2xl bg-card border-border/80">
          <DialogHeader>
            <DialogTitle className="text-xl font-bold">Add New Event</DialogTitle>
            <DialogDescription className="text-xs text-muted-foreground">
              Schedule a festival, gathering, or cultural celebration in Mangatarem
            </DialogDescription>
          </DialogHeader>

          <form onSubmit={handleSaveAdd} className="space-y-4 pt-2">
            <div className="space-y-1.5">
              <Label htmlFor="add-name" className="text-xs font-semibold">Event Name *</Label>
              <Input
                id="add-name"
                required
                placeholder="e.g. Mangatarem Feast Day, Bamboo Festival"
                value={formData.name}
                onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                className="rounded-xl"
              />
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
              <div className="space-y-1.5">
                <Label htmlFor="add-date" className="text-xs font-semibold">Event Date *</Label>
                <Input
                  id="add-date"
                  type="date"
                  required
                  value={formData.date}
                  onChange={(e) => setFormData({ ...formData, date: e.target.value })}
                  className="rounded-xl"
                />
              </div>

              <div className="space-y-1.5">
                <Label htmlFor="add-category" className="text-xs font-semibold">Category *</Label>
                <select
                  id="add-category"
                  value={formData.category}
                  onChange={(e) => setFormData({ ...formData, category: e.target.value })}
                  className="w-full h-9 px-3 rounded-xl bg-background border border-border/80 text-sm font-medium text-foreground focus:outline-none focus:ring-1 focus:ring-primary cursor-pointer"
                >
                  <option value="Festival">Festival</option>
                  <option value="Cultural">Cultural</option>
                  <option value="Religious">Religious</option>
                  <option value="Sports">Sports</option>
                  <option value="Agricultural">Agricultural</option>
                  <option value="Civic">Civic</option>
                  <option value="Community">Community</option>
                  <option value="Tourism">Tourism</option>
                </select>
              </div>
            </div>

            <div className="space-y-1.5">
              <Label htmlFor="add-location" className="text-xs font-semibold">Venue / Location</Label>
              <Input
                id="add-location"
                placeholder="e.g. Mangatarem Town Plaza, Municipal Gymnasium"
                value={formData.location}
                onChange={(e) => setFormData({ ...formData, location: e.target.value })}
                className="rounded-xl"
              />
            </div>

            <div className="space-y-1.5">
              <Label htmlFor="add-image" className="text-xs font-semibold">Image URL (Optional)</Label>
              <Input
                id="add-image"
                placeholder="https://..."
                value={formData.image_url}
                onChange={(e) => setFormData({ ...formData, image_url: e.target.value })}
                className="rounded-xl"
              />
            </div>

            <div className="space-y-1.5">
              <Label htmlFor="add-description" className="text-xs font-semibold">Event Description</Label>
              <Textarea
                id="add-description"
                rows={3}
                placeholder="Details, schedule, or program highlights..."
                value={formData.description}
                onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                className="rounded-xl resize-none text-xs"
              />
            </div>

            <DialogFooter className="pt-3 border-t border-border/60">
              <Button
                type="button"
                variant="outline"
                onClick={() => setAddModalOpen(false)}
                className="rounded-xl"
              >
                Cancel
              </Button>
              <Button
                type="submit"
                disabled={submittingModal}
                className="rounded-xl bg-primary text-primary-foreground"
              >
                {submittingModal ? <Loader2 className="h-4 w-4 animate-spin mr-1.5" /> : null}
                Create Event
              </Button>
            </DialogFooter>
          </form>
        </DialogContent>
      </Dialog>

      {/* Delete Confirmation Dialog */}
      <DeleteDialog
        open={!!deleteTarget}
        onOpenChange={(open) => !open && setDeleteTarget(null)}
        onConfirm={handleDelete}
        title="Delete Event"
        description={`Are you sure you want to permanently delete "${deleteTarget?.name ?? ""}"? This activity will be removed from the public event calendar.`}
      />
    </div>
  );
}

