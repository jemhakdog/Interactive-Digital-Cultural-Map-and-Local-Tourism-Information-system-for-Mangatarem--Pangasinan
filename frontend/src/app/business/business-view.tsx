"use client";

import { useState, useMemo } from "react";
import Link from "next/link";
import {
  Building2,
  Hotel,
  Utensils,
  Coffee,
  Sprout,
  Store,
  MapPin,
  Phone,
  Star,
  Sparkles,
  Search,
  SlidersHorizontal,
  ArrowRight,
  Wifi,
  Car,
  Wind,
  Tv,
  Waves,
  Bath,
  Check,
  Share2,
  X,
  Bed,
  ShieldCheck,
  LayoutGrid,
  List,
  Compass,
} from "lucide-react";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

export interface EstablishmentItem {
  id: number;
  name: string;
  type: string;
  description?: string | null;
  address?: string | null;
  latitude?: number | null;
  longitude?: number | null;
  contact_number?: string | null;
  email?: string | null;
  website?: string | null;
  price_range?: string | null;
  rating_avg?: number;
  review_count?: number;
  cover_image_url?: string | null;
  logo_url?: string | null;
  amenities?: string[];
  operating_hours?: Record<string, string> | null;
  barangay?: string | null;
  barangay_name?: string | null;
  is_featured?: boolean;
  created_at?: string | null;
  distance?: number;
}

interface BusinessViewProps {
  establishments: EstablishmentItem[];
}

// Category mappings with clean icons and labels
const CATEGORY_CONFIG: Record<
  string,
  { label: string; icon: typeof Building2; color: string }
> = {
  all: { label: "All Businesses", icon: Store, color: "text-primary" },
  inn: { label: "Inns & Lodging", icon: Hotel, color: "text-emerald-600 dark:text-emerald-400" },
  restaurant: { label: "Restaurants & Dining", icon: Utensils, color: "text-amber-600 dark:text-amber-400" },
  cafe: { label: "Cafes & Bakeries", icon: Coffee, color: "text-orange-600 dark:text-orange-400" },
  farm: { label: "Agro-Tourism & Farms", icon: Sprout, color: "text-lime-600 dark:text-lime-400" },
  fastfood: { label: "Fast Food & Bites", icon: Utensils, color: "text-rose-600 dark:text-rose-400" },
  shop: { label: "Shops & Souvenirs", icon: Store, color: "text-blue-600 dark:text-blue-400" },
};

// Amenity Icons dictionary
const AMENITY_ICONS: Record<string, { label: string; icon: typeof Wifi }> = {
  wifi: { label: "Free Wi-Fi", icon: Wifi },
  parking: { label: "Parking", icon: Car },
  aircon: { label: "Air Conditioning", icon: Wind },
  tv: { label: "Cable TV", icon: Tv },
  pool: { label: "Swimming Pool", icon: Waves },
  bathroom: { label: "Private Bath", icon: Bath },
  hot_water: { label: "Hot Water", icon: Waves },
};

export function BusinessView({ establishments }: BusinessViewProps) {
  const [searchQuery, setSearchQuery] = useState("");
  const [selectedType, setSelectedType] = useState<string>("all");
  const [selectedPrice, setSelectedPrice] = useState<string>("all");
  const [selectedBarangay, setSelectedBarangay] = useState<string>("all");
  const [selectedAmenity, setSelectedAmenity] = useState<string>("all");
  const [sortBy, setSortBy] = useState<"featured" | "rating" | "name" | "price_asc">("featured");
  const [viewMode, setViewMode] = useState<"grid" | "list">("grid");
  const [copiedId, setCopiedId] = useState<number | null>(null);

  // Extract unique types from data
  const availableTypes = useMemo(() => {
    const types = new Set<string>();
    establishments.forEach((e) => {
      if (e.type) types.add(e.type);
    });
    return Array.from(types);
  }, [establishments]);

  // Extract unique barangays
  const availableBarangays = useMemo(() => {
    const bars = new Set<string>();
    establishments.forEach((e) => {
      const b = e.barangay_name || e.barangay;
      if (b) bars.add(b);
    });
    return Array.from(bars);
  }, [establishments]);

  // Spotlight featured establishment
  const featuredSpotlight = useMemo(() => {
    if (establishments.length === 0) return null;
    const featured = establishments.find((e) => e.is_featured);
    return featured || establishments[0];
  }, [establishments]);

  // Filtered and Sorted establishments
  const filteredBusinesses = useMemo(() => {
    const result = establishments.filter((item) => {
      // Search matching (name, description, address, amenities, type)
      if (searchQuery.trim()) {
        const q = searchQuery.toLowerCase();
        const matchName = item.name.toLowerCase().includes(q);
        const matchDesc = item.description?.toLowerCase().includes(q) || false;
        const matchAddr = item.address?.toLowerCase().includes(q) || false;
        const matchType = item.type?.toLowerCase().includes(q) || false;
        const matchBarangay = (item.barangay_name || item.barangay)?.toLowerCase().includes(q) || false;
        const matchAmenities = item.amenities?.some((a) => a.toLowerCase().includes(q)) || false;

        if (!matchName && !matchDesc && !matchAddr && !matchType && !matchBarangay && !matchAmenities) {
          return false;
        }
      }

      // Type filter
      if (selectedType !== "all" && item.type !== selectedType) {
        return false;
      }

      // Price filter
      if (selectedPrice !== "all" && item.price_range !== selectedPrice) {
        return false;
      }

      // Barangay filter
      if (selectedBarangay !== "all") {
        const b = item.barangay_name || item.barangay;
        if (b !== selectedBarangay) return false;
      }

      // Amenity filter
      if (selectedAmenity !== "all") {
        if (!item.amenities || !item.amenities.includes(selectedAmenity)) {
          return false;
        }
      }

      return true;
    });

    // Sorting
    return result.sort((a, b) => {
      if (sortBy === "featured") {
        if (a.is_featured && !b.is_featured) return -1;
        if (!a.is_featured && b.is_featured) return 1;
        return (b.rating_avg || 0) - (a.rating_avg || 0);
      }
      if (sortBy === "rating") {
        return (b.rating_avg || 0) - (a.rating_avg || 0);
      }
      if (sortBy === "name") {
        return a.name.localeCompare(b.name);
      }
      if (sortBy === "price_asc") {
        const priceOrder: Record<string, number> = { budget: 1, moderate: 2, luxury: 3 };
        const priceA = a.price_range ? priceOrder[a.price_range] || 2 : 2;
        const priceB = b.price_range ? priceOrder[b.price_range] || 2 : 2;
        return priceA - priceB;
      }
      return 0;
    });
  }, [
    establishments,
    searchQuery,
    selectedType,
    selectedPrice,
    selectedBarangay,
    selectedAmenity,
    sortBy,
  ]);

  const hasActiveFilters =
    searchQuery.trim() !== "" ||
    selectedType !== "all" ||
    selectedPrice !== "all" ||
    selectedBarangay !== "all" ||
    selectedAmenity !== "all";

  const handleClearFilters = () => {
    setSearchQuery("");
    setSelectedType("all");
    setSelectedPrice("all");
    setSelectedBarangay("all");
    setSelectedAmenity("all");
    setSortBy("featured");
  };

  const handleShare = async (e: React.MouseEvent, item: EstablishmentItem) => {
    e.preventDefault();
    e.stopPropagation();
    const url = `${window.location.origin}/business/${item.id}`;
    if (navigator.share) {
      try {
        await navigator.share({
          title: item.name,
          text: `Check out ${item.name} in Mangatarem, Pangasinan!`,
          url: url,
        });
        return;
      } catch {
        // Fallback to clipboard
      }
    }
    navigator.clipboard.writeText(url);
    setCopiedId(item.id);
    setTimeout(() => setCopiedId(null), 2000);
  };

  const getPriceBadge = (price?: string | null) => {
    switch (price) {
      case "budget":
        return { label: "₱ Budget", variant: "outline" as const, desc: "Affordable rates" };
      case "moderate":
        return { label: "₱₱ Moderate", variant: "secondary" as const, desc: "Mid-range pricing" };
      case "luxury":
        return { label: "₱₱₱ Premium", variant: "default" as const, desc: "Premium experience" };
      default:
        return { label: "₱ Accessible", variant: "outline" as const, desc: "Local rates" };
    }
  };

  const getTypeLabel = (type?: string | null) => {
    if (!type) return "Local Business";
    return CATEGORY_CONFIG[type]?.label || type.toUpperCase();
  };

  const getTypeIcon = (type?: string | null) => {
    if (!type) return Store;
    return CATEGORY_CONFIG[type]?.icon || Store;
  };

  return (
    <div className="space-y-8">
      {/* ── Featured Spotlight Banner ── */}
      {featuredSpotlight && !hasActiveFilters && (
        <section className="relative overflow-hidden rounded-3xl border border-border/70 bg-gradient-to-br from-card via-card/95 to-primary/5 p-6 md:p-8 shadow-sm">
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-center">
            {/* Visual Column */}
            <div className="lg:col-span-6 relative rounded-2xl overflow-hidden aspect-[16/10] bg-muted shadow-inner border border-border/40">
              {featuredSpotlight.cover_image_url ? (
                <img
                  src={featuredSpotlight.cover_image_url}
                  alt={featuredSpotlight.name}
                  className="w-full h-full object-cover transition-transform duration-700 hover:scale-105"
                />
              ) : (
                <div className="w-full h-full flex flex-col items-center justify-center bg-gradient-to-br from-primary/10 via-primary/5 to-muted p-6 text-center">
                  {(() => {
                    const IconComp = getTypeIcon(featuredSpotlight.type);
                    return <IconComp className="h-16 w-16 text-primary/40 mb-2" />;
                  })()}
                  <p className="text-xs font-semibold text-primary/70 tracking-wider uppercase">
                    Featured Mangatarem Establishment
                  </p>
                </div>
              )}

              {/* Floating Badges */}
              <div className="absolute top-3 left-3 flex flex-wrap gap-2">
                <Badge className="bg-primary text-primary-foreground font-semibold px-2.5 py-1 shadow-sm">
                  <Sparkles className="h-3 w-3 mr-1" /> Featured Hospitality
                </Badge>
                <Badge variant="secondary" className="backdrop-blur-md bg-background/85 font-medium">
                  {getTypeLabel(featuredSpotlight.type)}
                </Badge>
              </div>

              {featuredSpotlight.price_range && (
                <div className="absolute top-3 right-3 bg-background/90 backdrop-blur-md rounded-xl px-2.5 py-1 text-xs font-semibold shadow-sm border border-border/50">
                  {getPriceBadge(featuredSpotlight.price_range).label}
                </div>
              )}
            </div>

            {/* Content Column */}
            <div className="lg:col-span-6 flex flex-col justify-center space-y-4">
              <div className="space-y-2">
                <div className="flex items-center gap-2 text-xs font-medium text-primary">
                  <ShieldCheck className="h-4 w-4" />
                  <span>Verified Mangatarem Merchant</span>
                </div>

                <h2 className="text-2xl md:text-3xl font-bold tracking-tight text-foreground">
                  {featuredSpotlight.name}
                </h2>

                {featuredSpotlight.description && (
                  <p className="text-muted-foreground text-sm leading-relaxed line-clamp-3">
                    {featuredSpotlight.description}
                  </p>
                )}
              </div>

              {/* Amenities Highlights */}
              {featuredSpotlight.amenities && featuredSpotlight.amenities.length > 0 && (
                <div className="flex flex-wrap gap-2 pt-1">
                  {featuredSpotlight.amenities.slice(0, 4).map((amenity) => {
                    const info = AMENITY_ICONS[amenity.toLowerCase()] || {
                      label: amenity,
                      icon: Check,
                    };
                    const Icon = info.icon;
                    return (
                      <span
                        key={amenity}
                        className="inline-flex items-center gap-1 text-[11px] font-medium bg-muted/80 text-foreground/80 px-2.5 py-1 rounded-lg border border-border/40"
                      >
                        <Icon className="h-3 w-3 text-primary" />
                        {info.label}
                      </span>
                    );
                  })}
                </div>
              )}

              {/* Location and Meta */}
              <div className="flex flex-wrap gap-4 text-xs text-muted-foreground pt-1 border-t border-border/50">
                {featuredSpotlight.address && (
                  <div className="flex items-center gap-1">
                    <MapPin className="h-3.5 w-3.5 text-primary shrink-0" />
                    <span className="line-clamp-1">{featuredSpotlight.address}</span>
                  </div>
                )}
                {featuredSpotlight.contact_number && (
                  <div className="flex items-center gap-1">
                    <Phone className="h-3.5 w-3.5 text-muted-foreground shrink-0" />
                    <span>{featuredSpotlight.contact_number}</span>
                  </div>
                )}
              </div>

              {/* Actions */}
              <div className="flex flex-wrap items-center gap-3 pt-2">
                <Link href={`/business/${featuredSpotlight.id}`}>
                  <Button className="gap-2 shadow-sm font-medium">
                    {featuredSpotlight.type === "inn" ? (
                      <>
                        <Bed className="h-4 w-4" />
                        View Rooms & Rates
                      </>
                    ) : (
                      <>
                        <Utensils className="h-4 w-4" />
                        View Menu & Details
                      </>
                    )}
                    <ArrowRight className="h-4 w-4 ml-0.5" />
                  </Button>
                </Link>

                <Button
                  variant="outline"
                  onClick={(e) => handleShare(e, featuredSpotlight)}
                  className="gap-1.5"
                  aria-label="Share spotlight establishment"
                >
                  {copiedId === featuredSpotlight.id ? (
                    <>
                      <Check className="h-4 w-4 text-primary" />
                      <span>Copied Link</span>
                    </>
                  ) : (
                    <>
                      <Share2 className="h-4 w-4" />
                      <span>Share</span>
                    </>
                  )}
                </Button>
              </div>
            </div>
          </div>
        </section>
      )}

      {/* ── Search & Filter Controls ── */}
      <section className="space-y-4">
        {/* Top Control Row */}
        <div className="flex flex-col md:flex-row gap-3 items-stretch md:items-center justify-between">
          {/* Search Input */}
          <div className="relative flex-1 max-w-md">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
            <Input
              type="text"
              placeholder="Search inns, restaurants, cafes, farms, amenities..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="pl-9 pr-8 h-10 rounded-xl bg-card border-border/70 focus-visible:ring-primary"
              aria-label="Search businesses"
            />
            {searchQuery && (
              <button
                type="button"
                onClick={() => setSearchQuery("")}
                className="absolute right-2.5 top-1/2 -translate-y-1/2 p-1 text-muted-foreground hover:text-foreground rounded-full focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary cursor-pointer"
                aria-label="Clear search text"
              >
                <X className="h-3.5 w-3.5" />
              </button>
            )}
          </div>

          {/* Filters & View Switcher */}
          <div className="flex items-center gap-2 flex-wrap sm:flex-nowrap">
            {/* Price Filter */}
            <div className="relative">
              <select
                value={selectedPrice}
                onChange={(e) => setSelectedPrice(e.target.value)}
                className="h-10 text-xs sm:text-sm rounded-xl border border-border/70 bg-card px-3 py-2 text-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary cursor-pointer"
                aria-label="Filter by Price Tier"
              >
                <option value="all">All Prices</option>
                <option value="budget">₱ Budget</option>
                <option value="moderate">₱₱ Moderate</option>
                <option value="luxury">₱₱₱ Luxury</option>
              </select>
            </div>

            {/* Barangay Filter */}
            <div className="relative">
              <select
                value={selectedBarangay}
                onChange={(e) => setSelectedBarangay(e.target.value)}
                className="h-10 text-xs sm:text-sm rounded-xl border border-border/70 bg-card px-3 py-2 text-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary cursor-pointer"
                aria-label="Filter by Barangay"
              >
                <option value="all">All Barangays</option>
                {availableBarangays.map((b) => (
                  <option key={b} value={b}>
                    {b}
                  </option>
                ))}
              </select>
            </div>

            {/* Sort Selector */}
            <div className="relative">
              <select
                value={sortBy}
                onChange={(e) =>
                  setSortBy(e.target.value as "featured" | "rating" | "name" | "price_asc")
                }
                className="h-10 text-xs sm:text-sm rounded-xl border border-border/70 bg-card px-3 py-2 text-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary cursor-pointer"
                aria-label="Sort Establishments"
              >
                <option value="featured">Featured First</option>
                <option value="rating">Highest Rated</option>
                <option value="price_asc">Price: Low to High</option>
                <option value="name">Name (A-Z)</option>
              </select>
            </div>

            {/* View Mode Switcher */}
            <div className="flex items-center rounded-xl border border-border/70 bg-muted/60 p-1 shrink-0">
              <button
                type="button"
                onClick={() => setViewMode("grid")}
                className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium transition-all cursor-pointer ${
                  viewMode === "grid"
                    ? "bg-card text-foreground shadow-xs"
                    : "text-muted-foreground hover:text-foreground"
                }`}
                aria-label="Grid View"
              >
                <LayoutGrid className="h-3.5 w-3.5" />
                <span className="hidden sm:inline">Grid</span>
              </button>
              <button
                type="button"
                onClick={() => setViewMode("list")}
                className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium transition-all cursor-pointer ${
                  viewMode === "list"
                    ? "bg-card text-foreground shadow-xs"
                    : "text-muted-foreground hover:text-foreground"
                }`}
                aria-label="List View"
              >
                <List className="h-3.5 w-3.5" />
                <span className="hidden sm:inline">List</span>
              </button>
            </div>
          </div>
        </div>

        {/* Category Pills Bar */}
        <div className="flex items-center gap-2 overflow-x-auto pb-1 pt-1 no-scrollbar flex-wrap">
          <Button
            variant={selectedType === "all" ? "default" : "outline"}
            size="sm"
            onClick={() => setSelectedType("all")}
            className="rounded-full text-xs font-medium transition-all"
          >
            <Store className="h-3.5 w-3.5 mr-1.5" />
            All Categories
            <span className="ml-1.5 px-1.5 py-0.2 rounded-full text-[10px] bg-background/20">
              {establishments.length}
            </span>
          </Button>

          {availableTypes.map((t) => {
            const count = establishments.filter((e) => e.type === t).length;
            const isSelected = selectedType === t;
            const config = CATEGORY_CONFIG[t] || {
              label: t.toUpperCase(),
              icon: Building2,
            };
            const Icon = config.icon;
            return (
              <Button
                key={t}
                variant={isSelected ? "default" : "outline"}
                size="sm"
                onClick={() => setSelectedType(t)}
                className="rounded-full text-xs font-medium transition-all"
              >
                <Icon className="h-3.5 w-3.5 mr-1.5" />
                {config.label}
                <span className="ml-1.5 px-1.5 py-0.2 rounded-full text-[10px] bg-muted">
                  {count}
                </span>
              </Button>
            );
          })}
        </div>

        {/* Quick Amenities Filter Bar */}
        <div className="flex items-center gap-1.5 overflow-x-auto pb-1 text-xs text-muted-foreground flex-wrap">
          <span className="font-semibold text-foreground/80 mr-1 text-[11px] uppercase tracking-wider">
            Amenities:
          </span>
          {Object.entries(AMENITY_ICONS).map(([key, item]) => {
            const isSelected = selectedAmenity === key;
            const Icon = item.icon;
            return (
              <button
                key={key}
                type="button"
                onClick={() => setSelectedAmenity(isSelected ? "all" : key)}
                className={`inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-xs font-medium border transition-all cursor-pointer ${
                  isSelected
                    ? "bg-primary text-primary-foreground border-primary"
                    : "bg-card hover:bg-muted/70 text-foreground/80 border-border/70"
                }`}
              >
                <Icon className="h-3 w-3" />
                <span>{item.label}</span>
              </button>
            );
          })}
        </div>

        {/* Active Filter Chips & Feedback Bar */}
        {hasActiveFilters && (
          <div className="flex items-center justify-between text-xs text-muted-foreground bg-muted/40 px-3 py-2 rounded-xl border border-border/40">
            <div className="flex items-center gap-2 flex-wrap">
              <SlidersHorizontal className="h-3.5 w-3.5 text-primary" />
              <span>
                Showing <strong>{filteredBusinesses.length}</strong> of {establishments.length}{" "}
                establishments
              </span>

              {searchQuery && (
                <Badge variant="secondary" className="gap-1 text-[11px] py-0 px-2">
                  &quot;{searchQuery}&quot;
                  <button onClick={() => setSearchQuery("")} className="hover:text-foreground">
                    <X className="h-2.5 w-2.5" />
                  </button>
                </Badge>
              )}

              {selectedType !== "all" && (
                <Badge variant="secondary" className="gap-1 text-[11px] py-0 px-2">
                  Category: {getTypeLabel(selectedType)}
                  <button onClick={() => setSelectedType("all")} className="hover:text-foreground">
                    <X className="h-2.5 w-2.5" />
                  </button>
                </Badge>
              )}

              {selectedPrice !== "all" && (
                <Badge variant="secondary" className="gap-1 text-[11px] py-0 px-2 capitalize">
                  Price: {selectedPrice}
                  <button onClick={() => setSelectedPrice("all")} className="hover:text-foreground">
                    <X className="h-2.5 w-2.5" />
                  </button>
                </Badge>
              )}

              {selectedBarangay !== "all" && (
                <Badge variant="secondary" className="gap-1 text-[11px] py-0 px-2">
                  Barangay: {selectedBarangay}
                  <button
                    onClick={() => setSelectedBarangay("all")}
                    className="hover:text-foreground"
                  >
                    <X className="h-2.5 w-2.5" />
                  </button>
                </Badge>
              )}

              {selectedAmenity !== "all" && (
                <Badge variant="secondary" className="gap-1 text-[11px] py-0 px-2">
                  Amenity: {AMENITY_ICONS[selectedAmenity]?.label || selectedAmenity}
                  <button
                    onClick={() => setSelectedAmenity("all")}
                    className="hover:text-foreground"
                  >
                    <X className="h-2.5 w-2.5" />
                  </button>
                </Badge>
              )}
            </div>

            <button
              onClick={handleClearFilters}
              className="text-primary hover:underline font-medium ml-2 shrink-0 cursor-pointer"
            >
              Reset filters
            </button>
          </div>
        )}
      </section>

      {/* ── Establishments Display (Grid or List) ── */}
      {filteredBusinesses.length === 0 ? (
        <div className="text-center py-16 px-4 border border-dashed rounded-3xl border-border/80 bg-card/40">
          <Store className="h-12 w-12 mx-auto mb-3 text-muted-foreground/40" />
          <h3 className="text-lg font-semibold text-foreground">No establishments found</h3>
          <p className="text-sm text-muted-foreground mt-1 max-w-sm mx-auto">
            We couldn&apos;t find any businesses matching your search criteria. Try adjusting your
            filters or search terms.
          </p>
          {hasActiveFilters && (
            <Button
              variant="outline"
              size="sm"
              onClick={handleClearFilters}
              className="mt-4 rounded-xl"
            >
              Clear All Filters
            </Button>
          )}
        </div>
      ) : viewMode === "grid" ? (
        /* ── Grid View ── */
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredBusinesses.map((b) => {
            const priceMeta = getPriceBadge(b.price_range);
            const IconComponent = getTypeIcon(b.type);
            const barangayDisplay = b.barangay_name || b.barangay;

            return (
              <Link
                key={b.id}
                href={`/business/${b.id}`}
                className="group focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary focus-visible:ring-offset-2 rounded-2xl"
              >
                <Card className="h-full overflow-hidden border-border/70 bg-card hover:border-primary/40 hover:shadow-md transition-all duration-300 hover:-translate-y-1 flex flex-col justify-between">
                  <div>
                    {/* Media Banner */}
                    <div className="aspect-[16/10] bg-muted relative overflow-hidden">
                      {b.cover_image_url ? (
                        <img
                          src={b.cover_image_url}
                          alt={b.name}
                          className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
                        />
                      ) : (
                        <div className="w-full h-full flex flex-col items-center justify-center bg-gradient-to-br from-primary/10 via-primary/5 to-muted p-4 text-center">
                          <IconComponent className="h-12 w-12 text-primary/30 mb-1" />
                          <span className="text-[11px] font-semibold text-muted-foreground/70 uppercase tracking-wider">
                            {getTypeLabel(b.type)}
                          </span>
                        </div>
                      )}

                      {/* Top Category Badge */}
                      <div className="absolute top-3 left-3 flex gap-1.5">
                        <Badge
                          variant="secondary"
                          className="text-xs bg-background/90 backdrop-blur-md shadow-xs font-medium"
                        >
                          <IconComponent className="h-3 w-3 mr-1 text-primary" />
                          {getTypeLabel(b.type)}
                        </Badge>
                        {b.is_featured && (
                          <Badge className="bg-primary text-primary-foreground text-xs shadow-xs">
                            <Sparkles className="h-3 w-3 mr-0.5" /> Featured
                          </Badge>
                        )}
                      </div>

                      {/* Price Badge */}
                      {b.price_range && (
                        <div className="absolute top-3 right-3 bg-background/90 backdrop-blur-md rounded-lg px-2 py-0.5 text-xs font-semibold shadow-xs border border-border/40">
                          {priceMeta.label}
                        </div>
                      )}
                    </div>

                    {/* Card Content */}
                    <CardContent className="p-5 space-y-3">
                      <div>
                        <h3 className="font-bold text-base text-foreground leading-snug line-clamp-1 group-hover:text-primary transition-colors">
                          {b.name}
                        </h3>

                        {/* Rating and Reviews */}
                        <div className="flex items-center gap-2 mt-1 text-xs">
                          {b.rating_avg && b.rating_avg > 0 ? (
                            <span className="flex items-center gap-0.5 font-bold text-foreground">
                              <Star className="h-3.5 w-3.5 fill-amber-400 text-amber-400" />
                              {b.rating_avg.toFixed(1)}
                              <span className="text-muted-foreground font-normal ml-0.5">
                                ({b.review_count || 0})
                              </span>
                            </span>
                          ) : (
                            <span className="text-muted-foreground text-[11px]">
                              ★ New Mangatarem listing
                            </span>
                          )}

                          {barangayDisplay && (
                            <span className="text-muted-foreground flex items-center gap-1">
                              • <MapPin className="h-3 w-3 text-primary" /> Brgy. {barangayDisplay}
                            </span>
                          )}
                        </div>
                      </div>

                      {b.description && (
                        <p className="text-xs text-muted-foreground line-clamp-2 leading-relaxed">
                          {b.description}
                        </p>
                      )}

                      {/* Amenities Pills Preview */}
                      {b.amenities && b.amenities.length > 0 && (
                        <div className="flex flex-wrap gap-1.5 pt-1">
                          {b.amenities.slice(0, 3).map((a) => {
                            const info = AMENITY_ICONS[a.toLowerCase()] || {
                              label: a,
                              icon: Check,
                            };
                            const Icon = info.icon;
                            return (
                              <span
                                key={a}
                                className="inline-flex items-center gap-1 text-[10px] font-medium bg-muted px-2 py-0.5 rounded-md text-foreground/70"
                              >
                                <Icon className="h-2.5 w-2.5 text-primary" />
                                {info.label}
                              </span>
                            );
                          })}
                          {b.amenities.length > 3 && (
                            <span className="text-[10px] text-muted-foreground self-center">
                              +{b.amenities.length - 3} more
                            </span>
                          )}
                        </div>
                      )}
                    </CardContent>
                  </div>

                  {/* Card Footer Action */}
                  <div className="px-5 pb-4 pt-0 flex items-center justify-between text-xs text-muted-foreground border-t border-border/40 mt-2">
                    <span className="text-[11px] text-foreground/70 font-medium">
                      {b.type === "inn" ? "Rooms & Accommodations" : "Menu & Local Specials"}
                    </span>
                    <span className="text-primary font-semibold flex items-center gap-1 group-hover:translate-x-0.5 transition-transform">
                      Explore <ArrowRight className="h-3 w-3" />
                    </span>
                  </div>
                </Card>
              </Link>
            );
          })}
        </div>
      ) : (
        /* ── List / Compact View ── */
        <div className="space-y-4 max-w-4xl mx-auto">
          {filteredBusinesses.map((b) => {
            const priceMeta = getPriceBadge(b.price_range);
            const IconComponent = getTypeIcon(b.type);
            const barangayDisplay = b.barangay_name || b.barangay;

            return (
              <Link
                key={b.id}
                href={`/business/${b.id}`}
                className="block group focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary rounded-2xl"
              >
                <Card className="p-4 md:p-5 border-border/70 hover:border-primary/40 hover:shadow-md transition-all duration-300 hover:-translate-y-0.5 bg-card">
                  <div className="grid grid-cols-1 md:grid-cols-12 gap-4 items-center">
                    {/* Visual Icon / Thumbnail */}
                    <div className="md:col-span-3 aspect-[16/10] md:aspect-square rounded-xl bg-muted overflow-hidden relative">
                      {b.cover_image_url ? (
                        <img
                          src={b.cover_image_url}
                          alt={b.name}
                          className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
                        />
                      ) : (
                        <div className="w-full h-full flex flex-col items-center justify-center bg-gradient-to-br from-primary/10 via-primary/5 to-muted p-2 text-center">
                          <IconComponent className="h-10 w-10 text-primary/35 mb-1" />
                          <span className="text-[10px] font-semibold text-muted-foreground/70 uppercase">
                            {getTypeLabel(b.type)}
                          </span>
                        </div>
                      )}

                      {b.is_featured && (
                        <Badge className="absolute top-2 left-2 bg-primary text-primary-foreground text-[10px] py-0 px-1.5">
                          Featured
                        </Badge>
                      )}
                    </div>

                    {/* Content Details */}
                    <div className="md:col-span-7 space-y-2">
                      <div className="flex items-center gap-2 flex-wrap">
                        <h3 className="font-bold text-base text-foreground group-hover:text-primary transition-colors">
                          {b.name}
                        </h3>
                        <Badge variant="secondary" className="text-[11px] py-0 px-2">
                          {getTypeLabel(b.type)}
                        </Badge>
                        {b.price_range && (
                          <span className="text-xs font-semibold text-muted-foreground">
                            {priceMeta.label}
                          </span>
                        )}
                      </div>

                      {b.description && (
                        <p className="text-xs text-muted-foreground line-clamp-2 leading-relaxed">
                          {b.description}
                        </p>
                      )}

                      <div className="flex items-center gap-3 text-xs text-muted-foreground flex-wrap pt-1">
                        {b.address && (
                          <span className="flex items-center gap-1">
                            <MapPin className="h-3 w-3 text-primary shrink-0" />
                            <span className="truncate max-w-xs">{b.address}</span>
                          </span>
                        )}
                        {barangayDisplay && (
                          <span className="text-[11px] bg-muted px-1.5 py-0.5 rounded text-foreground/80">
                            Brgy. {barangayDisplay}
                          </span>
                        )}
                        {b.contact_number && (
                          <span className="flex items-center gap-1">
                            <Phone className="h-3 w-3 text-muted-foreground shrink-0" />
                            {b.contact_number}
                          </span>
                        )}
                      </div>
                    </div>

                    {/* Action Button */}
                    <div className="md:col-span-2 flex justify-end">
                      <Button
                        variant="outline"
                        size="sm"
                        className="w-full md:w-auto text-xs gap-1 group-hover:bg-primary group-hover:text-primary-foreground transition-all"
                      >
                        {b.type === "inn" ? "Rooms" : "Menu"}
                        <ArrowRight className="h-3 w-3" />
                      </Button>
                    </div>
                  </div>
                </Card>
              </Link>
            );
          })}
        </div>
      )}

      {/* ── Merchant Community Support Card ── */}
      <section className="rounded-3xl border border-primary/20 bg-gradient-to-br from-primary/5 via-card to-background p-6 md:p-8 flex flex-col md:flex-row items-center justify-between gap-6 shadow-xs">
        <div className="space-y-1.5 text-center md:text-left">
          <div className="flex items-center gap-2 justify-center md:justify-start text-xs font-semibold text-primary">
            <Compass className="h-4 w-4" />
            <span>Mangatarem Local Business Initiative</span>
          </div>
          <h3 className="text-lg md:text-xl font-bold text-foreground">
            Own a local business, inn, or restaurant in Mangatarem?
          </h3>
          <p className="text-xs md:text-sm text-muted-foreground max-w-xl">
            Partner with the Municipality of Mangatarem Tourism Office to list your rooms, menu
            specials, and agro-tourism activities on the official digital cultural map.
          </p>
        </div>

        <div className="flex items-center gap-3 shrink-0">
          <Link href="/auth/register">
            <Button className="shadow-sm">
              Register as Business
              <ArrowRight className="h-4 w-4 ml-1.5" />
            </Button>
          </Link>
        </div>
      </section>
    </div>
  );
}
