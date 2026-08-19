import {
  Landmark,
  TreePine,
  Music,
  Gem,
  Layers,
  Sparkles,
  BookOpen,
  MapPin,
  Building,
  ScrollText,
} from "lucide-react";

export interface HeritageItem {
  id: number;
  asset_type: "built" | "natural" | "intangible" | "movable" | "mixed" | string;
  name_of_asset: string;
  common_name?: string | null;
  barangay_id?: number | null;
  barangay_name?: string | null;
  location_details?: string | null;
  contact_person?: string | null;
  contact_number?: string | null;
  ownership_type?: string | null;
  owner_administrator?: string | null;
  usage_status?: string | null;
  latitude?: number | null;
  longitude?: number | null;
  significance?: string | null;
  conservation_status?: string | null;
  template_slug?: string | null;
  mapper_name?: string | null;
  date_profiled?: string | null;
  status?: string;
  image_url?: string | null;
  category?: string | null;
  stories?: string | null;
  protection_status?: string | null;
  created_at?: string | null;
  updated_at?: string | null;
  form_data?: Record<string, unknown> | null;
}

export interface HeritageTypeConfig {
  slug: string;
  label: string;
  label_plural: string;
  badgeLabel: string;
  subtitle: string;
  icon: typeof Landmark;
  color: string;
  badgeBg: string;
  borderColor: string;
  description: string;
  shortDesc: string;
}

export const HERITAGE_TYPES_CONFIG: Record<string, HeritageTypeConfig> = {
  built: {
    slug: "built",
    label: "Built Heritage",
    label_plural: "Built Heritage Sites",
    badgeLabel: "Built Landmark",
    subtitle: "Historic Architecture & Monuments",
    icon: Landmark,
    color: "text-amber-700 dark:text-amber-400",
    badgeBg: "bg-amber-100/80 text-amber-900 dark:bg-amber-950/60 dark:text-amber-300 border-amber-300 dark:border-amber-800",
    borderColor: "border-amber-200 dark:border-amber-900/40",
    description:
      "Historic civic buildings, Spanish-colonial religious architecture, century-old ancestral houses, and masonry monuments documenting the architectural heritage of Mangatarem.",
    shortDesc: "Civic buildings, churches, historic ancestral residences & monuments.",
  },
  natural: {
    slug: "natural",
    label: "Natural Heritage",
    label_plural: "Natural Heritage Sites",
    badgeLabel: "Natural Eco-Site",
    subtitle: "Protected Forests, Springs & Waterfalls",
    icon: TreePine,
    color: "text-emerald-700 dark:text-emerald-400",
    badgeBg: "bg-emerald-100/80 text-emerald-900 dark:bg-emerald-950/60 dark:text-emerald-300 border-emerald-300 dark:border-emerald-800",
    borderColor: "border-emerald-200 dark:border-emerald-900/40",
    description:
      "Protected natural landscapes, virgin rainforest reserves, thermal mineral springs, waterfalls, and freshwater river corridors in western Pangasinan.",
    shortDesc: "Hot springs, waterfalls, forest reserves & river watersheds.",
  },
  intangible: {
    slug: "intangible",
    label: "Intangible Heritage",
    label_plural: "Living Traditions & Lore",
    badgeLabel: "Living Tradition",
    subtitle: "Oral Lore, Culinary Arts & Folk Healing",
    icon: Music,
    color: "text-purple-700 dark:text-purple-400",
    badgeBg: "bg-purple-100/80 text-purple-900 dark:bg-purple-950/60 dark:text-purple-300 border-purple-300 dark:border-purple-800",
    borderColor: "border-purple-200 dark:border-purple-900/40",
    description:
      "Living cultural expressions including the traditional Tupig-making culinary craft, oral folklore of Manggat-Arem, indigenous botanical healing (Pang-agas), and performing arts.",
    shortDesc: "Tupig-making craft, oral legends, folk healing & living traditions.",
  },
  movable: {
    slug: "movable",
    label: "Movable Heritage",
    label_plural: "Historical Artifacts",
    badgeLabel: "Historic Artifact",
    subtitle: "Sacred Relics, Antique Bells & Museum Pieces",
    icon: Gem,
    color: "text-rose-700 dark:text-rose-400",
    badgeBg: "bg-rose-100/80 text-rose-900 dark:bg-rose-950/60 dark:text-rose-300 border-rose-300 dark:border-rose-800",
    borderColor: "border-rose-200 dark:border-rose-900/40",
    description:
      "Historical artifacts, 19th-century cast bronze church bells, sacred hardwood Santos, traditional rice milling implements (Lusong at Halo), and museum collections.",
    shortDesc: "Church bells, sacred relics, vintage farm implements & museum artifacts.",
  },
  mixed: {
    slug: "mixed",
    label: "Mixed Heritage",
    label_plural: "Cultural Landscapes",
    badgeLabel: "Cultural Landscape",
    subtitle: "Scenic Mountain Corridors & Historic Zones",
    icon: Layers,
    color: "text-sky-700 dark:text-sky-400",
    badgeBg: "bg-sky-100/80 text-sky-900 dark:bg-sky-950/60 dark:text-sky-300 border-sky-300 dark:border-sky-800",
    borderColor: "border-sky-200 dark:border-sky-900/40",
    description:
      "Integrated cultural landscapes combining protected mountain ecosystems with ancestral heritage routes, and preserved Spanish-colonial Poblacion town planning heritage.",
    shortDesc: "Poblacion historic zone, scenic mountain corridors & cultural landscapes.",
  },
};
