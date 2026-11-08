"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { Search, MapPin, Sparkles } from "lucide-react";
import { Button } from "@/components/ui/button";

const QUICK_FILTERS = [
  { label: "Hot Springs", q: "Manleluag" },
  { label: "Historic Church", q: "San Raymundo" },
  { label: "Waterfalls", q: "Waterfalls" },
  { label: "Nature Parks", q: "Nature" },
  { label: "Eco Tourism", q: "Eco" },
];

export function HeroSearch() {
  const router = useRouter();
  const [query, setQuery] = useState("");

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    const trimmed = query.trim();
    if (trimmed) {
      router.push(`/search?q=${encodeURIComponent(trimmed)}`);
    } else {
      router.push("/search");
    }
  };

  const handleFilterClick = (filterQuery: string) => {
    router.push(`/search?q=${encodeURIComponent(filterQuery)}`);
  };

  return (
    <div className="w-full max-w-2xl mx-auto mt-6">
      <form
        role="search"
        onSubmit={handleSearch}
        className="relative flex items-center bg-white/95 dark:bg-card/95 text-foreground backdrop-blur-md rounded-2xl p-2 shadow-xl shadow-black/10 border border-white/20 transition-all focus-within:ring-2 focus-within:ring-white focus-within:border-transparent"
      >
        <div className="flex items-center pl-3 pointer-events-none text-muted-foreground">
          <Search className="h-5 w-5" aria-hidden="true" />
        </div>
        <input
          type="search"
          name="q"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Search natural springs, churches, trails, local spots..."
          aria-label="Search destinations, cultural heritage, and activities in Mangatarem"
          autoComplete="off"
          autoCorrect="off"
          autoCapitalize="off"
          spellCheck="false"
          className="w-full bg-transparent px-3 py-2 text-sm sm:text-base outline-none placeholder:text-muted-foreground/70"
        />
        <Button
          type="submit"
          className="shrink-0 rounded-xl px-5 py-2 font-medium bg-primary text-primary-foreground hover:bg-primary/90 transition-transform active:scale-95"
        >
          Explore
        </Button>
      </form>

      {/* Quick Discovery Pills */}
      <div className="flex flex-wrap items-center justify-center gap-2 mt-4 text-xs">
        <span className="flex items-center gap-1 text-primary-foreground/80 font-medium">
          <Sparkles className="h-3.5 w-3.5" aria-hidden="true" /> Popular:
        </span>
        {QUICK_FILTERS.map((f) => (
          <button
            key={f.label}
            type="button"
            onClick={() => handleFilterClick(f.q)}
            className="inline-flex items-center gap-1 rounded-full bg-white/15 hover:bg-white/25 text-white px-3 py-1 text-xs backdrop-blur-sm border border-white/20 transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-white"
          >
            <MapPin className="h-3 w-3 opacity-70" aria-hidden="true" />
            {f.label}
          </button>
        ))}
      </div>
    </div>
  );
}
