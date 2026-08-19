"use client";

import React, { useState } from "react";
import { MarkerPlace } from "./types";
import { CATEGORY_CONFIG, DEFAULT_CATEGORY_STYLE, resolvePlaceImage, formatCoordinates } from "./data";
import {
  X,
  MapPin,
  Navigation,
  ExternalLink,
  Star,
  Clock,
  DollarSign,
  Phone,
  Layers,
  Copy,
  Check,
  Plus,
  Trash2,
  ShieldCheck,
  Info,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import Link from "next/link";

interface MapDetailSheetProps {
  place: MarkerPlace | null;
  onClose: () => void;
  isInTour?: boolean;
  onToggleTour?: (place: MarkerPlace) => void;
}

export function MapDetailSheet({
  place,
  onClose,
  isInTour = false,
  onToggleTour,
}: MapDetailSheetProps) {
  const [copiedCoords, setCopiedCoords] = useState(false);

  if (!place) return null;

  const config = CATEGORY_CONFIG[place.category] || DEFAULT_CATEGORY_STYLE;
  const imageUrl = resolvePlaceImage(place.image_url, place.name);
  const formattedCoords = formatCoordinates(place.latitude, place.longitude);
  const googleMapsUrl = `https://www.google.com/maps/dir/?api=1&destination=${place.latitude},${place.longitude}`;

  const handleCopyCoordinates = () => {
    navigator.clipboard.writeText(`${place.latitude}, ${place.longitude}`);
    setCopiedCoords(true);
    setTimeout(() => setCopiedCoords(false), 2000);
  };

  return (
    <div className="absolute bottom-4 left-4 right-4 sm:left-auto sm:right-4 sm:bottom-4 z-40 sm:w-96 max-h-[85vh] flex flex-col bg-background/95 backdrop-blur-md rounded-2xl border border-border/80 shadow-2xl overflow-hidden animate-in fade-in slide-in-from-bottom-4 duration-300">
      {/* Header Image */}
      <div className="relative h-44 w-full bg-muted shrink-0 overflow-hidden">
        <img
          src={imageUrl}
          alt={place.name}
          className="w-full h-full object-cover"
        />
        {/* Gradient Overlay */}
        <div className="absolute inset-0 bg-gradient-to-t from-background via-transparent to-black/30" />

        {/* Top Badges */}
        <div className="absolute top-3 left-3 flex items-center gap-1.5">
          <Badge
            className={`text-xs px-2 py-0.5 border shadow-sm ${config.bgClass} ${config.textClass} ${config.borderClass} bg-background/90 backdrop-blur-sm`}
          >
            {place.category}
          </Badge>
          {place.is_featured && (
            <Badge className="bg-amber-400/90 text-slate-900 text-[10px] px-1.5 py-0.5 font-semibold gap-1 shadow-sm">
              <Star className="w-2.5 h-2.5 fill-current" />
              Featured
            </Badge>
          )}
        </div>

        {/* Close Button */}
        <Button
          size="icon-xs"
          variant="secondary"
          className="absolute top-3 right-3 rounded-full size-7 bg-background/80 hover:bg-background shadow-sm"
          onClick={onClose}
          aria-label="Close details panel"
        >
          <X className="w-3.5 h-3.5" />
        </Button>

        {/* Bottom Title on Image */}
        <div className="absolute bottom-2.5 left-3 right-3">
          <h2 className="font-bold text-lg text-foreground leading-tight line-clamp-1 drop-shadow-xs">
            {place.name}
          </h2>
          <p className="text-xs text-muted-foreground flex items-center gap-1 mt-0.5">
            <MapPin className="w-3 h-3 text-primary shrink-0" />
            <span>{place.barangay_name ? `Brgy. ${place.barangay_name}, Mangatarem` : "Mangatarem, Pangasinan"}</span>
            {place.distanceKm !== undefined && (
              <>
                <span>·</span>
                <span className="font-medium text-primary">{place.distanceKm} km away</span>
              </>
            )}
          </p>
        </div>
      </div>

      {/* Body Content */}
      <div className="p-4 overflow-y-auto space-y-3.5 text-xs">
        {/* Status Chips */}
        <div className="flex items-center flex-wrap gap-1.5">
          {place.physical_status && (
            <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-md bg-emerald-500/10 text-emerald-700 dark:text-emerald-300 font-medium border border-emerald-500/20">
              <ShieldCheck className="w-3 h-3" />
              {place.physical_status}
            </span>
          )}

          {place.advisory_status && (
            <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-md bg-muted text-muted-foreground font-medium border border-border">
              <Info className="w-3 h-3" />
              Advisory: {place.advisory_status}
            </span>
          )}
        </div>

        {/* Description */}
        {place.description && (
          <p className="text-muted-foreground text-xs leading-relaxed">
            {place.description}
          </p>
        )}

        {/* Coordinates */}
        <div className="flex items-center justify-between p-2 rounded-lg bg-muted/50 border border-border/50 text-[11px]">
          <div className="flex items-center gap-1.5 text-muted-foreground">
            <Navigation className="w-3 h-3 text-primary" />
            <span className="font-mono">{formattedCoords}</span>
          </div>
          <button
            type="button"
            className="flex items-center gap-1 text-primary hover:underline font-medium ml-2"
            onClick={handleCopyCoordinates}
          >
            {copiedCoords ? (
              <>
                <Check className="w-3 h-3 text-emerald-600" />
                <span>Copied!</span>
              </>
            ) : (
              <>
                <Copy className="w-3 h-3" />
                <span>Copy</span>
              </>
            )}
          </button>
        </div>

        {/* Practical info if present */}
        {(place.opening_hours || place.entrance_fee || place.contact_info) && (
          <div className="space-y-1.5 pt-1 border-t border-border/50">
            {place.opening_hours && (
              <div className="flex items-center gap-2 text-muted-foreground">
                <Clock className="w-3.5 h-3.5 text-primary shrink-0" />
                <span>{place.opening_hours}</span>
              </div>
            )}
            {place.entrance_fee && (
              <div className="flex items-center gap-2 text-muted-foreground">
                <DollarSign className="w-3.5 h-3.5 text-primary shrink-0" />
                <span>{place.entrance_fee}</span>
              </div>
            )}
            {place.contact_info && (
              <div className="flex items-center gap-2 text-muted-foreground">
                <Phone className="w-3.5 h-3.5 text-primary shrink-0" />
                <span>{place.contact_info}</span>
              </div>
            )}
          </div>
        )}

        {/* Actions Footer */}
        <div className="pt-2 border-t border-border/60 flex flex-col gap-2">
          <div className="grid grid-cols-2 gap-2">
            {/* Directions button */}
            <a
              href={googleMapsUrl}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center justify-center gap-1.5 h-8 rounded-lg bg-secondary text-secondary-foreground hover:bg-secondary/80 font-medium text-xs border border-border transition-colors"
            >
              <Navigation className="w-3.5 h-3.5" />
              Directions
            </a>

            {/* Tour Waypoint Button */}
            {onToggleTour && (
              <Button
                size="sm"
                variant={isInTour ? "outline" : "outline"}
                className={`h-8 text-xs font-medium gap-1.5 ${
                  isInTour ? "border-destructive text-destructive hover:bg-destructive/10" : ""
                }`}
                onClick={() => onToggleTour(place)}
              >
                {isInTour ? (
                  <>
                    <Trash2 className="w-3 h-3" />
                    Remove Stop
                  </>
                ) : (
                  <>
                    <Plus className="w-3 h-3" />
                    Add to Tour
                  </>
                )}
              </Button>
            )}
          </div>

          {/* Full Attraction Page Link */}
          <Link
            href={`/attractions/${place.id}`}
            className="inline-flex items-center justify-center gap-1.5 h-8.5 rounded-lg bg-primary text-primary-foreground hover:bg-primary/90 font-medium text-xs shadow-xs transition-colors"
          >
            View Full Attraction Page
            <ExternalLink className="w-3.5 h-3.5 ml-0.5" />
          </Link>
        </div>
      </div>
    </div>
  );
}
