"use client";

import React from "react";
import { MarkerPlace } from "./types";
import { CATEGORY_CONFIG, DEFAULT_CATEGORY_STYLE, resolvePlaceImage } from "./data";
import { MapPin, Navigation, ExternalLink, Star, ArrowUpRight, Plus, Check } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import Link from "next/link";

interface MapPlaceCardProps {
  place: MarkerPlace;
  isSelected?: boolean;
  onSelect: (place: MarkerPlace) => void;
  onHover?: (id: number | null) => void;
  isInTour?: boolean;
  onToggleTour?: (place: MarkerPlace) => void;
}

export function MapPlaceCard({
  place,
  isSelected = false,
  onSelect,
  onHover,
  isInTour = false,
  onToggleTour,
}: MapPlaceCardProps) {
  const config = CATEGORY_CONFIG[place.category] || DEFAULT_CATEGORY_STYLE;
  const imageUrl = resolvePlaceImage(place.image_url, place.name);

  const googleMapsUrl = `https://www.google.com/maps/dir/?api=1&destination=${place.latitude},${place.longitude}`;

  return (
    <div
      className={`group relative flex flex-col sm:flex-row gap-3 p-3 rounded-xl border transition-all duration-200 cursor-pointer ${
        isSelected
          ? "bg-accent/40 border-primary shadow-sm ring-1 ring-primary/40"
          : "bg-card hover:bg-muted/40 border-border/70 hover:border-border hover:shadow-xs"
      }`}
      onClick={() => onSelect(place)}
      onMouseEnter={() => onHover?.(place.id)}
      onMouseLeave={() => onHover?.(null)}
      role="button"
      tabIndex={0}
      aria-label={`Select ${place.name}`}
      onKeyDown={(e) => {
        if (e.key === "Enter" || e.key === " ") {
          e.preventDefault();
          onSelect(place);
        }
      }}
    >
      {/* Thumbnail */}
      <div className="relative w-full sm:w-28 sm:h-28 aspect-video sm:aspect-square shrink-0 rounded-lg overflow-hidden bg-muted">
        <img
          src={imageUrl}
          alt={place.name}
          className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
          loading="lazy"
        />
        {/* Category Badge */}
        <Badge
          className={`absolute top-2 left-2 text-[10px] px-1.5 py-0.5 border shadow-xs ${config.bgClass} ${config.textClass} ${config.borderClass}`}
        >
          {place.category}
        </Badge>

        {/* Featured Tag */}
        {place.is_featured && (
          <div className="absolute top-2 right-2 size-5 rounded-full bg-amber-400 text-slate-900 flex items-center justify-center shadow-xs">
            <Star className="w-3 h-3 fill-current" />
          </div>
        )}
      </div>

      {/* Details */}
      <div className="flex-1 flex flex-col justify-between min-w-0">
        <div>
          <div className="flex items-start justify-between gap-1.5">
            <h3 className="font-semibold text-sm leading-snug text-foreground group-hover:text-primary transition-colors line-clamp-1">
              {place.name}
            </h3>
          </div>

          {/* Location & Distance */}
          <div className="flex items-center flex-wrap gap-x-2 gap-y-1 mt-1 text-xs text-muted-foreground">
            <span className="flex items-center gap-1">
              <MapPin className="w-3 h-3 text-muted-foreground shrink-0" />
              <span className="truncate">
                {place.barangay_name ? `Brgy. ${place.barangay_name}` : "Mangatarem"}
              </span>
            </span>

            {place.distanceKm !== undefined && (
              <span className="font-medium text-primary bg-primary/10 px-1.5 py-0.2 rounded text-[11px]">
                {place.distanceKm} km away
              </span>
            )}
          </div>

          {/* Short Description */}
          {place.description && (
            <p className="text-xs text-muted-foreground line-clamp-2 mt-1.5 leading-relaxed">
              {place.description}
            </p>
          )}
        </div>

        {/* Action Toolbar */}
        <div className="flex items-center justify-between gap-2 mt-2 pt-2 border-t border-border/40">
          <div className="flex items-center gap-1.5">
            {place.physical_status && (
              <span className="text-[10px] font-medium px-1.5 py-0.5 rounded bg-muted text-muted-foreground">
                {place.physical_status}
              </span>
            )}
          </div>

          <div className="flex items-center gap-1" onClick={(e) => e.stopPropagation()}>
            {/* Add to Tour Planner */}
            {onToggleTour && (
              <Button
                size="icon-xs"
                variant={isInTour ? "default" : "outline"}
                className="h-6 w-6 text-[10px]"
                onClick={() => onToggleTour(place)}
                title={isInTour ? "Remove from Itinerary" : "Add to Itinerary"}
              >
                {isInTour ? <Check className="w-3 h-3" /> : <Plus className="w-3 h-3" />}
              </Button>
            )}

            {/* Directions Link */}
            <a
              href={googleMapsUrl}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center justify-center size-6 rounded-md border border-border hover:bg-muted text-muted-foreground hover:text-foreground transition-colors"
              title="Get Directions on Google Maps"
            >
              <Navigation className="w-3 h-3" />
            </a>

            {/* Full Details Page */}
            <Link
              href={`/attractions/${place.id}`}
              className="inline-flex items-center justify-center size-6 rounded-md border border-border hover:bg-muted text-muted-foreground hover:text-foreground transition-colors"
              title="View Full Details Page"
            >
              <ArrowUpRight className="w-3 h-3" />
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}
