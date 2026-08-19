"use client";

import { useState } from "react";
import Link from "next/link";
import {
  MapPin,
  Star,
  ArrowLeft,
  Share2,
  Check,
  Heart,
  Navigation,
  ExternalLink,
  ShieldCheck,
  Clock,
  Coins,
  Compass,
  TreePine,
  Landmark,
  Building,
  CheckCircle2,
  AlertCircle,
  Footprints,
  Car,
  Utensils,
  Hotel,
  ChevronRight,
  Eye,
  Info,
  Maximize2,
  X,
  Sparkles,
} from "lucide-react";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button, buttonVariants } from "@/components/ui/button";
import { Separator } from "@/components/ui/separator";
import { ReviewForm } from "@/components/review-form";
import {
  AttractionItem,
  AttractionReviewItem,
  AttractionReviewSummary,
} from "../attraction-types";
import { enrichAttraction } from "../attraction-data";

interface AttractionDetailViewProps {
  attraction: AttractionItem;
  reviews: AttractionReviewItem[];
  reviewSummary?: AttractionReviewSummary | null;
  relatedAttractions?: AttractionItem[];
}

export function AttractionDetailView({
  attraction: rawAttraction,
  reviews = [],
  reviewSummary,
  relatedAttractions = [],
}: AttractionDetailViewProps) {
  const attraction = enrichAttraction(rawAttraction);
  const [selectedPhotoIndex, setSelectedPhotoIndex] = useState(0);
  const [lightboxOpen, setLightboxOpen] = useState(false);
  const [copied, setCopied] = useState(false);
  const [coordsCopied, setCoordsCopied] = useState(false);
  const [isFavorite, setIsFavorite] = useState<boolean>(() => {
    if (typeof window !== "undefined") {
      try {
        const saved = localStorage.getItem("mangatarem_fav_attractions");
        const list = saved ? JSON.parse(saved) : [];
        return list.includes(attraction.id);
      } catch {
        return false;
      }
    }
    return false;
  });

  const gallery =
    attraction.gallery && attraction.gallery.length > 0
      ? attraction.gallery
      : [attraction.image_url || "/img/mangatarem_map_teaser.webp"];

  const activePhoto = gallery[selectedPhotoIndex] || gallery[0];

  // Toggle favorite
  const handleToggleFavorite = () => {
    setIsFavorite((prev: boolean) => {
      const next = !prev;
      if (typeof window !== "undefined") {
        try {
          const saved = localStorage.getItem("mangatarem_fav_attractions");
          let list: number[] = saved ? JSON.parse(saved) : [];
          if (next) {
            if (!list.includes(attraction.id)) list.push(attraction.id);
          } else {
            list = list.filter((id) => id !== attraction.id);
          }
          localStorage.setItem("mangatarem_fav_attractions", JSON.stringify(list));
        } catch {
          // ignore
        }
      }
      return next;
    });
  };

  // Share action
  const handleShare = async () => {
    const url = typeof window !== "undefined" ? window.location.href : "";
    if (navigator.share) {
      try {
        await navigator.share({
          title: `${attraction.name} | Mangatarem Tourism`,
          text: `Explore ${attraction.name} in Mangatarem, Pangasinan!`,
          url,
        });
        return;
      } catch {
        // Fallback to clipboard
      }
    }

    if (navigator.clipboard) {
      await navigator.clipboard.writeText(url);
      setCopied(true);
      setTimeout(() => setCopied(false), 2500);
    }
  };

  // Copy GPS Coordinates
  const handleCopyCoords = () => {
    if (attraction.latitude && attraction.longitude) {
      const text = `${attraction.latitude.toFixed(5)}, ${attraction.longitude.toFixed(5)}`;
      navigator.clipboard.writeText(text);
      setCoordsCopied(true);
      setTimeout(() => setCoordsCopied(false), 2000);
    }
  };

  // Google Maps directions URL
  const googleMapsUrl =
    attraction.latitude && attraction.longitude
      ? `https://www.google.com/maps/dir/?api=1&destination=${attraction.latitude},${attraction.longitude}`
      : `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(
          `${attraction.name}, Mangatarem, Pangasinan`
        )}`;

  // Distribution calculation for rating summary
  const summary = reviewSummary || {
    average: reviews.length > 0 ? (reviews.reduce((acc, r) => acc + r.rating, 0) / reviews.length) : (attraction.rating || 5.0),
    total: reviews.length,
    distribution: {
      "5": reviews.filter((r) => r.rating === 5).length,
      "4": reviews.filter((r) => r.rating === 4).length,
      "3": reviews.filter((r) => r.rating === 3).length,
      "2": reviews.filter((r) => r.rating === 2).length,
      "1": reviews.filter((r) => r.rating === 1).length,
    },
  };

  return (
    <div className="space-y-8">
      {/* ── Top Navigation & Breadcrumb Bar ── */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div className="flex items-center gap-2 text-xs sm:text-sm text-muted-foreground">
          <Link href="/attractions" className="hover:text-foreground transition-colors flex items-center gap-1">
            <ArrowLeft className="h-3.5 w-3.5" /> Attractions
          </Link>
          <span>/</span>
          <span className="text-primary font-medium">{attraction.category}</span>
          <span>/</span>
          <span className="text-foreground font-semibold line-clamp-1">{attraction.name}</span>
        </div>

        <div className="flex items-center gap-2">
          {attraction.latitude && attraction.longitude && (
            <Link
              href={`/map?highlight=${attraction.id}`}
              className={buttonVariants({ variant: "outline", size: "sm", className: "rounded-xl gap-1.5 text-xs font-medium" })}
            >
              <Compass className="h-3.5 w-3.5 text-primary" /> View on Map
            </Link>
          )}

          <a
            href={googleMapsUrl}
            target="_blank"
            rel="noopener noreferrer"
            className={buttonVariants({ variant: "outline", size: "sm", className: "rounded-xl gap-1.5 text-xs font-medium" })}
          >
            <Navigation className="h-3.5 w-3.5 text-primary" /> Directions
          </a>

          <Button
            variant="outline"
            size="sm"
            onClick={handleShare}
            className="rounded-xl gap-1.5 text-xs"
          >
            {copied ? (
              <>
                <Check className="h-3.5 w-3.5 text-primary" /> Copied
              </>
            ) : (
              <>
                <Share2 className="h-3.5 w-3.5 text-muted-foreground" /> Share
              </>
            )}
          </Button>

          <Button
            variant="outline"
            size="sm"
            onClick={handleToggleFavorite}
            className={`rounded-xl px-2.5 transition-colors ${
              isFavorite ? "border-rose-200 bg-rose-50 text-rose-500 dark:bg-rose-950/40" : ""
            }`}
            title={isFavorite ? "Saved to favorites" : "Save to favorites"}
          >
            <Heart className={`h-4 w-4 ${isFavorite ? "fill-current" : ""}`} />
          </Button>
        </div>
      </div>

      {/* ── Visual Media & Photo Gallery Showcase ── */}
      <section className="space-y-3">
        {/* Main Photo Banner */}
        <div className="relative aspect-[16/9] sm:aspect-[21/9] rounded-3xl overflow-hidden bg-muted border border-border/60 shadow-lg group">
          <img
            src={activePhoto}
            alt={attraction.name}
            className="w-full h-full object-cover transition-transform duration-700 group-hover:scale-102 cursor-pointer"
            onClick={() => setLightboxOpen(true)}
          />
          <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-black/20 to-transparent pointer-events-none" />

          {/* Floating Badges */}
          <div className="absolute top-4 left-4 flex flex-wrap gap-2 pointer-events-none">
            <Badge className="bg-primary text-primary-foreground font-semibold shadow-md text-xs px-3 py-1">
              {attraction.category}
            </Badge>
            {attraction.is_featured && (
              <Badge className="bg-amber-500 text-white font-bold text-xs gap-1 shadow-md">
                <Star className="h-3 w-3 fill-current" /> Featured Destination
              </Badge>
            )}
            <Badge variant="secondary" className="bg-background/90 backdrop-blur-md text-foreground font-medium text-xs">
              {attraction.physical_status || "Open Public"}
            </Badge>
          </div>

          {/* Expand Lightbox Button */}
          <button
            onClick={() => setLightboxOpen(true)}
            className="absolute top-4 right-4 p-2.5 rounded-full bg-black/50 text-white hover:bg-black/70 backdrop-blur-md transition-colors"
            title="Expand Photo"
          >
            <Maximize2 className="h-4 w-4" />
          </button>

          {/* Bottom Hero Overlay Information */}
          <div className="absolute bottom-4 sm:bottom-6 left-4 sm:left-6 right-4 sm:right-6 text-white flex flex-col sm:flex-row sm:items-end justify-between gap-3 pointer-events-none">
            <div className="space-y-1.5">
              <div className="flex items-center gap-2 text-xs font-medium text-white/90">
                <span className="flex items-center gap-1 bg-black/50 backdrop-blur-md px-2.5 py-1 rounded-full">
                  <MapPin className="h-3.5 w-3.5 text-primary" />
                  Brgy. {attraction.barangay_name}, Mangatarem
                </span>
                {attraction.elevation && (
                  <span className="bg-black/50 backdrop-blur-md px-2.5 py-1 rounded-full">
                    {attraction.elevation}
                  </span>
                )}
              </div>
              <h1 className="text-2xl sm:text-4xl font-extrabold tracking-tight text-white drop-shadow-md">
                {attraction.name}
              </h1>
            </div>

            {attraction.rating && (
              <div className="flex items-center gap-2 bg-black/60 backdrop-blur-md px-3.5 py-2 rounded-2xl border border-white/10 self-start sm:self-auto">
                <Star className="h-5 w-5 fill-amber-400 text-amber-400" />
                <div>
                  <div className="text-base font-bold text-white leading-none">
                    {attraction.rating.toFixed(1)} <span className="text-xs font-normal text-white/80">/ 5.0</span>
                  </div>
                  <div className="text-[10px] text-white/70">{attraction.review_count || 1} verified ratings</div>
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Thumbnail Selector Strip (if multiple photos) */}
        {gallery.length > 1 && (
          <div className="flex items-center gap-2 overflow-x-auto pb-2 scrollbar-none">
            {gallery.map((photo, i) => (
              <button
                key={i}
                onClick={() => setSelectedPhotoIndex(i)}
                className={`relative aspect-[16/10] w-24 sm:w-28 rounded-xl overflow-hidden border-2 transition-all shrink-0 ${
                  selectedPhotoIndex === i
                    ? "border-primary ring-2 ring-primary/20 scale-102"
                    : "border-transparent opacity-70 hover:opacity-100"
                }`}
              >
                <img src={photo} alt={`${attraction.name} ${i + 1}`} className="w-full h-full object-cover" />
              </button>
            ))}
          </div>
        )}
      </section>

      {/* ── Photo Lightbox Modal ── */}
      {lightboxOpen && (
        <div
          className="fixed inset-0 z-50 bg-black/90 backdrop-blur-md flex items-center justify-center p-4"
          onClick={() => setLightboxOpen(false)}
        >
          <button
            onClick={() => setLightboxOpen(false)}
            className="absolute top-4 right-4 p-3 rounded-full bg-white/10 text-white hover:bg-white/20 transition-colors"
          >
            <X className="h-6 w-6" />
          </button>
          <img
            src={activePhoto}
            alt={attraction.name}
            className="max-h-[85vh] max-w-[90vw] object-contain rounded-2xl shadow-2xl"
            onClick={(e) => e.stopPropagation()}
          />
        </div>
      )}

      {/* ── Two-Column Main Content & Sidebar Grid ── */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
        {/* ── Main Left Column (8 cols) ── */}
        <div className="lg:col-span-8 space-y-8">
          {/* Overview & Story */}
          <section className="bg-card border border-border/60 rounded-3xl p-6 sm:p-8 space-y-4 shadow-sm">
            <div className="flex items-center gap-2 text-primary font-semibold text-xs tracking-wider uppercase">
              <Info className="h-4 w-4" /> Overview & Heritage
            </div>
            <h2 className="text-2xl font-bold tracking-tight text-foreground">About {attraction.name}</h2>
            <p className="text-base text-foreground/80 leading-relaxed whitespace-pre-line">
              {attraction.description}
            </p>

            {/* Advisory Notice Banner (if applicable) */}
            {attraction.advisory_message && (
              <div
                className={`mt-4 p-4 rounded-2xl border flex items-start gap-3 text-xs sm:text-sm ${
                  attraction.advisory_status === "Caution"
                    ? "bg-amber-500/10 border-amber-500/30 text-amber-900 dark:text-amber-200"
                    : "bg-primary/10 border-primary/20 text-primary-900 dark:text-primary-200"
                }`}
              >
                <AlertCircle className="h-5 w-5 shrink-0 mt-0.5" />
                <div>
                  <strong className="font-semibold block mb-0.5">
                    Visitor Advisory ({attraction.advisory_status || "Notice"})
                  </strong>
                  <span>{attraction.advisory_message}</span>
                </div>
              </div>
            )}
          </section>

          {/* Key Highlights Grid */}
          {attraction.highlights && attraction.highlights.length > 0 && (
            <section className="bg-card border border-border/60 rounded-3xl p-6 sm:p-8 space-y-5 shadow-sm">
              <div className="flex items-center gap-2 text-primary font-semibold text-xs tracking-wider uppercase">
                <Sparkles className="h-4 w-4" /> Key Highlights
              </div>
              <h2 className="text-xl sm:text-2xl font-bold tracking-tight text-foreground">What Makes It Special</h2>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                {attraction.highlights.map((highlight, index) => (
                  <div
                    key={index}
                    className="p-4 rounded-2xl bg-muted/40 border border-border/50 flex items-start gap-3"
                  >
                    <div className="h-6 w-6 rounded-full bg-primary/10 text-primary flex items-center justify-center shrink-0 mt-0.5 font-bold text-xs">
                      <Check className="h-3.5 w-3.5 text-primary" />
                    </div>
                    <span className="text-sm font-medium text-foreground/90 leading-snug">{highlight}</span>
                  </div>
                ))}
              </div>
            </section>
          )}

          {/* Facilities & Visitor Amenities */}
          {Array.isArray(attraction.facilities) && attraction.facilities.length > 0 && (
            <section className="bg-card border border-border/60 rounded-3xl p-6 sm:p-8 space-y-5 shadow-sm">
              <div className="flex items-center gap-2 text-primary font-semibold text-xs tracking-wider uppercase">
                <Building className="h-4 w-4" /> Available Facilities
              </div>
              <h2 className="text-xl sm:text-2xl font-bold tracking-tight text-foreground">
                Amenities & Infrastructure
              </h2>
              <div className="grid grid-cols-2 sm:grid-cols-3 gap-3">
                {attraction.facilities.map((fac, i) => (
                  <div
                    key={i}
                    className="p-3 rounded-xl bg-muted/50 border border-border/50 flex items-center gap-2.5 text-xs sm:text-sm font-medium text-foreground"
                  >
                    <div className="h-2 w-2 rounded-full bg-primary" />
                    <span>{fac}</span>
                  </div>
                ))}
              </div>
            </section>
          )}

          {/* How to Get There & Commuter Guide */}
          <section className="bg-card border border-border/60 rounded-3xl p-6 sm:p-8 space-y-5 shadow-sm">
            <div className="flex items-center gap-2 text-primary font-semibold text-xs tracking-wider uppercase">
              <Car className="h-4 w-4" /> Travel & Access
            </div>
            <h2 className="text-xl sm:text-2xl font-bold tracking-tight text-foreground">
              How to Get There
            </h2>
            <div className="space-y-4 text-sm text-muted-foreground leading-relaxed">
              <p>{attraction.directions}</p>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 pt-2">
                <div className="p-3.5 rounded-2xl bg-muted/40 border border-border/50 space-y-1">
                  <span className="text-xs font-semibold uppercase text-foreground">Public Commute</span>
                  <p className="text-xs text-muted-foreground">
                    Tricycles available from Mangatarem Public Market Terminal in Poblacion direct to Barangay{" "}
                    {attraction.barangay_name}.
                  </p>
                </div>
                <div className="p-3.5 rounded-2xl bg-muted/40 border border-border/50 space-y-1">
                  <span className="text-xs font-semibold uppercase text-foreground">Private Vehicle / Moto</span>
                  <p className="text-xs text-muted-foreground">
                    Accessible via Romulo Highway. Follow designated directional signages toward Barangay{" "}
                    {attraction.barangay_name}.
                  </p>
                </div>
              </div>

              <div className="pt-2 flex flex-wrap items-center gap-3">
                <a
                  href={googleMapsUrl}
                  target="_blank"
                  rel="noopener noreferrer"
                  className={buttonVariants({ variant: "default", size: "default", className: "rounded-xl gap-2 shadow-sm font-semibold" })}
                >
                  <Navigation className="h-4 w-4" /> Open Turn-by-Turn GPS
                </a>
                {attraction.latitude && attraction.longitude && (
                  <Link
                    href={`/map?highlight=${attraction.id}`}
                    className={buttonVariants({ variant: "outline", size: "default", className: "rounded-xl gap-2 font-medium" })}
                  >
                    <Compass className="h-4 w-4 text-primary" /> View on Cultural Map
                  </Link>
                )}
              </div>
            </div>
          </section>

          {/* Visitor Reviews & Community Rating Form */}
          <section className="bg-card border border-border/60 rounded-3xl p-6 sm:p-8 space-y-6 shadow-sm">
            <div className="flex items-center justify-between">
              <div>
                <div className="flex items-center gap-2 text-primary font-semibold text-xs tracking-wider uppercase">
                  <Star className="h-4 w-4 fill-primary" /> Community Feedback
                </div>
                <h2 className="text-xl sm:text-2xl font-bold tracking-tight text-foreground mt-1">
                  Visitor Reviews & Ratings
                </h2>
              </div>
            </div>

            {/* Rating Summary Card */}
            {summary.total > 0 ? (
              <div className="p-5 rounded-2xl bg-muted/40 border border-border/50 grid grid-cols-1 sm:grid-cols-12 gap-6 items-center">
                <div className="sm:col-span-5 text-center sm:text-left space-y-1 sm:border-r border-border/50 sm:pr-6">
                  <div className="text-4xl font-extrabold text-foreground">
                    {summary.average.toFixed(1)}
                    <span className="text-sm font-normal text-muted-foreground"> / 5.0</span>
                  </div>
                  <div className="flex items-center justify-center sm:justify-start gap-1 text-amber-400">
                    {[1, 2, 3, 4, 5].map((star) => (
                      <Star
                        key={star}
                        className={`h-4 w-4 ${
                          star <= Math.round(summary.average)
                            ? "fill-amber-400 text-amber-400"
                            : "text-muted-foreground/30"
                        }`}
                      />
                    ))}
                  </div>
                  <p className="text-xs text-muted-foreground">
                    Based on {summary.total} verified visitor feedback
                  </p>
                </div>

                {/* Rating Bars */}
                <div className="sm:col-span-7 space-y-1.5 text-xs">
                  {[5, 4, 3, 2, 1].map((ratingNum) => {
                    const key = String(ratingNum) as keyof typeof summary.distribution;
                    const count = summary.distribution[key] || 0;
                    const percent = summary.total > 0 ? (count / summary.total) * 100 : 0;

                    return (
                      <div key={ratingNum} className="flex items-center gap-2">
                        <span className="w-6 text-right font-medium text-muted-foreground">{ratingNum}★</span>
                        <div className="flex-1 h-2 rounded-full bg-muted overflow-hidden">
                          <div
                            className="h-full rounded-full bg-amber-400"
                            style={{ width: `${percent}%` }}
                          />
                        </div>
                        <span className="w-6 text-muted-foreground text-[11px]">{count}</span>
                      </div>
                    );
                  })}
                </div>
              </div>
            ) : (
              <div className="p-5 rounded-2xl bg-muted/30 border border-border/50 text-center space-y-2">
                <Star className="h-8 w-8 text-amber-400/50 mx-auto" />
                <h4 className="font-semibold text-sm text-foreground">No Community Reviews Yet</h4>
                <p className="text-xs text-muted-foreground max-w-sm mx-auto">
                  Have you visited {attraction.name}? Be the first to share your experience, travel tips, and feedback with fellow explorers!
                </p>
              </div>
            )}

            {/* Review Form */}
            <div className="space-y-2">
              <ReviewForm attractionId={attraction.id} />
            </div>

            {/* Reviews List */}
            {reviews.length > 0 && (
              <div className="space-y-4 pt-4 border-t border-border/40">
                <h3 className="font-semibold text-sm text-foreground">Recent Visitor Comments</h3>
                <div className="space-y-3">
                  {reviews.map((r) => (
                    <div
                      key={r.id}
                      className="p-4 rounded-2xl border border-border/50 bg-background/50 space-y-2"
                    >
                      <div className="flex items-center justify-between">
                        <div className="flex items-center gap-2">
                          <div className="h-7 w-7 rounded-full bg-primary/10 text-primary flex items-center justify-center font-bold text-xs">
                            {r.username.charAt(0).toUpperCase()}
                          </div>
                          <div>
                            <span className="font-semibold text-xs text-foreground block">{r.username}</span>
                            {r.created_at && (
                              <span className="text-[10px] text-muted-foreground">
                                {new Date(r.created_at).toLocaleDateString("en-PH", {
                                  month: "short",
                                  day: "numeric",
                                  year: "numeric",
                                })}
                              </span>
                            )}
                          </div>
                        </div>

                        <div className="flex items-center text-amber-400 text-xs">
                          {"★".repeat(r.rating)}
                        </div>
                      </div>

                      <p className="text-xs sm:text-sm text-muted-foreground leading-relaxed pl-9">
                        {r.comment}
                      </p>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </section>
        </div>

        {/* ── Sidebar Right Column (4 cols) ── */}
        <aside className="lg:col-span-4 space-y-6 lg:sticky lg:top-24">
          {/* Quick Facts Card */}
          <Card className="border-border/60 rounded-3xl p-6 bg-card shadow-sm space-y-5">
            <h3 className="font-bold text-lg text-foreground flex items-center gap-2">
              <Info className="h-4 w-4 text-primary" /> At A Glance
            </h3>

            <div className="space-y-3.5 text-xs sm:text-sm">
              <div className="flex items-start justify-between pb-3 border-b border-border/40 gap-2">
                <span className="text-muted-foreground">Barangay</span>
                <span className="font-semibold text-foreground text-right">
                  Brgy. {attraction.barangay_name}
                </span>
              </div>

              <div className="flex items-start justify-between pb-3 border-b border-border/40 gap-2">
                <span className="text-muted-foreground">Category</span>
                <Badge variant="outline" className="text-primary text-xs font-semibold">
                  {attraction.category}
                </Badge>
              </div>

              <div className="flex items-start justify-between pb-3 border-b border-border/40 gap-2">
                <span className="text-muted-foreground">Entrance Fee</span>
                <span className="font-semibold text-foreground text-right">
                  {attraction.entrance_fee || "Free Entry"}
                </span>
              </div>

              <div className="flex items-start justify-between pb-3 border-b border-border/40 gap-2">
                <span className="text-muted-foreground">Visiting Hours</span>
                <span className="font-semibold text-foreground text-right">
                  {attraction.opening_hours || "Open Daily"}
                </span>
              </div>

              <div className="flex items-start justify-between pb-3 border-b border-border/40 gap-2">
                <span className="text-muted-foreground">Difficulty</span>
                <span className="font-semibold text-foreground">{attraction.difficulty || "Easy"}</span>
              </div>

              {attraction.best_time_to_visit && (
                <div className="pb-3 border-b border-border/40 space-y-1">
                  <span className="text-muted-foreground block">Best Time to Visit</span>
                  <span className="font-medium text-foreground text-xs leading-relaxed block">
                    {attraction.best_time_to_visit}
                  </span>
                </div>
              )}

              {attraction.latitude && attraction.longitude && (
                <div className="space-y-1.5 pt-1">
                  <span className="text-muted-foreground block">GPS Coordinates</span>
                  <div className="flex items-center justify-between p-2.5 rounded-xl bg-muted/60 text-xs font-mono">
                    <span>
                      {attraction.latitude.toFixed(5)}, {attraction.longitude.toFixed(5)}
                    </span>
                    <button
                      onClick={handleCopyCoords}
                      className="text-primary hover:underline font-sans font-semibold text-[11px]"
                    >
                      {coordsCopied ? "Copied!" : "Copy"}
                    </button>
                  </div>
                </div>
              )}
            </div>

            {/* Quick CTAs */}
            <div className="space-y-2 pt-2">
              <a
                href={googleMapsUrl}
                target="_blank"
                rel="noopener noreferrer"
                className={buttonVariants({ variant: "default", size: "default", className: "w-full rounded-xl shadow-sm gap-2 font-semibold" })}
              >
                <Navigation className="h-4 w-4" /> Start Navigation
              </a>
              {attraction.latitude && attraction.longitude && (
                <Link
                  href={`/map?highlight=${attraction.id}`}
                  className={buttonVariants({ variant: "outline", size: "default", className: "w-full rounded-xl gap-2 font-medium" })}
                >
                  <Compass className="h-4 w-4 text-primary" /> View on Map
                </Link>
              )}
            </div>
          </Card>

          {/* Eat & Stay Nearby Banner */}
          <Card className="border-border/60 rounded-3xl p-6 bg-gradient-to-br from-card to-primary/5 shadow-sm space-y-4">
            <div className="flex items-center gap-2 text-primary font-semibold text-xs tracking-wider uppercase">
              <Utensils className="h-4 w-4" /> Local Experience
            </div>
            <div>
              <h3 className="font-bold text-base text-foreground">Stay & Dine in {attraction.barangay_name}</h3>
              <p className="text-xs text-muted-foreground mt-1 leading-relaxed">
                Discover cozy local inns, authentic Pangasinan karinderyas, native coffee shops, and farm stays near this attraction.
              </p>
            </div>
            <Link
              href={`/business?barangay=${encodeURIComponent(attraction.barangay_name || "")}`}
              className={buttonVariants({ variant: "secondary", size: "sm", className: "w-full rounded-xl gap-1 text-xs font-semibold" })}
            >
              Explore Nearby Businesses <ChevronRight className="h-3.5 w-3.5" />
            </Link>
          </Card>

          {/* Related Attractions */}
          {relatedAttractions.length > 0 && (
            <Card className="border-border/60 rounded-3xl p-6 bg-card shadow-sm space-y-4">
              <h3 className="font-bold text-base text-foreground">Other Attractions to Visit</h3>
              <div className="space-y-3">
                {relatedAttractions.slice(0, 3).map((rel) => {
                  const enrichedRel = enrichAttraction(rel);

                  return (
                    <Link
                      key={rel.id}
                      href={`/attractions/${rel.id}`}
                      className="group flex items-center gap-3 p-2.5 rounded-2xl hover:bg-muted/60 transition-colors border border-transparent hover:border-border/50"
                    >
                      <div className="h-14 w-14 rounded-xl overflow-hidden bg-muted shrink-0">
                        <img
                          src={enrichedRel.image_url || "/img/mangatarem_map_teaser.webp"}
                          alt={rel.name}
                          className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                        />
                      </div>
                      <div className="flex-1 min-w-0">
                        <h4 className="font-semibold text-xs sm:text-sm text-foreground group-hover:text-primary transition-colors truncate">
                          {rel.name}
                        </h4>
                        <p className="text-[11px] text-muted-foreground truncate">
                          {rel.category} • Brgy. {rel.barangay_name}
                        </p>
                      </div>
                      <ChevronRight className="h-4 w-4 text-muted-foreground group-hover:text-primary transition-colors shrink-0" />
                    </Link>
                  );
                })}
              </div>
            </Card>
          )}
        </aside>
      </div>
    </div>
  );
}
