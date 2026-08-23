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
  Loader2,
  Plus,
  Pencil,
  Trash2,
  MapPin,
  Search,
  Star,
  Eye,
  LayoutGrid,
  List,
  ExternalLink,
  Clock,
  Banknote,
  Phone,
  ShieldAlert,
  CheckCircle2,
  X,
  Copy,
  Check,
  Compass,
  Layers,
  ArrowUpDown,
  RefreshCw,
  Sparkles,
} from "lucide-react";
import { DeleteDialog } from "@/components/admin-dialogs";

interface Attraction {
  id: number;
  name: string;
  description?: string | null;
  category: string;
  status: string;
  is_featured: boolean;
  latitude?: number | null;
  longitude?: number | null;
  barangay_name?: string | null;
  barangay_id?: number | null;
  image_url?: string | null;
  physical_status?: string | null;
  opening_hours?: string | null;
  entrance_fee?: string | null;
  contact_info?: string | null;
  facilities?: string[] | string | null;
  advisory_message?: string | null;
  advisory_status?: string | null;
  rating?: number | null;
  created_at?: string | null;
}

const CATEGORY_COLORS: Record<string, string> = {
  Nature: "bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 border-emerald-500/20",
  Natural: "bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 border-emerald-500/20",
  Heritage: "bg-amber-500/10 text-amber-600 dark:text-amber-400 border-amber-500/20",
  Historical: "bg-amber-500/10 text-amber-600 dark:text-amber-400 border-amber-500/20",
  Cultural: "bg-indigo-500/10 text-indigo-600 dark:text-indigo-400 border-indigo-500/20",
  Religious: "bg-sky-500/10 text-sky-600 dark:text-sky-400 border-sky-500/20",
  Recreation: "bg-teal-500/10 text-teal-600 dark:text-teal-400 border-teal-500/20",
  "Eco-Tourism": "bg-emerald-600/10 text-emerald-700 dark:text-emerald-300 border-emerald-600/20",
  Agricultural: "bg-lime-500/10 text-lime-600 dark:text-lime-400 border-lime-500/20",
};

export default function AdminAttractionsPage() {
  const { user, loading: authLoading } = useAuth();
  const router = useRouter();

  const [attractions, setAttractions] = useState<Attraction[]>([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [actionError, setActionError] = useState<string | null>(null);
  const [successNotice, setSuccessNotice] = useState<string | null>(null);

  // Filters & Controls
  const [searchQuery, setSearchQuery] = useState("");
  const [selectedCategory, setSelectedCategory] = useState<string>("all");
  const [selectedStatus, setSelectedStatus] = useState<string>("all");
  const [selectedBarangay, setSelectedBarangay] = useState<string>("all");
  const [featuredOnly, setFeaturedOnly] = useState(false);
  const [sortBy, setSortBy] = useState<"name" | "rating" | "newest" | "status">("name");
  const [viewMode, setViewMode] = useState<"table" | "grid">("grid");

  // Selection & Dialogs
  const [inspectTarget, setInspectTarget] = useState<Attraction | null>(null);
  const [deleteTarget, setDeleteTarget] = useState<Attraction | null>(null);
  const [copiedCoords, setCopiedCoords] = useState<number | null>(null);

  const loadAttractions = useCallback(async () => {
    try {
      const data = await fetchAPI<{ attractions: Attraction[] }>("/api/attractions");
      setAttractions(data?.attractions ?? []);
    } catch (err) {
      setActionError(err instanceof APIError ? err.detail : "Failed to load attractions.");
    }
  }, []);

  useEffect(() => {
    if (!authLoading && (!user || user.role !== "admin")) {
      router.push("/dashboard");
    }
  }, [user, authLoading, router]);

  useEffect(() => {
    if (!user) return;
    loadAttractions().finally(() => setLoading(false));
  }, [user, loadAttractions]);

  const handleRefresh = async () => {
    setRefreshing(true);
    await loadAttractions();
    setRefreshing(false);
  };

  // Toggle Featured status inline
  const handleToggleFeatured = async (attraction: Attraction) => {
    const nextVal = !attraction.is_featured;
    // Optimistic update
    setAttractions((prev) =>
      prev.map((a) => (a.id === attraction.id ? { ...a, is_featured: nextVal } : a))
    );
    if (inspectTarget?.id === attraction.id) {
      setInspectTarget({ ...inspectTarget, is_featured: nextVal });
    }

    try {
      await fetchAPI(`/api/attractions/${attraction.id}`, {
        method: "PUT",
        body: JSON.stringify({ is_featured: nextVal }),
      });
      setSuccessNotice(`"${attraction.name}" featured status updated.`);
      setTimeout(() => setSuccessNotice(null), 3000);
    } catch (err) {
      // Revert optimistic update
      setAttractions((prev) =>
        prev.map((a) => (a.id === attraction.id ? { ...a, is_featured: !nextVal } : a))
      );
      setActionError(err instanceof APIError ? err.detail : "Failed to toggle featured status.");
    }
  };

  // Toggle Publish / Draft status inline
  const handleToggleStatus = async (attraction: Attraction) => {
    const current = (attraction.status || "draft").toLowerCase();
    const nextStatus = current === "published" || current === "approved" ? "draft" : "published";

    // Optimistic update
    setAttractions((prev) =>
      prev.map((a) => (a.id === attraction.id ? { ...a, status: nextStatus } : a))
    );
    if (inspectTarget?.id === attraction.id) {
      setInspectTarget({ ...inspectTarget, status: nextStatus });
    }

    try {
      await fetchAPI(`/api/attractions/${attraction.id}`, {
        method: "PUT",
        body: JSON.stringify({ status: nextStatus }),
      });
      setSuccessNotice(`"${attraction.name}" set to ${nextStatus}.`);
      setTimeout(() => setSuccessNotice(null), 3000);
    } catch (err) {
      // Revert
      setAttractions((prev) =>
        prev.map((a) => (a.id === attraction.id ? { ...a, status: current } : a))
      );
      setActionError(err instanceof APIError ? err.detail : "Failed to update attraction status.");
    }
  };

  const handleDelete = async () => {
    if (!deleteTarget) return;
    try {
      await fetchAPI(`/api/attractions/${deleteTarget.id}`, { method: "DELETE" });
      setAttractions((prev) => prev.filter((a) => a.id !== deleteTarget.id));
      if (inspectTarget?.id === deleteTarget.id) {
        setInspectTarget(null);
      }
      setDeleteTarget(null);
      setSuccessNotice(`Deleted "${deleteTarget.name}".`);
      setTimeout(() => setSuccessNotice(null), 3000);
    } catch (err) {
      setActionError(err instanceof APIError ? err.detail : "Failed to delete attraction.");
    }
  };

  const handleCopyCoords = (a: Attraction) => {
    if (a.latitude != null && a.longitude != null) {
      navigator.clipboard.writeText(`${a.latitude}, ${a.longitude}`);
      setCopiedCoords(a.id);
      setTimeout(() => setCopiedCoords(null), 2000);
    }
  };

  // Unique lists for filtering
  const categories = useMemo(() => {
    const set = new Set<string>();
    attractions.forEach((a) => {
      if (a.category) set.add(a.category);
    });
    return Array.from(set).sort();
  }, [attractions]);

  const barangays = useMemo(() => {
    const set = new Set<string>();
    attractions.forEach((a) => {
      if (a.barangay_name) set.add(a.barangay_name);
    });
    return Array.from(set).sort();
  }, [attractions]);

  // Filtered & Sorted list
  const filteredAttractions = useMemo(() => {
    return attractions
      .filter((a) => {
        // Search query
        if (searchQuery.trim()) {
          const q = searchQuery.toLowerCase();
          const matchName = a.name?.toLowerCase().includes(q);
          const matchDesc = a.description?.toLowerCase().includes(q);
          const matchBarangay = a.barangay_name?.toLowerCase().includes(q);
          const matchCat = a.category?.toLowerCase().includes(q);
          if (!matchName && !matchDesc && !matchBarangay && !matchCat) return false;
        }
        // Category
        if (selectedCategory !== "all" && a.category !== selectedCategory) {
          return false;
        }
        // Status
        if (selectedStatus !== "all") {
          const st = (a.status || "draft").toLowerCase();
          if (selectedStatus === "published" && st !== "published" && st !== "approved") return false;
          if (selectedStatus === "draft" && st !== "draft" && st !== "pending") return false;
          if (selectedStatus === "archived" && st !== "archived") return false;
        }
        // Featured
        if (featuredOnly && !a.is_featured) {
          return false;
        }
        // Barangay
        if (selectedBarangay !== "all" && a.barangay_name !== selectedBarangay) {
          return false;
        }
        return true;
      })
      .sort((a, b) => {
        if (sortBy === "name") return a.name.localeCompare(b.name);
        if (sortBy === "rating") return (b.rating || 0) - (a.rating || 0);
        if (sortBy === "status") return (a.status || "").localeCompare(b.status || "");
        if (sortBy === "newest") return (b.id || 0) - (a.id || 0);
        return 0;
      });
  }, [attractions, searchQuery, selectedCategory, selectedStatus, selectedBarangay, featuredOnly, sortBy]);

  // Statistics calculation
  const totalCount = attractions.length;
  const publishedCount = attractions.filter(
    (a) => (a.status || "").toLowerCase() === "published" || (a.status || "").toLowerCase() === "approved"
  ).length;
  const draftCount = attractions.filter(
    (a) => (a.status || "").toLowerCase() === "draft" || (a.status || "").toLowerCase() === "pending"
  ).length;
  const featuredCount = attractions.filter((a) => a.is_featured).length;

  if (authLoading || !user || loading) {
    return (
      <div className="container mx-auto px-4 py-16 max-w-7xl">
        <div className="flex flex-col items-center justify-center gap-3">
          <Loader2 className="h-8 w-8 animate-spin text-primary" />
          <p className="text-sm text-muted-foreground animate-pulse">Loading attraction database...</p>
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
            <Compass className="h-6 w-6" />
          </div>
          <div>
            <div className="flex items-center gap-2.5">
              <h1 className="text-2xl sm:text-3xl font-extrabold tracking-tight text-foreground">
                Attraction Management
              </h1>
              <Badge variant="outline" className="font-mono text-xs px-2.5 py-0.5 rounded-full border-border bg-muted/50">
                {totalCount} Total
              </Badge>
            </div>
            <p className="text-sm text-muted-foreground mt-1">
              Curate, review, and manage cultural and ecotourism landmarks across Mangatarem
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
            onClick={() => router.push("/admin/attractions/new")}
            className="rounded-xl h-10 gap-2 bg-primary text-primary-foreground hover:bg-primary/90 shadow-sm transition-all"
          >
            <Plus className="h-4 w-4" />
            <span>Add Landmark</span>
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
              <p className="text-xs font-medium text-muted-foreground uppercase tracking-wider">Total Sites</p>
              <h3 className="text-2xl font-bold mt-1 text-foreground">{totalCount}</h3>
              <p className="text-xs text-muted-foreground mt-0.5">{categories.length} distinct categories</p>
            </div>
            <div className="h-11 w-11 rounded-xl bg-primary/10 text-primary flex items-center justify-center">
              <MapPin className="h-5 w-5" />
            </div>
          </CardContent>
        </Card>

        <Card className="rounded-2xl border-border/60 shadow-xs bg-card/60 backdrop-blur-xs">
          <CardContent className="p-4 sm:p-5 flex items-center justify-between">
            <div>
              <p className="text-xs font-medium text-muted-foreground uppercase tracking-wider">Published / Live</p>
              <h3 className="text-2xl font-bold mt-1 text-foreground">{publishedCount}</h3>
              <p className="text-xs text-emerald-600 dark:text-emerald-400 mt-0.5 flex items-center gap-1">
                <CheckCircle2 className="h-3 w-3 inline" />
                {totalCount > 0 ? `${Math.round((publishedCount / totalCount) * 100)}% of catalog` : "0%"}
              </p>
            </div>
            <div className="h-11 w-11 rounded-xl bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 flex items-center justify-center">
              <Layers className="h-5 w-5" />
            </div>
          </CardContent>
        </Card>

        <Card className="rounded-2xl border-border/60 shadow-xs bg-card/60 backdrop-blur-xs">
          <CardContent className="p-4 sm:p-5 flex items-center justify-between">
            <div>
              <p className="text-xs font-medium text-muted-foreground uppercase tracking-wider">Draft / Review</p>
              <h3 className="text-2xl font-bold mt-1 text-foreground">{draftCount}</h3>
              <p className="text-xs text-amber-600 dark:text-amber-400 mt-0.5">
                {draftCount > 0 ? "Pending publication" : "All up to date"}
              </p>
            </div>
            <div className="h-11 w-11 rounded-xl bg-amber-500/10 text-amber-600 dark:text-amber-400 flex items-center justify-center">
              <Clock className="h-5 w-5" />
            </div>
          </CardContent>
        </Card>

        <Card className="rounded-2xl border-border/60 shadow-xs bg-card/60 backdrop-blur-xs">
          <CardContent className="p-4 sm:p-5 flex items-center justify-between">
            <div>
              <p className="text-xs font-medium text-muted-foreground uppercase tracking-wider">Featured</p>
              <h3 className="text-2xl font-bold mt-1 text-foreground">{featuredCount}</h3>
              <p className="text-xs text-amber-500 mt-0.5 flex items-center gap-1">
                <Sparkles className="h-3 w-3 inline" /> Promoted on homepage
              </p>
            </div>
            <div className="h-11 w-11 rounded-xl bg-amber-500/10 text-amber-500 flex items-center justify-center">
              <Star className="h-5 w-5 fill-amber-500/20" />
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
              placeholder="Search attractions by name, description, barangay..."
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
              <option value="published">Published</option>
              <option value="draft">Draft</option>
              <option value="archived">Archived</option>
            </select>

            {/* Barangay Select */}
            {barangays.length > 0 && (
              <select
                value={selectedBarangay}
                onChange={(e) => setSelectedBarangay(e.target.value)}
                className="h-10 px-3 rounded-xl bg-background border border-border/80 text-sm font-medium text-foreground focus:outline-none focus:ring-1 focus:ring-primary cursor-pointer max-w-[160px] truncate"
              >
                <option value="all">All Barangays</option>
                {barangays.map((b) => (
                  <option key={b} value={b}>
                    {b}
                  </option>
                ))}
              </select>
            )}

            {/* Featured toggle button */}
            <Button
              variant={featuredOnly ? "default" : "outline"}
              size="sm"
              onClick={() => setFeaturedOnly(!featuredOnly)}
              className={`h-10 rounded-xl gap-1.5 transition-colors ${
                featuredOnly
                  ? "bg-amber-500 text-white hover:bg-amber-600 border-amber-600"
                  : "bg-background text-muted-foreground hover:text-foreground"
              }`}
            >
              <Star className={`h-3.5 w-3.5 ${featuredOnly ? "fill-white" : ""}`} />
              <span className="text-xs font-semibold">Featured</span>
            </Button>

            {/* Sort options */}
            <div className="flex items-center rounded-xl bg-background border border-border/80 h-10 px-2 gap-1 text-muted-foreground">
              <ArrowUpDown className="h-3.5 w-3.5 ml-1 text-muted-foreground/80" />
              <select
                value={sortBy}
                onChange={(e) => setSortBy(e.target.value as "name" | "rating" | "newest" | "status")}
                className="bg-transparent border-0 text-xs font-medium text-foreground focus:outline-none cursor-pointer pr-2"
              >
                <option value="name">Name (A-Z)</option>
                <option value="rating">Top Rated</option>
                <option value="newest">Newest Added</option>
                <option value="status">Status</option>
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
        {(searchQuery || selectedCategory !== "all" || selectedStatus !== "all" || selectedBarangay !== "all" || featuredOnly) && (
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
            {selectedCategory !== "all" && (
              <Badge variant="secondary" className="gap-1 rounded-md text-xs py-0.5">
                Category: {selectedCategory}
                <button onClick={() => setSelectedCategory("all")} className="hover:text-foreground cursor-pointer">
                  <X className="h-3 w-3" />
                </button>
              </Badge>
            )}
            {selectedStatus !== "all" && (
              <Badge variant="secondary" className="gap-1 rounded-md text-xs py-0.5">
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
            {featuredOnly && (
              <Badge variant="secondary" className="gap-1 rounded-md text-xs py-0.5">
                Featured Only
                <button onClick={() => setFeaturedOnly(false)} className="hover:text-foreground cursor-pointer">
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
                setSelectedBarangay("all");
                setFeaturedOnly(false);
              }}
              className="h-6 px-2 text-xs text-primary hover:underline hover:bg-transparent"
            >
              Reset all
            </Button>
            <span className="ml-auto text-xs font-medium text-foreground">
              Showing {filteredAttractions.length} of {totalCount}
            </span>
          </div>
        )}
      </div>

      {/* Content Rendering: Grid vs Table */}
      {filteredAttractions.length === 0 ? (
        <div className="border border-dashed border-border/80 rounded-2xl py-20 text-center bg-card/40">
          <div className="h-14 w-14 rounded-2xl bg-muted/80 text-muted-foreground/60 flex items-center justify-center mx-auto mb-4 border border-border/60">
            <Compass className="h-7 w-7" />
          </div>
          <h3 className="text-base font-bold text-foreground">No attractions found</h3>
          <p className="text-sm text-muted-foreground mt-1 max-w-sm mx-auto">
            We couldn&apos;t find any attractions matching your current search or filter criteria.
          </p>
          <div className="mt-5 flex justify-center gap-3">
            <Button
              variant="outline"
              size="sm"
              onClick={() => {
                setSearchQuery("");
                setSelectedCategory("all");
                setSelectedStatus("all");
                setSelectedBarangay("all");
                setFeaturedOnly(false);
              }}
              className="rounded-xl"
            >
              Clear Filters
            </Button>
            <Button
              size="sm"
              onClick={() => router.push("/admin/attractions/new")}
              className="rounded-xl gap-1.5"
            >
              <Plus className="h-4 w-4" /> Add Landmark
            </Button>
          </div>
        </div>
      ) : viewMode === "grid" ? (
        /* Visual Card Grid Mode */
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
          {filteredAttractions.map((attraction) => {
            const isLive =
              (attraction.status || "").toLowerCase() === "published" ||
              (attraction.status || "").toLowerCase() === "approved";
            const categoryStyle =
              CATEGORY_COLORS[attraction.category] ??
              "bg-primary/10 text-primary border-primary/20";

            return (
              <Card
                key={attraction.id}
                className="group relative overflow-hidden rounded-2xl border-border/60 hover:border-border transition-all duration-200 hover:shadow-md bg-card flex flex-col justify-between"
              >
                <div>
                  {/* Image & Header Overlay */}
                  <div className="relative aspect-video w-full overflow-hidden bg-muted">
                    {attraction.image_url ? (
                      // eslint-disable-next-line @next/next/no-img-element
                      <img
                        src={attraction.image_url}
                        alt={attraction.name}
                        className="h-full w-full object-cover transition-transform duration-300 group-hover:scale-105"
                      />
                    ) : (
                      <div className="flex h-full w-full items-center justify-center bg-gradient-to-br from-muted to-muted/60 text-muted-foreground/40">
                        <Compass className="h-12 w-12" />
                      </div>
                    )}

                    {/* Gradient shade */}
                    <div className="absolute inset-0 bg-gradient-to-t from-black/70 via-black/20 to-transparent" />

                    {/* Category badge on top left */}
                    <div className="absolute top-3 left-3">
                      <span
                        className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-semibold backdrop-blur-md border ${categoryStyle}`}
                      >
                        {attraction.category || "General"}
                      </span>
                    </div>

                    {/* Featured star toggle top right */}
                    <div className="absolute top-3 right-3 flex items-center gap-1.5">
                      <button
                        onClick={(e) => {
                          e.stopPropagation();
                          handleToggleFeatured(attraction);
                        }}
                        className={`p-1.5 rounded-full backdrop-blur-md transition-all cursor-pointer ${
                          attraction.is_featured
                            ? "bg-amber-500 text-white shadow-sm"
                            : "bg-black/40 text-white/70 hover:text-white hover:bg-black/60"
                        }`}
                        title={attraction.is_featured ? "Featured Landmark" : "Set as Featured"}
                      >
                        <Star className={`h-3.5 w-3.5 ${attraction.is_featured ? "fill-white" : ""}`} />
                      </button>
                    </div>

                    {/* Bottom overlay: Barangay & Rating */}
                    <div className="absolute bottom-3 left-3 right-3 flex items-center justify-between text-white text-xs">
                      <div className="flex items-center gap-1 truncate font-medium drop-shadow-xs">
                        <MapPin className="h-3.5 w-3.5 flex-shrink-0 text-primary" />
                        <span className="truncate">
                          {attraction.barangay_name ? `Brgy. ${attraction.barangay_name}` : "Mangatarem"}
                        </span>
                      </div>
                      {attraction.rating != null && attraction.rating > 0 && (
                        <div className="flex items-center gap-1 bg-black/50 backdrop-blur-md px-2 py-0.5 rounded-md font-semibold text-amber-400">
                          <Star className="h-3 w-3 fill-amber-400" />
                          <span>{attraction.rating.toFixed(1)}</span>
                        </div>
                      )}
                    </div>
                  </div>

                  {/* Body Details */}
                  <div className="p-4 sm:p-5 space-y-3">
                    <div>
                      <div className="flex items-start justify-between gap-2">
                        <h3 className="font-bold text-base text-foreground line-clamp-1 group-hover:text-primary transition-colors">
                          {attraction.name}
                        </h3>
                        <button
                          onClick={() => handleToggleStatus(attraction)}
                          className="cursor-pointer flex-shrink-0"
                          title={`Click to ${isLive ? "unpublish" : "publish"}`}
                        >
                          <Badge
                            variant="outline"
                            className={`text-[10px] font-bold uppercase tracking-wider px-2 py-0.5 rounded-full border transition-colors ${
                              isLive
                                ? "bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 border-emerald-500/20 hover:bg-emerald-500/20"
                                : "bg-amber-500/10 text-amber-600 dark:text-amber-400 border-amber-500/20 hover:bg-amber-500/20"
                            }`}
                          >
                            {isLive ? "Published" : "Draft"}
                          </Badge>
                        </button>
                      </div>
                      <p className="text-xs text-muted-foreground line-clamp-2 mt-1.5 leading-relaxed">
                        {attraction.description || "No description provided for this attraction yet."}
                      </p>
                    </div>

                    {/* Coordinate snippet if present */}
                    {attraction.latitude != null && attraction.longitude != null && (
                      <div className="flex items-center justify-between text-[11px] text-muted-foreground bg-muted/40 rounded-lg px-2.5 py-1.5 font-mono">
                        <span className="truncate">
                          {attraction.latitude.toFixed(4)}, {attraction.longitude.toFixed(4)}
                        </span>
                        <button
                          onClick={() => handleCopyCoords(attraction)}
                          className="hover:text-foreground p-0.5 rounded cursor-pointer transition-colors"
                          title="Copy Coordinates"
                        >
                          {copiedCoords === attraction.id ? (
                            <Check className="h-3 w-3 text-emerald-500" />
                          ) : (
                            <Copy className="h-3 w-3" />
                          )}
                        </button>
                      </div>
                    )}
                  </div>
                </div>

                {/* Card Actions Footer */}
                <div className="p-4 pt-0 sm:p-5 sm:pt-0 flex items-center justify-between gap-2 border-t border-border/40 mt-2">
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => setInspectTarget(attraction)}
                    className="rounded-xl h-8 text-xs gap-1.5 flex-1 hover:bg-muted"
                  >
                    <Eye className="h-3.5 w-3.5 text-muted-foreground" />
                    Quick View
                  </Button>

                  <div className="flex items-center gap-1">
                    <Button
                      variant="ghost"
                      size="icon"
                      onClick={() => router.push(`/admin/attractions/${attraction.id}/edit`)}
                      className="h-8 w-8 rounded-lg text-muted-foreground hover:text-foreground hover:bg-muted"
                      title="Edit Attraction"
                    >
                      <Pencil className="h-3.5 w-3.5" />
                    </Button>
                    <Button
                      variant="ghost"
                      size="icon"
                      onClick={() => setDeleteTarget(attraction)}
                      className="h-8 w-8 rounded-lg text-muted-foreground hover:text-destructive hover:bg-destructive/10"
                      title="Delete Attraction"
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
                <TableHead className="w-[80px]">Image</TableHead>
                <TableHead>Landmark Name</TableHead>
                <TableHead>Category</TableHead>
                <TableHead>Barangay</TableHead>
                <TableHead className="text-center">Featured</TableHead>
                <TableHead>Status</TableHead>
                <TableHead className="text-right">Actions</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {filteredAttractions.map((attraction) => {
                const isLive =
                  (attraction.status || "").toLowerCase() === "published" ||
                  (attraction.status || "").toLowerCase() === "approved";
                const categoryStyle =
                  CATEGORY_COLORS[attraction.category] ??
                  "bg-primary/10 text-primary border-primary/20";

                return (
                  <TableRow key={attraction.id} className="hover:bg-muted/30 transition-colors">
                    {/* Thumbnail */}
                    <TableCell className="py-3">
                      <div className="h-12 w-12 rounded-xl overflow-hidden bg-muted border border-border/50 flex-shrink-0">
                        {attraction.image_url ? (
                          // eslint-disable-next-line @next/next/no-img-element
                          <img
                            src={attraction.image_url}
                            alt={attraction.name}
                            className="h-full w-full object-cover"
                          />
                        ) : (
                          <div className="flex h-full w-full items-center justify-center text-muted-foreground/40">
                            <Compass className="h-5 w-5" />
                          </div>
                        )}
                      </div>
                    </TableCell>

                    {/* Name & Quick Desc */}
                    <TableCell className="py-3 max-w-xs">
                      <div className="font-bold text-sm text-foreground hover:text-primary cursor-pointer transition-colors"
                        onClick={() => setInspectTarget(attraction)}>
                        {attraction.name}
                      </div>
                      <p className="text-xs text-muted-foreground line-clamp-1 mt-0.5">
                        {attraction.description || "No description"}
                      </p>
                    </TableCell>

                    {/* Category */}
                    <TableCell className="py-3">
                      <Badge
                        variant="outline"
                        className={`text-xs font-semibold border ${categoryStyle}`}
                      >
                        {attraction.category || "General"}
                      </Badge>
                    </TableCell>

                    {/* Barangay */}
                    <TableCell className="py-3 text-sm text-muted-foreground">
                      <div className="flex items-center gap-1 text-xs">
                        <MapPin className="h-3.5 w-3.5 text-muted-foreground/70" />
                        <span>{attraction.barangay_name || "Mangatarem"}</span>
                      </div>
                    </TableCell>

                    {/* Featured toggle */}
                    <TableCell className="py-3 text-center">
                      <button
                        onClick={() => handleToggleFeatured(attraction)}
                        className={`p-1.5 rounded-lg transition-colors cursor-pointer inline-flex items-center justify-center ${
                          attraction.is_featured
                            ? "text-amber-500 bg-amber-500/10 hover:bg-amber-500/20"
                            : "text-muted-foreground/40 hover:text-amber-500 hover:bg-muted"
                        }`}
                        title={attraction.is_featured ? "Featured on homepage" : "Set as featured"}
                      >
                        <Star className={`h-4 w-4 ${attraction.is_featured ? "fill-amber-500" : ""}`} />
                      </button>
                    </TableCell>

                    {/* Status */}
                    <TableCell className="py-3">
                      <button
                        onClick={() => handleToggleStatus(attraction)}
                        className="cursor-pointer"
                        title={`Click to switch to ${isLive ? "draft" : "published"}`}
                      >
                        <Badge
                          variant="outline"
                          className={`text-[11px] font-semibold capitalize px-2.5 py-0.5 rounded-full border transition-colors ${
                            isLive
                              ? "bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 border-emerald-500/20 hover:bg-emerald-500/20"
                              : "bg-amber-500/10 text-amber-600 dark:text-amber-400 border-amber-500/20 hover:bg-amber-500/20"
                          }`}
                        >
                          {isLive ? "Published" : "Draft"}
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
                          onClick={() => setInspectTarget(attraction)}
                          title="Quick View"
                        >
                          <Eye className="h-3.5 w-3.5" />
                        </Button>
                        <Button
                          variant="ghost"
                          size="icon"
                          className="h-8 w-8 rounded-lg text-muted-foreground hover:text-foreground"
                          onClick={() => router.push(`/admin/attractions/${attraction.id}/edit`)}
                          title="Edit Attraction"
                        >
                          <Pencil className="h-3.5 w-3.5" />
                        </Button>
                        <Button
                          variant="ghost"
                          size="icon"
                          className="h-8 w-8 rounded-lg text-muted-foreground hover:text-destructive hover:bg-destructive/10"
                          onClick={() => setDeleteTarget(attraction)}
                          title="Delete Attraction"
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
                    <Compass className="h-16 w-16" />
                  </div>
                )}
                <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-black/30 to-transparent" />
                <div className="absolute bottom-4 left-5 right-5 text-white">
                  <div className="flex items-center gap-2 mb-1.5">
                    <Badge variant="outline" className="text-xs bg-white/20 text-white backdrop-blur-md border-white/30">
                      {inspectTarget.category}
                    </Badge>
                    {inspectTarget.is_featured && (
                      <Badge className="text-xs bg-amber-500 text-white gap-1 border-0">
                        <Star className="h-3 w-3 fill-white" /> Featured
                      </Badge>
                    )}
                  </div>
                  <h2 className="text-xl font-bold">{inspectTarget.name}</h2>
                  <p className="text-xs text-white/80 flex items-center gap-1 mt-1">
                    <MapPin className="h-3.5 w-3.5 text-primary" />
                    {inspectTarget.barangay_name ? `Brgy. ${inspectTarget.barangay_name}, Mangatarem` : "Mangatarem, Pangasinan"}
                  </p>
                </div>
              </div>

              {/* Sheet Metadata Body */}
              <div className="px-6 space-y-5">
                {/* Description */}
                <div>
                  <h4 className="text-xs font-bold uppercase tracking-wider text-muted-foreground mb-1.5">
                    Overview
                  </h4>
                  <p className="text-sm text-foreground leading-relaxed">
                    {inspectTarget.description || "No description provided."}
                  </p>
                </div>

                {/* Advisory Banner if exists */}
                {inspectTarget.advisory_message && (
                  <div className="rounded-xl border border-amber-500/30 bg-amber-500/10 p-3.5 text-xs text-amber-800 dark:text-amber-300 flex items-start gap-2.5">
                    <ShieldAlert className="h-4 w-4 flex-shrink-0 mt-0.5 text-amber-600 dark:text-amber-400" />
                    <div>
                      <span className="font-bold block mb-0.5">
                        Visitor Advisory ({inspectTarget.advisory_status || "Active"})
                      </span>
                      {inspectTarget.advisory_message}
                    </div>
                  </div>
                )}

                {/* Key Attributes Grid */}
                <div className="grid grid-cols-2 gap-3 pt-2">
                  <div className="p-3 rounded-xl bg-muted/40 border border-border/50">
                    <span className="text-[11px] font-medium text-muted-foreground flex items-center gap-1 mb-1">
                      <Clock className="h-3 w-3" /> Operating Hours
                    </span>
                    <p className="text-xs font-semibold text-foreground">
                      {inspectTarget.opening_hours || "Always Open / Unspecified"}
                    </p>
                  </div>

                  <div className="p-3 rounded-xl bg-muted/40 border border-border/50">
                    <span className="text-[11px] font-medium text-muted-foreground flex items-center gap-1 mb-1">
                      <Banknote className="h-3 w-3" /> Entrance Fee
                    </span>
                    <p className="text-xs font-semibold text-foreground">
                      {inspectTarget.entrance_fee || "Free / Public Access"}
                    </p>
                  </div>

                  <div className="p-3 rounded-xl bg-muted/40 border border-border/50">
                    <span className="text-[11px] font-medium text-muted-foreground flex items-center gap-1 mb-1">
                      <Phone className="h-3 w-3" /> Contact Info
                    </span>
                    <p className="text-xs font-semibold text-foreground truncate">
                      {inspectTarget.contact_info || "Mangatarem Tourism Office"}
                    </p>
                  </div>

                  <div className="p-3 rounded-xl bg-muted/40 border border-border/50">
                    <span className="text-[11px] font-medium text-muted-foreground flex items-center gap-1 mb-1">
                      <Layers className="h-3 w-3" /> Physical Status
                    </span>
                    <p className="text-xs font-semibold text-foreground">
                      {inspectTarget.physical_status || "Open Public"}
                    </p>
                  </div>
                </div>

                {/* Facilities */}
                {inspectTarget.facilities && (
                  <div>
                    <h4 className="text-xs font-bold uppercase tracking-wider text-muted-foreground mb-2">
                      Available Amenities & Facilities
                    </h4>
                    <div className="flex flex-wrap gap-1.5">
                      {Array.isArray(inspectTarget.facilities)
                        ? inspectTarget.facilities.map((fac, i) => (
                            <Badge key={i} variant="secondary" className="text-xs font-normal">
                              {fac}
                            </Badge>
                          ))
                        : String(inspectTarget.facilities)
                            .split(",")
                            .map((fac, i) => (
                              <Badge key={i} variant="secondary" className="text-xs font-normal">
                                {fac.trim()}
                              </Badge>
                            ))}
                    </div>
                  </div>
                )}

                {/* GPS Coordinates */}
                {inspectTarget.latitude != null && inspectTarget.longitude != null && (
                  <div className="p-3.5 rounded-xl border border-border/60 bg-muted/20 flex items-center justify-between gap-3">
                    <div className="space-y-0.5">
                      <span className="text-[11px] font-medium text-muted-foreground">Coordinates (Lat, Lng)</span>
                      <p className="text-xs font-mono font-semibold text-foreground">
                        {inspectTarget.latitude.toFixed(6)}, {inspectTarget.longitude.toFixed(6)}
                      </p>
                    </div>
                    <div className="flex items-center gap-1.5">
                      <Button
                        size="sm"
                        variant="outline"
                        onClick={() => handleCopyCoords(inspectTarget)}
                        className="h-8 rounded-lg text-xs gap-1"
                      >
                        {copiedCoords === inspectTarget.id ? (
                          <>
                            <Check className="h-3 w-3 text-emerald-500" /> Copied
                          </>
                        ) : (
                          <>
                            <Copy className="h-3 w-3" /> Copy
                          </>
                        )}
                      </Button>
                      <a
                        href={`https://www.google.com/maps?q=${inspectTarget.latitude},${inspectTarget.longitude}`}
                        target="_blank"
                        rel="noreferrer"
                        className="inline-flex items-center justify-center h-8 px-2.5 rounded-lg border border-border bg-background text-xs font-medium text-muted-foreground hover:text-foreground hover:bg-muted transition-colors gap-1"
                      >
                        <ExternalLink className="h-3 w-3" /> Map
                      </a>
                    </div>
                  </div>
                )}
              </div>

              {/* Action Buttons in Sheet */}
              <div className="px-6 pt-4 border-t border-border/60 flex flex-col gap-2.5">
                <div className="grid grid-cols-2 gap-2">
                  <Button
                    variant="outline"
                    onClick={() => handleToggleFeatured(inspectTarget)}
                    className="rounded-xl h-10 text-xs gap-1.5"
                  >
                    <Star className={`h-3.5 w-3.5 ${inspectTarget.is_featured ? "fill-amber-500 text-amber-500" : ""}`} />
                    {inspectTarget.is_featured ? "Unfeature" : "Feature"}
                  </Button>

                  <Button
                    variant="outline"
                    onClick={() => handleToggleStatus(inspectTarget)}
                    className="rounded-xl h-10 text-xs gap-1.5"
                  >
                    <CheckCircle2 className="h-3.5 w-3.5" />
                    {(inspectTarget.status || "").toLowerCase() === "published" ? "Set to Draft" : "Publish"}
                  </Button>
                </div>

                <div className="flex items-center gap-2">
                  <Link
                    href={`/attractions/${inspectTarget.id}`}
                    target="_blank"
                    className="flex-1 inline-flex items-center justify-center h-10 rounded-xl bg-muted hover:bg-muted/80 text-foreground font-medium text-xs gap-1.5 border border-border/60 transition-colors"
                  >
                    <ExternalLink className="h-3.5 w-3.5" /> Public Page
                  </Link>

                  <Button
                    onClick={() => router.push(`/admin/attractions/${inspectTarget.id}/edit`)}
                    className="flex-1 rounded-xl h-10 text-xs gap-1.5 bg-primary text-primary-foreground"
                  >
                    <Pencil className="h-3.5 w-3.5" /> Full Edit
                  </Button>
                </div>
              </div>
            </div>
          )}
        </SheetContent>
      </Sheet>

      {/* Delete Confirmation Dialog */}
      <DeleteDialog
        open={!!deleteTarget}
        onOpenChange={(open) => !open && setDeleteTarget(null)}
        onConfirm={handleDelete}
        title="Delete Attraction Landmark"
        description={`Are you sure you want to permanently remove "${deleteTarget?.name ?? ""}"? This action will remove it from the digital cultural map and visitor directories.`}
      />
    </div>
  );
}

