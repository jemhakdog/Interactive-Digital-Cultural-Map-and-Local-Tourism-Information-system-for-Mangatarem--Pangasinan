"use client";

import { useEffect, useRef } from "react";

interface Marker {
  id: number;
  name: string;
  category: string;
  latitude: number;
  longitude: number;
  barangay_name: string | null;
}

export function MapView({ markers }: { markers: Marker[] }) {
  const mapRef = useRef<HTMLDivElement>(null);
  const mapInstanceRef = useRef<unknown>(null);

  useEffect(() => {
    if (!mapRef.current || mapInstanceRef.current) return;

    // Dynamic import of Leaflet
    Promise.all([
      import("leaflet"),
      import("leaflet/dist/leaflet.css"),
    ]).then(([L]) => {
      if (!mapRef.current) return;

      const map = L.map(mapRef.current).setView([15.98, 120.0], 12);

      L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',
      }).addTo(map);

      // Category color map
      const colors: Record<string, string> = {
        Nature: "#22c55e",
        Heritage: "#f59e0b",
        Religious: "#8b5cf6",
        Historical: "#ef4444",
      };

      markers.forEach((m) => {
        const color = colors[m.category] || "#0ea5e9";
        const marker = L.circleMarker([m.latitude, m.longitude], {
          radius: 8,
          fillColor: color,
          color: "#fff",
          weight: 2,
          fillOpacity: 0.9,
        }).addTo(map);

        marker.bindPopup(`
          <div>
            <strong>${m.name}</strong><br/>
            <small>${m.category}${m.barangay_name ? ` · ${m.barangay_name}` : ""}</small>
          </div>
        `);
      });

      // Fit bounds
      if (markers.length > 0) {
        const bounds = L.latLngBounds(markers.map((m) => [m.latitude, m.longitude] as [number, number]));
        map.fitBounds(bounds, { padding: [50, 50] });
      }

      mapInstanceRef.current = map;
    });

    return () => {
      if (mapInstanceRef.current) {
        (mapInstanceRef.current as { remove: () => void }).remove();
        mapInstanceRef.current = null;
      }
    };
  }, [markers]);

  return <div ref={mapRef} className="w-full h-full" />;
}
