"use client";

import { useState, useMemo } from "react";
import Link from "next/link";
import {
  Calendar,
  MapPin,
  Search,
  SlidersHorizontal,
  Sparkles,
  ArrowRight,
  Clock,
  LayoutGrid,
  ListFilter,
  CalendarDays,
  X,
  Share2,
  Check,
} from "lucide-react";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

export interface EventItem {
  id: number;
  name: string;
  category?: string;
  date?: string;
  location?: string;
  image_url?: string;
  barangay_name?: string;
  description?: string;
  status?: string;
}

interface EventsViewProps {
  events: EventItem[];
}

export function EventsView({ events }: EventsViewProps) {
  const [searchQuery, setSearchQuery] = useState("");
  const [selectedCategory, setSelectedCategory] = useState<string>("all");
  const [timeFilter, setTimeFilter] = useState<"all" | "upcoming" | "past">("all");
  const [selectedBarangay, setSelectedBarangay] = useState<string>("all");
  const [viewMode, setViewMode] = useState<"grid" | "timeline">("grid");
  const [copiedId, setCopiedId] = useState<number | null>(null);

  // Extract unique categories and barangays with counts
  const categories = useMemo(() => {
    const cats = new Set<string>();
    events.forEach((e) => {
      if (e.category) cats.add(e.category);
    });
    return Array.from(cats);
  }, [events]);

  const barangays = useMemo(() => {
    const bars = new Set<string>();
    events.forEach((e) => {
      if (e.barangay_name) bars.add(e.barangay_name);
    });
    return Array.from(bars);
  }, [events]);

  // Featured Spotlight Event (find premier festival like Tupig Festival or earliest upcoming)
  const featuredEvent = useMemo(() => {
    if (events.length === 0) return null;
    const tupig = events.find((e) => e.name.toLowerCase().includes("tupig"));
    return tupig || events[0];
  }, [events]);

  // Filtered Events
  const filteredEvents = useMemo(() => {
    const now = new Date();
    return events.filter((event) => {
      // Search match
      if (searchQuery.trim()) {
        const q = searchQuery.toLowerCase();
        const matchName = event.name.toLowerCase().includes(q);
        const matchLoc = event.location?.toLowerCase().includes(q) || false;
        const matchBarangay = event.barangay_name?.toLowerCase().includes(q) || false;
        const matchDesc = event.description?.toLowerCase().includes(q) || false;
        const matchCat = event.category?.toLowerCase().includes(q) || false;
        if (!matchName && !matchLoc && !matchBarangay && !matchDesc && !matchCat) {
          return false;
        }
      }

      // Category match
      if (selectedCategory !== "all" && event.category !== selectedCategory) {
        return false;
      }

      // Barangay match
      if (selectedBarangay !== "all" && event.barangay_name !== selectedBarangay) {
        return false;
      }

      // Time filter
      if (event.date) {
        const eventDate = new Date(event.date);
        if (timeFilter === "upcoming" && eventDate < now) return false;
        if (timeFilter === "past" && eventDate >= now) return false;
      }

      return true;
    });
  }, [events, searchQuery, selectedCategory, selectedBarangay, timeFilter]);

  // Chronologically group for timeline view
  const timelineGroups = useMemo(() => {
    const groups: { [key: string]: EventItem[] } = {};
    const sorted = [...filteredEvents].sort((a, b) => {
      const dateA = a.date ? new Date(a.date).getTime() : 0;
      const dateB = b.date ? new Date(b.date).getTime() : 0;
      return dateB - dateA;
    });

    sorted.forEach((event) => {
      let monthYear = "Dates TBA";
      if (event.date) {
        const d = new Date(event.date);
        monthYear = d.toLocaleDateString("en-PH", { month: "long", year: "numeric" });
      }
      if (!groups[monthYear]) {
        groups[monthYear] = [];
      }
      groups[monthYear].push(event);
    });

    return Object.entries(groups);
  }, [filteredEvents]);

  const hasActiveFilters =
    searchQuery.trim() !== "" ||
    selectedCategory !== "all" ||
    selectedBarangay !== "all" ||
    timeFilter !== "all";

  const handleClearFilters = () => {
    setSearchQuery("");
    setSelectedCategory("all");
    setSelectedBarangay("all");
    setTimeFilter("all");
  };

  const handleShare = async (e: React.MouseEvent, event: EventItem) => {
    e.preventDefault();
    e.stopPropagation();
    const url = `${window.location.origin}/events/${event.id}`;
    if (navigator.share) {
      try {
        await navigator.share({
          title: event.name,
          text: `Check out ${event.name} in Mangatarem, Pangasinan!`,
          url: url,
        });
        return;
      } catch {
        // Fallback to clipboard
      }
    }
    navigator.clipboard.writeText(url);
    setCopiedId(event.id);
    setTimeout(() => setCopiedId(null), 2000);
  };

  const formatEventDate = (dateStr?: string) => {
    if (!dateStr) return { month: "TBA", day: "—", time: "", full: "Date to be announced" };
    const d = new Date(dateStr);
    return {
      month: d.toLocaleDateString("en-PH", { month: "short" }).toUpperCase(),
      day: d.getDate(),
      time: d.toLocaleTimeString("en-PH", { hour: "numeric", minute: "2-digit" }),
      full: d.toLocaleDateString("en-PH", {
        weekday: "short",
        month: "short",
        day: "numeric",
        year: "numeric",
      }),
    };
  };

  return (
    <div className="space-y-8">
      {/* ── Featured Spotlight Banner ── */}
      {featuredEvent && !hasActiveFilters && (
        <section className="relative overflow-hidden rounded-2xl border border-border/60 bg-gradient-to-br from-card via-card/90 to-primary/5 p-6 md:p-8 shadow-sm">
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-center">
            {/* Visual Column */}
            <div className="lg:col-span-6 relative rounded-xl overflow-hidden aspect-[16/10] bg-muted shadow-inner">
              {featuredEvent.image_url ? (
                <img
                  src={featuredEvent.image_url}
                  alt={featuredEvent.name}
                  className="w-full h-full object-cover transition-transform duration-700 hover:scale-105"
                />
              ) : (
                <div className="w-full h-full flex items-center justify-center bg-primary/10">
                  <Calendar className="h-16 w-16 text-primary/40" />
                </div>
              )}
              <div className="absolute top-3 left-3 flex gap-2">
                <Badge className="bg-primary text-primary-foreground font-semibold px-2.5 py-1 shadow-sm">
                  <Sparkles className="h-3 w-3 mr-1" /> Spotlight Festival
                </Badge>
                {featuredEvent.category && (
                  <Badge variant="secondary" className="backdrop-blur-md bg-background/80">
                    {featuredEvent.category}
                  </Badge>
                )}
              </div>
            </div>

            {/* Content Column */}
            <div className="lg:col-span-6 flex flex-col justify-center space-y-4">
              <div className="space-y-2">
                <div className="flex items-center gap-2 text-sm text-primary font-medium">
                  <CalendarDays className="h-4 w-4" />
                  <span>
                    {featuredEvent.date
                      ? formatEventDate(featuredEvent.date).full
                      : "Annual Celebration"}
                  </span>
                </div>
                <h2 className="text-2xl md:text-3xl font-bold tracking-tight text-foreground">
                  {featuredEvent.name}
                </h2>
                {featuredEvent.description && (
                  <p className="text-muted-foreground text-sm leading-relaxed line-clamp-3">
                    {featuredEvent.description}
                  </p>
                )}
              </div>

              {/* Meta information */}
              <div className="flex flex-wrap gap-4 text-xs text-muted-foreground pt-1 border-t border-border/40">
                {featuredEvent.location && (
                  <div className="flex items-center gap-1">
                    <MapPin className="h-3.5 w-3.5 text-primary" />
                    <span>{featuredEvent.location}</span>
                  </div>
                )}
                {featuredEvent.barangay_name && (
                  <div className="flex items-center gap-1">
                    <span className="font-semibold text-foreground/80">Barangay:</span>
                    <span>{featuredEvent.barangay_name}</span>
                  </div>
                )}
                {featuredEvent.date && (
                  <div className="flex items-center gap-1">
                    <Clock className="h-3.5 w-3.5 text-muted-foreground" />
                    <span>{formatEventDate(featuredEvent.date).time}</span>
                  </div>
                )}
              </div>

              {/* Action buttons */}
              <div className="flex flex-wrap items-center gap-3 pt-2">
                <Link href={`/events/${featuredEvent.id}`}>
                  <Button className="gap-2 shadow-sm font-medium">
                    Explore Festival Guide
                    <ArrowRight className="h-4 w-4" />
                  </Button>
                </Link>
                <Button
                  variant="outline"
                  size="default"
                  onClick={(e) => handleShare(e, featuredEvent)}
                  className="gap-1.5"
                  aria-label="Share spotlight festival"
                >
                  {copiedId === featuredEvent.id ? (
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

      {/* ── Filters & Search Control Bar ── */}
      <section className="space-y-4">
        <div className="flex flex-col md:flex-row gap-3 items-stretch md:items-center justify-between">
          {/* Search Input */}
          <div className="relative flex-1 max-w-md">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
            <Input
              type="text"
              placeholder="Search events, festivals, venues, or barangays..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="pl-9 pr-8 h-10 rounded-xl bg-card border-border/70 focus-visible:ring-primary"
              aria-label="Search events"
            />
            {searchQuery && (
              <button
                type="button"
                onClick={() => setSearchQuery("")}
                className="absolute right-2.5 top-1/2 -translate-y-1/2 p-1 text-muted-foreground hover:text-foreground rounded-full focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary"
                aria-label="Clear search text"
              >
                <X className="h-3.5 w-3.5" />
              </button>
            )}
          </div>

          {/* View Mode & Barangay Select */}
          <div className="flex items-center gap-2 flex-wrap sm:flex-nowrap">
            {/* Barangay selector */}
            <div className="relative">
              <select
                value={selectedBarangay}
                onChange={(e) => setSelectedBarangay(e.target.value)}
                className="h-10 text-xs sm:text-sm rounded-xl border border-border/70 bg-card px-3 py-2 text-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary cursor-pointer"
                aria-label="Filter by Barangay"
              >
                <option value="all">All Barangays</option>
                {barangays.map((b) => (
                  <option key={b} value={b}>
                    {b}
                  </option>
                ))}
              </select>
            </div>

            {/* Time Filter Select */}
            <div className="relative">
              <select
                value={timeFilter}
                onChange={(e) => setTimeFilter(e.target.value as "all" | "upcoming" | "past")}
                className="h-10 text-xs sm:text-sm rounded-xl border border-border/70 bg-card px-3 py-2 text-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary cursor-pointer"
                aria-label="Filter by Time"
              >
                <option value="all">All Dates</option>
                <option value="upcoming">Upcoming</option>
                <option value="past">Past Events</option>
              </select>
            </div>

            {/* View Mode Switcher */}
            <div className="flex items-center rounded-xl border border-border/70 bg-muted/60 p-1">
              <button
                type="button"
                onClick={() => setViewMode("grid")}
                className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium transition-all ${
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
                onClick={() => setViewMode("timeline")}
                className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium transition-all ${
                  viewMode === "timeline"
                    ? "bg-card text-foreground shadow-xs"
                    : "text-muted-foreground hover:text-foreground"
                }`}
                aria-label="Timeline View"
              >
                <ListFilter className="h-3.5 w-3.5" />
                <span className="hidden sm:inline">Timeline</span>
              </button>
            </div>
          </div>
        </div>

        {/* Category Pills Bar */}
        <div className="flex items-center gap-2 overflow-x-auto pb-1 pt-1 no-scrollbar flex-wrap">
          <Button
            variant={selectedCategory === "all" ? "default" : "outline"}
            size="sm"
            onClick={() => setSelectedCategory("all")}
            className="rounded-full text-xs font-medium transition-all"
          >
            All Categories
            <span className="ml-1.5 px-1.5 py-0.2 rounded-full text-[10px] bg-background/20">
              {events.length}
            </span>
          </Button>

          {categories.map((cat) => {
            const count = events.filter((e) => e.category === cat).length;
            const isSelected = selectedCategory === cat;
            return (
              <Button
                key={cat}
                variant={isSelected ? "default" : "outline"}
                size="sm"
                onClick={() => setSelectedCategory(cat)}
                className="rounded-full text-xs font-medium transition-all"
              >
                {cat}
                <span className="ml-1.5 px-1.5 py-0.2 rounded-full text-[10px] bg-muted">
                  {count}
                </span>
              </Button>
            );
          })}
        </div>

        {/* Active Filter Chips & Feedback Bar */}
        {hasActiveFilters && (
          <div className="flex items-center justify-between text-xs text-muted-foreground bg-muted/40 px-3 py-2 rounded-xl border border-border/40">
            <div className="flex items-center gap-2 flex-wrap">
              <SlidersHorizontal className="h-3.5 w-3.5 text-primary" />
              <span>
                Showing <strong>{filteredEvents.length}</strong> of {events.length} events
              </span>
              {searchQuery && (
                <Badge variant="secondary" className="gap-1 text-[11px] py-0 px-2">
                  &quot;{searchQuery}&quot;
                  <button onClick={() => setSearchQuery("")} className="hover:text-foreground">
                    <X className="h-2.5 w-2.5" />
                  </button>
                </Badge>
              )}
              {selectedCategory !== "all" && (
                <Badge variant="secondary" className="gap-1 text-[11px] py-0 px-2">
                  Category: {selectedCategory}
                  <button onClick={() => setSelectedCategory("all")} className="hover:text-foreground">
                    <X className="h-2.5 w-2.5" />
                  </button>
                </Badge>
              )}
              {selectedBarangay !== "all" && (
                <Badge variant="secondary" className="gap-1 text-[11px] py-0 px-2">
                  Barangay: {selectedBarangay}
                  <button onClick={() => setSelectedBarangay("all")} className="hover:text-foreground">
                    <X className="h-2.5 w-2.5" />
                  </button>
                </Badge>
              )}
              {timeFilter !== "all" && (
                <Badge variant="secondary" className="gap-1 text-[11px] py-0 px-2 capitalize">
                  {timeFilter}
                  <button onClick={() => setTimeFilter("all")} className="hover:text-foreground">
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

      {/* ── Events Display (Grid or Timeline) ── */}
      {filteredEvents.length === 0 ? (
        <div className="text-center py-16 px-4 border border-dashed rounded-2xl border-border/80 bg-card/40">
          <Calendar className="h-12 w-12 mx-auto mb-3 text-muted-foreground/40" />
          <h3 className="text-lg font-semibold text-foreground">No events found</h3>
          <p className="text-sm text-muted-foreground mt-1 max-w-sm mx-auto">
            We couldn&apos;t find any events matching your search criteria. Try adjusting your filters or search terms.
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
          {filteredEvents.map((e) => {
            const dateMeta = formatEventDate(e.date);
            return (
              <Link
                key={e.id}
                href={`/events/${e.id}`}
                className="group focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary focus-visible:ring-offset-2 rounded-2xl"
              >
                <Card className="h-full overflow-hidden border-border/60 bg-card hover:border-primary/40 hover:shadow-md transition-all duration-300 hover:-translate-y-1 flex flex-col justify-between">
                  <div>
                    {/* Card Media Header */}
                    <div className="aspect-[16/10] bg-muted relative overflow-hidden">
                      {e.image_url ? (
                        <img
                          src={e.image_url}
                          alt={e.name}
                          className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
                        />
                      ) : (
                        <div className="w-full h-full flex items-center justify-center bg-primary/5">
                          <Calendar className="h-10 w-10 text-primary/25" />
                        </div>
                      )}

                      {/* Category Badge */}
                      {e.category && (
                        <Badge
                          variant="secondary"
                          className="absolute top-3 left-3 text-xs bg-background/90 backdrop-blur-md shadow-xs"
                        >
                          {e.category}
                        </Badge>
                      )}

                      {/* Date Badge */}
                      {e.date && (
                        <div className="absolute top-3 right-3 bg-background/95 backdrop-blur-md rounded-xl p-1.5 px-2.5 text-center shadow-sm border border-border/40">
                          <p className="text-[10px] font-bold text-primary tracking-wider uppercase leading-none">
                            {dateMeta.month}
                          </p>
                          <p className="text-base font-extrabold text-foreground leading-tight">
                            {dateMeta.day}
                          </p>
                        </div>
                      )}
                    </div>

                    {/* Card Body */}
                    <CardContent className="p-5 space-y-2.5">
                      <h3 className="font-bold text-base text-foreground leading-snug line-clamp-2 group-hover:text-primary transition-colors">
                        {e.name}
                      </h3>

                      {e.description && (
                        <p className="text-xs text-muted-foreground line-clamp-2 leading-relaxed">
                          {e.description}
                        </p>
                      )}

                      <div className="space-y-1 pt-1 text-xs text-muted-foreground">
                        {e.location && (
                          <div className="flex items-center gap-1.5">
                            <MapPin className="h-3.5 w-3.5 text-primary shrink-0" />
                            <span className="truncate">{e.location}</span>
                          </div>
                        )}
                        {e.barangay_name && (
                          <div className="flex items-center gap-1.5 pl-5">
                            <span className="text-[11px] bg-muted px-1.5 py-0.5 rounded-md text-foreground/70">
                              Brgy. {e.barangay_name}
                            </span>
                          </div>
                        )}
                      </div>
                    </CardContent>
                  </div>

                  {/* Card Action Footer */}
                  <div className="px-5 pb-4 pt-0 flex items-center justify-between text-xs text-muted-foreground border-t border-border/30 mt-2">
                    <span className="font-medium text-foreground/70">{dateMeta.full}</span>
                    <span className="text-primary font-semibold flex items-center gap-1 group-hover:translate-x-0.5 transition-transform">
                      Details <ArrowRight className="h-3 w-3" />
                    </span>
                  </div>
                </Card>
              </Link>
            );
          })}
        </div>
      ) : (
        /* ── Timeline View ── */
        <div className="space-y-10 max-w-4xl mx-auto">
          {timelineGroups.map(([monthYear, monthEvents]) => (
            <div key={monthYear} className="space-y-4">
              {/* Month Header Banner */}
              <div className="sticky top-16 z-10 flex items-center gap-3 bg-background/95 backdrop-blur-md py-2 border-b border-border/60">
                <div className="flex h-7 w-7 items-center justify-center rounded-lg bg-primary/10 text-primary">
                  <CalendarDays className="h-4 w-4" />
                </div>
                <h3 className="text-base font-bold tracking-tight text-foreground">
                  {monthYear}
                </h3>
                <span className="text-xs text-muted-foreground font-medium">
                  ({monthEvents.length} event{monthEvents.length > 1 ? "s" : ""})
                </span>
              </div>

              {/* Event Nodes List */}
              <div className="relative pl-6 space-y-4 before:absolute before:left-2.5 before:top-3 before:bottom-3 before:w-0.5 before:bg-border">
                {monthEvents.map((e) => {
                  const dateMeta = formatEventDate(e.date);
                  return (
                    <div key={e.id} className="relative group">
                      {/* Timeline dot */}
                      <div className="absolute -left-6 top-5 flex h-4 w-4 items-center justify-center rounded-full bg-background border-2 border-primary group-hover:scale-125 transition-transform" />

                      {/* Timeline Card */}
                      <Link
                        href={`/events/${e.id}`}
                        className="block focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary rounded-xl"
                      >
                        <Card className="p-4 md:p-5 border-border/60 hover:border-primary/40 hover:shadow-md transition-all duration-300 hover:-translate-y-0.5 bg-card">
                          <div className="grid grid-cols-1 md:grid-cols-12 gap-4 items-center">
                            {/* Date Column */}
                            <div className="md:col-span-2 flex md:flex-col items-center justify-start md:justify-center text-left md:text-center p-2 rounded-xl bg-muted/60 border border-border/40">
                              <span className="text-xs font-bold text-primary uppercase">
                                {dateMeta.month}
                              </span>
                              <span className="text-xl md:text-2xl font-black text-foreground md:my-0.5 ml-2 md:ml-0">
                                {dateMeta.day}
                              </span>
                              {dateMeta.time && (
                                <span className="text-[10px] text-muted-foreground ml-auto md:ml-0">
                                  {dateMeta.time}
                                </span>
                              )}
                            </div>

                            {/* Info Column */}
                            <div className="md:col-span-8 space-y-1.5">
                              <div className="flex items-center gap-2 flex-wrap">
                                <h4 className="font-bold text-base text-foreground group-hover:text-primary transition-colors">
                                  {e.name}
                                </h4>
                                {e.category && (
                                  <Badge variant="secondary" className="text-[11px] py-0 px-2">
                                    {e.category}
                                  </Badge>
                                )}
                              </div>

                              {e.description && (
                                <p className="text-xs text-muted-foreground line-clamp-2 leading-relaxed">
                                  {e.description}
                                </p>
                              )}

                              <div className="flex items-center gap-3 text-xs text-muted-foreground flex-wrap pt-1">
                                {e.location && (
                                  <span className="flex items-center gap-1">
                                    <MapPin className="h-3 w-3 text-primary" />
                                    {e.location}
                                  </span>
                                )}
                                {e.barangay_name && (
                                  <span>Brgy. {e.barangay_name}</span>
                                )}
                              </div>
                            </div>

                            {/* Action CTA */}
                            <div className="md:col-span-2 flex justify-end">
                              <Button
                                variant="outline"
                                size="sm"
                                className="w-full md:w-auto text-xs gap-1 group-hover:bg-primary group-hover:text-primary-foreground transition-all"
                              >
                                View
                                <ArrowRight className="h-3 w-3" />
                              </Button>
                            </div>
                          </div>
                        </Card>
                      </Link>
                    </div>
                  );
                })}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
