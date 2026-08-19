"use client";

import React, { useEffect, useMemo, useRef, useState, useCallback } from "react";
import {
  Map,
  MapMarker,
  MarkerContent,
  MarkerPopup,
  MapControls,
  MapRoute,
  useMap,
} from "@/components/ui/map";
import { MarkerPlace, CuratedTrail, UserLocation, MapStyleOption } from "./types";
import { MapMarkerPin, UserLocationPin } from "./map-marker-pin";
import { CATEGORY_CONFIG, DEFAULT_CATEGORY_STYLE, resolvePlaceImage } from "./data";
import { Layers, Compass, Maximize2, RotateCcw, Navigation, ExternalLink, ArrowRight } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";

// Basemap style URLs (Carto GL styles)
const BASEMAP_STYLES = {
  voyager: "https://basemaps.cartocdn.com/gl/voyager-gl-style/style.json",
  positron: "https://basemaps.cartocdn.com/gl/positron-gl-style/style.json",
  "dark-matter": "https://basemaps.cartocdn.com/gl/dark-matter-gl-style/style.json",
};

// Default center on Mangatarem, Pangasinan
const MANGATAREM_CENTER: [number, number] = [120.2928, 15.7891];
const DEFAULT_ZOOM = 12;

interface MapContainerProps {
  markers: MarkerPlace[];
  selectedPlace: MarkerPlace | null;
  hoveredPlaceId: number | null;
  activeTrail: CuratedTrail | null;
  userLocation: UserLocation | null;
  onSelectPlace: (place: MarkerPlace | null) => void;
  onLocateUser?: (coords: { longitude: number; latitude: number }) => void;
  className?: string;
}

/**
 * Controller bridge component inside MapContext to execute programmatic map operations
 */
function MapBridgeController({
  selectedPlace,
  activeTrail,
  markers,
  mapStyle,
  is3DMode,
  resetTrigger,
  fitTrigger,
}: {
  selectedPlace: MarkerPlace | null;
  activeTrail: CuratedTrail | null;
  markers: MarkerPlace[];
  mapStyle: MapStyleOption;
  is3DMode: boolean;
  resetTrigger: number;
  fitTrigger: number;
}) {
  const { map, isLoaded } = useMap();
  const lastSelectedIdRef = useRef<number | null>(null);

  // Fly to selected place
  useEffect(() => {
    if (!isLoaded || !map || !selectedPlace) return;
    if (lastSelectedIdRef.current === selectedPlace.id) return;
    lastSelectedIdRef.current = selectedPlace.id;

    map.flyTo({
      center: [selectedPlace.longitude, selectedPlace.latitude],
      zoom: 14.5,
      pitch: is3DMode ? 45 : 0,
      duration: 1200,
      essential: true,
    });
  }, [selectedPlace, isLoaded, map, is3DMode]);

  // Fit bounds when active trail changes
  useEffect(() => {
    if (!isLoaded || !map || !activeTrail || activeTrail.stops.length === 0) return;

    const lngs = activeTrail.stops.map((s) => s.coordinates[0]);
    const lats = activeTrail.stops.map((s) => s.coordinates[1]);
    const minLng = Math.min(...lngs);
    const maxLng = Math.max(...lngs);
    const minLat = Math.min(...lats);
    const maxLat = Math.max(...lats);

    map.fitBounds(
      [
        [minLng - 0.02, minLat - 0.02],
        [maxLng + 0.02, maxLat + 0.02],
      ],
      {
        padding: { top: 60, bottom: 60, left: 60, right: 60 },
        duration: 1400,
        pitch: is3DMode ? 40 : 0,
      }
    );
  }, [activeTrail, isLoaded, map, is3DMode]);

  // Handle manual Fit All Markers
  useEffect(() => {
    if (!isLoaded || !map || fitTrigger === 0 || markers.length === 0) return;

    const lngs = markers.map((m) => m.longitude);
    const lats = markers.map((m) => m.latitude);
    const minLng = Math.min(...lngs);
    const maxLng = Math.max(...lngs);
    const minLat = Math.min(...lats);
    const maxLat = Math.max(...lats);

    map.fitBounds(
      [
        [minLng - 0.015, minLat - 0.015],
        [maxLng + 0.015, maxLat + 0.015],
      ],
      {
        padding: { top: 50, bottom: 50, left: 50, right: 50 },
        duration: 1200,
      }
    );
  }, [fitTrigger, markers, isLoaded, map]);

  // Handle Reset View
  useEffect(() => {
    if (!isLoaded || !map || resetTrigger === 0) return;
    map.flyTo({
      center: MANGATAREM_CENTER,
      zoom: DEFAULT_ZOOM,
      pitch: 0,
      bearing: 0,
      duration: 1200,
    });
  }, [resetTrigger, isLoaded, map]);

  // Update pitch for 3D mode
  useEffect(() => {
    if (!isLoaded || !map) return;
    map.easeTo({
      pitch: is3DMode ? 45 : 0,
      duration: 600,
    });
  }, [is3DMode, isLoaded, map]);

  return null;
}

export function MapContainer({
  markers,
  selectedPlace,
  hoveredPlaceId,
  activeTrail,
  userLocation,
  onSelectPlace,
  onLocateUser,
  className = "",
}: MapContainerProps) {
  const [mapStyle, setMapStyle] = useState<MapStyleOption>("voyager");
  const [is3DMode, setIs3DMode] = useState(false);
  const [resetTrigger, setResetTrigger] = useState(0);
  const [fitTrigger, setFitTrigger] = useState(0);
  const [styleMenuOpen, setStyleMenuOpen] = useState(false);

  const initialCenter = useMemo<[number, number]>(() => {
    if (selectedPlace) return [selectedPlace.longitude, selectedPlace.latitude];
    if (markers.length > 0) return [markers[0].longitude, markers[0].latitude];
    return MANGATAREM_CENTER;
  }, [selectedPlace, markers]);

  const customStyles = useMemo(
    () => ({
      light: BASEMAP_STYLES[mapStyle],
      dark: mapStyle === "dark-matter" ? BASEMAP_STYLES["dark-matter"] : BASEMAP_STYLES[mapStyle],
    }),
    [mapStyle]
  );

  return (
    <div className={`relative h-full w-full overflow-hidden select-none ${className}`}>
      <Map
        center={initialCenter}
        zoom={DEFAULT_ZOOM}
        styles={customStyles}
        className="h-full w-full"
      >
        <MapControls
          position="bottom-right"
          showZoom
          showCompass
          showLocate
          showFullscreen
          onLocate={(coords) => {
            onLocateUser?.(coords);
          }}
        />

        {/* Controller Bridge */}
        <MapBridgeController
          selectedPlace={selectedPlace}
          activeTrail={activeTrail}
          markers={markers}
          mapStyle={mapStyle}
          is3DMode={is3DMode}
          resetTrigger={resetTrigger}
          fitTrigger={fitTrigger}
        />

        {/* Curated Trail Polyline */}
        {activeTrail && (
          <MapRoute
            id={activeTrail.id}
            coordinates={activeTrail.pathCoordinates}
            color={activeTrail.color || "#16a34a"}
            width={4}
            opacity={0.85}
          />
        )}

        {/* User GPS Location Marker */}
        {userLocation && (
          <MapMarker
            longitude={userLocation.longitude}
            latitude={userLocation.latitude}
          >
            <MarkerContent>
              <UserLocationPin />
            </MarkerContent>
            <MarkerPopup>
              <div className="p-1 text-xs">
                <p className="font-semibold text-foreground">Your Current Location</p>
                <p className="text-muted-foreground text-[11px]">GPS Active</p>
              </div>
            </MarkerPopup>
          </MapMarker>
        )}

        {/* Markers for Places */}
        {markers.map((place) => {
          const isSelected = selectedPlace?.id === place.id;
          const isHovered = hoveredPlaceId === place.id;
          const config = CATEGORY_CONFIG[place.category] || DEFAULT_CATEGORY_STYLE;
          const imgUrl = resolvePlaceImage(place.image_url, place.name);

          // Check if this place is a stop in active curated trail
          const trailStop = activeTrail?.stops.find(
            (s) => s.placeId === place.id || s.name.toLowerCase() === place.name.toLowerCase()
          );

          return (
            <MapMarker
              key={place.id}
              longitude={place.longitude}
              latitude={place.latitude}
              onClick={() => onSelectPlace(place)}
            >
              <MarkerContent>
                <div
                  className="cursor-pointer"
                  role="button"
                  tabIndex={0}
                  aria-label={`View ${place.name}`}
                  onKeyDown={(e) => {
                    if (e.key === "Enter" || e.key === " ") {
                      e.preventDefault();
                      onSelectPlace(place);
                    }
                  }}
                >
                  <MapMarkerPin
                    place={place}
                    isSelected={isSelected}
                    isHovered={isHovered}
                    orderNumber={trailStop?.order}
                  />
                </div>
              </MarkerContent>

              {/* Popup on Marker */}
              <MarkerPopup closeButton className="p-0 overflow-hidden max-w-[240px]">
                <div className="flex flex-col text-left">
                  {/* Photo thumbnail */}
                  <div className="relative h-24 w-full bg-muted overflow-hidden">
                    <img
                      src={imgUrl}
                      alt={place.name}
                      className="w-full h-full object-cover"
                      loading="lazy"
                    />
                    <Badge
                      className={`absolute top-2 left-2 text-[10px] px-1.5 py-0.5 border shadow-xs ${config.bgClass} ${config.textClass} ${config.borderClass}`}
                    >
                      {place.category}
                    </Badge>
                  </div>

                  {/* Body */}
                  <div className="p-3 space-y-1.5">
                    <h3 className="font-semibold text-sm leading-tight text-foreground line-clamp-1">
                      {place.name}
                    </h3>
                    <p className="text-xs text-muted-foreground flex items-center gap-1">
                      <span>{place.barangay_name ? `Brgy. ${place.barangay_name}` : "Mangatarem"}</span>
                      {place.physical_status && (
                        <>
                          <span>·</span>
                          <span className="text-primary font-medium">{place.physical_status}</span>
                        </>
                      )}
                    </p>

                    {/* Actions */}
                    <div className="pt-2 flex items-center justify-between gap-2 border-t border-border/40">
                      <Button
                        size="xs"
                        variant="default"
                        className="w-full text-xs font-medium"
                        onClick={() => onSelectPlace(place)}
                      >
                        View Details
                        <ArrowRight className="w-3 h-3 ml-1" />
                      </Button>
                    </div>
                  </div>
                </div>
              </MarkerPopup>
            </MapMarker>
          );
        })}
      </Map>

      {/* Floating On-Map Toolbar */}
      <div className="absolute top-3 left-3 z-30 flex items-center gap-1.5 bg-background/95 backdrop-blur-md p-1 rounded-lg border border-border/60 shadow-md">
        {/* Style Selector */}
        <div className="relative">
          <Button
            size="sm"
            variant="ghost"
            className="h-8 px-2.5 text-xs font-medium gap-1.5"
            onClick={() => setStyleMenuOpen(!styleMenuOpen)}
            title="Change Map Style"
            aria-expanded={styleMenuOpen}
          >
            <Layers className="w-3.5 h-3.5 text-muted-foreground" />
            <span className="capitalize">{mapStyle}</span>
          </Button>

          {styleMenuOpen && (
            <div className="absolute top-full left-0 mt-1.5 w-36 bg-popover/95 backdrop-blur-md rounded-lg border border-border shadow-lg p-1 space-y-0.5 z-50">
              <button
                type="button"
                className={`w-full text-left px-2.5 py-1.5 text-xs rounded-md transition-colors ${
                  mapStyle === "voyager" ? "bg-accent font-semibold text-accent-foreground" : "hover:bg-muted"
                }`}
                onClick={() => {
                  setMapStyle("voyager");
                  setStyleMenuOpen(false);
                }}
              >
                Voyager (Detailed)
              </button>
              <button
                type="button"
                className={`w-full text-left px-2.5 py-1.5 text-xs rounded-md transition-colors ${
                  mapStyle === "positron" ? "bg-accent font-semibold text-accent-foreground" : "hover:bg-muted"
                }`}
                onClick={() => {
                  setMapStyle("positron");
                  setStyleMenuOpen(false);
                }}
              >
                Positron (Light)
              </button>
              <button
                type="button"
                className={`w-full text-left px-2.5 py-1.5 text-xs rounded-md transition-colors ${
                  mapStyle === "dark-matter" ? "bg-accent font-semibold text-accent-foreground" : "hover:bg-muted"
                }`}
                onClick={() => {
                  setMapStyle("dark-matter");
                  setStyleMenuOpen(false);
                }}
              >
                Dark Matter (Dark)
              </button>
            </div>
          )}
        </div>

        <div className="h-4 w-px bg-border" />

        {/* 3D Tilt Mode Toggle */}
        <Button
          size="sm"
          variant={is3DMode ? "default" : "ghost"}
          className="h-8 px-2 text-xs gap-1"
          onClick={() => setIs3DMode(!is3DMode)}
          title="Toggle 3D Perspective Tilt"
        >
          <Compass className="w-3.5 h-3.5" />
          <span className="text-[11px] font-medium">{is3DMode ? "3D Active" : "3D"}</span>
        </Button>

        {/* Fit Bounds */}
        <Button
          size="sm"
          variant="ghost"
          className="h-8 px-2 text-xs"
          onClick={() => setFitTrigger((t) => t + 1)}
          title="Fit all markers in view"
        >
          <Maximize2 className="w-3.5 h-3.5" />
        </Button>

        {/* Reset View to Mangatarem */}
        <Button
          size="sm"
          variant="ghost"
          className="h-8 px-2 text-xs"
          onClick={() => setResetTrigger((t) => t + 1)}
          title="Reset camera to Mangatarem center"
        >
          <RotateCcw className="w-3.5 h-3.5" />
        </Button>
      </div>

      {/* Active Trail Banner Indicator */}
      {activeTrail && (
        <div className="absolute top-3 right-14 z-30 hidden sm:flex items-center gap-2 bg-background/95 backdrop-blur-md px-3 py-1.5 rounded-lg border border-primary/40 shadow-md">
          <span className="size-2 rounded-full bg-primary animate-pulse" />
          <p className="text-xs font-medium text-foreground">
            Active Tour: <span className="font-semibold text-primary">{activeTrail.title}</span>
          </p>
        </div>
      )}
    </div>
  );
}
