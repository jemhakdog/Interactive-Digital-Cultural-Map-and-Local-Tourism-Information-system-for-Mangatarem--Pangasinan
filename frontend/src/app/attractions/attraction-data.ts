import { AttractionItem } from "./attraction-types";
import { resolvePlaceImage } from "@/components/map/data";

/**
 * Curated rich metadata for Mangatarem Attractions
 */
export const CURATED_ATTRACTION_METADATA: Record<number, Partial<AttractionItem>> = {
  1: {
    id: 1,
    name: "Manleluag Spring Protected Landscape",
    category: "Nature",
    barangay_name: "Malabobo",
    latitude: 15.6667,
    longitude: 120.2833,
    description:
      "A 1,935-hectare national protected landscape nestled in the foothills of the Zambales Mountain Range. Renowned for its natural sulfuric thermal hot springs, crystal-clear cold stream pools, lush dipterocarp forests, shaded riverside picnic cottages under century-old tree canopies, and diverse endemic birdlife.",
    highlights: [
      "Natural Sulfuric Hot Springs & Mineral Baths with therapeutic relaxation benefits",
      "1,935-Hectare Protected National Forest Reserve & Biodiversity Sanctuary",
      "Riverside Picnic Cottages & Shaded Forest Pavilions",
      "Upland Nature Trekking Trails & Wildlife Birdwatching Vantage Points",
    ],
    facilities: [
      "Hot Spring Pools",
      "Cold Stream Baths",
      "Picnic Cottages",
      "Trekking Trails",
      "Restrooms & Shower",
      "Parking Area",
      "Refreshment Kiosks",
      "Souvenir Stalls",
      "Park Ranger Station",
    ],
    activities: [
      "Thermal Bathing & Soaking",
      "Picnicking & BBQ",
      "Forest Hiking & Trekking",
      "Birdwatching",
      "Nature Photography",
    ],
    entrance_fee: "₱30 (Adults) / ₱15 (Students & Seniors) / Free (Under 5)",
    opening_hours: "6:00 AM – 5:30 PM Daily (Open Year-Round)",
    best_time_to_visit: "Early morning (6:00 AM – 9:00 AM) or late afternoon for the most soothing thermal bath temperature and bird activity.",
    what_to_bring: [
      "Swimwear / Extra Change of Clothes",
      "Towel & Eco-friendly Toiletries",
      "Reusable Water Bottle & Snacks",
      "Trash Bag for Clean As You Go (CLAYGO)",
      "Cash for Entrance and Cottage Rentals",
    ],
    directions:
      "Located along Romulo Highway toward Zambales border. Turn left at the Barangay Malabobo junction (marked with DENR-PENRO welcome arch); proceed 2.5 km along the paved scenic access road to the park gate. Tricycles available at Mangatarem Public Market terminal.",
    advisory_status: "Normal",
    advisory_message:
      "Open to the public. Alcohol and glass containers are strictly prohibited in the thermal pool area. Leave No Trace policy strictly enforced.",
    difficulty: "Easy",
    elevation: "180m ASL",
    gallery: [
      "/img/manleluag_spring.webp",
      "/img/attractions/manleluag_spring_protected_landscape/image_1.jpg",
      "/img/attractions/manleluag_spring_protected_landscape/image_2.jpg",
      "/img/attractions/manleluag_spring_protected_landscape/image_3.jpg",
      "/img/attractions/manleluag_spring_protected_landscape/image_4.jpg",
      "/img/attractions/manleluag_spring_protected_landscape/image_5.jpg",
      "/img/attractions/manleluag_spring_protected_landscape/image_6.jpg",
      "/img/attractions/manleluag_spring_protected_landscape/image_7.jpg",
    ],
  },
  2: {
    id: 2,
    name: "Daang Kalikasan",
    category: "Nature",
    barangay_name: "Malabobo",
    latitude: 15.7,
    longitude: 120.25,
    description:
      "A scenic mountain highway spanning the ridgeways of the Zambales Mountain Range connecting Mangatarem, Pangasinan to Santa Cruz, Zambales. Celebrated as one of the most picturesque road trip, mototouring, and cycling destinations in Northern Luzon, featuring 360-degree panoramic views of rolling hills, sunrise sea of clouds, and mountain pine trees.",
    highlights: [
      "Sweeping Panoramic Mountain Ridge Views & Rolling Green Hills",
      "Spectacular Sunrise & Morning Sea of Clouds over Valley Ridges",
      "Iconic Serpentine Road Architecture & Scenic Viewpoint Pull-Offs",
      "Premier Northern Luzon Mototouring & Road Cycling Destination",
    ],
    facilities: [
      "Scenic Viewpoints & Stopovers",
      "Roadside Native Eateries (Karinderya)",
      "Fresh Coconut & Local Produce Stalls",
      "Designated Parking Bays",
      "Tourism Safety Checkpoint",
    ],
    activities: [
      "Scenic Road Trip & Mototouring",
      "Road Cycling & Hill Climbing",
      "Sunrise & Golden Hour Photography",
      "Sightseeing & Picnicking",
    ],
    entrance_fee: "Free Public Access (Eco-tourism guidelines apply)",
    opening_hours: "6:00 AM – 6:00 PM Daily (Daylight hours strictly advised for mountain driving)",
    best_time_to_visit: "5:30 AM – 8:30 AM for the morning sea of clouds and cool breeze, or 4:30 PM – 6:00 PM for golden sunset over the Zambales ranges.",
    what_to_bring: [
      "Windbreaker / Jacket (cool mountain breezes)",
      "Fully Fueled Vehicle / Road-Ready Bicycle",
      "Camera / Smartphone with Full Battery",
      "Drinking Water & Light Snacks",
    ],
    directions:
      "From Mangatarem town center, head southwest along Romulo Highway towards Barangay Malabobo. Follow directional signboards to Daang Kalikasan. Concrete 2-lane mountain highway with gentle to moderate gradients.",
    advisory_status: "Normal",
    advisory_message:
      "Mountain highway is open. Drive cautiously along sharp curves and downhill grades. Parking only permitted in designated scenic viewing bays. Camping along road shoulders is strictly prohibited.",
    difficulty: "Scenic Drive",
    elevation: "320m ASL",
    gallery: [
      "/img/daang_kalikasan.webp",
      "/img/attractions/daang_kalikasan/image_1.jpg",
      "/img/attractions/daang_kalikasan/image_2.jpg",
      "/img/attractions/daang_kalikasan/image_3.jpg",
      "/img/attractions/daang_kalikasan/image_4.jpg",
      "/img/attractions/daang_kalikasan/image_5.jpg",
    ],
  },
  3: {
    id: 3,
    name: "St. Raymund de Penafort Church",
    category: "Historical",
    barangay_name: "Poblacion",
    latitude: 15.7889,
    longitude: 120.2986,
    description:
      "Founded in 1835 by Dominican friars and completed in 1875, this monumental Spanish colonial church is built of massive red clay brick and mortar. Dedicated to Saint Raymund of Peñafort, it features a grand classical facade, historic 4-tier belfry, antique church bells, wooden rafters, and an expansive parish plaza representing the spiritual and historical epicenter of Mangatarem.",
    highlights: [
      "19th-Century Spanish Colonial Red-Brick Architecture & Massive Buttresses",
      "Historic 4-Tier Bell Tower with Antique Spanish-era Bells",
      "Grand High Altar (Retablo) and Historic Sacred Statues",
      "Peaceful Courtyard & Century-Old Convent Grounds",
    ],
    facilities: [
      "Parish Worship Hall",
      "Historic Belfry",
      "Parish Office & Religious Article Shop",
      "Courtyard Benches & Shaded Grounds",
      "Paved Parking",
      "Wheelchair Ramp Access",
      "Restrooms",
    ],
    activities: [
      "Holy Mass & Religious Reflection",
      "Architectural & Cultural Heritage Tour",
      "Pilgrimage & Devotional Visit",
      "Heritage Photography",
    ],
    entrance_fee: "Free (Voluntary donations for church heritage upkeep)",
    opening_hours: "5:00 AM – 7:00 PM Daily (Regular Mass schedules on weekends)",
    best_time_to_visit: "Morning (7:00 AM – 11:00 AM) or late afternoon during golden hour when sunlight illuminates the red brick facade.",
    what_to_bring: [
      "Modest attire (shoulders and knees covered for church visits)",
      "Camera / Phone for exterior heritage photography",
    ],
    directions:
      "Situated in the heart of Poblacion along the main municipal road directly across the Municipal Plaza and Town Hall. Easy walking distance from any point in the town center.",
    advisory_status: "Normal",
    advisory_message:
      "Active place of worship. Reverence and silence requested during liturgical celebrations and personal prayer.",
    difficulty: "Easy",
    elevation: "25m ASL",
    heritage_asset_type: "built_heritage",
    gallery: [
      "/img/st_raymund_church.webp",
      "/img/attractions/saint_raymund_de_penafort_parish_church/image_1.jpg",
      "/img/attractions/saint_raymund_de_penafort_parish_church/image_2.jpg",
      "/img/attractions/saint_raymund_de_penafort_parish_church/image_3.jpg",
      "/img/attractions/saint_raymund_de_penafort_parish_church/image_4.jpg",
      "/img/attractions/saint_raymund_de_penafort_parish_church/image_5.png",
    ],
  },
  4: {
    id: 4,
    name: "Timmanguyob Falls",
    category: "Nature",
    barangay_name: "Cabaluyan",
    latitude: 15.65,
    longitude: 120.22,
    description:
      "A multi-tiered cascading waterfall hidden within the lush western hills of Barangay Cabaluyan. Known for its crystal-clear emerald waters, natural rock plunge pools, and untouched tropical rainforest canopy. An ideal destination for eco-trekkers, adventurous hikers, and nature photographers seeking peaceful immersion in nature.",
    highlights: [
      "Multi-Tiered Cascading Waterfalls & Natural Cold Plunge Pool",
      "Untouched Forest Eco-Trail & Shaded River Crossings",
      "Natural Rock Formations & Rainforest Rest Stops",
      "Invigorating Freshwater Swimming & Forest Bathing",
    ],
    facilities: [
      "Trailhead Registration Desk",
      "Community Guide Station",
      "Bamboo Resting Benches",
      "Native Changing Enclosures",
    ],
    activities: [
      "Waterfall Swimming & Plunge Pool Dip",
      "Forest Trail Trekking",
      "Nature Photography",
      "Riverside Picnicking",
    ],
    entrance_fee: "₱20 (Environmental Fee) + Optional Local Guide Tip",
    opening_hours: "7:00 AM – 4:00 PM Daily (Trekking restricted after 3:30 PM for safety)",
    best_time_to_visit: "8:00 AM – 2:00 PM during dry to moderate rainy season (October to June) when water clarity is highest.",
    what_to_bring: [
      "Aqua shoes / Trekking sandals with good grip",
      "Dry bag for electronics and valuables",
      "Extra dry clothing & towel",
      "Reusable water bottle & energy snacks",
      "Biodegradable insect repellent",
    ],
    directions:
      "Take Romulo Highway south toward Cabaluyan; turn into the barangay access road toward the foothills. Register at the Barangay Tourism desk; trail begins with a scenic 20-30 minute guided foot trek along forest paths.",
    advisory_status: "Caution",
    advisory_message:
      "Wear anti-slip footwear. Rocks near waterfall base can be slippery. Swimming is supervised; always check water depth before diving.",
    difficulty: "Moderate",
    elevation: "140m ASL",
    gallery: [
      "/img/attractions/timmanguyob_falls.png",
      "/img/attractions/timmanguyob_falls/image_1.jpg",
      "/img/attractions/timmanguyob_falls/image_2.png",
      "/img/attractions/timmanguyob_falls/image_3.jpg",
    ],
  },
  6: {
    id: 6,
    name: "Canding (Kanding) Falls",
    category: "Nature",
    barangay_name: "Poblacion",
    latitude: 15.7891,
    longitude: 120.2928,
    description:
      "A serene cascading waterfall with natural cold mountain spring waters surrounded by rocky ravines and indigenous vegetation. A beloved local retreat for residents and travelers seeking quiet relaxation, refreshing dips, and peaceful nature picnics away from crowded tourist spots.",
    highlights: [
      "Natural Mountain Spring Cascades & Clear Plunge Pool",
      "Shaded Rocky Ravine Microclimate with Cool Mountain Air",
      "Peaceful Eco-Friendly Picnic Spots",
    ],
    facilities: [
      "Natural Boulder Seating",
      "Trail Path",
      "Footbridge Access",
      "Shaded Rest Area",
    ],
    activities: [
      "Cold Water Swimming",
      "Family Picnic",
      "Nature Walk",
      "Landscape Photography",
    ],
    entrance_fee: "Free Public Access / Community Donation",
    opening_hours: "7:00 AM – 5:00 PM Daily",
    best_time_to_visit: "Morning hours (8:00 AM – 11:30 AM) for gentle sunshine and crisp spring water.",
    what_to_bring: [
      "Towel & Swimwear",
      "Water Bottle & Light Snacks",
      "Eco Trash Bag for CLAYGO",
    ],
    directions:
      "Accessible via upland access road from Poblacion toward the western foothills. Tricycle or motorcycle access to trail head.",
    advisory_status: "Normal",
    advisory_message: "Practice Clean As You Go (CLAYGO). Respect the natural habitat and refrain from loud music.",
    difficulty: "Easy",
    elevation: "110m ASL",
    gallery: [
      "/img/attractions/canding_falls/image_1.jpg",
      "/img/attractions/canding_falls/image_2.jpg",
    ],
  },
  5: {
    id: 5,
    name: "Pacalat River",
    category: "Nature",
    barangay_name: "Poblacion",
    latitude: 15.7891,
    longitude: 120.2928,
    description:
      "The historic and ecological river artery flowing through Mangatarem. Featuring serene riverbanks, lush riparian vegetation, fresh breezes, and scenic spots where locals gather for afternoon strolls, riverside fishing, and peaceful sunset vistas reflecting over calm waters.",
    highlights: [
      "Scenic Riverbanks & Green Riparian Corridor",
      "Sunset Viewing Vantage Point over River Waters",
      "Peaceful Afternoon Strolls & Community Gathering",
    ],
    facilities: [
      "Riverside Walking Path",
      "Stone Benches",
      "Lighting along Promenade",
      "Street Food Stalls Nearby",
    ],
    activities: [
      "Riverside Walking & Jogging",
      "Sunset Watching",
      "Casual Fishing",
      "Street Food Dining",
    ],
    entrance_fee: "Free Public Access",
    opening_hours: "Open 24 Hours (Best from 5:00 AM to 8:00 PM)",
    best_time_to_visit: "4:30 PM – 6:30 PM for sunset golden hour reflection over the calm water.",
    what_to_bring: [
      "Comfortable Walking Shoes",
      "Camera / Phone for Sunset Shots",
      "Pocket money for local street snacks",
    ],
    directions:
      "Located within Poblacion, accessible via walking paths adjacent to the municipal civic center.",
    advisory_status: "Normal",
    advisory_message: "Keep riverbanks clean. Single-use plastics must be placed in designated trash bins.",
    difficulty: "Easy",
    elevation: "20m ASL",
    gallery: [
      "/img/attractions/pacalat_river/image_1.jpg",
      "/img/attractions/pacalat_river/image_2.jpg",
      "/img/attractions/pacalat_river/image_3.jpg",
      "/img/attractions/pacalat_river/image_4.jpg",
      "/img/attractions/pacalat_river/image_5.jpg",
    ],
  },
  7: {
    id: 7,
    name: "Municipal Town Plaza",
    category: "Public Space",
    barangay_name: "Poblacion",
    latitude: 15.7891,
    longitude: 120.2928,
    description:
      "The cultural, civic, and social heart of Mangatarem. Features the historic Dr. Jose Rizal monument, landscaped green gardens, covered municipal gymnasium, children's park, commemorative heritage markers, and community event stage. The primary meeting place for town fiestas, food fairs, and evening family leisure.",
    highlights: [
      "Historic Dr. Jose Rizal Monument & Heritage Markers",
      "Landscaped Civic Gardens & Shade Trees",
      "Central Venue for Town Fiestas, Food Fairs & Cultural Festivals",
      "Direct Proximity to Town Hall, Parish Church & Public Market",
    ],
    facilities: [
      "Plaza Benches & Gazebos",
      "Illuminated Walkways",
      "Public Restrooms",
      "Children's Playground Area",
      "Free Public Wi-Fi Zone",
      "Food Kiosks",
    ],
    activities: [
      "Civic & Cultural Events",
      "Evening Promenade",
      "Family Recreation",
      "Street Food & Local Delicacies",
    ],
    entrance_fee: "Free Public Access",
    opening_hours: "Open 24/7 (Plaza illumination active until 10:00 PM)",
    best_time_to_visit: "Late afternoon & evening (4:00 PM – 9:00 PM) when community street food vendors and lighting are active.",
    what_to_bring: [
      "Comfortable footwear",
      "Camera / Smartphone",
      "Pocket money for Tupig, Puto, and local delicacies",
    ],
    directions:
      "Directly located at town center intersection of Romulo Highway in Poblacion.",
    advisory_status: "Normal",
    advisory_message: "Family friendly civic park. Pet friendly on leash. Keep premises clean.",
    difficulty: "Easy",
    elevation: "22m ASL",
    gallery: [
      "/img/attractions/municipal_hall/image_1.jpg",
      "/img/attractions/municipal_hall/image_2.jpg",
      "/img/attractions/dr_jose_rizal_monument/image_1.png",
    ],
  },
};

/**
 * Merges raw API data with rich curated data and verified local photos
 */
export function enrichAttraction(raw: AttractionItem): AttractionItem {
  const curated = CURATED_ATTRACTION_METADATA[raw.id] || {};

  // Clean facilities into string array
  let facilitiesArray: string[] = [];
  if (Array.isArray(raw.facilities)) {
    facilitiesArray = raw.facilities;
  } else if (typeof raw.facilities === "string") {
    try {
      const parsed = JSON.parse(raw.facilities);
      if (Array.isArray(parsed)) facilitiesArray = parsed;
    } catch {
      facilitiesArray = raw.facilities.split(",").map((s) => s.trim()).filter(Boolean);
    }
  }

  if (facilitiesArray.length === 0 && curated.facilities) {
    facilitiesArray = curated.facilities as string[];
  }

  // Resolve best image path
  const resolvedImg = resolvePlaceImage(raw.image_url, raw.name);

  // Gallery resolution
  const gallery =
    curated.gallery && curated.gallery.length > 0
      ? curated.gallery
      : [resolvedImg];

  return {
    ...raw,
    name: raw.name,
    category: raw.category || curated.category || "Nature",
    barangay_name: raw.barangay_name || curated.barangay_name || "Mangatarem",
    description: raw.description || curated.description || "Discover the beauty and culture of Mangatarem.",
    image_url: resolvedImg,
    gallery,
    highlights: curated.highlights || [
      "Protected natural scenery and local biodiversity",
      "Authentic Pangasinan cultural landscape",
      "Family-friendly outdoor destination",
    ],
    facilities: facilitiesArray.length > 0 ? facilitiesArray : [
      "Open Grounds",
      "Rest Area",
      "Access Road",
    ],
    activities: curated.activities || [
      "Sightseeing",
      "Nature Photography",
      "Cultural Tour",
    ],
    entrance_fee: raw.entrance_fee || curated.entrance_fee || "Free Public Access",
    opening_hours: raw.opening_hours || curated.opening_hours || "Open Daily (Daylight Hours)",
    best_time_to_visit: curated.best_time_to_visit || "Morning or late afternoon for comfortable temperatures.",
    what_to_bring: curated.what_to_bring || [
      "Comfortable clothing & footwear",
      "Reusable water bottle",
      "Camera or smartphone",
      "Trash bag (Leave No Trace)",
    ],
    directions: raw.directions || curated.directions || "Accessible via Romulo Highway in Mangatarem, Pangasinan.",
    advisory_status: raw.advisory_status || curated.advisory_status || "Normal",
    advisory_message: raw.advisory_message || curated.advisory_message || "Open to all visitors. Keep surroundings clean.",
    physical_status: raw.physical_status || "Open Public",
    is_verified: raw.is_verified ?? true,
    is_featured: raw.is_featured ?? false,
    rating: raw.rating ?? (raw.id === 1 ? 5.0 : raw.id === 2 ? 4.9 : raw.id === 3 ? 4.8 : raw.id === 4 ? 4.7 : 4.6),
    review_count: raw.review_count ?? (raw.id === 1 ? 14 : raw.id === 2 ? 28 : raw.id === 3 ? 19 : 8),
    difficulty: curated.difficulty || "Easy",
    elevation: curated.elevation || "25m ASL",
  };
}
