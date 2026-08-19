"use client";

import { useState, useMemo } from "react";
import Link from "next/link";
import {
  MapPin,
  Star,
  Search,
  Sparkles,
  TreePine,
  Landmark,
  Building,
  Navigation,
  Compass,
  ArrowRight,
  Share2,
  Check,
  Heart,
  SlidersHorizontal,
  LayoutGrid,
  List,
  ShieldCheck,
  Clock,
  Coins,
  Footprints,
  Waves,
  Mountain,
  Eye,
  Info,
  ExternalLink,
  ChevronRight,
  Route,
  X,
} from "lucide-react";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button, buttonVariants } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { AttractionItem } from "./attraction-types";
import { enrichAttraction, CURATED_ATTRACTION_METADATA } from "./attraction-data";
import { CURATED_TRAILS } from "@/components/map/data";

interface AttractionsViewProps {
  initialAttractions: AttractionItem[];
}

// Category filter configuration
const CATEGORY_CONFIG: Record<
  string,
  { label: string; icon: typeof TreePine; color: string; bgClass: string; textClass: string }
> = {
  all: {
    label: "All Attractions",
    icon: Compass,
    color: "text-primary",
    bgClass: "bg-primary/10",
    textClass: "text-primary",
  },
  Nature: {
    label: "Nature & Waterfalls",
    icon: TreePine,
    color: "text-emerald-600 dark:text-emerald-400",
    bgClass: "bg-emerald-500/10 text-emerald-700 dark:text-emerald-300 border-emerald-500/30",
    textClass: "text-emerald-700 dark:text-emerald-300",
  },
  Historical: {
    label: "Historical & Heritage",
    icon: Landmark,
    color: "text-amber-600 dark:text-amber-400",
    bgClass: "bg-amber-500/10 text-amber-700 dark:text-amber-300 border-amber-500/30",
    textClass: "text-amber-700 dark:text-amber-300",
  },
  "Public Space": {
    label: "Public Spaces & Plazas",
    icon: Building,
    color: "text-teal-600 dark:text-teal-400",
    bgClass: "bg-teal-500/10 text-teal-700 dark:text-teal-300 border-teal-500/30",
    textClass: "text-teal-700 dark:text-teal-300",
  },
};

// Popular facility filters
const POPULAR_FACILITIES = [
  "Hot Spring Pools",
  "Trekking Trails",
  "Scenic Viewpoints",
  "Picnic Cottages",
  "Restrooms",
  "Parking Area",
  "Historic Belfry",
];

export function AttractionsView({ initialAttractions }: AttractionsViewProps) {
  const [searchQuery, setSearchQuery] = useState("");
  const [selectedCategory, setSelectedCategory] = useState<string>("all");
  const [selectedBarangay, setSelectedBarangay] = useState<string>("all");
  const [selectedFacility, setSelectedFacility] = useState<string>("all");
  const [selectedDifficulty, setSelectedDifficulty] = useState<string>("all");
  const [sortBy, setSortBy] = useState<"featured" | "rating" | "name" | "barangay">("featured");
  const [viewMode, setViewMode] = useState<"grid" | "list">("grid");
  const [copiedId, setCopiedId] = useState<number | null>(null);
  const [favorites, setFavorites] = useState<number[]>(() => {
    if (typeof window !== "undefined") {
      try {
        const saved = localStorage.getItem("mangatarem_fav_attractions");
        return saved ? JSON.parse(saved) : [];
      } catch {
        return [];
      }
    }
    return [];
  });

  // Enrich attractions with verified local photography and metadata
  const attractions = useMemo(() => {
    const sourceList =
      initialAttractions && initialAttractions.length > 0
        ? initialAttractions
        : (Object.values(CURATED_ATTRACTION_METADATA) as AttractionItem[]);

    return sourceList.map((a) => enrichAttraction(a));
  }, [initialAttractions]);

  // Extract unique barangays
  const availableBarangays = useMemo(() => {
    const set = new Set<string>();
    attractions.forEach((a) => {
      if (a.barangay_name) set.add(a.barangay_name);
    });
    return Array.from(set).sort();
  }, [attractions]);

  // Key metrics
  const metrics = useMemo(() => {
    const total = attractions.length;
    const nature = attractions.filter((a) => a.category === "Nature").length;
    const historical = attractions.filter((a) => a.category === "Historical").length;
    const publicSpaces = attractions.filter((a) => a.category === "Public Space").length;
    const barangayCount = new Set(attractions.map((a) => a.barangay_name).filter(Boolean)).size;

    return { total, nature, historical, publicSpaces, barangayCount };
  }, [attractions]);

  // Spotlight featured attraction (Manleluag or Daang Kalikasan)
  const spotlightAttraction = useMemo(() => {
    return (
      attractions.find((a) => a.id === 1) ||
      attractions.find((a) => a.is_featured) ||
      attractions[0]
    );
  }, [attractions]);

  // Filtered & sorted attractions
  const filteredAttractions = useMemo(() => {
    const q = searchQuery.toLowerCase().trim();

    return attractions
      .filter((item) => {
        // Search filter
        if (q) {
          const matchName = item.name.toLowerCase().includes(q);
          const matchDesc = (item.description || "").toLowerCase().includes(q);
          const matchBrgy = (item.barangay_name || "").toLowerCase().includes(q);
          const matchCat = (item.category || "").toLowerCase().includes(q);
          const matchFacilities = Array.isArray(item.facilities)
            ? item.facilities.some((f) => f.toLowerCase().includes(q))
            : false;
          const matchHighlights = Array.isArray(item.highlights)
            ? item.highlights.some((h) => h.toLowerCase().includes(q))
            : false;

          if (!matchName && !matchDesc && !matchBrgy && !matchCat && !matchFacilities && !matchHighlights) {
            return false;
          }
        }

        // Category filter
        if (selectedCategory !== "all" && item.category !== selectedCategory) {
          return false;
        }

        // Barangay filter
        if (selectedBarangay !== "all" && item.barangay_name !== selectedBarangay) {
          return false;
        }

        // Facility filter
        if (selectedFacility !== "all") {
          const facilities = Array.isArray(item.facilities) ? item.facilities : [];
          if (!facilities.some((f) => f.toLowerCase().includes(selectedFacility.toLowerCase()))) {
            return false;
          }
        }

        // Difficulty filter
        if (selectedDifficulty !== "all" && item.difficulty !== selectedDifficulty) {
          return false;
        }

        return true;
      })
      .sort((a, b) => {
        if (sortBy === "rating") {
          return (b.rating || 0) - (a.rating || 0);
        }
        if (sortBy === "name") {
          return a.name.localeCompare(b.name);
        }
        if (sortBy === "barangay") {
          return (a.barangay_name || "").localeCompare(b.barangay_name || "");
        }
        // Default: featured first, then by ID
        if (a.is_featured && !b.is_featured) return -1;
        if (!a.is_featured && b.is_featured) return 1;
        return a.id - b.id;
      });
  }, [
    attractions,
    searchQuery,
    selectedCategory,
    selectedBarangay,
    selectedFacility,
    selectedDifficulty,
    sortBy,
  ]);

  // Toggle favorite
  const toggleFavorite = (e: React.MouseEvent, id: number) => {
    e.preventDefault();
    e.stopPropagation();
    setFavorites((prev) => {
      const next = prev.includes(id) ? prev.filter((item) => item !== id) : [...prev, id];
      try {
        localStorage.setItem("mangatarem_fav_attractions", JSON.stringify(next));
      } catch {
        // ignore localStorage errors
      }
      return next;
    });
  };

  // Copy link
  const handleCopyLink = (e: React.MouseEvent, id: number) => {
    e.preventDefault();
    e.stopPropagation();
    const url = `${window.location.origin}/attractions/${id}`;
    navigator.clipboard.writeText(url);
    setCopiedId(id);
    setTimeout(() => setCopiedId(null), 2000);
  };

  // Clear all filters
  const resetFilters = () => {
    setSearchQuery("");
    setSelectedCategory("all");
    setSelectedBarangay("all");
    setSelectedFacility("all");
    setSelectedDifficulty("all");
    setSortBy("featured");
  };

  const isFilteringActive =
    searchQuery !== "" ||
    selectedCategory !== "all" ||
    selectedBarangay !== "all" ||
    selectedFacility !== "all" ||
    selectedDifficulty !== "all";

  return (
    <div className="space-y-12">
      {/* ── Spotlight Hero Banner ── */}
      {spotlightAttraction && (
        <section className="relative overflow-hidden rounded-3xl border border-border/60 bg-gradient-to-br from-card via-card/90 to-primary/5 shadow-xl transition-all duration-300">
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-0">
            {/* Image Showcase */}
            <div className="relative lg:col-span-7 aspect-[16/10] lg:aspect-auto min-h-[320px] lg:min-h-[440px] overflow-hidden group">
              <img
                src={spotlightAttraction.image_url || "/img/manleluag_spring.webp"}
                alt={spotlightAttraction.name}
                className="w-full h-full object-cover transition-transform duration-700 group-hover:scale-105"
              />
              <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-black/30 to-transparent lg:hidden" />
              
              {/* Badges on Image */}
              <div className="absolute top-4 left-4 flex flex-wrap items-center gap-2">
                <Badge className="bg-primary text-primary-foreground font-semibold shadow-md gap-1 px-3 py-1 text-xs">
                  <Sparkles className="h-3.5 w-3.5" /> Spotlight Destination
                </Badge>
                {spotlightAttraction.is_verified && (
                  <Badge variant="secondary" className="bg-background/90 backdrop-blur-md text-foreground font-medium text-xs gap-1">
                    <ShieldCheck className="h-3.5 w-3.5 text-primary" /> Verified Landmark
                  </Badge>
                )}
              </div>

              {/* Quick Image Pill Overlay */}
              <div className="absolute bottom-4 left-4 right-4 flex items-center justify-between text-white text-xs lg:hidden">
                <div className="flex items-center gap-1.5 font-medium bg-black/60 backdrop-blur-md px-3 py-1.5 rounded-full">
                  <MapPin className="h-3.5 w-3.5 text-primary" />
                  <span>{spotlightAttraction.barangay_name}, Mangatarem</span>
                </div>
                {spotlightAttraction.rating && (
                  <div className="flex items-center gap-1 font-semibold bg-black/60 backdrop-blur-md px-3 py-1.5 rounded-full text-amber-400">
                    <Star className="h-3.5 w-3.5 fill-amber-400" />
                    <span>{spotlightAttraction.rating.toFixed(1)}</span>
                  </div>
                )}
              </div>
            </div>

            {/* Content & Action Column */}
            <div className="lg:col-span-5 p-6 sm:p-8 lg:p-10 flex flex-col justify-between">
              <div className="space-y-4">
                <div className="hidden lg:flex items-center justify-between gap-2">
                  <div className="flex items-center gap-2">
                    <Badge variant="outline" className="text-primary border-primary/30 bg-primary/5 font-medium text-xs px-2.5 py-0.5">
                      {spotlightAttraction.category}
                    </Badge>
                    <span className="text-xs text-muted-foreground flex items-center gap-1">
                      <MapPin className="h-3 w-3 text-primary" />
                      Brgy. {spotlightAttraction.barangay_name}
                    </span>
                  </div>
                  {spotlightAttraction.rating && (
                    <div className="flex items-center gap-1 text-xs font-semibold text-amber-600 dark:text-amber-400 bg-amber-50 dark:bg-amber-950/40 px-2.5 py-1 rounded-full border border-amber-200/50 dark:border-amber-800/50">
                      <Star className="h-3.5 w-3.5 fill-amber-400 text-amber-400" />
                      <span>{spotlightAttraction.rating.toFixed(1)}</span>
                      <span className="text-muted-foreground">({spotlightAttraction.review_count} reviews)</span>
                    </div>
                  )}
                </div>

                <div>
                  <h2 className="text-2xl sm:text-3xl font-bold tracking-tight text-foreground group-hover:text-primary transition-colors">
                    {spotlightAttraction.name}
                  </h2>
                  <p className="mt-3 text-sm sm:text-base text-muted-foreground line-clamp-3 sm:line-clamp-4 leading-relaxed">
                    {spotlightAttraction.description}
                  </p>
                </div>

                {/* Key Highlights */}
                {spotlightAttraction.highlights && (
                  <div className="space-y-2 pt-2">
                    <p className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">Key Highlights</p>
                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                      {spotlightAttraction.highlights.slice(0, 4).map((h, i) => (
                        <div key={i} className="flex items-start gap-1.5 text-xs text-foreground/90">
                          <Check className="h-3.5 w-3.5 text-primary shrink-0 mt-0.5" />
                          <span className="line-clamp-1">{h}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>

              {/* Actions */}
              <div className="pt-6 mt-6 border-t border-border/50 flex flex-wrap items-center gap-3">
                <Link
                  href={`/attractions/${spotlightAttraction.id}`}
                  className={buttonVariants({ variant: "default", size: "default", className: "flex-1 sm:flex-none shadow-md shadow-primary/10 font-semibold" })}
                >
                  Explore Landmark <ArrowRight className="ml-1.5 h-4 w-4" />
                </Link>

                {spotlightAttraction.latitude && spotlightAttraction.longitude && (
                  <Link
                    href={`/map?highlight=${spotlightAttraction.id}`}
                    className={buttonVariants({ variant: "outline", size: "default", className: "flex-1 sm:flex-none gap-1.5 font-medium" })}
                  >
                    <Navigation className="h-4 w-4 text-primary" /> View on Map
                  </Link>
                )}

                <Button
                  variant="ghost"
                  size="icon"
                  onClick={(e) => handleCopyLink(e, spotlightAttraction.id)}
                  title="Share link"
                  className="rounded-full"
                >
                  {copiedId === spotlightAttraction.id ? (
                    <Check className="h-4 w-4 text-primary" />
                  ) : (
                    <Share2 className="h-4 w-4 text-muted-foreground" />
                  )}
                </Button>
              </div>
            </div>
          </div>
        </section>
      )}

      {/* ── Quick Metrics Ribbon ── */}
      <section className="grid grid-cols-2 sm:grid-cols-4 gap-3 sm:gap-4">
        <Card className="border-border/50 bg-card/60 backdrop-blur-sm p-4 sm:p-5 flex items-center gap-3.5">
          <div className="p-2.5 rounded-xl bg-primary/10 text-primary">
            <Compass className="h-5 w-5" />
          </div>
          <div>
            <div className="text-xl sm:text-2xl font-bold tracking-tight text-foreground">{metrics.total}</div>
            <div className="text-xs text-muted-foreground font-medium">Total Attractions</div>
          </div>
        </Card>

        <Card className="border-border/50 bg-card/60 backdrop-blur-sm p-4 sm:p-5 flex items-center gap-3.5">
          <div className="p-2.5 rounded-xl bg-emerald-500/10 text-emerald-600 dark:text-emerald-400">
            <TreePine className="h-5 w-5" />
          </div>
          <div>
            <div className="text-xl sm:text-2xl font-bold tracking-tight text-foreground">{metrics.nature}</div>
            <div className="text-xs text-muted-foreground font-medium">Nature & Waterfalls</div>
          </div>
        </Card>

        <Card className="border-border/50 bg-card/60 backdrop-blur-sm p-4 sm:p-5 flex items-center gap-3.5">
          <div className="p-2.5 rounded-xl bg-amber-500/10 text-amber-600 dark:text-amber-400">
            <Landmark className="h-5 w-5" />
          </div>
          <div>
            <div className="text-xl sm:text-2xl font-bold tracking-tight text-foreground">{metrics.historical}</div>
            <div className="text-xs text-muted-foreground font-medium">Historic Sites</div>
          </div>
        </Card>

        <Card className="border-border/50 bg-card/60 backdrop-blur-sm p-4 sm:p-5 flex items-center gap-3.5">
          <div className="p-2.5 rounded-xl bg-teal-500/10 text-teal-600 dark:text-teal-400">
            <MapPin className="h-5 w-5" />
          </div>
          <div>
            <div className="text-xl sm:text-2xl font-bold tracking-tight text-foreground">{metrics.barangayCount}</div>
            <div className="text-xs text-muted-foreground font-medium">Barangays Covered</div>
          </div>
        </Card>
      </section>

      {/* ── Interactive Filter & Search Hub ── */}
      <section className="space-y-6">
        {/* Category Pills Row */}
        <div className="flex items-center gap-2 overflow-x-auto pb-2 scrollbar-none">
          {Object.entries(CATEGORY_CONFIG).map(([key, config]) => {
            const Icon = config.icon;
            const isSelected = selectedCategory === key;
            const count =
              key === "all"
                ? attractions.length
                : attractions.filter((a) => a.category === key).length;

            return (
              <button
                key={key}
                onClick={() => setSelectedCategory(key)}
                className={`flex items-center gap-2 px-4 py-2.5 rounded-xl text-xs sm:text-sm font-medium transition-all whitespace-nowrap border ${
                  isSelected
                    ? "bg-primary text-primary-foreground border-primary shadow-sm"
                    : "bg-card hover:bg-muted text-muted-foreground hover:text-foreground border-border/60"
                }`}
              >
                <Icon className={`h-4 w-4 ${isSelected ? "text-primary-foreground" : config.color}`} />
                <span>{config.label}</span>
                <span
                  className={`text-[11px] px-1.5 py-0.5 rounded-full font-bold ${
                    isSelected
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

        {/* Filter Controls Bar */}
        <div className="bg-card border border-border/60 rounded-2xl p-4 shadow-sm space-y-4">
          <div className="flex flex-col md:flex-row items-center gap-3">
            {/* Search Input */}
            <div className="relative w-full md:flex-1">
              <Search className="absolute left-3.5 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
              <Input
                type="text"
                placeholder="Search attractions, waterfalls, hot springs, facilities..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="pl-9 pr-8 bg-background h-10 rounded-xl"
              />
              {searchQuery && (
                <button
                  onClick={() => setSearchQuery("")}
                  className="absolute right-3 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground"
                >
                  <X className="h-4 w-4" />
                </button>
              )}
            </div>

            {/* Barangay Select */}
            <div className="w-full md:w-48">
              <select
                value={selectedBarangay}
                onChange={(e) => setSelectedBarangay(e.target.value)}
                className="w-full h-10 px-3 rounded-xl border border-input bg-background text-xs sm:text-sm font-medium focus:outline-none focus:ring-2 focus:ring-primary"
              >
                <option value="all">All Barangays</option>
                {availableBarangays.map((b) => (
                  <option key={b} value={b}>
                    Brgy. {b}
                  </option>
                ))}
              </select>
            </div>

            {/* Sort Select */}
            <div className="w-full md:w-44">
              <select
                value={sortBy}
                onChange={(e) => setSortBy(e.target.value as typeof sortBy)}
                className="w-full h-10 px-3 rounded-xl border border-input bg-background text-xs sm:text-sm font-medium focus:outline-none focus:ring-2 focus:ring-primary"
              >
                <option value="featured">Featured First</option>
                <option value="rating">Highest Rated</option>
                <option value="name">Name (A-Z)</option>
                <option value="barangay">By Barangay</option>
              </select>
            </div>

            {/* View Mode Toggle */}
            <div className="flex items-center gap-1 border border-border/60 rounded-xl p-1 bg-muted/40 self-end md:self-auto">
              <Button
                variant={viewMode === "grid" ? "default" : "ghost"}
                size="sm"
                onClick={() => setViewMode("grid")}
                className="h-8 px-2.5 rounded-lg"
                title="Grid view"
              >
                <LayoutGrid className="h-4 w-4" />
              </Button>
              <Button
                variant={viewMode === "list" ? "default" : "ghost"}
                size="sm"
                onClick={() => setViewMode("list")}
                className="h-8 px-2.5 rounded-lg"
                title="List view"
              >
                <List className="h-4 w-4" />
              </Button>
            </div>
          </div>

          {/* Quick Facility Tags & Reset Bar */}
          <div className="flex flex-wrap items-center justify-between gap-2 pt-2 border-t border-border/40 text-xs">
            <div className="flex flex-wrap items-center gap-1.5">
              <span className="text-muted-foreground font-medium mr-1 flex items-center gap-1">
                <SlidersHorizontal className="h-3 w-3" /> Quick Filter:
              </span>
              <button
                onClick={() => setSelectedFacility("all")}
                className={`px-2.5 py-1 rounded-lg transition-colors ${
                  selectedFacility === "all"
                    ? "bg-secondary text-secondary-foreground font-semibold"
                    : "text-muted-foreground hover:text-foreground hover:bg-muted"
                }`}
              >
                Any Facility
              </button>
              {POPULAR_FACILITIES.map((facility) => (
                <button
                  key={facility}
                  onClick={() => setSelectedFacility(selectedFacility === facility ? "all" : facility)}
                  className={`px-2.5 py-1 rounded-lg transition-colors ${
                    selectedFacility === facility
                      ? "bg-primary text-primary-foreground font-semibold"
                      : "text-muted-foreground hover:text-foreground hover:bg-muted"
                  }`}
                >
                  {facility}
                </button>
              ))}
            </div>

            {/* Results counter & Reset */}
            <div className="flex items-center gap-2">
              <span className="text-muted-foreground">
                Showing <strong className="text-foreground">{filteredAttractions.length}</strong> of {attractions.length}
              </span>
              {isFilteringActive && (
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={resetFilters}
                  className="h-7 text-xs text-destructive hover:text-destructive hover:bg-destructive/10 px-2"
                >
                  Reset
                </Button>
              )}
            </div>
          </div>
        </div>
      </section>

      {/* ── Attractions Results (Grid vs List) ── */}
      <section>
        {filteredAttractions.length === 0 ? (
          <div className="text-center py-20 border border-dashed border-border rounded-3xl p-8 bg-card/40">
            <div className="h-16 w-16 mx-auto mb-4 rounded-2xl bg-muted/60 flex items-center justify-center text-muted-foreground">
              <MapPin className="h-8 w-8 opacity-40" />
            </div>
            <h3 className="text-lg font-semibold text-foreground">No attractions match your criteria</h3>
            <p className="text-sm text-muted-foreground mt-1 max-w-md mx-auto">
              Try adjusting your search query, clearing specific facilities, or browsing other barangays.
            </p>
            <Button onClick={resetFilters} variant="outline" className="mt-5 rounded-xl">
              Clear All Filters
            </Button>
          </div>
        ) : viewMode === "grid" ? (
          /* ── Grid View ── */
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {filteredAttractions.map((a) => {
              const isFav = favorites.includes(a.id);

              return (
                <Card
                  key={a.id}
                  className="group overflow-hidden border-border/60 hover:border-primary/40 hover:shadow-xl hover:shadow-primary/5 transition-all duration-300 hover:-translate-y-1 flex flex-col h-full bg-card rounded-2xl"
                >
                  {/* Card Media Header */}
                  <div className="aspect-[16/10] bg-muted relative overflow-hidden">
                    <img
                      src={a.image_url || "/img/mangatarem_map_teaser.webp"}
                      alt={a.name}
                      className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
                    />
                    <div className="absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-black/30" />

                    {/* Top Badges */}
                    <div className="absolute top-3 left-3 right-3 flex items-center justify-between">
                      <div className="flex items-center gap-1.5">
                        <Badge
                          variant="secondary"
                          className="bg-background/90 backdrop-blur-md text-foreground font-semibold text-xs border border-border/40 shadow-sm"
                        >
                          {a.category}
                        </Badge>
                        {a.is_featured && (
                          <Badge className="bg-amber-500 text-white font-bold text-[10px] px-1.5 py-0.5 gap-0.5 shadow-sm">
                            <Star className="h-3 w-3 fill-current" /> Featured
                          </Badge>
                        )}
                      </div>

                      {/* Favorite Button */}
                      <button
                        onClick={(e) => toggleFavorite(e, a.id)}
                        className={`p-2 rounded-full backdrop-blur-md transition-transform active:scale-90 ${
                          isFav
                            ? "bg-rose-500 text-white shadow-md"
                            : "bg-black/40 text-white/80 hover:text-white hover:bg-black/60"
                        }`}
                        title={isFav ? "Remove from wishlist" : "Save to wishlist"}
                      >
                        <Heart className={`h-3.5 w-3.5 ${isFav ? "fill-current" : ""}`} />
                      </button>
                    </div>

                    {/* Bottom Image Overlay Info */}
                    <div className="absolute bottom-3 left-3 right-3 flex items-center justify-between text-white text-xs">
                      <div className="flex items-center gap-1 font-medium bg-black/60 backdrop-blur-md px-2.5 py-1 rounded-full">
                        <MapPin className="h-3 w-3 text-primary" />
                        <span>Brgy. {a.barangay_name}</span>
                      </div>
                      {a.rating && (
                        <div className="flex items-center gap-1 font-semibold bg-black/60 backdrop-blur-md px-2.5 py-1 rounded-full text-amber-300">
                          <Star className="h-3 w-3 fill-amber-300" />
                          <span>{a.rating.toFixed(1)}</span>
                        </div>
                      )}
                    </div>
                  </div>

                  {/* Card Content Body */}
                  <CardContent className="p-5 flex-1 flex flex-col justify-between space-y-4">
                    <div className="space-y-2">
                      <div className="flex items-start justify-between gap-2">
                        <h3 className="font-bold text-lg text-foreground group-hover:text-primary transition-colors line-clamp-1">
                          <Link href={`/attractions/${a.id}`}>{a.name}</Link>
                        </h3>
                      </div>

                      <p className="text-xs sm:text-sm text-muted-foreground line-clamp-2 leading-relaxed">
                        {a.description}
                      </p>

                      {/* Facilities Chips */}
                      {Array.isArray(a.facilities) && a.facilities.length > 0 && (
                        <div className="flex flex-wrap gap-1 pt-1">
                          {a.facilities.slice(0, 3).map((f, i) => (
                            <span
                              key={i}
                              className="text-[11px] px-2 py-0.5 rounded-md bg-muted text-muted-foreground font-medium"
                            >
                              {f}
                            </span>
                          ))}
                          {a.facilities.length > 3 && (
                            <span className="text-[11px] px-1.5 py-0.5 rounded-md bg-muted text-muted-foreground font-medium">
                              +{a.facilities.length - 3}
                            </span>
                          )}
                        </div>
                      )}
                    </div>

                    {/* Card Actions Footer */}
                    <div className="pt-3 border-t border-border/50 flex items-center justify-between gap-2">
                      <Link
                        href={`/attractions/${a.id}`}
                        className={buttonVariants({ variant: "default", size: "sm", className: "flex-1 rounded-xl text-xs font-semibold" })}
                      >
                        View Details <ArrowRight className="ml-1 h-3.5 w-3.5" />
                      </Link>

                      {a.latitude && a.longitude && (
                        <Link
                          href={`/map?highlight=${a.id}`}
                          className={buttonVariants({ variant: "outline", size: "sm", className: "px-2.5 rounded-xl" })}
                          title="View on map"
                        >
                          <Navigation className="h-3.5 w-3.5 text-primary" />
                        </Link>
                      )}

                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={(e) => handleCopyLink(e, a.id)}
                        className="px-2.5 rounded-xl"
                        title="Share link"
                      >
                        {copiedId === a.id ? (
                          <Check className="h-3.5 w-3.5 text-primary" />
                        ) : (
                          <Share2 className="h-3.5 w-3.5 text-muted-foreground" />
                        )}
                      </Button>
                    </div>
                  </CardContent>
                </Card>
              );
            })}
          </div>
        ) : (
          /* ── List View ── */
          <div className="space-y-4">
            {filteredAttractions.map((a) => {
              const isFav = favorites.includes(a.id);

              return (
                <Card
                  key={a.id}
                  className="group overflow-hidden border-border/60 hover:border-primary/40 hover:shadow-lg transition-all duration-200 bg-card rounded-2xl"
                >
                  <div className="grid grid-cols-1 md:grid-cols-12 gap-0">
                    {/* Left Image */}
                    <div className="md:col-span-4 aspect-[16/10] md:aspect-auto min-h-[200px] relative overflow-hidden bg-muted">
                      <img
                        src={a.image_url || "/img/mangatarem_map_teaser.webp"}
                        alt={a.name}
                        className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
                      />
                      <div className="absolute top-3 left-3 flex gap-1.5">
                        <Badge variant="secondary" className="bg-background/90 backdrop-blur-md text-xs font-semibold">
                          {a.category}
                        </Badge>
                        {a.is_featured && (
                          <Badge className="bg-amber-500 text-white font-bold text-[10px]">
                            ★ Featured
                          </Badge>
                        )}
                      </div>
                    </div>

                    {/* Right Content */}
                    <div className="md:col-span-8 p-5 flex flex-col justify-between space-y-4">
                      <div className="space-y-2">
                        <div className="flex flex-wrap items-center justify-between gap-2">
                          <div className="flex items-center gap-2">
                            <h3 className="font-bold text-lg text-foreground group-hover:text-primary transition-colors">
                              <Link href={`/attractions/${a.id}`}>{a.name}</Link>
                            </h3>
                            {a.is_verified && (
                              <span title="Verified landmark">
                                <ShieldCheck className="h-4 w-4 text-primary shrink-0" />
                              </span>
                            )}
                          </div>

                          <div className="flex items-center gap-2">
                            {a.rating && (
                              <div className="flex items-center gap-1 text-xs font-semibold text-amber-600 dark:text-amber-400 bg-amber-50 dark:bg-amber-950/40 px-2 py-0.5 rounded-full border border-amber-200/40">
                                <Star className="h-3 w-3 fill-amber-400 text-amber-400" />
                                <span>{a.rating.toFixed(1)}</span>
                              </div>
                            )}
                            <button
                              onClick={(e) => toggleFavorite(e, a.id)}
                              className={`p-1.5 rounded-full border transition-colors ${
                                isFav
                                  ? "bg-rose-50 border-rose-200 text-rose-500 dark:bg-rose-950/30"
                                  : "border-border/60 text-muted-foreground hover:text-foreground"
                              }`}
                            >
                              <Heart className={`h-3.5 w-3.5 ${isFav ? "fill-current" : ""}`} />
                            </button>
                          </div>
                        </div>

                        <div className="flex items-center gap-2 text-xs text-muted-foreground">
                          <span className="flex items-center gap-1">
                            <MapPin className="h-3 w-3 text-primary" /> Brgy. {a.barangay_name}
                          </span>
                          <span>•</span>
                          <span>{a.entrance_fee || "Free Entry"}</span>
                          <span>•</span>
                          <span>{a.opening_hours || "Open Daily"}</span>
                        </div>

                        <p className="text-sm text-muted-foreground line-clamp-2 leading-relaxed">
                          {a.description}
                        </p>

                        {/* Facilities tags */}
                        {Array.isArray(a.facilities) && (
                          <div className="flex flex-wrap gap-1.5 pt-1">
                            {a.facilities.map((f, i) => (
                              <span
                                key={i}
                                className="text-[11px] px-2.5 py-0.5 rounded-md bg-muted text-muted-foreground font-medium"
                              >
                                {f}
                              </span>
                            ))}
                          </div>
                        )}
                      </div>

                      {/* Bottom Action Row */}
                      <div className="pt-3 border-t border-border/40 flex items-center justify-between gap-3">
                        <div className="text-xs text-muted-foreground">
                          Difficulty: <strong className="text-foreground">{a.difficulty || "Easy"}</strong>
                        </div>

                        <div className="flex items-center gap-2">
                          {a.latitude && a.longitude && (
                            <Link
                              href={`/map?highlight=${a.id}`}
                              className={buttonVariants({ variant: "outline", size: "sm", className: "rounded-xl gap-1 text-xs" })}
                            >
                              <Navigation className="h-3.5 w-3.5 text-primary" /> Map
                            </Link>
                          )}
                          <Link
                            href={`/attractions/${a.id}`}
                            className={buttonVariants({ variant: "default", size: "sm", className: "rounded-xl text-xs font-semibold" })}
                          >
                            Explore <ArrowRight className="ml-1 h-3.5 w-3.5" />
                          </Link>
                        </div>
                      </div>
                    </div>
                  </div>
                </Card>
              );
            })}
          </div>
        )}
      </section>

      {/* ── Curated Tour Routes & Trails Section ── */}
      <section className="space-y-6 pt-4">
        <div className="flex flex-col sm:flex-row sm:items-end justify-between gap-4">
          <div>
            <div className="flex items-center gap-2 mb-1">
              <Route className="h-5 w-5 text-primary" />
              <span className="text-xs font-bold uppercase tracking-wider text-primary">Curated Itineraries</span>
            </div>
            <h2 className="text-2xl sm:text-3xl font-bold tracking-tight text-foreground">
              Recommended Tourism Trails
            </h2>
            <p className="text-muted-foreground text-sm mt-1">
              Ready-made exploration routes connecting Mangatarem&apos;s top natural landscapes and heritage sites.
            </p>
          </div>
          <Link
            href="/map"
            className={buttonVariants({ variant: "outline", size: "default", className: "rounded-xl gap-1.5 shrink-0" })}
          >
            <Compass className="h-4 w-4 text-primary" /> Open Interactive Map
          </Link>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {CURATED_TRAILS.map((trail) => (
            <Card
              key={trail.id}
              className="border-border/60 hover:border-primary/40 hover:shadow-lg transition-all duration-300 flex flex-col justify-between bg-card rounded-2xl p-5 space-y-4"
            >
              <div className="space-y-3">
                <div className="flex items-center justify-between">
                  <Badge variant="outline" className="text-xs font-semibold" style={{ color: trail.color, borderColor: `${trail.color}40` }}>
                    {trail.category}
                  </Badge>
                  <span className="text-xs text-muted-foreground font-medium">{trail.durationEst}</span>
                </div>

                <div>
                  <h3 className="font-bold text-lg text-foreground">{trail.title}</h3>
                  <p className="text-xs text-primary font-medium mt-0.5">{trail.subtitle}</p>
                </div>

                <p className="text-xs text-muted-foreground line-clamp-3 leading-relaxed">
                  {trail.description}
                </p>

                {/* Trail Stops Timeline Preview */}
                <div className="space-y-1.5 pt-2 border-t border-border/40">
                  <p className="text-[11px] font-bold uppercase tracking-wider text-muted-foreground">Itinerary Stops</p>
                  <div className="space-y-1">
                    {trail.stops.map((s, i) => (
                      <div key={i} className="flex items-center gap-2 text-xs text-foreground/90">
                        <span
                          className="h-4 w-4 rounded-full flex items-center justify-center text-[10px] font-bold text-white shrink-0"
                          style={{ backgroundColor: trail.color }}
                        >
                          {s.order}
                        </span>
                        <span className="font-medium line-clamp-1">{s.name}</span>
                        <span className="text-[11px] text-muted-foreground ml-auto shrink-0">{s.barangay}</span>
                      </div>
                    ))}
                  </div>
                </div>
              </div>

              <div className="pt-3 border-t border-border/40 flex items-center justify-between gap-2">
                <span className="text-xs text-muted-foreground font-medium">
                  {trail.distanceKm} km • {trail.difficulty}
                </span>
                <Link
                  href={`/map?trail=${trail.id}`}
                  className={buttonVariants({ variant: "secondary", size: "sm", className: "rounded-xl gap-1 text-xs" })}
                >
                  View Trail <ChevronRight className="h-3.5 w-3.5" />
                </Link>
              </div>
            </Card>
          ))}
        </div>
      </section>

      {/* ── Eco-Tourism Guidelines & Community Notice ── */}
      <section className="rounded-3xl border border-border/60 bg-gradient-to-r from-emerald-950/10 via-card to-primary/5 p-6 sm:p-8">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-center">
          <div className="lg:col-span-8 space-y-3">
            <div className="flex items-center gap-2">
              <ShieldCheck className="h-5 w-5 text-emerald-600 dark:text-emerald-400" />
              <span className="text-xs font-bold uppercase tracking-wider text-emerald-600 dark:text-emerald-400">
                Responsible Eco-Tourism
              </span>
            </div>
            <h3 className="text-xl sm:text-2xl font-bold tracking-tight text-foreground">
              Preserving Mangatarem&apos;s Natural Wonders Together
            </h3>
            <p className="text-sm text-muted-foreground leading-relaxed">
              Help us protect the fragile biodiversity of Manleluag Spring, the pristine falls of Timmanguyob, and our mountain highways. Please practice Clean As You Go (CLAYGO), avoid single-use plastics, stay on marked footpaths, and support local barangay guides and merchants.
            </p>
            <div className="flex flex-wrap items-center gap-4 pt-2 text-xs text-muted-foreground">
              <span className="flex items-center gap-1.5 font-medium text-foreground">
                <Check className="h-4 w-4 text-emerald-500" /> Leave No Trace
              </span>
              <span className="flex items-center gap-1.5 font-medium text-foreground">
                <Check className="h-4 w-4 text-emerald-500" /> Support Local Guides
              </span>
              <span className="flex items-center gap-1.5 font-medium text-foreground">
                <Check className="h-4 w-4 text-emerald-500" /> Protect Wildlife Habitats
              </span>
            </div>
          </div>

          <div className="lg:col-span-4 flex flex-col sm:flex-row lg:flex-col gap-3 justify-center">
            <Link
              href="/business?type=inn"
              className={buttonVariants({ variant: "default", size: "default", className: "rounded-xl shadow-md font-semibold" })}
            >
              Find Local Inns & Dining
            </Link>
            <Link
              href="/events"
              className={buttonVariants({ variant: "outline", size: "default", className: "rounded-xl font-medium" })}
            >
              Upcoming Cultural Events
            </Link>
          </div>
        </div>
      </section>
    </div>
  );
}
