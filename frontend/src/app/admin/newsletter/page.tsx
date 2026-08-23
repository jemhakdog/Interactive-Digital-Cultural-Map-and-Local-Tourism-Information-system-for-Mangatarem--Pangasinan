"use client";

import { useCallback, useEffect, useMemo, useState } from "react";
import { useAuth } from "@/lib/auth";
import { useRouter } from "next/navigation";
import {
  Loader2,
  Mail,
  PenSquare,
  History,
  Download,
  Trash2,
  Search,
  CheckCircle2,
  AlertCircle,
  Users,
  Send,
  Sparkles,
  RefreshCw,
  X,
  Eye,
  ArrowUpDown,
  ChevronLeft,
  ChevronRight,
  SendHorizontal,
  MailCheck,
  ShieldAlert,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Badge } from "@/components/ui/badge";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogDescription,
  DialogFooter,
} from "@/components/ui/dialog";
import { fetchAPI } from "@/lib/api";

interface Subscriber {
  id: number;
  email: string;
  is_active: boolean;
  created_at: string | null;
}

interface Dispatch {
  id: number;
  subject: string;
  content: string | null;
  recipient_count: number;
  sender_id: number | null;
  sent_at: string | null;
}

const TEMPLATES = [
  {
    name: "🌟 Festival Announcement",
    subject: "Discover the Magic of Mangatarem: Upcoming Town Celebrations",
    content: `Dear Explorer,\n\nWe are delighted to invite you and your family to the upcoming cultural festivities in Mangatarem, Pangasinan!\n\nJoin us as we celebrate our local traditions, vibrant street dances, agricultural exhibits, and delicious Pangasinense culinary treats.\n\nCheck out the full itinerary on our official portal!\n\nWarm regards,\nMangatarem Tourism Office`,
  },
  {
    name: "🌿 Eco-Tourism & Hot Springs",
    subject: "Experience Serenity: Manleluag Spring Protected Landscape",
    content: `Hello Fellow Traveler,\n\nLooking for your next nature getaway? The Manleluag Spring Protected Landscape is open and welcoming visitors.\n\nEnjoy our rejuvenating hot springs, lush forest trails, and diverse bird species. Remember to book your visits in advance to ensure an eco-friendly experience.\n\nSee you in Mangatarem!\n\nMangatarem Tourism Office`,
  },
  {
    name: "🏛️ Cultural Heritage Spotlight",
    subject: "Preserving Our Roots: Mangatarem Heritage Spotlight",
    content: `Greetings,\n\nThis month, we are spotlighting our treasured historical landmarks and centuries-old architectural heritage.\n\nExplore our digital cultural registry to learn about the stories, heroes, and historical structures that shaped our beloved municipality.\n\nMangatarem Tourism & Culture Committee`,
  },
];

const ITEMS_PER_PAGE = 8;

export default function AdminNewsletterPage() {
  const { user, loading: authLoading } = useAuth();
  const router = useRouter();

  // Data states
  const [subscribers, setSubscribers] = useState<Subscriber[]>([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Table filtering & pagination
  const [searchQuery, setSearchQuery] = useState("");
  const [statusFilter, setStatusFilter] = useState<"all" | "active" | "inactive">("all");
  const [sortBy, setSortBy] = useState<"newest" | "oldest" | "email-asc" | "email-desc">("newest");
  const [currentPage, setCurrentPage] = useState(1);

  // Compose modal state
  const [composeOpen, setComposeOpen] = useState(false);
  const [composeTab, setComposeTab] = useState<"edit" | "preview">("edit");
  const [subject, setSubject] = useState("");
  const [content, setContent] = useState("");
  const [sending, setSending] = useState(false);
  const [sendError, setSendError] = useState<string | null>(null);
  const [sendSuccessMessage, setSendSuccessMessage] = useState<string | null>(null);

  // History modal state
  const [historyOpen, setHistoryOpen] = useState(false);
  const [history, setHistory] = useState<Dispatch[]>([]);
  const [historyLoading, setHistoryLoading] = useState(false);
  const [historySearch, setHistorySearch] = useState("");
  const [expandedDispatchId, setExpandedDispatchId] = useState<number | null>(null);

  // Deactivation confirmation modal state
  const [deactivatingSub, setDeactivatingSub] = useState<Subscriber | null>(null);
  const [actionLoading, setActionLoading] = useState(false);

  useEffect(() => {
    if (!authLoading && (!user || user.role !== "admin")) router.push("/dashboard");
  }, [user, authLoading, router]);

  const loadSubscribers = useCallback(async (isRefresh = false) => {
    if (isRefresh) setRefreshing(true);
    else setLoading(true);
    setError(null);
    try {
      const data = await fetchAPI<Subscriber[]>("/api/newsletter/subscribers");
      setSubscribers(data);
    } catch {
      setError("Failed to load subscribers. Please verify network connection and try again.");
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  }, []);

  const loadHistory = useCallback(async () => {
    setHistoryLoading(true);
    try {
      const data = await fetchAPI<Dispatch[]>("/api/newsletter/history");
      setHistory(data);
    } catch {
      setError("Failed to load dispatch history.");
    } finally {
      setHistoryLoading(false);
    }
  }, []);

  useEffect(() => {
    if (!user) return;
    loadSubscribers();
    loadHistory();
  }, [user, loadSubscribers, loadHistory]);

  // Derived metrics
  const activeCount = useMemo(() => subscribers.filter((s) => s.is_active).length, [subscribers]);
  const inactiveCount = useMemo(() => subscribers.filter((s) => !s.is_active).length, [subscribers]);
  const totalCount = subscribers.length;
  const activePercent = totalCount > 0 ? Math.round((activeCount / totalCount) * 100) : 0;

  // Filtered and sorted subscribers
  const filteredSubscribers = useMemo(() => {
    let result = [...subscribers];

    // Status filter
    if (statusFilter === "active") {
      result = result.filter((s) => s.is_active);
    } else if (statusFilter === "inactive") {
      result = result.filter((s) => !s.is_active);
    }

    // Search query
    if (searchQuery.trim()) {
      const q = searchQuery.toLowerCase().trim();
      result = result.filter((s) => s.email.toLowerCase().includes(q));
    }

    // Sorting
    result.sort((a, b) => {
      if (sortBy === "newest") {
        return new Date(b.created_at || 0).getTime() - new Date(a.created_at || 0).getTime();
      }
      if (sortBy === "oldest") {
        return new Date(a.created_at || 0).getTime() - new Date(b.created_at || 0).getTime();
      }
      if (sortBy === "email-asc") {
        return a.email.localeCompare(b.email);
      }
      if (sortBy === "email-desc") {
        return b.email.localeCompare(a.email);
      }
      return 0;
    });

    return result;
  }, [subscribers, statusFilter, searchQuery, sortBy]);

  // Pagination calculations
  const totalPages = Math.max(1, Math.ceil(filteredSubscribers.length / ITEMS_PER_PAGE));
  const paginatedSubscribers = useMemo(() => {
    const start = (currentPage - 1) * ITEMS_PER_PAGE;
    return filteredSubscribers.slice(start, start + ITEMS_PER_PAGE);
  }, [filteredSubscribers, currentPage]);

  // Reset page when filter/search changes
  useEffect(() => {
    setCurrentPage(1);
  }, [searchQuery, statusFilter, sortBy]);

  // Actions
  const handleUnsubscribeConfirm = async () => {
    if (!deactivatingSub) return;
    setActionLoading(true);
    setError(null);
    try {
      await fetchAPI(`/api/newsletter/subscribers/${deactivatingSub.id}`, { method: "DELETE" });
      await loadSubscribers();
      setDeactivatingSub(null);
    } catch {
      setError("Failed to deactivate subscriber. Please try again.");
    } finally {
      setActionLoading(false);
    }
  };

  const handleSend = async () => {
    if (!subject.trim() || !content.trim()) return;
    setSending(true);
    setSendError(null);
    try {
      await fetchAPI<Dispatch>("/api/newsletter/send", {
        method: "POST",
        body: JSON.stringify({ subject: subject.trim(), content: content.trim() }),
      });
      setSubject("");
      setContent("");
      setComposeOpen(false);
      setSendSuccessMessage(`Dispatch successfully recorded for ${activeCount} active recipients.`);
      loadHistory();
      setTimeout(() => setSendSuccessMessage(null), 6000);
    } catch {
      setSendError("Failed to record dispatch. Please check the backend connection.");
    } finally {
      setSending(false);
    }
  };

  const exportCsv = () => {
    const rows = [
      ["ID", "Email Address", "Status", "Joined Date"],
      ...filteredSubscribers.map((s) => [
        s.id,
        s.email,
        s.is_active ? "Active" : "Inactive",
        s.created_at ? new Date(s.created_at).toISOString() : "",
      ]),
    ];
    const csvContent = rows
      .map((r) => r.map((v) => `"${String(v).replace(/"/g, '""')}"`).join(","))
      .join("\n");
    const blob = new Blob([csvContent], { type: "text/csv;charset=utf-8;" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = `newsletter-subscribers-${new Date().toISOString().split("T")[0]}.csv`;
    link.click();
    URL.revokeObjectURL(url);
  };

  const applyTemplate = (tmpl: (typeof TEMPLATES)[number]) => {
    setSubject(tmpl.subject);
    setContent(tmpl.content);
  };

  const filteredHistory = useMemo(() => {
    if (!historySearch.trim()) return history;
    const q = historySearch.toLowerCase();
    return history.filter(
      (h) => h.subject.toLowerCase().includes(q) || (h.content && h.content.toLowerCase().includes(q))
    );
  }, [history, historySearch]);

  if (authLoading || !user || loading) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[60vh] gap-3">
        <Loader2 className="h-8 w-8 animate-spin text-emerald-600 dark:text-emerald-400" />
        <p className="text-sm font-medium text-muted-foreground">Loading Newsletter Center...</p>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8 max-w-6xl space-y-8">
      {/* ── Page Header ── */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-2 border-b border-border/40">
        <div className="flex items-center gap-3.5">
          <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 border border-emerald-500/20 shadow-xs">
            <Mail className="h-6 w-6" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h1 className="text-2xl sm:text-3xl font-bold tracking-tight text-foreground">Newsletter Center</h1>
              <Badge variant="outline" className="text-xs bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 border-emerald-500/30">
                LGU Broadcasts
              </Badge>
            </div>
            <p className="text-muted-foreground text-sm mt-0.5">
              Engage subscribers with tourism bulletins, cultural updates, and announcements
            </p>
          </div>
        </div>

        <div className="flex items-center gap-2.5">
          <Button
            variant="outline"
            size="sm"
            onClick={() => loadSubscribers(true)}
            disabled={refreshing}
            className="border-border/60 hover:bg-muted/60 cursor-pointer"
          >
            <RefreshCw className={`h-4 w-4 mr-1.5 ${refreshing ? "animate-spin" : ""}`} />
            Refresh
          </Button>
          <Button
            size="sm"
            onClick={() => {
              setComposeTab("edit");
              setComposeOpen(true);
            }}
            className="bg-emerald-600 hover:bg-emerald-700 text-white shadow-xs cursor-pointer gap-1.5 font-medium"
          >
            <PenSquare className="h-4 w-4" />
            Compose Dispatch
          </Button>
        </div>
      </div>

      {/* ── Alert Messages ── */}
      {error && (
        <div className="p-4 rounded-xl border border-destructive/30 bg-destructive/10 text-destructive flex items-center justify-between gap-3 text-sm">
          <div className="flex items-center gap-2">
            <AlertCircle className="h-4 w-4 shrink-0" />
            <span>{error}</span>
          </div>
          <Button variant="ghost" size="icon-sm" onClick={() => setError(null)} className="h-6 w-6">
            <X className="h-3.5 w-3.5" />
          </Button>
        </div>
      )}

      {sendSuccessMessage && (
        <div className="p-4 rounded-xl border border-emerald-500/30 bg-emerald-500/10 text-emerald-700 dark:text-emerald-300 flex items-center justify-between gap-3 text-sm animate-in fade-in-50">
          <div className="flex items-center gap-2">
            <CheckCircle2 className="h-4 w-4 shrink-0 text-emerald-600 dark:text-emerald-400" />
            <span>{sendSuccessMessage}</span>
          </div>
          <Button variant="ghost" size="icon-sm" onClick={() => setSendSuccessMessage(null)} className="h-6 w-6">
            <X className="h-3.5 w-3.5" />
          </Button>
        </div>
      )}

      {/* ── Metric KPI Cards ── */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
        {/* KPI 1: Active Subscribers */}
        <div className="rounded-2xl border border-border/60 bg-card p-5 shadow-xs hover:border-emerald-500/30 transition-all">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">
              Active Subscribers
            </span>
            <div className="p-2.5 rounded-xl bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 border border-emerald-500/20">
              <MailCheck className="h-5 w-5" />
            </div>
          </div>
          <div className="mt-3 flex items-baseline gap-2">
            <span className="text-3xl font-black tracking-tight text-foreground">{activeCount}</span>
            <span className="text-xs text-muted-foreground font-medium">/ {totalCount} total</span>
          </div>
          <div className="mt-3 flex items-center gap-2">
            <div className="h-1.5 flex-1 rounded-full bg-muted overflow-hidden">
              <div
                className="h-full bg-emerald-500 rounded-full transition-all duration-500"
                style={{ width: `${activePercent}%` }}
              />
            </div>
            <span className="text-[11px] font-semibold text-emerald-600 dark:text-emerald-400">
              {activePercent}% active
            </span>
          </div>
        </div>

        {/* KPI 2: Broadcast Campaigns */}
        <div className="rounded-2xl border border-border/60 bg-card p-5 shadow-xs hover:border-primary/30 transition-all flex flex-col justify-between">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">
              Sent Campaigns
            </span>
            <div className="p-2.5 rounded-xl bg-blue-500/10 text-blue-600 dark:text-blue-400 border border-blue-500/20">
              <Send className="h-5 w-5" />
            </div>
          </div>
          <div className="mt-3 flex items-baseline justify-between">
            <div>
              <span className="text-3xl font-black tracking-tight text-foreground">{history.length}</span>
              <p className="text-xs text-muted-foreground mt-0.5">Total dispatches broadcasted</p>
            </div>
            <Button
              variant="outline"
              size="sm"
              onClick={() => setHistoryOpen(true)}
              className="text-xs h-8 cursor-pointer border-border/60 hover:bg-muted/60"
            >
              <History className="h-3.5 w-3.5 mr-1" />
              View Archive
            </Button>
          </div>
        </div>

        {/* KPI 3: Quick Operations */}
        <div className="rounded-2xl border border-border/60 bg-card p-5 shadow-xs hover:border-emerald-500/30 transition-all flex flex-col justify-between">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">
              Export &amp; Actions
            </span>
            <div className="p-2.5 rounded-xl bg-amber-500/10 text-amber-600 dark:text-amber-400 border border-amber-500/20">
              <Sparkles className="h-5 w-5" />
            </div>
          </div>
          <div className="mt-3 flex items-center gap-2">
            <Button
              variant="outline"
              size="sm"
              onClick={exportCsv}
              disabled={filteredSubscribers.length === 0}
              className="flex-1 text-xs h-9 cursor-pointer border-border/60 hover:bg-muted/60"
            >
              <Download className="h-3.5 w-3.5 mr-1.5" />
              Export CSV ({filteredSubscribers.length})
            </Button>
            <Button
              size="sm"
              onClick={() => {
                setComposeTab("edit");
                setComposeOpen(true);
              }}
              className="flex-1 text-xs h-9 bg-emerald-600 hover:bg-emerald-700 text-white cursor-pointer"
            >
              <SendHorizontal className="h-3.5 w-3.5 mr-1.5" />
              Dispatch
            </Button>
          </div>
        </div>
      </div>

      {/* ── Subscriber Directory Section ── */}
      <div className="rounded-2xl border border-border/60 bg-card shadow-xs overflow-hidden">
        {/* Table Header Bar */}
        <div className="p-5 border-b border-border/50 flex flex-col md:flex-row md:items-center justify-between gap-4 bg-muted/20">
          <div>
            <h2 className="text-lg font-bold tracking-tight text-foreground flex items-center gap-2">
              <Users className="h-5 w-5 text-emerald-600 dark:text-emerald-400" />
              Subscriber Directory
            </h2>
            <p className="text-xs text-muted-foreground mt-0.5">
              Verified recipient roster for municipal updates and newsletters
            </p>
          </div>

          {/* Search and Filters */}
          <div className="flex flex-wrap items-center gap-2.5">
            {/* Search Input */}
            <div className="relative min-w-[220px] sm:min-w-[260px]">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
              <Input
                type="text"
                placeholder="Search email address..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="pl-9 pr-8 h-9 text-xs bg-background/80 border-border/60"
              />
              {searchQuery && (
                <button
                  onClick={() => setSearchQuery("")}
                  className="absolute right-2.5 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground cursor-pointer"
                >
                  <X className="h-3.5 w-3.5" />
                </button>
              )}
            </div>

            {/* Status Filter Buttons */}
            <div className="inline-flex rounded-lg border border-border/60 bg-muted/40 p-0.5 text-xs">
              <button
                onClick={() => setStatusFilter("all")}
                className={`px-3 py-1.5 rounded-md font-medium transition-colors cursor-pointer ${
                  statusFilter === "all"
                    ? "bg-background text-foreground shadow-xs font-semibold"
                    : "text-muted-foreground hover:text-foreground"
                }`}
              >
                All ({totalCount})
              </button>
              <button
                onClick={() => setStatusFilter("active")}
                className={`px-3 py-1.5 rounded-md font-medium transition-colors cursor-pointer ${
                  statusFilter === "active"
                    ? "bg-background text-emerald-600 dark:text-emerald-400 shadow-xs font-semibold"
                    : "text-muted-foreground hover:text-foreground"
                }`}
              >
                Active ({activeCount})
              </button>
              <button
                onClick={() => setStatusFilter("inactive")}
                className={`px-3 py-1.5 rounded-md font-medium transition-colors cursor-pointer ${
                  statusFilter === "inactive"
                    ? "bg-background text-foreground shadow-xs font-semibold"
                    : "text-muted-foreground hover:text-foreground"
                }`}
              >
                Inactive ({inactiveCount})
              </button>
            </div>

            {/* Sort Toggle */}
            <div className="relative">
              <select
                value={sortBy}
                onChange={(e) => setSortBy(e.target.value as any)}
                className="h-9 px-3 rounded-lg border border-border/60 bg-background/80 text-xs text-foreground font-medium appearance-none pr-8 cursor-pointer focus:outline-none focus:ring-1 focus:ring-emerald-500"
              >
                <option value="newest">Newest Joined</option>
                <option value="oldest">Oldest Joined</option>
                <option value="email-asc">Email (A to Z)</option>
                <option value="email-desc">Email (Z to A)</option>
              </select>
              <ArrowUpDown className="absolute right-2.5 top-1/2 -translate-y-1/2 h-3.5 w-3.5 text-muted-foreground pointer-events-none" />
            </div>
          </div>
        </div>

        {/* Subscribers Table */}
        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="border-b border-border/60 bg-muted/40 text-[11px] font-bold uppercase tracking-wider text-muted-foreground">
                <th className="py-3.5 px-6">Subscriber</th>
                <th className="py-3.5 px-6">Status</th>
                <th className="py-3.5 px-6">Joined Date</th>
                <th className="py-3.5 px-6 text-right">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-border/40">
              {paginatedSubscribers.length === 0 ? (
                <tr>
                  <td colSpan={4} className="py-16 text-center">
                    <div className="max-w-sm mx-auto flex flex-col items-center justify-center text-center">
                      <div className="p-4 rounded-full bg-muted/60 text-muted-foreground/60 mb-3">
                        <Mail className="h-8 w-8" />
                      </div>
                      <p className="font-semibold text-foreground text-sm">
                        {searchQuery || statusFilter !== "all"
                          ? "No subscribers match your search"
                          : "No subscribers found yet"}
                      </p>
                      <p className="text-xs text-muted-foreground mt-1">
                        {searchQuery || statusFilter !== "all"
                          ? "Try adjusting your search terms or filter selection."
                          : "Subscribers will appear here once visitors opt in via the public portal."}
                      </p>
                      {(searchQuery || statusFilter !== "all") && (
                        <Button
                          variant="outline"
                          size="sm"
                          onClick={() => {
                            setSearchQuery("");
                            setStatusFilter("all");
                          }}
                          className="mt-4 text-xs h-8 cursor-pointer"
                        >
                          Clear Filters
                        </Button>
                      )}
                    </div>
                  </td>
                </tr>
              ) : (
                paginatedSubscribers.map((sub) => {
                  const initial = sub.email.charAt(0).toUpperCase();
                  return (
                    <tr
                      key={sub.id}
                      className="hover:bg-muted/30 transition-colors group"
                    >
                      {/* Email & Initial Avatar */}
                      <td className="py-3.5 px-6">
                        <div className="flex items-center gap-3">
                          <div className="h-8 w-8 rounded-lg bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 border border-emerald-500/20 flex items-center justify-center font-bold text-xs shrink-0">
                            {initial}
                          </div>
                          <div>
                            <span className="font-medium text-sm text-foreground block">
                              {sub.email}
                            </span>
                            <span className="text-[10px] text-muted-foreground">ID #{sub.id}</span>
                          </div>
                        </div>
                      </td>

                      {/* Status */}
                      <td className="py-3.5 px-6">
                        {sub.is_active ? (
                          <span className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-xs font-semibold bg-emerald-500/10 text-emerald-700 dark:text-emerald-400 border border-emerald-500/20">
                            <span className="h-1.5 w-1.5 rounded-full bg-emerald-500" />
                            Active
                          </span>
                        ) : (
                          <span className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-xs font-medium bg-muted text-muted-foreground border border-border">
                            <span className="h-1.5 w-1.5 rounded-full bg-muted-foreground" />
                            Inactive
                          </span>
                        )}
                      </td>

                      {/* Joined Date */}
                      <td className="py-3.5 px-6 text-xs text-muted-foreground">
                        {sub.created_at
                          ? new Date(sub.created_at).toLocaleDateString(undefined, {
                              year: "numeric",
                              month: "short",
                              day: "numeric",
                            })
                          : "—"}
                      </td>

                      {/* Action */}
                      <td className="py-3.5 px-6 text-right">
                        {sub.is_active ? (
                          <Button
                            variant="ghost"
                            size="sm"
                            onClick={() => setDeactivatingSub(sub)}
                            className="h-8 text-xs text-muted-foreground hover:text-destructive hover:bg-destructive/10 cursor-pointer"
                            title="Deactivate subscriber"
                          >
                            <Trash2 className="h-3.5 w-3.5 mr-1" />
                            Deactivate
                          </Button>
                        ) : (
                          <span className="text-xs text-muted-foreground/60 italic">Deactivated</span>
                        )}
                      </td>
                    </tr>
                  );
                })
              )}
            </tbody>
          </table>
        </div>

        {/* Table Footer / Pagination */}
        {filteredSubscribers.length > 0 && (
          <div className="p-4 border-t border-border/50 flex flex-col sm:flex-row items-center justify-between gap-3 text-xs text-muted-foreground bg-muted/10">
            <div>
              Showing{" "}
              <span className="font-semibold text-foreground">
                {(currentPage - 1) * ITEMS_PER_PAGE + 1}
              </span>{" "}
              to{" "}
              <span className="font-semibold text-foreground">
                {Math.min(currentPage * ITEMS_PER_PAGE, filteredSubscribers.length)}
              </span>{" "}
              of{" "}
              <span className="font-semibold text-foreground">
                {filteredSubscribers.length}
              </span>{" "}
              subscribers
            </div>

            <div className="flex items-center gap-1.5">
              <Button
                variant="outline"
                size="icon-sm"
                onClick={() => setCurrentPage((p) => Math.max(1, p - 1))}
                disabled={currentPage === 1}
                className="h-8 w-8 cursor-pointer"
              >
                <ChevronLeft className="h-4 w-4" />
              </Button>

              <span className="px-2 font-medium">
                Page {currentPage} of {totalPages}
              </span>

              <Button
                variant="outline"
                size="icon-sm"
                onClick={() => setCurrentPage((p) => Math.min(totalPages, p + 1))}
                disabled={currentPage === totalPages}
                className="h-8 w-8 cursor-pointer"
              >
                <ChevronRight className="h-4 w-4" />
              </Button>
            </div>
          </div>
        )}
      </div>

      {/* ── Compose Dispatch Dialog Modal ── */}
      <Dialog open={composeOpen} onOpenChange={setComposeOpen}>
        <DialogContent className="sm:max-w-2xl max-h-[90vh] overflow-y-auto p-0 border border-border/70 rounded-2xl">
          <div className="p-6 border-b border-border/50 bg-muted/20">
            <DialogHeader>
              <div className="flex items-center gap-2.5">
                <div className="p-2 rounded-xl bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 border border-emerald-500/20">
                  <PenSquare className="h-5 w-5" />
                </div>
                <div>
                  <DialogTitle className="text-xl font-bold">Compose Dispatch</DialogTitle>
                  <DialogDescription className="text-xs text-muted-foreground mt-0.5">
                    Send a customized bulletin directly to active newsletter subscribers.
                  </DialogDescription>
                </div>
              </div>
            </DialogHeader>

            {/* Recipient Notice */}
            <div className="mt-4 p-3 rounded-xl bg-emerald-500/10 border border-emerald-500/20 flex items-center justify-between text-xs text-emerald-700 dark:text-emerald-300">
              <div className="flex items-center gap-2">
                <MailCheck className="h-4 w-4 text-emerald-600 dark:text-emerald-400 shrink-0" />
                <span>
                  Will be broadcasted to <strong>{activeCount}</strong> active subscriber(s).
                </span>
              </div>
              <Badge variant="outline" className="text-[10px] bg-background/60 border-emerald-500/30">
                Ready to Send
              </Badge>
            </div>
          </div>

          <div className="p-6 space-y-4">
            {/* Tab switch: Edit / Preview */}
            <div className="flex items-center justify-between">
              <div className="inline-flex rounded-lg border border-border/60 bg-muted/40 p-0.5 text-xs">
                <button
                  type="button"
                  onClick={() => setComposeTab("edit")}
                  className={`px-3 py-1.5 rounded-md font-medium transition-colors cursor-pointer ${
                    composeTab === "edit"
                      ? "bg-background text-foreground shadow-xs font-semibold"
                      : "text-muted-foreground hover:text-foreground"
                  }`}
                >
                  <PenSquare className="h-3.5 w-3.5 inline mr-1" />
                  Editor
                </button>
                <button
                  type="button"
                  onClick={() => setComposeTab("preview")}
                  className={`px-3 py-1.5 rounded-md font-medium transition-colors cursor-pointer ${
                    composeTab === "preview"
                      ? "bg-background text-emerald-600 dark:text-emerald-400 shadow-xs font-semibold"
                      : "text-muted-foreground hover:text-foreground"
                  }`}
                >
                  <Eye className="h-3.5 w-3.5 inline mr-1" />
                  Live Preview
                </button>
              </div>

              {composeTab === "edit" && (
                <div className="flex items-center gap-1.5">
                  <span className="text-[11px] text-muted-foreground">Quick Templates:</span>
                  {TEMPLATES.map((tmpl) => (
                    <button
                      key={tmpl.name}
                      type="button"
                      onClick={() => applyTemplate(tmpl)}
                      className="text-[11px] px-2 py-1 rounded bg-muted hover:bg-muted/80 text-foreground border border-border/60 cursor-pointer transition-colors"
                    >
                      {tmpl.name}
                    </button>
                  ))}
                </div>
              )}
            </div>

            {composeTab === "edit" ? (
              <div className="space-y-4">
                <div>
                  <div className="flex justify-between items-center mb-1.5">
                    <label className="text-xs font-semibold text-foreground">Email Subject</label>
                    <span className="text-[10px] text-muted-foreground">{subject.length} / 200</span>
                  </div>
                  <Input
                    value={subject}
                    onChange={(e) => setSubject(e.target.value)}
                    placeholder="e.g., Discover Mangatarem: Upcoming Cultural Festivities & Eco-Tours"
                    maxLength={200}
                    className="text-sm border-border/60"
                  />
                </div>

                <div>
                  <div className="flex justify-between items-center mb-1.5">
                    <label className="text-xs font-semibold text-foreground">Message Body</label>
                    <span className="text-[10px] text-muted-foreground">{content.length} characters</span>
                  </div>
                  <Textarea
                    value={content}
                    onChange={(e) => setContent(e.target.value)}
                    placeholder="Write your newsletter announcement here. Line breaks and paragraphs will be cleanly formatted..."
                    rows={8}
                    className="text-sm font-sans border-border/60 leading-relaxed"
                  />
                </div>
              </div>
            ) : (
              /* Live Email Preview */
              <div className="rounded-xl border border-border/80 bg-background overflow-hidden shadow-xs">
                <div className="p-3 bg-muted/40 border-b border-border/60 flex items-center justify-between text-xs">
                  <div className="flex items-center gap-2 text-muted-foreground">
                    <span className="font-semibold text-foreground">To:</span> Active Subscribers ({activeCount})
                  </div>
                  <span className="text-[10px] bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 px-2 py-0.5 rounded font-medium border border-emerald-500/20">
                    HTML Simulation
                  </span>
                </div>
                <div className="p-6 bg-card space-y-4">
                  <div className="border-b border-border/40 pb-3">
                    <p className="text-xs uppercase font-bold tracking-wider text-emerald-600 dark:text-emerald-400">
                      Mangatarem Tourism Bulletin
                    </p>
                    <h3 className="text-lg font-bold text-foreground mt-1">
                      {subject.trim() || "No Subject Specified"}
                    </h3>
                  </div>
                  <div className="text-sm text-foreground/90 whitespace-pre-wrap leading-relaxed min-h-[140px]">
                    {content.trim() || (
                      <span className="text-muted-foreground italic">
                        Message body is empty. Type in the editor to see live rendering.
                      </span>
                    )}
                  </div>
                  <div className="border-t border-border/40 pt-4 mt-6 text-center text-[11px] text-muted-foreground">
                    <p>© {new Date().getFullYear()} Municipality of Mangatarem, Pangasinan. All rights reserved.</p>
                    <p className="mt-1">You received this because you subscribed via our cultural tourism portal.</p>
                  </div>
                </div>
              </div>
            )}

            {sendError && (
              <p className="text-xs text-destructive flex items-center gap-1.5">
                <AlertCircle className="h-4 w-4" />
                {sendError}
              </p>
            )}
          </div>

          <DialogFooter className="p-4 border-t border-border/50 bg-muted/10 gap-2 sm:gap-0">
            <Button
              variant="outline"
              onClick={() => setComposeOpen(false)}
              disabled={sending}
              className="cursor-pointer text-xs"
            >
              Cancel
            </Button>
            <Button
              onClick={handleSend}
              disabled={sending || !subject.trim() || !content.trim() || activeCount === 0}
              className="bg-emerald-600 hover:bg-emerald-700 text-white cursor-pointer text-xs font-semibold gap-1.5"
            >
              {sending ? <Loader2 className="h-4 w-4 animate-spin" /> : <Send className="h-4 w-4" />}
              Send Broadcast ({activeCount})
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      {/* ── Dispatch History Modal Dialog ── */}
      <Dialog open={historyOpen} onOpenChange={setHistoryOpen}>
        <DialogContent className="sm:max-w-3xl max-h-[85vh] overflow-y-auto p-0 border border-border/70 rounded-2xl">
          <div className="p-6 border-b border-border/50 bg-muted/20">
            <DialogHeader>
              <div className="flex items-center gap-2.5">
                <div className="p-2 rounded-xl bg-blue-500/10 text-blue-600 dark:text-blue-400 border border-blue-500/20">
                  <History className="h-5 w-5" />
                </div>
                <div>
                  <DialogTitle className="text-xl font-bold">Dispatch History &amp; Archive</DialogTitle>
                  <DialogDescription className="text-xs text-muted-foreground mt-0.5">
                    Browse all past broadcast newsletters and announcements recorded in the system.
                  </DialogDescription>
                </div>
              </div>
            </DialogHeader>

            {/* History Search Bar */}
            <div className="mt-4 relative">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
              <Input
                type="text"
                placeholder="Search dispatches by subject or content..."
                value={historySearch}
                onChange={(e) => setHistorySearch(e.target.value)}
                className="pl-9 text-xs bg-background border-border/60"
              />
            </div>
          </div>

          <div className="p-6">
            {historyLoading ? (
              <div className="flex flex-col items-center justify-center py-12 gap-2 text-muted-foreground">
                <Loader2 className="h-6 w-6 animate-spin text-primary" />
                <p className="text-xs">Loading campaign archive...</p>
              </div>
            ) : filteredHistory.length === 0 ? (
              <div className="text-center py-12 text-muted-foreground">
                <div className="p-3 rounded-full bg-muted/60 text-muted-foreground/60 w-fit mx-auto mb-2">
                  <Send className="h-6 w-6" />
                </div>
                <p className="font-semibold text-sm text-foreground">No dispatches found</p>
                <p className="text-xs mt-1">
                  {historySearch ? "No dispatches match your search query." : "No broadcasts have been sent yet."}
                </p>
              </div>
            ) : (
              <div className="space-y-3">
                {filteredHistory.map((item) => {
                  const isExpanded = expandedDispatchId === item.id;
                  return (
                    <div
                      key={item.id}
                      className="rounded-xl border border-border/60 bg-card p-4 hover:border-border transition-all"
                    >
                      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
                        <div>
                          <h4 className="text-sm font-bold text-foreground">{item.subject}</h4>
                          <div className="flex items-center gap-3 text-[11px] text-muted-foreground mt-1">
                            <span className="inline-flex items-center gap-1 text-emerald-600 dark:text-emerald-400 font-semibold">
                              <Users className="h-3 w-3" /> {item.recipient_count} recipients
                            </span>
                            <span>•</span>
                            <span>
                              {item.sent_at
                                ? new Date(item.sent_at).toLocaleString(undefined, {
                                    year: "numeric",
                                    month: "short",
                                    day: "numeric",
                                    hour: "2-digit",
                                    minute: "2-digit",
                                  })
                                : "—"}
                            </span>
                          </div>
                        </div>

                        <Button
                          variant="ghost"
                          size="sm"
                          onClick={() => setExpandedDispatchId(isExpanded ? null : item.id)}
                          className="text-xs h-8 text-muted-foreground hover:text-foreground cursor-pointer"
                        >
                          {isExpanded ? "Hide Body" : "View Body"}
                        </Button>
                      </div>

                      {isExpanded && (
                        <div className="mt-3 pt-3 border-t border-border/50 text-xs text-foreground/80 whitespace-pre-wrap bg-muted/20 p-3 rounded-lg leading-relaxed">
                          {item.content || <span className="italic text-muted-foreground">No content body</span>}
                        </div>
                      )}
                    </div>
                  );
                })}
              </div>
            )}
          </div>

          <DialogFooter className="p-4 border-t border-border/50 bg-muted/10">
            <Button
              variant="outline"
              onClick={() => setHistoryOpen(false)}
              className="cursor-pointer text-xs"
            >
              Close Archive
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      {/* ── Deactivate Subscriber Confirmation Dialog ── */}
      <Dialog open={!!deactivatingSub} onOpenChange={(open) => !open && setDeactivatingSub(null)}>
        <DialogContent className="sm:max-w-md p-6 border border-border/70 rounded-2xl">
          <DialogHeader>
            <div className="flex items-center gap-2.5">
              <div className="p-2 rounded-xl bg-destructive/10 text-destructive border border-destructive/20">
                <ShieldAlert className="h-5 w-5" />
              </div>
              <div>
                <DialogTitle className="text-base font-bold">Deactivate Subscriber</DialogTitle>
                <DialogDescription className="text-xs text-muted-foreground mt-0.5">
                  Are you sure you want to deactivate this recipient?
                </DialogDescription>
              </div>
            </div>
          </DialogHeader>

          <div className="my-3 p-3 rounded-xl bg-muted/40 border border-border/50 text-xs text-foreground">
            <span className="text-muted-foreground block text-[10px] uppercase font-bold tracking-wider mb-0.5">
              Subscriber Email
            </span>
            <span className="font-semibold text-sm">{deactivatingSub?.email}</span>
          </div>

          <p className="text-xs text-muted-foreground leading-relaxed">
            Deactivated subscribers will no longer receive broadcast emails or announcements until they opt in again.
          </p>

          <DialogFooter className="mt-4 gap-2 sm:gap-0">
            <Button
              variant="outline"
              size="sm"
              onClick={() => setDeactivatingSub(null)}
              disabled={actionLoading}
              className="cursor-pointer text-xs"
            >
              Cancel
            </Button>
            <Button
              variant="destructive"
              size="sm"
              onClick={handleUnsubscribeConfirm}
              disabled={actionLoading}
              className="cursor-pointer text-xs font-semibold gap-1.5"
            >
              {actionLoading ? <Loader2 className="h-3.5 w-3.5 animate-spin" /> : <Trash2 className="h-3.5 w-3.5" />}
              Confirm Deactivate
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  );
}

