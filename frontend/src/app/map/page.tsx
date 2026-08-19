"use client";

import { useState, useEffect, type ComponentType } from "react";
import { fetchAPI } from "@/lib/api";
import { MapPin, Loader2 } from "lucide-react";
import Link from "next/link";

interface Marker {
  id: number;
  name: string;
  category: string;
  latitude: number;
  longitude: number;
  image_url: string | null;
  barangay_name: string | null;
}

interface MapViewProps {
  markers: Marker[];
}

export default function MapPage() {
  const [markers, setMarkers] = useState<Marker[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedCategory, setSelectedCategory] = useState("all");
  const [MapComponent, setMapComponent] = useState<ComponentType<MapViewProps> | null>(null);

  useEffect(() => {
    setLoading(true);
    fetchAPI<{ markers: Marker[] }>(`/api/map${selectedCategory !== "all" ? `?category=${selectedCategory}` : ""}`)
      .then((data) => setMarkers(data.markers))
      .catch(() => setMarkers([]))
      .finally(() => setLoading(false));
  }, [selectedCategory]);

  // Dynamic import for Leaflet map
  useEffect(() => {
    import("@/components/map-view").then((mod) => {
      setMapComponent(() => mod.MapView);
    });
  }, []);

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-3xl font-bold">Map</h1>
          <p className="text-muted-foreground text-sm mt-1">Explore Mangatarem on the interactive map</p>
        </div>
        <select
          value={selectedCategory}
          onChange={(e) => setSelectedCategory(e.target.value)}
          className="border rounded-md px-3 py-2 text-sm bg-background"
        >
          <option value="all">All Categories</option>
          <option value="Nature">Nature</option>
          <option value="Heritage">Heritage</option>
          <option value="Religious">Religious</option>
          <option value="Historical">Historical</option>
        </select>
      </div>

      {loading ? (
        <div className="flex items-center justify-center py-16 text-muted-foreground">
          <Loader2 className="h-6 w-6 animate-spin mr-2" /> Loading map...
        </div>
      ) : (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Map area */}
          <div className="lg:col-span-2">
            {MapComponent ? (
              <div className="rounded-lg overflow-hidden border h-[500px]">
                <MapComponent markers={markers} />
              </div>
            ) : (
              <div className="rounded-lg border h-[500px] bg-muted flex items-center justify-center text-muted-foreground">
                <MapPin className="h-12 w-12 opacity-30" />
              </div>
            )}
          </div>

          {/* Sidebar list */}
          <div className="space-y-2 max-h-[500px] overflow-y-auto">
            <h2 className="font-semibold text-sm text-muted-foreground mb-3">
              {markers.length} marker{markers.length !== 1 ? "s" : ""}
            </h2>
            {markers.map((m) => (
              <Link
                key={m.id}
                href={`/attractions/${m.id}`}
                className="block border rounded-lg p-3 hover:bg-muted transition-colors"
              >
                <h3 className="font-medium text-sm">{m.name}</h3>
                <p className="text-xs text-muted-foreground">
                  {m.category}{m.barangay_name ? ` · ${m.barangay_name}` : ""}
                </p>
              </Link>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
