import { CuratedTrail } from "./types";
import { PLACE_IMAGE_LOOKUP, LOCAL_ASSET_EXISTS } from "@/lib/place-images";

/**
 * Resolves an image URL to a clean local or remote path with fallback.
 *
 * - Externally hosted photos (uploads, etc.) are used as-is.
 * - Local asset paths are checked against the ones that actually exist.
 * - Otherwise falls back to a bundled local photo of the place, then a
 *   generic teaser image.
 */
export function resolvePlaceImage(imageUrl: string | null | undefined, name: string): string {
  if (imageUrl && !imageUrl.includes("placehold.co")) {
    // Placeholder services are treated as "no image".
    if (imageUrl.startsWith("/") || imageUrl.startsWith("http") || imageUrl.startsWith("data:")) {
      if (imageUrl.startsWith("/") && !imageUrl.includes("/uploads/")) {
        const basename = imageUrl.split("/").pop() ?? "";
        if (basename && !LOCAL_ASSET_EXISTS.has(basename)) {
          // Local file that isn't in public/img — map by attraction name instead.
          return matchLocalImage(name) ?? "/img/mangatarem_map_teaser.webp";
        }
        // Backend-served static (e.g. /static/img/foo.png) has no /static on the
        // frontend origin — the same file is bundled here, so serve it locally.
        if (imageUrl.startsWith("/static/")) {
          return "/img/" + basename;
        }
      }
      return imageUrl;
    }
  }

  // Known place-by-name fallback (bundled photos)
  const local = matchLocalImage(name);
  if (local) return local;

  // Generic category fallbacks
  return "/img/mangatarem_map_teaser.webp";
}

/** Case-insensitive substring lookup against bundled place photos. */
function matchLocalImage(name: string): string | undefined {
  const n = name.toLowerCase();
  for (const [key, path] of Object.entries(PLACE_IMAGE_LOOKUP)) {
    if (key.includes(n) || n.includes(key)) return path;
  }
  return undefined;
}

/**
 * Category styling, badges, and colors
 */
export const CATEGORY_CONFIG: Record<
  string,
  {
    label: string;
    color: string;
    bgClass: string;
    textClass: string;
    borderClass: string;
    pinColor: string;
    icon: string;
  }
> = {
  Nature: {
    label: "Nature & Eco-Tourism",
    color: "#16a34a",
    bgClass: "bg-emerald-500/10 dark:bg-emerald-500/20",
    textClass: "text-emerald-700 dark:text-emerald-300",
    borderClass: "border-emerald-500/30",
    pinColor: "#16a34a",
    icon: "TreePine",
  },
  Historical: {
    label: "Historical & Heritage",
    color: "#d97706",
    bgClass: "bg-amber-500/10 dark:bg-amber-500/20",
    textClass: "text-amber-700 dark:text-amber-300",
    borderClass: "border-amber-500/30",
    pinColor: "#d97706",
    icon: "Landmark",
  },
  Heritage: {
    label: "Cultural Heritage",
    color: "#b45309",
    bgClass: "bg-amber-600/10 dark:bg-amber-600/20",
    textClass: "text-amber-800 dark:text-amber-200",
    borderClass: "border-amber-600/30",
    pinColor: "#b45309",
    icon: "Landmark",
  },
  Religious: {
    label: "Religious & Faith",
    color: "#7c3aed",
    bgClass: "bg-violet-500/10 dark:bg-violet-500/20",
    textClass: "text-violet-700 dark:text-violet-300",
    borderClass: "border-violet-500/30",
    pinColor: "#7c3aed",
    icon: "Church",
  },
  "Public Space": {
    label: "Public Space & Parks",
    color: "#0d9488",
    bgClass: "bg-teal-500/10 dark:bg-teal-500/20",
    textClass: "text-teal-700 dark:text-teal-300",
    borderClass: "border-teal-500/30",
    pinColor: "#0d9488",
    icon: "Users",
  },
  "Food & Stay": {
    label: "Dining & Lodging",
    color: "#e11d48",
    bgClass: "bg-rose-500/10 dark:bg-rose-500/20",
    textClass: "text-rose-700 dark:text-rose-300",
    borderClass: "border-rose-500/30",
    pinColor: "#e11d48",
    icon: "Utensils",
  },
};

export const DEFAULT_CATEGORY_STYLE = {
  label: "Attraction",
  color: "#0284c7",
  bgClass: "bg-sky-500/10 dark:bg-sky-500/20",
  textClass: "text-sky-700 dark:text-sky-300",
  borderClass: "border-sky-500/30",
  pinColor: "#0284c7",
  icon: "MapPin",
};

/**
 * Pre-defined curated tour routes across Mangatarem
 */
export const CURATED_TRAILS: CuratedTrail[] = [
  {
    id: "eco-adventure",
    title: "Eco-Adventure Trail",
    subtitle: "Mountain vistas, hot springs & cascading falls",
    description:
      "A journey through the western mountains and protected landscapes of Mangatarem. Ride through the scenic ridges of Daang Kalikasan, relax in the natural hot springs of Manleluag, and hike to the hidden Timmanguyob Falls.",
    category: "Nature",
    distanceKm: 22.4,
    durationEst: "4-5 hours",
    difficulty: "Moderate",
    tags: ["Scenic Views", "Hot Springs", "Trekking", "Photography"],
    color: "#16a34a",
    stops: [
      {
        placeId: 2,
        name: "Daang Kalikasan",
        category: "Nature",
        barangay: "Malabobo",
        coordinates: [120.25, 15.7],
        tip: "Best visited early morning (6:00 - 8:30 AM) for golden sunrise lighting and cool mountain breeze.",
        order: 1,
      },
      {
        placeId: 1,
        name: "Manleluag Spring Protected Landscape",
        category: "Nature",
        barangay: "Malabobo",
        coordinates: [120.2833, 15.6667],
        tip: "Enjoy therapeutic sulfuric hot spring pools and shaded picnic cottages under century trees.",
        order: 2,
      },
      {
        placeId: 4,
        name: "Timmanguyob Falls",
        category: "Nature",
        barangay: "Cabaluyan",
        coordinates: [120.22, 15.65],
        tip: "Requires a 25-minute trail walk. Wear sturdy water-friendly footwear and bring hydration.",
        order: 3,
      },
    ],
    pathCoordinates: [
      [120.25, 15.7],
      [120.265, 15.685],
      [120.2833, 15.6667],
      [120.255, 15.658],
      [120.22, 15.65],
    ],
  },
  {
    id: "poblacion-heritage",
    title: "Poblacion Heritage & Cultural Walk",
    subtitle: "Colonial architecture, civic plaza & historic river",
    description:
      "Immerse yourself in Mangatarem's rich history and architectural heritage. Explore the century-old St. Raymund de Penafort Parish Church, historic municipal hall, town plaza, and the scenic Pacalat River promenade.",
    category: "Historical",
    distanceKm: 3.2,
    durationEst: "2 hours",
    difficulty: "Easy",
    tags: ["Colonial Heritage", "Walking Tour", "Architecture", "Family-Friendly"],
    color: "#d97706",
    stops: [
      {
        placeId: 7,
        name: "Municipal Town Plaza",
        category: "Public Space",
        barangay: "Poblacion",
        coordinates: [120.2928, 15.7891],
        tip: "Centrally located civic grounds with landmark monuments, shade trees, and local food stalls.",
        order: 1,
      },
      {
        placeId: 3,
        name: "St. Raymund de Penafort Church",
        category: "Historical",
        barangay: "Poblacion",
        coordinates: [120.2986, 15.7889],
        tip: "Founded in 1835. Notice the grand Spanish colonial facade, vintage belfry, and historic church bells.",
        order: 2,
      },
      {
        placeId: 5,
        name: "Pacalat River",
        category: "Nature",
        barangay: "Poblacion",
        coordinates: [120.2928, 15.7891],
        tip: "Peaceful riverbanks ideal for afternoon relaxation and sunset photography.",
        order: 3,
      },
    ],
    pathCoordinates: [
      [120.2928, 15.7891],
      [120.2955, 15.789],
      [120.2986, 15.7889],
      [120.296, 15.7885],
      [120.2928, 15.7891],
    ],
  },
  {
    id: "waterfalls-circuit",
    title: "Foothills & Waterfalls Circuit",
    subtitle: "Cascading cool waters and lush upland valleys",
    description:
      "A scenic circuit highlighting the hidden water gems of Mangatarem. Experience the cool waters of Canding Falls, cross the mountain ridgeway of Daang Kalikasan, and soak in Manleluag springs.",
    category: "Nature",
    distanceKm: 28.5,
    durationEst: "5-6 hours",
    difficulty: "Scenic Drive",
    tags: ["Waterfalls", "Mountain Highway", "Dip & Swim", "Day Tour"],
    color: "#0d9488",
    stops: [
      {
        placeId: 6,
        name: "Canding (Kanding) Falls",
        category: "Nature",
        barangay: "Poblacion",
        coordinates: [120.2928, 15.7891],
        tip: "Cool cascade with natural plunge pools nestled among forest boulders.",
        order: 1,
      },
      {
        placeId: 2,
        name: "Daang Kalikasan",
        category: "Nature",
        barangay: "Malabobo",
        coordinates: [120.25, 15.7],
        tip: "Panoramic mountain pass linking Mangatarem to Zambales.",
        order: 2,
      },
      {
        placeId: 1,
        name: "Manleluag Spring Protected Landscape",
        category: "Nature",
        barangay: "Malabobo",
        coordinates: [120.2833, 15.6667],
        tip: "Rejuvenating thermal mineral hot spring pools surrounded by lush greenery.",
        order: 3,
      },
    ],
    pathCoordinates: [
      [120.2928, 15.7891],
      [120.275, 15.74],
      [120.25, 15.7],
      [120.265, 15.685],
      [120.2833, 15.6667],
    ],
  },
];

/**
 * Haversine formula to compute great-circle distance between two points in km
 */
export function calculateDistance(
  lat1: number,
  lon1: number,
  lat2: number,
  lon2: number
): number {
  const R = 6371; // Radius of the Earth in km
  const dLat = (lat2 - lat1) * (Math.PI / 180);
  const dLon = (lon2 - lon1) * (Math.PI / 180);
  const a =
    Math.sin(dLat / 2) * Math.sin(dLat / 2) +
    Math.cos(lat1 * (Math.PI / 180)) *
      Math.cos(lat2 * (Math.PI / 180)) *
      Math.sin(dLon / 2) *
      Math.sin(dLon / 2);
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
  const d = R * c;
  return Math.round(d * 10) / 10;
}

/**
 * Format coordinates for clean human display
 */
export function formatCoordinates(lat: number, lng: number): string {
  const latDir = lat >= 0 ? "N" : "S";
  const lngDir = lng >= 0 ? "E" : "W";
  return `${Math.abs(lat).toFixed(4)}° ${latDir}, ${Math.abs(lng).toFixed(4)}° ${lngDir}`;
}
