"use client";

import { useState, useMemo } from "react";
import Link from "next/link";
import {
  Building2,
  Hotel,
  Utensils,
  Coffee,
  Sprout,
  Store,
  MapPin,
  Phone,
  Mail,
  Globe,
  Clock,
  Star,
  Sparkles,
  ArrowLeft,
  ArrowRight,
  Share2,
  Check,
  CheckCircle2,
  Wifi,
  Car,
  Wind,
  Tv,
  Waves,
  Bath,
  Bed,
  Users,
  MessageSquare,
  ShieldCheck,
  ExternalLink,
  Navigation,
  Send,
  Loader2,
  Heart,
} from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Textarea } from "@/components/ui/textarea";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { useAuth } from "@/lib/auth";
import { fetchAPI } from "@/lib/api";
import { EstablishmentItem } from "../business-view";

export interface RoomItem {
  id: number;
  name: string;
  description?: string | null;
  price_per_night?: number | null;
  capacity?: number | null;
  amenities?: string[] | null;
  image_urls?: string[] | null;
  is_available?: boolean;
}

export interface MenuItem {
  id: number;
  name: string;
  description?: string | null;
  price?: number | null;
  category?: string | null;
  image_url?: string | null;
  is_bestseller?: boolean;
  is_available?: boolean;
}

export interface ReviewReplyItem {
  id: number;
  user_id: number;
  username: string;
  comment: string;
  created_at?: string | null;
}

export interface BusinessReviewItem {
  id: number;
  user_id: number;
  username?: string;
  rating?: number | null;
  comment?: string | null;
  parent_id?: number | null;
  status?: string;
  created_at?: string | null;
  replies?: ReviewReplyItem[];
}

export interface BusinessDetailData {
  establishment: EstablishmentItem;
  rooms: RoomItem[];
  menu_items: MenuItem[];
  reviews: BusinessReviewItem[];
}

interface BusinessDetailViewProps {
  data: BusinessDetailData;
  relatedBusinesses?: EstablishmentItem[];
}

// Category Configuration
const CATEGORY_CONFIG: Record<
  string,
  { label: string; icon: typeof Building2; color: string }
> = {
  all: { label: "All Businesses", icon: Store, color: "text-primary" },
  inn: { label: "Inns & Lodging", icon: Hotel, color: "text-emerald-600 dark:text-emerald-400" },
  restaurant: { label: "Restaurants & Dining", icon: Utensils, color: "text-amber-600 dark:text-amber-400" },
  cafe: { label: "Cafes & Bakeries", icon: Coffee, color: "text-orange-600 dark:text-orange-400" },
  farm: { label: "Agro-Tourism & Farms", icon: Sprout, color: "text-lime-600 dark:text-lime-400" },
  fastfood: { label: "Fast Food & Bites", icon: Utensils, color: "text-rose-600 dark:text-rose-400" },
  shop: { label: "Shops & Souvenirs", icon: Store, color: "text-blue-600 dark:text-blue-400" },
};

// Amenity Icons Dictionary
const AMENITY_MAP: Record<string, { label: string; icon: typeof Wifi; description: string }> = {
  wifi: { label: "Free High-Speed Wi-Fi", icon: Wifi, description: "Complimentary wireless internet" },
  parking: { label: "Dedicated Parking", icon: Car, description: "Secure on-site guest parking" },
  aircon: { label: "Air Conditioning", icon: Wind, description: "Climate-controlled rooms & spaces" },
  tv: { label: "Cable Television", icon: Tv, description: "Flat-screen TV with premium channels" },
  pool: { label: "Swimming Pool", icon: Waves, description: "Clean, maintained swimming facility" },
  bathroom: { label: "Private Bathroom", icon: Bath, description: "En-suite bathroom with toilet & shower" },
  hot_water: { label: "Hot & Cold Shower", icon: Waves, description: "Reliable hot water system" },
};

const DAY_KEYS = [
  { key: "mon", label: "Monday", short: "Mon" },
  { key: "tue", label: "Tuesday", short: "Tue" },
  { key: "wed", label: "Wednesday", short: "Wed" },
  { key: "thu", label: "Thursday", short: "Thu" },
  { key: "fri", label: "Friday", short: "Fri" },
  { key: "sat", label: "Saturday", short: "Sat" },
  { key: "sun", label: "Sunday", short: "Sun" },
];

export function BusinessDetailView({
  data,
  relatedBusinesses = [],
}: BusinessDetailViewProps) {
  const { establishment, rooms, menu_items, reviews: initialReviews } = data;
  const { user } = useAuth();

  const [reviews, setReviews] = useState<BusinessReviewItem[]>(initialReviews);
  const [copied, setCopied] = useState(false);
  const [isSaved, setIsSaved] = useState(false);
  const [selectedMenuCategory, setSelectedMenuCategory] = useState<string>("all");

  // Review Form State
  const [reviewRating, setReviewRating] = useState(5);
  const [reviewComment, setReviewComment] = useState("");
  const [submittingReview, setSubmittingReview] = useState(false);
  const [reviewSuccess, setReviewSuccess] = useState(false);
  const [reviewError, setReviewError] = useState("");

  // Booking Modal State
  const [selectedRoom, setSelectedRoom] = useState<RoomItem | null>(null);
  const [bookingName, setBookingName] = useState("");
  const [bookingPhone, setBookingPhone] = useState("");
  const [bookingDate, setBookingDate] = useState("");
  const [bookingGuests, setBookingGuests] = useState("1");
  const [bookingNotes, setBookingNotes] = useState("");
  const [bookingSent, setBookingSent] = useState(false);

  // Category Configuration
  const categoryConfig = CATEGORY_CONFIG[establishment.type] || {
    label: establishment.type.toUpperCase(),
    icon: Building2,
    color: "text-primary",
  };
  const CategoryIcon = categoryConfig.icon;

  // Operating status calculation (Open Now vs Closed)
  const openStatus = useMemo(() => {
    if (!establishment.operating_hours) {
      return { isOpen: true, text: "Open Today", badgeClass: "bg-emerald-500/10 text-emerald-600 dark:text-emerald-400" };
    }
    const days = ["sun", "mon", "tue", "wed", "thu", "fri", "sat"];
    const now = new Date();
    const currentDay = days[now.getDay()];
    const hours = establishment.operating_hours[currentDay];

    if (!hours || hours.toLowerCase() === "closed") {
      return { isOpen: false, text: "Closed Today", badgeClass: "bg-destructive/10 text-destructive" };
    }

    // Check if 24 hours
    if (hours === "00:00-23:59" || hours.includes("24")) {
      return { isOpen: true, text: "Open 24 Hours", badgeClass: "bg-emerald-500/10 text-emerald-600 dark:text-emerald-400" };
    }

    // Try parsing "HH:MM-HH:MM"
    const match = hours.match(/(\d{1,2}):(\d{2})\s*-\s*(\d{1,2}):(\d{2})/);
    if (match) {
      const openHour = parseInt(match[1], 10);
      const openMin = parseInt(match[2], 10);
      const closeHour = parseInt(match[3], 10);
      const closeMin = parseInt(match[4], 10);

      const curMinutes = now.getHours() * 60 + now.getMinutes();
      const openMinutes = openHour * 60 + openMin;
      const closeMinutes = closeHour * 60 + closeMin;

      if (curMinutes >= openMinutes && curMinutes <= closeMinutes) {
        return { isOpen: true, text: `Open Now until ${match[3]}:${match[4]}`, badgeClass: "bg-emerald-500/10 text-emerald-600 dark:text-emerald-400" };
      } else {
        return { isOpen: false, text: `Closed • Opens at ${match[1]}:${match[2]}`, badgeClass: "bg-amber-500/10 text-amber-600 dark:text-amber-400" };
      }
    }

    return { isOpen: true, text: `Open: ${hours}`, badgeClass: "bg-emerald-500/10 text-emerald-600 dark:text-emerald-400" };
  }, [establishment.operating_hours]);

  // Menu categories
  const menuCategories = useMemo(() => {
    const cats = new Set<string>();
    menu_items.forEach((m) => {
      if (m.category) cats.add(m.category);
    });
    return Array.from(cats);
  }, [menu_items]);

  const filteredMenuItems = useMemo(() => {
    if (selectedMenuCategory === "all") return menu_items;
    return menu_items.filter((m) => m.category === selectedMenuCategory);
  }, [menu_items, selectedMenuCategory]);

  const bestsellers = useMemo(() => {
    return menu_items.filter((m) => m.is_bestseller);
  }, [menu_items]);

  // Price Range Info
  const priceMeta = useMemo(() => {
    switch (establishment.price_range) {
      case "budget":
        return { label: "₱ Budget Friendly", desc: "Affordable local rates (Under ₱500/person)" };
      case "moderate":
        return { label: "₱₱ Moderate Range", desc: "Balanced pricing & great value (₱500 - ₱1,500)" };
      case "luxury":
        return { label: "₱₱₱ Premium / Luxury", desc: "High-end experience (₱1,500+)" };
      default:
        return { label: "₱ Accessible Pricing", desc: "Standard community rates" };
    }
  }, [establishment.price_range]);

  // Share handler
  const handleShare = async () => {
    const url = typeof window !== "undefined" ? window.location.href : "";
    if (navigator.share) {
      try {
        await navigator.share({
          title: `${establishment.name} | Mangatarem Tourism`,
          text: `Check out ${establishment.name} in Mangatarem, Pangasinan!`,
          url: url,
        });
        return;
      } catch {
        // Fallback to clipboard
      }
    }
    navigator.clipboard.writeText(url);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  // Review submission
  const handleSubmitReview = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!reviewComment.trim()) {
      setReviewError("Please write a few words about your experience.");
      return;
    }

    setSubmittingReview(true);
    setReviewError("");

    try {
      await fetchAPI(`/api/business/${establishment.id}/reviews`, {
        method: "POST",
        body: JSON.stringify({
          rating: reviewRating,
          comment: reviewComment,
        }),
      });

      // Add to local state
      const newRev: BusinessReviewItem = {
        id: Date.now(),
        user_id: user?.id || 0,
        username: user?.name || "You",
        rating: reviewRating,
        comment: reviewComment,
        created_at: new Date().toISOString(),
        status: "approved",
      };

      setReviews([newRev, ...reviews]);
      setReviewSuccess(true);
      setReviewComment("");
    } catch (err) {
      setReviewError(err instanceof Error ? err.message : "Failed to post review. Please try again.");
    } finally {
      setSubmittingReview(false);
    }
  };

  // Booking inquiry
  const handleSendBookingInquiry = (e: React.FormEvent) => {
    e.preventDefault();
    setBookingSent(true);
    setTimeout(() => {
      setBookingSent(false);
      setSelectedRoom(null);
    }, 3000);
  };

  const barangayDisplay = establishment.barangay_name || establishment.barangay;

  return (
    <div className="space-y-10">
      {/* ── Breadcrumb & Top Action Header ── */}
      <div className="flex flex-wrap items-center justify-between gap-4">
        <Link
          href="/business"
          className="inline-flex items-center gap-1.5 text-xs sm:text-sm font-medium text-muted-foreground hover:text-foreground transition-colors group"
        >
          <ArrowLeft className="h-4 w-4 group-hover:-translate-x-0.5 transition-transform" />
          <span>Back to Business Directory</span>
        </Link>

        <div className="flex items-center gap-2">
          <Button
            variant="outline"
            size="sm"
            onClick={() => setIsSaved(!isSaved)}
            className="text-xs gap-1.5 rounded-xl cursor-pointer"
            aria-label="Save establishment"
          >
            <Heart
              className={`h-3.5 w-3.5 ${
                isSaved ? "fill-rose-500 text-rose-500" : "text-muted-foreground"
              }`}
            />
            <span>{isSaved ? "Saved" : "Save"}</span>
          </Button>

          <Button
            variant="outline"
            size="sm"
            onClick={handleShare}
            className="text-xs gap-1.5 rounded-xl cursor-pointer"
            aria-label="Share establishment"
          >
            {copied ? (
              <>
                <Check className="h-3.5 w-3.5 text-primary" />
                <span>Copied Link</span>
              </>
            ) : (
              <>
                <Share2 className="h-3.5 w-3.5 text-muted-foreground" />
                <span>Share</span>
              </>
            )}
          </Button>
        </div>
      </div>

      {/* ── Showcase Media & Profile Header ── */}
      <section className="relative overflow-hidden rounded-3xl border border-border/70 bg-gradient-to-br from-card via-card/95 to-primary/5 shadow-xs">
        {/* Cover / Media Banner */}
        <div className="aspect-[21/9] sm:aspect-[24/9] w-full bg-muted relative overflow-hidden">
          {establishment.cover_image_url ? (
            <img
              src={establishment.cover_image_url}
              alt={establishment.name}
              className="w-full h-full object-cover"
            />
          ) : (
            <div className="w-full h-full flex flex-col items-center justify-center bg-gradient-to-br from-primary/15 via-primary/5 to-muted p-6 text-center">
              <CategoryIcon className="h-20 w-20 text-primary/30 mb-2" />
              <p className="text-xs font-bold text-primary/70 tracking-widest uppercase">
                Mangatarem Local Merchant & Hospitality
              </p>
            </div>
          )}

          {/* Floating Badges */}
          <div className="absolute top-4 left-4 flex flex-wrap gap-2">
            <Badge className="bg-background/90 text-foreground backdrop-blur-md border border-border/50 text-xs shadow-sm font-semibold">
              <CategoryIcon className="h-3.5 w-3.5 mr-1 text-primary" />
              {categoryConfig.label}
            </Badge>

            {establishment.is_featured && (
              <Badge className="bg-primary text-primary-foreground text-xs shadow-sm font-semibold">
                <Sparkles className="h-3 w-3 mr-1" /> Featured Listing
              </Badge>
            )}
          </div>

          <div className="absolute top-4 right-4 flex gap-2">
            <Badge
              variant="outline"
              className={`backdrop-blur-md text-xs font-semibold px-2.5 py-1 ${openStatus.badgeClass} border-border/50 bg-background/90 shadow-sm`}
            >
              <Clock className="h-3 w-3 mr-1 inline-block" />
              {openStatus.text}
            </Badge>
          </div>
        </div>

        {/* Profile Content Body */}
        <div className="p-6 md:p-8 space-y-6">
          <div className="flex flex-col lg:flex-row lg:items-start justify-between gap-6">
            <div className="space-y-3 max-w-3xl">
              <div className="flex items-center gap-2 text-xs font-semibold text-primary">
                <ShieldCheck className="h-4 w-4" />
                <span>Verified Mangatarem Merchant</span>
                {barangayDisplay && (
                  <span className="text-muted-foreground font-normal">
                    • Brgy. {barangayDisplay}
                  </span>
                )}
              </div>

              <h1 className="text-3xl sm:text-4xl font-extrabold tracking-tight text-foreground">
                {establishment.name}
              </h1>

              {/* Rating & Location meta */}
              <div className="flex flex-wrap items-center gap-4 text-sm">
                <div className="flex items-center gap-1 font-bold text-foreground">
                  <Star className="h-4 w-4 fill-amber-400 text-amber-400" />
                  <span>
                    {establishment.rating_avg && establishment.rating_avg > 0
                      ? establishment.rating_avg.toFixed(1)
                      : "New"}
                  </span>
                  <span className="text-xs text-muted-foreground font-normal ml-0.5">
                    ({establishment.review_count || reviews.length} customer reviews)
                  </span>
                </div>

                <div className="text-muted-foreground">•</div>

                <span className="text-xs sm:text-sm font-medium text-foreground/80 bg-muted px-2.5 py-0.5 rounded-lg border border-border/40">
                  {priceMeta.label}
                </span>

                {establishment.address && (
                  <>
                    <div className="text-muted-foreground hidden sm:inline">•</div>
                    <div className="flex items-center gap-1 text-xs sm:text-sm text-muted-foreground">
                      <MapPin className="h-4 w-4 text-primary shrink-0" />
                      <span>{establishment.address}</span>
                    </div>
                  </>
                )}
              </div>

              {establishment.description && (
                <p className="text-sm md:text-base text-muted-foreground leading-relaxed pt-2">
                  {establishment.description}
                </p>
              )}
            </div>

            {/* Quick Action Box */}
            <div className="lg:w-72 shrink-0 rounded-2xl border border-border/70 bg-card p-5 space-y-3.5 shadow-xs">
              <h3 className="text-xs font-bold uppercase tracking-wider text-muted-foreground">
                Contact & Inquiries
              </h3>

              <div className="space-y-2 text-xs">
                {establishment.contact_number && (
                  <a
                    href={`tel:${establishment.contact_number}`}
                    className="flex items-center gap-2.5 p-2 rounded-xl bg-muted/50 hover:bg-primary/10 text-foreground transition-colors font-medium"
                  >
                    <Phone className="h-4 w-4 text-primary shrink-0" />
                    <span className="truncate">{establishment.contact_number}</span>
                  </a>
                )}

                {establishment.email && (
                  <a
                    href={`mailto:${establishment.email}`}
                    className="flex items-center gap-2.5 p-2 rounded-xl bg-muted/50 hover:bg-primary/10 text-foreground transition-colors font-medium"
                  >
                    <Mail className="h-4 w-4 text-primary shrink-0" />
                    <span className="truncate">{establishment.email}</span>
                  </a>
                )}

                {establishment.website && (
                  <a
                    href={establishment.website}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="flex items-center gap-2.5 p-2 rounded-xl bg-muted/50 hover:bg-primary/10 text-foreground transition-colors font-medium"
                  >
                    <Globe className="h-4 w-4 text-primary shrink-0" />
                    <span className="truncate">Official Website</span>
                    <ExternalLink className="h-3 w-3 ml-auto text-muted-foreground" />
                  </a>
                )}

                {establishment.latitude && establishment.longitude && (
                  <a
                    href={`https://www.google.com/maps/search/?api=1&query=${establishment.latitude},${establishment.longitude}`}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="flex items-center gap-2.5 p-2 rounded-xl bg-muted/50 hover:bg-primary/10 text-foreground transition-colors font-medium"
                  >
                    <Navigation className="h-4 w-4 text-primary shrink-0" />
                    <span>Get Directions</span>
                    <ExternalLink className="h-3 w-3 ml-auto text-muted-foreground" />
                  </a>
                )}
              </div>

              {rooms.length > 0 ? (
                <a href="#rooms-section" className="block w-full">
                  <Button className="w-full text-xs font-semibold shadow-xs">
                    <Bed className="h-3.5 w-3.5 mr-1.5" />
                    View Available Rooms ({rooms.length})
                  </Button>
                </a>
              ) : menu_items.length > 0 ? (
                <a href="#menu-section" className="block w-full">
                  <Button className="w-full text-xs font-semibold shadow-xs">
                    <Utensils className="h-3.5 w-3.5 mr-1.5" />
                    View Menu Items ({menu_items.length})
                  </Button>
                </a>
              ) : null}
            </div>
          </div>
        </div>
      </section>

      {/* ── Main Detail Grid: Details, Hours & Amenities ── */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
        {/* Left Column: Amenities & Hours */}
        <div className="lg:col-span-8 space-y-8">
          {/* Amenities & Features */}
          {establishment.amenities && establishment.amenities.length > 0 && (
            <Card className="rounded-3xl border-border/70 p-6 md:p-8 space-y-5 bg-card">
              <div>
                <h2 className="text-xl font-bold tracking-tight text-foreground flex items-center gap-2">
                  <Sparkles className="h-5 w-5 text-primary" />
                  Amenities & Facilities
                </h2>
                <p className="text-xs text-muted-foreground mt-0.5">
                  Guest perks and features offered at {establishment.name}
                </p>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3.5">
                {establishment.amenities.map((item) => {
                  const info = AMENITY_MAP[item.toLowerCase()] || {
                    label: item.replace(/_/g, " ").toUpperCase(),
                    icon: CheckCircle2,
                    description: "Available guest amenity",
                  };
                  const Icon = info.icon;
                  return (
                    <div
                      key={item}
                      className="flex items-start gap-3 p-3.5 rounded-2xl bg-muted/40 border border-border/40"
                    >
                      <div className="p-2 rounded-xl bg-primary/10 text-primary shrink-0 mt-0.5">
                        <Icon className="h-4 w-4" />
                      </div>
                      <div>
                        <h4 className="text-xs font-bold text-foreground capitalize">
                          {info.label}
                        </h4>
                        <p className="text-[11px] text-muted-foreground leading-tight mt-0.5">
                          {info.description}
                        </p>
                      </div>
                    </div>
                  );
                })}
              </div>
            </Card>
          )}

          {/* ── Rooms & Accommodations Section ── */}
          {rooms && rooms.length > 0 && (
            <section id="rooms-section" className="space-y-4">
              <div className="flex items-center justify-between">
                <div>
                  <h2 className="text-2xl font-bold tracking-tight text-foreground flex items-center gap-2">
                    <Hotel className="h-6 w-6 text-primary" />
                    Accommodations & Rooms
                  </h2>
                  <p className="text-xs text-muted-foreground mt-0.5">
                    Clean, comfortable guest rooms in Mangatarem
                  </p>
                </div>
                <Badge variant="secondary" className="text-xs font-semibold">
                  {rooms.length} Room Type{rooms.length > 1 ? "s" : ""}
                </Badge>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-5">
                {rooms.map((room) => (
                  <Card
                    key={room.id}
                    className="overflow-hidden border-border/70 bg-card rounded-2xl flex flex-col justify-between hover:border-primary/40 hover:shadow-md transition-all duration-300"
                  >
                    <div className="p-5 space-y-3">
                      <div className="flex items-start justify-between gap-2">
                        <div>
                          <h3 className="font-bold text-base text-foreground leading-snug">
                            {room.name}
                          </h3>
                          {room.capacity && (
                            <span className="inline-flex items-center gap-1 text-xs text-muted-foreground mt-1">
                              <Users className="h-3.5 w-3.5 text-primary" />
                              <span>Up to {room.capacity} guest{room.capacity > 1 ? "s" : ""}</span>
                            </span>
                          )}
                        </div>
                        {room.price_per_night != null && (
                          <div className="text-right">
                            <span className="text-lg font-extrabold text-primary">
                              ₱{Number(room.price_per_night).toLocaleString()}
                            </span>
                            <span className="text-[10px] text-muted-foreground block leading-none">
                              per night
                            </span>
                          </div>
                        )}
                      </div>

                      {room.description && (
                        <p className="text-xs text-muted-foreground leading-relaxed line-clamp-3">
                          {room.description}
                        </p>
                      )}

                      {/* Room Amenities */}
                      {room.amenities && room.amenities.length > 0 && (
                        <div className="flex flex-wrap gap-1.5 pt-2 border-t border-border/30">
                          {room.amenities.map((a) => {
                            const info = AMENITY_MAP[a.toLowerCase()] || {
                              label: a,
                              icon: Check,
                            };
                            const Icon = info.icon;
                            return (
                              <span
                                key={a}
                                className="inline-flex items-center gap-1 text-[10px] font-medium bg-muted px-2 py-0.5 rounded-md text-foreground/70"
                              >
                                <Icon className="h-2.5 w-2.5 text-primary" />
                                {info.label}
                              </span>
                            );
                          })}
                        </div>
                      )}
                    </div>

                    <div className="p-4 pt-0">
                      <Dialog>
                        <DialogTrigger
                          render={
                            <Button
                              onClick={() => setSelectedRoom(room)}
                              className="w-full text-xs font-semibold rounded-xl shadow-xs"
                            >
                              Inquire / Book Room
                            </Button>
                          }
                        />
                        <DialogContent className="sm:max-w-md rounded-2xl">
                          <DialogHeader>
                            <DialogTitle className="text-lg font-bold">
                              Book {selectedRoom?.name || room.name}
                            </DialogTitle>
                            <DialogDescription className="text-xs">
                              Send your reservation inquiry directly to {establishment.name}.
                            </DialogDescription>
                          </DialogHeader>

                          {bookingSent ? (
                            <div className="py-6 text-center space-y-2">
                              <CheckCircle2 className="h-12 w-12 text-primary mx-auto" />
                              <h4 className="font-bold text-base">Inquiry Submitted!</h4>
                              <p className="text-xs text-muted-foreground">
                                The management will contact you at {bookingPhone || "your phone"} to
                                confirm availability.
                              </p>
                            </div>
                          ) : (
                            <form onSubmit={handleSendBookingInquiry} className="space-y-4 py-2">
                              <div className="space-y-1">
                                <Label htmlFor="b-name" className="text-xs font-medium">
                                  Full Name
                                </Label>
                                <Input
                                  id="b-name"
                                  placeholder="Juan Dela Cruz"
                                  value={bookingName}
                                  onChange={(e) => setBookingName(e.target.value)}
                                  required
                                  className="h-9 text-xs rounded-xl"
                                />
                              </div>

                              <div className="grid grid-cols-2 gap-3">
                                <div className="space-y-1">
                                  <Label htmlFor="b-phone" className="text-xs font-medium">
                                    Contact Phone
                                  </Label>
                                  <Input
                                    id="b-phone"
                                    placeholder="0917-000-0000"
                                    value={bookingPhone}
                                    onChange={(e) => setBookingPhone(e.target.value)}
                                    required
                                    className="h-9 text-xs rounded-xl"
                                  />
                                </div>
                                <div className="space-y-1">
                                  <Label htmlFor="b-date" className="text-xs font-medium">
                                    Target Check-In
                                  </Label>
                                  <Input
                                    id="b-date"
                                    type="date"
                                    value={bookingDate}
                                    onChange={(e) => setBookingDate(e.target.value)}
                                    required
                                    className="h-9 text-xs rounded-xl"
                                  />
                                </div>
                              </div>

                              <div className="space-y-1">
                                <Label htmlFor="b-guests" className="text-xs font-medium">
                                  Number of Guests
                                </Label>
                                <Input
                                  id="b-guests"
                                  type="number"
                                  min="1"
                                  max="10"
                                  value={bookingGuests}
                                  onChange={(e) => setBookingGuests(e.target.value)}
                                  className="h-9 text-xs rounded-xl"
                                />
                              </div>

                              <div className="space-y-1">
                                <Label htmlFor="b-notes" className="text-xs font-medium">
                                  Special Requests / Notes
                                </Label>
                                <Textarea
                                  id="b-notes"
                                  placeholder="Estimated arrival time, early check-in, extra pillows, etc."
                                  value={bookingNotes}
                                  onChange={(e) => setBookingNotes(e.target.value)}
                                  rows={2}
                                  className="text-xs rounded-xl"
                                />
                              </div>

                              <Button type="submit" className="w-full text-xs font-semibold mt-2">
                                Submit Reservation Inquiry
                              </Button>
                            </form>
                          )}
                        </DialogContent>
                      </Dialog>
                    </div>
                  </Card>
                ))}
              </div>
            </section>
          )}

          {/* ── Menu & Specialties Section ── */}
          {menu_items && menu_items.length > 0 && (
            <section id="menu-section" className="space-y-5">
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
                <div>
                  <h2 className="text-2xl font-bold tracking-tight text-foreground flex items-center gap-2">
                    <Utensils className="h-6 w-6 text-primary" />
                    Menu & House Specialties
                  </h2>
                  <p className="text-xs text-muted-foreground mt-0.5">
                    Authentic local flavors and dishes prepared fresh in Mangatarem
                  </p>
                </div>

                {/* Category Pills */}
                {menuCategories.length > 1 && (
                  <div className="flex items-center gap-1.5 overflow-x-auto pb-1">
                    <Button
                      variant={selectedMenuCategory === "all" ? "default" : "outline"}
                      size="sm"
                      onClick={() => setSelectedMenuCategory("all")}
                      className="rounded-full text-xs h-8 px-3"
                    >
                      All ({menu_items.length})
                    </Button>
                    {menuCategories.map((cat) => (
                      <Button
                        key={cat}
                        variant={selectedMenuCategory === cat ? "default" : "outline"}
                        size="sm"
                        onClick={() => setSelectedMenuCategory(cat)}
                        className="rounded-full text-xs h-8 px-3 capitalize"
                      >
                        {cat}
                      </Button>
                    ))}
                  </div>
                )}
              </div>

              {/* Bestseller Spotlight */}
              {bestsellers.length > 0 && selectedMenuCategory === "all" && (
                <div className="rounded-2xl border border-amber-500/30 bg-amber-500/5 p-4 space-y-3">
                  <div className="flex items-center gap-1.5 text-xs font-bold text-amber-600 dark:text-amber-400">
                    <Sparkles className="h-4 w-4" />
                    <span>Customer Favorites & Signature Dishes</span>
                  </div>

                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                    {bestsellers.map((item) => (
                      <div
                        key={item.id}
                        className="p-3.5 rounded-xl bg-card border border-border/60 flex items-start justify-between gap-3 shadow-xs"
                      >
                        <div className="space-y-1">
                          <div className="flex items-center gap-1.5">
                            <h4 className="font-bold text-sm text-foreground">{item.name}</h4>
                            <Badge className="bg-amber-500 text-white text-[9px] py-0 px-1.5">
                              Bestseller
                            </Badge>
                          </div>
                          {item.description && (
                            <p className="text-xs text-muted-foreground line-clamp-2">
                              {item.description}
                            </p>
                          )}
                        </div>
                        {item.price != null && (
                          <span className="font-extrabold text-primary text-sm whitespace-nowrap">
                            ₱{Number(item.price).toLocaleString()}
                          </span>
                        )}
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* General Menu Items Grid */}
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3.5">
                {filteredMenuItems.map((item) => (
                  <div
                    key={item.id}
                    className="p-4 rounded-2xl bg-card border border-border/70 hover:border-primary/40 transition-all flex items-start justify-between gap-4"
                  >
                    <div className="space-y-1">
                      <div className="flex items-center gap-2 flex-wrap">
                        <h4 className="font-semibold text-sm text-foreground">{item.name}</h4>
                        {item.category && (
                          <Badge variant="secondary" className="text-[10px] py-0 px-1.5 capitalize">
                            {item.category}
                          </Badge>
                        )}
                        {item.is_bestseller && (
                          <Badge className="bg-amber-500 text-white text-[9px] py-0 px-1">
                            ★ Popular
                          </Badge>
                        )}
                      </div>
                      {item.description && (
                        <p className="text-xs text-muted-foreground leading-relaxed line-clamp-2">
                          {item.description}
                        </p>
                      )}
                    </div>

                    {item.price != null && (
                      <span className="font-extrabold text-sm text-foreground whitespace-nowrap shrink-0">
                        ₱{Number(item.price).toLocaleString()}
                      </span>
                    )}
                  </div>
                ))}
              </div>
            </section>
          )}

          {/* ── Customer Reviews & Feedback Section ── */}
          <section className="space-y-6">
            <div className="flex items-center justify-between">
              <div>
                <h2 className="text-2xl font-bold tracking-tight text-foreground flex items-center gap-2">
                  <MessageSquare className="h-6 w-6 text-primary" />
                  Visitor Reviews
                </h2>
                <p className="text-xs text-muted-foreground mt-0.5">
                  Real experiences from travellers and local residents
                </p>
              </div>

              <div className="flex items-center gap-1 font-bold text-sm bg-muted/60 px-3 py-1.5 rounded-xl border border-border/40">
                <Star className="h-4 w-4 fill-amber-400 text-amber-400" />
                <span>
                  {establishment.rating_avg && establishment.rating_avg > 0
                    ? establishment.rating_avg.toFixed(1)
                    : "5.0"}
                </span>
                <span className="text-xs text-muted-foreground font-normal ml-0.5">
                  ({reviews.length})
                </span>
              </div>
            </div>

            {/* Review Submission Form Card */}
            <Card className="p-6 rounded-3xl border-border/70 bg-card/60 shadow-xs space-y-4">
              <h3 className="text-sm font-bold text-foreground">Write a Review</h3>

              {reviewSuccess ? (
                <div className="p-4 rounded-xl bg-emerald-500/10 border border-emerald-500/20 text-emerald-700 dark:text-emerald-300 text-xs flex items-center gap-2">
                  <CheckCircle2 className="h-4 w-4 shrink-0" />
                  <span>Thank you! Your review has been posted successfully.</span>
                </div>
              ) : user ? (
                <form onSubmit={handleSubmitReview} className="space-y-4">
                  {/* Rating Selector */}
                  <div className="space-y-1.5">
                    <Label className="text-xs font-semibold text-foreground">Your Rating</Label>
                    <div className="flex items-center gap-1.5">
                      {[1, 2, 3, 4, 5].map((star) => (
                        <button
                          key={star}
                          type="button"
                          onClick={() => setReviewRating(star)}
                          className="p-1 text-muted-foreground hover:scale-110 transition-transform focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary rounded-md cursor-pointer"
                          aria-label={`Rate ${star} star`}
                        >
                          <Star
                            className={`h-6 w-6 ${
                              star <= reviewRating
                                ? "fill-amber-400 text-amber-400"
                                : "text-muted-foreground/30"
                            }`}
                          />
                        </button>
                      ))}
                      <span className="text-xs font-semibold ml-2 text-foreground/80">
                        {reviewRating === 5
                          ? "Excellent! 5/5"
                          : reviewRating === 4
                          ? "Very Good 4/5"
                          : reviewRating === 3
                          ? "Average 3/5"
                          : `${reviewRating}/5`}
                      </span>
                    </div>
                  </div>

                  {/* Comment input */}
                  <div className="space-y-1.5">
                    <Label htmlFor="rev-comment" className="text-xs font-semibold text-foreground">
                      Share your experience
                    </Label>
                    <Textarea
                      id="rev-comment"
                      placeholder="How was the food, service, cleanliness, or room atmosphere? Tell fellow travellers what you enjoyed..."
                      value={reviewComment}
                      onChange={(e) => setReviewComment(e.target.value)}
                      rows={3}
                      className="text-xs rounded-xl bg-card border-border/70"
                      required
                    />
                  </div>

                  {reviewError && (
                    <p className="text-xs text-destructive font-medium">{reviewError}</p>
                  )}

                  <Button
                    type="submit"
                    disabled={submittingReview}
                    className="text-xs font-semibold gap-1.5 rounded-xl shadow-xs"
                  >
                    {submittingReview ? (
                      <>
                        <Loader2 className="h-3.5 w-3.5 animate-spin" />
                        Posting Review...
                      </>
                    ) : (
                      <>
                        <Send className="h-3.5 w-3.5" />
                        Submit Review
                      </>
                    )}
                  </Button>
                </form>
              ) : (
                <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 p-4 rounded-2xl bg-muted/40 border border-border/50">
                  <div className="space-y-0.5">
                    <p className="text-xs font-semibold text-foreground">
                      Visited {establishment.name}?
                    </p>
                    <p className="text-[11px] text-muted-foreground">
                      Log in with your tourist or resident account to leave a verified rating and review.
                    </p>
                  </div>
                  <Link href={`/auth/login?redirect=/business/${establishment.id}`}>
                    <Button size="sm" variant="outline" className="text-xs shrink-0 rounded-xl">
                      Log In to Review
                    </Button>
                  </Link>
                </div>
              )}
            </Card>

            {/* Reviews List */}
            {reviews.length === 0 ? (
              <div className="text-center py-12 px-4 border border-dashed rounded-3xl border-border/80 bg-card/30">
                <MessageSquare className="h-10 w-10 mx-auto mb-2 text-muted-foreground/30" />
                <h4 className="text-sm font-semibold text-foreground">No reviews yet</h4>
                <p className="text-xs text-muted-foreground mt-1 max-w-sm mx-auto">
                  Be the first to share your experience at {establishment.name}!
                </p>
              </div>
            ) : (
              <div className="space-y-3.5">
                {reviews.map((r) => (
                  <Card
                    key={r.id}
                    className="p-5 rounded-2xl border-border/60 bg-card space-y-3 shadow-xs"
                  >
                    <div className="flex items-start justify-between gap-2">
                      <div className="flex items-center gap-2.5">
                        <div className="h-8 w-8 rounded-full bg-primary/10 text-primary font-bold text-xs flex items-center justify-center">
                          {(r.username || "V")[0].toUpperCase()}
                        </div>
                        <div>
                          <h4 className="font-semibold text-xs text-foreground">
                            {r.username || "Visitor"}
                          </h4>
                          <span className="text-[10px] text-muted-foreground">
                            {r.created_at
                              ? new Date(r.created_at).toLocaleDateString("en-PH", {
                                  month: "short",
                                  day: "numeric",
                                  year: "numeric",
                                })
                              : "Verified Guest"}
                          </span>
                        </div>
                      </div>

                      {r.rating != null && (
                        <div className="flex items-center gap-0.5">
                          {[1, 2, 3, 4, 5].map((s) => (
                            <Star
                              key={s}
                              className={`h-3 w-3 ${
                                s <= (r.rating || 5)
                                  ? "fill-amber-400 text-amber-400"
                                  : "text-muted-foreground/20"
                              }`}
                            />
                          ))}
                        </div>
                      )}
                    </div>

                    {r.comment && (
                      <p className="text-xs text-muted-foreground leading-relaxed pl-10">
                        {r.comment}
                      </p>
                    )}

                    {/* Owner replies */}
                    {r.replies && r.replies.length > 0 && (
                      <div className="ml-10 mt-2 space-y-2">
                        {r.replies.map((reply) => (
                          <div
                            key={reply.id}
                            className="p-3 rounded-xl bg-muted/60 border border-border/40 text-xs space-y-1"
                          >
                            <div className="flex items-center gap-1.5 font-bold text-[11px] text-primary">
                              <ShieldCheck className="h-3.5 w-3.5" />
                              <span>Response from {reply.username || "Owner"}</span>
                            </div>
                            <p className="text-muted-foreground text-[11px] leading-relaxed">
                              {reply.comment}
                            </p>
                          </div>
                        ))}
                      </div>
                    )}
                  </Card>
                ))}
              </div>
            )}
          </section>
        </div>

        {/* Right Sidebar: Operating Hours, Location & Related */}
        <div className="lg:col-span-4 space-y-6">
          {/* Operating Hours Timetable Card */}
          <Card className="p-6 rounded-3xl border-border/70 bg-card space-y-4 shadow-xs">
            <div className="flex items-center justify-between">
              <h3 className="text-base font-bold text-foreground flex items-center gap-2">
                <Clock className="h-4 w-4 text-primary" />
                Operating Hours
              </h3>
              <Badge
                variant="outline"
                className={`text-[10px] font-semibold ${openStatus.badgeClass} border-border/40`}
              >
                {openStatus.isOpen ? "Open" : "Closed"}
              </Badge>
            </div>

            {establishment.operating_hours ? (
              <div className="space-y-2 text-xs divide-y divide-border/30">
                {DAY_KEYS.map((day) => {
                  const hours = establishment.operating_hours?.[day.key] || "Closed";
                  const isCurrentDay =
                    new Date().getDay() ===
                    (day.key === "sun"
                      ? 0
                      : day.key === "mon"
                      ? 1
                      : day.key === "tue"
                      ? 2
                      : day.key === "wed"
                      ? 3
                      : day.key === "thu"
                      ? 4
                      : day.key === "fri"
                      ? 5
                      : 6);

                  return (
                    <div
                      key={day.key}
                      className={`flex items-center justify-between pt-2 ${
                        isCurrentDay
                          ? "font-bold text-primary"
                          : "text-muted-foreground"
                      }`}
                    >
                      <span className="flex items-center gap-1.5">
                        {isCurrentDay && (
                          <span className="h-1.5 w-1.5 rounded-full bg-primary" />
                        )}
                        {day.label}
                      </span>
                      <span>
                        {hours === "00:00-23:59" ? "Open 24 Hours" : hours}
                      </span>
                    </div>
                  );
                })}
              </div>
            ) : (
              <p className="text-xs text-muted-foreground leading-relaxed">
                Standard operating hours vary by season. Call ahead for special holiday schedules.
              </p>
            )}
          </Card>

          {/* Location & Map Direction Card */}
          <Card className="p-6 rounded-3xl border-border/70 bg-card space-y-4 shadow-xs">
            <h3 className="text-base font-bold text-foreground flex items-center gap-2">
              <MapPin className="h-4 w-4 text-primary" />
              Location & Map
            </h3>

            {establishment.address && (
              <div className="space-y-1 text-xs text-muted-foreground">
                <p className="font-semibold text-foreground">{establishment.address}</p>
                <p>Municipality of Mangatarem, Pangasinan, Philippines</p>
              </div>
            )}

            {establishment.latitude && establishment.longitude && (
              <div className="p-3 rounded-xl bg-muted/50 border border-border/40 text-[11px] text-muted-foreground space-y-1">
                <div className="flex justify-between">
                  <span>Latitude:</span>
                  <span className="font-mono text-foreground">{establishment.latitude}</span>
                </div>
                <div className="flex justify-between">
                  <span>Longitude:</span>
                  <span className="font-mono text-foreground">{establishment.longitude}</span>
                </div>
              </div>
            )}

            <div className="space-y-2 pt-1">
              <Link href="/map" className="block w-full">
                <Button variant="outline" className="w-full text-xs gap-1.5 rounded-xl">
                  <Navigation className="h-3.5 w-3.5 text-primary" />
                  View on Interactive Map
                </Button>
              </Link>

              {establishment.latitude && establishment.longitude && (
                <a
                  href={`https://www.google.com/maps/search/?api=1&query=${establishment.latitude},${establishment.longitude}`}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="block w-full"
                >
                  <Button variant="secondary" className="w-full text-xs gap-1.5 rounded-xl">
                    <ExternalLink className="h-3.5 w-3.5" />
                    Open in Google Maps
                  </Button>
                </a>
              )}
            </div>
          </Card>

          {/* Related / Nearby Establishments */}
          {relatedBusinesses && relatedBusinesses.length > 0 && (
            <Card className="p-6 rounded-3xl border-border/70 bg-card space-y-4 shadow-xs">
              <h3 className="text-base font-bold text-foreground">
                Other Places in Mangatarem
              </h3>

              <div className="space-y-3">
                {relatedBusinesses.slice(0, 3).map((item) => {
                  const Icon = CATEGORY_CONFIG[item.type]?.icon || Store;
                  return (
                    <Link
                      key={item.id}
                      href={`/business/${item.id}`}
                      className="block p-3 rounded-2xl bg-muted/40 hover:bg-primary/10 border border-border/40 transition-colors group"
                    >
                      <div className="flex items-center gap-3">
                        <div className="p-2 rounded-xl bg-card border border-border/40 text-primary shrink-0">
                          <Icon className="h-4 w-4" />
                        </div>
                        <div className="min-w-0 flex-1">
                          <h4 className="text-xs font-bold text-foreground truncate group-hover:text-primary transition-colors">
                            {item.name}
                          </h4>
                          <p className="text-[10px] text-muted-foreground truncate">
                            {CATEGORY_CONFIG[item.type]?.label || item.type}
                            {item.barangay_name ? ` • Brgy. ${item.barangay_name}` : ""}
                          </p>
                        </div>
                        <ArrowRight className="h-3.5 w-3.5 text-muted-foreground group-hover:text-primary group-hover:translate-x-0.5 transition-all shrink-0" />
                      </div>
                    </Link>
                  );
                })}
              </div>
            </Card>
          )}
        </div>
      </div>
    </div>
  );
}
