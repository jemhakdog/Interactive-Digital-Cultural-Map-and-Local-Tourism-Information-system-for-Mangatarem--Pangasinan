"use client";

import React, { useState, useEffect, useMemo, useCallback } from "react";
import { fetchAPI } from "@/lib/api";
// TODO: map content (attraction/event locations) is managed via /admin/attractions and /admin/events — no dedicated map-admin section exists.
import { AdminManageBar } from "@/components/layout/admin-manage-bar";
import { MarkerPlace, CuratedTrail, UserLocation, SortOption, ViewMode } from "@/components/map/types";
import { calculateDistance, CURATED_TRAILS } from "@/components/map/data";
import { MapContainer } from "@/components/map/map-container";
import { MapSidebar } from "@/components/map/map-sidebar";
import { MapDetailSheet } from "@/components/map/map-detail-sheet";
import { MapGridView } from "@/components/map/map-grid-view";
import {
  MapPin,
  Loader2,
  Columns2,
  Maximize,
  LayoutGrid,
  Locate,
  Route,
  Sparkles,
  SlidersHorizontal,
  ChevronLeft,
  ChevronRight,
  RefreshCw,
  Share2,
  Check,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";

export default function MapPage() {
  const [allMarkers, setAllMarkers] = useState<MarkerPlace[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Filters and state
  const [searchQuery, setSearchQuery] = useState("");
  const [selectedCategory, setSelectedCategory] = useState("all");
  const [selectedBarangay, setSelectedBarangay] = useState("all");
  const [sortBy, setSortBy] = useState<SortOption>("featured");

  // Interactive selection
  const [selectedPlace, setSelectedPlace] = useState<MarkerPlace | null>(null);
  const [hoveredPlaceId, setHoveredPlaceId] = useState<number | null>(null);
  const [activeTrail, setActiveTrail] = useState<CuratedTrail | null>(null);
  const [customTourPlaces, setCustomTourPlaces] = useState<MarkerPlace[]>([]);

  // Geolocation
  const [userLocation, setUserLocation] = useState<UserLocation | null>(null);
  const [locatingUser, setLocatingUser] = useState(false);

  // Layout View Mode
  const [viewMode, setViewMode] = useState<ViewMode>("split");
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [copiedLink, setCopiedLink] = useState(false);

  // Fetch all markers
  const loadMarkers = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await fetchAPI<{ markers: MarkerPlace[] }>("/api/map");
      setAllMarkers(data.markers || []);
    } catch (err) {
      console.error("Failed to load map markers:", err);
      setError("Unable to load map data. Please check your connection and try again.");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadMarkers();
  }, [loadMarkers]);

  // Request GPS Geolocation
  const handleLocateMe = useCallback(() => {
    if (!("geolocation" in navigator)) {
      alert("Geolocation is not supported by your browser.");
      return;
    }

    setLocatingUser(true);
    navigator.geolocation.getCurrentPosition(
      (pos) => {
        const coords = {
          latitude: pos.coords.latitude,
          longitude: pos.coords.longitude,
          accuracy: pos.coords.accuracy,
        };
        setUserLocation(coords);
        setLocatingUser(false);
      },
      (err) => {
        console.warn("Geolocation permission denied or timed out:", err);
        setLocatingUser(false);
      },
      { enableHighAccuracy: true, timeout: 10000 }
    );
  }, []);

  // Sync URL parameters on initial load
  useEffect(() => {
    if (typeof window === "undefined" || allMarkers.length === 0) return;

    const params = new URLSearchParams(window.location.search);
    const categoryParam = params.get("category");
    const barangayParam = params.get("barangay");
    const placeParam = params.get("place");
    const trailParam = params.get("trail");

    if (categoryParam) setSelectedCategory(categoryParam);
    if (barangayParam) setSelectedBarangay(barangayParam);

    if (placeParam) {
      const target = allMarkers.find((m) => m.id === Number(placeParam));
      if (target) setSelectedPlace(target);
    }

    if (trailParam) {
      const targetTrail = CURATED_TRAILS.find((t) => t.id === trailParam);
      if (targetTrail) setActiveTrail(targetTrail);
    }
  }, [allMarkers]);

  // Keyboard shortcut listener
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === "Escape") {
        if (selectedPlace) setSelectedPlace(null);
      }
    };
    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, [selectedPlace]);

  // Compute distances relative to user location
  const markersWithDistance = useMemo(() => {
    if (!userLocation) return allMarkers;
    return allMarkers.map((m) => {
      const dist = calculateDistance(
        userLocation.latitude,
        userLocation.longitude,
        m.latitude,
        m.longitude
      );
      return { ...m, distanceKm: dist };
    });
  }, [allMarkers, userLocation]);

  // Filter and sort markers
  const filteredMarkers = useMemo(() => {
    let result = [...markersWithDistance];

    // Category filter
    if (selectedCategory !== "all") {
      result = result.filter((m) => m.category === selectedCategory);
    }

    // Barangay filter
    if (selectedBarangay !== "all") {
      result = result.filter((m) => m.barangay_name === selectedBarangay);
    }

    // Search query filter
    if (searchQuery.trim()) {
      const q = searchQuery.toLowerCase().trim();
      result = result.filter(
        (m) =>
          m.name.toLowerCase().includes(q) ||
          m.category.toLowerCase().includes(q) ||
          (m.barangay_name && m.barangay_name.toLowerCase().includes(q)) ||
          (m.description && m.description.toLowerCase().includes(q))
      );
    }

    // Sorting
    if (sortBy === "featured") {
      result.sort((a, b) => (b.is_featured ? 1 : 0) - (a.is_featured ? 1 : 0));
    } else if (sortBy === "name") {
      result.sort((a, b) => a.name.localeCompare(b.name));
    } else if (sortBy === "distance" && userLocation) {
      result.sort((a, b) => (a.distanceKm ?? 9999) - (b.distanceKm ?? 9999));
    }

    return result;
  }, [markersWithDistance, selectedCategory, selectedBarangay, searchQuery, sortBy, userLocation]);

  // Reset all filters
  const handleResetFilters = () => {
    setSearchQuery("");
    setSelectedCategory("all");
    setSelectedBarangay("all");
    setSortBy("featured");
  };

  // Toggle custom tour waypoint
  const handleToggleCustomTour = (place: MarkerPlace) => {
    setCustomTourPlaces((prev) => {
      const exists = prev.some((p) => p.id === place.id);
      if (exists) {
        return prev.filter((p) => p.id !== place.id);
      }
      return [...prev, place];
    });
  };

  // Clear custom tour
  const handleClearCustomTour = () => {
    setCustomTourPlaces([]);
  };

  // Share current map view URL
  const handleShareMap = () => {
    const params = new URLSearchParams();
    if (selectedCategory !== "all") params.set("category", selectedCategory);
    if (selectedBarangay !== "all") params.set("barangay", selectedBarangay);
    if (selectedPlace) params.set("place", String(selectedPlace.id));
    if (activeTrail) params.set("trail", activeTrail.id);

    const queryString = params.toString();
    const shareUrl = `${window.location.origin}/map${queryString ? `?${queryString}` : ""}`;
    navigator.clipboard.writeText(shareUrl);
    setCopiedLink(true);
    setTimeout(() => setCopiedLink(false), 2000);
  };

  return (
    <div className="flex flex-col h-[calc(100vh-64px)] w-full overflow-hidden bg-background">
      <AdminManageBar label="Map data" href="/admin/attractions" note="(locations are managed via Attractions & Events)" />
      {/* Top Action & Sub-Navigation Bar */}
      <header className="h-14 border-b border-border/80 px-4 flex items-center justify-between gap-3 bg-background/95 backdrop-blur-md z-30 shrink-0">
        {/* Title and stats */}
        <div className="flex items-center gap-3 min-w-0">
          <div className="flex items-center gap-2 min-w-0">
            <div className="size-8 rounded-lg bg-primary/10 text-primary flex items-center justify-center shrink-0 border border-primary/20">
              <MapPin className="w-4 h-4" />
            </div>
            <div className="min-w-0">
              <h1 className="font-bold text-sm sm:text-base text-foreground leading-none truncate">
                Interactive Cultural Map
              </h1>
              <p className="text-[11px] text-muted-foreground hidden sm:block mt-0.5 truncate">
                Explore Mangatarem on the interactive map · {allMarkers.length} Recorded Landmarks & Trails
              </p>
            </div>
          </div>

          {activeTrail && (
            <Badge
              variant="secondary"
              className="hidden md:inline-flex items-center gap-1 text-[11px] bg-primary/10 text-primary border-primary/20"
            >
              <Sparkles className="w-3 h-3" />
              Tour Active: {activeTrail.title}
            </Badge>
          )}
        </div>

        {/* Action Controls */}
        <div className="flex items-center gap-1.5 shrink-0">
          {/* Geolocation locate button */}
          <Button
            size="sm"
            variant={userLocation ? "default" : "outline"}
            className="h-8 text-xs gap-1.5"
            onClick={handleLocateMe}
            disabled={locatingUser}
            title={userLocation ? "GPS Location Active" : "Find my location"}
          >
            {locatingUser ? (
              <Loader2 className="w-3.5 h-3.5 animate-spin" />
            ) : (
              <Locate className="w-3.5 h-3.5" />
            )}
            <span className="hidden md:inline">
              {userLocation ? "Located" : "Locate Me"}
            </span>
          </Button>

          {/* Share Map link */}
          <Button
            size="sm"
            variant="outline"
            className="h-8 text-xs gap-1.5 hidden sm:flex"
            onClick={handleShareMap}
            title="Share current map view link"
          >
            {copiedLink ? (
              <>
                <Check className="w-3.5 h-3.5 text-emerald-600" />
                <span>Link Copied</span>
              </>
            ) : (
              <>
                <Share2 className="w-3.5 h-3.5" />
                <span>Share</span>
              </>
            )}
          </Button>

          {/* View Mode Switcher */}
          <div className="flex items-center bg-muted p-0.5 rounded-lg border border-border">
            <button
              type="button"
              className={`p-1.5 rounded-md text-xs font-medium transition-colors ${
                viewMode === "split"
                  ? "bg-background text-foreground shadow-xs"
                  : "text-muted-foreground hover:text-foreground"
              }`}
              onClick={() => setViewMode("split")}
              title="Split View (Map + Panel)"
            >
              <Columns2 className="w-4 h-4" />
            </button>
            <button
              type="button"
              className={`p-1.5 rounded-md text-xs font-medium transition-colors ${
                viewMode === "full"
                  ? "bg-background text-foreground shadow-xs"
                  : "text-muted-foreground hover:text-foreground"
              }`}
              onClick={() => setViewMode("full")}
              title="Full Map Canvas View"
            >
              <Maximize className="w-4 h-4" />
            </button>
            <button
              type="button"
              className={`p-1.5 rounded-md text-xs font-medium transition-colors ${
                viewMode === "grid"
                  ? "bg-background text-foreground shadow-xs"
                  : "text-muted-foreground hover:text-foreground"
              }`}
              onClick={() => setViewMode("grid")}
              title="Directory Grid View"
            >
              <LayoutGrid className="w-4 h-4" />
            </button>
          </div>
        </div>
      </header>

      {/* Main Content Body */}
      {loading ? (
        <div className="flex-1 flex flex-col items-center justify-center gap-3 text-muted-foreground">
          <Loader2 className="h-8 w-8 animate-spin text-primary" />
          <p className="font-medium text-sm text-foreground">Loading Mangatarem Cultural Map...</p>
          <p className="text-xs text-muted-foreground">Fetching attractions, heritage landmarks & trails</p>
        </div>
      ) : error ? (
        <div className="flex-1 flex flex-col items-center justify-center gap-3 text-center p-6">
          <div className="size-12 rounded-full bg-destructive/10 text-destructive flex items-center justify-center">
            <MapPin className="w-6 h-6" />
          </div>
          <h2 className="font-bold text-lg text-foreground">Failed to Load Map Data</h2>
          <p className="text-xs text-muted-foreground max-w-sm">{error}</p>
          <Button size="sm" onClick={loadMarkers} className="mt-2 gap-1.5">
            <RefreshCw className="w-3.5 h-3.5" />
            Retry
          </Button>
        </div>
      ) : viewMode === "grid" ? (
        /* Grid Directory View */
        <div className="flex-1 overflow-y-auto">
          <MapGridView
            markers={filteredMarkers}
            onSelectOnMap={(place) => {
              setSelectedPlace(place);
              setViewMode("split");
            }}
          />
        </div>
      ) : (
        /* Split & Full Map Modes */
        <div className="flex-1 relative flex overflow-hidden">
          {/* Collapsible Left Sidebar (Split Mode) */}
          {viewMode === "split" && (
            <div
              className={`transition-all duration-300 ease-in-out relative z-20 shrink-0 ${
                sidebarOpen
                  ? "w-full md:w-[380px] lg:w-[420px]"
                  : "w-0 overflow-hidden"
              }`}
            >
              <MapSidebar
                markers={filteredMarkers}
                allMarkers={allMarkers}
                selectedPlace={selectedPlace}
                hoveredPlaceId={hoveredPlaceId}
                activeTrail={activeTrail}
                searchQuery={searchQuery}
                selectedCategory={selectedCategory}
                selectedBarangay={selectedBarangay}
                sortBy={sortBy}
                customTourPlaces={customTourPlaces}
                hasUserLocation={!!userLocation}
                onSearchChange={setSearchQuery}
                onCategoryChange={setSelectedCategory}
                onBarangayChange={setSelectedBarangay}
                onSortChange={setSortBy}
                onSelectPlace={setSelectedPlace}
                onHoverPlace={setHoveredPlaceId}
                onActivateTrail={setActiveTrail}
                onDeactivateTrail={() => setActiveTrail(null)}
                onToggleCustomTour={handleToggleCustomTour}
                onClearCustomTour={handleClearCustomTour}
                onResetFilters={handleResetFilters}
              />
            </div>
          )}

          {/* Sidebar Collapse Toggle Handle Button */}
          {viewMode === "split" && (
            <button
              type="button"
              className="hidden md:flex absolute top-1/2 -translate-y-1/2 z-30 size-6 bg-background border border-border rounded-r-md shadow-md items-center justify-center text-muted-foreground hover:text-foreground transition-all duration-300"
              style={{
                left: sidebarOpen ? "calc(min(420px, 100vw))" : "0px",
              }}
              onClick={() => setSidebarOpen(!sidebarOpen)}
              title={sidebarOpen ? "Collapse sidebar" : "Expand sidebar"}
            >
              {sidebarOpen ? (
                <ChevronLeft className="w-3.5 h-3.5" />
              ) : (
                <ChevronRight className="w-3.5 h-3.5" />
              )}
            </button>
          )}

          {/* Interactive Map Canvas Area */}
          <div className="flex-1 relative h-full w-full overflow-hidden">
            <MapContainer
              markers={filteredMarkers}
              selectedPlace={selectedPlace}
              hoveredPlaceId={hoveredPlaceId}
              activeTrail={activeTrail}
              userLocation={userLocation}
              onSelectPlace={(place) => setSelectedPlace(place)}
              onLocateUser={(coords) => {
                setUserLocation({
                  latitude: coords.latitude,
                  longitude: coords.longitude,
                });
              }}
            />

            {/* Selected Place Detail Floating Sheet */}
            <MapDetailSheet
              place={selectedPlace}
              onClose={() => setSelectedPlace(null)}
              isInTour={
                selectedPlace
                  ? customTourPlaces.some((p) => p.id === selectedPlace.id)
                  : false
              }
              onToggleTour={handleToggleCustomTour}
            />
          </div>
        </div>
      )}
    </div>
  );
}
