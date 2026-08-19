"use client";

import React from "react";
import { MarkerPlace } from "./types";
import { CATEGORY_CONFIG, DEFAULT_CATEGORY_STYLE, resolvePlaceImage } from "./data";
import { MapPin, Star, Navigation, ArrowRight, ShieldCheck } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import Link from "next/link";

interface MapGridViewProps {
  markers: MarkerPlace[];
  onSelectOnMap: (place: MarkerPlace) => void;
}

export function MapGridView({ markers, onSelectOnMap }: MapGridViewProps) {
  if (markers.length === 0) {
    return (
      <div className="text-center py-20 text-muted-foreground">
        <MapPin className="h-12 w-12 mx-auto mb-3 opacity-30" />
        <p className="font-semibold text-base text-foreground">No places found</p>
        <p className="text-sm text-muted-foreground mt-1">Try adjusting your filters or search terms.</p>
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4 p-4">
      {markers.map((place) => {
        const config = CATEGORY_CONFIG[place.category] || DEFAULT_CATEGORY_STYLE;
        const imageUrl = resolvePlaceImage(place.image_url, place.name);

        return (
          <div
            key={place.id}
            className="group flex flex-col justify-between rounded-xl border border-border/80 bg-card overflow-hidden hover:shadow-md transition-all duration-300 hover:-translate-y-0.5"
          >
            {/* Image Header */}
            <div className="relative aspect-video w-full bg-muted overflow-hidden">
              <img
                src={imageUrl}
                alt={place.name}
                className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
                loading="lazy"
              />
              <div className="absolute inset-0 bg-gradient-to-t from-black/40 via-transparent to-transparent" />

              {/* Category Badge */}
              <Badge
                className={`absolute top-3 left-3 text-xs px-2 py-0.5 border shadow-xs ${config.bgClass} ${config.textClass} ${config.borderClass} bg-background/90 backdrop-blur-sm`}
              >
                {place.category}
              </Badge>

              {/* Featured Star */}
              {place.is_featured && (
                <div className="absolute top-3 right-3 size-6 rounded-full bg-amber-400 text-slate-900 flex items-center justify-center shadow-xs">
                  <Star className="w-3.5 h-3.5 fill-current" />
                </div>
              )}
            </div>

            {/* Content */}
            <div className="p-4 flex-1 flex flex-col justify-between space-y-3">
              <div className="space-y-1.5">
                <h3 className="font-bold text-base text-foreground leading-snug line-clamp-1 group-hover:text-primary transition-colors">
                  {place.name}
                </h3>
                <p className="text-xs text-muted-foreground flex items-center gap-1">
                  <MapPin className="w-3.5 h-3.5 text-primary shrink-0" />
                  <span>{place.barangay_name ? `Brgy. ${place.barangay_name}` : "Mangatarem"}</span>
                  {place.distanceKm !== undefined && (
                    <>
                      <span>·</span>
                      <span className="font-medium text-primary">{place.distanceKm} km away</span>
                    </>
                  )}
                </p>

                {place.description && (
                  <p className="text-xs text-muted-foreground line-clamp-2 leading-relaxed pt-1">
                    {place.description}
                  </p>
                )}
              </div>

              {/* Card Footer Actions */}
              <div className="pt-3 border-t border-border/50 flex items-center justify-between gap-2">
                <Button
                  size="sm"
                  variant="default"
                  className="flex-1 text-xs font-medium h-8"
                  onClick={() => onSelectOnMap(place)}
                >
                  <MapPin className="w-3.5 h-3.5 mr-1" />
                  Show on Map
                </Button>

                <Link
                  href={`/attractions/${place.id}`}
                  className="inline-flex items-center justify-center size-8 rounded-lg border border-border hover:bg-muted text-muted-foreground hover:text-foreground transition-colors"
                  title="View full attraction page"
                >
                  <ArrowRight className="w-3.5 h-3.5" />
                </Link>
              </div>
            </div>
          </div>
        );
      })}
    </div>
  );
}
