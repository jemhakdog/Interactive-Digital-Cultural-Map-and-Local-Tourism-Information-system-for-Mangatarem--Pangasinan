"use client";

import {
  Map,
  MapMarker,
  MarkerContent,
  MarkerPopup,
  MapControls,
} from "@/components/ui/map";
import { MarkerPlace } from "./map/types";
import { MapMarkerPin } from "./map/map-marker-pin";
import { resolvePlaceImage, CATEGORY_CONFIG, DEFAULT_CATEGORY_STYLE } from "./map/data";
import { Badge } from "@/components/ui/badge";
import Link from "next/link";
import { ArrowRight } from "lucide-react";

export function MapView({
  markers,
  center,
  zoom = 12,
  className = "h-full w-full",
}: {
  markers: MarkerPlace[] | { id: number; name: string; category: string; latitude: number; longitude: number; barangay_name?: string | null; image_url?: string | null }[];
  center?: [number, number];
  zoom?: number;
  className?: string;
}) {
  const mapCenter: [number, number] = center
    ? center
    : markers.length > 0
    ? [markers[0].longitude, markers[0].latitude]
    : [120.2928, 15.7891];

  return (
    <Map center={mapCenter} zoom={zoom} className={className}>
      <MapControls showZoom showLocate showFullscreen />
      {markers.map((m) => {
        const place: MarkerPlace = {
          id: m.id,
          name: m.name,
          category: m.category,
          latitude: m.latitude,
          longitude: m.longitude,
          barangay_name: m.barangay_name ?? null,
          image_url: m.image_url ?? null,
          description: "description" in m ? (m.description as string | null) : null,
          is_featured: "is_featured" in m ? Boolean(m.is_featured) : false,
          physical_status: "physical_status" in m ? (m.physical_status as string | null) : "Open Public",
          advisory_status: "advisory_status" in m ? (m.advisory_status as string | null) : "Normal",
          advisory_message: null,
          opening_hours: null,
          entrance_fee: null,
          contact_info: null,
          facilities: null,
          directions: null,
        };

        const config = CATEGORY_CONFIG[m.category] || DEFAULT_CATEGORY_STYLE;
        const imgUrl = resolvePlaceImage(m.image_url, m.name);

        return (
          <MapMarker key={m.id} longitude={m.longitude} latitude={m.latitude}>
            <MarkerContent>
              <MapMarkerPin place={place} />
            </MarkerContent>
            <MarkerPopup closeButton className="p-0 overflow-hidden max-w-[220px]">
              <div className="flex flex-col text-left">
                <div className="relative h-20 w-full bg-muted overflow-hidden">
                  <img
                    src={imgUrl}
                    alt={m.name}
                    className="w-full h-full object-cover"
                    loading="lazy"
                  />
                  <Badge
                    className={`absolute top-1.5 left-1.5 text-[9px] px-1 py-0 border shadow-xs ${config.bgClass} ${config.textClass} ${config.borderClass}`}
                  >
                    {m.category}
                  </Badge>
                </div>
                <div className="p-2.5 space-y-1">
                  <p className="font-semibold text-xs leading-tight text-foreground line-clamp-1">{m.name}</p>
                  <p className="text-[10px] text-muted-foreground">
                    {m.barangay_name ? `Brgy. ${m.barangay_name}` : "Mangatarem"}
                  </p>
                  <div className="pt-1.5 border-t border-border/40">
                    <Link
                      href={`/attractions/${m.id}`}
                      className="inline-flex items-center gap-1 text-[11px] font-medium text-primary hover:underline"
                    >
                      View Details <ArrowRight className="w-2.5 h-2.5" />
                    </Link>
                  </div>
                </div>
              </div>
            </MarkerPopup>
          </MapMarker>
        );
      })}
    </Map>
  );
}
