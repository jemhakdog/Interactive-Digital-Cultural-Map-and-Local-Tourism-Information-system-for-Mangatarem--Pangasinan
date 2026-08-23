"use client";

import { useEffect, useState, useMemo, useCallback } from "react";
import { useAuth } from "@/lib/auth";
import { fetchAPI } from "@/lib/api";
import { useRouter } from "next/navigation";
import {
  Loader2,
  Images,
  Check,
  X,
  Trash2,
  Search,
  LayoutGrid,
  List,
  ExternalLink,
  Film,
  Camera,
  Maximize2,
  RefreshCw,
  Copy,
  Clock,
  CheckCircle2,
  XCircle,
  AlertCircle,
  ChevronLeft,
  ChevronRight,
} from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogDescription,
} from "@/components/ui/dialog";

interface GalleryRow {
  id: number;
  type: string;
  url: string;
  caption?: string | null;
  status: string;
  created_at?: string | null;
}

type StatusFilter = "all" | "pending" | "approved" | "rejected";
type MediaTypeFilter = "all" | "image" | "video";
type SortOption = "newest" | "oldest" | "status";

const STATUS_CONFIG: Record<
  string,
  { label: string; badgeClass: string; icon: typeof CheckCircle2 }
> = {
  pending: {
    label: "Pending Review",
    badgeClass: "bg-amber-500/10 text-amber-600 border-amber-500/20 dark:text-amber-400",
    icon: Clock,
  },
  approved: {
    label: "Approved",
    badgeClass: "bg-emerald-500/10 text-emerald-600 border-emerald-500/20 dark:text-emerald-400",
    icon: CheckCircle2,
  },
  rejected: {
    label: "Rejected",
    badgeClass: "bg-rose-500/10 text-rose-600 border-rose-500/20 dark:text-rose-400",
    icon: XCircle,
  },
};

export default function AdminGalleryPage() {
  const { user, loading: authLoading } = useAuth();
  const router = useRouter();

  const [items, setItems] = useState<GalleryRow[]>([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [successMsg, setSuccessMsg] = useState<string | null>(null);

  // Filters & Search
  const [statusFilter, setStatusFilter] = useState<StatusFilter>("pending");
  const [mediaTypeFilter, setMediaTypeFilter] = useState<MediaTypeFilter>("all");
  const [searchQuery, setSearchQuery] = useState("");
  const [sortBy, setSortBy] = useState<SortOption>("newest");
  const [viewMode, setViewMode] = useState<"grid" | "table">("grid");

  // Selection & Batch Operations
  const [selectedIds, setSelectedIds] = useState<Set<number>>(new Set());
  const [actingId, setActingId] = useState<number | null>(null);
  const [isBatchProcessing, setIsBatchProcessing] = useState(false);

  // Modal / Preview Inspection
  const [inspectItem, setInspectItem] = useState<GalleryRow | null>(null);
  const [copiedUrl, setCopiedUrl] = useState(false);

  // Delete Confirmation Modal
  const [itemToDelete, setItemToDelete] = useState<GalleryRow | null>(null);

  const load = useCallback(async (isRefresh = false) => {
    if (isRefresh) setRefreshing(true);
    else setLoading(true);
    setError(null);
    try {
      const data = await fetchAPI<{ items: GalleryRow[] }>("/api/admin/gallery");
      setItems(data.items || []);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load gallery items.");
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  }, []);

  useEffect(() => {
    if (!authLoading && (!user || user.role !== "admin")) {
      router.push("/dashboard");
    }
  }, [user, authLoading, router]);

  useEffect(() => {
    if (!user || user.role !== "admin") return;
    load();
  }, [user, load]);

  // Status message timer
  useEffect(() => {
    if (successMsg) {
      const timer = setTimeout(() => setSuccessMsg(null), 3500);
      return () => clearTimeout(timer);
    }
  }, [successMsg]);

  // Statistics calculation
  const stats = useMemo(() => {
    const total = items.length;
    const pending = items.filter((i) => i.status === "pending").length;
    const approved = items.filter((i) => i.status === "approved").length;
    const rejected = items.filter((i) => i.status === "rejected").length;
    const images = items.filter(
      (i) => i.type === "image" || /\.(jpg|jpeg|png|gif|webp)$/i.test(i.url)
    ).length;
    const videos = total - images;
    return { total, pending, approved, rejected, images, videos };
  }, [items]);

  // Filtered & Sorted items
  const filteredItems = useMemo(() => {
    return items
      .filter((item) => {
        // Status filter
        if (statusFilter !== "all" && item.status !== statusFilter) return false;

        // Media type filter
        const isImg = item.type === "image" || /\.(jpg|jpeg|png|gif|webp)$/i.test(item.url);
        if (mediaTypeFilter === "image" && !isImg) return false;
        if (mediaTypeFilter === "video" && isImg) return false;

        // Search query filter
        if (searchQuery.trim()) {
          const q = searchQuery.toLowerCase().trim();
          const matchCaption = item.caption?.toLowerCase().includes(q);
          const matchUrl = item.url.toLowerCase().includes(q);
          const matchId = String(item.id).includes(q);
          if (!matchCaption && !matchUrl && !matchId) return false;
        }

        return true;
      })
      .sort((a, b) => {
        if (sortBy === "newest") {
          return new Date(b.created_at || 0).getTime() - new Date(a.created_at || 0).getTime();
        }
        if (sortBy === "oldest") {
          return new Date(a.created_at || 0).getTime() - new Date(b.created_at || 0).getTime();
        }
        if (sortBy === "status") {
          const priority: Record<string, number> = { pending: 0, approved: 1, rejected: 2 };
          return (priority[a.status] ?? 3) - (priority[b.status] ?? 3);
        }
        return 0;
      });
  }, [items, statusFilter, mediaTypeFilter, searchQuery, sortBy]);

  // Multi-selection helpers
  const isAllSelected =
    filteredItems.length > 0 && filteredItems.every((item) => selectedIds.has(item.id));

  const toggleSelectAll = () => {
    if (isAllSelected) {
      setSelectedIds(new Set());
    } else {
      const next = new Set(selectedIds);
      filteredItems.forEach((item) => next.add(item.id));
      setSelectedIds(next);
    }
  };

  const toggleSelectItem = (id: number) => {
    const next = new Set(selectedIds);
    if (next.has(id)) {
      next.delete(id);
    } else {
      next.add(id);
    }
    setSelectedIds(next);
  };

  // Moderation Handlers
  const moderate = async (id: number, action: "approve" | "reject") => {
    setActingId(id);
    try {
      await fetchAPI(`/api/admin/gallery/${id}/moderate`, {
        method: "POST",
        body: JSON.stringify({ action }),
      });
      // Update locally for optimistic feel
      setItems((prev) =>
        prev.map((it) => (it.id === id ? { ...it, status: action === "approve" ? "approved" : "rejected" } : it))
      );
      if (inspectItem && inspectItem.id === id) {
        setInspectItem((prev) =>
          prev ? { ...prev, status: action === "approve" ? "approved" : "rejected" } : null
        );
      }
      setSuccessMsg(`Item #${id} marked as ${action === "approve" ? "Approved" : "Rejected"}.`);
    } catch (err) {
      setError(err instanceof Error ? err.message : `Failed to ${action} item.`);
    } finally {
      setActingId(null);
    }
  };

  const remove = async (id: number) => {
    setActingId(id);
    try {
      await fetchAPI(`/api/admin/gallery/${id}`, { method: "DELETE" });
      setItems((prev) => prev.filter((it) => it.id !== id));
      setSelectedIds((prev) => {
        const next = new Set(prev);
        next.delete(id);
        return next;
      });
      if (inspectItem && inspectItem.id === id) {
        setInspectItem(null);
      }
      setItemToDelete(null);
      setSuccessMsg(`Gallery item #${id} permanently deleted.`);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to delete item.");
    } finally {
      setActingId(null);
    }
  };

  // Batch Moderation
  const handleBatchModerate = async (action: "approve" | "reject") => {
    if (selectedIds.size === 0) return;
    setIsBatchProcessing(true);
    const ids = Array.from(selectedIds);
    try {
      await Promise.all(
        ids.map((id) =>
          fetchAPI(`/api/admin/gallery/${id}/moderate`, {
            method: "POST",
            body: JSON.stringify({ action }),
          })
        )
      );
      setItems((prev) =>
        prev.map((it) =>
          selectedIds.has(it.id)
            ? { ...it, status: action === "approve" ? "approved" : "rejected" }
            : it
        )
      );
      setSuccessMsg(`Successfully ${action}d ${ids.length} items.`);
      setSelectedIds(new Set());
    } catch (err) {
      setError(err instanceof Error ? err.message : `Failed to batch ${action} items.`);
    } finally {
      setIsBatchProcessing(false);
    }
  };

  const handleBatchDelete = async () => {
    if (selectedIds.size === 0) return;
    if (!confirm(`Are you sure you want to permanently delete ${selectedIds.size} selected item(s)?`)) {
      return;
    }
    setIsBatchProcessing(true);
    const ids = Array.from(selectedIds);
    try {
      await Promise.all(ids.map((id) => fetchAPI(`/api/admin/gallery/${id}`, { method: "DELETE" })));
      setItems((prev) => prev.filter((it) => !selectedIds.has(it.id)));
      setSuccessMsg(`Successfully deleted ${ids.length} items.`);
      setSelectedIds(new Set());
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to batch delete items.");
    } finally {
      setIsBatchProcessing(false);
    }
  };

  const handleCopyLink = (url: string) => {
    navigator.clipboard.writeText(url);
    setCopiedUrl(true);
    setTimeout(() => setCopiedUrl(false), 2000);
  };

  // Lightbox Navigation
  const handleNextInspect = () => {
    if (!inspectItem) return;
    const currentIndex = filteredItems.findIndex((i) => i.id === inspectItem.id);
    if (currentIndex < filteredItems.length - 1) {
      setInspectItem(filteredItems[currentIndex + 1]);
    }
  };

  const handlePrevInspect = () => {
    if (!inspectItem) return;
    const currentIndex = filteredItems.findIndex((i) => i.id === inspectItem.id);
    if (currentIndex > 0) {
      setInspectItem(filteredItems[currentIndex - 1]);
    }
  };

  if (authLoading || !user || loading) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[60vh] gap-3">
        <Loader2 className="h-8 w-8 animate-spin text-primary" />
        <p className="text-sm font-medium text-muted-foreground">Loading Gallery Moderation Portal...</p>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8 max-w-7xl space-y-6">
      {/* Top Header & Breadcrumb */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-border/60 pb-6">
        <div className="flex items-center gap-3.5">
          <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-primary/10 text-primary border border-primary/20 shadow-xs">
            <Images className="h-6 w-6" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h1 className="text-2xl md:text-3xl font-bold tracking-tight text-foreground">
                Gallery Moderation
              </h1>
              <Badge variant="outline" className="bg-primary/5 text-primary border-primary/20 text-[10px] font-bold uppercase tracking-wider">
                Admin Pro
              </Badge>
            </div>
            <p className="text-muted-foreground text-xs md:text-sm mt-0.5">
              Review, approve, curate, and moderate community media submissions
            </p>
          </div>
        </div>

        <div className="flex items-center gap-2 self-start md:self-auto">
          <Button
            variant="outline"
            size="sm"
            onClick={() => load(true)}
            disabled={refreshing}
            className="gap-1.5 h-9 rounded-xl border-border/80 text-xs font-medium hover:bg-muted/80"
          >
            <RefreshCw className={`h-3.5 w-3.5 ${refreshing ? "animate-spin" : ""}`} />
            <span>Refresh</span>
          </Button>
        </div>
      </div>

      {/* Feedback Alert Banners */}
      {error && (
        <div className="flex items-center justify-between p-4 rounded-xl bg-destructive/10 border border-destructive/20 text-destructive text-sm animate-in fade-in">
          <div className="flex items-center gap-2.5">
            <AlertCircle className="h-5 w-5 shrink-0" />
            <span>{error}</span>
          </div>
          <button onClick={() => setError(null)} className="p-1 hover:opacity-75">
            <X className="h-4 w-4" />
          </button>
        </div>
      )}

      {successMsg && (
        <div className="flex items-center justify-between p-4 rounded-xl bg-emerald-500/10 border border-emerald-500/20 text-emerald-600 dark:text-emerald-400 text-sm animate-in fade-in">
          <div className="flex items-center gap-2.5">
            <CheckCircle2 className="h-5 w-5 shrink-0" />
            <span>{successMsg}</span>
          </div>
          <button onClick={() => setSuccessMsg(null)} className="p-1 hover:opacity-75">
            <X className="h-4 w-4" />
          </button>
        </div>
      )}

      {/* Analytics & Moderation KPI Cards */}
      <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3">
        <button
          onClick={() => setStatusFilter("all")}
          className={`p-3.5 rounded-2xl border text-left transition-all relative overflow-hidden ${
            statusFilter === "all"
              ? "bg-card border-primary ring-2 ring-primary/20 shadow-sm"
              : "bg-card/60 border-border/60 hover:bg-card hover:border-border"
          }`}
        >
          <div className="text-[11px] font-semibold text-muted-foreground uppercase tracking-wider">Total Items</div>
          <div className="text-2xl font-black mt-1 text-foreground">{stats.total}</div>
          <div className="text-[10px] text-muted-foreground mt-0.5">All media uploads</div>
        </button>

        <button
          onClick={() => setStatusFilter("pending")}
          className={`p-3.5 rounded-2xl border text-left transition-all relative overflow-hidden ${
            statusFilter === "pending"
              ? "bg-amber-500/10 border-amber-500 ring-2 ring-amber-500/20 shadow-sm"
              : "bg-card/60 border-border/60 hover:bg-card hover:border-border"
          }`}
        >
          {stats.pending > 0 && (
            <span className="absolute top-2 right-2 flex h-2.5 w-2.5">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-amber-400 opacity-75"></span>
              <span className="relative inline-flex rounded-full h-2.5 w-2.5 bg-amber-500"></span>
            </span>
          )}
          <div className="text-[11px] font-semibold text-amber-600 dark:text-amber-400 uppercase tracking-wider flex items-center gap-1">
            <Clock className="h-3 w-3" /> Pending
          </div>
          <div className="text-2xl font-black mt-1 text-amber-600 dark:text-amber-400">{stats.pending}</div>
          <div className="text-[10px] text-muted-foreground mt-0.5">Awaiting action</div>
        </button>

        <button
          onClick={() => setStatusFilter("approved")}
          className={`p-3.5 rounded-2xl border text-left transition-all relative overflow-hidden ${
            statusFilter === "approved"
              ? "bg-emerald-500/10 border-emerald-500 ring-2 ring-emerald-500/20 shadow-sm"
              : "bg-card/60 border-border/60 hover:bg-card hover:border-border"
          }`}
        >
          <div className="text-[11px] font-semibold text-emerald-600 dark:text-emerald-400 uppercase tracking-wider flex items-center gap-1">
            <CheckCircle2 className="h-3 w-3" /> Approved
          </div>
          <div className="text-2xl font-black mt-1 text-emerald-600 dark:text-emerald-400">{stats.approved}</div>
          <div className="text-[10px] text-muted-foreground mt-0.5">Publicly visible</div>
        </button>

        <button
          onClick={() => setStatusFilter("rejected")}
          className={`p-3.5 rounded-2xl border text-left transition-all relative overflow-hidden ${
            statusFilter === "rejected"
              ? "bg-rose-500/10 border-rose-500 ring-2 ring-rose-500/20 shadow-sm"
              : "bg-card/60 border-border/60 hover:bg-card hover:border-border"
          }`}
        >
          <div className="text-[11px] font-semibold text-rose-600 dark:text-rose-400 uppercase tracking-wider flex items-center gap-1">
            <XCircle className="h-3 w-3" /> Rejected
          </div>
          <div className="text-2xl font-black mt-1 text-rose-600 dark:text-rose-400">{stats.rejected}</div>
          <div className="text-[10px] text-muted-foreground mt-0.5">Hidden from gallery</div>
        </button>

        <div className="p-3.5 rounded-2xl border border-border/60 bg-card/60">
          <div className="text-[11px] font-semibold text-muted-foreground uppercase tracking-wider flex items-center gap-1">
            <Camera className="h-3 w-3" /> Photos
          </div>
          <div className="text-2xl font-black mt-1 text-foreground">{stats.images}</div>
          <div className="text-[10px] text-muted-foreground mt-0.5">Still images</div>
        </div>

        <div className="p-3.5 rounded-2xl border border-border/60 bg-card/60">
          <div className="text-[11px] font-semibold text-muted-foreground uppercase tracking-wider flex items-center gap-1">
            <Film className="h-3 w-3" /> Videos
          </div>
          <div className="text-2xl font-black mt-1 text-foreground">{stats.videos}</div>
          <div className="text-[10px] text-muted-foreground mt-0.5">Clips & motion</div>
        </div>
      </div>

      {/* Filter Toolbar & Actions */}
      <div className="p-4 rounded-2xl border border-border/70 bg-card shadow-xs space-y-4">
        <div className="flex flex-col lg:flex-row gap-3 items-stretch lg:items-center justify-between">
          {/* Search Input */}
          <div className="relative flex-1 max-w-lg">
            <Search className="absolute left-3.5 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
            <Input
              type="text"
              placeholder="Search by caption, URL, or media ID..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="pl-9.5 pr-8 h-10 rounded-xl bg-background border-border/80 text-sm focus-visible:ring-1 focus-visible:ring-primary"
            />
            {searchQuery && (
              <button
                onClick={() => setSearchQuery("")}
                className="absolute right-3 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground"
              >
                <X className="h-3.5 w-3.5" />
              </button>
            )}
          </div>

          {/* Quick Segment Controls */}
          <div className="flex flex-wrap items-center gap-2">
            {/* Media Type Filter */}
            <div className="flex items-center p-1 bg-muted/60 rounded-xl border border-border/50 text-xs">
              <button
                onClick={() => setMediaTypeFilter("all")}
                className={`px-3 py-1.5 rounded-lg font-medium transition-all ${
                  mediaTypeFilter === "all"
                    ? "bg-background text-foreground shadow-xs"
                    : "text-muted-foreground hover:text-foreground"
                }`}
              >
                All Types
              </button>
              <button
                onClick={() => setMediaTypeFilter("image")}
                className={`px-3 py-1.5 rounded-lg font-medium flex items-center gap-1 transition-all ${
                  mediaTypeFilter === "image"
                    ? "bg-background text-foreground shadow-xs"
                    : "text-muted-foreground hover:text-foreground"
                }`}
              >
                <Camera className="h-3.5 w-3.5" /> Photos
              </button>
              <button
                onClick={() => setMediaTypeFilter("video")}
                className={`px-3 py-1.5 rounded-lg font-medium flex items-center gap-1 transition-all ${
                  mediaTypeFilter === "video"
                    ? "bg-background text-foreground shadow-xs"
                    : "text-muted-foreground hover:text-foreground"
                }`}
              >
                <Film className="h-3.5 w-3.5" /> Videos
              </button>
            </div>

            {/* Sort Order Dropdown */}
            <select
              aria-label="Sort gallery items"
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value as SortOption)}
              className="h-9 px-3 rounded-xl border border-border/80 bg-background text-xs font-medium text-foreground focus:outline-none focus:ring-1 focus:ring-primary"
            >
              <option value="newest">Sort: Newest First</option>
              <option value="oldest">Sort: Oldest First</option>
              <option value="status">Sort: By Status Priority</option>
            </select>

            {/* View Switcher */}
            <div className="flex items-center p-1 bg-muted/60 rounded-xl border border-border/50">
              <button
                onClick={() => setViewMode("grid")}
                title="Grid View"
                className={`p-1.5 rounded-lg transition-all ${
                  viewMode === "grid"
                    ? "bg-background text-foreground shadow-xs"
                    : "text-muted-foreground hover:text-foreground"
                }`}
              >
                <LayoutGrid className="h-4 w-4" />
              </button>
              <button
                onClick={() => setViewMode("table")}
                title="Table View"
                className={`p-1.5 rounded-lg transition-all ${
                  viewMode === "table"
                    ? "bg-background text-foreground shadow-xs"
                    : "text-muted-foreground hover:text-foreground"
                }`}
              >
                <List className="h-4 w-4" />
              </button>
            </div>
          </div>
        </div>

        {/* Status Tabs Bar */}
        <div className="flex items-center justify-between border-t border-border/40 pt-3 flex-wrap gap-2">
          <div className="flex gap-1.5 flex-wrap">
            {(["pending", "approved", "rejected", "all"] as StatusFilter[]).map((st) => {
              const count =
                st === "all"
                  ? items.length
                  : items.filter((i) => i.status === st).length;
              return (
                <button
                  key={st}
                  onClick={() => setStatusFilter(st)}
                  className={`px-3.5 py-1.5 rounded-xl font-semibold text-xs capitalize transition-all border ${
                    statusFilter === st
                      ? "bg-primary text-primary-foreground border-primary shadow-xs"
                      : "bg-muted/40 border-border/60 text-muted-foreground hover:bg-muted hover:text-foreground"
                  }`}
                >
                  {st}
                  <span
                    className={`ml-1.5 text-[10px] px-1.5 py-0.2 rounded-full font-mono ${
                      statusFilter === st
                        ? "bg-primary-foreground/20 text-primary-foreground"
                        : "bg-muted-foreground/15 text-muted-foreground"
                    }`}
                  >
                    {count}
                  </span>
                </button>
              );
            })}
          </div>

          {/* Select All Checkbox */}
          {filteredItems.length > 0 && (
            <div className="flex items-center gap-2">
              <Button
                variant="ghost"
                size="sm"
                onClick={toggleSelectAll}
                className="text-xs text-muted-foreground hover:text-foreground h-8 px-2.5 rounded-lg"
              >
                {isAllSelected ? "Deselect All" : "Select All"} ({filteredItems.length})
              </Button>
            </div>
          )}
        </div>
      </div>

      {/* Batch Actions Floating Toolbar */}
      {selectedIds.size > 0 && (
        <div className="sticky top-4 z-20 p-3.5 rounded-2xl bg-card border border-primary/30 shadow-lg shadow-primary/5 flex flex-wrap items-center justify-between gap-3 animate-in slide-in-from-top-2">
          <div className="flex items-center gap-2">
            <Badge className="bg-primary text-primary-foreground text-xs font-bold rounded-lg px-2.5 py-1">
              {selectedIds.size} Selected
            </Badge>
            <span className="text-xs text-muted-foreground hidden sm:inline">
              Apply bulk action to chosen submissions:
            </span>
          </div>

          <div className="flex items-center gap-2">
            <Button
              size="sm"
              onClick={() => handleBatchModerate("approve")}
              disabled={isBatchProcessing}
              className="gap-1.5 h-8.5 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white font-medium text-xs shadow-xs"
            >
              <Check className="h-3.5 w-3.5" /> Approve Selected
            </Button>
            <Button
              size="sm"
              variant="outline"
              onClick={() => handleBatchModerate("reject")}
              disabled={isBatchProcessing}
              className="gap-1.5 h-8.5 rounded-xl border-rose-500/30 text-rose-600 dark:text-rose-400 hover:bg-rose-500/10 font-medium text-xs"
            >
              <X className="h-3.5 w-3.5" /> Reject Selected
            </Button>
            <Button
              size="sm"
              variant="destructive"
              onClick={handleBatchDelete}
              disabled={isBatchProcessing}
              className="gap-1.5 h-8.5 rounded-xl font-medium text-xs shadow-xs"
            >
              <Trash2 className="h-3.5 w-3.5" /> Delete
            </Button>
            <Button
              size="sm"
              variant="ghost"
              onClick={() => setSelectedIds(new Set())}
              className="h-8.5 text-xs text-muted-foreground hover:text-foreground rounded-xl"
            >
              Cancel
            </Button>
          </div>
        </div>
      )}

      {/* Content Display: Empty State */}
      {filteredItems.length === 0 ? (
        <div className="border border-dashed border-border/80 rounded-3xl py-24 text-center bg-card/40 space-y-3">
          <div className="h-16 w-16 mx-auto rounded-2xl bg-muted/60 border border-border/60 flex items-center justify-center text-muted-foreground/60">
            <Images className="h-8 w-8" />
          </div>
          <div className="space-y-1">
            <h3 className="text-base font-bold text-foreground">No gallery submissions found</h3>
            <p className="text-xs text-muted-foreground max-w-sm mx-auto">
              {searchQuery
                ? `No matching media entries for query "${searchQuery}". Try clearing search filters.`
                : `There are currently no items under status "${statusFilter}".`}
            </p>
          </div>
          {(searchQuery || statusFilter !== "all" || mediaTypeFilter !== "all") && (
            <Button
              variant="outline"
              size="sm"
              onClick={() => {
                setSearchQuery("");
                setStatusFilter("all");
                setMediaTypeFilter("all");
              }}
              className="rounded-xl text-xs h-8.5"
            >
              Clear all filters
            </Button>
          )}
        </div>
      ) : viewMode === "grid" ? (
        /* Grid View Mode */
        <div className="grid gap-4.5 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
          {filteredItems.map((g) => {
            const isSelected = selectedIds.has(g.id);
            const isImg = g.type === "image" || /\.(jpg|jpeg|png|gif|webp)$/i.test(g.url);
            const config = STATUS_CONFIG[g.status] || STATUS_CONFIG.pending;
            const StatusIcon = config.icon;

            return (
              <div
                key={g.id}
                className={`group rounded-2xl border transition-all flex flex-col bg-card overflow-hidden relative ${
                  isSelected
                    ? "border-primary ring-2 ring-primary/20 shadow-md"
                    : "border-border/60 hover:border-border/90 hover:shadow-md"
                }`}
              >
                {/* Select Checkbox Top Left */}
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    toggleSelectItem(g.id);
                  }}
                  title={isSelected ? "Deselect item" : "Select item"}
                  className={`absolute top-3 left-3 z-10 h-7 w-7 rounded-xl border flex items-center justify-center backdrop-blur-md transition-all ${
                    isSelected
                      ? "bg-primary border-primary text-primary-foreground shadow-xs"
                      : "bg-black/40 border-white/20 text-white hover:bg-black/60 opacity-80 group-hover:opacity-100"
                  }`}
                >
                  {isSelected ? <Check className="h-4 w-4 stroke-[3]" /> : <span className="text-[10px] font-mono">#{g.id}</span>}
                </button>

                {/* Media Format Badge Top Right */}
                <div className="absolute top-3 right-3 z-10 flex items-center gap-1.5">
                  <Badge
                    variant="outline"
                    className="bg-black/50 backdrop-blur-md text-white border-white/20 text-[10px] font-medium py-0.5 px-2 rounded-lg gap-1"
                  >
                    {isImg ? <Camera className="h-3 w-3" /> : <Film className="h-3 w-3" />}
                    {isImg ? "Photo" : "Video"}
                  </Badge>
                </div>

                {/* Media Thumbnail Container */}
                <div
                  onClick={() => setInspectItem(g)}
                  className="aspect-video bg-muted/40 relative cursor-pointer overflow-hidden flex items-center justify-center group/thumb"
                >
                  {isImg ? (
                    // eslint-disable-next-line @next/next/no-img-element
                    <img
                      src={g.url}
                      alt={g.caption || `Gallery item #${g.id}`}
                      className="h-full w-full object-cover transition-transform duration-500 group-hover/thumb:scale-105"
                      onError={(e) => {
                        (e.target as HTMLElement).style.display = "none";
                      }}
                    />
                  ) : (
                    <div className="h-full w-full bg-slate-950 flex flex-col items-center justify-center text-slate-400 p-4 relative">
                      <video src={g.url} className="h-full w-full object-cover opacity-60" preload="metadata" />
                      <div className="absolute inset-0 flex items-center justify-center bg-black/30">
                        <div className="h-10 w-10 rounded-full bg-white/20 backdrop-blur-sm border border-white/30 flex items-center justify-center text-white">
                          <Film className="h-5 w-5" />
                        </div>
                      </div>
                    </div>
                  )}

                  {/* Quick Lightbox Open Hover Overlay */}
                  <div className="absolute inset-0 bg-black/40 opacity-0 group-hover/thumb:opacity-100 transition-opacity flex items-center justify-center gap-2">
                    <span className="px-3 py-1.5 rounded-xl bg-white/90 dark:bg-black/90 backdrop-blur-md text-foreground text-xs font-semibold flex items-center gap-1.5 shadow-md">
                      <Maximize2 className="h-3.5 w-3.5" /> Inspect Preview
                    </span>
                  </div>
                </div>

                {/* Card Content & Details */}
                <div className="p-4 space-y-3 flex-1 flex flex-col justify-between">
                  <div className="space-y-2">
                    <div className="flex items-center justify-between gap-2">
                      <Badge
                        variant="outline"
                        className={`text-[9px] font-bold uppercase tracking-wider py-0.5 px-2 rounded-lg border gap-1 flex items-center ${config.badgeClass}`}
                      >
                        <StatusIcon className="h-2.5 w-2.5" />
                        {config.label}
                      </Badge>
                      <span className="text-[11px] text-muted-foreground flex items-center gap-1 font-mono">
                        {g.created_at ? new Date(g.created_at).toLocaleDateString() : `ID: ${g.id}`}
                      </span>
                    </div>

                    <p
                      className="text-xs font-medium text-foreground line-clamp-2 leading-relaxed"
                      title={g.caption || "No caption provided"}
                    >
                      {g.caption ? g.caption : <span className="italic text-muted-foreground">No caption provided</span>}
                    </p>
                  </div>

                  {/* Micro-Actions Toolbar */}
                  <div className="pt-2 border-t border-border/50 flex flex-col gap-2">
                    <div className="flex gap-1.5">
                      {g.status !== "approved" && (
                        <Button
                          size="sm"
                          disabled={actingId === g.id}
                          onClick={() => moderate(g.id, "approve")}
                          className="h-8 flex-1 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white font-medium text-xs gap-1 shadow-xs"
                        >
                          <Check className="h-3.5 w-3.5" /> Approve
                        </Button>
                      )}
                      {g.status !== "rejected" && (
                        <Button
                          size="sm"
                          variant="outline"
                          disabled={actingId === g.id}
                          onClick={() => moderate(g.id, "reject")}
                          className="h-8 flex-1 rounded-xl border-rose-500/30 text-rose-600 dark:text-rose-400 hover:bg-rose-500/10 font-medium text-xs gap-1"
                        >
                          <X className="h-3.5 w-3.5" /> Reject
                        </Button>
                      )}
                      <Button
                        size="sm"
                        variant="ghost"
                        title="Delete media"
                        disabled={actingId === g.id}
                        onClick={() => setItemToDelete(g)}
                        className="h-8 w-8 p-0 rounded-xl text-muted-foreground hover:text-destructive hover:bg-destructive/10"
                      >
                        <Trash2 className="h-3.5 w-3.5" />
                      </Button>
                    </div>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      ) : (
        /* Table View Mode */
        <div className="rounded-2xl border border-border/70 bg-card overflow-hidden shadow-xs">
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-muted/50 border-b border-border/60 text-muted-foreground font-semibold uppercase tracking-wider text-[10px]">
                <tr>
                  <th className="p-3.5 w-10 text-center">
                    <input
                      type="checkbox"
                      checked={isAllSelected}
                      onChange={toggleSelectAll}
                      className="rounded border-border text-primary focus:ring-primary cursor-pointer"
                      aria-label="Select all entries"
                    />
                  </th>
                  <th className="p-3.5 w-24">Media</th>
                  <th className="p-3.5">Caption & URL</th>
                  <th className="p-3.5 w-28">Type</th>
                  <th className="p-3.5 w-36">Status</th>
                  <th className="p-3.5 w-32">Date</th>
                  <th className="p-3.5 w-44 text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-border/40">
                {filteredItems.map((g) => {
                  const isSelected = selectedIds.has(g.id);
                  const isImg = g.type === "image" || /\.(jpg|jpeg|png|gif|webp)$/i.test(g.url);
                  const config = STATUS_CONFIG[g.status] || STATUS_CONFIG.pending;
                  const StatusIcon = config.icon;

                  return (
                    <tr
                      key={g.id}
                      className={`hover:bg-muted/30 transition-colors ${
                        isSelected ? "bg-primary/5" : ""
                      }`}
                    >
                      <td className="p-3.5 text-center">
                        <input
                          type="checkbox"
                          checked={isSelected}
                          onChange={() => toggleSelectItem(g.id)}
                          className="rounded border-border text-primary focus:ring-primary cursor-pointer"
                          aria-label={`Select item ${g.id}`}
                        />
                      </td>
                      <td className="p-3.5">
                        <button
                          onClick={() => setInspectItem(g)}
                          className="h-12 w-16 rounded-lg bg-muted/60 overflow-hidden relative border border-border/60 block hover:opacity-80 transition-opacity"
                        >
                          {isImg ? (
                            // eslint-disable-next-line @next/next/no-img-element
                            <img src={g.url} alt="" className="h-full w-full object-cover" />
                          ) : (
                            <div className="h-full w-full bg-slate-900 flex items-center justify-center text-white">
                              <Film className="h-4 w-4" />
                            </div>
                          )}
                        </button>
                      </td>
                      <td className="p-3.5 max-w-xs">
                        <div className="font-medium text-foreground truncate">
                          {g.caption || <span className="italic text-muted-foreground">No caption</span>}
                        </div>
                        <div className="text-[10px] text-muted-foreground truncate font-mono mt-0.5 max-w-[280px]">
                          {g.url}
                        </div>
                      </td>
                      <td className="p-3.5">
                        <Badge variant="outline" className="text-[10px] py-0 px-2 rounded-md font-medium capitalize">
                          {isImg ? "Photo" : "Video"}
                        </Badge>
                      </td>
                      <td className="p-3.5">
                        <Badge
                          variant="outline"
                          className={`text-[9px] font-bold uppercase tracking-wider py-0.5 px-2 rounded-lg border gap-1 inline-flex items-center ${config.badgeClass}`}
                        >
                          <StatusIcon className="h-2.5 w-2.5" />
                          {config.label}
                        </Badge>
                      </td>
                      <td className="p-3.5 text-muted-foreground text-[11px] font-mono">
                        {g.created_at ? new Date(g.created_at).toLocaleDateString() : "—"}
                      </td>
                      <td className="p-3.5 text-right space-x-1">
                        <Button
                          size="sm"
                          variant="ghost"
                          onClick={() => setInspectItem(g)}
                          className="h-8 px-2 rounded-lg text-muted-foreground hover:text-foreground text-xs"
                          title="Inspect item"
                        >
                          <Maximize2 className="h-3.5 w-3.5" />
                        </Button>
                        {g.status !== "approved" && (
                          <Button
                            size="sm"
                            onClick={() => moderate(g.id, "approve")}
                            disabled={actingId === g.id}
                            className="h-8 px-2.5 rounded-lg bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-medium"
                            title="Approve"
                          >
                            <Check className="h-3.5 w-3.5" />
                          </Button>
                        )}
                        {g.status !== "rejected" && (
                          <Button
                            size="sm"
                            variant="outline"
                            onClick={() => moderate(g.id, "reject")}
                            disabled={actingId === g.id}
                            className="h-8 px-2.5 rounded-lg border-rose-500/30 text-rose-600 dark:text-rose-400 hover:bg-rose-500/10 text-xs font-medium"
                            title="Reject"
                          >
                            <X className="h-3.5 w-3.5" />
                          </Button>
                        )}
                        <Button
                          size="sm"
                          variant="ghost"
                          onClick={() => setItemToDelete(g)}
                          disabled={actingId === g.id}
                          className="h-8 px-2 rounded-lg text-muted-foreground hover:text-destructive hover:bg-destructive/10 text-xs"
                          title="Delete"
                        >
                          <Trash2 className="h-3.5 w-3.5" />
                        </Button>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Lightbox / Full-Screen Inspection Modal */}
      {inspectItem && (
        <Dialog open={!!inspectItem} onOpenChange={(open) => !open && setInspectItem(null)}>
          <DialogContent className="max-w-4xl p-0 overflow-hidden rounded-3xl bg-card border border-border/80 shadow-2xl">
            <div className="flex flex-col lg:flex-row max-h-[85vh]">
              {/* Media Preview Viewport */}
              <div className="lg:w-3/5 bg-black/95 relative flex items-center justify-center min-h-[320px] lg:min-h-[460px] p-2">
                {inspectItem.type === "image" || /\.(jpg|jpeg|png|gif|webp)$/i.test(inspectItem.url) ? (
                  // eslint-disable-next-line @next/next/no-img-element
                  <img
                    src={inspectItem.url}
                    alt={inspectItem.caption || "Gallery Preview"}
                    className="max-h-[70vh] w-auto max-w-full object-contain rounded-lg"
                  />
                ) : (
                  <video
                    src={inspectItem.url}
                    controls
                    autoPlay
                    className="max-h-[70vh] w-full object-contain rounded-lg"
                  />
                )}

                {/* Navigation Arrows */}
                <div className="absolute inset-x-3 top-1/2 -translate-y-1/2 flex justify-between pointer-events-none">
                  <Button
                    size="sm"
                    variant="outline"
                    onClick={handlePrevInspect}
                    className="h-9 w-9 p-0 rounded-full bg-black/60 hover:bg-black text-white border-white/20 pointer-events-auto shadow-md"
                  >
                    <ChevronLeft className="h-4 w-4" />
                  </Button>
                  <Button
                    size="sm"
                    variant="outline"
                    onClick={handleNextInspect}
                    className="h-9 w-9 p-0 rounded-full bg-black/60 hover:bg-black text-white border-white/20 pointer-events-auto shadow-md"
                  >
                    <ChevronRight className="h-4 w-4" />
                  </Button>
                </div>
              </div>

              {/* Sidebar Inspection Info */}
              <div className="lg:w-2/5 p-6 flex flex-col justify-between overflow-y-auto space-y-6">
                <div className="space-y-5">
                  <div className="flex items-center justify-between gap-2 border-b border-border/60 pb-4">
                    <div className="space-y-1">
                      <span className="text-[10px] font-mono text-muted-foreground uppercase tracking-wider">
                        Submission ID #{inspectItem.id}
                      </span>
                      <h3 className="text-lg font-bold text-foreground leading-tight">
                        Media Inspection
                      </h3>
                    </div>
                    {STATUS_CONFIG[inspectItem.status] && (
                      <Badge
                        variant="outline"
                        className={`text-[9px] font-bold uppercase tracking-wider py-0.5 px-2 rounded-lg border gap-1 ${
                          STATUS_CONFIG[inspectItem.status].badgeClass
                        }`}
                      >
                        {STATUS_CONFIG[inspectItem.status].label}
                      </Badge>
                    )}
                  </div>

                  {/* Caption */}
                  <div className="space-y-1.5">
                    <label className="text-[11px] font-semibold text-muted-foreground uppercase tracking-wider">
                      Caption / Description
                    </label>
                    <p className="text-sm text-foreground bg-muted/30 p-3 rounded-xl border border-border/50 leading-relaxed">
                      {inspectItem.caption || <span className="italic text-muted-foreground">No description provided.</span>}
                    </p>
                  </div>

                  {/* Direct Media Link */}
                  <div className="space-y-1.5">
                    <label className="text-[11px] font-semibold text-muted-foreground uppercase tracking-wider">
                      Direct Media Link
                    </label>
                    <div className="flex items-center gap-1.5">
                      <Input
                        readOnly
                        value={inspectItem.url}
                        className="h-8.5 text-xs font-mono bg-muted/40 rounded-xl"
                      />
                      <Button
                        size="sm"
                        variant="outline"
                        onClick={() => handleCopyLink(inspectItem.url)}
                        className="h-8.5 px-2.5 rounded-xl text-xs gap-1 shrink-0"
                        title="Copy direct link"
                      >
                        {copiedUrl ? <Check className="h-3.5 w-3.5 text-emerald-500" /> : <Copy className="h-3.5 w-3.5" />}
                      </Button>
                      <a
                        href={inspectItem.url}
                        target="_blank"
                        rel="noreferrer"
                        className="inline-flex items-center justify-center h-8.5 px-2.5 rounded-xl border border-border bg-background hover:bg-muted text-xs shrink-0"
                        title="Open in new tab"
                      >
                        <ExternalLink className="h-3.5 w-3.5" />
                      </a>
                    </div>
                  </div>

                  {/* Date & Attributes */}
                  <div className="grid grid-cols-2 gap-3 text-xs bg-muted/20 p-3 rounded-xl border border-border/40">
                    <div>
                      <span className="text-muted-foreground text-[10px] block">Uploaded Date</span>
                      <span className="font-semibold text-foreground">
                        {inspectItem.created_at ? new Date(inspectItem.created_at).toLocaleString() : "Unknown"}
                      </span>
                    </div>
                    <div>
                      <span className="text-muted-foreground text-[10px] block">Format</span>
                      <span className="font-semibold text-foreground capitalize">
                        {inspectItem.type || "Media file"}
                      </span>
                    </div>
                  </div>
                </div>

                {/* Moderation Controls in Modal */}
                <div className="pt-4 border-t border-border/60 space-y-2">
                  <div className="flex gap-2">
                    <Button
                      onClick={() => moderate(inspectItem.id, "approve")}
                      disabled={actingId === inspectItem.id || inspectItem.status === "approved"}
                      className="flex-1 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-semibold gap-1.5 h-9 shadow-xs"
                    >
                      <Check className="h-4 w-4" /> Approve Item
                    </Button>
                    <Button
                      variant="outline"
                      onClick={() => moderate(inspectItem.id, "reject")}
                      disabled={actingId === inspectItem.id || inspectItem.status === "rejected"}
                      className="flex-1 rounded-xl border-rose-500/30 text-rose-600 dark:text-rose-400 hover:bg-rose-500/10 text-xs font-semibold gap-1.5 h-9"
                    >
                      <X className="h-4 w-4" /> Reject Item
                    </Button>
                  </div>

                  <Button
                    variant="ghost"
                    onClick={() => {
                      setItemToDelete(inspectItem);
                    }}
                    className="w-full text-xs text-muted-foreground hover:text-destructive hover:bg-destructive/10 rounded-xl h-8 gap-1.5"
                  >
                    <Trash2 className="h-3.5 w-3.5" /> Delete from database
                  </Button>
                </div>
              </div>
            </div>
          </DialogContent>
        </Dialog>
      )}

      {/* Delete Confirmation Safe Modal */}
      {itemToDelete && (
        <Dialog open={!!itemToDelete} onOpenChange={(open) => !open && setItemToDelete(null)}>
          <DialogContent className="max-w-md p-6 rounded-3xl bg-card border border-border/80 shadow-2xl">
            <DialogHeader className="space-y-2">
              <div className="h-12 w-12 rounded-2xl bg-destructive/10 border border-destructive/20 text-destructive flex items-center justify-center mb-1">
                <Trash2 className="h-6 w-6" />
              </div>
              <DialogTitle className="text-lg font-bold text-foreground">
                Delete Gallery Item #{itemToDelete.id}?
              </DialogTitle>
              <DialogDescription className="text-xs text-muted-foreground leading-relaxed">
                This action is permanent and will completely remove the media item and caption from the database. This cannot be undone.
              </DialogDescription>
            </DialogHeader>

            <div className="flex gap-2.5 pt-4">
              <Button
                variant="outline"
                onClick={() => setItemToDelete(null)}
                className="flex-1 rounded-xl text-xs h-9"
              >
                Cancel
              </Button>
              <Button
                variant="destructive"
                onClick={() => remove(itemToDelete.id)}
                disabled={actingId === itemToDelete.id}
                className="flex-1 rounded-xl text-xs font-semibold h-9 gap-1.5"
              >
                {actingId === itemToDelete.id ? <Loader2 className="h-4 w-4 animate-spin" /> : <Trash2 className="h-4 w-4" />}
                Confirm Delete
              </Button>
            </div>
          </DialogContent>
        </Dialog>
      )}
    </div>
  );
}

