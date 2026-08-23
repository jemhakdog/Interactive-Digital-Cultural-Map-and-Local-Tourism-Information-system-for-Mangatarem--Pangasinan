"use client";

import { useEffect, useState, useCallback, useMemo } from "react";
import { useAuth } from "@/lib/auth";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { fetchAPI, APIError } from "@/lib/api";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent } from "@/components/ui/card";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Sheet, SheetContent } from "@/components/ui/sheet";
import { DeleteDialog } from "@/components/admin-dialogs";
import {
  Loader2,
  Store,
  Check,
  X,
  Trash2,
  Search,
  LayoutGrid,
  List,
  RefreshCw,
  Clock,
  CheckCircle2,
  XCircle,
  Building2,
  Coffee,
  Utensils,
  Hotel,
  ShoppingBag,
  ExternalLink,
  MapPin,
  User,
  ShieldCheck,
  Star,
  Eye,
  Copy,
  ArrowUpDown,
  Filter,
  Layers,
  AlertTriangle,
} from "lucide-react";

interface Establishment {
  id: number;
  name: string;
  type?: string;
  status?: string;
  barangay?: string | null;
  owner_name?: string | null;
  owner_id?: number | null;
  verified?: boolean;
  cover_image_url?: string | null;
  rating_avg?: number | null;
  created_at?: string;
  address?: string | null;
  contact_number?: string | null;
  email?: string | null;
  website?: string | null;
  price_range?: string | null;
  latitude?: number | null;
  longitude?: number | null;
  description?: string | null;
}

const TYPE_CONFIG: Record<string, { label: string; icon: React.ElementType; color: string }> = {
  inn: { label: "Inn / Hotel", icon: Hotel, color: "text-indigo-600 dark:text-indigo-400 bg-indigo-500/10 border-indigo-500/20" },
  restaurant: { label: "Restaurant", icon: Utensils, color: "text-amber-600 dark:text-amber-400 bg-amber-500/10 border-amber-500/20" },
  cafe: { label: "Café", icon: Coffee, color: "text-orange-600 dark:text-orange-400 bg-orange-500/10 border-orange-500/20" },
  fastfood: { label: "Fast Food", icon: Utensils, color: "text-rose-600 dark:text-rose-400 bg-rose-500/10 border-rose-500/20" },
  retail: { label: "Retail Shop", icon: ShoppingBag, color: "text-teal-600 dark:text-teal-400 bg-teal-500/10 border-teal-500/20" },
  default: { label: "Business", icon: Store, color: "text-primary bg-primary/10 border-primary/20" },
};

const STATUS_BADGE: Record<string, { label: string; className: string; icon: React.ElementType }> = {
  pending: {
    label: "Pending",
    className: "bg-amber-500/10 text-amber-700 dark:text-amber-300 border-amber-500/30",
    icon: Clock,
  },
  approved: {
    label: "Approved",
    className: "bg-emerald-500/10 text-emerald-700 dark:text-emerald-300 border-emerald-500/30",
    icon: CheckCircle2,
  },
  rejected: {
    label: "Rejected",
    className: "bg-rose-500/10 text-rose-700 dark:text-rose-300 border-rose-500/30",
    icon: XCircle,
  },
};

export default function AdminEstablishmentsPage() {
  const { user, loading: authLoading } = useAuth();
  const router = useRouter();

  const [items, setItems] = useState<Establishment[]>([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [feedback, setFeedback] = useState<{ type: "success" | "error"; message: string } | null>(null);

  // Filters & State
  const [searchQuery, setSearchQuery] = useState("");
  const [statusFilter, setStatusFilter] = useState<string>("all");
  const [typeFilter, setTypeFilter] = useState<string>("all");
  const [barangayFilter, setBarangayFilter] = useState<string>("all");
  const [verifiedFilter, setVerifiedFilter] = useState(false);
  const [sortBy, setSortBy] = useState<"newest" | "name" | "status" | "rating">("newest");
  const [viewMode, setViewMode] = useState<"grid" | "table">("grid");

  // Selection for inspect / delete
  const [inspectTarget, setInspectTarget] = useState<Establishment | null>(null);
  const [deleteTarget, setDeleteTarget] = useState<Establishment | null>(null);
  const [copiedCoords, setCopiedCoords] = useState<number | null>(null);
  const [actionLoading, setActionLoading] = useState<number | null>(null);

  const loadData = useCallback(async () => {
    try {
      const data = await fetchAPI<{ establishments: Establishment[] }>("/api/admin/establishments");
      setItems(data.establishments ?? []);
    } catch (err) {
      setFeedback({
        type: "error",
        message: err instanceof APIError ? err.detail : "Failed to load establishment directory.",
      });
    }
  }, []);

  useEffect(() => {
    if (!authLoading && (!user || user.role !== "admin")) router.push("/dashboard");
  }, [user, authLoading, router]);

  useEffect(() => {
    if (!user) return;
    loadData().finally(() => setLoading(false));
  }, [user, loadData]);

  const handleRefresh = async () => {
    setRefreshing(true);
    await loadData();
    setRefreshing(false);
  };

  const handleModerate = async (est: Establishment, action: "approve" | "reject" | "delete") => {
    setActionLoading(est.id);
    try {
      await fetchAPI(`/api/admin/establishments/${est.id}/moderate`, {
        method: "POST",
        body: JSON.stringify({ action }),
      });
      setFeedback({
        type: "success",
        message: `"${est.name}" was successfully ${action === "approve" ? "approved" : action === "reject" ? "rejected" : "deleted"}.`,
      });

      // Update state locally
      if (action === "delete") {
        setItems((prev) => prev.filter((item) => item.id !== est.id));
        if (inspectTarget?.id === est.id) setInspectTarget(null);
      } else {
        const nextStatus = action === "approve" ? "approved" : "rejected";
        setItems((prev) =>
          prev.map((item) => (item.id === est.id ? { ...item, status: nextStatus } : item))
        );
        if (inspectTarget?.id === est.id) {
          setInspectTarget({ ...inspectTarget, status: nextStatus });
        }
      }
    } catch (err) {
      setFeedback({
        type: "error",
        message: err instanceof APIError ? err.detail : `Could not perform action on "${est.name}".`,
      });
    } finally {
      setActionLoading(null);
      setDeleteTarget(null);
      setTimeout(() => setFeedback(null), 4000);
    }
  };

  const handleCopyCoords = (est: Establishment) => {
    if (est.latitude != null && est.longitude != null) {
      navigator.clipboard.writeText(`${est.latitude}, ${est.longitude}`);
      setCopiedCoords(est.id);
      setTimeout(() => setCopiedCoords(null), 2000);
    }
  };

  // Unique options for filters
  const types = useMemo(() => {
    const set = new Set<string>();
    items.forEach((i) => {
      if (i.type) set.add(i.type);
    });
    return Array.from(set).sort();
  }, [items]);

  const barangays = useMemo(() => {
    const set = new Set<string>();
    items.forEach((i) => {
      if (i.barangay) set.add(i.barangay);
    });
    return Array.from(set).sort();
  }, [items]);

  // Filtered & Sorted Records
  const filteredItems = useMemo(() => {
    return items
      .filter((est) => {
        // Query search
        if (searchQuery.trim()) {
          const q = searchQuery.toLowerCase();
          const matchName = est.name?.toLowerCase().includes(q);
          const matchOwner = est.owner_name?.toLowerCase().includes(q);
          const matchBarangay = est.barangay?.toLowerCase().includes(q);
          const matchType = est.type?.toLowerCase().includes(q);
          if (!matchName && !matchOwner && !matchBarangay && !matchType) return false;
        }

        // Status filter
        if (statusFilter !== "all") {
          const st = (est.status || "pending").toLowerCase();
          if (st !== statusFilter) return false;
        }

        // Type filter
        if (typeFilter !== "all" && est.type !== typeFilter) {
          return false;
        }

        // Barangay filter
        if (barangayFilter !== "all" && est.barangay !== barangayFilter) {
          return false;
        }

        // Verified filter
        if (verifiedFilter && !est.verified) {
          return false;
        }

        return true;
      })
      .sort((a, b) => {
        if (sortBy === "name") return (a.name || "").localeCompare(b.name || "");
        if (sortBy === "status") return (a.status || "").localeCompare(b.status || "");
        if (sortBy === "rating") return (b.rating_avg || 0) - (a.rating_avg || 0);
        if (sortBy === "newest") return (b.id || 0) - (a.id || 0);
        return 0;
      });
  }, [items, searchQuery, statusFilter, typeFilter, barangayFilter, verifiedFilter, sortBy]);

  // Metrics
  const totalCount = items.length;
  const pendingCount = items.filter((e) => (e.status || "pending").toLowerCase() === "pending").length;
  const approvedCount = items.filter((e) => (e.status || "").toLowerCase() === "approved").length;
  const rejectedCount = items.filter((e) => (e.status || "").toLowerCase() === "rejected").length;
  const verifiedCount = items.filter((e) => e.verified).length;

  if (authLoading || !user || loading) {
    return (
      <div className="container mx-auto px-4 py-20 max-w-7xl">
        <div className="flex flex-col items-center justify-center gap-3">
          <Loader2 className="h-8 w-8 animate-spin text-primary" />
          <p className="text-sm text-muted-foreground animate-pulse">Loading business registry...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8 max-w-7xl space-y-8">
      {/* Header Banner */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-border/60 pb-6">
        <div className="flex items-center gap-4">
          <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-primary/10 text-primary border border-primary/20 shadow-xs">
            <Building2 className="h-6 w-6" />
          </div>
          <div>
            <div className="flex items-center gap-2.5">
              <h1 className="text-2xl sm:text-3xl font-extrabold tracking-tight text-foreground">
                Business Establishments
              </h1>
              <Badge variant="outline" className="font-mono text-xs px-2.5 py-0.5 rounded-full border-border bg-muted/50">
                {totalCount} Total
              </Badge>
            </div>
            <p className="text-sm text-muted-foreground mt-1">
              Moderate local businesses, dining, accommodations, and tourist services in Mangatarem
            </p>
          </div>
        </div>

        <div className="flex items-center gap-2.5">
          <Button
            variant="outline"
            size="sm"
            onClick={handleRefresh}
            disabled={refreshing}
            className="rounded-xl h-10 gap-2 text-muted-foreground hover:text-foreground cursor-pointer"
          >
            <RefreshCw className={`h-4 w-4 ${refreshing ? "animate-spin" : ""}`} />
            <span className="hidden sm:inline">Refresh</span>
          </Button>

          <Link href="/business" target="_blank">
            <Button variant="outline" size="sm" className="rounded-xl h-10 gap-2 text-muted-foreground hover:text-foreground cursor-pointer">
              <ExternalLink className="h-4 w-4" />
              <span>Public Directory</span>
            </Button>
          </Link>
        </div>
      </div>

      {/* Alert Notices */}
      {feedback && (
        <div
          className={`rounded-xl border px-4 py-3 text-sm flex items-center justify-between gap-2 shadow-xs animate-in fade-in slide-in-from-top-1 ${
            feedback.type === "success"
              ? "border-emerald-500/30 bg-emerald-500/10 text-emerald-700 dark:text-emerald-300"
              : "border-destructive/30 bg-destructive/10 text-destructive"
          }`}
        >
          <div className="flex items-center gap-2">
            {feedback.type === "success" ? (
              <CheckCircle2 className="h-4 w-4 shrink-0 text-emerald-600" />
            ) : (
              <AlertTriangle className="h-4 w-4 shrink-0 text-destructive" />
            )}
            <span className="font-medium">{feedback.message}</span>
          </div>
          <Button
            variant="ghost"
            size="icon"
            className="h-6 w-6 rounded-md hover:bg-black/5"
            onClick={() => setFeedback(null)}
          >
            <X className="h-3.5 w-3.5" />
          </Button>
        </div>
      )}

      {/* KPI Metric Overview */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <Card className="rounded-2xl border-border/60 shadow-xs bg-card/60 backdrop-blur-xs">
          <CardContent className="p-4 sm:p-5 flex items-center justify-between">
            <div>
              <p className="text-xs font-medium text-muted-foreground uppercase tracking-wider">Pending Review</p>
              <h3 className="text-2xl font-bold mt-1 text-foreground">{pendingCount}</h3>
              <p className="text-xs text-amber-600 dark:text-amber-400 mt-0.5">
                {pendingCount > 0 ? "Requires moderation" : "All caught up"}
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
              <p className="text-xs font-medium text-muted-foreground uppercase tracking-wider">Approved / Live</p>
              <h3 className="text-2xl font-bold mt-1 text-foreground">{approvedCount}</h3>
              <p className="text-xs text-emerald-600 dark:text-emerald-400 mt-0.5 flex items-center gap-1">
                <CheckCircle2 className="h-3 w-3 inline" />
                {totalCount > 0 ? `${Math.round((approvedCount / totalCount) * 100)}% of directory` : "0%"}
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
              <p className="text-xs font-medium text-muted-foreground uppercase tracking-wider">Verified Merchants</p>
              <h3 className="text-2xl font-bold mt-1 text-foreground">{verifiedCount}</h3>
              <p className="text-xs text-blue-600 dark:text-blue-400 mt-0.5">Official Permit Verified</p>
            </div>
            <div className="h-11 w-11 rounded-xl bg-blue-500/10 text-blue-600 dark:text-blue-400 flex items-center justify-center">
              <ShieldCheck className="h-5 w-5" />
            </div>
          </CardContent>
        </Card>

        <Card className="rounded-2xl border-border/60 shadow-xs bg-card/60 backdrop-blur-xs">
          <CardContent className="p-4 sm:p-5 flex items-center justify-between">
            <div>
              <p className="text-xs font-medium text-muted-foreground uppercase tracking-wider">Rejected</p>
              <h3 className="text-2xl font-bold mt-1 text-foreground">{rejectedCount}</h3>
              <p className="text-xs text-muted-foreground mt-0.5">Non-compliant or closed</p>
            </div>
            <div className="h-11 w-11 rounded-xl bg-rose-500/10 text-rose-600 dark:text-rose-400 flex items-center justify-center">
              <XCircle className="h-5 w-5" />
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Filter & Toolbar Area */}
      <div className="flex flex-col gap-4 bg-muted/40 p-4 rounded-2xl border border-border/50">
        <div className="flex flex-col lg:flex-row items-stretch lg:items-center justify-between gap-3">
          {/* Search Input */}
          <div className="relative flex-1">
            <Search className="absolute left-3.5 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
            <Input
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Search establishments by name, owner, type, barangay..."
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

          {/* Quick Filter Selects */}
          <div className="flex flex-wrap items-center gap-2">
            {/* Status Select */}
            <select
              value={statusFilter}
              onChange={(e) => setStatusFilter(e.target.value)}
              className="h-10 px-3 rounded-xl bg-background border border-border/80 text-sm font-medium text-foreground focus:outline-none focus:ring-1 focus:ring-primary cursor-pointer"
            >
              <option value="all">All Statuses</option>
              <option value="pending">Pending ({pendingCount})</option>
              <option value="approved">Approved ({approvedCount})</option>
              <option value="rejected">Rejected ({rejectedCount})</option>
            </select>

            {/* Type Select */}
            <select
              value={typeFilter}
              onChange={(e) => setTypeFilter(e.target.value)}
              className="h-10 px-3 rounded-xl bg-background border border-border/80 text-sm font-medium text-foreground focus:outline-none focus:ring-1 focus:ring-primary cursor-pointer"
            >
              <option value="all">All Business Types</option>
              {types.map((t) => (
                <option key={t} value={t}>
                  {TYPE_CONFIG[t]?.label ?? t.toUpperCase()}
                </option>
              ))}
            </select>

            {/* Barangay Select */}
            {barangays.length > 0 && (
              <select
                value={barangayFilter}
                onChange={(e) => setBarangayFilter(e.target.value)}
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

            {/* Verified Filter Button */}
            <Button
              variant={verifiedFilter ? "default" : "outline"}
              size="sm"
              onClick={() => setVerifiedFilter(!verifiedFilter)}
              className={`h-10 rounded-xl gap-1.5 transition-colors cursor-pointer ${
                verifiedFilter
                  ? "bg-blue-600 text-white hover:bg-blue-700 border-blue-700"
                  : "bg-background text-muted-foreground hover:text-foreground"
              }`}
            >
              <ShieldCheck className="h-4 w-4" />
              <span className="text-xs font-semibold">Verified</span>
            </Button>

            {/* Sort Dropdown */}
            <div className="flex items-center rounded-xl bg-background border border-border/80 h-10 px-2 gap-1 text-muted-foreground">
              <ArrowUpDown className="h-3.5 w-3.5 ml-1 text-muted-foreground/80" />
              <select
                value={sortBy}
                onChange={(e) => setSortBy(e.target.value as "newest" | "name" | "status" | "rating")}
                className="bg-transparent border-0 text-xs font-medium text-foreground focus:outline-none cursor-pointer pr-2"
              >
                <option value="newest">Newest Added</option>
                <option value="name">Name (A-Z)</option>
                <option value="rating">Top Rated</option>
                <option value="status">Status</option>
              </select>
            </div>

            {/* View Mode Switcher */}
            <div className="flex items-center rounded-xl bg-background border border-border/80 p-1 h-10">
              <Button
                variant={viewMode === "grid" ? "secondary" : "ghost"}
                size="icon"
                onClick={() => setViewMode("grid")}
                className="h-8 w-8 rounded-lg cursor-pointer"
                title="Grid View"
              >
                <LayoutGrid className="h-4 w-4" />
              </Button>
              <Button
                variant={viewMode === "table" ? "secondary" : "ghost"}
                size="icon"
                onClick={() => setViewMode("table")}
                className="h-8 w-8 rounded-lg cursor-pointer"
                title="Table View"
              >
                <List className="h-4 w-4" />
              </Button>
            </div>
          </div>
        </div>

        {/* Active Filter Badges */}
        {(searchQuery || statusFilter !== "all" || typeFilter !== "all" || barangayFilter !== "all" || verifiedFilter) && (
          <div className="flex flex-wrap items-center gap-2 pt-2 border-t border-border/50 text-xs text-muted-foreground">
            <span className="font-medium flex items-center gap-1">
              <Filter className="h-3.5 w-3.5" /> Filters:
            </span>
            {searchQuery && (
              <Badge variant="secondary" className="gap-1 rounded-md text-xs py-0.5">
                Query: {searchQuery}
                <button onClick={() => setSearchQuery("")} className="hover:text-foreground cursor-pointer">
                  <X className="h-3 w-3" />
                </button>
              </Badge>
            )}
            {statusFilter !== "all" && (
              <Badge variant="secondary" className="gap-1 rounded-md text-xs py-0.5">
                Status: {statusFilter}
                <button onClick={() => setStatusFilter("all")} className="hover:text-foreground cursor-pointer">
                  <X className="h-3 w-3" />
                </button>
              </Badge>
            )}
            {typeFilter !== "all" && (
              <Badge variant="secondary" className="gap-1 rounded-md text-xs py-0.5">
                Type: {typeFilter}
                <button onClick={() => setTypeFilter("all")} className="hover:text-foreground cursor-pointer">
                  <X className="h-3 w-3" />
                </button>
              </Badge>
            )}
            {barangayFilter !== "all" && (
              <Badge variant="secondary" className="gap-1 rounded-md text-xs py-0.5">
                Barangay: {barangayFilter}
                <button onClick={() => setBarangayFilter("all")} className="hover:text-foreground cursor-pointer">
                  <X className="h-3 w-3" />
                </button>
              </Badge>
            )}
            {verifiedFilter && (
              <Badge variant="secondary" className="gap-1 rounded-md text-xs py-0.5">
                Verified Only
                <button onClick={() => setVerifiedFilter(false)} className="hover:text-foreground cursor-pointer">
                  <X className="h-3 w-3" />
                </button>
              </Badge>
            )}
            <Button
              variant="ghost"
              size="sm"
              onClick={() => {
                setSearchQuery("");
                setStatusFilter("all");
                setTypeFilter("all");
                setBarangayFilter("all");
                setVerifiedFilter(false);
              }}
              className="h-6 px-2 text-xs text-primary hover:underline hover:bg-transparent cursor-pointer"
            >
              Reset all
            </Button>
            <span className="ml-auto text-xs font-medium text-foreground">
              Showing {filteredItems.length} of {totalCount}
            </span>
          </div>
        )}
      </div>

      {/* Main Content Area */}
      {filteredItems.length === 0 ? (
        <div className="border border-dashed border-border/80 rounded-2xl py-20 text-center bg-card/40">
          <div className="h-14 w-14 rounded-2xl bg-muted/80 text-muted-foreground/60 flex items-center justify-center mx-auto mb-4 border border-border/60">
            <Store className="h-7 w-7" />
          </div>
          <h3 className="text-base font-bold text-foreground">No establishments found</h3>
          <p className="text-sm text-muted-foreground mt-1 max-w-sm mx-auto">
            {items.length === 0
              ? "Business listings will appear here once registered by merchant owners."
              : "No business establishments match your current filter and search conditions."}
          </p>
          {items.length > 0 && (
            <div className="mt-5">
              <Button
                variant="outline"
                size="sm"
                onClick={() => {
                  setSearchQuery("");
                  setStatusFilter("all");
                  setTypeFilter("all");
                  setBarangayFilter("all");
                  setVerifiedFilter(false);
                }}
                className="rounded-xl cursor-pointer"
              >
                Clear all filters
              </Button>
            </div>
          )}
        </div>
      ) : viewMode === "grid" ? (
        /* Visual Card Grid Mode */
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
          {filteredItems.map((est) => {
            const rawStatus = (est.status ?? "pending").toLowerCase();
            const statusConfig = STATUS_BADGE[rawStatus] ?? STATUS_BADGE.pending;
            const StatusIcon = statusConfig.icon;
            const typeConfig = TYPE_CONFIG[est.type ?? ""] ?? TYPE_CONFIG.default;
            const TypeIcon = typeConfig.icon;

            return (
              <Card
                key={est.id}
                className="group relative overflow-hidden rounded-2xl border-border/60 hover:border-border transition-all duration-200 hover:shadow-md bg-card flex flex-col justify-between"
              >
                <div>
                  {/* Image banner */}
                  <div className="relative aspect-video w-full overflow-hidden bg-muted">
                    {est.cover_image_url ? (
                      // eslint-disable-next-line @next/next/no-img-element
                      <img
                        src={est.cover_image_url}
                        alt={est.name}
                        className="h-full w-full object-cover transition-transform duration-300 group-hover:scale-105"
                      />
                    ) : (
                      <div className="flex h-full w-full items-center justify-center bg-gradient-to-br from-muted to-muted/60 text-muted-foreground/40">
                        <TypeIcon className="h-12 w-12 stroke-[1.25]" />
                      </div>
                    )}

                    {/* Gradient Overlay */}
                    <div className="absolute inset-0 bg-gradient-to-t from-black/75 via-black/20 to-transparent" />

                    {/* Category Type Badge */}
                    <div className="absolute top-3 left-3 flex items-center gap-1.5">
                      <span className={`inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-semibold backdrop-blur-md border ${typeConfig.color}`}>
                        <TypeIcon className="h-3 w-3" />
                        {typeConfig.label}
                      </span>
                      {est.verified && (
                        <span className="inline-flex items-center gap-0.5 px-2 py-0.5 rounded-full text-[10px] font-bold bg-blue-500/90 text-white shadow-xs backdrop-blur-md">
                          <ShieldCheck className="h-3 w-3" /> Verified
                        </span>
                      )}
                    </div>

                    {/* Status Badge */}
                    <div className="absolute top-3 right-3">
                      <span className={`inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-bold capitalize backdrop-blur-md border shadow-xs ${statusConfig.className}`}>
                        <StatusIcon className="h-3 w-3" />
                        {statusConfig.label}
                      </span>
                    </div>

                    {/* Location & Rating bottom bar */}
                    <div className="absolute bottom-3 left-3 right-3 flex items-center justify-between text-white text-xs">
                      <div className="flex items-center gap-1 truncate font-medium drop-shadow-xs">
                        <MapPin className="h-3.5 w-3.5 shrink-0 text-primary" />
                        <span className="truncate">
                          {est.barangay ? `Brgy. ${est.barangay}` : "Mangatarem"}
                        </span>
                      </div>
                      {est.rating_avg != null && est.rating_avg > 0 && (
                        <div className="flex items-center gap-1 bg-black/60 backdrop-blur-md px-2 py-0.5 rounded-md font-semibold text-amber-400">
                          <Star className="h-3 w-3 fill-amber-400" />
                          <span>{est.rating_avg.toFixed(1)}</span>
                        </div>
                      )}
                    </div>
                  </div>

                  {/* Body Info */}
                  <div className="p-4 sm:p-5 space-y-3">
                    <div>
                      <h3 className="font-bold text-base text-foreground line-clamp-1 group-hover:text-primary transition-colors">
                        {est.name}
                      </h3>
                      <div className="flex items-center gap-2 text-xs text-muted-foreground mt-1">
                        <User className="h-3.5 w-3.5 text-muted-foreground/70" />
                        <span className="truncate">Owner: {est.owner_name ?? `Merchant #${est.owner_id ?? "—"}`}</span>
                      </div>
                    </div>

                    {est.description && (
                      <p className="text-xs text-muted-foreground line-clamp-2 leading-relaxed">
                        {est.description}
                      </p>
                    )}
                  </div>
                </div>

                {/* Card Actions Footer */}
                <div className="p-4 pt-0 sm:p-5 sm:pt-0 flex flex-col gap-2.5 border-t border-border/40 mt-2">
                  <div className="flex items-center justify-between gap-2 pt-3">
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => setInspectTarget(est)}
                      className="rounded-xl h-8 text-xs gap-1.5 flex-1 hover:bg-muted cursor-pointer"
                    >
                      <Eye className="h-3.5 w-3.5 text-muted-foreground" />
                      Details
                    </Button>

                    <Button
                      variant="ghost"
                      size="icon"
                      onClick={() => setDeleteTarget(est)}
                      className="h-8 w-8 rounded-lg text-destructive hover:bg-destructive/10 cursor-pointer"
                      title="Delete Establishment"
                    >
                      <Trash2 className="h-3.5 w-3.5" />
                    </Button>
                  </div>

                  {/* Quick Moderate Buttons */}
                  <div className="grid grid-cols-2 gap-2">
                    <Button
                      size="sm"
                      variant={rawStatus === "approved" ? "secondary" : "default"}
                      disabled={actionLoading === est.id || rawStatus === "approved"}
                      onClick={() => handleModerate(est, "approve")}
                      className={`h-8 rounded-xl text-xs gap-1 cursor-pointer ${
                        rawStatus !== "approved" ? "bg-emerald-600 hover:bg-emerald-700 text-white" : ""
                      }`}
                    >
                      {actionLoading === est.id ? (
                        <Loader2 className="h-3.5 w-3.5 animate-spin" />
                      ) : (
                        <Check className="h-3.5 w-3.5" />
                      )}
                      {rawStatus === "approved" ? "Approved" : "Approve"}
                    </Button>

                    <Button
                      size="sm"
                      variant={rawStatus === "rejected" ? "secondary" : "outline"}
                      disabled={actionLoading === est.id || rawStatus === "rejected"}
                      onClick={() => handleModerate(est, "reject")}
                      className={`h-8 rounded-xl text-xs gap-1 cursor-pointer ${
                        rawStatus !== "rejected" ? "text-rose-600 border-rose-200 hover:bg-rose-50 dark:hover:bg-rose-950/30" : ""
                      }`}
                    >
                      {actionLoading === est.id ? (
                        <Loader2 className="h-3.5 w-3.5 animate-spin" />
                      ) : (
                        <X className="h-3.5 w-3.5" />
                      )}
                      {rawStatus === "rejected" ? "Rejected" : "Reject"}
                    </Button>
                  </div>
                </div>
              </Card>
            );
          })}
        </div>
      ) : (
        /* Data Table Mode */
        <div className="rounded-2xl border border-border/70 overflow-hidden bg-card shadow-xs">
          <Table>
            <TableHeader className="bg-muted/50">
              <TableRow>
                <TableHead className="w-[300px]">Establishment</TableHead>
                <TableHead>Type</TableHead>
                <TableHead>Owner</TableHead>
                <TableHead>Barangay</TableHead>
                <TableHead>Status</TableHead>
                <TableHead className="text-right">Actions</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {filteredItems.map((est) => {
                const rawStatus = (est.status ?? "pending").toLowerCase();
                const statusConfig = STATUS_BADGE[rawStatus] ?? STATUS_BADGE.pending;
                const StatusIcon = statusConfig.icon;
                const typeConfig = TYPE_CONFIG[est.type ?? ""] ?? TYPE_CONFIG.default;
                const TypeIcon = typeConfig.icon;

                return (
                  <TableRow key={est.id} className="hover:bg-muted/30 transition-colors">
                    <TableCell>
                      <div className="flex items-center gap-3">
                        {est.cover_image_url ? (
                          // eslint-disable-next-line @next/next/no-img-element
                          <img
                            src={est.cover_image_url}
                            alt={est.name}
                            className="h-10 w-10 rounded-xl object-cover border border-border"
                          />
                        ) : (
                          <div className="h-10 w-10 rounded-xl bg-muted border border-border/80 flex items-center justify-center text-muted-foreground">
                            <TypeIcon className="h-5 w-5" />
                          </div>
                        )}
                        <div>
                          <div className="font-bold text-foreground flex items-center gap-1.5">
                            <span>{est.name}</span>
                            {est.verified && (
                              <span title="Verified Business">
                                <ShieldCheck className="h-3.5 w-3.5 text-blue-500" />
                              </span>
                            )}
                          </div>
                          {est.rating_avg != null && est.rating_avg > 0 && (
                            <div className="flex items-center gap-1 text-xs text-amber-500 mt-0.5">
                              <Star className="h-3 w-3 fill-amber-500" />
                              <span>{est.rating_avg.toFixed(1)}</span>
                            </div>
                          )}
                        </div>
                      </div>
                    </TableCell>

                    <TableCell>
                      <span className={`inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-semibold border ${typeConfig.color}`}>
                        <TypeIcon className="h-3 w-3" />
                        {typeConfig.label}
                      </span>
                    </TableCell>

                    <TableCell className="text-sm font-medium text-foreground">
                      {est.owner_name ?? `ID #${est.owner_id ?? "—"}`}
                    </TableCell>

                    <TableCell className="text-sm text-muted-foreground">
                      {est.barangay ? `Brgy. ${est.barangay}` : "—"}
                    </TableCell>

                    <TableCell>
                      <Badge variant="outline" className={`text-xs gap-1 font-semibold ${statusConfig.className}`}>
                        <StatusIcon className="h-3 w-3" />
                        {statusConfig.label}
                      </Badge>
                    </TableCell>

                    <TableCell className="text-right">
                      <div className="flex items-center justify-end gap-1.5">
                        <Button
                          variant="ghost"
                          size="icon"
                          onClick={() => setInspectTarget(est)}
                          className="h-8 w-8 rounded-lg text-muted-foreground hover:text-foreground cursor-pointer"
                          title="Inspect Details"
                        >
                          <Eye className="h-4 w-4" />
                        </Button>

                        {rawStatus !== "approved" && (
                          <Button
                            size="icon"
                            variant="ghost"
                            disabled={actionLoading === est.id}
                            onClick={() => handleModerate(est, "approve")}
                            className="h-8 w-8 rounded-lg text-emerald-600 hover:bg-emerald-500/10 cursor-pointer"
                            title="Approve"
                          >
                            <Check className="h-4 w-4" />
                          </Button>
                        )}

                        {rawStatus !== "rejected" && (
                          <Button
                            size="icon"
                            variant="ghost"
                            disabled={actionLoading === est.id}
                            onClick={() => handleModerate(est, "reject")}
                            className="h-8 w-8 rounded-lg text-rose-600 hover:bg-rose-500/10 cursor-pointer"
                            title="Reject"
                          >
                            <X className="h-4 w-4" />
                          </Button>
                        )}

                        <Button
                          size="icon"
                          variant="ghost"
                          onClick={() => setDeleteTarget(est)}
                          className="h-8 w-8 rounded-lg text-destructive hover:bg-destructive/10 cursor-pointer"
                          title="Delete"
                        >
                          <Trash2 className="h-4 w-4" />
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

      {/* Quick Inspection Drawer */}
      <Sheet open={!!inspectTarget} onOpenChange={(open) => !open && setInspectTarget(null)}>
        <SheetContent className="w-full sm:max-w-md overflow-y-auto p-0">
          {inspectTarget && (
            <div className="flex flex-col h-full">
              {/* Drawer Hero Image */}
              <div className="relative aspect-video w-full bg-muted">
                {inspectTarget.cover_image_url ? (
                  // eslint-disable-next-line @next/next/no-img-element
                  <img
                    src={inspectTarget.cover_image_url}
                    alt={inspectTarget.name}
                    className="h-full w-full object-cover"
                  />
                ) : (
                  <div className="flex h-full w-full items-center justify-center bg-muted text-muted-foreground/40">
                    <Building2 className="h-16 w-16" />
                  </div>
                )}
                <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-black/30 to-transparent" />
                <div className="absolute bottom-4 left-4 right-4 text-white">
                  <div className="flex items-center gap-2">
                    <span className="px-2.5 py-0.5 rounded-full text-xs font-semibold bg-white/20 backdrop-blur-md border border-white/30">
                      {TYPE_CONFIG[inspectTarget.type ?? ""]?.label ?? inspectTarget.type}
                    </span>
                    {inspectTarget.verified && (
                      <span className="px-2 py-0.5 rounded-full text-xs font-bold bg-blue-500 text-white flex items-center gap-1">
                        <ShieldCheck className="h-3 w-3" /> Verified
                      </span>
                    )}
                  </div>
                  <h2 className="text-xl font-bold mt-1 text-white">{inspectTarget.name}</h2>
                </div>
              </div>

              {/* Drawer Content Details */}
              <div className="p-6 space-y-6 flex-1">
                {/* Status & ID bar */}
                <div className="flex items-center justify-between bg-muted/40 p-3 rounded-xl border border-border/60">
                  <div>
                    <p className="text-[11px] font-medium text-muted-foreground uppercase">Listing Status</p>
                    <p className="text-sm font-bold capitalize text-foreground mt-0.5">
                      {inspectTarget.status ?? "pending"}
                    </p>
                  </div>
                  <div>
                    <p className="text-[11px] font-medium text-muted-foreground uppercase text-right">Directory ID</p>
                    <p className="text-sm font-mono font-bold text-foreground text-right mt-0.5">
                      #{inspectTarget.id}
                    </p>
                  </div>
                </div>

                {/* Info Fields */}
                <div className="space-y-4">
                  <div>
                    <label className="text-xs font-semibold text-muted-foreground uppercase">Owner / Merchant</label>
                    <p className="text-sm font-medium text-foreground mt-0.5 flex items-center gap-2">
                      <User className="h-4 w-4 text-primary" />
                      {inspectTarget.owner_name ?? "No owner attached"}
                    </p>
                  </div>

                  <div>
                    <label className="text-xs font-semibold text-muted-foreground uppercase">Location / Barangay</label>
                    <p className="text-sm font-medium text-foreground mt-0.5 flex items-center gap-2">
                      <MapPin className="h-4 w-4 text-primary" />
                      {inspectTarget.barangay ? `Brgy. ${inspectTarget.barangay}` : "Mangatarem, Pangasinan"}
                    </p>
                  </div>

                  {inspectTarget.description && (
                    <div>
                      <label className="text-xs font-semibold text-muted-foreground uppercase">Description</label>
                      <p className="text-sm text-muted-foreground mt-1 leading-relaxed bg-muted/30 p-3 rounded-xl border border-border/40">
                        {inspectTarget.description}
                      </p>
                    </div>
                  )}

                  {/* Coordinates snippet */}
                  {inspectTarget.latitude != null && inspectTarget.longitude != null && (
                    <div>
                      <label className="text-xs font-semibold text-muted-foreground uppercase">Map Coordinates</label>
                      <div className="flex items-center justify-between text-xs text-muted-foreground bg-muted/50 rounded-xl px-3 py-2 mt-1 font-mono border border-border/50">
                        <span>{inspectTarget.latitude.toFixed(5)}, {inspectTarget.longitude.toFixed(5)}</span>
                        <button
                          onClick={() => handleCopyCoords(inspectTarget)}
                          className="hover:text-foreground cursor-pointer flex items-center gap-1 font-sans text-[11px]"
                        >
                          {copiedCoords === inspectTarget.id ? (
                            <span className="text-emerald-600 flex items-center gap-1 font-bold">
                              <Check className="h-3.5 w-3.5" /> Copied
                            </span>
                          ) : (
                            <span className="flex items-center gap-1">
                              <Copy className="h-3.5 w-3.5" /> Copy
                            </span>
                          )}
                        </button>
                      </div>
                    </div>
                  )}
                </div>

                {/* Moderation Actions Inside Drawer */}
                <div className="pt-4 border-t border-border/60 space-y-2">
                  <p className="text-xs font-semibold text-muted-foreground uppercase mb-2">Moderate Listing</p>
                  <div className="grid grid-cols-2 gap-2">
                    <Button
                      onClick={() => handleModerate(inspectTarget, "approve")}
                      disabled={actionLoading === inspectTarget.id || inspectTarget.status === "approved"}
                      className="rounded-xl gap-1.5 bg-emerald-600 hover:bg-emerald-700 text-white cursor-pointer"
                    >
                      <Check className="h-4 w-4" /> Approve
                    </Button>
                    <Button
                      variant="outline"
                      onClick={() => handleModerate(inspectTarget, "reject")}
                      disabled={actionLoading === inspectTarget.id || inspectTarget.status === "rejected"}
                      className="rounded-xl gap-1.5 text-rose-600 border-rose-200 hover:bg-rose-50 dark:hover:bg-rose-950/30 cursor-pointer"
                    >
                      <X className="h-4 w-4" /> Reject
                    </Button>
                  </div>
                  <Button
                    variant="ghost"
                    onClick={() => {
                      setDeleteTarget(inspectTarget);
                      setInspectTarget(null);
                    }}
                    className="w-full text-destructive hover:bg-destructive/10 rounded-xl gap-1.5 text-xs cursor-pointer mt-2"
                  >
                    <Trash2 className="h-4 w-4" /> Delete Establishment
                  </Button>
                </div>
              </div>
            </div>
          )}
        </SheetContent>
      </Sheet>

      {/* Confirmation Dialog for Deletion */}
      <DeleteDialog
        open={!!deleteTarget}
        onOpenChange={(open) => !open && setDeleteTarget(null)}
        title="Delete Business Establishment?"
        description={`Are you sure you want to permanently delete "${deleteTarget?.name}"? This will remove all associated rooms, menus, reviews, and bookings. This action cannot be undone.`}
        onConfirm={async () => {
          if (deleteTarget) {
            await handleModerate(deleteTarget, "delete");
          }
        }}
      />
    </div>
  );
}
