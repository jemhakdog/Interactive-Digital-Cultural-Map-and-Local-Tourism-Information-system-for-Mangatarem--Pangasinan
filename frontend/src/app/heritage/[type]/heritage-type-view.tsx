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
  MapPin,
  ArrowRight,
  ArrowLeft,
  Share2,
  Check,
  X,
  LayoutGrid,
  List,
  Compass,
  FileText,
  ShieldCheck,
  ChevronRight,
} from "lucide-react";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button, buttonVariants } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import {
  HeritageItem,
  HERITAGE_TYPES_CONFIG,
  HeritageTypeConfig,
} from "../heritage-types";

interface HeritageTypeViewProps {
  typeSlug: string;
  items: HeritageItem[];
  otherTypes: { slug: string; label: string; count: number }[];
}

export function HeritageTypeView({
  typeSlug,
  items,
  otherTypes,
}: HeritageTypeViewProps) {
  const [searchQuery, setSearchQuery] = useState("");
  const [selectedBarangay, setSelectedBarangay] = useState("all");
  const [sortBy, setSortBy] = useState<"name" | "newest">("name");
  const [viewMode, setViewMode] = useState<"grid" | "list">("grid");
  const [copiedId, setCopiedId] = useState<number | null>(null);

  const config: HeritageTypeConfig =
    HERITAGE_TYPES_CONFIG[typeSlug] || HERITAGE_TYPES_CONFIG.built;
  const Icon = config.icon;

  // Extract unique barangays in this category
  const availableBarangays = useMemo(() => {
    const bars = new Set<string>();
    items.forEach((item) => {
      if (item.barangay_name) bars.add(item.barangay_name);
    });
    return Array.from(bars).sort();
  }, [items]);

  // Filtered items
  const filteredItems = useMemo(() => {
    return items
      .filter((item) => {
        if (searchQuery.trim()) {
          const q = searchQuery.toLowerCase();
          const matchName = item.name_of_asset.toLowerCase().includes(q);
          const matchCommon = item.common_name?.toLowerCase().includes(q) || false;
          const matchLoc = item.location_details?.toLowerCase().includes(q) || false;
          const matchSignificance = item.significance?.toLowerCase().includes(q) || false;

          if (!matchName && !matchCommon && !matchLoc && !matchSignificance) {
            return false;
          }
        }

        if (selectedBarangay !== "all" && item.barangay_name !== selectedBarangay) {
          return false;
        }

        return true;
      })
      .sort((a, b) => {
        if (sortBy === "name") return a.name_of_asset.localeCompare(b.name_of_asset);
        return (b.id || 0) - (a.id || 0);
      });
  }, [items, searchQuery, selectedBarangay, sortBy]);

  const handleCopyLink = (e: React.MouseEvent, item: HeritageItem) => {
    e.preventDefault();
    e.stopPropagation();
    const url = `${window.location.origin}/heritage/${item.asset_type}/${item.id}`;
    navigator.clipboard.writeText(url);
    setCopiedId(item.id);
    setTimeout(() => setCopiedId(null), 2000);
  };

  return (
    <div className="space-y-8">
      {/* ── Breadcrumb ── */}
      <nav className="flex items-center gap-2 text-xs text-muted-foreground font-medium">
        <Link href="/heritage" className="hover:text-primary transition-colors">
          Heritage Registry
        </Link>
        <ChevronRight className="h-3.5 w-3.5 text-muted-foreground/60" />
        <span className="text-foreground font-semibold">{config.label}</span>
      </nav>

      {/* ── Category Banner ── */}
      <div className="rounded-3xl p-6 md:p-10 border border-border/60 bg-gradient-to-br from-card via-card to-muted/30 shadow-sm relative overflow-hidden">
        <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-6 relative z-10">
          <div className="space-y-3 max-w-3xl">
            <div className="flex flex-wrap items-center gap-2">
              <Badge className="bg-primary text-primary-foreground font-bold text-xs">
                {config.badgeLabel}
              </Badge>
              <Badge variant="outline" className="text-xs font-medium">
                {config.subtitle}
              </Badge>
            </div>

            <h1 className="text-3xl md:text-4xl lg:text-5xl font-bold tracking-tight text-foreground flex items-center gap-3">
              <div className="h-10 w-10 md:h-12 md:w-12 rounded-2xl bg-primary/10 text-primary flex items-center justify-center shrink-0">
                <Icon className="h-6 w-6" />
              </div>
              <span>{config.label_plural}</span>
            </h1>

            <p className="text-muted-foreground text-sm md:text-base leading-relaxed">
              {config.description}
            </p>
          </div>

          {/* Stat Box */}
          <div className="p-5 rounded-2xl bg-background/80 backdrop-blur-sm border border-border/60 shrink-0 text-center lg:text-right">
            <span className="text-3xl md:text-4xl font-bold text-primary block">
              {items.length}
            </span>
            <span className="text-xs text-muted-foreground uppercase font-bold tracking-wider">
              Documented Entries
            </span>
          </div>
        </div>

        {/* Quick Type Jump Bar */}
        <div className="mt-8 pt-6 border-t border-border/50 flex flex-wrap items-center gap-2">
          <span className="text-xs font-semibold text-muted-foreground mr-1">Other Classifications:</span>
          {otherTypes.map((ot) => {
            if (ot.slug === typeSlug) return null;
            return (
              <Link
                key={ot.slug}
                href={`/heritage/${ot.slug}`}
                className="px-3 py-1 rounded-full text-xs font-medium bg-muted hover:bg-muted/80 text-foreground transition-colors"
              >
                {ot.label} ({ot.count})
              </Link>
            );
          })}
        </div>
      </div>

      {/* ── Search & Filter Controls ── */}
      <div className="p-4 md:p-6 rounded-2xl bg-card border border-border/60 shadow-sm space-y-4">
        <div className="flex flex-col md:flex-row gap-3">
          <div className="relative flex-1">
            <Search className="absolute left-3.5 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
            <Input
              type="text"
              placeholder={`Search ${config.label.toLowerCase()} by name, location, or significance...`}
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

          <select
            value={sortBy}
            onChange={(e) => setSortBy(e.target.value as "name" | "newest")}
            className="h-11 px-3.5 rounded-md border border-input bg-background text-sm focus:outline-none focus:ring-2 focus:ring-primary/20"
          >
            <option value="name">Name (A to Z)</option>
            <option value="newest">Recently Registered</option>
          </select>

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

        {(searchQuery || selectedBarangay !== "all") && (
          <div className="flex items-center justify-between pt-2 border-t border-border/40 text-xs">
            <span className="text-muted-foreground">
              Filtering results in {config.label}
            </span>
            <button
              onClick={() => {
                setSearchQuery("");
                setSelectedBarangay("all");
              }}
              className="text-destructive font-medium hover:underline flex items-center gap-1"
            >
              <X className="h-3 w-3" />
              Reset
            </button>
          </div>
        )}
      </div>

      {/* ── Empty State ── */}
      {filteredItems.length === 0 && (
        <div className="text-center py-16 px-4 rounded-3xl border-2 border-dashed border-border/80 bg-muted/20">
          <Icon className="h-12 w-12 mx-auto text-muted-foreground/30 mb-4" />
          <h3 className="text-lg font-bold text-foreground">No entries found</h3>
          <p className="text-sm text-muted-foreground max-w-md mx-auto mt-1">
            No {config.label.toLowerCase()} entries matched your current search parameters.
          </p>
          <Button
            variant="outline"
            onClick={() => {
              setSearchQuery("");
              setSelectedBarangay("all");
            }}
            className="mt-5 text-xs"
          >
            Clear Filters
          </Button>
        </div>
      )}

      {/* ── Grid View ── */}
      {viewMode === "grid" && filteredItems.length > 0 && (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredItems.map((item) => (
            <Card
              key={item.id}
              className="group overflow-hidden border-border/60 hover:border-primary/40 hover:shadow-lg transition-all duration-300 flex flex-col justify-between h-full bg-card"
            >
              <div>
                <div className="aspect-[16/10] bg-muted relative overflow-hidden">
                  {item.image_url ? (
                    <img
                      src={item.image_url}
                      alt={item.name_of_asset}
                      className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
                    />
                  ) : (
                    <div className="w-full h-full flex flex-col items-center justify-center bg-muted text-muted-foreground/40">
                      <Icon className="h-12 w-12 mb-2" />
                      <span className="text-xs uppercase tracking-wider font-semibold">
                        {config.label}
                      </span>
                    </div>
                  )}

                  <div className="absolute top-3 left-3 flex flex-wrap gap-1.5">
                    <Badge className="bg-background/90 backdrop-blur-sm text-foreground text-[10px] font-bold shadow-xs">
                      {config.badgeLabel}
                    </Badge>
                    {item.barangay_name && (
                      <Badge variant="secondary" className="bg-background/80 backdrop-blur-sm text-foreground text-[10px]">
                        Brgy. {item.barangay_name}
                      </Badge>
                    )}
                  </div>

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

                <CardContent className="p-5 space-y-3">
                  <div className="space-y-1">
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
                    {item.significance || "Official registration in the Mangatarem Cultural Heritage Registry."}
                  </p>

                  {item.location_details && (
                    <div className="flex items-center gap-1.5 text-xs text-muted-foreground pt-1">
                      <MapPin className="h-3.5 w-3.5 text-primary shrink-0" />
                      <span className="truncate">{item.location_details}</span>
                    </div>
                  )}
                </CardContent>
              </div>

              <div className="p-5 pt-0">
                <Link
                  href={`/heritage/${typeSlug}/${item.id}`}
                  className={buttonVariants({ variant: "outline", size: "default", className: "w-full justify-between group-hover:bg-primary group-hover:text-primary-foreground transition-colors text-xs font-semibold" })}
                >
                  <span>View Full Profile</span>
                  <ArrowRight className="h-3.5 w-3.5 group-hover:translate-x-1 transition-transform" />
                </Link>
              </div>
            </Card>
          ))}
        </div>
      )}

      {/* ── List View ── */}
      {viewMode === "list" && filteredItems.length > 0 && (
        <div className="space-y-3">
          {filteredItems.map((item) => (
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
                      {config.badgeLabel}
                    </Badge>
                    {item.barangay_name && (
                      <span className="text-xs text-muted-foreground font-medium">
                        Brgy. {item.barangay_name}
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
                  href={`/heritage/${typeSlug}/${item.id}`}
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
          ))}
        </div>
      )}
    </div>
  );
}
