import { CuratedTrail, MarkerPlace } from "./types";

/**
 * Local image fallbacks for Mangatarem landmarks
 */
export const LOCAL_PLACE_IMAGES: Record<string, string> = {
  "Manleluag Spring Protected Landscape": "/img/manleluag_spring.webp",
  "Daang Kalikasan": "/img/daang_kalikasan.webp",
  "St. Raymund de Penafort Church": "/img/st_raymund_church.webp",
  "Timmanguyob Falls": "/img/attractions/timmanguyob_falls.png",
  "Pacalat River": "/img/attractions/pacalat_river/image_1.jpg",
  "Canding (Kanding) Falls": "/img/attractions/canding_falls/image_1.jpg",
  "Municipal Town Plaza": "/img/attractions/municipal_hall/image_1.jpg",
};

/**
 * Resolves an image URL to a clean local or remote path with fallback
 */
export function resolvePlaceImage(imageUrl: string | null | undefined, name: string): string {
  if (imageUrl && !imageUrl.includes("placehold.co")) {
    return imageUrl;
  }

  for (const [key, path] of Object.entries(LOCAL_PLACE_IMAGES)) {
    if (name.toLowerCase().includes(key.toLowerCase()) || key.toLowerCase().includes(name.toLowerCase())) {
      return path;
    }
  }

  // Generic category fallbacks
  return "/img/mangatarem_map_teaser.webp";
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

/**
 * Curated fallback places used when API is cold or unseeded
 */
export const DEFAULT_PLACES: MarkerPlace[] = [
  {
    id: 1,
    name: "Manleluag Spring Protected Landscape",
    description: "A 1,935-hectare national protected landscape nestled in the foothills of the Zambales Mountain Range. Renowned for its natural sulfuric thermal hot springs, crystal-clear cold stream pools, lush dipterocarp forests, and riverside picnic cottages.",
    category: "Nature",
    latitude: 15.6667,
    longitude: 120.2833,
    image_url: "/img/manleluag_spring.webp",
    barangay_name: "Malabobo",
    is_featured: true,
    physical_status: "Open",
    advisory_status: "Normal",
    advisory_message: "Open to the public. Leave No Trace policy strictly enforced.",
    opening_hours: "6:00 AM – 5:30 PM Daily",
    entrance_fee: "₱30 (Adults) / ₱15 (Students & Seniors)",
    contact_info: "mangatarem.tourism@pangasinan.gov.ph",
    facilities: "Hot Spring Pools, Cold Stream Baths, Picnic Cottages, Restrooms, Parking",
    directions: "Romulo Highway toward Zambales border. Turn left at Brgy. Malabobo junction.",
  },
  {
    id: 2,
    name: "Daang Kalikasan",
    description: "A breathtaking 54-kilometer scenic mountain highway that traverses the undulating ridges of the Zambales Mountain Range, connecting Mangatarem to Santa Cruz, Zambales.",
    category: "Nature",
    latitude: 15.7000,
    longitude: 120.2500,
    image_url: "/img/daang_kalikasan.webp",
    barangay_name: "Malabobo",
    is_featured: true,
    physical_status: "Open",
    advisory_status: "Normal",
    advisory_message: "Drive with care. Heavy fog and clouds possible during early morning.",
    opening_hours: "6:00 AM – 6:00 PM Daily",
    entrance_fee: "Free Entry (Public Scenic Highway)",
    contact_info: null,
    facilities: "Viewpoints, Roadside Stalls, Parking Bays",
    directions: "From town center head southwest along Romulo Highway towards Brgy. Malabobo.",
  },
  {
    id: 3,
    name: "St. Raymund de Penafort Church",
    description: "A Spanish colonial brick-and-stone Roman Catholic church originally established by Dominican missionaries in 1835. Features a Baroque and Neoclassical facade constructed from local clay bricks.",
    category: "Historical",
    latitude: 15.7889,
    longitude: 120.2986,
    image_url: "/img/st_raymund_church.webp",
    barangay_name: "Poblacion",
    is_featured: true,
    physical_status: "Open",
    advisory_status: "Normal",
    advisory_message: "Active place of worship. Respect ongoing masses and ceremonies.",
    opening_hours: "5:30 AM – 7:00 PM Daily",
    entrance_fee: "Free Entry (Active Parish Church)",
    contact_info: "parish.mangatarem@lingayen-dagupan.org",
    facilities: "Parish Hall, Restrooms, Courtyard Plaza, Candle Chapel",
    directions: "Directly located at the town center along Romulo Highway fronting the municipal plaza.",
  },
  {
    id: 4,
    name: "Timmanguyob Falls",
    description: "A cascade hidden within the western mountain rainforest of Mangatarem. Features a secluded freshwater plunge pool and lush endemic forest flora.",
    category: "Nature",
    latitude: 15.6833,
    longitude: 120.2667,
    image_url: "/img/attractions/timmanguyob_falls.png",
    barangay_name: "Cabaluyan 2nd",
    is_featured: false,
    physical_status: "Open",
    advisory_status: "Guide Recommended",
    advisory_message: "Trek with local barangay guide. Trails can be slippery during rainy weather.",
    opening_hours: "6:00 AM – 4:30 PM Daily",
    entrance_fee: "₱20 Barangay Environmental Fee + Guide Fee",
    contact_info: null,
    facilities: "Natural Plunge Pool, Forest Trails, River Crossing Boulders",
    directions: "Access via Barangay Cabaluyan staging area followed by a 45-minute guided river trek.",
  },
  {
    id: 5,
    name: "Canding (Kanding) Falls",
    description: "A series of pristine mountain rapids, tiered cascades, and deep limestone pools surrounded by wild bamboo groves and rolling foothills.",
    category: "Nature",
    latitude: 15.7891,
    longitude: 120.2928,
    image_url: "/img/attractions/canding_falls/image_1.jpg",
    barangay_name: "Poblacion",
    is_featured: false,
    physical_status: "Open",
    advisory_status: "Normal",
    advisory_message: "Wear water shoes for slippery rock surfaces.",
    opening_hours: "7:00 AM – 5:00 PM Daily",
    entrance_fee: "₱20 Eco Fee",
    contact_info: null,
    facilities: "Natural Swimmable Pools, Bamboo Shade Huts, Staging Grounds",
    directions: "From town center proceed north-west to the trail jump-off point.",
  },
  {
    id: 6,
    name: "Pacalat River",
    description: "A historic waterway flowing through the heart of Mangatarem, offering scenic riverbanks, bamboo hanging bridges, and refreshing freshwater swimming.",
    category: "Nature",
    latitude: 15.7891,
    longitude: 120.2928,
    image_url: "/img/attractions/pacalat_river/image_1.jpg",
    barangay_name: "Poblacion",
    is_featured: false,
    physical_status: "Open",
    advisory_status: "Normal",
    advisory_message: "Do not swim during heavy rain upstream.",
    opening_hours: "Open 24 Hours",
    entrance_fee: "Free Access",
    contact_info: null,
    facilities: "Riverbanks, Shaded Trees, Walking Path",
    directions: "Accessible from the poblacion bridge and riverside embankments.",
  },
  {
    id: 7,
    name: "Municipal Town Plaza",
    description: "The municipal civic and cultural center featuring the historical municipal hall, war memorial, children's park, and landscaped civic gardens.",
    category: "Public Space",
    latitude: 15.7885,
    longitude: 120.2960,
    image_url: "/img/attractions/municipal_hall/image_1.jpg",
    barangay_name: "Poblacion",
    is_featured: false,
    physical_status: "Open",
    advisory_status: "Normal",
    advisory_message: "Open to the public for recreation and community strolls.",
    opening_hours: "Open 24 Hours",
    entrance_fee: "Free Access",
    contact_info: "info@mangatarem.gov.ph",
    facilities: "Open Plaza, Benches, Night Lighting, Event Stage, Children Playground",
    directions: "Town center, Poblacion, Mangatarem, Pangasinan.",
  },
];
