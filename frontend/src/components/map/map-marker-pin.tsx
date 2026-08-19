"use client";

import React from "react";
import { TreePine, Landmark, Church, Users, Utensils, MapPin, Star } from "lucide-react";
import { CATEGORY_CONFIG, DEFAULT_CATEGORY_STYLE } from "./data";
import { MarkerPlace } from "./types";

interface MapMarkerPinProps {
  place: MarkerPlace;
  isSelected?: boolean;
  isHovered?: boolean;
  orderNumber?: number;
}

export function MapMarkerPin({
  place,
  isSelected = false,
  isHovered = false,
  orderNumber,
}: MapMarkerPinProps) {
  const config = CATEGORY_CONFIG[place.category] || DEFAULT_CATEGORY_STYLE;

  const renderIcon = () => {
    if (orderNumber !== undefined) {
      return (
        <span className="text-xs font-bold text-white leading-none">
          {orderNumber}
        </span>
      );
    }

    const iconProps = { className: "w-3.5 h-3.5 text-white" };

    switch (config.icon) {
      case "TreePine":
        return <TreePine {...iconProps} />;
      case "Landmark":
        return <Landmark {...iconProps} />;
      case "Church":
        return <Church {...iconProps} />;
      case "Users":
        return <Users {...iconProps} />;
      case "Utensils":
        return <Utensils {...iconProps} />;
      default:
        return <MapPin {...iconProps} />;
    }
  };

  return (
    <div
      className={`group relative flex items-center justify-center transition-all duration-300 ${
        isSelected ? "scale-125 z-50" : isHovered ? "scale-115 z-40" : "scale-100 z-10"
      }`}
    >
      {/* Pulse ring for selected marker */}
      {isSelected && (
        <span
          className="absolute -inset-2 rounded-full animate-ping opacity-75 pointer-events-none"
          style={{ backgroundColor: config.pinColor }}
        />
      )}

      {/* Featured Star Badge */}
      {place.is_featured && !orderNumber && (
        <div className="absolute -top-1.5 -right-1.5 z-20 size-4 bg-amber-400 text-slate-900 rounded-full flex items-center justify-center shadow-xs border border-white dark:border-slate-900">
          <Star className="w-2.5 h-2.5 fill-current" />
        </div>
      )}

      {/* Custom Pin Shape */}
      <div
        className={`relative flex items-center justify-center size-8 rounded-full shadow-md border-2 border-white dark:border-slate-900 transition-transform ${
          isSelected
            ? "ring-4 ring-primary/40 ring-offset-1"
            : isHovered
            ? "ring-2 ring-primary/30"
            : ""
        }`}
        style={{
          backgroundColor: config.pinColor,
          boxShadow: isSelected
            ? `0 4px 14px ${config.pinColor}66`
            : "0 2px 8px rgba(0,0,0,0.18)",
        }}
      >
        {renderIcon()}
      </div>

      {/* Subtle pointer anchor */}
      <div
        className="absolute -bottom-1 w-2 h-2 rotate-45 border-r border-b border-white/60 dark:border-slate-900/60 pointer-events-none"
        style={{ backgroundColor: config.pinColor }}
      />
    </div>
  );
}

export function UserLocationPin() {
  return (
    <div className="relative flex items-center justify-center z-50">
      <span className="absolute size-8 rounded-full bg-blue-500/30 animate-ping pointer-events-none" />
      <span className="absolute size-5 rounded-full bg-blue-500/50 pointer-events-none" />
      <div className="size-3.5 bg-blue-600 border-2 border-white rounded-full shadow-md" />
    </div>
  );
}
