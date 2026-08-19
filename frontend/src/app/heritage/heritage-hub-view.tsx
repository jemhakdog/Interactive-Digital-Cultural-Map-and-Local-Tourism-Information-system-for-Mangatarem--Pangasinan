"use client";

import { useState, useMemo } from "react";
import Link from "next/link";
import {
  Landmark,
  TreePine,
  Music,
  Gem,
  Layers,
  Search,
  SlidersHorizontal,
  MapPin,
  Sparkles,
  ArrowRight,
  ShieldCheck,
  Building,
  Check,
  Share2,
  X,
  LayoutGrid,
  List,
  BookOpen,
  Compass,
  FileText,
  Calendar,
  Eye,
  Info,
} from "lucide-react";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button, buttonVariants } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import {
  HeritageItem,
  HERITAGE_TYPES_CONFIG,
  HeritageTypeConfig,
} from "./heritage-types";

interface HeritageHubViewProps {
  initialItems: HeritageItem[];
  typeCounts: Record<string, number>;
}

export function HeritageHubView({
  initialItems,
  typeCounts,
}: HeritageHubViewProps) {
  const [searchQuery, setSearchQuery] = useState("");
  const [selectedType, setSelectedType] = useState<string>("all");
  const [selectedBarangay, setSelectedBarangay] = useState<string>("all");
  const [selectedStatus, setSelectedStatus] = useState<string>("all");
  const [sortBy, setSortBy] = useState<"featured" | "name" | "newest">("featured");
  const [viewMode, setViewMode] = useState<"grid" | "list">("grid");
  const [copiedId, setCopiedId] = useState<number | null>(null);

  // Extract unique barangays
  const availableBarangays = useMemo(() => {
    const bars = new Set<string>();
    initialItems.forEach((item) => {
      if (item.barangay_name) bars.add(item.barangay_name);
    });
    return Array.from(bars).sort();
  }, [initialItems]);

  // Featured Heritage Site (e.g. Manleluag Spring or Municipal Hall or Tupig)
  const featuredItem = useMemo(() => {
    if (initialItems.length === 0) return null;
    const manleluag = initialItems.find((i) =>
      i.name_of_asset.toLowerCase().includes("manleluag")
    );
    const presidencia = initialItems.find((i) =>
      i.name_of_asset.toLowerCase().includes("presidencia") ||
      i.name_of_asset.toLowerCase().includes("municipal hall")
    );
    return manleluag || presidencia || initialItems[0];
  }, [initialItems]);

  // Filtered Heritage Items
  const filteredItems = useMemo(() => {
    return initialItems.filter((item) => {
      // Search query
      if (searchQuery.trim()) {
        const q = searchQuery.toLowerCase();
        const matchName = item.name_of_asset.toLowerCase().includes(q);
        const matchCommon = item.common_name?.toLowerCase().includes(q) || false;
        const matchLoc = item.location_details?.toLowerCase().includes(q) || false;
        const matchBarangay = item.barangay_name?.toLowerCase().includes(q) || false;
        const matchSignificance = item.significance?.toLowerCase().includes(q) || false;
        const matchCategory = item.category?.toLowerCase().includes(q) || false;

        if (
          !matchName &&
          !matchCommon &&
          !matchLoc &&
          !matchBarangay &&
          !matchSignificance &&
          !matchCategory
        ) {
          return false;
        }
      }

      // Type filter
      if (selectedType !== "all" && item.asset_type !== selectedType) {
        return false;
      }

      // Barangay filter
      if (selectedBarangay !== "all" && item.barangay_name !== selectedBarangay) {
        return false;
      }

      // Conservation Status filter
      if (selectedStatus !== "all") {
        if (!item.conservation_status?.toLowerCase().includes(selectedStatus.toLowerCase())) {
          return false;
        }
      }

      return true;
    }).sort((a, b) => {
      if (sortBy === "name") {
        return a.name_of_asset.localeCompare(b.name_of_asset);
      }
      if (sortBy === "newest") {
        return (b.id || 0) - (a.id || 0);
      }
      return 0; // default featured order
    });
  }, [initialItems, searchQuery, selectedType, selectedBarangay, selectedStatus, sortBy]);

  // Copy link helper
  const handleCopyLink = (e: React.MouseEvent, item: HeritageItem) => {
    e.preventDefault();
    e.stopPropagation();
    const url = `${window.location.origin}/heritage/${item.asset_type}/${item.id}`;
    navigator.clipboard.writeText(url);
    setCopiedId(item.id);
    setTimeout(() => setCopiedId(null), 2000);
  };

  const totalRegistered = initialItems.length;

  return (
    <div className="space-y-12">
      {/* ── Category Cards Grid ── */}
      <section>
        <div className="flex flex-col md:flex-row md:items-end justify-between mb-6 gap-4">
          <div>
            <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-primary/10 text-primary text-xs font-semibold mb-2">
              <BookOpen className="h-3.5 w-3.5" />
              <span>Cultural Heritage Registry</span>
            </div>
            <h2 className="text-2xl md:text-3xl font-bold tracking-tight text-foreground">
              Heritage Classifications
            </h2>
            <p className="text-muted-foreground text-sm mt-1">
              Explore documented cultural property cataloged across the municipality of Mangatarem.
            </p>
          </div>
          <div className="text-xs font-semibold text-muted-foreground uppercase tracking-wider">
            {totalRegistered} Assets Profiled
          </div>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-5 gap-4">
          {Object.entries(HERITAGE_TYPES_CONFIG).map(([slug, config]) => {
            const count = typeCounts[slug] || 0;
            const Icon = config.icon;
            const isSelected = selectedType === slug;

            return (
              <div
                key={slug}
                onClick={() => setSelectedType(isSelected ? "all" : slug)}
                className={`group relative rounded-2xl p-5 border transition-all duration-300 cursor-pointer flex flex-col justify-between ${
                  isSelected
                    ? "bg-primary/5 border-primary shadow-md ring-2 ring-primary/20"
                    : "bg-card hover:bg-muted/40 border-border/60 hover:border-primary/40 hover:shadow-sm"
                }`}
              >
                <div>
                  <div className="flex items-center justify-between mb-3">
                    <div
                      className={`h-10 w-10 rounded-xl flex items-center justify-center transition-transform group-hover:scale-110 ${
                        isSelected
                          ? "bg-primary text-primary-foreground"
                          : "bg-muted text-foreground group-hover:bg-primary/10 group-hover:text-primary"
                      }`}
                    >
                      <Icon className="h-5 w-5" />
                    </div>
                    <Badge
                      variant="outline"
                      className="text-[10px] font-semibold tracking-wider"
                    >
                      {config.badgeLabel}
                    </Badge>
                  </div>

                  <h3 className="font-bold text-base text-foreground group-hover:text-primary transition-colors">
                    {config.label}
                  </h3>
                  <p className="text-xs text-muted-foreground mt-1 line-clamp-2 leading-relaxed">
                    {config.shortDesc}
                  </p>
                </div>

                <div className="mt-4 pt-3 border-t border-border/50 flex items-center justify-between text-xs">
                  <span className="font-bold text-foreground">
                    {count} {count === 1 ? "element" : "elements"}
                  </span>
                  <Link
                    href={`/heritage/${slug}`}
                    onClick={(e) => e.stopPropagation()}
                    className="inline-flex items-center gap-1 text-primary font-medium hover:underline"
                  >
                    <span>Browse</span>
                    <ArrowRight className="h-3 w-3" />
                  </Link>
                </div>
              </div>
            );
          })}
        </div>
      </section>

      {/* ── Featured Spotlight Heritage Card ── */}
      {featuredItem && (
        <section>
          <div className="relative rounded-3xl overflow-hidden border border-border/60 bg-card shadow-lg">
            <div className="grid grid-cols-1 lg:grid-cols-12 gap-0">
              {/* Image side */}
              <div className="lg:col-span-6 relative min-h-[300px] lg:min-h-[420px] bg-muted overflow-hidden">
                <img
                  src={
                    featuredItem.image_url ||
                    "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=1200&q=80"
                  }
                  alt={featuredItem.name_of_asset}
                  className="absolute inset-0 w-full h-full object-cover group-hover:scale-105 transition-transform duration-700"
                />
                <div className="absolute inset-0 bg-gradient-to-t from-black/70 via-black/20 to-transparent" />
                <div className="absolute top-4 left-4 flex flex-wrap gap-2">
                  <Badge className="bg-primary text-primary-foreground font-semibold shadow-sm">
                    <Sparkles className="h-3 w-3 mr-1" />
                    Spotlight Heritage
                  </Badge>
                  {featuredItem.category && (
                    <Badge variant="secondary" className="bg-background/90 backdrop-blur-sm text-foreground text-xs">
                      {featuredItem.category}
                    </Badge>
                  )}
                </div>
                <div className="absolute bottom-4 left-4 right-4 text-white">
                  <div className="flex items-center gap-1.5 text-xs text-white/80 mb-1">
                    <MapPin className="h-3.5 w-3.5 text-primary" />
                    <span>{featuredItem.location_details || featuredItem.barangay_name || "Mangatarem, Pangasinan"}</span>
                  </div>
                  <h3 className="text-xl md:text-2xl font-bold leading-tight drop-shadow-sm">
                    {featuredItem.name_of_asset}
                  </h3>
                </div>
              </div>

              {/* Information side */}
              <div className="lg:col-span-6 p-6 md:p-8 flex flex-col justify-between">
                <div className="space-y-4">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <span className="text-xs font-bold uppercase tracking-widest text-primary">
                        {HERITAGE_TYPES_CONFIG[featuredItem.asset_type]?.label || featuredItem.asset_type}
                      </span>
                    </div>
                    {featuredItem.barangay_name && (
                      <Badge variant="outline" className="text-xs">
                        Brgy. {featuredItem.barangay_name}
                      </Badge>
                    )}
                  </div>

                  {featuredItem.common_name && (
                    <p className="text-sm font-medium text-muted-foreground italic">
                      Also known as: &ldquo;{featuredItem.common_name}&rdquo;
                    </p>
                  )}

                  <div className="space-y-2">
                    <h4 className="text-xs font-bold uppercase tracking-wider text-muted-foreground">
                      Cultural Significance
                    </h4>
                    <p className="text-sm md:text-base text-foreground leading-relaxed">
                      {featuredItem.significance || "Documented landmark registered in the Mangatarem Cultural Heritage Inventory."}
                    </p>
                  </div>

                  {featuredItem.ownership_type && (
                    <div className="grid grid-cols-2 gap-3 pt-2 text-xs">
                      <div className="p-2.5 rounded-xl bg-muted/50">
                        <span className="text-muted-foreground block text-[10px] uppercase font-bold">Ownership</span>
                        <span className="font-semibold text-foreground truncate block mt-0.5">{featuredItem.ownership_type}</span>
                      </div>
                      <div className="p-2.5 rounded-xl bg-muted/50">
                        <span className="text-muted-foreground block text-[10px] uppercase font-bold">Conservation</span>
                        <span className="font-semibold text-foreground truncate block mt-0.5">{featuredItem.conservation_status || "Maintained"}</span>
                      </div>
                    </div>
                  )}
                </div>

                <div className="pt-6 mt-6 border-t border-border/60 flex flex-wrap items-center gap-3">
                  <Link
                    href={`/heritage/${featuredItem.asset_type}/${featuredItem.id}`}
                    className={buttonVariants({ variant: "default", size: "default", className: "gap-2 font-semibold" })}
                  >
                    <FileText className="h-4 w-4" />
                    <span>View Profile</span>
                  </Link>

                  {featuredItem.latitude && featuredItem.longitude && (
                    <Link
                      href={`/map?lat=${featuredItem.latitude}&lng=${featuredItem.longitude}&zoom=16`}
                      className={buttonVariants({ variant: "outline", size: "default", className: "gap-2 text-xs" })}
                    >
                      <Compass className="h-3.5 w-3.5 text-primary" />
                      <span>Locate on Map</span>
                    </Link>
                  )}

                  <Button
                    variant="ghost"
                    size="icon"
                    onClick={(e) => handleCopyLink(e, featuredItem)}
                    className="ml-auto text-muted-foreground hover:text-foreground"
                    title="Share link"
                  >
                    {copiedId === featuredItem.id ? (
                      <Check className="h-4 w-4 text-emerald-600" />
                    ) : (
                      <Share2 className="h-4 w-4" />
                    )}
                  </Button>
                </div>
              </div>
            </div>
          </div>
        </section>
      )}

      {/* ── Search & Filter Suite ── */}
      <section className="space-y-6 pt-2">
        <div className="p-4 md:p-6 rounded-2xl bg-card border border-border/60 shadow-sm space-y-4">
          {/* Main search bar */}
          <div className="flex flex-col md:flex-row gap-3">
            <div className="relative flex-1">
              <Search className="absolute left-3.5 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
              <Input
                type="text"
                placeholder="Search by landmark name, common name, lore, or keywords..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="pl-10 h-11 bg-background text-sm"
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

            {/* Barangay selector */}
            <select
              value={selectedBarangay}
              onChange={(e) => setSelectedBarangay(e.target.value)}
              className="h-11 px-3.5 rounded-md border border-input bg-background text-sm focus:outline-none focus:ring-2 focus:ring-primary/20"
            >
              <option value="all">All Barangays ({availableBarangays.length})</option>
              {availableBarangays.map((b) => (
                <option key={b} value={b}>
                  Brgy. {b}
                </option>
              ))}
            </select>

            {/* Sort selector */}
            <select
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value as "featured" | "name" | "newest")}
              className="h-11 px-3.5 rounded-md border border-input bg-background text-sm focus:outline-none focus:ring-2 focus:ring-primary/20"
            >
              <option value="featured">Featured Order</option>
              <option value="name">Name (A to Z)</option>
              <option value="newest">Recently Registered</option>
            </select>

            {/* View mode buttons */}
            <div className="flex items-center border border-input rounded-md p-1 bg-muted/40">
              <button
                onClick={() => setViewMode("grid")}
                className={`p-1.5 rounded ${
                  viewMode === "grid"
                    ? "bg-background text-foreground shadow-xs"
                    : "text-muted-foreground hover:text-foreground"
                }`}
                title="Grid View"
              >
                <LayoutGrid className="h-4 w-4" />
              </button>
              <button
                onClick={() => setViewMode("list")}
                className={`p-1.5 rounded ${
                  viewMode === "list"
                    ? "bg-background text-foreground shadow-xs"
                    : "text-muted-foreground hover:text-foreground"
                }`}
                title="List View"
              >
                <List className="h-4 w-4" />
              </button>
            </div>
          </div>

          {/* Category Filter Pills */}
          <div className="flex flex-wrap items-center gap-2 pt-2 border-t border-border/40">
            <span className="text-xs font-semibold text-muted-foreground mr-1">Classification:</span>
            <button
              onClick={() => setSelectedType("all")}
              className={`px-3 py-1.5 rounded-full text-xs font-semibold transition-colors ${
                selectedType === "all"
                  ? "bg-primary text-primary-foreground shadow-xs"
                  : "bg-muted hover:bg-muted/80 text-muted-foreground hover:text-foreground"
              }`}
            >
              All Assets ({initialItems.length})
            </button>
            {Object.entries(HERITAGE_TYPES_CONFIG).map(([slug, config]) => {
              const count = typeCounts[slug] || 0;
              const isSelected = selectedType === slug;
              const Icon = config.icon;
              return (
                <button
                  key={slug}
                  onClick={() => setSelectedType(slug)}
                  className={`inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs font-semibold transition-colors ${
                    isSelected
                      ? "bg-primary text-primary-foreground shadow-xs"
                      : "bg-muted hover:bg-muted/80 text-muted-foreground hover:text-foreground"
                  }`}
                >
                  <Icon className="h-3 w-3" />
                  <span>{config.label}</span>
                  <span className={`text-[10px] px-1.5 py-0.2 rounded-full ${isSelected ? "bg-primary-foreground/20 text-primary-foreground" : "bg-background/80 text-foreground"}`}>
                    {count}
                  </span>
                </button>
              );
            })}

            {(searchQuery || selectedType !== "all" || selectedBarangay !== "all" || selectedStatus !== "all") && (
              <button
                onClick={() => {
                  setSearchQuery("");
                  setSelectedType("all");
                  setSelectedBarangay("all");
                  setSelectedStatus("all");
                }}
                className="ml-auto text-xs font-medium text-destructive hover:underline flex items-center gap-1"
              >
                <X className="h-3 w-3" />
                Reset Filters
              </button>
            )}
          </div>
        </div>

        {/* Results Header */}
        <div className="flex items-center justify-between text-xs text-muted-foreground">
          <p>
            Showing <strong className="text-foreground">{filteredItems.length}</strong> of{" "}
            <strong className="text-foreground">{initialItems.length}</strong> heritage entries
          </p>
          {selectedType !== "all" && (
            <span className="font-semibold text-primary">
              Filtered by: {HERITAGE_TYPES_CONFIG[selectedType]?.label}
            </span>
          )}
        </div>

        {/* Empty state */}
        {filteredItems.length === 0 && (
          <div className="text-center py-16 px-4 rounded-3xl border-2 border-dashed border-border/80 bg-muted/20">
            <Landmark className="h-12 w-12 mx-auto text-muted-foreground/30 mb-4" />
            <h3 className="text-lg font-bold text-foreground">No heritage records found</h3>
            <p className="text-sm text-muted-foreground max-w-md mx-auto mt-1">
              We couldn&apos;t find any records matching your active filters. Try adjusting your search query or resetting filters.
            </p>
            <Button
              variant="outline"
              onClick={() => {
                setSearchQuery("");
                setSelectedType("all");
                setSelectedBarangay("all");
                setSelectedStatus("all");
              }}
              className="mt-5 text-xs"
            >
              Reset All Filters
            </Button>
          </div>
        )}

        {/* Grid View */}
        {viewMode === "grid" && filteredItems.length > 0 && (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {filteredItems.map((item) => {
              const typeConfig = HERITAGE_TYPES_CONFIG[item.asset_type];
              const Icon = typeConfig?.icon || Landmark;

              return (
                <Card
                  key={item.id}
                  className="group overflow-hidden border-border/60 hover:border-primary/40 hover:shadow-lg transition-all duration-300 flex flex-col justify-between h-full bg-card"
                >
                  <div>
                    {/* Card Header Media */}
                    <div className="aspect-[16/10] bg-muted relative overflow-hidden">
                      {item.image_url ? (
                        <img
                          src={item.image_url}
                          alt={item.name_of_asset}
                          className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
                        />
                      ) : (
                        <div className="w-full h-full flex flex-col items-center justify-center bg-gradient-to-br from-muted/80 to-muted text-muted-foreground/40">
                          <Icon className="h-12 w-12 mb-2" />
                          <span className="text-xs uppercase tracking-wider font-semibold">
                            {typeConfig?.label || "Heritage Site"}
                          </span>
                        </div>
                      )}

                      {/* Top badges */}
                      <div className="absolute top-3 left-3 flex flex-wrap gap-1.5">
                        <Badge className="bg-background/90 backdrop-blur-sm text-foreground text-[10px] font-bold shadow-xs">
                          {typeConfig?.badgeLabel || "Heritage"}
                        </Badge>
                        {item.barangay_name && (
                          <Badge variant="secondary" className="bg-background/80 backdrop-blur-sm text-foreground text-[10px]">
                            {item.barangay_name}
                          </Badge>
                        )}
                      </div>

                      {/* Share button */}
                      <button
                        onClick={(e) => handleCopyLink(e, item)}
                        className="absolute top-3 right-3 h-7 w-7 rounded-full bg-background/80 backdrop-blur-sm flex items-center justify-center text-muted-foreground hover:text-foreground shadow-xs transition-colors"
                        title="Copy link"
                      >
                        {copiedId === item.id ? (
                          <Check className="h-3.5 w-3.5 text-emerald-600" />
                        ) : (
                          <Share2 className="h-3.5 w-3.5" />
                        )}
                      </button>
                    </div>

                    {/* Card Body */}
                    <CardContent className="p-5 space-y-3">
                      <div className="space-y-1">
                        <div className="flex items-center gap-1.5 text-[11px] font-bold text-primary uppercase tracking-wider">
                          <Icon className="h-3 w-3" />
                          <span>{typeConfig?.label || item.asset_type}</span>
                        </div>
                        <h3 className="font-bold text-base text-foreground leading-snug line-clamp-2 group-hover:text-primary transition-colors">
                          {item.name_of_asset}
                        </h3>
                        {item.common_name && (
                          <p className="text-xs text-muted-foreground line-clamp-1 italic">
                            &ldquo;{item.common_name}&rdquo;
                          </p>
                        )}
                      </div>

                      <p className="text-xs text-muted-foreground leading-relaxed line-clamp-3">
                        {item.significance || "Registered cultural property under the Mangatarem Cultural Heritage Registry."}
                      </p>

                      {/* Metadata row */}
                      {item.ownership_type && (
                        <div className="pt-2 border-t border-border/50 flex items-center justify-between text-[11px] text-muted-foreground">
                          <span className="truncate max-w-[200px]">{item.ownership_type}</span>
                          {item.category && (
                            <span className="text-[10px] text-muted-foreground/80">{item.category}</span>
                          )}
                        </div>
                      )}
                    </CardContent>
                  </div>

                  {/* Card Action footer */}
                  <div className="p-5 pt-0">
                    <Link
                      href={`/heritage/${item.asset_type}/${item.id}`}
                      className={buttonVariants({ variant: "outline", size: "default", className: "w-full justify-between group-hover:bg-primary group-hover:text-primary-foreground transition-colors text-xs font-semibold" })}
                    >
                      <span>View Profile</span>
                      <ArrowRight className="h-3.5 w-3.5 group-hover:translate-x-1 transition-transform" />
                    </Link>
                  </div>
                </Card>
              );
            })}
          </div>
        )}

        {/* List View */}
        {viewMode === "list" && filteredItems.length > 0 && (
          <div className="space-y-3">
            {filteredItems.map((item) => {
              const typeConfig = HERITAGE_TYPES_CONFIG[item.asset_type];
              const Icon = typeConfig?.icon || Landmark;

              return (
                <div
                  key={item.id}
                  className="group rounded-2xl border border-border/60 hover:border-primary/40 bg-card p-4 md:p-5 hover:shadow-md transition-all flex flex-col md:flex-row md:items-center justify-between gap-4"
                >
                  <div className="flex items-start gap-4">
                    <div className="h-16 w-16 md:h-20 md:w-20 rounded-xl bg-muted overflow-hidden shrink-0 relative">
                      {item.image_url ? (
                        <img
                          src={item.image_url}
                          alt={item.name_of_asset}
                          className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
                        />
                      ) : (
                        <div className="w-full h-full flex items-center justify-center text-muted-foreground/40">
                          <Icon className="h-8 w-8" />
                        </div>
                      )}
                    </div>

                    <div className="space-y-1">
                      <div className="flex flex-wrap items-center gap-2">
                        <Badge variant="outline" className="text-[10px] font-bold">
                          {typeConfig?.badgeLabel || "Heritage"}
                        </Badge>
                        <span className="text-xs font-bold text-primary uppercase tracking-wider">
                          {typeConfig?.label || item.asset_type}
                        </span>
                        {item.barangay_name && (
                          <span className="text-xs text-muted-foreground">
                            • Brgy. {item.barangay_name}
                          </span>
                        )}
                      </div>

                      <h3 className="font-bold text-base text-foreground group-hover:text-primary transition-colors">
                        {item.name_of_asset}
                      </h3>

                      <p className="text-xs text-muted-foreground line-clamp-1 max-w-2xl">
                        {item.significance || "Official entry in the Mangatarem Cultural Heritage Registry."}
                      </p>
                    </div>
                  </div>

                  <div className="flex items-center gap-2 md:self-center shrink-0">
                    <Link
                      href={`/heritage/${item.asset_type}/${item.id}`}
                      className={buttonVariants({ variant: "default", size: "sm", className: "text-xs gap-1.5 font-semibold" })}
                    >
                      <span>View Profile</span>
                      <ArrowRight className="h-3.5 w-3.5" />
                    </Link>
                    <Button
                      variant="ghost"
                      size="icon"
                      onClick={(e) => handleCopyLink(e, item)}
                      className="text-muted-foreground hover:text-foreground"
                    >
                      {copiedId === item.id ? (
                        <Check className="h-4 w-4 text-emerald-600" />
                      ) : (
                        <Share2 className="h-4 w-4" />
                      )}
                    </Button>
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </section>

      {/* ── Heritage Preservation Information Banner ── */}
      <section className="rounded-3xl p-8 md:p-10 border border-border/60 bg-gradient-to-br from-card via-card to-muted/40 shadow-sm relative overflow-hidden">
        <div className="max-w-3xl space-y-4 relative z-10">
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-primary/10 text-primary text-xs font-bold uppercase tracking-wider">
            <ShieldCheck className="h-3.5 w-3.5" />
            <span>Cultural Heritage Stewardship</span>
          </div>
          <h3 className="text-xl md:text-2xl font-bold text-foreground">
            Preserving Mangatarem&apos;s Living Heritage
          </h3>
          <p className="text-sm text-muted-foreground leading-relaxed">
            The Mangatarem Cultural Heritage Registry is an initiative dedicated to identifying, documenting, and safeguarding our town&apos;s historical sites, natural wonders, and oral traditions for future generations.
          </p>
          <div className="pt-2 flex flex-wrap gap-4 text-xs font-semibold">
            <Link
              href="/map"
              className="inline-flex items-center gap-1.5 text-primary hover:underline"
            >
              <Compass className="h-4 w-4" />
              <span>Explore Interactive Cultural Map</span>
            </Link>
            <span className="text-muted-foreground">•</span>
            <Link
              href="/attractions"
              className="inline-flex items-center gap-1.5 text-primary hover:underline"
            >
              <Landmark className="h-4 w-4" />
              <span>Browse Tourism Attractions</span>
            </Link>
          </div>
        </div>
      </section>
    </div>
  );
}
