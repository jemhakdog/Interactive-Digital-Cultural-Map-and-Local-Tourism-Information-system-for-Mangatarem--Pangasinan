"use client";

import { useMemo, useState } from "react";
import Link from "next/link";
import { Search, MapPin, ArrowRight, Album } from "lucide-react";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent } from "@/components/ui/card";

export interface BarangayItem {
  name: string;
  tags?: string[];
  category?: string;
  attraction_count?: number;
  image_url?: string;
}

const CATEGORIES = ["All", "Nature", "History", "Food", "Festivals"] as const;

export function BarangayExplorer({ barangays }: { barangays: BarangayItem[] }) {
  const [query, setQuery] = useState("");
  const [category, setCategory] = useState<string>("All");

  const filtered = useMemo(() => {
    const q = query.trim().toLowerCase();
    return barangays.filter((b) => {
      const matchesQuery = !q || b.name.toLowerCase().includes(q);
      const matchesCategory =
        category === "All" || b.category === category || (b.tags ?? []).includes(category);
      return matchesQuery && matchesCategory;
    });
  }, [barangays, query, category]);

  return (
    <div className="space-y-8">
      {/* Search + filter */}
      <div className="bg-card border border-border/60 rounded-2xl p-5 sm:p-6 shadow-sm space-y-4">
        <div className="relative">
          <Search className="absolute left-3.5 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
          <Input
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Search by barangay name..."
            className="pl-10 h-11 rounded-xl bg-background border-input text-sm"
          />
        </div>
        <div className="flex flex-wrap gap-2">
          {CATEGORIES.map((c) => {
            const active = category === c;
            return (
              <button
                key={c}
                type="button"
                onClick={() => setCategory(c)}
                className={`px-3.5 py-1.5 rounded-full text-xs font-semibold transition-colors ${
                  active
                    ? "bg-primary text-primary-foreground"
                    : "bg-muted text-muted-foreground hover:bg-primary/10 hover:text-primary"
                }`}
              >
                {c === "All" ? "All Experiences" : c}
              </button>
            );
          })}
        </div>
      </div>

      <div className="flex items-center justify-between">
        <span className="text-sm font-semibold text-muted-foreground">
          {filtered.length} Barangay{filtered.length === 1 ? "" : "s"}
        </span>
      </div>

      {filtered.length === 0 ? (
        <div className="text-center py-20 bg-card border border-dashed border-border rounded-2xl">
          <Album className="h-12 w-12 mx-auto text-muted-foreground/40 mb-4" />
          <h3 className="text-xl font-bold text-foreground mb-2">No barangays found</h3>
          <p className="text-sm text-muted-foreground max-w-md mx-auto">
            Try a different search term or category filter.
          </p>
        </div>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
          {filtered.map((b) => (
            <Link key={b.name} href={`/barangays/${encodeURIComponent(b.name)}`} className="group block">
              <Card className="rounded-2xl border-border/60 overflow-hidden hover:border-primary/40 hover:shadow-md transition-all h-full">
                <div className="aspect-[4/3] bg-muted relative flex items-center justify-center overflow-hidden">
                  {b.image_url ? (
                    // eslint-disable-next-line @next/next/no-img-element
                    <img
                      src={b.image_url}
                      alt={b.name}
                      className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
                      loading="lazy"
                    />
                  ) : (
                    <MapPin className="h-16 w-16 text-primary/20" />
                  )}
                  <div className="absolute top-3 left-3">
                    <Badge variant="secondary" className="bg-card/90 text-primary font-bold uppercase tracking-wider text-[10px]">
                      {b.tags?.[0] ?? b.category ?? "Discovery"}
                    </Badge>
                  </div>
                </div>
                <CardContent className="p-4 text-center space-y-2">
                  <h3 className="text-lg font-bold text-foreground group-hover:text-primary transition-colors">
                    {b.name}
                  </h3>
                  <div className="flex items-center justify-center gap-2 text-xs text-muted-foreground uppercase tracking-wider">
                    <span>{b.attraction_count ?? 0} Spots</span>
                    <span className="w-1 h-1 rounded-full bg-primary/40" />
                    <span className="inline-flex items-center gap-1">
                      Enter <ArrowRight className="h-3 w-3" />
                    </span>
                  </div>
                </CardContent>
              </Card>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}
