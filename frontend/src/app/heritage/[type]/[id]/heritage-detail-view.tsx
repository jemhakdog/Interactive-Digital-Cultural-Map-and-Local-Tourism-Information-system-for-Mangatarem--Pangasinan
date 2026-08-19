"use client";

import { useState } from "react";
import Link from "next/link";
import {
  Landmark,
  TreePine,
  Music,
  Gem,
  Layers,
  MapPin,
  Calendar,
  User,
  ShieldCheck,
  Building,
  Check,
  Share2,
  Printer,
  Compass,
  ArrowLeft,
  ArrowRight,
  ChevronRight,
  Info,
  BookOpen,
  Quote,
  Sparkles,
  ExternalLink,
  Tag,
  Clock,
  Award,
} from "lucide-react";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button, buttonVariants } from "@/components/ui/button";
import { Separator } from "@/components/ui/separator";
import {
  HeritageItem,
  HERITAGE_TYPES_CONFIG,
  HeritageTypeConfig,
} from "../../heritage-types";

interface HeritageDetailViewProps {
  item: HeritageItem;
  relatedItems?: HeritageItem[];
}

export function HeritageDetailView({
  item,
  relatedItems = [],
}: HeritageDetailViewProps) {
  const [copied, setCopied] = useState(false);

  const config: HeritageTypeConfig =
    HERITAGE_TYPES_CONFIG[item.asset_type] || HERITAGE_TYPES_CONFIG.built;
  const Icon = config.icon;

  const handleCopyLink = () => {
    navigator.clipboard.writeText(window.location.href);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handlePrint = () => {
    window.print();
  };

  return (
    <div className="space-y-10">
      {/* ── Breadcrumb Navigation ── */}
      <nav className="flex items-center gap-2 text-xs text-muted-foreground font-medium flex-wrap">
        <Link href="/heritage" className="hover:text-primary transition-colors">
          Heritage Registry
        </Link>
        <ChevronRight className="h-3.5 w-3.5 text-muted-foreground/60" />
        <Link
          href={`/heritage/${item.asset_type}`}
          className="hover:text-primary transition-colors"
        >
          {config.label}
        </Link>
        <ChevronRight className="h-3.5 w-3.5 text-muted-foreground/60" />
        <span className="text-foreground font-semibold truncate max-w-[200px] md:max-w-none">
          {item.name_of_asset}
        </span>
      </nav>

      {/* ── Editorial Header Banner ── */}
      <div className="rounded-3xl border border-border/60 bg-gradient-to-br from-card via-card to-muted/30 p-6 md:p-10 shadow-sm relative overflow-hidden space-y-6">
        <div className="flex flex-wrap items-center gap-2.5">
          <Badge className="bg-primary text-primary-foreground font-bold text-xs">
            {config.badgeLabel}
          </Badge>
          <Badge variant="outline" className="text-xs font-semibold">
            {config.subtitle}
          </Badge>
          {item.barangay_name && (
            <Badge variant="secondary" className="text-xs">
              <MapPin className="h-3 w-3 mr-1 text-primary" />
              Barangay {item.barangay_name}
            </Badge>
          )}
        </div>

        <div className="space-y-2 max-w-4xl">
          <h1 className="text-3xl md:text-5xl font-bold tracking-tight text-foreground leading-tight">
            {item.name_of_asset}
          </h1>
          {item.common_name && (
            <p className="text-base md:text-lg text-muted-foreground italic font-serif">
              Local Name / Oral Title: &ldquo;{item.common_name}&rdquo;
            </p>
          )}
        </div>

        {/* Quick Action Toolbar */}
        <div className="flex flex-wrap items-center gap-3 pt-4 border-t border-border/50">
          <Button
            variant="outline"
            size="sm"
            onClick={handleCopyLink}
            className="gap-2 text-xs font-semibold"
          >
            {copied ? (
              <>
                <Check className="h-3.5 w-3.5 text-emerald-600" />
                <span>Link Copied!</span>
              </>
            ) : (
              <>
                <Share2 className="h-3.5 w-3.5" />
                <span>Share Profile</span>
              </>
            )}
          </Button>

          <Button
            variant="outline"
            size="sm"
            onClick={handlePrint}
            className="gap-2 text-xs font-semibold"
          >
            <Printer className="h-3.5 w-3.5" />
            <span>Print Profile</span>
          </Button>

          {item.latitude && item.longitude && (
            <Link
              href={`/map?lat=${item.latitude}&lng=${item.longitude}&zoom=16`}
              className={buttonVariants({ variant: "default", size: "sm", className: "gap-2 text-xs font-semibold" })}
            >
              <Compass className="h-3.5 w-3.5" />
              <span>Locate on Cultural Map</span>
            </Link>
          )}

          <Link
            href={`/heritage/${item.asset_type}`}
            className={buttonVariants({ variant: "ghost", size: "sm", className: "ml-auto text-xs text-muted-foreground hover:text-foreground" })}
          >
            <ArrowLeft className="h-3.5 w-3.5 mr-1" />
            <span>Back to {config.label}</span>
          </Link>
        </div>
      </div>

      {/* ── Featured Photography Area (if available) ── */}
      {item.image_url && (
        <div className="rounded-3xl overflow-hidden border border-border/60 shadow-md bg-muted aspect-[21/9] max-h-[480px] relative">
          <img
            src={item.image_url}
            alt={item.name_of_asset}
            className="w-full h-full object-cover"
          />
          <div className="absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-transparent" />
          <div className="absolute bottom-4 left-6 right-6 text-white text-xs flex items-center justify-between">
            <span className="font-medium drop-shadow-sm">
              Official Heritage Documentation Photography — Mangatarem Cultural Registry
            </span>
            <span className="hidden sm:inline font-mono opacity-80">
              {item.location_details || `Mangatarem, Pangasinan`}
            </span>
          </div>
        </div>
      )}

      {/* ── Main Content Grid ── */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
        {/* Main Narrative Column (8 cols) */}
        <div className="lg:col-span-8 space-y-8">
          {/* Section 1: Physical Description & Identity */}
          <section className="p-6 md:p-8 rounded-3xl bg-card border border-border/60 shadow-sm space-y-4">
            <div className="flex items-center gap-2.5 pb-3 border-b border-border/50">
              <div className="h-8 w-8 rounded-lg bg-primary/10 text-primary flex items-center justify-center">
                <Building className="h-4 w-4" />
              </div>
              <h2 className="text-xl md:text-2xl font-bold text-foreground">
                Physical Description & Overview
              </h2>
            </div>

            <div className="text-muted-foreground text-sm md:text-base leading-relaxed space-y-3">
              <p>
                {item.location_details
                  ? `Located at ${item.location_details}. `
                  : ""}
                This registered {config.label.toLowerCase()} entry forms an integral part of Mangatarem&apos;s cultural heritage registry.
              </p>
              {item.category && (
                <div className="inline-flex items-center gap-2 px-3 py-1 rounded-lg bg-muted text-foreground text-xs font-semibold">
                  <Tag className="h-3 w-3 text-primary" />
                  <span>Category: {item.category}</span>
                </div>
              )}
            </div>
          </section>

          {/* Section 2: Historical & Cultural Significance */}
          <section className="p-6 md:p-8 rounded-3xl bg-card border border-border/60 shadow-sm space-y-4">
            <div className="flex items-center gap-2.5 pb-3 border-b border-border/50">
              <div className="h-8 w-8 rounded-lg bg-amber-500/10 text-amber-600 dark:text-amber-400 flex items-center justify-center">
                <Sparkles className="h-4 w-4" />
              </div>
              <h2 className="text-xl md:text-2xl font-bold text-foreground">
                Cultural & Historical Significance
              </h2>
            </div>

            <div className="p-5 md:p-6 rounded-2xl bg-amber-50/50 dark:bg-amber-950/20 border border-amber-200/60 dark:border-amber-900/40 relative">
              <Quote className="h-8 w-8 text-amber-500/20 absolute right-4 bottom-4" />
              <p className="text-foreground text-sm md:text-base leading-relaxed font-serif italic">
                {item.significance ||
                  "This cultural property is recognized for its historical, artistic, scientific, and socio-cultural value to the people of Mangatarem and the Province of Pangasinan."}
              </p>
            </div>
          </section>

          {/* Section 3: Associated Stories, Lore & Oral Traditions */}
          {item.stories && (
            <section className="p-6 md:p-8 rounded-3xl bg-card border border-border/60 shadow-sm space-y-4">
              <div className="flex items-center gap-2.5 pb-3 border-b border-border/50">
                <div className="h-8 w-8 rounded-lg bg-purple-500/10 text-purple-600 dark:text-purple-400 flex items-center justify-center">
                  <BookOpen className="h-4 w-4" />
                </div>
                <h2 className="text-xl md:text-2xl font-bold text-foreground">
                  Associated Lore & Community Narratives
                </h2>
              </div>

              <div className="text-muted-foreground text-sm md:text-base leading-relaxed p-4 rounded-2xl bg-muted/40 border border-border/40">
                <p>{item.stories}</p>
              </div>
            </section>
          )}

          {/* Section 4: Conservation Status & Protection */}
          <section className="p-6 md:p-8 rounded-3xl bg-card border border-border/60 shadow-sm space-y-4">
            <div className="flex items-center gap-2.5 pb-3 border-b border-border/50">
              <div className="h-8 w-8 rounded-lg bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 flex items-center justify-center">
                <ShieldCheck className="h-4 w-4" />
              </div>
              <h2 className="text-xl md:text-2xl font-bold text-foreground">
                Conservation & Protection Status
              </h2>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div className="p-4 rounded-2xl bg-muted/50 border border-border/50 space-y-1">
                <span className="text-xs font-bold text-muted-foreground uppercase tracking-wider block">
                  Current Condition
                </span>
                <span className="font-semibold text-foreground text-sm block">
                  {item.conservation_status || "Maintained by Custodian / Community"}
                </span>
              </div>

              <div className="p-4 rounded-2xl bg-muted/50 border border-border/50 space-y-1">
                <span className="text-xs font-bold text-muted-foreground uppercase tracking-wider block">
                  Protection Level
                </span>
                <span className="font-semibold text-foreground text-sm block">
                  {item.protection_status || "Registered Local Heritage Property (RA 10066)"}
                </span>
              </div>
            </div>
          </section>
        </div>

        {/* Sidebar Information Column (4 cols) */}
        <div className="lg:col-span-4 space-y-6">
          {/* Registry Metadata Card */}
          <div className="p-6 rounded-3xl bg-card border border-border/60 shadow-sm space-y-5">
            <h3 className="font-bold text-base text-foreground pb-3 border-b border-border/50 flex items-center gap-2">
              <Award className="h-4 w-4 text-primary" />
              <span>Heritage Information</span>
            </h3>

            <div className="space-y-3.5 text-xs">
              <div>
                <span className="text-muted-foreground block text-[11px] uppercase font-bold tracking-wider">
                  Classification
                </span>
                <span className="font-semibold text-foreground mt-0.5 block">
                  {config.label}
                </span>
              </div>

              {item.ownership_type && (
                <div>
                  <span className="text-muted-foreground block text-[11px] uppercase font-bold tracking-wider">
                    Ownership Type
                  </span>
                  <span className="font-semibold text-foreground mt-0.5 block">
                    {item.ownership_type}
                  </span>
                </div>
              )}

              {item.owner_administrator && (
                <div>
                  <span className="text-muted-foreground block text-[11px] uppercase font-bold tracking-wider">
                    Administrator / Custodian
                  </span>
                  <span className="font-semibold text-foreground mt-0.5 block">
                    {item.owner_administrator}
                  </span>
                </div>
              )}

              {item.usage_status && (
                <div>
                  <span className="text-muted-foreground block text-[11px] uppercase font-bold tracking-wider">
                    Usage Status
                  </span>
                  <span className="font-semibold text-foreground mt-0.5 block">
                    {item.usage_status}
                  </span>
                </div>
              )}

              {item.mapper_name && (
                <div>
                  <span className="text-muted-foreground block text-[11px] uppercase font-bold tracking-wider">
                    Documenting Agency
                  </span>
                  <span className="font-semibold text-foreground mt-0.5 block">
                    {item.mapper_name}
                  </span>
                </div>
              )}

              {item.date_profiled && (
                <div>
                  <span className="text-muted-foreground block text-[11px] uppercase font-bold tracking-wider">
                    Date Documented
                  </span>
                  <span className="font-semibold text-foreground mt-0.5 block">
                    {item.date_profiled}
                  </span>
                </div>
              )}
            </div>
          </div>

          {/* Geo-Location Card (if coordinates exist) */}
          {item.latitude && item.longitude && (
            <div className="p-6 rounded-3xl bg-card border border-border/60 shadow-sm space-y-4">
              <h3 className="font-bold text-base text-foreground pb-2 border-b border-border/50 flex items-center gap-2">
                <MapPin className="h-4 w-4 text-primary" />
                <span>Geographic Location</span>
              </h3>

              <div className="p-4 rounded-2xl bg-muted/60 font-mono text-xs space-y-1.5">
                <div className="flex justify-between">
                  <span className="text-muted-foreground">LATITUDE:</span>
                  <span className="font-bold text-foreground">{item.latitude.toFixed(5)}° N</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-muted-foreground">LONGITUDE:</span>
                  <span className="font-bold text-foreground">{item.longitude.toFixed(5)}° E</span>
                </div>
                {item.barangay_name && (
                  <div className="flex justify-between pt-1 border-t border-border/50">
                    <span className="text-muted-foreground">BARANGAY:</span>
                    <span className="font-bold text-foreground">Brgy. {item.barangay_name}</span>
                  </div>
                )}
              </div>

              <Link
                href={`/map?lat=${item.latitude}&lng=${item.longitude}&zoom=16`}
                className={buttonVariants({ variant: "default", size: "default", className: "w-full text-xs font-semibold gap-2" })}
              >
                <Compass className="h-4 w-4" />
                <span>Open on Cultural Map</span>
              </Link>
            </div>
          )}

          {/* Tourism Office Contact Card */}
          <div className="p-6 rounded-3xl bg-gradient-to-br from-primary/5 to-muted/40 border border-border/60 shadow-sm space-y-3">
            <h4 className="font-bold text-sm text-foreground flex items-center gap-2">
              <Info className="h-4 w-4 text-primary" />
              <span>Cultural Heritage Office</span>
            </h4>
            <p className="text-xs text-muted-foreground leading-relaxed">
              For academic research, visitation guidelines, or inquiries regarding this heritage site, contact the Municipal Tourism & Heritage Office.
            </p>
            <div className="pt-2">
              <Link
                href="/dashboard"
                className={buttonVariants({ variant: "outline", size: "sm", className: "w-full text-xs font-medium" })}
              >
                <span>Contact Tourism Staff</span>
              </Link>
            </div>
          </div>
        </div>
      </div>

      {/* ── Related Heritage Section ── */}
      {relatedItems.length > 0 && (
        <section className="pt-8 border-t border-border/60 space-y-6">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-xl md:text-2xl font-bold text-foreground">
                More in {config.label}
              </h2>
              <p className="text-xs text-muted-foreground mt-0.5">
                Explore related cultural properties in Mangatarem.
              </p>
            </div>
            <Link
              href={`/heritage/${item.asset_type}`}
              className={buttonVariants({ variant: "ghost", size: "sm", className: "text-xs font-semibold gap-1" })}
            >
              <span>View All</span>
              <ArrowRight className="h-3.5 w-3.5" />
            </Link>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {relatedItems.slice(0, 3).map((rel) => (
              <Card
                key={rel.id}
                className="group overflow-hidden border-border/60 hover:border-primary/40 hover:shadow-md transition-all duration-300 flex flex-col justify-between h-full bg-card"
              >
                <div>
                  <div className="aspect-[16/10] bg-muted relative overflow-hidden">
                    {rel.image_url ? (
                      <img
                        src={rel.image_url}
                        alt={rel.name_of_asset}
                        className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
                      />
                    ) : (
                      <div className="w-full h-full flex items-center justify-center text-muted-foreground/40">
                        <Icon className="h-10 w-10" />
                      </div>
                    )}
                    {rel.barangay_name && (
                      <Badge variant="secondary" className="absolute top-3 left-3 text-[10px] bg-background/80 backdrop-blur-sm">
                        {rel.barangay_name}
                      </Badge>
                    )}
                  </div>

                  <CardContent className="p-4 space-y-2">
                    <h3 className="font-bold text-sm text-foreground line-clamp-1 group-hover:text-primary transition-colors">
                      {rel.name_of_asset}
                    </h3>
                    <p className="text-xs text-muted-foreground line-clamp-2 leading-relaxed">
                      {rel.significance || "Registered entry in the Mangatarem Cultural Heritage Registry."}
                    </p>
                  </CardContent>
                </div>

                <div className="p-4 pt-0">
                  <Link
                    href={`/heritage/${rel.asset_type}/${rel.id}`}
                    className={buttonVariants({ variant: "outline", size: "sm", className: "w-full justify-between text-xs font-semibold group-hover:bg-primary group-hover:text-primary-foreground transition-colors" })}
                  >
                    <span>View Profile</span>
                    <ArrowRight className="h-3 w-3" />
                  </Link>
                </div>
              </Card>
            ))}
          </div>
        </section>
      )}
    </div>
  );
}
