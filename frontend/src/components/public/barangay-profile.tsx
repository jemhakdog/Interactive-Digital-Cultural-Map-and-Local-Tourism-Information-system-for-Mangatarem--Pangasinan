"use client";

import type { ReactNode } from "react";
import Link from "next/link";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { MapPin, Landmark, Calendar, Images, Sparkles, ArrowRight } from "lucide-react";

export interface BarangayInfo {
  mission?: string;
  vision?: string;
  history?: string;
  unique_features?: string;
  cultural_assets?: string;
  traditions?: string;
  local_practices?: string;
}

export interface SimpleItem {
  id?: number;
  name?: string;
  title?: string;
}

export function BarangayProfile({
  barangayName,
  info,
  attractions,
  events,
  gallery,
}: {
  barangayName: string;
  info: BarangayInfo | null;
  attractions: SimpleItem[];
  events: SimpleItem[];
  gallery: SimpleItem[];
}) {
  const hasInfo = !!info;

  return (
    <div className="space-y-8">
      {/* Modern tab switcher */}
      <Tabs defaultValue="cultural" className="w-full">
        <div className="bg-card border border-border/60 rounded-2xl p-2 flex overflow-x-auto no-scrollbar gap-2 shadow-sm max-w-3xl mx-auto">
          <TabsList className="flex w-full gap-2 bg-transparent">
            <TabsTrigger value="cultural" className="flex-1 rounded-xl text-xs sm:text-sm font-semibold">
              <Landmark className="h-4 w-4 mr-1.5" /> Cultural Profile
            </TabsTrigger>
            <TabsTrigger value="attractions" className="flex-1 rounded-xl text-xs sm:text-sm font-semibold">
              <MapPin className="h-4 w-4 mr-1.5" /> Attractions ({attractions.length})
            </TabsTrigger>
            <TabsTrigger value="events" className="flex-1 rounded-xl text-xs sm:text-sm font-semibold">
              <Calendar className="h-4 w-4 mr-1.5" /> Events ({events.length})
            </TabsTrigger>
            <TabsTrigger value="gallery" className="flex-1 rounded-xl text-xs sm:text-sm font-semibold">
              <Images className="h-4 w-4 mr-1.5" /> Gallery ({gallery.length})
            </TabsTrigger>
          </TabsList>
        </div>

        <div className="mt-8 min-h-[300px]">
          {/* Cultural Profile */}
          <TabsContent value="cultural" className="space-y-6 mt-0">
            {hasInfo ? (
              <div className="space-y-6">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  {info.mission && (
                    <Card className="rounded-2xl border-border/60 p-6">
                      <h3 className="text-lg font-bold text-foreground mb-2 flex items-center gap-2">
                        <Sparkles className="h-4 w-4 text-primary" /> Our Mission
                      </h3>
                      <p className="text-sm text-muted-foreground leading-relaxed whitespace-pre-line">
                        {info.mission}
                      </p>
                    </Card>
                  )}
                  {info.vision && (
                    <Card className="rounded-2xl border-border/60 p-6">
                      <h3 className="text-lg font-bold text-foreground mb-2 flex items-center gap-2">
                        <Sparkles className="h-4 w-4 text-primary" /> Our Vision
                      </h3>
                      <p className="text-sm text-muted-foreground leading-relaxed whitespace-pre-line">
                        {info.vision}
                      </p>
                    </Card>
                  )}
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  {info.history && (
                    <Card className="rounded-2xl border-border/60 p-6 md:col-span-2">
                      <h3 className="text-lg font-bold text-foreground mb-2 flex items-center gap-2">
                        <Landmark className="h-4 w-4 text-primary" /> Our History
                      </h3>
                      <p className="text-sm text-muted-foreground leading-relaxed whitespace-pre-line">
                        {info.history}
                      </p>
                    </Card>
                  )}
                  {info.unique_features && (
                    <Card className="rounded-2xl border-border/60 p-6 bg-primary/5">
                      <h3 className="text-lg font-bold text-foreground mb-2 flex items-center gap-2">
                        <Sparkles className="h-4 w-4 text-primary" /> Unique Gems
                      </h3>
                      <p className="text-sm text-muted-foreground leading-relaxed whitespace-pre-line">
                        {info.unique_features}
                      </p>
                    </Card>
                  )}
                  {info.cultural_assets && (
                    <Card className="rounded-2xl border-border/60 p-6">
                      <h3 className="text-lg font-bold text-foreground mb-2 flex items-center gap-2">
                        <Landmark className="h-4 w-4 text-primary" /> Cultural Assets
                      </h3>
                      <p className="text-sm text-muted-foreground leading-relaxed whitespace-pre-line">
                        {info.cultural_assets}
                      </p>
                    </Card>
                  )}
                  {info.traditions && (
                    <Card className="rounded-2xl border-border/60 p-6">
                      <h3 className="text-lg font-bold text-foreground mb-2 flex items-center gap-2">
                        <Sparkles className="h-4 w-4 text-primary" /> Living Traditions
                      </h3>
                      <p className="text-sm text-muted-foreground leading-relaxed whitespace-pre-line">
                        {info.traditions}
                      </p>
                    </Card>
                  )}
                  {info.local_practices && (
                    <Card className="rounded-2xl border-border/60 p-6">
                      <h3 className="text-lg font-bold text-foreground mb-2 flex items-center gap-2">
                        <Sparkles className="h-4 w-4 text-primary" /> Local Wisdom
                      </h3>
                      <p className="text-sm text-muted-foreground leading-relaxed whitespace-pre-line">
                        {info.local_practices}
                      </p>
                    </Card>
                  )}
                </div>
              </div>
            ) : (
              <EmptyState
                icon={<Landmark className="h-10 w-10 text-primary/30" />}
                title="Cultural Journey Pending"
                description={`The stories and traditions of ${barangayName} are yet to be discovered.`}
              />
            )}
          </TabsContent>

          {/* Attractions */}
          <TabsContent value="attractions" className="mt-0">
            {attractions.length > 0 ? (
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
                {attractions.map((a, i) => (
                  <Card key={a.id ?? i} className="rounded-2xl border-border/60 p-5">
                    <h3 className="font-bold text-foreground">{a.name ?? a.title}</h3>
                  </Card>
                ))}
              </div>
            ) : (
              <EmptyState
                icon={<MapPin className="h-10 w-10 text-primary/30" />}
                title="No attractions listed yet"
                description={`Attractions in ${barangayName} will appear here once catalogued.`}
                cta={{
                  label: "Browse all attractions",
                  href: "/attractions",
                }}
              />
            )}
          </TabsContent>

          {/* Events */}
          <TabsContent value="events" className="mt-0">
            {events.length > 0 ? (
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
                {events.map((e, i) => (
                  <Card key={e.id ?? i} className="rounded-2xl border-border/60 p-5">
                    <h3 className="font-bold text-foreground">{e.name ?? e.title}</h3>
                  </Card>
                ))}
              </div>
            ) : (
              <EmptyState
                icon={<Calendar className="h-10 w-10 text-primary/30" />}
                title="No events scheduled yet"
                description={`Events in ${barangayName} will appear here once announced.`}
                cta={{ label: "Browse all events", href: "/events" }}
              />
            )}
          </TabsContent>

          {/* Gallery */}
          <TabsContent value="gallery" className="mt-0">
            {gallery.length > 0 ? (
              <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-4">
                {gallery.map((g, i) => (
                  <Card key={g.id ?? i} className="rounded-2xl border-border/60 p-5">
                    <h3 className="font-bold text-foreground">{g.name ?? g.title}</h3>
                  </Card>
                ))}
              </div>
            ) : (
              <EmptyState
                icon={<Images className="h-10 w-10 text-primary/30" />}
                title="No gallery items yet"
                description={`Community photos from ${barangayName} will appear here.`}
                cta={{ label: "Browse the gallery", href: "/gallery" }}
              />
            )}
          </TabsContent>
        </div>
      </Tabs>
    </div>
  );
}

function EmptyState({
  icon,
  title,
  description,
  cta,
}: {
  icon: ReactNode;
  title: string;
  description: string;
  cta?: { label: string; href: string };
}) {
  return (
    <div className="text-center py-16 bg-card border border-dashed border-border rounded-2xl">
      <div className="flex justify-center mb-4">{icon}</div>
      <h3 className="text-lg font-bold text-foreground mb-1">{title}</h3>
      <p className="text-sm text-muted-foreground max-w-md mx-auto mb-4">{description}</p>
      {cta && (
        <Link href={cta.href}>
          <Button variant="outline" size="sm" className="rounded-xl gap-1.5">
            {cta.label} <ArrowRight className="h-3.5 w-3.5" />
          </Button>
        </Link>
      )}
    </div>
  );
}
