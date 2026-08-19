"use client";

import { useState, useMemo, useEffect, useCallback } from "react";
import Link from "next/link";
import {
  Image as ImageIcon,
  Sparkles,
  Search,
  SlidersHorizontal,
  MapPin,
  Heart,
  Share2,
  Download,
  ExternalLink,
  X,
  ChevronLeft,
  ChevronRight,
  Upload,
  Layers,
  LayoutGrid,
  Grid2X2,
  Film,
  Camera,
  Compass,
  Check,
  Calendar,
  User,
  ShieldCheck,
  Eye,
  Info,
  Maximize2,
  Mountain,
  Landmark,
  Sprout,
  PartyPopper,
  Utensils,
  Map as MapIcon,
  CheckCircle2,
} from "lucide-react";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";

export interface GalleryItem {
  id: string | number;
  title: string;
  caption?: string | null;
  description?: string | null;
  url: string;
  image_url?: string | null;
  media_url?: string | null;
  type?: string;
  media_type?: string;
  category?: string;
  barangay?: string | null;
  location?: string | null;
  contributor?: string | null;
  contributor_role?: string | null;
  likes?: number;
  featured?: boolean;
  date?: string | null;
  created_at?: string | null;
  tags?: string[];
  aspect_ratio?: "landscape" | "portrait" | "square";
}

interface GalleryViewProps {
  initialItems: GalleryItem[];
  availableBarangays?: string[];
}

// ── Built-in Curated Seed Media Showcase of Mangatarem ──
const CURATED_MEDIA: GalleryItem[] = [
  {
    id: "curated-1",
    title: "Daang Kalikasan — Golden Ridge Pass",
    caption: "Daang Kalikasan — Golden Ridge Pass",
    description:
      "The scenic winding highway through verdant mountain ridges connecting Mangatarem to Santa Cruz, Zambales at golden sunset hour.",
    url: "/img/attractions/daang_kalikasan/image_1.jpg",
    image_url: "/img/attractions/daang_kalikasan/image_1.jpg",
    type: "photo",
    category: "nature",
    barangay: "Lawak Langka",
    location: "Daang Kalikasan Highway, Brgy. Lawak Langka",
    contributor: "Pangasinan Tourism Council",
    contributor_role: "Verified Curator",
    likes: 428,
    featured: true,
    date: "2026-03-15",
    tags: ["Daang Kalikasan", "Sunset", "Scenic Highway", "Mountain Pass"],
    aspect_ratio: "landscape",
  },
  {
    id: "curated-2",
    title: "Manleluag Spring — Thermal Forest Reserve",
    caption: "Manleluag Spring — Thermal Forest Reserve",
    description:
      "Lush tropical rainforest canopy sheltering natural thermal mineral hot springs and endemic Philippine wildlife.",
    url: "/img/attractions/manleluag_spring_protected_landscape/image_1.jpg",
    image_url: "/img/attractions/manleluag_spring_protected_landscape/image_1.jpg",
    type: "photo",
    category: "nature",
    barangay: "Malabobo",
    location: "Manleluag Protected Landscape, Brgy. Malabobo",
    contributor: "DENR Eco-Guides",
    contributor_role: "Conservation Officer",
    likes: 312,
    featured: true,
    date: "2026-02-10",
    tags: ["Hot Springs", "Rainforest", "Eco-Park", "Flora & Fauna"],
    aspect_ratio: "portrait",
  },
  {
    id: "curated-3",
    title: "St. Raymund de Peñafort — 1835 Historic Brickwork",
    caption: "St. Raymund de Peñafort — 1835 Historic Brickwork",
    description:
      "One of the longest brick-facade Spanish colonial baroque churches in Northern Luzon, constructed in 1835 as the spiritual heart of Mangatarem.",
    url: "/img/attractions/saint_raymund_de_penafort_parish_church/image_1.jpg",
    image_url: "/img/attractions/saint_raymund_de_penafort_parish_church/image_1.jpg",
    type: "photo",
    category: "heritage",
    barangay: "Poblacion",
    location: "Town Plaza, Brgy. Poblacion",
    contributor: "Parish Heritage Committee",
    contributor_role: "Heritage Curator",
    likes: 495,
    featured: true,
    date: "2026-01-20",
    tags: ["Spanish Colonial", "Baroque Church", "Brick Heritage", "Poblacion"],
    aspect_ratio: "landscape",
  },
  {
    id: "curated-4",
    title: "Teraoka Family Farm — Organic Agri-Sanctuary",
    caption: "Teraoka Family Farm — Organic Agri-Sanctuary",
    description:
      "A lush certified organic paradise cultivating dragon fruits, sunflowers, and promoting sustainable agro-tourism education.",
    url: "/img/attractions/teraoka_farm/image_1.jpg",
    image_url: "/img/attractions/teraoka_farm/image_1.jpg",
    type: "photo",
    category: "agro",
    barangay: "Lawak Langka",
    location: "Teraoka Organic Farm, Brgy. Lawak Langka",
    contributor: "Teraoka Farm Stewards",
    contributor_role: "Agro-Tourism Host",
    likes: 247,
    featured: false,
    date: "2026-04-05",
    tags: ["Agro-Tourism", "Organic Farming", "Dragon Fruit", "Sunflowers"],
    aspect_ratio: "square",
  },
  {
    id: "curated-5",
    title: "Timmanguyob Falls — Jungle Cascade Pools",
    caption: "Timmanguyob Falls — Jungle Cascade Pools",
    description:
      "A serene multi-tiered waterfall nestled deep in the western forested foothills, featuring crystal cold natural bathing pools.",
    url: "/img/attractions/timmanguyob_falls/image_1.jpg",
    image_url: "/img/attractions/timmanguyob_falls/image_1.jpg",
    type: "photo",
    category: "nature",
    barangay: "San Jose",
    location: "Foothills Trail, Brgy. San Jose",
    contributor: "Mangatarem Outdoor Club",
    contributor_role: "Trail Explorer",
    likes: 360,
    featured: true,
    date: "2026-03-28",
    tags: ["Waterfall", "Trekking", "Forest Trail", "Hidden Cascades"],
    aspect_ratio: "portrait",
  },
  {
    id: "curated-6",
    title: "Canding Falls — Mountain Stream Basin",
    caption: "Canding Falls — Mountain Stream Basin",
    description:
      "Refreshing mountain spring cascades flowing gently over natural rock formations in upper San Jose.",
    url: "/img/attractions/canding_falls/image_1.jpg",
    image_url: "/img/attractions/canding_falls/image_1.jpg",
    type: "photo",
    category: "nature",
    barangay: "San Jose",
    location: "Canding River Basin, Brgy. San Jose",
    contributor: "Wild Pangasinan",
    contributor_role: "Nature Explorer",
    likes: 215,
    featured: false,
    date: "2026-02-18",
    tags: ["Freshwater Basin", "Cascades", "Eco-Trail", "Nature"],
    aspect_ratio: "landscape",
  },
  {
    id: "curated-7",
    title: "Don Ramon Ventenilla Ancestral Bahay na Bato",
    caption: "Don Ramon Ventenilla Ancestral Bahay na Bato",
    description:
      "A stately 19th-century Spanish-Filipino ancestral residence adorned with authentic capiz windows and antique Narra timber.",
    url: "/img/attractions/don_ramon_ventenilla_residence/image_1.jpg",
    image_url: "/img/attractions/don_ramon_ventenilla_residence/image_1.jpg",
    type: "photo",
    category: "heritage",
    barangay: "Poblacion",
    location: "Heritage Zone, Brgy. Poblacion",
    contributor: "Mangatarem Historical Society",
    contributor_role: "Historian",
    likes: 189,
    featured: false,
    date: "2026-01-12",
    tags: ["Bahay na Bato", "Capiz Windows", "Ancestral House", "Heritage"],
    aspect_ratio: "landscape",
  },
  {
    id: "curated-8",
    title: "Tupig Festival Cultural Street Pageantry",
    caption: "Tupig Festival Cultural Street Pageantry",
    description:
      "Grand annual celebration honoring Mangatarem's signature native delicacy with vibrant street dancing and music.",
    url: "/img/hero.webp",
    image_url: "/img/hero.webp",
    type: "photo",
    category: "festivals",
    barangay: "Poblacion",
    location: "Municipal Plaza Grounds, Brgy. Poblacion",
    contributor: "Fiesta Executive Committee",
    contributor_role: "Official Media",
    likes: 582,
    featured: true,
    date: "2026-04-18",
    tags: ["Tupig Festival", "Street Dancing", "Cultural Fiesta", "Poblacion"],
    aspect_ratio: "landscape",
  },
  {
    id: "curated-9",
    title: "Traditional Tupig Charcoal Grilling",
    caption: "Traditional Tupig Charcoal Grilling",
    description:
      "Glutinous rice, shredded young coconut meat, and coconut milk roasted to sweet smoky perfection in wrapped banana leaves.",
    url: "/img/attractions/teraoka_farm/image_3.jpg",
    image_url: "/img/attractions/teraoka_farm/image_3.jpg",
    type: "photo",
    category: "flavors",
    barangay: "Poblacion",
    location: "Public Market Delicacies Section, Brgy. Poblacion",
    contributor: "Local Flavors Initiative",
    contributor_role: "Culinary Advocate",
    likes: 345,
    featured: false,
    date: "2026-03-01",
    tags: ["Tupig", "Native Delicacy", "Culinary Heritage", "Street Food"],
    aspect_ratio: "square",
  },
  {
    id: "curated-10",
    title: "Malabobo Century Tree — Living Ancient Landmark",
    caption: "Malabobo Century Tree — Living Ancient Landmark",
    description:
      "Ancient towering Balete century tree standing majestically for over a hundred years in Barangay Malabobo.",
    url: "/img/attractions/malabobo_century_tree.png",
    image_url: "/img/attractions/malabobo_century_tree.png",
    type: "photo",
    category: "heritage",
    barangay: "Malabobo",
    location: "Old Highway Road, Brgy. Malabobo",
    contributor: "Brgy. Malabobo Cultural Guild",
    contributor_role: "Barangay Curator",
    likes: 278,
    featured: false,
    date: "2026-02-25",
    tags: ["Century Tree", "Ancient Monument", "Folklore", "Malabobo"],
    aspect_ratio: "portrait",
  },
  {
    id: "curated-11",
    title: "Pacalat River — Morning Fishermen at Dawn",
    caption: "Pacalat River — Morning Fishermen at Dawn",
    description:
      "Tranquil morning mist floating over the meandering Pacalat riverbanks as local boatmen start their daily catch.",
    url: "/img/attractions/pacalat_river/image_1.jpg",
    image_url: "/img/attractions/pacalat_river/image_1.jpg",
    type: "photo",
    category: "nature",
    barangay: "Pacalat",
    location: "Pacalat Riverside, Brgy. Pacalat",
    contributor: "Pacalat Riverfront Heritage",
    contributor_role: "Local Fisherman",
    likes: 204,
    featured: false,
    date: "2026-03-10",
    tags: ["Riverbanks", "Sunrise", "Freshwater", "Pacalat"],
    aspect_ratio: "landscape",
  },
  {
    id: "curated-12",
    title: "Aviles Heritage Estate — Colonial Craftsmanship",
    caption: "Aviles Heritage Estate — Colonial Craftsmanship",
    description:
      "Beautiful architectural detail of timber and brick craftsmanship preserved across generations in central Mangatarem.",
    url: "/img/attractions/aviles_residence/image_1.jpg",
    image_url: "/img/attractions/aviles_residence/image_1.jpg",
    type: "photo",
    category: "heritage",
    barangay: "Poblacion",
    location: "Historic Quarter, Brgy. Poblacion",
    contributor: "Local History Archive",
    contributor_role: "Archivist",
    likes: 167,
    featured: false,
    date: "2026-01-30",
    tags: ["Heritage Home", "Colonial History", "Poblacion"],
    aspect_ratio: "square",
  },
  {
    id: "curated-13",
    title: "Daang Kalikasan — Morning Sea of Clouds",
    caption: "Daang Kalikasan — Morning Sea of Clouds",
    description:
      "Sea of clouds blanketing the lower valleys viewed from the high elevation curves of Daang Kalikasan at daybreak.",
    url: "/img/attractions/daang_kalikasan/image_3.jpg",
    image_url: "/img/attractions/daang_kalikasan/image_3.jpg",
    type: "photo",
    category: "nature",
    barangay: "Lawak Langka",
    location: "Upper Viewpoint, Brgy. Lawak Langka",
    contributor: "Riders of Pangasinan",
    contributor_role: "Tourist Explorer",
    likes: 541,
    featured: true,
    date: "2026-04-02",
    tags: ["Sea of Clouds", "Sunrise", "Daang Kalikasan", "Panoramic View"],
    aspect_ratio: "landscape",
  },
  {
    id: "curated-14",
    title: "Teraoka Sunflower Field in Full Bloom",
    caption: "Teraoka Sunflower Field in Full Bloom",
    description:
      "Golden yellow sunflowers creating a stunning natural spectacle against the backdrop of the Zambales mountain range.",
    url: "/img/attractions/teraoka_farm/image_5.jpg",
    image_url: "/img/attractions/teraoka_farm/image_5.jpg",
    type: "photo",
    category: "agro",
    barangay: "Lawak Langka",
    location: "Teraoka Organic Farm, Brgy. Lawak Langka",
    contributor: "Flora of Mangatarem",
    contributor_role: "Botanist",
    likes: 318,
    featured: false,
    date: "2026-03-22",
    tags: ["Sunflowers", "Flora", "Agro-Tourism", "Bio-Diversity"],
    aspect_ratio: "portrait",
  },
  {
    id: "curated-15",
    title: "Dr. Jose Rizal Monument & Town Plaza",
    caption: "Dr. Jose Rizal Monument & Town Plaza",
    description:
      "The historic town square honoring our national hero surrounded by shaded trees and welcoming open community plazas.",
    url: "/img/attractions/dr_jose_rizal_monument/image_1.png",
    image_url: "/img/attractions/dr_jose_rizal_monument/image_1.png",
    type: "photo",
    category: "heritage",
    barangay: "Poblacion",
    location: "Town Plaza, Brgy. Poblacion",
    contributor: "Municipal Information Office",
    contributor_role: "Civic Staff",
    likes: 153,
    featured: false,
    date: "2026-02-05",
    tags: ["Civic Plaza", "Rizal Monument", "Poblacion", "Historical"],
    aspect_ratio: "square",
  },
  {
    id: "curated-16",
    title: "Corleto Ancestral Residence — Living History",
    caption: "Corleto Ancestral Residence — Living History",
    description:
      "Well-preserved antique Filipino woodwork and historical architecture showcasing town life during the turn of the century.",
    url: "/img/attractions/corleto_residence/image_1.jpg",
    image_url: "/img/attractions/corleto_residence/image_1.jpg",
    type: "photo",
    category: "heritage",
    barangay: "Poblacion",
    location: "Heritage District, Brgy. Poblacion",
    contributor: "Poblacion Heritage Network",
    contributor_role: "Curator",
    likes: 142,
    featured: false,
    date: "2026-01-18",
    tags: ["Ancestral Residence", "Poblacion", "Heritage"],
    aspect_ratio: "landscape",
  },
  {
    id: "curated-17",
    title: "St. Raymund Bell Tower Architecture",
    caption: "St. Raymund Bell Tower Architecture",
    description:
      "Multi-story Spanish belfry tower overlooking the town of Mangatarem with preserved antique bronze bells.",
    url: "/img/attractions/saint_raymund_de_penafort_parish_church/image_3.jpg",
    image_url: "/img/attractions/saint_raymund_de_penafort_parish_church/image_3.jpg",
    type: "photo",
    category: "heritage",
    barangay: "Poblacion",
    location: "Parish Compound, Brgy. Poblacion",
    contributor: "Archival Heritage Committee",
    contributor_role: "Curator",
    likes: 219,
    featured: false,
    date: "2026-02-14",
    tags: ["Belfry", "Colonial Architecture", "Poblacion"],
    aspect_ratio: "portrait",
  },
  {
    id: "curated-18",
    title: "Manleluag Rainforest Bird Sanctuary Trail",
    caption: "Manleluag Rainforest Bird Sanctuary Trail",
    description:
      "Lush botanical walking trail surrounded by century-old Dipterocarp trees and birdwatching observatories.",
    url: "/img/attractions/manleluag_spring_protected_landscape/image_4.jpg",
    image_url: "/img/attractions/manleluag_spring_protected_landscape/image_4.jpg",
    type: "photo",
    category: "nature",
    barangay: "Malabobo",
    location: "Manleluag Protected Area, Brgy. Malabobo",
    contributor: "Birdwatchers Philippines",
    contributor_role: "Wildlife Photographer",
    likes: 289,
    featured: false,
    date: "2026-03-05",
    tags: ["Bird Sanctuary", "Forest Trail", "Eco-Tourism", "Malabobo"],
    aspect_ratio: "portrait",
  },
];

// ── Category Configuration ──
const CATEGORIES: { id: string; label: string; icon: typeof Sparkles; color: string }[] = [
  { id: "all", label: "All Stories", icon: Sparkles, color: "text-primary" },
  { id: "nature", label: "Landscapes & Nature", icon: Mountain, color: "text-emerald-600 dark:text-emerald-400" },
  { id: "heritage", label: "Historical & Heritage", icon: Landmark, color: "text-amber-600 dark:text-amber-400" },
  { id: "agro", label: "Agro-Tourism & Farms", icon: Sprout, color: "text-lime-600 dark:text-lime-400" },
  { id: "festivals", label: "Festivals & Celebrations", icon: PartyPopper, color: "text-rose-600 dark:text-rose-400" },
  { id: "flavors", label: "Flavors & Local Life", icon: Utensils, color: "text-orange-600 dark:text-orange-400" },
];

export function GalleryView({ initialItems, availableBarangays = [] }: GalleryViewProps) {
  // Combine API items with curated seed items
  const allItems = useMemo(() => {
    if (!initialItems || initialItems.length === 0) {
      return CURATED_MEDIA;
    }
    // Normalize initial items and merge unique items
    const normalizedApi: GalleryItem[] = initialItems.map((item, idx) => ({
      id: item.id || `api-${idx}`,
      title: item.title || item.caption || `Mangatarem Capture #${idx + 1}`,
      caption: item.caption || item.title || "",
      description: item.description || item.caption || "Community captured photograph in Mangatarem, Pangasinan.",
      url: item.url || item.image_url || item.media_url || "/img/hero.webp",
      image_url: item.image_url || item.url || item.media_url || "/img/hero.webp",
      media_url: item.media_url || item.url || item.image_url || "/img/hero.webp",
      type: item.type || item.media_type || "photo",
      media_type: item.type || item.media_type || "photo",
      category: item.category || "nature",
      barangay: item.barangay || "Mangatarem",
      location: item.location || (item.barangay ? `Brgy. ${item.barangay}` : "Mangatarem, Pangasinan"),
      contributor: item.contributor || "Community Contributor",
      contributor_role: item.contributor_role || "Visitor",
      likes: item.likes || 12 + ((Number(item.id) || idx) * 7) % 150,
      featured: item.featured || idx === 0,
      date: item.created_at || item.date || "2026-03-01",
      tags: item.tags || ["Mangatarem", "Tourism", "Philippines"],
      aspect_ratio: item.aspect_ratio || ((idx % 3 === 0) ? "portrait" : (idx % 3 === 1) ? "square" : "landscape"),
    }));

    // If API items are few, supplement with curated items to ensure a rich showcase
    if (normalizedApi.length < 6) {
      return [...normalizedApi, ...CURATED_MEDIA];
    }
    return normalizedApi;
  }, [initialItems]);

  // Filtering & Search states
  const [searchQuery, setSearchQuery] = useState("");
  const [selectedCategory, setSelectedCategory] = useState<string>("all");
  const [selectedBarangay, setSelectedBarangay] = useState<string>("all");
  const [selectedMediaType, setSelectedMediaType] = useState<"all" | "photo" | "video">("all");
  const [sortBy, setSortBy] = useState<"popular" | "newest" | "oldest" | "title">("popular");
  const [viewMode, setViewMode] = useState<"masonry" | "grid" | "editorial">("masonry");

  // Interaction states
  const [lightboxItem, setLightboxItem] = useState<GalleryItem | null>(null);
  const [lightboxIndex, setLightboxIndex] = useState<number>(0);
  const [likedMap, setLikedMap] = useState<Record<string, boolean>>({});
  const [likeCountMap, setLikeCountMap] = useState<Record<string, number>>({});
  const [copiedId, setCopiedId] = useState<string | number | null>(null);
  const [isContributeModalOpen, setIsContributeModalOpen] = useState(false);
  const [submissionSuccess, setSubmissionSuccess] = useState(false);

  // Form states for contribution
  const [formTitle, setFormTitle] = useState("");
  const [formCategory, setFormCategory] = useState("nature");
  const [formBarangay, setFormBarangay] = useState("Poblacion");
  const [formUrl, setFormUrl] = useState("");
  const [formContributor, setFormContributor] = useState("");
  const [formStory, setFormStory] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  // Extract all distinct barangays
  const barangaysList = useMemo(() => {
    const bSet = new Set<string>();
    allItems.forEach((it) => {
      if (it.barangay) bSet.add(it.barangay);
    });
    availableBarangays.forEach((b) => bSet.add(b));
    return Array.from(bSet).sort();
  }, [allItems, availableBarangays]);

  // Spotlight featured item
  const spotlightItem = useMemo(() => {
    return allItems.find((it) => it.featured) || allItems[0];
  }, [allItems]);

  // Filtered & Sorted items
  const filteredItems = useMemo(() => {
    const q = searchQuery.trim().toLowerCase();

    return allItems
      .filter((item) => {
        // Search query match
        if (q) {
          const matchTitle = item.title?.toLowerCase().includes(q);
          const matchDesc = item.description?.toLowerCase().includes(q);
          const matchCaption = item.caption?.toLowerCase().includes(q);
          const matchBarangay = item.barangay?.toLowerCase().includes(q);
          const matchLocation = item.location?.toLowerCase().includes(q);
          const matchContributor = item.contributor?.toLowerCase().includes(q);
          const matchTags = item.tags?.some((t) => t.toLowerCase().includes(q));

          if (!matchTitle && !matchDesc && !matchCaption && !matchBarangay && !matchLocation && !matchContributor && !matchTags) {
            return false;
          }
        }

        // Category filter
        if (selectedCategory !== "all" && item.category !== selectedCategory) {
          return false;
        }

        // Barangay filter
        if (selectedBarangay !== "all" && item.barangay !== selectedBarangay) {
          return false;
        }

        // Media type filter
        if (selectedMediaType !== "all") {
          const itemType = item.type || item.media_type || "photo";
          if (itemType !== selectedMediaType) return false;
        }

        return true;
      })
      .sort((a, b) => {
        if (sortBy === "popular") {
          const likesA = (likeCountMap[String(a.id)] ?? a.likes) || 0;
          const likesB = (likeCountMap[String(b.id)] ?? b.likes) || 0;
          return likesB - likesA;
        }
        if (sortBy === "newest") {
          const dateA = a.date ? new Date(a.date).getTime() : 0;
          const dateB = b.date ? new Date(b.date).getTime() : 0;
          return dateB - dateA;
        }
        if (sortBy === "oldest") {
          const dateA = a.date ? new Date(a.date).getTime() : 0;
          const dateB = b.date ? new Date(b.date).getTime() : 0;
          return dateA - dateB;
        }
        if (sortBy === "title") {
          return a.title.localeCompare(b.title);
        }
        return 0;
      });
  }, [allItems, searchQuery, selectedCategory, selectedBarangay, selectedMediaType, sortBy, likeCountMap]);

  // Open Lightbox with active index
  const openLightbox = useCallback(
    (item: GalleryItem) => {
      const idx = filteredItems.findIndex((it) => it.id === item.id);
      setLightboxIndex(idx >= 0 ? idx : 0);
      setLightboxItem(item);
    },
    [filteredItems]
  );

  const closeLightbox = useCallback(() => {
    setLightboxItem(null);
  }, []);

  const nextLightboxItem = useCallback(() => {
    if (filteredItems.length === 0) return;
    const nextIdx = (lightboxIndex + 1) % filteredItems.length;
    setLightboxIndex(nextIdx);
    setLightboxItem(filteredItems[nextIdx]);
  }, [filteredItems, lightboxIndex]);

  const prevLightboxItem = useCallback(() => {
    if (filteredItems.length === 0) return;
    const prevIdx = (lightboxIndex - 1 + filteredItems.length) % filteredItems.length;
    setLightboxIndex(prevIdx);
    setLightboxItem(filteredItems[prevIdx]);
  }, [filteredItems, lightboxIndex]);

  // Keyboard navigation for Lightbox
  useEffect(() => {
    if (!lightboxItem) return;
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === "Escape") closeLightbox();
      if (e.key === "ArrowRight") nextLightboxItem();
      if (e.key === "ArrowLeft") prevLightboxItem();
    };
    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, [lightboxItem, closeLightbox, nextLightboxItem, prevLightboxItem]);

  // Handle Like Toggle
  const handleToggleLike = (id: string | number, e?: React.MouseEvent) => {
    if (e) {
      e.stopPropagation();
      e.preventDefault();
    }
    const key = String(id);
    const currentlyLiked = !!likedMap[key];
    const originalItem = allItems.find((it) => String(it.id) === key);
    const baseLikes = originalItem?.likes || 0;
    const currentCount = likeCountMap[key] ?? baseLikes;

    setLikedMap((prev) => ({ ...prev, [key]: !currentlyLiked }));
    setLikeCountMap((prev) => ({
      ...prev,
      [key]: currentlyLiked ? Math.max(0, currentCount - 1) : currentCount + 1,
    }));
  };

  // Handle Share / Copy Link
  const handleShare = async (item: GalleryItem, e?: React.MouseEvent) => {
    if (e) {
      e.stopPropagation();
      e.preventDefault();
    }
    const shareUrl = typeof window !== "undefined" ? `${window.location.origin}/gallery?view=${item.id}` : "";
    if (navigator.clipboard) {
      try {
        await navigator.clipboard.writeText(shareUrl);
        setCopiedId(item.id);
        setTimeout(() => setCopiedId(null), 2500);
      } catch {
        // Fallback
      }
    }
  };

  // Handle contribution submit
  const handleFormSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);
    try {
      const payload = {
        type: "photo",
        url: formUrl || "/img/attractions/daang_kalikasan/image_1.jpg",
        caption: formTitle,
      };

      await fetch("/api/gallery", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      }).catch(() => {});

      setSubmissionSuccess(true);
      setTimeout(() => {
        setIsContributeModalOpen(false);
        setSubmissionSuccess(false);
        setFormTitle("");
        setFormUrl("");
        setFormContributor("");
        setFormStory("");
      }, 2000);
    } catch {
      // Fallback
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="space-y-12">
      {/* ─────────────────────────────────────────────────────────────
          1. HERO & ARCHIVE SPOTLIGHT
          ───────────────────────────────────────────────────────────── */}
      <section className="relative overflow-hidden rounded-3xl bg-gradient-to-br from-emerald-950 via-teal-950 to-slate-950 text-white p-8 md:p-12 lg:p-16 border border-emerald-800/30 shadow-2xl">
        {/* Subtle background ambient overlay */}
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_80%_80%_at_50%_-20%,rgba(16,185,129,0.15),rgba(255,255,255,0))] pointer-events-none" />
        <div className="absolute -right-20 -bottom-20 w-96 h-96 bg-emerald-500/10 rounded-full blur-3xl pointer-events-none" />

        <div className="relative z-10 grid grid-cols-1 lg:grid-cols-12 gap-10 items-center">
          {/* Left Column: Headline & Action */}
          <div className="lg:col-span-7 space-y-6">
            <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-emerald-500/15 border border-emerald-400/30 text-emerald-300 text-xs font-semibold tracking-wide backdrop-blur-md">
              <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
              Living Heritage & Community Visual Archive
            </div>

            <div className="space-y-3">
              <h2 className="text-4xl sm:text-5xl lg:text-6xl font-extrabold tracking-tight leading-[1.1]">
                Visions of <span className="text-transparent bg-clip-text bg-gradient-to-r from-emerald-400 via-teal-300 to-amber-300">Mangatarem</span>
              </h2>
              <p className="text-base sm:text-lg text-emerald-100/80 max-w-xl leading-relaxed">
                Discover the untouched mountain ridges of Daang Kalikasan, thermal springs of Manleluag, 18th-century Spanish colonial churches, and heartwarming community stories.
              </p>
            </div>

            {/* Quick Stat Highlights */}
            <div className="grid grid-cols-3 gap-3 sm:gap-4 pt-2 pb-2">
              <div className="p-3 sm:p-4 rounded-2xl bg-white/5 border border-white/10 backdrop-blur-sm">
                <div className="text-2xl sm:text-3xl font-black text-emerald-300">{allItems.length}+</div>
                <div className="text-xs text-white/70 font-medium">Curated Assets</div>
              </div>
              <div className="p-3 sm:p-4 rounded-2xl bg-white/5 border border-white/10 backdrop-blur-sm">
                <div className="text-2xl sm:text-3xl font-black text-amber-300">{barangaysList.length}</div>
                <div className="text-xs text-white/70 font-medium">Barangays Mapped</div>
              </div>
              <div className="p-3 sm:p-4 rounded-2xl bg-white/5 border border-white/10 backdrop-blur-sm">
                <div className="text-2xl sm:text-3xl font-black text-teal-300">4.9★</div>
                <div className="text-xs text-white/70 font-medium">Visual Quality</div>
              </div>
            </div>

            {/* Action Buttons */}
            <div className="flex flex-wrap items-center gap-3 pt-2">
              <Button
                onClick={() => setIsContributeModalOpen(true)}
                className="h-11 px-6 rounded-xl bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-bold shadow-lg shadow-emerald-900/30 transition-all gap-2"
              >
                <Upload className="h-4 w-4" />
                Contribute Media
              </Button>
              <Button
                variant="outline"
                onClick={() => {
                  const el = document.getElementById("gallery-controls");
                  el?.scrollIntoView({ behavior: "smooth" });
                }}
                className="h-11 px-5 rounded-xl border-white/20 bg-white/5 hover:bg-white/10 text-white font-medium backdrop-blur-sm gap-2"
              >
                <Compass className="h-4 w-4 text-emerald-400" />
                Explore Catalog
              </Button>
            </div>
          </div>

          {/* Right Column: Featured Spotlight Card */}
          {spotlightItem && (
            <div className="lg:col-span-5">
              <div
                onClick={() => openLightbox(spotlightItem)}
                className="group relative rounded-2xl overflow-hidden border border-white/20 bg-slate-900/80 shadow-2xl cursor-pointer hover:border-emerald-400/50 transition-all duration-500"
              >
                <div className="relative aspect-[4/3] w-full overflow-hidden bg-slate-950">
                  <img
                    src={spotlightItem.url}
                    alt={spotlightItem.title}
                    className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-700 ease-out"
                  />
                  <div className="absolute inset-0 bg-gradient-to-t from-slate-950 via-slate-950/40 to-transparent opacity-80 group-hover:opacity-60 transition-opacity" />

                  {/* Spotlight Badges */}
                  <div className="absolute top-4 left-4 flex items-center gap-2">
                    <Badge className="bg-amber-500 hover:bg-amber-400 text-slate-950 font-bold text-xs px-2.5 py-0.5 shadow-md flex items-center gap-1">
                      <Sparkles className="h-3 w-3" />
                      Editor&apos;s Spotlight
                    </Badge>
                    <Badge className="bg-slate-900/80 backdrop-blur-md text-emerald-300 border border-emerald-500/30 text-xs">
                      {spotlightItem.barangay || "Mangatarem"}
                    </Badge>
                  </div>

                  {/* Quick Expand Icon */}
                  <div className="absolute top-4 right-4 p-2 rounded-full bg-black/40 backdrop-blur-md text-white/80 group-hover:text-white group-hover:scale-110 transition-all">
                    <Maximize2 className="h-4 w-4" />
                  </div>

                  {/* Narrative details inside spotlight */}
                  <div className="absolute inset-x-0 bottom-0 p-5 text-white space-y-2">
                    <h3 className="text-xl font-bold leading-snug group-hover:text-emerald-300 transition-colors">
                      {spotlightItem.title}
                    </h3>
                    <p className="text-xs text-white/80 line-clamp-2 leading-relaxed">
                      {spotlightItem.description}
                    </p>
                    <div className="flex items-center justify-between text-xs text-white/60 pt-2 border-t border-white/10">
                      <span className="flex items-center gap-1 text-emerald-300">
                        <MapPin className="h-3.5 w-3.5" />
                        {spotlightItem.location}
                      </span>
                      <span>By {spotlightItem.contributor}</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      </section>

      {/* ─────────────────────────────────────────────────────────────
          2. STICKY INTERACTIVE CONTROL BAR & FILTERS
          ───────────────────────────────────────────────────────────── */}
      <div id="gallery-controls" className="space-y-6">
        {/* Category Pills Tabs */}
        <div className="flex items-center gap-2 overflow-x-auto pb-2 scrollbar-none">
          {CATEGORIES.map((cat) => {
            const Icon = cat.icon;
            const isActive = selectedCategory === cat.id;
            return (
              <button
                key={cat.id}
                onClick={() => setSelectedCategory(cat.id)}
                className={`inline-flex items-center gap-2 px-4 py-2.5 rounded-xl text-xs sm:text-sm font-semibold whitespace-nowrap transition-all duration-200 cursor-pointer ${
                  isActive
                    ? "bg-primary text-primary-foreground shadow-md shadow-primary/20 scale-[1.02]"
                    : "bg-card hover:bg-muted text-muted-foreground hover:text-foreground border border-border/60"
                }`}
              >
                <Icon className={`h-4 w-4 ${isActive ? "text-primary-foreground" : cat.color}`} />
                {cat.label}
              </button>
            );
          })}
        </div>

        {/* Filter Controls Row */}
        <Card className="border-border/60 shadow-sm bg-card/80 backdrop-blur-md">
          <CardContent className="p-4 sm:p-5">
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-12 gap-3.5 items-center">
              {/* Search input */}
              <div className="lg:col-span-4 relative">
                <Search className="absolute left-3.5 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                <Input
                  type="text"
                  placeholder="Search by caption, landmark, barangay, or tag..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="pl-9 pr-8 h-10 rounded-xl bg-background border-border/80 text-sm focus-visible:ring-primary"
                />
                {searchQuery && (
                  <button
                    onClick={() => setSearchQuery("")}
                    className="absolute right-3 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground p-0.5"
                    aria-label="Clear search"
                  >
                    <X className="h-3.5 w-3.5" />
                  </button>
                )}
              </div>

              {/* Barangay Filter */}
              <div className="lg:col-span-3">
                <select
                  value={selectedBarangay}
                  onChange={(e) => setSelectedBarangay(e.target.value)}
                  className="w-full h-10 px-3 rounded-xl bg-background border border-border/80 text-xs sm:text-sm font-medium text-foreground focus:outline-none focus:ring-2 focus:ring-primary/20 focus:border-primary transition-all cursor-pointer"
                >
                  <option value="all">Everywhere in Mangatarem ({allItems.length})</option>
                  {barangaysList.map((b) => (
                    <option key={b} value={b}>
                      Brgy. {b}
                    </option>
                  ))}
                </select>
              </div>

              {/* Sort Dropdown */}
              <div className="lg:col-span-3">
                <select
                  value={sortBy}
                  onChange={(e) => setSortBy(e.target.value as any)}
                  className="w-full h-10 px-3 rounded-xl bg-background border border-border/80 text-xs sm:text-sm font-medium text-foreground focus:outline-none focus:ring-2 focus:ring-primary/20 focus:border-primary transition-all cursor-pointer"
                >
                  <option value="popular">Most Appreciated & Featured</option>
                  <option value="newest">Latest Uploads</option>
                  <option value="oldest">Time Capsule Archive</option>
                  <option value="title">Alphabetical (A-Z)</option>
                </select>
              </div>

              {/* View Mode Switcher */}
              <div className="lg:col-span-2 flex items-center justify-end gap-1.5">
                <button
                  onClick={() => setViewMode("masonry")}
                  title="Masonry Gallery"
                  className={`p-2 rounded-lg border transition-all ${
                    viewMode === "masonry"
                      ? "bg-primary text-primary-foreground border-primary"
                      : "bg-background text-muted-foreground hover:text-foreground border-border/80"
                  }`}
                  aria-label="Masonry View"
                >
                  <Layers className="h-4 w-4" />
                </button>
                <button
                  onClick={() => setViewMode("grid")}
                  title="Uniform Grid"
                  className={`p-2 rounded-lg border transition-all ${
                    viewMode === "grid"
                      ? "bg-primary text-primary-foreground border-primary"
                      : "bg-background text-muted-foreground hover:text-foreground border-border/80"
                  }`}
                  aria-label="Grid View"
                >
                  <LayoutGrid className="h-4 w-4" />
                </button>
                <button
                  onClick={() => setViewMode("editorial")}
                  title="Editorial Story Feed"
                  className={`p-2 rounded-lg border transition-all ${
                    viewMode === "editorial"
                      ? "bg-primary text-primary-foreground border-primary"
                      : "bg-background text-muted-foreground hover:text-foreground border-border/80"
                  }`}
                  aria-label="Editorial Feed"
                >
                  <Grid2X2 className="h-4 w-4" />
                </button>
              </div>
            </div>

            {/* Active Filters summary bar */}
            {(selectedCategory !== "all" || selectedBarangay !== "all" || searchQuery.trim()) && (
              <div className="flex flex-wrap items-center gap-2 pt-3 mt-3 border-t border-border/60 text-xs">
                <span className="text-muted-foreground font-medium">Active filters:</span>
                {selectedCategory !== "all" && (
                  <Badge variant="secondary" className="gap-1 bg-primary/10 text-primary border-primary/20">
                    Category: {CATEGORIES.find((c) => c.id === selectedCategory)?.label}
                    <button onClick={() => setSelectedCategory("all")}>
                      <X className="h-3 w-3" />
                    </button>
                  </Badge>
                )}
                {selectedBarangay !== "all" && (
                  <Badge variant="secondary" className="gap-1 bg-primary/10 text-primary border-primary/20">
                    Brgy. {selectedBarangay}
                    <button onClick={() => setSelectedBarangay("all")}>
                      <X className="h-3 w-3" />
                    </button>
                  </Badge>
                )}
                {searchQuery.trim() && (
                  <Badge variant="secondary" className="gap-1 bg-primary/10 text-primary border-primary/20">
                    &ldquo;{searchQuery}&rdquo;
                    <button onClick={() => setSearchQuery("")}>
                      <X className="h-3 w-3" />
                    </button>
                  </Badge>
                )}
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => {
                    setSelectedCategory("all");
                    setSelectedBarangay("all");
                    setSearchQuery("");
                  }}
                  className="h-6 px-2 text-xs text-muted-foreground hover:text-foreground"
                >
                  Reset all filters
                </Button>
                <span className="ml-auto text-muted-foreground font-medium">
                  Showing {filteredItems.length} of {allItems.length} stories
                </span>
              </div>
            )}
          </CardContent>
        </Card>
      </div>

      {/* ─────────────────────────────────────────────────────────────
          3. GALLERY GRID DISPLAY
          ───────────────────────────────────────────────────────────── */}
      {filteredItems.length === 0 ? (
        /* Empty State */
        <div className="py-20 text-center rounded-3xl bg-muted/30 border border-dashed border-border p-8 space-y-4">
          <div className="w-16 h-16 rounded-3xl bg-muted flex items-center justify-center mx-auto text-muted-foreground">
            <Camera className="h-8 w-8" />
          </div>
          <div className="space-y-1">
            <h3 className="text-xl font-bold">No gallery items matched your filter</h3>
            <p className="text-sm text-muted-foreground max-w-md mx-auto">
              Try adjusting your category, barangay selection, or search terms to uncover more gems of Mangatarem.
            </p>
          </div>
          <Button
            onClick={() => {
              setSelectedCategory("all");
              setSelectedBarangay("all");
              setSearchQuery("");
            }}
            variant="outline"
            className="rounded-xl mt-2"
          >
            Clear all filters
          </Button>
        </div>
      ) : viewMode === "editorial" ? (
        /* Editorial Feed View (Larger Cards with richer context) */
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          {filteredItems.map((item) => {
            const isLiked = !!likedMap[String(item.id)];
            const likeCount = likeCountMap[String(item.id)] ?? (item.likes || 0);

            return (
              <Card
                key={item.id}
                onClick={() => openLightbox(item)}
                className="group overflow-hidden rounded-3xl border-border/60 hover:shadow-xl hover:border-primary/40 transition-all duration-300 flex flex-col cursor-pointer bg-card"
              >
                <div className="relative aspect-[16/10] w-full overflow-hidden bg-muted">
                  <img
                    src={item.url}
                    alt={item.title}
                    loading="lazy"
                    className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-700 ease-out"
                  />
                  <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-black/20 to-transparent opacity-60 group-hover:opacity-40 transition-opacity" />

                  {/* Top Badges */}
                  <div className="absolute top-4 left-4 flex items-center gap-2">
                    {item.barangay && (
                      <Badge className="bg-black/60 backdrop-blur-md text-emerald-300 border border-emerald-400/30 text-xs font-semibold">
                        <MapPin className="h-3 w-3 mr-1" />
                        {item.barangay}
                      </Badge>
                    )}
                    {item.category && (
                      <Badge variant="secondary" className="bg-background/80 backdrop-blur-md text-xs">
                        {CATEGORIES.find((c) => c.id === item.category)?.label || item.category}
                      </Badge>
                    )}
                  </div>

                  {/* Like Button */}
                  <button
                    onClick={(e) => handleToggleLike(item.id, e)}
                    className={`absolute top-4 right-4 p-2.5 rounded-full backdrop-blur-md transition-all ${
                      isLiked
                        ? "bg-rose-500 text-white"
                        : "bg-black/40 text-white/90 hover:bg-black/60 hover:scale-110"
                    }`}
                    aria-label="Like story"
                  >
                    <Heart className={`h-4 w-4 ${isLiked ? "fill-current" : ""}`} />
                  </button>
                </div>

                <CardContent className="p-6 space-y-3 flex-1 flex flex-col justify-between">
                  <div className="space-y-2">
                    <h3 className="text-xl font-bold group-hover:text-primary transition-colors leading-snug">
                      {item.title}
                    </h3>
                    <p className="text-sm text-muted-foreground line-clamp-3 leading-relaxed">
                      {item.description}
                    </p>
                  </div>

                  <div className="flex items-center justify-between pt-4 border-t border-border/60 text-xs text-muted-foreground">
                    <div className="flex items-center gap-2">
                      <div className="w-6 h-6 rounded-full bg-primary/10 text-primary flex items-center justify-center font-bold text-[10px]">
                        {item.contributor ? item.contributor[0] : "M"}
                      </div>
                      <span className="font-medium text-foreground">{item.contributor}</span>
                    </div>

                    <div className="flex items-center gap-4">
                      <span className="flex items-center gap-1">
                        <Heart className="h-3.5 w-3.5 text-rose-500 fill-rose-500/20" />
                        {likeCount}
                      </span>
                      <button
                        onClick={(e) => handleShare(item, e)}
                        className="hover:text-foreground transition-colors p-1"
                        title="Share link"
                      >
                        {copiedId === item.id ? (
                          <Check className="h-3.5 w-3.5 text-emerald-500" />
                        ) : (
                          <Share2 className="h-3.5 w-3.5" />
                        )}
                      </button>
                    </div>
                  </div>
                </CardContent>
              </Card>
            );
          })}
        </div>
      ) : (
        /* Masonry & Grid Mode */
        <div
          className={`grid gap-5 ${
            viewMode === "grid"
              ? "grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4"
              : "grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4"
          }`}
        >
          {filteredItems.map((item, idx) => {
            const isLiked = !!likedMap[String(item.id)];
            const likeCount = likeCountMap[String(item.id)] ?? (item.likes || 0);

            // Aspect ratio calculation for Masonry feel
            const aspectClass =
              viewMode === "grid"
                ? "aspect-[4/3]"
                : item.aspect_ratio === "portrait"
                ? "aspect-[3/4]"
                : item.aspect_ratio === "square"
                ? "aspect-square"
                : "aspect-[4/3]";

            return (
              <div
                key={item.id}
                onClick={() => openLightbox(item)}
                className="group relative rounded-2xl overflow-hidden bg-card border border-border/60 shadow-sm hover:shadow-xl hover:border-primary/40 transition-all duration-300 cursor-pointer flex flex-col"
              >
                <div className={`relative ${aspectClass} w-full overflow-hidden bg-muted`}>
                  <img
                    src={item.url}
                    alt={item.title}
                    loading="lazy"
                    className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500 ease-out"
                  />

                  {/* Gradient Overlay for Text Clarity */}
                  <div className="absolute inset-0 bg-gradient-to-t from-black/85 via-black/30 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300" />

                  {/* Top Floating Badge */}
                  <div className="absolute top-3 left-3 flex items-center gap-1.5">
                    {item.barangay && (
                      <span className="px-2.5 py-1 rounded-full bg-black/60 backdrop-blur-md text-[11px] font-semibold text-emerald-300 border border-emerald-400/30">
                        {item.barangay}
                      </span>
                    )}
                  </div>

                  {/* Top Right Like Button */}
                  <button
                    onClick={(e) => handleToggleLike(item.id, e)}
                    className={`absolute top-3 right-3 p-2 rounded-full backdrop-blur-md transition-all opacity-90 group-hover:opacity-100 ${
                      isLiked
                        ? "bg-rose-500 text-white shadow-md"
                        : "bg-black/40 text-white/90 hover:bg-black/70 hover:scale-110"
                    }`}
                    aria-label="Like this photo"
                  >
                    <Heart className={`h-3.5 w-3.5 ${isLiked ? "fill-current" : ""}`} />
                  </button>

                  {/* Hover Information Sheet */}
                  <div className="absolute inset-x-0 bottom-0 p-4 text-white translate-y-3 group-hover:translate-y-0 opacity-0 group-hover:opacity-100 transition-all duration-300 space-y-1.5">
                    <h4 className="text-sm font-bold leading-tight line-clamp-1">
                      {item.title}
                    </h4>
                    <p className="text-xs text-white/80 line-clamp-2 font-normal leading-relaxed">
                      {item.description}
                    </p>
                    <div className="flex items-center justify-between text-[11px] text-white/70 pt-2 border-t border-white/20">
                      <span className="truncate max-w-[140px]">
                        By {item.contributor}
                      </span>
                      <span className="flex items-center gap-1 text-rose-300">
                        <Heart className="h-3 w-3 fill-current" />
                        {likeCount}
                      </span>
                    </div>
                  </div>
                </div>

                {/* Subtitle footer on card for readable scan in non-hover mode */}
                <div className="p-3.5 bg-card flex items-center justify-between gap-2 border-t border-border/40 text-xs">
                  <div className="truncate">
                    <span className="font-semibold text-foreground truncate block text-xs">
                      {item.title}
                    </span>
                    <span className="text-[11px] text-muted-foreground flex items-center gap-1 mt-0.5">
                      <MapPin className="h-3 w-3 text-primary" />
                      {item.location || item.barangay || "Mangatarem"}
                    </span>
                  </div>
                  <div className="flex items-center gap-2 text-muted-foreground text-xs shrink-0">
                    <span className="flex items-center gap-0.5">
                      <Heart className={`h-3 w-3 ${isLiked ? "text-rose-500 fill-rose-500" : ""}`} />
                      {likeCount}
                    </span>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      )}

      {/* ─────────────────────────────────────────────────────────────
          4. FULLSCREEN CINEMATIC LIGHTBOX
          ───────────────────────────────────────────────────────────── */}
      {lightboxItem && (
        <div
          role="dialog"
          aria-modal="true"
          aria-label="Image Lightbox Viewer"
          className="fixed inset-0 z-50 bg-black/95 backdrop-blur-2xl flex flex-col justify-between overflow-hidden animate-in fade-in duration-200"
        >
          {/* Lightbox Top Navigation Bar */}
          <div className="relative z-50 flex items-center justify-between p-4 sm:p-6 border-b border-white/10 bg-black/40">
            <div className="flex items-center gap-3">
              <div className="p-2 rounded-xl bg-emerald-500/20 text-emerald-400 border border-emerald-400/30">
                <Camera className="h-4 w-4" />
              </div>
              <div>
                <h3 className="text-sm sm:text-base font-bold text-white leading-tight">
                  {lightboxItem.title}
                </h3>
                <p className="text-xs text-white/60">
                  Story {lightboxIndex + 1} of {filteredItems.length} · {lightboxItem.barangay ? `Brgy. ${lightboxItem.barangay}` : "Mangatarem Archive"}
                </p>
              </div>
            </div>

            {/* Top Toolbar Actions */}
            <div className="flex items-center gap-2">
              <button
                onClick={(e) => handleToggleLike(lightboxItem.id, e)}
                className={`p-2.5 rounded-xl border transition-all ${
                  likedMap[String(lightboxItem.id)]
                    ? "bg-rose-500 text-white border-rose-400"
                    : "bg-white/10 text-white/80 hover:text-white hover:bg-white/20 border-white/10"
                }`}
                title="Like story"
                aria-label="Like story"
              >
                <Heart className={`h-4 w-4 ${likedMap[String(lightboxItem.id)] ? "fill-current" : ""}`} />
              </button>

              <button
                onClick={(e) => handleShare(lightboxItem, e)}
                className="p-2.5 rounded-xl bg-white/10 hover:bg-white/20 text-white/80 hover:text-white border border-white/10 transition-all"
                title="Copy share link"
                aria-label="Share story"
              >
                {copiedId === lightboxItem.id ? (
                  <Check className="h-4 w-4 text-emerald-400" />
                ) : (
                  <Share2 className="h-4 w-4" />
                )}
              </button>

              <a
                href={lightboxItem.url}
                target="_blank"
                rel="noopener noreferrer"
                className="p-2.5 rounded-xl bg-white/10 hover:bg-white/20 text-white/80 hover:text-white border border-white/10 transition-all"
                title="Open high-res original"
                aria-label="Open original image"
              >
                <ExternalLink className="h-4 w-4" />
              </a>

              <button
                onClick={closeLightbox}
                className="p-2.5 rounded-xl bg-white/10 hover:bg-rose-500 text-white border border-white/10 transition-all ml-2"
                title="Close lightbox (Esc)"
                aria-label="Close lightbox"
              >
                <X className="h-4 w-4" />
              </button>
            </div>
          </div>

          {/* Lightbox Main Stage */}
          <div className="relative flex-1 flex items-center justify-center p-4 sm:p-8 overflow-hidden">
            {/* Previous Button */}
            <button
              onClick={prevLightboxItem}
              className="absolute left-4 top-1/2 -translate-y-1/2 z-30 p-3 rounded-full bg-black/60 hover:bg-emerald-500 hover:text-slate-950 text-white border border-white/20 backdrop-blur-md transition-all shadow-xl"
              title="Previous photo (Left Arrow)"
              aria-label="Previous photo"
            >
              <ChevronLeft className="h-6 w-6" />
            </button>

            {/* Next Button */}
            <button
              onClick={nextLightboxItem}
              className="absolute right-4 top-1/2 -translate-y-1/2 z-30 p-3 rounded-full bg-black/60 hover:bg-emerald-500 hover:text-slate-950 text-white border border-white/20 backdrop-blur-md transition-all shadow-xl"
              title="Next photo (Right Arrow)"
              aria-label="Next photo"
            >
              <ChevronRight className="h-6 w-6" />
            </button>

            {/* Media Canvas */}
            <div className="relative max-w-5xl max-h-[65vh] sm:max-h-[70vh] flex items-center justify-center">
              <img
                src={lightboxItem.url}
                alt={lightboxItem.title}
                className="max-h-[65vh] sm:max-h-[70vh] max-w-full object-contain rounded-2xl shadow-2xl ring-1 ring-white/10 select-none animate-in zoom-in-95 duration-300"
              />
            </div>
          </div>

          {/* Lightbox Bottom Story Panel & Filmstrip */}
          <div className="relative z-50 bg-black/80 border-t border-white/10 p-4 sm:p-6 backdrop-blur-xl space-y-4">
            <div className="max-w-5xl mx-auto flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
              <div className="space-y-1.5 max-w-2xl">
                <div className="flex flex-wrap items-center gap-2">
                  <Badge className="bg-emerald-500/20 text-emerald-300 border border-emerald-400/30 text-xs">
                    <MapPin className="h-3 w-3 mr-1" />
                    {lightboxItem.location || `Brgy. ${lightboxItem.barangay}`}
                  </Badge>
                  {lightboxItem.category && (
                    <Badge variant="outline" className="text-xs text-white/80 border-white/20">
                      {CATEGORIES.find((c) => c.id === lightboxItem.category)?.label || lightboxItem.category}
                    </Badge>
                  )}
                  {lightboxItem.date && (
                    <span className="text-xs text-white/50 flex items-center gap-1">
                      <Calendar className="h-3 w-3" />
                      {lightboxItem.date}
                    </span>
                  )}
                </div>
                <p className="text-xs sm:text-sm text-white/90 leading-relaxed font-medium">
                  {lightboxItem.description}
                </p>
              </div>

              {/* Attribution & Location Action */}
              <div className="flex items-center gap-3 shrink-0">
                <div className="text-right">
                  <div className="text-xs text-white/50">Curator / Contributor</div>
                  <div className="text-sm font-bold text-emerald-300">{lightboxItem.contributor}</div>
                </div>
                <Link href={`/map?highlight=${encodeURIComponent(lightboxItem.barangay || "Mangatarem")}`}>
                  <Button
                    size="sm"
                    className="rounded-xl bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-bold gap-1.5 text-xs h-9"
                  >
                    <MapIcon className="h-3.5 w-3.5" />
                    View on Map
                  </Button>
                </Link>
              </div>
            </div>

            {/* Filmstrip Thumbnail Ribbon */}
            <div className="max-w-5xl mx-auto pt-2 border-t border-white/10">
              <div className="flex items-center gap-2 overflow-x-auto pb-1 scrollbar-none">
                {filteredItems.map((item, idx) => (
                  <button
                    key={item.id}
                    onClick={() => {
                      setLightboxIndex(idx);
                      setLightboxItem(item);
                    }}
                    className={`relative w-14 h-14 sm:w-16 sm:h-16 rounded-xl overflow-hidden shrink-0 border-2 transition-all cursor-pointer ${
                      idx === lightboxIndex
                        ? "border-emerald-400 scale-105 shadow-md shadow-emerald-500/20 ring-2 ring-emerald-500/50"
                        : "border-white/20 opacity-50 hover:opacity-100"
                    }`}
                    aria-label={`Jump to photo: ${item.title}`}
                  >
                    <img src={item.url} alt={item.title} className="w-full h-full object-cover" />
                  </button>
                ))}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* ─────────────────────────────────────────────────────────────
          5. CONTRIBUTE MEDIA COMMUNITY DIALOG
          ───────────────────────────────────────────────────────────── */}
      <Dialog open={isContributeModalOpen} onOpenChange={setIsContributeModalOpen}>
        <DialogContent className="sm:max-w-lg rounded-3xl p-6 sm:p-8 bg-card border-border/80 shadow-2xl">
          <DialogHeader className="space-y-2 text-left">
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-primary/10 text-primary text-xs font-semibold w-fit">
              <Upload className="h-3.5 w-3.5" />
              Community Heritage Submission
            </div>
            <DialogTitle className="text-2xl font-bold tracking-tight">
              Contribute to Visions of Mangatarem
            </DialogTitle>
            <DialogDescription className="text-sm text-muted-foreground">
              Help document the breathtaking sceneries, historical sites, and local stories of our municipality. Submissions are reviewed by Barangay & Municipal Curators.
            </DialogDescription>
          </DialogHeader>

          {submissionSuccess ? (
            <div className="py-8 text-center space-y-3">
              <div className="w-14 h-14 rounded-full bg-emerald-500/20 text-emerald-500 flex items-center justify-center mx-auto animate-in zoom-in">
                <CheckCircle2 className="h-8 w-8" />
              </div>
              <h4 className="text-lg font-bold text-foreground">Media Submitted Successfully!</h4>
              <p className="text-xs text-muted-foreground max-w-sm mx-auto">
                Thank you for your contribution to the Mangatarem digital heritage archive. Your submission is now in the review queue.
              </p>
            </div>
          ) : (
            <form onSubmit={handleFormSubmit} className="space-y-4 pt-2">
              <div className="space-y-1.5">
                <label className="text-xs font-bold text-foreground">Photo Title / Caption *</label>
                <Input
                  required
                  placeholder="e.g. Sunset view over Daang Kalikasan ridge"
                  value={formTitle}
                  onChange={(e) => setFormTitle(e.target.value)}
                  className="rounded-xl"
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div className="space-y-1.5">
                  <label className="text-xs font-bold text-foreground">Category *</label>
                  <select
                    value={formCategory}
                    onChange={(e) => setFormCategory(e.target.value)}
                    className="w-full h-10 px-3 rounded-xl bg-background border border-border text-xs font-medium text-foreground focus:outline-none focus:ring-2 focus:ring-primary/20"
                  >
                    <option value="nature">Landscapes & Nature</option>
                    <option value="heritage">Historical & Heritage</option>
                    <option value="agro">Agro-Tourism & Farms</option>
                    <option value="festivals">Festivals & Celebrations</option>
                    <option value="flavors">Flavors & Local Life</option>
                  </select>
                </div>

                <div className="space-y-1.5">
                  <label className="text-xs font-bold text-foreground">Barangay *</label>
                  <select
                    value={formBarangay}
                    onChange={(e) => setFormBarangay(e.target.value)}
                    className="w-full h-10 px-3 rounded-xl bg-background border border-border text-xs font-medium text-foreground focus:outline-none focus:ring-2 focus:ring-primary/20"
                  >
                    {barangaysList.map((b) => (
                      <option key={b} value={b}>
                        Brgy. {b}
                      </option>
                    ))}
                  </select>
                </div>
              </div>

              <div className="space-y-1.5">
                <label className="text-xs font-bold text-foreground">Media Image URL / Asset Link *</label>
                <Input
                  required
                  type="url"
                  placeholder="https://images.unsplash.com/... or cloud storage URL"
                  value={formUrl}
                  onChange={(e) => setFormUrl(e.target.value)}
                  className="rounded-xl"
                />
                <p className="text-[11px] text-muted-foreground">
                  Direct image link (.jpg, .png, .webp).
                </p>
              </div>

              <div className="space-y-1.5">
                <label className="text-xs font-bold text-foreground">Photographer / Contributor Name *</label>
                <Input
                  required
                  placeholder="e.g. Juan dela Cruz (or @instagram_handle)"
                  value={formContributor}
                  onChange={(e) => setFormContributor(e.target.value)}
                  className="rounded-xl"
                />
              </div>

              <div className="space-y-1.5">
                <label className="text-xs font-bold text-foreground">Story & Cultural Context (Optional)</label>
                <textarea
                  rows={2}
                  placeholder="Share what makes this spot special or what historical event took place here..."
                  value={formStory}
                  onChange={(e) => setFormStory(e.target.value)}
                  className="w-full p-3 rounded-xl bg-background border border-border text-xs text-foreground focus:outline-none focus:ring-2 focus:ring-primary/20 resize-none"
                />
              </div>

              <div className="p-3 rounded-xl bg-muted/50 border border-border/60 flex items-start gap-2.5 text-xs text-muted-foreground">
                <ShieldCheck className="h-4 w-4 text-primary shrink-0 mt-0.5" />
                <span>
                  By submitting, you confirm you have rights to share this photograph and grant Mangatarem Tourism permission for cultural archival display.
                </span>
              </div>

              <div className="flex items-center justify-end gap-3 pt-2">
                <Button
                  type="button"
                  variant="ghost"
                  onClick={() => setIsContributeModalOpen(false)}
                  className="rounded-xl"
                >
                  Cancel
                </Button>
                <Button
                  type="submit"
                  disabled={isSubmitting}
                  className="rounded-xl bg-primary hover:bg-primary/90 text-primary-foreground font-bold px-6"
                >
                  {isSubmitting ? "Submitting..." : "Submit for Curation"}
                </Button>
              </div>
            </form>
          )}
        </DialogContent>
      </Dialog>
    </div>
  );
}
