"use client";

import React, { useState } from "react";
import { MarkerPlace, CuratedTrail, SortOption } from "./types";
import { CATEGORY_CONFIG, CURATED_TRAILS } from "./data";
import { MapPlaceCard } from "./map-place-card";
import { MapTrailCard } from "./map-trail-card";
import {
  Search,
  X,
  SlidersHorizontal,
  Compass,
  MapPin,
  Route,
  BookOpen,
  Sparkles,
  Navigation,
  Trash2,
  Share2,
  Check,
  ChevronRight,
  Landmark,
  TreePine,
} from "lucide-react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";

interface MapSidebarProps {
  markers: MarkerPlace[];
  allMarkers: MarkerPlace[];
  selectedPlace: MarkerPlace | null;
  hoveredPlaceId: number | null;
  activeTrail: CuratedTrail | null;
  searchQuery: string;
  selectedCategory: string;
  selectedBarangay: string;
  sortBy: SortOption;
  customTourPlaces: MarkerPlace[];
  hasUserLocation: boolean;
  onSearchChange: (q: string) => void;
  onCategoryChange: (cat: string) => void;
  onBarangayChange: (brgy: string) => void;
  onSortChange: (sort: SortOption) => void;
  onSelectPlace: (place: MarkerPlace | null) => void;
  onHoverPlace: (id: number | null) => void;
  onActivateTrail: (trail: CuratedTrail) => void;
  onDeactivateTrail: () => void;
  onToggleCustomTour: (place: MarkerPlace) => void;
  onClearCustomTour: () => void;
  onResetFilters: () => void;
}

export function MapSidebar({
  markers,
  allMarkers,
  selectedPlace,
  hoveredPlaceId,
  activeTrail,
  searchQuery,
  selectedCategory,
  selectedBarangay,
  sortBy,
  customTourPlaces,
  hasUserLocation,
  onSearchChange,
  onCategoryChange,
  onBarangayChange,
  onSortChange,
  onSelectPlace,
  onHoverPlace,
  onActivateTrail,
  onDeactivateTrail,
  onToggleCustomTour,
  onClearCustomTour,
  onResetFilters,
}: MapSidebarProps) {
  const [activeTab, setActiveTab] = useState<"places" | "trails" | "guide">("places");
  const [copiedShare, setCopiedShare] = useState(false);

  // Extract unique barangays that have attractions
  const uniqueBarangays = Array.from(
    new Set(allMarkers.map((m) => m.barangay_name).filter(Boolean))
  ) as string[];

  // Calculate total tour distance for custom planner
  const customTourDistance = customTourPlaces.reduce((acc, curr, idx, arr) => {
    if (idx === 0) return 0;
    const prev = arr[idx - 1];
    // Simple approx distance in km
    const latDiff = (curr.latitude - prev.latitude) * 111;
    const lngDiff = (curr.longitude - prev.longitude) * 105;
    return acc + Math.sqrt(latDiff * latDiff + lngDiff * lngDiff);
  }, 0);

  // Google Maps Multi-Stop directions for custom itinerary
  const customTourGoogleUrl =
    customTourPlaces.length > 0
      ? `https://www.google.com/maps/dir/?api=1&origin=${customTourPlaces[0].latitude},${customTourPlaces[0].longitude}&destination=${
          customTourPlaces[customTourPlaces.length - 1].latitude
        },${customTourPlaces[customTourPlaces.length - 1].longitude}${
          customTourPlaces.length > 2
            ? `&waypoints=${customTourPlaces
                .slice(1, -1)
                .map((p) => `${p.latitude},${p.longitude}`)
                .join("|")}`
            : ""
        }`
      : "#";

  const handleShareCustomTour = () => {
    if (customTourPlaces.length === 0) return;
    const placeIds = customTourPlaces.map((p) => p.id).join(",");
    const url = `${window.location.origin}/map?tour=${placeIds}`;
    navigator.clipboard.writeText(url);
    setCopiedShare(true);
    setTimeout(() => setCopiedShare(false), 2000);
  };

  return (
    <aside aria-label="Map Sidebar" className="flex flex-col h-full bg-background border-r border-border/80 overflow-hidden">
      {/* Search and Navigation Tabs */}
      <div className="p-4 border-b border-border/70 space-y-3 bg-muted/20 shrink-0">
        {/* Search Bar */}
        <div className="relative">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
          <Input
            value={searchQuery}
            onChange={(e) => onSearchChange(e.target.value)}
            placeholder="Search attractions, falls, churches..."
            className="pl-9 pr-8 h-9 text-xs bg-background shadow-xs"
          />
          {searchQuery && (
            <button
              type="button"
              className="absolute right-2.5 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground"
              onClick={() => onSearchChange("")}
            >
              <X className="w-3.5 h-3.5" />
            </button>
          )}
        </div>

        {/* Tab Buttons */}
        <div className="grid grid-cols-3 gap-1 bg-muted p-1 rounded-lg text-xs font-medium">
          <button
            type="button"
            className={`flex items-center justify-center gap-1.5 py-1.5 rounded-md transition-colors ${
              activeTab === "places"
                ? "bg-background text-foreground shadow-xs font-semibold"
                : "text-muted-foreground hover:text-foreground"
            }`}
            onClick={() => setActiveTab("places")}
          >
            <MapPin className="w-3.5 h-3.5 text-primary" />
            <span>Places ({markers.length})</span>
          </button>

          <button
            type="button"
            className={`flex items-center justify-center gap-1.5 py-1.5 rounded-md transition-colors ${
              activeTab === "trails"
                ? "bg-background text-foreground shadow-xs font-semibold"
                : "text-muted-foreground hover:text-foreground"
            }`}
            onClick={() => setActiveTab("trails")}
          >
            <Route className="w-3.5 h-3.5 text-primary" />
            <span>Tours & Trails</span>
            {customTourPlaces.length > 0 && (
              <span className="size-1.5 rounded-full bg-primary" />
            )}
          </button>

          <button
            type="button"
            className={`flex items-center justify-center gap-1.5 py-1.5 rounded-md transition-colors ${
              activeTab === "guide"
                ? "bg-background text-foreground shadow-xs font-semibold"
                : "text-muted-foreground hover:text-foreground"
            }`}
            onClick={() => setActiveTab("guide")}
          >
            <BookOpen className="w-3.5 h-3.5 text-primary" />
            <span>Barangay Guide</span>
          </button>
        </div>

        {/* Category & Filter Row (Only when in places tab) */}
        {activeTab === "places" && (
          <div className="space-y-2 pt-1">
            {/* Category horizontal scroll list */}
            <div className="flex items-center gap-1.5 overflow-x-auto pb-1 no-scrollbar text-xs">
              <button
                type="button"
                className={`px-2.5 py-1 rounded-full text-xs shrink-0 font-medium transition-colors border ${
                  selectedCategory === "all"
                    ? "bg-primary text-primary-foreground border-primary"
                    : "bg-background hover:bg-muted text-muted-foreground border-border"
                }`}
                onClick={() => onCategoryChange("all")}
              >
                All Categories ({allMarkers.length})
              </button>

              {Object.keys(CATEGORY_CONFIG).map((cat) => {
                const count = allMarkers.filter((m) => m.category === cat).length;
                if (count === 0 && cat !== "Nature" && cat !== "Historical") return null;

                const isSelected = selectedCategory === cat;
                return (
                  <button
                    key={cat}
                    type="button"
                    className={`px-2.5 py-1 rounded-full text-xs shrink-0 font-medium transition-colors border ${
                      isSelected
                        ? "bg-primary text-primary-foreground border-primary"
                        : "bg-background hover:bg-muted text-muted-foreground border-border"
                    }`}
                    onClick={() => onCategoryChange(cat)}
                  >
                    {cat} {count > 0 ? `(${count})` : ""}
                  </button>
                );
              })}
            </div>

            {/* Filter Dropdowns Grid */}
            <div className="grid grid-cols-2 gap-2 text-xs">
              {/* Category Filter Dropdown */}
              <select
                value={selectedCategory}
                onChange={(e) => onCategoryChange(e.target.value)}
                className="h-8 rounded-md border border-border bg-background px-2.5 py-1 text-xs text-foreground focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring"
                aria-label="Filter by Category"
              >
                <option value="all">All Categories</option>
                <option value="Nature">Nature</option>
                <option value="Historical">Historical</option>
                <option value="Heritage">Heritage</option>
                <option value="Religious">Religious</option>
                <option value="Public Space">Public Space</option>
              </select>

              {/* Barangay Filter */}
              <select
                value={selectedBarangay}
                onChange={(e) => onBarangayChange(e.target.value)}
                className="h-8 rounded-md border border-border bg-background px-2.5 py-1 text-xs text-foreground focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring"
                aria-label="Filter by Barangay"
              >
                <option value="all">All Barangays (82)</option>
                {uniqueBarangays.map((b) => (
                  <option key={b} value={b}>
                    Brgy. {b}
                  </option>
                ))}
              </select>
            </div>

            {/* Sort Row */}
            <div className="flex items-center justify-between text-xs pt-0.5">
              <span className="text-[11px] text-muted-foreground">Sort order:</span>
              <select
                value={sortBy}
                onChange={(e) => onSortChange(e.target.value as SortOption)}
                className="w-40 h-7 rounded-md border border-border bg-background px-2 py-0.5 text-xs text-foreground focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring"
                aria-label="Sort places"
              >
                <option value="featured">Featured First</option>
                <option value="name">Alphabetical (A-Z)</option>
                {hasUserLocation && <option value="distance">Nearest to Me</option>}
              </select>
            </div>
          </div>
        )}
      </div>

      {/* Tab 1: Places Content */}
      {activeTab === "places" && (
        <div className="flex-1 overflow-y-auto p-4 space-y-3">
          {/* Active Filter Summary */}
          {(selectedCategory !== "all" || selectedBarangay !== "all" || searchQuery) && (
            <div className="flex items-center justify-between text-xs py-1 px-2 rounded-md bg-muted/60 text-muted-foreground">
              <span>
                Showing {markers.length} of {allMarkers.length} locations
              </span>
              <button
                type="button"
                className="text-primary font-medium hover:underline flex items-center gap-1"
                onClick={onResetFilters}
              >
                Reset filters
              </button>
            </div>
          )}

          {markers.length === 0 ? (
            <div className="text-center py-12 px-4 space-y-3">
              <div className="size-12 rounded-full bg-muted flex items-center justify-center mx-auto text-muted-foreground">
                <MapPin className="w-6 h-6 opacity-40" />
              </div>
              <div>
                <h4 className="font-semibold text-sm text-foreground">No places found</h4>
                <p className="text-xs text-muted-foreground mt-1">
                  Try adjusting your search terms or category filters.
                </p>
              </div>
              <Button size="sm" variant="outline" onClick={onResetFilters}>
                Reset all filters
              </Button>
            </div>
          ) : (
            markers.map((place) => {
              const isSelected = selectedPlace?.id === place.id;
              const isInTour = customTourPlaces.some((p) => p.id === place.id);

              return (
                <MapPlaceCard
                  key={place.id}
                  place={place}
                  isSelected={isSelected}
                  onSelect={onSelectPlace}
                  onHover={onHoverPlace}
                  isInTour={isInTour}
                  onToggleTour={onToggleCustomTour}
                />
              );
            })
          )}
        </div>
      )}

      {/* Tab 2: Curated Trails & Itinerary Content */}
      {activeTab === "trails" && (
        <div className="flex-1 overflow-y-auto p-4 space-y-6">
          {/* Curated Suggested Trails */}
          <div className="space-y-3">
            <div className="flex items-center justify-between">
              <h3 className="font-bold text-sm text-foreground flex items-center gap-1.5">
                <Sparkles className="w-4 h-4 text-primary" />
                Curated Day Tours
              </h3>
              <span className="text-[11px] text-muted-foreground">Mangatarem Special</span>
            </div>

            <div className="space-y-3">
              {CURATED_TRAILS.map((trail) => {
                const isActive = activeTrail?.id === trail.id;
                return (
                  <MapTrailCard
                    key={trail.id}
                    trail={trail}
                    isActive={isActive}
                    onActivate={onActivateTrail}
                    onDeactivate={onDeactivateTrail}
                  />
                );
              })}
            </div>
          </div>

          {/* Custom Tour Planner Box */}
          <div className="p-4 rounded-xl border border-border bg-muted/30 space-y-3">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-1.5">
                <Route className="w-4 h-4 text-primary" />
                <h4 className="font-semibold text-sm text-foreground">Custom Day Itinerary</h4>
              </div>
              {customTourPlaces.length > 0 && (
                <span className="text-xs font-semibold text-primary">
                  {customTourPlaces.length} stop{customTourPlaces.length !== 1 ? "s" : ""}
                </span>
              )}
            </div>

            <p className="text-xs text-muted-foreground leading-relaxed">
              Build your own tour by clicking the <span className="font-medium text-foreground">+</span> button on any attraction card in the Places tab.
            </p>

            {customTourPlaces.length === 0 ? (
              <div className="text-center py-6 border border-dashed border-border rounded-lg text-xs text-muted-foreground">
                No stops added yet. Explore places to add waypoints to your custom tour!
              </div>
            ) : (
              <div className="space-y-3">
                {/* Waypoint list */}
                <div className="space-y-1.5">
                  {customTourPlaces.map((p, idx) => (
                    <div
                      key={p.id}
                      className="flex items-center justify-between gap-2 p-2 rounded-lg bg-background border border-border text-xs"
                    >
                      <div className="flex items-center gap-2 min-w-0">
                        <span className="flex items-center justify-center size-5 rounded-full bg-primary text-primary-foreground font-bold text-[10px] shrink-0">
                          {idx + 1}
                        </span>
                        <span className="font-medium text-foreground truncate">{p.name}</span>
                      </div>
                      <button
                        type="button"
                        className="text-muted-foreground hover:text-destructive p-1"
                        onClick={() => onToggleCustomTour(p)}
                        title="Remove stop"
                      >
                        <Trash2 className="w-3.5 h-3.5" />
                      </button>
                    </div>
                  ))}
                </div>

                {/* Tour metrics summary */}
                <div className="flex items-center justify-between text-xs font-medium text-muted-foreground pt-1">
                  <span>Est. Distance: ~{customTourDistance.toFixed(1)} km</span>
                  <button
                    type="button"
                    className="text-destructive hover:underline text-[11px]"
                    onClick={onClearCustomTour}
                  >
                    Clear All
                  </button>
                </div>

                {/* Itinerary Action Buttons */}
                <div className="grid grid-cols-2 gap-2 pt-1">
                  <a
                    href={customTourGoogleUrl}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="inline-flex items-center justify-center gap-1.5 h-8 rounded-lg bg-primary text-primary-foreground hover:bg-primary/90 text-xs font-medium shadow-xs"
                  >
                    <Navigation className="w-3.5 h-3.5" />
                    Navigate
                  </a>

                  <Button
                    size="sm"
                    variant="outline"
                    className="h-8 text-xs font-medium gap-1.5"
                    onClick={handleShareCustomTour}
                  >
                    {copiedShare ? (
                      <>
                        <Check className="w-3.5 h-3.5 text-emerald-600" />
                        Copied!
                      </>
                    ) : (
                      <>
                        <Share2 className="w-3.5 h-3.5" />
                        Share Tour
                      </>
                    )}
                  </Button>
                </div>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Tab 3: Barangay Guide Content */}
      {activeTab === "guide" && (
        <div className="flex-1 overflow-y-auto p-4 space-y-4 text-xs">
          <div className="p-3.5 rounded-xl bg-primary/10 border border-primary/20 space-y-2">
            <h3 className="font-bold text-sm text-primary flex items-center gap-1.5">
              <Landmark className="w-4 h-4" />
              Mangatarem Tourism Overview
            </h3>
            <p className="text-muted-foreground leading-relaxed text-[11px]">
              Mangatarem is the largest municipality by land area in Pangasinan, encompassing 82 barangays. It spans from the western mountain ranges of Zambales down to fertile plains and rivers.
            </p>
          </div>

          {/* Tourism Clusters */}
          <div className="space-y-3">
            <h4 className="font-semibold text-xs text-foreground uppercase tracking-wider text-muted-foreground">
              Geographic Tourism Clusters
            </h4>

            {/* Cluster 1 */}
            <div className="p-3 rounded-lg border border-border bg-card space-y-1.5">
              <div className="flex items-center justify-between">
                <span className="font-semibold text-foreground flex items-center gap-1.5">
                  <TreePine className="w-3.5 h-3.5 text-emerald-600" />
                  Upland & Mountain Corridor
                </span>
                <Badge variant="secondary" className="text-[10px]">
                  Brgy. Malabobo
                </Badge>
              </div>
              <p className="text-muted-foreground text-[11px] leading-relaxed">
                Home to the breathtaking Daang Kalikasan scenic highway and the Manleluag Spring Protected Landscape. Ideal for road trips, cycling, and nature retreat.
              </p>
            </div>

            {/* Cluster 2 */}
            <div className="p-3 rounded-lg border border-border bg-card space-y-1.5">
              <div className="flex items-center justify-between">
                <span className="font-semibold text-foreground flex items-center gap-1.5">
                  <Landmark className="w-3.5 h-3.5 text-amber-600" />
                  Poblacion Civic & Heritage Core
                </span>
                <Badge variant="secondary" className="text-[10px]">
                  Brgy. Poblacion
                </Badge>
              </div>
              <p className="text-muted-foreground text-[11px] leading-relaxed">
                The heart of Mangatarem containing the historic 1835 St. Raymund de Penafort Parish Church, Municipal Town Plaza, Rizal Monument, and ancestral heritage residences.
              </p>
            </div>

            {/* Cluster 3 */}
            <div className="p-3 rounded-lg border border-border bg-card space-y-1.5">
              <div className="flex items-center justify-between">
                <span className="font-semibold text-foreground flex items-center gap-1.5">
                  <Compass className="w-3.5 h-3.5 text-teal-600" />
                  Foothills & Waterfalls Zone
                </span>
                <Badge variant="secondary" className="text-[10px]">
                  Brgy. Cabaluyan & Foothills
                </Badge>
              </div>
              <p className="text-muted-foreground text-[11px] leading-relaxed">
                Undeveloped eco-tourism havens featuring Timmanguyob Falls, Canding Falls, and pristine mountain rivers for trekking adventures.
              </p>
            </div>
          </div>
        </div>
      )}
    </aside>
  );
}
