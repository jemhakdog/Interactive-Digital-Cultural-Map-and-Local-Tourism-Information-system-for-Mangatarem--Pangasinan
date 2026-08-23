"use client";

import { useMemo, useState, useCallback } from "react";
import Link from "next/link";
import {
  Search,
  MapPin,
  ArrowRight,
  Album,
  LayoutGrid,
  Grid3X3,
  List,
  Building2,
  Trees,
  Wheat,
  Compass,
  ArrowUpDown,
  X,
  Sparkles,
  ChevronRight,
  ExternalLink,
  Share2,
  Check,
  Eye,
  Shuffle,
  Landmark,
  UtensilsCrossed,
  PartyPopper,
  Info,
} from "lucide-react";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogDescription,
} from "@/components/ui/dialog";

export interface BarangayItem {
  name: string;
  district?: "poblacion" | "upland" | "valley";
  tags?: string[];
  category?: string;
  attraction_count?: number;
  image_url?: string;
}

const DISTRICT_FILTERS = [
  { id: "all", label: "All Districts", icon: Compass },
  { id: "poblacion", label: "Poblacion Core", icon: Building2 },
  { id: "upland", label: "Eco & Upland", icon: Trees },
  { id: "valley", label: "Agrarian Valley", icon: Wheat },
] as const;

const THEMATIC_CATEGORIES = [
  { id: "All", label: "All Themes", icon: Sparkles },
  { id: "Nature & Eco", label: "Nature & Eco", icon: Trees },
  { id: "Heritage & History", label: "Heritage & History", icon: Landmark },
  { id: "Agriculture & Food", label: "Agri & Local Food", icon: UtensilsCrossed },
  { id: "Traditions & Fiestas", label: "Traditions & Fiestas", icon: PartyPopper },
] as const;

const SORT_OPTIONS = [
  { id: "az", label: "Name (A–Z)" },
  { id: "za", label: "Name (Z–A)" },
  { id: "attractions", label: "Most Attractions" },
  { id: "district", label: "District Classification" },
] as const;

const QUICK_TAG_SUGGESTIONS = [
  { label: "Poblacion Core", query: "Poblacion" },
  { label: "Daang Kalikasan Corridor", query: "Eco" },
  { label: "Bogtong Cluster", query: "Bogtong" },
  { label: "Dorongan Corridor", query: "Dorongan" },
  { label: "Cabaluyan Valley", query: "Cabaluyan" },
];

const ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ".split("");

// Generative thematic palette styling by district & hash
function getBarangayTheme(name: string, district?: string) {
  if (district === "poblacion") {
    return {
      gradient: "from-amber-500/15 via-orange-500/10 to-amber-600/5",
      border: "border-amber-500/30 hover:border-amber-500/60",
      accent: "text-amber-700 dark:text-amber-400",
      badge: "bg-amber-500/10 text-amber-800 dark:text-amber-300 border-amber-500/20",
      icon: Building2,
      zoneName: "Poblacion Heritage Core",
      desc: "Historic colonial street grid, municipal square, and heritage town center.",
    };
  }
  if (district === "upland") {
    return {
      gradient: "from-emerald-500/15 via-teal-500/10 to-emerald-600/5",
      border: "border-emerald-500/30 hover:border-emerald-500/60",
      accent: "text-emerald-700 dark:text-emerald-400",
      badge: "bg-emerald-500/10 text-emerald-800 dark:text-emerald-300 border-emerald-500/20",
      icon: Trees,
      zoneName: "Upland Eco & Protected Corridor",
      desc: "Mountain foothills, Manleluag Spring protected landscape, and Daang Kalikasan scenic pass.",
    };
  }
  // Valley & plains
  let hash = 0;
  for (let i = 0; i < name.length; i++) {
    hash = (hash << 5) - hash + name.charCodeAt(i);
    hash |= 0;
  }
  const isTeal = Math.abs(hash) % 2 === 0;
  return {
    gradient: isTeal
      ? "from-teal-500/15 via-cyan-500/10 to-primary/5"
      : "from-blue-500/15 via-indigo-500/10 to-sky-500/5",
    border: isTeal
      ? "border-teal-500/30 hover:border-teal-500/60"
      : "border-blue-500/30 hover:border-blue-500/60",
    accent: isTeal
      ? "text-teal-700 dark:text-teal-400"
      : "text-blue-700 dark:text-blue-400",
    badge: isTeal
      ? "bg-teal-500/10 text-teal-800 dark:text-teal-300 border-teal-500/20"
      : "bg-blue-500/10 text-blue-800 dark:text-blue-300 border-blue-500/20",
    icon: Wheat,
    zoneName: "Agrarian Valley Basin",
    desc: "Rich fertile agricultural basin, artisan traditions, and riverfront settlements.",
  };
}

export function BarangayExplorer({ barangays }: { barangays: BarangayItem[] }) {
  const [query, setQuery] = useState("");
  const [category, setCategory] = useState<string>("All");
  const [districtFilter, setDistrictFilter] = useState<"all" | "poblacion" | "upland" | "valley">("all");
  const [activeLetter, setActiveLetter] = useState<string>("ALL");
  const [sortBy, setSortBy] = useState<"az" | "za" | "attractions" | "district">("az");
  const [viewMode, setViewMode] = useState<"grid" | "compact" | "list">("grid");
  
  // Spotlight Quick View Dialog
  const [spotlightBarangay, setSpotlightBarangay] = useState<BarangayItem | null>(null);
  const [copiedName, setCopiedName] = useState<string | null>(null);

  // Alphabet letter availability map
  const letterCounts = useMemo(() => {
    const map = new Map<string, number>();
    barangays.forEach((b) => {
      const firstChar = b.name.trim().charAt(0).toUpperCase();
      if (firstChar >= "A" && firstChar <= "Z") {
        map.set(firstChar, (map.get(firstChar) || 0) + 1);
      }
    });
    return map;
  }, [barangays]);

  // Dynamic district counts
  const districtCounts = useMemo(() => {
    return {
      all: barangays.length,
      poblacion: barangays.filter((b) => b.district === "poblacion").length,
      upland: barangays.filter((b) => b.district === "upland").length,
      valley: barangays.filter((b) => b.district === "valley").length,
    };
  }, [barangays]);

  // Filter and sort items
  const filtered = useMemo(() => {
    const q = query.trim().toLowerCase();

    const list = barangays.filter((b) => {
      // District filter
      if (districtFilter !== "all" && b.district !== districtFilter) return false;

      // Alphabet filter
      if (activeLetter !== "ALL") {
        if (!b.name.trim().toUpperCase().startsWith(activeLetter)) return false;
      }

      // Search query match (name, category, tags)
      if (q) {
        const matchesName = b.name.toLowerCase().includes(q);
        const matchesCategory = b.category?.toLowerCase().includes(q);
        const matchesTags = b.tags?.some((t) => t.toLowerCase().includes(q));
        if (!matchesName && !matchesCategory && !matchesTags) return false;
      }

      // Thematic category filter
      if (category !== "All") {
        const matchesCat = b.category === category || (b.tags ?? []).includes(category);
        if (!matchesCat) return false;
      }

      return true;
    });

    return list.sort((a, b) => {
      if (sortBy === "az") return a.name.localeCompare(b.name);
      if (sortBy === "za") return b.name.localeCompare(a.name);
      if (sortBy === "attractions") return (b.attraction_count ?? 0) - (a.attraction_count ?? 0);
      if (sortBy === "district") return (a.district ?? "").localeCompare(b.district ?? "");
      return 0;
    });
  }, [barangays, query, category, districtFilter, activeLetter, sortBy]);

  const clearAllFilters = useCallback(() => {
    setQuery("");
    setCategory("All");
    setDistrictFilter("all");
    setActiveLetter("ALL");
    setSortBy("az");
  }, []);

  const handleRandomSurprise = useCallback(() => {
    if (barangays.length === 0) return;
    const randomIdx = Math.floor(Math.random() * barangays.length);
    setSpotlightBarangay(barangays[randomIdx]);
  }, [barangays]);

  const handleCopyLink = useCallback((barangayName: string) => {
    if (typeof window !== "undefined") {
      const url = `${window.location.origin}/barangays/${encodeURIComponent(barangayName)}`;
      navigator.clipboard.writeText(url);
      setCopiedName(barangayName);
      setTimeout(() => setCopiedName(null), 2500);
    }
  }, []);

  const hasActiveFilters =
    query.trim() !== "" ||
    category !== "All" ||
    districtFilter !== "all" ||
    activeLetter !== "ALL" ||
    sortBy !== "az";

  return (
    <div className="space-y-8">
      {/* ── Filter & Search Control Hub ── */}
      <div className="bg-card/85 backdrop-blur-md border border-border/80 rounded-3xl p-5 sm:p-7 shadow-xs space-y-6">
        {/* Top Control Bar: Search Input, Random Button, Sort & View Selector */}
        <div className="flex flex-col lg:flex-row gap-4 items-stretch lg:items-center justify-between">
          <div className="relative flex-1">
            <Search className="absolute left-4 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground pointer-events-none" />
            <Input
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Search by barangay name, theme, or heritage tag (e.g., Macarang, Poblacion, Eco)..."
              className="pl-11 pr-10 h-12 rounded-2xl bg-background border-border/80 text-sm focus-visible:ring-primary/30 shadow-xs"
            />
            {query && (
              <button
                type="button"
                onClick={() => setQuery("")}
                className="absolute right-3.5 top-1/2 -translate-y-1/2 p-1 rounded-full text-muted-foreground hover:text-foreground hover:bg-muted transition-colors cursor-pointer"
                title="Clear search"
                aria-label="Clear search query"
              >
                <X className="h-4 w-4" />
              </button>
            )}
          </div>

          <div className="flex flex-wrap items-center gap-3">
            {/* Surprise Random Barangay Button */}
            <Button
              variant="outline"
              size="sm"
              onClick={handleRandomSurprise}
              className="h-12 px-3.5 rounded-2xl border-border/80 bg-background hover:bg-primary/10 hover:text-primary hover:border-primary/40 text-xs font-semibold gap-1.5 transition-all cursor-pointer shrink-0"
              title="Surprise me with a random barangay"
            >
              <Shuffle className="h-3.5 w-3.5" />
              <span>Surprise Me</span>
            </Button>

            {/* Sort Dropdown */}
            <div className="flex items-center gap-1.5 bg-background border border-border/80 rounded-2xl px-3 py-1.5 h-12 shrink-0">
              <ArrowUpDown className="h-4 w-4 text-muted-foreground shrink-0" />
              <select
                value={sortBy}
                onChange={(e) => setSortBy(e.target.value as "az" | "za" | "attractions" | "district")}
                aria-label="Sort barangays"
                className="bg-transparent text-xs font-semibold text-foreground focus:outline-none cursor-pointer pr-1"
              >
                {SORT_OPTIONS.map((opt) => (
                  <option key={opt.id} value={opt.id} className="bg-popover text-popover-foreground">
                    {opt.label}
                  </option>
                ))}
              </select>
            </div>

            {/* 3-Way View Mode Switcher */}
            <div className="flex items-center p-1 bg-muted/70 border border-border/80 rounded-2xl h-12 shrink-0">
              <Button
                variant={viewMode === "grid" ? "secondary" : "ghost"}
                size="sm"
                onClick={() => setViewMode("grid")}
                className={`h-10 px-2.5 rounded-xl gap-1 text-xs font-medium cursor-pointer ${
                  viewMode === "grid" ? "bg-background shadow-xs text-foreground font-semibold" : "text-muted-foreground"
                }`}
                title="Rich Cards Grid"
              >
                <LayoutGrid className="h-4 w-4" />
                <span className="hidden sm:inline">Cards</span>
              </Button>
              <Button
                variant={viewMode === "compact" ? "secondary" : "ghost"}
                size="sm"
                onClick={() => setViewMode("compact")}
                className={`h-10 px-2.5 rounded-xl gap-1 text-xs font-medium cursor-pointer ${
                  viewMode === "compact" ? "bg-background shadow-xs text-foreground font-semibold" : "text-muted-foreground"
                }`}
                title="Compact Tiles"
              >
                <Grid3X3 className="h-4 w-4" />
                <span className="hidden sm:inline">Tiles</span>
              </Button>
              <Button
                variant={viewMode === "list" ? "secondary" : "ghost"}
                size="sm"
                onClick={() => setViewMode("list")}
                className={`h-10 px-2.5 rounded-xl gap-1 text-xs font-medium cursor-pointer ${
                  viewMode === "list" ? "bg-background shadow-xs text-foreground font-semibold" : "text-muted-foreground"
                }`}
                title="Directory List Table"
              >
                <List className="h-4 w-4" />
                <span className="hidden sm:inline">Directory</span>
              </Button>
            </div>
          </div>
        </div>

        {/* Quick Tag Recommendations */}
        <div className="flex items-center gap-2 overflow-x-auto no-scrollbar pt-1 text-xs">
          <span className="text-muted-foreground font-semibold text-[11px] uppercase tracking-wider shrink-0 mr-1">
            Quick Discovery:
          </span>
          {QUICK_TAG_SUGGESTIONS.map((tag) => (
            <button
              key={tag.label}
              type="button"
              onClick={() => setQuery(tag.query)}
              className="inline-flex items-center gap-1 px-3 py-1 rounded-full bg-background border border-border/70 text-muted-foreground hover:border-primary/50 hover:text-primary transition-colors cursor-pointer shrink-0 text-xs font-medium"
            >
              <Sparkles className="h-3 w-3 text-primary/70" />
              <span>{tag.label}</span>
            </button>
          ))}
        </div>

        {/* District & Thematic Category Filters */}
        <div className="flex flex-col xl:flex-row gap-5 items-start xl:items-center justify-between border-t border-border/60 pt-5">
          {/* District Classification Tabs with Live Counts */}
          <div className="flex flex-wrap items-center gap-2">
            <span className="text-xs font-semibold text-muted-foreground uppercase tracking-wider mr-1 hidden sm:inline">
              District:
            </span>
            {DISTRICT_FILTERS.map((df) => {
              const Icon = df.icon;
              const active = districtFilter === df.id;
              const count = districtCounts[df.id];
              return (
                <button
                  key={df.id}
                  type="button"
                  onClick={() => setDistrictFilter(df.id)}
                  className={`inline-flex items-center gap-2 px-3.5 py-1.5 rounded-xl text-xs font-semibold transition-all cursor-pointer ${
                    active
                      ? "bg-primary text-primary-foreground shadow-xs scale-102"
                      : "bg-background border border-border/80 text-muted-foreground hover:border-primary/40 hover:text-foreground"
                  }`}
                >
                  <Icon className="h-3.5 w-3.5" />
                  <span>{df.label}</span>
                  <span
                    className={`text-[10px] px-1.5 py-0.2 rounded-full font-bold ${
                      active
                        ? "bg-primary-foreground/20 text-primary-foreground"
                        : "bg-muted text-muted-foreground"
                    }`}
                  >
                    {count}
                  </span>
                </button>
              );
            })}
          </div>

          {/* Thematic Categories */}
          <div className="flex flex-wrap items-center gap-1.5">
            <span className="text-xs font-semibold text-muted-foreground uppercase tracking-wider mr-1 hidden sm:inline">
              Theme:
            </span>
            {THEMATIC_CATEGORIES.map((tc) => {
              const Icon = tc.icon;
              const active = category === tc.id;
              return (
                <button
                  key={tc.id}
                  type="button"
                  onClick={() => setCategory(tc.id)}
                  className={`inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-xs font-medium transition-all cursor-pointer ${
                    active
                      ? "bg-foreground text-background font-bold shadow-xs"
                      : "bg-background border border-border/80 text-muted-foreground hover:border-primary/40 hover:text-foreground"
                  }`}
                >
                  <Icon className="h-3.5 w-3.5 opacity-80" />
                  <span>{tc.label}</span>
                </button>
              );
            })}
          </div>
        </div>

        {/* Alphabet A-Z Ribbon */}
        <div className="border-t border-border/60 pt-4">
          <div className="flex items-center justify-between gap-1.5 overflow-x-auto pb-1 no-scrollbar text-xs">
            <button
              type="button"
              onClick={() => setActiveLetter("ALL")}
              className={`px-3 py-1.5 rounded-xl font-bold shrink-0 transition-all cursor-pointer ${
                activeLetter === "ALL"
                  ? "bg-primary text-primary-foreground shadow-xs"
                  : "text-muted-foreground hover:text-foreground hover:bg-muted"
              }`}
            >
              ALL ({barangays.length})
            </button>
            {ALPHABET.map((char) => {
              const count = letterCounts.get(char) || 0;
              const hasData = count > 0;
              const isActive = activeLetter === char;
              return (
                <button
                  key={char}
                  type="button"
                  disabled={!hasData}
                  onClick={() => setActiveLetter(char)}
                  title={`${char}: ${count} barangays`}
                  className={`min-w-[32px] h-8 px-1 rounded-lg font-medium flex items-center justify-center gap-0.5 shrink-0 transition-all cursor-pointer ${
                    isActive
                      ? "bg-primary text-primary-foreground font-bold shadow-xs scale-105"
                      : hasData
                      ? "text-foreground hover:bg-muted hover:text-primary font-semibold"
                      : "text-muted-foreground/30 cursor-not-allowed"
                  }`}
                >
                  <span>{char}</span>
                  {hasData && (
                    <span className="text-[9px] opacity-60 font-normal">
                      {count}
                    </span>
                  )}
                </button>
              );
            })}
          </div>
        </div>
      </div>

      {/* ── Active Status & Result Summary Bar ── */}
      <div className="flex flex-wrap items-center justify-between gap-3 px-1">
        <div className="flex items-center gap-2.5">
          <span className="text-sm font-extrabold text-foreground">
            {filtered.length} {filtered.length === 1 ? "Barangay" : "Barangays"} Displayed
          </span>
          {hasActiveFilters && (
            <span className="text-xs text-muted-foreground bg-muted/60 px-2 py-0.5 rounded-md">
              Filtered from {barangays.length} total
            </span>
          )}
        </div>

        {hasActiveFilters && (
          <Button
            variant="ghost"
            size="sm"
            onClick={clearAllFilters}
            className="text-xs text-muted-foreground hover:text-primary h-8 px-2.5 gap-1.5 cursor-pointer rounded-xl"
          >
            <X className="h-3.5 w-3.5" />
            <span>Reset all filters</span>
          </Button>
        )}
      </div>

      {/* ── Content View ── */}
      {filtered.length === 0 ? (
        <div className="text-center py-20 bg-card/60 border border-dashed border-border/80 rounded-3xl p-8 space-y-4 shadow-xs">
          <div className="h-16 w-16 mx-auto rounded-2xl bg-muted/70 flex items-center justify-center text-muted-foreground/60">
            <Album className="h-8 w-8" />
          </div>
          <div className="space-y-1.5 max-w-md mx-auto">
            <h3 className="text-lg font-bold text-foreground">No barangays match your filter criteria</h3>
            <p className="text-xs sm:text-sm text-muted-foreground leading-relaxed">
              We could not find any communities matching &ldquo;{query || activeLetter || category}&rdquo;. Try broadening your keywords or resetting active filters.
            </p>
          </div>
          <Button
            variant="outline"
            size="sm"
            onClick={clearAllFilters}
            className="rounded-xl mt-2 cursor-pointer"
          >
            Reset Filters
          </Button>
        </div>
      ) : viewMode === "grid" ? (
        /* ── Rich Card Grid View ── */
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
          {filtered.map((b) => {
            const theme = getBarangayTheme(b.name, b.district);
            const Icon = theme.icon;

            return (
              <Card
                key={b.name}
                className={`group rounded-3xl border ${theme.border} overflow-hidden hover:shadow-xl hover:shadow-primary/5 transition-all duration-300 flex flex-col bg-card/85 backdrop-blur-xs`}
              >
                {/* Visual Banner Area */}
                <div className="aspect-[16/10] bg-muted/40 relative flex items-center justify-center overflow-hidden border-b border-border/50">
                  {b.image_url ? (
                    // eslint-disable-next-line @next/next/no-img-element
                    <img
                      src={b.image_url}
                      alt={b.name}
                      className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
                      loading="lazy"
                    />
                  ) : (
                    <div
                      className={`w-full h-full bg-gradient-to-br ${theme.gradient} flex flex-col items-center justify-center p-6 text-center transition-transform duration-500 group-hover:scale-105`}
                    >
                      <div className="w-12 h-12 rounded-2xl bg-background/90 backdrop-blur-md shadow-xs flex items-center justify-center mb-2 border border-border/60">
                        <Icon className={`h-6 w-6 ${theme.accent}`} />
                      </div>
                      <span className="text-[11px] font-bold tracking-wider uppercase opacity-85 text-foreground">
                        {theme.zoneName}
                      </span>
                      <span className="text-[10px] text-muted-foreground mt-0.5 line-clamp-1 max-w-[200px]">
                        {theme.desc}
                      </span>
                    </div>
                  )}

                  {/* Top Badges */}
                  <div className="absolute top-3 left-3 right-3 flex items-center justify-between gap-2">
                    <Badge
                      variant="secondary"
                      className="bg-background/90 backdrop-blur-md text-foreground font-semibold text-[10px] uppercase tracking-wider px-2.5 py-0.5 shadow-xs border border-border/70"
                    >
                      {b.tags?.[0] ?? b.category ?? "Discovery"}
                    </Badge>
                    <Badge className={`${theme.badge} border font-bold text-[10px] uppercase tracking-wider px-2 py-0.5 shadow-xs`}>
                      {b.district === "poblacion" ? "Poblacion" : b.district === "upland" ? "Eco Upland" : "Valley"}
                    </Badge>
                  </div>
                </div>

                {/* Card Body */}
                <CardContent className="p-5 flex-1 flex flex-col justify-between space-y-4">
                  <div className="space-y-2">
                    <div className="flex items-center gap-1.5 text-xs text-muted-foreground">
                      <MapPin className="h-3.5 w-3.5 text-primary shrink-0" />
                      <span>Mangatarem, Pangasinan</span>
                    </div>
                    <Link
                      href={`/barangays/${encodeURIComponent(b.name)}`}
                      className="block focus:outline-none"
                    >
                      <h3 className="text-base sm:text-lg font-bold text-foreground group-hover:text-primary transition-colors line-clamp-1">
                        {b.name}
                      </h3>
                    </Link>
                    <p className="text-xs text-muted-foreground line-clamp-2 leading-relaxed">
                      {theme.desc}
                    </p>
                  </div>

                  {/* Quick Action Footer */}
                  <div className="pt-3 border-t border-border/60 flex items-center justify-between text-xs text-muted-foreground gap-2">
                    <div className="flex items-center gap-1.5 font-medium">
                      <Sparkles className="h-3.5 w-3.5 text-amber-500 shrink-0" />
                      <span className="text-xs">{b.attraction_count ?? 0} Spots</span>
                    </div>

                    <div className="flex items-center gap-1">
                      {/* Quick Spotlight Button */}
                      <button
                        type="button"
                        onClick={() => setSpotlightBarangay(b)}
                        className="p-1.5 rounded-lg text-muted-foreground hover:text-foreground hover:bg-muted transition-colors cursor-pointer"
                        title={`Quick view ${b.name}`}
                        aria-label={`Quick view ${b.name}`}
                      >
                        <Eye className="h-4 w-4" />
                      </button>

                      {/* Share Button */}
                      <button
                        type="button"
                        onClick={() => handleCopyLink(b.name)}
                        className="p-1.5 rounded-lg text-muted-foreground hover:text-foreground hover:bg-muted transition-colors cursor-pointer"
                        title={`Copy share link for ${b.name}`}
                        aria-label={`Copy share link for ${b.name}`}
                      >
                        {copiedName === b.name ? (
                          <Check className="h-4 w-4 text-emerald-600 dark:text-emerald-400" />
                        ) : (
                          <Share2 className="h-4 w-4" />
                        )}
                      </button>

                      {/* Full Profile Link */}
                      <Link
                        href={`/barangays/${encodeURIComponent(b.name)}`}
                        className="inline-flex items-center gap-1 font-semibold text-primary pl-1 hover:underline"
                      >
                        <span>Explore</span>
                        <ChevronRight className="h-3.5 w-3.5 group-hover:translate-x-0.5 transition-transform" />
                      </Link>
                    </div>
                  </div>
                </CardContent>
              </Card>
            );
          })}
        </div>
      ) : viewMode === "compact" ? (
        /* ── Compact Modern Tiles View ── */
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
          {filtered.map((b) => {
            const theme = getBarangayTheme(b.name, b.district);
            const Icon = theme.icon;

            return (
              <div
                key={b.name}
                className={`group p-4 rounded-2xl border ${theme.border} bg-card/85 hover:shadow-md transition-all flex flex-col justify-between gap-3`}
              >
                <div className="flex items-start justify-between gap-2">
                  <div className="flex items-center gap-2.5">
                    <div className="w-9 h-9 rounded-xl bg-background border border-border/80 flex items-center justify-center shrink-0">
                      <Icon className={`h-4 w-4 ${theme.accent}`} />
                    </div>
                    <div>
                      <Link
                        href={`/barangays/${encodeURIComponent(b.name)}`}
                        className="font-bold text-sm text-foreground group-hover:text-primary transition-colors line-clamp-1"
                      >
                        {b.name}
                      </Link>
                      <div className="text-[11px] text-muted-foreground flex items-center gap-1">
                        <MapPin className="h-3 w-3 text-primary/70 shrink-0" />
                        <span>{theme.zoneName}</span>
                      </div>
                    </div>
                  </div>

                  <Badge className={`${theme.badge} border text-[9px] font-bold uppercase tracking-wider px-1.5 py-0.2 shrink-0`}>
                    {b.district === "poblacion" ? "Poblacion" : b.district === "upland" ? "Eco" : "Valley"}
                  </Badge>
                </div>

                <div className="flex items-center justify-between border-t border-border/50 pt-2 text-xs">
                  <span className="text-[11px] text-muted-foreground">
                    {b.tags?.[0] ?? b.category ?? "Discovery"}
                  </span>
                  <div className="flex items-center gap-2">
                    <button
                      type="button"
                      onClick={() => setSpotlightBarangay(b)}
                      className="text-xs text-muted-foreground hover:text-foreground cursor-pointer"
                      title="Quick Preview"
                    >
                      <Eye className="h-3.5 w-3.5" />
                    </button>
                    <Link
                      href={`/barangays/${encodeURIComponent(b.name)}`}
                      className="inline-flex items-center gap-1 font-semibold text-primary hover:underline text-xs"
                    >
                      <span>View</span>
                      <ArrowRight className="h-3 w-3" />
                    </Link>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      ) : (
        /* ── Detailed Directory Table List View ── */
        <div className="bg-card/85 border border-border/70 rounded-3xl overflow-hidden shadow-xs divide-y divide-border/60">
          <div className="p-4 bg-muted/50 grid grid-cols-12 text-[11px] font-bold text-muted-foreground uppercase tracking-wider">
            <div className="col-span-6 sm:col-span-4">Barangay Name</div>
            <div className="col-span-3 sm:col-span-3">District Classification</div>
            <div className="hidden sm:block sm:col-span-3">Thematic Tag</div>
            <div className="col-span-3 sm:col-span-2 text-right">Actions</div>
          </div>
          {filtered.map((b) => {
            const theme = getBarangayTheme(b.name, b.district);
            const Icon = theme.icon;

            return (
              <div
                key={b.name}
                className="group p-4 grid grid-cols-12 items-center hover:bg-muted/40 transition-colors text-xs sm:text-sm"
              >
                <div className="col-span-6 sm:col-span-4 flex items-center gap-3">
                  <div className="w-8 h-8 rounded-xl bg-background border border-border/80 flex items-center justify-center shrink-0">
                    <Icon className={`h-4 w-4 ${theme.accent}`} />
                  </div>
                  <div>
                    <Link
                      href={`/barangays/${encodeURIComponent(b.name)}`}
                      className="font-bold text-foreground group-hover:text-primary transition-colors block"
                    >
                      {b.name}
                    </Link>
                    <div className="text-[11px] text-muted-foreground sm:hidden">
                      {b.tags?.[0] ?? b.category ?? "Discovery"}
                    </div>
                  </div>
                </div>

                <div className="col-span-3 sm:col-span-3">
                  <Badge className={`${theme.badge} border text-[10px] font-bold uppercase tracking-wider`}>
                    {theme.zoneName}
                  </Badge>
                </div>

                <div className="hidden sm:block sm:col-span-3 text-muted-foreground text-xs">
                  <div className="flex items-center gap-1.5">
                    <span className="font-medium">{b.tags?.[0] ?? b.category ?? "Discovery"}</span>
                    <span className="text-[11px] text-muted-foreground/70">• {b.attraction_count ?? 0} spots</span>
                  </div>
                </div>

                <div className="col-span-3 sm:col-span-2 flex items-center justify-end gap-2">
                  <button
                    type="button"
                    onClick={() => setSpotlightBarangay(b)}
                    className="p-1.5 rounded-lg text-muted-foreground hover:text-foreground hover:bg-muted transition-colors cursor-pointer hidden sm:inline-flex"
                    title="Quick Preview"
                  >
                    <Eye className="h-3.5 w-3.5" />
                  </button>
                  <Link
                    href={`/barangays/${encodeURIComponent(b.name)}`}
                    className="inline-flex items-center gap-1 text-xs font-semibold text-primary group-hover:translate-x-0.5 transition-transform"
                  >
                    <span>Details</span>
                    <ArrowRight className="h-3.5 w-3.5" />
                  </Link>
                </div>
              </div>
            );
          })}
        </div>
      )}

      {/* ── Spotlight / Quick View Dialog ── */}
      {spotlightBarangay && (
        <Dialog open={!!spotlightBarangay} onOpenChange={(open) => !open && setSpotlightBarangay(null)}>
          <DialogContent className="sm:max-w-lg rounded-3xl p-6 bg-card border-border/80">
            {(() => {
              const theme = getBarangayTheme(spotlightBarangay.name, spotlightBarangay.district);
              const Icon = theme.icon;

              return (
                <div className="space-y-5">
                  <DialogHeader className="space-y-2">
                    <div className="flex items-center gap-2">
                      <Badge className={`${theme.badge} border text-[10px] font-bold uppercase tracking-wider`}>
                        {theme.zoneName}
                      </Badge>
                      <Badge variant="outline" className="text-[10px] font-semibold">
                        {spotlightBarangay.tags?.[0] ?? spotlightBarangay.category ?? "Cultural Heritage"}
                      </Badge>
                    </div>
                    <DialogTitle className="text-2xl font-extrabold text-foreground flex items-center gap-2">
                      <span>{spotlightBarangay.name}</span>
                    </DialogTitle>
                    <DialogDescription className="text-xs text-muted-foreground flex items-center gap-1.5">
                      <MapPin className="h-3.5 w-3.5 text-primary" />
                      <span>Municipality of Mangatarem, Pangasinan, Philippines</span>
                    </DialogDescription>
                  </DialogHeader>

                  {/* Visual Spotlight Backdrop Banner */}
                  <div className={`p-6 rounded-2xl bg-gradient-to-br ${theme.gradient} border border-border/60 flex items-center gap-4`}>
                    <div className="w-14 h-14 rounded-2xl bg-background/90 shadow-sm flex items-center justify-center shrink-0 border border-border/80">
                      <Icon className={`h-7 w-7 ${theme.accent}`} />
                    </div>
                    <div className="space-y-1">
                      <div className="text-xs font-bold text-foreground">
                        {theme.zoneName}
                      </div>
                      <div className="text-xs text-muted-foreground leading-relaxed">
                        {theme.desc}
                      </div>
                    </div>
                  </div>

                  {/* Highlights and Quick Stats */}
                  <div className="grid grid-cols-2 gap-3">
                    <div className="p-3.5 rounded-2xl bg-muted/40 border border-border/60 text-center">
                      <div className="text-xl font-extrabold text-foreground">
                        {spotlightBarangay.attraction_count ?? 0}
                      </div>
                      <div className="text-[11px] font-medium text-muted-foreground uppercase tracking-wider">
                        Heritage Attractions
                      </div>
                    </div>
                    <div className="p-3.5 rounded-2xl bg-muted/40 border border-border/60 text-center">
                      <div className="text-xl font-extrabold text-primary">
                        Mangatarem
                      </div>
                      <div className="text-[11px] font-medium text-muted-foreground uppercase tracking-wider">
                        Jurisdiction
                      </div>
                    </div>
                  </div>

                  {/* Action Shortcuts */}
                  <div className="flex flex-col sm:flex-row items-center gap-2.5 pt-2">
                    <Link
                      href={`/barangays/${encodeURIComponent(spotlightBarangay.name)}`}
                      className="w-full sm:flex-1 inline-flex items-center justify-center gap-2 px-4 py-2.5 rounded-xl bg-primary text-primary-foreground font-semibold text-xs hover:bg-primary/90 transition-all shadow-xs"
                      onClick={() => setSpotlightBarangay(null)}
                    >
                      <span>Full Heritage Profile</span>
                      <ArrowRight className="h-3.5 w-3.5" />
                    </Link>

                    <Link
                      href={`/map?barangay=${encodeURIComponent(spotlightBarangay.name)}`}
                      className="w-full sm:w-auto inline-flex items-center justify-center gap-2 px-4 py-2.5 rounded-xl bg-muted border border-border text-foreground font-semibold text-xs hover:bg-muted/80 transition-all"
                      onClick={() => setSpotlightBarangay(null)}
                    >
                      <Compass className="h-3.5 w-3.5 text-primary" />
                      <span>View on Map</span>
                    </Link>

                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => handleCopyLink(spotlightBarangay.name)}
                      className="w-full sm:w-auto rounded-xl h-9.5 px-3 text-xs gap-1.5 cursor-pointer"
                    >
                      {copiedName === spotlightBarangay.name ? (
                        <>
                          <Check className="h-3.5 w-3.5 text-emerald-600 dark:text-emerald-400" />
                          <span>Link Copied!</span>
                        </>
                      ) : (
                        <>
                          <Share2 className="h-3.5 w-3.5" />
                          <span>Share</span>
                        </>
                      )}
                    </Button>
                  </div>
                </div>
              );
            })()}
          </DialogContent>
        </Dialog>
      )}
    </div>
  );
}
