"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { Search as SearchIcon, MapPin, Calendar, Loader2 } from "lucide-react";
import { Input } from "@/components/ui/input";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { fetchAPI } from "@/lib/api";

export default function SearchPage() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<{ attractions: unknown[]; events: unknown[] } | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!query.trim()) { setResults(null); return; }
    const t = setTimeout(() => {
      setLoading(true);
      fetchAPI(`/api/search?q=${encodeURIComponent(query)}`)
        .then((data) => setResults(data as { attractions: unknown[]; events: unknown[] }))
        .catch(() => setResults(null))
        .finally(() => setLoading(false));
    }, 400);
    return () => clearTimeout(t);
  }, [query]);

  const attractions = (results?.attractions ?? []) as { id: number; name: string; category?: string }[];
  const events = (results?.events ?? []) as { id: number; name: string; date?: string }[];

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-6">Search</h1>

      <div className="relative max-w-xl mb-8">
        <SearchIcon className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
        <Input
          placeholder="Search attractions, events..."
          className="pl-10"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          autoFocus
        />
      </div>

      {loading && (
        <div className="flex items-center gap-2 text-muted-foreground py-8">
          <Loader2 className="h-4 w-4 animate-spin" /> Searching...
        </div>
      )}

      {!loading && results && attractions.length === 0 && events.length === 0 && (
        <p className="text-muted-foreground py-8">No results found for &ldquo;{query}&rdquo;</p>
      )}

      {attractions.length > 0 && (
        <section className="mb-8">
          <h2 className="text-xl font-semibold mb-4">Attractions ({attractions.length})</h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {attractions.map((a) => (
              <Link key={a.id} href={`/attractions/${a.id}`}>
                <Card className="hover:shadow-md transition-shadow cursor-pointer h-full">
                  <CardContent className="p-4">
                    <div className="flex items-start gap-3">
                      <MapPin className="h-5 w-5 text-primary shrink-0 mt-0.5" />
                      <div>
                        <h3 className="font-medium text-sm">{a.name}</h3>
                        {a.category && <Badge variant="secondary" className="mt-1 text-xs">{a.category}</Badge>}
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </Link>
            ))}
          </div>
        </section>
      )}

      {events.length > 0 && (
        <section>
          <h2 className="text-xl font-semibold mb-4">Events ({events.length})</h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {events.map((e) => (
              <Link key={e.id} href={`/events/${e.id}`}>
                <Card className="hover:shadow-md transition-shadow cursor-pointer h-full">
                  <CardContent className="p-4">
                    <div className="flex items-start gap-3">
                      <Calendar className="h-5 w-5 text-primary shrink-0 mt-0.5" />
                      <div>
                        <h3 className="font-medium text-sm">{e.name}</h3>
                        {e.date && <p className="text-xs text-muted-foreground">{new Date(e.date).toLocaleDateString()}</p>}
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </Link>
            ))}
          </div>
        </section>
      )}
    </div>
  );
}
