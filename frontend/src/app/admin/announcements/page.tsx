"use client";

import { useEffect, useState, useMemo, useCallback } from "react";
import { useAuth } from "@/lib/auth";
import { fetchAPI } from "@/lib/api";
import { useRouter } from "next/navigation";
import {
  Loader2,
  Megaphone,
  Plus,
  Pencil,
  Trash2,
  Check,
  X,
  Search,
  LayoutGrid,
  List,
  RefreshCw,
  Copy,
  Clock,
  CheckCircle2,
  XCircle,
  AlertCircle,
  Building2,
  Eye,
  FileText,
  Calendar,
  User as UserIcon,
  Sparkles,
} from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogDescription,
} from "@/components/ui/dialog";

interface Announcement {
  id: number;
  title: string;
  content: string;
  status: string;
  barangay_id?: number | null;
  barangay_name?: string | null;
  author_name?: string;
  created_at?: string | null;
}

interface BarangayOption {
  id: number;
  name: string;
}

type StatusFilter = "all" | "published" | "pending" | "approved" | "rejected";
type ScopeFilter = "all" | "lgu" | "barangay";
type SortOption = "newest" | "oldest" | "title-asc" | "title-desc";

const STATUS_CONFIG: Record<
  string,
  { label: string; badgeClass: string; icon: typeof CheckCircle2 }
> = {
  published: {
    label: "Published",
    badgeClass: "bg-emerald-500/10 text-emerald-600 border-emerald-500/20 dark:text-emerald-400 dark:border-emerald-500/30",
    icon: CheckCircle2,
  },
  approved: {
    label: "Approved",
    badgeClass: "bg-sky-500/10 text-sky-600 border-sky-500/20 dark:text-sky-400 dark:border-sky-500/30",
    icon: CheckCircle2,
  },
  pending: {
    label: "Pending Review",
    badgeClass: "bg-amber-500/10 text-amber-600 border-amber-500/20 dark:text-amber-400 dark:border-amber-500/30",
    icon: Clock,
  },
  rejected: {
    label: "Rejected",
    badgeClass: "bg-rose-500/10 text-rose-600 border-rose-500/20 dark:text-rose-400 dark:border-rose-500/30",
    icon: XCircle,
  },
};

const EMPTY_FORM = { title: "", content: "", barangay_id: "" };

export default function AdminAnnouncementsPage() {
  const { user, loading: authLoading } = useAuth();
  const router = useRouter();

  const [items, setItems] = useState<Announcement[]>([]);
  const [barangays, setBarangays] = useState<BarangayOption[]>([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [successMsg, setSuccessMsg] = useState<string | null>(null);

  // Filters, Search & Layout View
  const [statusFilter, setStatusFilter] = useState<StatusFilter>("all");
  const [scopeFilter, setScopeFilter] = useState<ScopeFilter>("all");
  const [selectedBarangayId, setSelectedBarangayId] = useState<string>("all");
  const [searchQuery, setSearchQuery] = useState("");
  const [sortBy, setSortBy] = useState<SortOption>("newest");
  const [viewMode, setViewMode] = useState<"grid" | "table">("grid");

  // Selection & Batch Actions
  const [selectedIds, setSelectedIds] = useState<Set<number>>(new Set());
  const [isBatchDeleting, setIsBatchDeleting] = useState(false);

  // Modals & States
  const [dialogOpen, setDialogOpen] = useState(false);
  const [editing, setEditing] = useState<Announcement | null>(null);
  const [form, setForm] = useState(EMPTY_FORM);
  const [saving, setSaving] = useState(false);

  const [previewItem, setPreviewItem] = useState<Announcement | null>(null);
  const [itemToDelete, setItemToDelete] = useState<Announcement | null>(null);
  const [actingId, setActingId] = useState<number | null>(null);
  const [copiedId, setCopiedId] = useState<number | null>(null);

  const load = useCallback(async (isRefresh = false) => {
    if (isRefresh) setRefreshing(true);
    else setLoading(true);
    setError(null);
    try {
      const [annData, bData] = await Promise.all([
        fetchAPI<{ announcements: Announcement[] }>("/api/admin/announcements"),
        fetchAPI<{ barangays: BarangayOption[] }>("/api/admin/barangays"),
      ]);
      setItems(annData.announcements || []);
      setBarangays(bData.barangays || []);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load announcements.");
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

  // Flash message timer
  useEffect(() => {
    if (successMsg) {
      const timer = setTimeout(() => setSuccessMsg(null), 3500);
      return () => clearTimeout(timer);
    }
  }, [successMsg]);

  // Analytics & Stats
  const stats = useMemo(() => {
    const total = items.length;
    const published = items.filter((a) => a.status === "published" || a.status === "approved").length;
    const pending = items.filter((a) => a.status === "pending").length;
    const barangayLevel = items.filter((a) => a.barangay_id !== null && a.barangay_id !== undefined).length;
    const lguLevel = total - barangayLevel;
    return { total, published, pending, barangayLevel, lguLevel };
  }, [items]);

  // Filtered and Sorted announcements
  const filteredItems = useMemo(() => {
    return items
      .filter((item) => {
        // Status filter
        if (statusFilter !== "all" && item.status !== statusFilter) return false;

        // Scope filter
        if (scopeFilter === "lgu" && item.barangay_id) return false;
        if (scopeFilter === "barangay" && !item.barangay_id) return false;

        // Specific Barangay filter
        if (selectedBarangayId !== "all" && String(item.barangay_id) !== selectedBarangayId) {
          return false;
        }

        // Search query filter
        if (searchQuery.trim()) {
          const q = searchQuery.toLowerCase().trim();
          const matchTitle = item.title.toLowerCase().includes(q);
          const matchContent = item.content.toLowerCase().includes(q);
          const matchAuthor = item.author_name?.toLowerCase().includes(q);
          const matchBarangay = item.barangay_name?.toLowerCase().includes(q);
          const matchId = String(item.id).includes(q);
          if (!matchTitle && !matchContent && !matchAuthor && !matchBarangay && !matchId) {
            return false;
          }
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
        if (sortBy === "title-asc") {
          return a.title.localeCompare(b.title);
        }
        if (sortBy === "title-desc") {
          return b.title.localeCompare(a.title);
        }
        return 0;
      });
  }, [items, statusFilter, scopeFilter, selectedBarangayId, searchQuery, sortBy]);

  // Selection handlers
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

  // Dialog Handlers
  const openCreate = () => {
    setEditing(null);
    setForm(EMPTY_FORM);
    setDialogOpen(true);
  };

  const openEdit = (a: Announcement) => {
    setEditing(a);
    setForm({
      title: a.title,
      content: a.content,
      barangay_id: a.barangay_id ? String(a.barangay_id) : "",
    });
    setDialogOpen(true);
  };

  const save = async () => {
    if (!form.title.trim() || !form.content.trim()) return;
    setSaving(true);
    try {
      const body = JSON.stringify({
        title: form.title.trim(),
        content: form.content.trim(),
        barangay_id: form.barangay_id ? Number(form.barangay_id) : null,
      });

      if (editing) {
        await fetchAPI(`/api/admin/announcements/${editing.id}`, { method: "PUT", body });
        setSuccessMsg(`Announcement "${form.title.trim()}" updated successfully.`);
      } else {
        await fetchAPI("/api/admin/announcements", { method: "POST", body });
        setSuccessMsg(`Announcement "${form.title.trim()}" published successfully.`);
      }

      setDialogOpen(false);
      await load();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to save announcement.");
    } finally {
      setSaving(false);
    }
  };

  const executeDelete = async (id: number) => {
    setActingId(id);
    try {
      await fetchAPI(`/api/admin/announcements/${id}`, { method: "DELETE" });
      setItems((prev) => prev.filter((a) => a.id !== id));
      setSelectedIds((prev) => {
        const next = new Set(prev);
        next.delete(id);
        return next;
      });
      if (previewItem?.id === id) setPreviewItem(null);
      setItemToDelete(null);
      setSuccessMsg("Announcement removed successfully.");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to delete announcement.");
    } finally {
      setActingId(null);
    }
  };

  const handleBatchDelete = async () => {
    if (selectedIds.size === 0) return;
    setIsBatchDeleting(true);
    const ids = Array.from(selectedIds);
    try {
      await Promise.all(
        ids.map((id) => fetchAPI(`/api/admin/announcements/${id}`, { method: "DELETE" }))
      );
      setItems((prev) => prev.filter((a) => !selectedIds.has(a.id)));
      setSuccessMsg(`Successfully deleted ${ids.length} announcement(s).`);
      setSelectedIds(new Set());
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to batch delete announcements.");
    } finally {
      setIsBatchDeleting(false);
    }
  };

  const copyToClipboard = (a: Announcement) => {
    const text = `${a.title}\n\n${a.content}\n\n— ${a.barangay_name ? `${a.barangay_name}, ` : ""}LGU Mangatarem`;
    navigator.clipboard.writeText(text);
    setCopiedId(a.id);
    setSuccessMsg("Announcement copied to clipboard!");
    setTimeout(() => setCopiedId(null), 2000);
  };

  if (authLoading || !user || loading) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[60vh] gap-3">
        <Loader2 className="h-8 w-8 animate-spin text-primary" />
        <p className="text-sm font-medium text-muted-foreground animate-pulse">
          Loading announcements and bulletins...
        </p>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8 max-w-7xl space-y-8">
      {/* ── Header Section ── */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-border/60 pb-6">
        <div className="flex items-start gap-3.5">
          <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-primary/10 text-primary border border-primary/20 shadow-xs">
            <Megaphone className="h-6 w-6" />
          </div>
          <div>
            <div className="flex items-center gap-2.5">
              <h1 className="text-2xl sm:text-3xl font-bold tracking-tight text-foreground">
                Announcements Management
              </h1>
              <Badge variant="outline" className="text-xs font-semibold px-2 py-0.5 border-primary/20 bg-primary/5 text-primary">
                {items.length} Total
              </Badge>
            </div>
            <p className="text-muted-foreground text-sm mt-1">
              Publish official bulletins, municipal updates, and community alerts across Mangatarem
            </p>
          </div>
        </div>

        <div className="flex items-center gap-2.5 self-start md:self-auto">
          <Button
            variant="outline"
            size="sm"
            onClick={() => load(true)}
            disabled={refreshing}
            className="h-10 px-3 gap-2 rounded-xl cursor-pointer hover:bg-muted/80 transition-colors"
          >
            <RefreshCw className={`h-4 w-4 ${refreshing ? "animate-spin text-primary" : ""}`} />
            <span className="hidden sm:inline">Refresh</span>
          </Button>
          <Button
            onClick={openCreate}
            size="sm"
            className="h-10 px-4 gap-2 rounded-xl bg-primary text-primary-foreground hover:bg-primary/90 shadow-sm cursor-pointer transition-all duration-200"
          >
            <Plus className="h-4 w-4" />
            <span>New Announcement</span>
          </Button>
        </div>
      </div>

      {/* ── Status Toast / Alerts ── */}
      {error && (
        <div className="flex items-center justify-between p-4 rounded-xl bg-destructive/10 border border-destructive/20 text-destructive text-sm animate-in fade-in slide-in-from-top-2 duration-200">
          <div className="flex items-center gap-2.5">
            <AlertCircle className="h-4 w-4 shrink-0" />
            <span className="font-medium">{error}</span>
          </div>
          <Button
            variant="ghost"
            size="sm"
            onClick={() => setError(null)}
            className="h-7 w-7 p-0 text-destructive hover:bg-destructive/10 rounded-lg cursor-pointer"
          >
            <X className="h-4 w-4" />
          </Button>
        </div>
      )}

      {successMsg && (
        <div className="flex items-center justify-between p-4 rounded-xl bg-emerald-500/10 border border-emerald-500/20 text-emerald-600 dark:text-emerald-400 text-sm animate-in fade-in slide-in-from-top-2 duration-200">
          <div className="flex items-center gap-2.5">
            <CheckCircle2 className="h-4 w-4 shrink-0" />
            <span className="font-medium">{successMsg}</span>
          </div>
          <Button
            variant="ghost"
            size="sm"
            onClick={() => setSuccessMsg(null)}
            className="h-7 w-7 p-0 text-emerald-600 dark:text-emerald-400 hover:bg-emerald-500/10 rounded-lg cursor-pointer"
          >
            <X className="h-4 w-4" />
          </Button>
        </div>
      )}

      {/* ── KPI Stat Cards ── */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="p-5 rounded-2xl bg-card border border-border/80 shadow-xs hover:border-primary/30 transition-colors">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">
              Total Bulletins
            </span>
            <div className="p-2 rounded-xl bg-muted text-foreground">
              <FileText className="h-4 w-4" />
            </div>
          </div>
          <p className="text-2xl font-bold text-foreground mt-2">{stats.total}</p>
          <p className="text-xs text-muted-foreground mt-1">All recorded announcements</p>
        </div>

        <div className="p-5 rounded-2xl bg-card border border-border/80 shadow-xs hover:border-emerald-500/30 transition-colors">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold uppercase tracking-wider text-emerald-600 dark:text-emerald-400">
              Published & Live
            </span>
            <div className="p-2 rounded-xl bg-emerald-500/10 text-emerald-600 dark:text-emerald-400">
              <CheckCircle2 className="h-4 w-4" />
            </div>
          </div>
          <p className="text-2xl font-bold text-foreground mt-2">{stats.published}</p>
          <p className="text-xs text-muted-foreground mt-1">Active on public portal</p>
        </div>

        <div className="p-5 rounded-2xl bg-card border border-border/80 shadow-xs hover:border-sky-500/30 transition-colors">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold uppercase tracking-wider text-sky-600 dark:text-sky-400">
              Barangay Focused
            </span>
            <div className="p-2 rounded-xl bg-sky-500/10 text-sky-600 dark:text-sky-400">
              <Building2 className="h-4 w-4" />
            </div>
          </div>
          <p className="text-2xl font-bold text-foreground mt-2">{stats.barangayLevel}</p>
          <p className="text-xs text-muted-foreground mt-1">Targeted to specific barangays</p>
        </div>

        <div className="p-5 rounded-2xl bg-card border border-border/80 shadow-xs hover:border-amber-500/30 transition-colors">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold uppercase tracking-wider text-amber-600 dark:text-amber-400">
              Municipal / LGU-Wide
            </span>
            <div className="p-2 rounded-xl bg-amber-500/10 text-amber-600 dark:text-amber-400">
              <Sparkles className="h-4 w-4" />
            </div>
          </div>
          <p className="text-2xl font-bold text-foreground mt-2">{stats.lguLevel}</p>
          <p className="text-xs text-muted-foreground mt-1">Town-wide public advisories</p>
        </div>
      </div>

      {/* ── Search & Filter Controls ── */}
      <div className="space-y-4">
        <div className="flex flex-col md:flex-row items-stretch md:items-center justify-between gap-3">
          {/* Search bar */}
          <div className="relative flex-1">
            <Search className="absolute left-3.5 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
            <Input
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Search by title, keywords, author, or barangay..."
              className="pl-9.5 pr-8 h-10.5 rounded-xl border-border/80 bg-card text-sm focus-visible:ring-primary"
            />
            {searchQuery && (
              <button
                onClick={() => setSearchQuery("")}
                className="absolute right-3 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground cursor-pointer"
              >
                <X className="h-3.5 w-3.5" />
              </button>
            )}
          </div>

          {/* Barangay Dropdown Filter */}
          <div className="flex items-center gap-2">
            <select
              value={selectedBarangayId}
              onChange={(e) => setSelectedBarangayId(e.target.value)}
              className="h-10.5 px-3 rounded-xl border border-border/80 bg-card text-xs sm:text-sm text-foreground focus:outline-none focus:ring-2 focus:ring-primary/20 cursor-pointer"
            >
              <option value="all">All Locations (Municipal & All Barangays)</option>
              {barangays.map((b) => (
                <option key={b.id} value={String(b.id)}>
                  Barangay {b.name}
                </option>
              ))}
            </select>

            {/* Sort Dropdown */}
            <div className="relative">
              <select
                value={sortBy}
                onChange={(e) => setSortBy(e.target.value as SortOption)}
                className="h-10.5 px-3 rounded-xl border border-border/80 bg-card text-xs sm:text-sm text-foreground focus:outline-none focus:ring-2 focus:ring-primary/20 cursor-pointer"
              >
                <option value="newest">Newest First</option>
                <option value="oldest">Oldest First</option>
                <option value="title-asc">Title (A-Z)</option>
                <option value="title-desc">Title (Z-A)</option>
              </select>
            </div>

            {/* View Mode Toggle */}
            <div className="flex items-center p-1 rounded-xl bg-muted border border-border/60">
              <Button
                variant={viewMode === "grid" ? "secondary" : "ghost"}
                size="sm"
                onClick={() => setViewMode("grid")}
                className={`h-8 w-8 p-0 rounded-lg cursor-pointer transition-all ${
                  viewMode === "grid" ? "bg-card shadow-xs text-foreground" : "text-muted-foreground hover:text-foreground"
                }`}
                title="Grid View"
              >
                <LayoutGrid className="h-4 w-4" />
              </Button>
              <Button
                variant={viewMode === "table" ? "secondary" : "ghost"}
                size="sm"
                onClick={() => setViewMode("table")}
                className={`h-8 w-8 p-0 rounded-lg cursor-pointer transition-all ${
                  viewMode === "table" ? "bg-card shadow-xs text-foreground" : "text-muted-foreground hover:text-foreground"
                }`}
                title="Table View"
              >
                <List className="h-4 w-4" />
              </Button>
            </div>
          </div>
        </div>

        {/* Status & Scope Filter Tabs */}
        <div className="flex flex-wrap items-center justify-between gap-3 pt-1">
          <div className="flex flex-wrap items-center gap-1.5 p-1 rounded-xl bg-muted/60 border border-border/50">
            {(
              [
                { id: "all", label: "All Status", count: items.length },
                { id: "published", label: "Published", count: stats.published },
                { id: "pending", label: "Pending Review", count: stats.pending },
                { id: "rejected", label: "Rejected", count: items.filter((a) => a.status === "rejected").length },
              ] as const
            ).map((tab) => (
              <button
                key={tab.id}
                onClick={() => setStatusFilter(tab.id as StatusFilter)}
                className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold transition-all cursor-pointer ${
                  statusFilter === tab.id
                    ? "bg-card text-foreground shadow-xs border border-border/60"
                    : "text-muted-foreground hover:text-foreground"
                }`}
              >
                <span>{tab.label}</span>
                <span className="text-[10px] px-1.5 py-0.2 rounded-full bg-muted font-bold text-muted-foreground">
                  {tab.count}
                </span>
              </button>
            ))}
          </div>

          <div className="flex items-center gap-2">
            <span className="text-xs text-muted-foreground font-medium">
              Showing <strong className="text-foreground">{filteredItems.length}</strong> of{" "}
              {items.length} announcements
            </span>
          </div>
        </div>
      </div>

      {/* ── Multi-select Batch Action Bar ── */}
      {selectedIds.size > 0 && (
        <div className="flex items-center justify-between p-3.5 px-4 rounded-xl bg-primary/5 border border-primary/20 animate-in fade-in slide-in-from-top-1 duration-200">
          <div className="flex items-center gap-3">
            <input
              type="checkbox"
              checked={isAllSelected}
              onChange={toggleSelectAll}
              className="h-4 w-4 rounded border-border text-primary focus:ring-primary cursor-pointer"
            />
            <span className="text-xs sm:text-sm font-semibold text-foreground">
              {selectedIds.size} announcement{selectedIds.size > 1 ? "s" : ""} selected
            </span>
          </div>
          <div className="flex items-center gap-2">
            <Button
              variant="outline"
              size="sm"
              onClick={() => setSelectedIds(new Set())}
              className="h-8 text-xs rounded-lg cursor-pointer"
            >
              Deselect All
            </Button>
            <Button
              variant="destructive"
              size="sm"
              onClick={handleBatchDelete}
              disabled={isBatchDeleting}
              className="h-8 gap-1.5 text-xs rounded-lg cursor-pointer"
            >
              {isBatchDeleting ? <Loader2 className="h-3.5 w-3.5 animate-spin" /> : <Trash2 className="h-3.5 w-3.5" />}
              Delete Selected
            </Button>
          </div>
        </div>
      )}

      {/* ── Content View (Grid or Table) ── */}
      {filteredItems.length === 0 ? (
        <div className="border border-dashed border-border/80 rounded-2xl p-16 text-center bg-card/40">
          <div className="flex h-16 w-16 items-center justify-center rounded-2xl bg-muted/80 text-muted-foreground/60 mx-auto mb-4">
            <Megaphone className="h-8 w-8" />
          </div>
          <h3 className="text-lg font-bold text-foreground">No announcements found</h3>
          <p className="text-sm text-muted-foreground max-w-sm mx-auto mt-1 mb-5">
            {searchQuery || statusFilter !== "all" || selectedBarangayId !== "all"
              ? "No announcements match your current filter criteria. Try adjusting your search query or filters."
              : "Start by publishing your first public bulletin or advisory for Mangatarem."}
          </p>
          {searchQuery || statusFilter !== "all" || selectedBarangayId !== "all" ? (
            <Button
              variant="outline"
              size="sm"
              onClick={() => {
                setSearchQuery("");
                setStatusFilter("all");
                setSelectedBarangayId("all");
              }}
              className="rounded-xl cursor-pointer"
            >
              Reset Filters
            </Button>
          ) : (
            <Button onClick={openCreate} size="sm" className="rounded-xl gap-1.5 cursor-pointer">
              <Plus className="h-4 w-4" /> Create Announcement
            </Button>
          )}
        </div>
      ) : viewMode === "grid" ? (
        /* ── Grid View ── */
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
          {filteredItems.map((a) => {
            const isSelected = selectedIds.has(a.id);
            const statusMeta = STATUS_CONFIG[a.status] || STATUS_CONFIG.published;
            const StatusIcon = statusMeta.icon;

            return (
              <div
                key={a.id}
                className={`group relative flex flex-col justify-between rounded-2xl bg-card border transition-all duration-200 hover:shadow-md hover:border-primary/40 ${
                  isSelected ? "border-primary ring-2 ring-primary/20 bg-primary/[0.02]" : "border-border/80"
                }`}
              >
                <div className="p-5.5 space-y-3.5">
                  {/* Top Bar: Select checkbox, Scope Badge, Status Badge */}
                  <div className="flex items-center justify-between gap-2">
                    <div className="flex items-center gap-2">
                      <input
                        type="checkbox"
                        checked={isSelected}
                        onChange={() => toggleSelectItem(a.id)}
                        className="h-4 w-4 rounded border-border text-primary focus:ring-primary cursor-pointer"
                      />
                      {a.barangay_name ? (
                        <Badge
                          variant="outline"
                          className="text-[10px] font-bold uppercase tracking-wider bg-sky-500/10 text-sky-600 border-sky-500/20 dark:text-sky-400 gap-1 py-0.5"
                        >
                          <Building2 className="h-3 w-3" />
                          {a.barangay_name}
                        </Badge>
                      ) : (
                        <Badge
                          variant="outline"
                          className="text-[10px] font-bold uppercase tracking-wider bg-amber-500/10 text-amber-600 border-amber-500/20 dark:text-amber-400 gap-1 py-0.5"
                        >
                          <Sparkles className="h-3 w-3" />
                          LGU-Wide
                        </Badge>
                      )}
                    </div>

                    <Badge
                      variant="outline"
                      className={`text-[10px] font-bold uppercase tracking-wider gap-1 py-0.5 ${statusMeta.badgeClass}`}
                    >
                      <StatusIcon className="h-3 w-3" />
                      {statusMeta.label}
                    </Badge>
                  </div>

                  {/* Title & Excerpt */}
                  <div>
                    <h3
                      onClick={() => setPreviewItem(a)}
                      className="font-bold text-base text-foreground group-hover:text-primary transition-colors line-clamp-1 cursor-pointer"
                      title={a.title}
                    >
                      {a.title}
                    </h3>
                    <p className="text-xs sm:text-sm text-muted-foreground mt-2 line-clamp-3 leading-relaxed">
                      {a.content}
                    </p>
                  </div>

                  {/* Author & Timestamp */}
                  <div className="flex items-center justify-between text-[11px] text-muted-foreground pt-2 border-t border-border/50">
                    <div className="flex items-center gap-1.5">
                      <UserIcon className="h-3.5 w-3.5 text-muted-foreground/70" />
                      <span className="font-medium truncate max-w-[120px]">
                        {a.author_name || "LGU Mangatarem"}
                      </span>
                    </div>
                    <div className="flex items-center gap-1">
                      <Calendar className="h-3.5 w-3.5 text-muted-foreground/70" />
                      <span>{a.created_at ? new Date(a.created_at).toLocaleDateString() : "Recent"}</span>
                    </div>
                  </div>
                </div>

                {/* Card Action Footer */}
                <div className="flex items-center justify-between px-5.5 py-3 bg-muted/40 border-t border-border/50 rounded-b-2xl">
                  <Button
                    size="sm"
                    variant="ghost"
                    onClick={() => setPreviewItem(a)}
                    className="h-8 px-2.5 text-xs text-muted-foreground hover:text-foreground gap-1.5 rounded-lg cursor-pointer"
                  >
                    <Eye className="h-3.5 w-3.5" /> Preview
                  </Button>

                  <div className="flex items-center gap-1">
                    <Button
                      size="sm"
                      variant="ghost"
                      onClick={() => copyToClipboard(a)}
                      className="h-8 w-8 p-0 text-muted-foreground hover:text-foreground rounded-lg cursor-pointer"
                      title="Copy text"
                    >
                      {copiedId === a.id ? <Check className="h-3.5 w-3.5 text-emerald-500" /> : <Copy className="h-3.5 w-3.5" />}
                    </Button>
                    <Button
                      size="sm"
                      variant="ghost"
                      onClick={() => openEdit(a)}
                      className="h-8 w-8 p-0 text-muted-foreground hover:text-foreground rounded-lg cursor-pointer"
                      title="Edit"
                    >
                      <Pencil className="h-3.5 w-3.5" />
                    </Button>
                    <Button
                      size="sm"
                      variant="ghost"
                      onClick={() => setItemToDelete(a)}
                      className="h-8 w-8 p-0 text-destructive/80 hover:text-destructive hover:bg-destructive/10 rounded-lg cursor-pointer"
                      title="Delete"
                    >
                      <Trash2 className="h-3.5 w-3.5" />
                    </Button>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      ) : (
        /* ── Table View ── */
        <div className="rounded-2xl border border-border/80 bg-card overflow-hidden shadow-xs">
          <div className="overflow-x-auto">
            <table className="w-full text-left text-sm">
              <thead className="bg-muted/60 text-xs uppercase font-semibold text-muted-foreground border-b border-border/80">
                <tr>
                  <th className="p-4 w-10">
                    <input
                      type="checkbox"
                      checked={isAllSelected}
                      onChange={toggleSelectAll}
                      className="h-4 w-4 rounded border-border text-primary focus:ring-primary cursor-pointer"
                    />
                  </th>
                  <th className="p-4 font-semibold">Title & Details</th>
                  <th className="p-4 font-semibold">Scope / Location</th>
                  <th className="p-4 font-semibold">Status</th>
                  <th className="p-4 font-semibold">Author & Date</th>
                  <th className="p-4 text-right font-semibold">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-border/60">
                {filteredItems.map((a) => {
                  const isSelected = selectedIds.has(a.id);
                  const statusMeta = STATUS_CONFIG[a.status] || STATUS_CONFIG.published;
                  const StatusIcon = statusMeta.icon;

                  return (
                    <tr
                      key={a.id}
                      className={`hover:bg-muted/30 transition-colors ${
                        isSelected ? "bg-primary/[0.03]" : ""
                      }`}
                    >
                      <td className="p-4">
                        <input
                          type="checkbox"
                          checked={isSelected}
                          onChange={() => toggleSelectItem(a.id)}
                          className="h-4 w-4 rounded border-border text-primary focus:ring-primary cursor-pointer"
                        />
                      </td>
                      <td className="p-4 max-w-xs sm:max-w-md">
                        <div
                          onClick={() => setPreviewItem(a)}
                          className="font-bold text-foreground hover:text-primary cursor-pointer truncate"
                          title={a.title}
                        >
                          {a.title}
                        </div>
                        <p className="text-xs text-muted-foreground line-clamp-1 mt-0.5">
                          {a.content}
                        </p>
                      </td>
                      <td className="p-4 whitespace-nowrap">
                        {a.barangay_name ? (
                          <Badge
                            variant="outline"
                            className="text-[10px] font-bold uppercase tracking-wider bg-sky-500/10 text-sky-600 border-sky-500/20 dark:text-sky-400 gap-1 py-0.5"
                          >
                            <Building2 className="h-3 w-3" />
                            {a.barangay_name}
                          </Badge>
                        ) : (
                          <Badge
                            variant="outline"
                            className="text-[10px] font-bold uppercase tracking-wider bg-amber-500/10 text-amber-600 border-amber-500/20 dark:text-amber-400 gap-1 py-0.5"
                          >
                            <Sparkles className="h-3 w-3" />
                            LGU-Wide
                          </Badge>
                        )}
                      </td>
                      <td className="p-4 whitespace-nowrap">
                        <Badge
                          variant="outline"
                          className={`text-[10px] font-bold uppercase tracking-wider gap-1 py-0.5 ${statusMeta.badgeClass}`}
                        >
                          <StatusIcon className="h-3 w-3" />
                          {statusMeta.label}
                        </Badge>
                      </td>
                      <td className="p-4 whitespace-nowrap text-xs text-muted-foreground">
                        <div className="font-medium text-foreground">{a.author_name || "LGU Mangatarem"}</div>
                        <div className="text-[11px] mt-0.5">
                          {a.created_at ? new Date(a.created_at).toLocaleDateString() : "Recent"}
                        </div>
                      </td>
                      <td className="p-4 text-right whitespace-nowrap">
                        <div className="flex items-center justify-end gap-1">
                          <Button
                            size="sm"
                            variant="ghost"
                            onClick={() => setPreviewItem(a)}
                            className="h-8 w-8 p-0 text-muted-foreground hover:text-foreground rounded-lg cursor-pointer"
                            title="Preview"
                          >
                            <Eye className="h-4 w-4" />
                          </Button>
                          <Button
                            size="sm"
                            variant="ghost"
                            onClick={() => copyToClipboard(a)}
                            className="h-8 w-8 p-0 text-muted-foreground hover:text-foreground rounded-lg cursor-pointer"
                            title="Copy"
                          >
                            {copiedId === a.id ? <Check className="h-4 w-4 text-emerald-500" /> : <Copy className="h-4 w-4" />}
                          </Button>
                          <Button
                            size="sm"
                            variant="ghost"
                            onClick={() => openEdit(a)}
                            className="h-8 w-8 p-0 text-muted-foreground hover:text-foreground rounded-lg cursor-pointer"
                            title="Edit"
                          >
                            <Pencil className="h-4 w-4" />
                          </Button>
                          <Button
                            size="sm"
                            variant="ghost"
                            onClick={() => setItemToDelete(a)}
                            className="h-8 w-8 p-0 text-destructive hover:bg-destructive/10 rounded-lg cursor-pointer"
                            title="Delete"
                          >
                            <Trash2 className="h-4 w-4" />
                          </Button>
                        </div>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* ── Preview / Inspection Modal ── */}
      <Dialog open={!!previewItem} onOpenChange={(open) => !open && setPreviewItem(null)}>
        <DialogContent className="max-w-2xl rounded-2xl p-6">
          {previewItem && (
            <div className="space-y-5">
              <DialogHeader>
                <div className="flex flex-wrap items-center gap-2 mb-2">
                  {previewItem.barangay_name ? (
                    <Badge
                      variant="outline"
                      className="text-xs font-bold uppercase tracking-wider bg-sky-500/10 text-sky-600 border-sky-500/20 dark:text-sky-400 gap-1"
                    >
                      <Building2 className="h-3.5 w-3.5" />
                      {previewItem.barangay_name}
                    </Badge>
                  ) : (
                    <Badge
                      variant="outline"
                      className="text-xs font-bold uppercase tracking-wider bg-amber-500/10 text-amber-600 border-amber-500/20 dark:text-amber-400 gap-1"
                    >
                      <Sparkles className="h-3.5 w-3.5" />
                      LGU-Wide Public Advisory
                    </Badge>
                  )}
                  <Badge
                    variant="outline"
                    className={`text-xs font-bold uppercase tracking-wider ${
                      (STATUS_CONFIG[previewItem.status] || STATUS_CONFIG.published).badgeClass
                    }`}
                  >
                    {previewItem.status}
                  </Badge>
                </div>
                <DialogTitle className="text-xl sm:text-2xl font-bold text-foreground leading-snug">
                  {previewItem.title}
                </DialogTitle>
                <DialogDescription className="text-xs text-muted-foreground flex items-center gap-2 pt-1">
                  <span>Author: {previewItem.author_name || "LGU Mangatarem"}</span>
                  <span>•</span>
                  <span>
                    {previewItem.created_at
                      ? new Date(previewItem.created_at).toLocaleDateString(undefined, {
                          year: "numeric",
                          month: "long",
                          day: "numeric",
                        })
                      : "Recent"}
                  </span>
                </DialogDescription>
              </DialogHeader>

              {/* Body Text */}
              <div className="p-4.5 rounded-xl bg-muted/40 border border-border/60 max-h-[50vh] overflow-y-auto">
                <p className="text-sm sm:text-base text-foreground leading-relaxed whitespace-pre-wrap">
                  {previewItem.content}
                </p>
              </div>

              {/* Statistics & Metadata */}
              <div className="flex items-center justify-between text-xs text-muted-foreground px-1">
                <span>
                  {previewItem.content.split(/\s+/).filter(Boolean).length} words ·{" "}
                  {previewItem.content.length} characters
                </span>
                <button
                  onClick={() => copyToClipboard(previewItem)}
                  className="flex items-center gap-1.5 text-primary hover:underline cursor-pointer font-medium"
                >
                  <Copy className="h-3.5 w-3.5" /> Copy announcement text
                </button>
              </div>

              {/* Modal Actions */}
              <div className="flex items-center justify-end gap-2.5 pt-3 border-t border-border/60">
                <Button
                  variant="outline"
                  onClick={() => setPreviewItem(null)}
                  className="rounded-xl cursor-pointer"
                >
                  Close
                </Button>
                <Button
                  onClick={() => {
                    const item = previewItem;
                    setPreviewItem(null);
                    openEdit(item);
                  }}
                  className="gap-1.5 rounded-xl cursor-pointer"
                >
                  <Pencil className="h-4 w-4" /> Edit Announcement
                </Button>
              </div>
            </div>
          )}
        </DialogContent>
      </Dialog>

      {/* ── Create / Edit Dialog ── */}
      <Dialog open={dialogOpen} onOpenChange={setDialogOpen}>
        <DialogContent className="max-w-xl rounded-2xl p-6">
          <DialogHeader>
            <DialogTitle className="text-xl font-bold">
              {editing ? "Edit Announcement" : "Create New Announcement"}
            </DialogTitle>
            <DialogDescription className="text-xs text-muted-foreground">
              {editing
                ? "Update bulletin information, title, or target barangay."
                : "Post a new municipal advisory or barangay-specific announcement to the tourism portal."}
            </DialogDescription>
          </DialogHeader>

          <div className="space-y-4 pt-2">
            {/* Title */}
            <div className="space-y-1.5">
              <div className="flex justify-between items-center">
                <Label htmlFor="ann-title" className="text-xs font-bold uppercase tracking-wider">
                  Title <span className="text-destructive">*</span>
                </Label>
                <span className="text-[11px] text-muted-foreground">
                  {form.title.length}/200
                </span>
              </div>
              <Input
                id="ann-title"
                maxLength={200}
                value={form.title}
                onChange={(e) => setForm({ ...form, title: e.target.value })}
                placeholder="e.g., Water Service Interruption Advisory or Cultural Festival 2026"
                className="h-10.5 rounded-xl border-border/80 text-sm focus-visible:ring-primary"
              />
            </div>

            {/* Scope / Barangay */}
            <div className="space-y-1.5">
              <Label htmlFor="ann-barangay" className="text-xs font-bold uppercase tracking-wider">
                Target Barangay Scope
              </Label>
              <select
                id="ann-barangay"
                value={form.barangay_id}
                onChange={(e) => setForm({ ...form, barangay_id: e.target.value })}
                className="w-full h-10.5 rounded-xl border border-border/80 bg-card px-3 text-sm text-foreground focus:outline-none focus:ring-2 focus:ring-primary/20 cursor-pointer"
              >
                <option value="">All Barangays (LGU / Town-Wide Advisory)</option>
                {barangays.map((b) => (
                  <option key={b.id} value={b.id}>
                    Barangay {b.name}
                  </option>
                ))}
              </select>
              <p className="text-[11px] text-muted-foreground">
                Leave as &quot;All Barangays&quot; for municipality-wide announcements.
              </p>
            </div>

            {/* Content Textarea */}
            <div className="space-y-1.5">
              <div className="flex justify-between items-center">
                <Label htmlFor="ann-content" className="text-xs font-bold uppercase tracking-wider">
                  Announcement Body <span className="text-destructive">*</span>
                </Label>
                <span className="text-[11px] text-muted-foreground">
                  {form.content.length} characters
                </span>
              </div>
              <Textarea
                id="ann-content"
                rows={7}
                value={form.content}
                onChange={(e) => setForm({ ...form, content: e.target.value })}
                placeholder="Write full announcement details, guidelines, dates, affected areas, and contact hotlines..."
                className="rounded-xl border-border/80 text-sm focus-visible:ring-primary leading-relaxed resize-y"
              />
            </div>

            {/* Dialog Footer Actions */}
            <div className="flex items-center justify-end gap-2.5 pt-3 border-t border-border/60">
              <Button
                variant="outline"
                onClick={() => setDialogOpen(false)}
                className="rounded-xl cursor-pointer"
              >
                <X className="h-4 w-4 mr-1" /> Cancel
              </Button>
              <Button
                onClick={save}
                disabled={saving || !form.title.trim() || !form.content.trim()}
                className="rounded-xl gap-1.5 cursor-pointer bg-primary text-primary-foreground hover:bg-primary/90"
              >
                {saving ? (
                  <Loader2 className="h-4 w-4 animate-spin" />
                ) : (
                  <Check className="h-4 w-4" />
                )}
                <span>{editing ? "Save Changes" : "Publish Announcement"}</span>
              </Button>
            </div>
          </div>
        </DialogContent>
      </Dialog>

      {/* ── Delete Confirmation Modal ── */}
      <Dialog open={!!itemToDelete} onOpenChange={(open) => !open && setItemToDelete(null)}>
        <DialogContent className="max-w-md rounded-2xl p-6">
          {itemToDelete && (
            <div className="space-y-4">
              <div className="flex items-center gap-3 text-destructive">
                <div className="p-3 rounded-2xl bg-destructive/10 border border-destructive/20">
                  <AlertCircle className="h-6 w-6" />
                </div>
                <div>
                  <DialogTitle className="text-lg font-bold">Delete Announcement?</DialogTitle>
                  <DialogDescription className="text-xs text-muted-foreground mt-0.5">
                    This action cannot be undone.
                  </DialogDescription>
                </div>
              </div>

              <div className="p-3.5 rounded-xl bg-muted/50 border border-border/60 text-xs space-y-1">
                <p className="font-semibold text-foreground line-clamp-1">{itemToDelete.title}</p>
                <p className="text-muted-foreground line-clamp-2">{itemToDelete.content}</p>
              </div>

              <div className="flex items-center justify-end gap-2.5 pt-2">
                <Button
                  variant="outline"
                  onClick={() => setItemToDelete(null)}
                  className="rounded-xl cursor-pointer"
                >
                  Cancel
                </Button>
                <Button
                  variant="destructive"
                  onClick={() => executeDelete(itemToDelete.id)}
                  disabled={actingId === itemToDelete.id}
                  className="gap-1.5 rounded-xl cursor-pointer"
                >
                  {actingId === itemToDelete.id ? (
                    <Loader2 className="h-4 w-4 animate-spin" />
                  ) : (
                    <Trash2 className="h-4 w-4" />
                  )}
                  <span>Permanently Delete</span>
                </Button>
              </div>
            </div>
          )}
        </DialogContent>
      </Dialog>
    </div>
  );
}

