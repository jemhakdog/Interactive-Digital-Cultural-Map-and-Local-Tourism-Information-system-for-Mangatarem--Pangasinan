export interface MarkerPlace {
  id: number;
  name: string;
  description: string | null;
  category: string;
  latitude: number;
  longitude: number;
  image_url: string | null;
  barangay_name: string | null;
  is_featured: boolean;
  physical_status: string | null;
  advisory_status: string | null;
  advisory_message: string | null;
  opening_hours: string | null;
  entrance_fee: string | null;
  contact_info: string | null;
  facilities: string | null;
  directions: string | null;
  distanceKm?: number;
}

export interface TrailStop {
  placeId?: number;
  name: string;
  category: string;
  barangay: string;
  coordinates: [number, number]; // [lng, lat]
  tip: string;
  order: number;
}

export interface CuratedTrail {
  id: string;
  title: string;
  subtitle: string;
  description: string;
  category: string;
  distanceKm: number;
  durationEst: string;
  difficulty: "Easy" | "Moderate" | "Scenic Drive";
  tags: string[];
  color: string;
  stops: TrailStop[];
  pathCoordinates: [number, number][]; // [lng, lat] sequence
}

export interface UserLocation {
  latitude: number;
  longitude: number;
  accuracy?: number;
}

export type MapStyleOption = "voyager" | "positron" | "dark-matter";
export type ViewMode = "split" | "full" | "grid";
export type SortOption = "featured" | "name" | "distance";
