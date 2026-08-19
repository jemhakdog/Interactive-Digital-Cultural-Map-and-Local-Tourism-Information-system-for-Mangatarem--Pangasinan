"use client";

import React, { useState } from "react";
import { CuratedTrail } from "./types";
import { CATEGORY_CONFIG, DEFAULT_CATEGORY_STYLE } from "./data";
import { Route, Clock, Compass, ChevronDown, ChevronUp, Navigation, CheckCircle2, Sparkles } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";

interface MapTrailCardProps {
  trail: CuratedTrail;
  isActive: boolean;
  onActivate: (trail: CuratedTrail) => void;
  onDeactivate: () => void;
}

export function MapTrailCard({
  trail,
  isActive,
  onActivate,
  onDeactivate,
}: MapTrailCardProps) {
  const [expanded, setExpanded] = useState(false);
  const config = CATEGORY_CONFIG[trail.category] || DEFAULT_CATEGORY_STYLE;

  // Build Google Maps Multi-Stop directions URL
  const origin = `${trail.stops[0].coordinates[1]},${trail.stops[0].coordinates[0]}`;
  const destination = `${trail.stops[trail.stops.length - 1].coordinates[1]},${trail.stops[trail.stops.length - 1].coordinates[0]}`;
  const waypoints = trail.stops
    .slice(1, -1)
    .map((s) => `${s.coordinates[1]},${s.coordinates[0]}`)
    .join("|");

  const multiStopGoogleMapsUrl = `https://www.google.com/maps/dir/?api=1&origin=${origin}&destination=${destination}${
    waypoints ? `&waypoints=${waypoints}` : ""
  }`;

  return (
    <div
      className={`rounded-xl border transition-all duration-200 overflow-hidden ${
        isActive
          ? "bg-accent/30 border-primary shadow-sm ring-1 ring-primary/40"
          : "bg-card hover:bg-muted/30 border-border/70"
      }`}
    >
      {/* Main Header Card */}
      <div className="p-4 space-y-3">
        <div className="flex items-start justify-between gap-2">
          <div>
            <div className="flex items-center gap-1.5 mb-1">
              <Badge
                variant="secondary"
                className="text-[10px] px-1.5 py-0 font-medium"
                style={{ backgroundColor: `${trail.color}15`, color: trail.color }}
              >
                <Sparkles className="w-2.5 h-2.5 mr-1" />
                {trail.difficulty}
              </Badge>
              <span className="text-xs text-muted-foreground">·</span>
              <span className="text-xs text-muted-foreground font-medium">
                {trail.stops.length} Stops
              </span>
            </div>
            <h3 className="font-semibold text-base text-foreground leading-snug">
              {trail.title}
            </h3>
            <p className="text-xs text-muted-foreground mt-0.5">{trail.subtitle}</p>
          </div>
        </div>

        {/* Trail Metrics */}
        <div className="grid grid-cols-2 gap-2 py-2 px-3 rounded-lg bg-muted/50 text-xs">
          <div className="flex items-center gap-1.5">
            <Route className="w-3.5 h-3.5 text-primary" />
            <span className="text-muted-foreground">Distance:</span>
            <span className="font-medium text-foreground">{trail.distanceKm} km</span>
          </div>
          <div className="flex items-center gap-1.5">
            <Clock className="w-3.5 h-3.5 text-primary" />
            <span className="text-muted-foreground">Duration:</span>
            <span className="font-medium text-foreground">{trail.durationEst}</span>
          </div>
        </div>

        {/* Description */}
        <p className="text-xs text-muted-foreground leading-relaxed line-clamp-2">
          {trail.description}
        </p>

        {/* Action Buttons */}
        <div className="flex items-center justify-between gap-2 pt-1">
          <Button
            size="sm"
            variant={isActive ? "default" : "outline"}
            className="flex-1 text-xs font-medium h-8"
            onClick={() => (isActive ? onDeactivate() : onActivate(trail))}
          >
            {isActive ? (
              <>
                <CheckCircle2 className="w-3.5 h-3.5 mr-1.5" />
                Active on Map
              </>
            ) : (
              <>
                <Compass className="w-3.5 h-3.5 mr-1.5" />
                Preview Trail on Map
              </>
            )}
          </Button>

          <Button
            size="sm"
            variant="ghost"
            className="h-8 px-2.5 text-xs text-muted-foreground hover:text-foreground"
            onClick={() => setExpanded(!expanded)}
          >
            {expanded ? (
              <>
                Less <ChevronUp className="w-3.5 h-3.5 ml-1" />
              </>
            ) : (
              <>
                Stops <ChevronDown className="w-3.5 h-3.5 ml-1" />
              </>
            )}
          </Button>
        </div>
      </div>

      {/* Expandable Stops List */}
      {expanded && (
        <div className="px-4 pb-4 pt-1 border-t border-border/50 bg-muted/20 space-y-3">
          <div className="space-y-2.5">
            {trail.stops.map((stop, idx) => (
              <div key={idx} className="flex items-start gap-2.5 text-xs">
                <span
                  className="flex items-center justify-center size-5 rounded-full text-white font-bold text-[10px] shrink-0 mt-0.5"
                  style={{ backgroundColor: trail.color }}
                >
                  {stop.order}
                </span>
                <div className="flex-1 min-w-0">
                  <div className="flex items-center justify-between gap-1">
                    <p className="font-semibold text-foreground truncate">{stop.name}</p>
                    <span className="text-[10px] text-muted-foreground shrink-0">
                      Brgy. {stop.barangay}
                    </span>
                  </div>
                  <p className="text-[11px] text-muted-foreground mt-0.5 leading-normal">
                    {stop.tip}
                  </p>
                </div>
              </div>
            ))}
          </div>

          <div className="pt-2 flex justify-end">
            <a
              href={multiStopGoogleMapsUrl}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-1.5 text-xs font-medium text-primary hover:underline"
            >
              <Navigation className="w-3 h-3" />
              Open Multi-Stop in Google Maps
            </a>
          </div>
        </div>
      )}
    </div>
  );
}
