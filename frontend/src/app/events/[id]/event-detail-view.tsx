"use client";

import { useState } from "react";
import Link from "next/link";
import {
  Calendar,
  MapPin,
  Clock,
  ArrowLeft,
  ArrowRight,
  Share2,
  CalendarPlus,
  Check,
  Navigation,
  Sparkles,
  Info,
  Building,
  CheckCircle2,
  ArrowUpRight,
} from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Separator } from "@/components/ui/separator";
import { EventItem } from "../events-view";

interface EventDetailViewProps {
  event: EventItem;
  relatedEvents?: EventItem[];
}

export function EventDetailView({ event, relatedEvents = [] }: EventDetailViewProps) {
  const [copied, setCopied] = useState(false);

  // Format date helper
  const formatDate = (dateStr?: string) => {
    if (!dateStr) return { full: "Date to be announced", day: "", month: "", time: "", weekday: "" };
    const d = new Date(dateStr);
    return {
      full: d.toLocaleDateString("en-PH", {
        weekday: "long",
        month: "long",
        day: "numeric",
        year: "numeric",
      }),
      weekday: d.toLocaleDateString("en-PH", { weekday: "long" }),
      month: d.toLocaleDateString("en-PH", { month: "short" }).toUpperCase(),
      day: d.getDate().toString(),
      year: d.getFullYear().toString(),
      time: d.toLocaleTimeString("en-PH", { hour: "numeric", minute: "2-digit" }),
    };
  };

  const dateMeta = formatDate(event.date);

  // Generate .ics file for Apple Calendar, Outlook, etc.
  const handleDownloadICS = () => {
    const startDate = event.date ? new Date(event.date) : new Date();
    const endDate = new Date(startDate.getTime() + 4 * 60 * 60 * 1000); // 4-hour default
    const formatICSDate = (d: Date) =>
      d.toISOString().replace(/[-:]/g, "").split(".")[0] + "Z";

    const ics = [
      "BEGIN:VCALENDAR",
      "VERSION:2.0",
      "PRODID:-//Mangatarem Tourism//Cultural Events//EN",
      "CALSCALE:GREGORIAN",
      "BEGIN:VEVENT",
      `SUMMARY:${event.name}`,
      `DESCRIPTION:${(event.description || "").replace(/\n/g, " ")}`,
      `LOCATION:${event.location ? `${event.location}, ` : ""}Mangatarem, Pangasinan`,
      `DTSTART:${formatICSDate(startDate)}`,
      `DTEND:${formatICSDate(endDate)}`,
      "STATUS:CONFIRMED",
      "END:VEVENT",
      "END:VCALENDAR",
    ].join("\r\n");

    const blob = new Blob([ics], { type: "text/calendar;charset=utf-8" });
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.setAttribute("download", `${event.name.toLowerCase().replace(/[^a-z0-9]/g, "_")}.ics`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  // Google Calendar Link
  const getGoogleCalendarLink = () => {
    const startDate = event.date ? new Date(event.date) : new Date();
    const endDate = new Date(startDate.getTime() + 4 * 60 * 60 * 1000);
    const formatGDate = (d: Date) =>
      d.toISOString().replace(/[-:]/g, "").split(".")[0] + "Z";

    const params = new URLSearchParams({
      action: "TEMPLATE",
      text: event.name,
      dates: `${formatGDate(startDate)}/${formatGDate(endDate)}`,
      details: event.description || "",
      location: `${event.location || ""}, Mangatarem, Pangasinan`,
    });
    return `https://calendar.google.com/calendar/render?${params.toString()}`;
  };

  // Share action
  const handleShare = async () => {
    const url = typeof window !== "undefined" ? window.location.href : "";
    if (navigator.share) {
      try {
        await navigator.share({
          title: event.name,
          text: `Check out ${event.name} in Mangatarem, Pangasinan!`,
          url: url,
        });
        return;
      } catch {
        // user cancelled or failed, fallback to clipboard
      }
    }
    navigator.clipboard.writeText(url);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  // Generate highlights dynamically based on category
  const highlights = [
    {
      title: "Cultural Celebration",
      description: "Experience authentic Mangatarem traditions, local hospitality, and festive pride.",
    },
    {
      title: "Local Gastronomy & Delicacies",
      description: "Taste native Pangasinan delicacies, street eats, and home-cooked regional specialties.",
    },
    {
      title: "Community Performances & Exhibits",
      description: "Enjoy vibrant street performances, agricultural exhibits, and artisanal craft booths.",
    },
    {
      title: "Free & Family Friendly",
      description: "Open to tourists, families, and visitors of all ages with designated visitor assistance.",
    },
  ];

  return (
    <div className="space-y-8 max-w-6xl mx-auto">
      {/* ── Breadcrumb & Back Link ── */}
      <div className="flex items-center justify-between flex-wrap gap-4">
        <Link
          href="/events"
          className="inline-flex items-center gap-1.5 text-sm font-medium text-muted-foreground hover:text-foreground transition-colors group"
        >
          <ArrowLeft className="h-4 w-4 group-hover:-translate-x-1 transition-transform" />
          Back to Events
        </Link>
        <div className="flex items-center gap-2">
          <Button
            variant="outline"
            size="sm"
            onClick={handleShare}
            className="gap-1.5 rounded-xl text-xs"
            aria-label="Share this event"
          >
            {copied ? (
              <>
                <Check className="h-3.5 w-3.5 text-primary" />
                <span>Link Copied!</span>
              </>
            ) : (
              <>
                <Share2 className="h-3.5 w-3.5" />
                <span>Share</span>
              </>
            )}
          </Button>

          <Button
            variant="default"
            size="sm"
            onClick={handleDownloadICS}
            className="gap-1.5 rounded-xl text-xs"
          >
            <CalendarPlus className="h-3.5 w-3.5" />
            <span>Add to Calendar</span>
          </Button>
        </div>
      </div>

      {/* ── Hero Banner Section ── */}
      <div className="relative rounded-2xl overflow-hidden border border-border/60 bg-muted aspect-[21/9] sm:aspect-[21/8] shadow-sm">
        {event.image_url ? (
          <img
            src={event.image_url}
            alt={event.name}
            className="w-full h-full object-cover"
          />
        ) : (
          <div className="w-full h-full flex items-center justify-center bg-primary/10">
            <Calendar className="h-20 w-20 text-primary/30" />
          </div>
        )}
        <div className="absolute inset-0 bg-gradient-to-t from-background/90 via-background/30 to-transparent" />

        {/* Floating Badges in Hero */}
        <div className="absolute top-4 left-4 flex gap-2">
          {event.category && (
            <Badge variant="secondary" className="backdrop-blur-md bg-background/90 font-medium">
              {event.category}
            </Badge>
          )}
          {event.barangay_name && (
            <Badge variant="outline" className="backdrop-blur-md bg-background/80">
              Brgy. {event.barangay_name}
            </Badge>
          )}
        </div>

        {event.date && (
          <div className="absolute bottom-4 left-4 right-4 sm:right-auto sm:max-w-xl flex items-center gap-3 bg-background/95 backdrop-blur-md p-3 px-4 rounded-xl border border-border/50 shadow-sm">
            <div className="flex flex-col items-center justify-center px-3 py-1 bg-primary/10 rounded-lg text-primary text-center">
              <span className="text-[10px] font-bold uppercase leading-none">{dateMeta.month}</span>
              <span className="text-xl font-extrabold leading-tight">{dateMeta.day}</span>
            </div>
            <div>
              <p className="text-xs text-muted-foreground font-medium">{dateMeta.weekday}</p>
              <p className="text-sm font-semibold text-foreground">{dateMeta.full}</p>
            </div>
          </div>
        )}
      </div>

      {/* ── Title & Quick Meta ── */}
      <div className="space-y-3">
        <h1 className="text-3xl sm:text-4xl font-bold tracking-tight text-foreground">
          {event.name}
        </h1>

        <div className="flex flex-wrap items-center gap-y-2 gap-x-5 text-sm text-muted-foreground">
          {event.date && (
            <div className="flex items-center gap-1.5">
              <Clock className="h-4 w-4 text-primary" />
              <span>{dateMeta.time ? `Starts at ${dateMeta.time}` : "All Day Event"}</span>
            </div>
          )}
          {event.location && (
            <div className="flex items-center gap-1.5">
              <MapPin className="h-4 w-4 text-primary" />
              <span>{event.location}</span>
            </div>
          )}
          {event.barangay_name && (
            <div className="flex items-center gap-1.5">
              <Building className="h-4 w-4 text-muted-foreground" />
              <span>Barangay {event.barangay_name}, Mangatarem</span>
            </div>
          )}
        </div>
      </div>

      <Separator className="bg-border/60" />

      {/* ── Two Column Main Layout ── */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
        {/* Main Column (8 cols) */}
        <div className="lg:col-span-8 space-y-8">
          {/* About the Event */}
          <section className="space-y-3">
            <h2 className="text-xl font-bold tracking-tight text-foreground flex items-center gap-2">
              <Info className="h-5 w-5 text-primary" />
              About this Event
            </h2>
            <div className="prose prose-neutral dark:prose-invert max-w-none text-muted-foreground leading-relaxed">
              <p className="text-base text-foreground/90 whitespace-pre-line">
                {event.description ||
                  `${event.name} is an important cultural gathering celebrated in Mangatarem, Pangasinan. Bringing together residents, visitors, and cultural heritage advocates to celebrate community traditions.`}
              </p>
            </div>
          </section>

          {/* Festival Highlights */}
          <section className="space-y-4">
            <h2 className="text-xl font-bold tracking-tight text-foreground flex items-center gap-2">
              <Sparkles className="h-5 w-5 text-primary" />
              Event Highlights & Activities
            </h2>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              {highlights.map((h, i) => (
                <Card key={i} className="border-border/60 bg-card p-4 rounded-xl">
                  <div className="flex items-start gap-3">
                    <CheckCircle2 className="h-5 w-5 text-primary shrink-0 mt-0.5" />
                    <div>
                      <h3 className="font-semibold text-sm text-foreground">{h.title}</h3>
                      <p className="text-xs text-muted-foreground mt-1 leading-relaxed">
                        {h.description}
                      </p>
                    </div>
                  </div>
                </Card>
              ))}
            </div>
          </section>

          {/* Visitor Guide */}
          <section className="rounded-2xl border border-border/60 bg-muted/30 p-6 space-y-4">
            <h2 className="text-lg font-bold text-foreground">Visitor Tips & Guidelines</h2>
            <ul className="space-y-2.5 text-sm text-muted-foreground">
              <li className="flex items-start gap-2">
                <span className="text-primary font-bold">•</span>
                <span>
                  <strong>Admission:</strong> General admission to town plaza and community fiestas is free and open to the public.
                </span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-primary font-bold">•</span>
                <span>
                  <strong>Best Time to Arrive:</strong> Arrive 30 to 45 minutes before scheduled program times for optimal viewing and easy parking.
                </span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-primary font-bold">•</span>
                <span>
                  <strong>Local Etiquette:</strong> Respect local traditions, support resident food vendors, and follow municipal cleanliness policies.
                </span>
              </li>
            </ul>
          </section>
        </div>

        {/* Sidebar Column (4 cols) */}
        <div className="lg:col-span-4 space-y-6">
          {/* Quick Details Card */}
          <Card className="border-border/60 bg-card p-5 rounded-2xl shadow-xs space-y-4">
            <h3 className="font-bold text-base text-foreground">Event Overview</h3>
            <div className="space-y-3.5 text-sm">
              <div className="flex items-start gap-3">
                <Calendar className="h-4 w-4 text-primary shrink-0 mt-0.5" />
                <div>
                  <p className="text-xs text-muted-foreground">Date</p>
                  <p className="font-medium text-foreground">{dateMeta.full}</p>
                </div>
              </div>

              {dateMeta.time && (
                <div className="flex items-start gap-3">
                  <Clock className="h-4 w-4 text-primary shrink-0 mt-0.5" />
                  <div>
                    <p className="text-xs text-muted-foreground">Time</p>
                    <p className="font-medium text-foreground">{dateMeta.time}</p>
                  </div>
                </div>
              )}

              <div className="flex items-start gap-3">
                <MapPin className="h-4 w-4 text-primary shrink-0 mt-0.5" />
                <div>
                  <p className="text-xs text-muted-foreground">Venue</p>
                  <p className="font-medium text-foreground">{event.location || "Mangatarem"}</p>
                  {event.barangay_name && (
                    <p className="text-xs text-muted-foreground">Brgy. {event.barangay_name}</p>
                  )}
                </div>
              </div>

              {event.category && (
                <div className="flex items-start gap-3">
                  <Sparkles className="h-4 w-4 text-primary shrink-0 mt-0.5" />
                  <div>
                    <p className="text-xs text-muted-foreground">Category</p>
                    <p className="font-medium text-foreground">{event.category}</p>
                  </div>
                </div>
              )}
            </div>

            <Separator className="bg-border/60 my-2" />

            {/* Calendar & Map Actions */}
            <div className="space-y-2 pt-1">
              <a
                href={getGoogleCalendarLink()}
                target="_blank"
                rel="noopener noreferrer"
                className="w-full"
              >
                <Button variant="outline" className="w-full justify-between rounded-xl text-xs">
                  <span>Add to Google Calendar</span>
                  <ArrowUpRight className="h-3.5 w-3.5 text-muted-foreground" />
                </Button>
              </a>
              <Link href="/map" className="w-full block">
                <Button variant="secondary" className="w-full justify-between rounded-xl text-xs">
                  <span className="flex items-center gap-1.5">
                    <Navigation className="h-3.5 w-3.5 text-primary" />
                    Open Interactive Map
                  </span>
                  <ArrowUpRight className="h-3.5 w-3.5 text-muted-foreground" />
                </Button>
              </Link>
            </div>
          </Card>

          {/* Location & Barangay Card */}
          <Card className="border-border/60 bg-muted/40 p-5 rounded-2xl space-y-3">
            <h3 className="font-bold text-sm text-foreground flex items-center gap-1.5">
              <Building className="h-4 w-4 text-primary" />
              Host Community
            </h3>
            <p className="text-xs text-muted-foreground leading-relaxed">
              Organized by the Local Government Unit of Mangatarem in partnership with Barangay{" "}
              <strong>{event.barangay_name || "Poblacion"}</strong> and the Municipal Tourism Office.
            </p>
          </Card>
        </div>
      </div>

      {/* ── Related Events Section ── */}
      {relatedEvents.length > 0 && (
        <section className="pt-8 border-t border-border/60 space-y-6">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-2xl font-bold tracking-tight text-foreground">
                More Events in Mangatarem
              </h2>
              <p className="text-sm text-muted-foreground mt-0.5">
                Explore more local festivals and upcoming community events
              </p>
            </div>
            <Link href="/events">
              <Button variant="ghost" size="sm" className="text-xs gap-1">
                View All Events <ArrowRight className="h-3 w-3" />
              </Button>
            </Link>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-5">
            {relatedEvents.slice(0, 3).map((r) => {
              const rDate = formatDate(r.date);
              return (
                <Link key={r.id} href={`/events/${r.id}`} className="group">
                  <Card className="overflow-hidden border-border/60 bg-card hover:border-primary/40 hover:shadow-md transition-all duration-300 hover:-translate-y-1 h-full">
                    <div className="aspect-[16/10] bg-muted relative overflow-hidden">
                      {r.image_url ? (
                        <img
                          src={r.image_url}
                          alt={r.name}
                          className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
                        />
                      ) : (
                        <div className="w-full h-full flex items-center justify-center bg-primary/5">
                          <Calendar className="h-8 w-8 text-primary/30" />
                        </div>
                      )}
                      {r.category && (
                        <Badge
                          variant="secondary"
                          className="absolute top-2.5 left-2.5 text-[10px] bg-background/90"
                        >
                          {r.category}
                        </Badge>
                      )}
                      {r.date && (
                        <div className="absolute top-2.5 right-2.5 bg-background/90 backdrop-blur-sm rounded-lg px-2 py-1 text-center shadow-xs">
                          <p className="text-[9px] font-bold text-primary leading-none uppercase">
                            {rDate.month}
                          </p>
                          <p className="text-xs font-bold leading-tight">{rDate.day}</p>
                        </div>
                      )}
                    </div>
                    <CardContent className="p-4 space-y-1.5">
                      <h3 className="font-semibold text-sm line-clamp-1 group-hover:text-primary transition-colors">
                        {r.name}
                      </h3>
                      {r.barangay_name && (
                        <p className="text-xs text-muted-foreground">Brgy. {r.barangay_name}</p>
                      )}
                    </CardContent>
                  </Card>
                </Link>
              );
            })}
          </div>
        </section>
      )}
    </div>
  );
}
