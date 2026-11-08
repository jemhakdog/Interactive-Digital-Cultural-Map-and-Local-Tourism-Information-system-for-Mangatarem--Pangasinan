"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/lib/auth";
import { fetchAPI } from "@/lib/api";
import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Loader2, Award, MapPin, Star, Sparkles, BookOpen } from "lucide-react";

export default function PassportPage() {
  const { user, loading: authLoading } = useAuth();
  const [passport, setPassport] = useState<Record<string, unknown> | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!user) {
      setLoading(false);
      return;
    }
    fetchAPI("/api/gamification/passport")
      .then((data) => setPassport(data as Record<string, unknown>))
      .catch(() => {})
      .finally(() => setLoading(false));
  }, [user]);

  if (authLoading || (user && loading)) {
    return <div className="flex justify-center py-16"><Loader2 className="h-6 w-6 animate-spin text-muted-foreground" /></div>;
  }

  // Guest Passport preview if unauthenticated
  if (!user) {
    return (
      <div className="container mx-auto px-4 py-10 max-w-4xl">
        <div className="rounded-2xl border bg-card p-6 md:p-10 shadow-sm text-center mb-8">
          <div className="h-20 w-20 rounded-full bg-primary/10 flex items-center justify-center mx-auto mb-4">
            <BookOpen className="h-10 w-10 text-primary" />
          </div>
          <Badge variant="secondary" className="mb-3">Digital Heritage Passport</Badge>
          <h1 className="text-3xl md:text-4xl font-bold tracking-tight mb-3">
            Explore Mangatarem & Collect Stamps
          </h1>
          <p className="text-muted-foreground max-w-xl mx-auto mb-6">
            Check in at historical landmarks, eco-tourism spots, and local events across Mangatarem to earn commemorative digital stamps and unlock explorer badges.
          </p>
          <div className="flex flex-wrap items-center justify-center gap-3">
            <Link href="/auth/register">
              <Button size="lg" className="rounded-xl gap-2">
                <Sparkles className="h-4 w-4" /> Start Your Passport
              </Button>
            </Link>
            <Link href="/auth/login">
              <Button variant="outline" size="lg" className="rounded-xl">
                Log In to View Stamps
              </Button>
            </Link>
          </div>
        </div>

        <h2 className="text-xl font-bold mb-4">Sample Collector Badges</h2>
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 mb-8">
          {[
            { icon: "🏛️", title: "Heritage Sentinel", desc: "Visit San Raymundo Church" },
            { icon: "🌿", title: "Canopy Pioneer", desc: "Check in at Manleluag Spring" },
            { icon: "⛰️", title: "Ridge Cruiser", desc: "Traverse Daang Kalikasan" },
            { icon: "🥭", title: "Fiesta Explorer", desc: "Attend local town celebrations" },
          ].map((item, idx) => (
            <Card key={idx} className="text-center p-4">
              <div className="text-3xl mb-2">{item.icon}</div>
              <p className="font-semibold text-sm">{item.title}</p>
              <p className="text-xs text-muted-foreground mt-1">{item.desc}</p>
            </Card>
          ))}
        </div>
      </div>
    );
  }

  const stamps = (passport?.stamps ?? []) as Record<string, unknown>[];
  const badges = (passport?.badges ?? []) as Record<string, unknown>[];

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="flex items-center gap-3 mb-8">
        <div className="h-16 w-16 rounded-full bg-primary/10 flex items-center justify-center">
          <span className="text-2xl">📕</span>
        </div>
        <div>
          <h1 className="text-3xl font-bold">Tourist Passport</h1>
          <p className="text-muted-foreground">Your Mangatarem adventure stamps</p>
        </div>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-2 md:grid-cols-3 gap-4 mb-8">
        <Card>
          <CardContent className="p-4 text-center">
            <MapPin className="h-6 w-6 text-primary mx-auto mb-1" />
            <p className="text-2xl font-bold">{stamps.length}</p>
            <p className="text-xs text-muted-foreground">Places Visited</p>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4 text-center">
            <Award className="h-6 w-6 text-primary mx-auto mb-1" />
            <p className="text-2xl font-bold">{badges.length}</p>
            <p className="text-xs text-muted-foreground">Badges Earned</p>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4 text-center">
            <Star className="h-6 w-6 text-primary mx-auto mb-1" />
            <p className="text-2xl font-bold">{(passport?.points as number) ?? 0}</p>
            <p className="text-xs text-muted-foreground">Points</p>
          </CardContent>
        </Card>
      </div>

      {/* Badges */}
      {badges.length > 0 && (
        <div className="mb-8">
          <h2 className="text-xl font-bold mb-4">Badges</h2>
          <div className="flex flex-wrap gap-3">
            {badges.map((b, i) => (
              <Card key={i} className="w-32 text-center">
                <CardContent className="p-4">
                  <span className="text-3xl">{String(b.icon ?? "🏆")}</span>
                  <p className="text-xs font-medium mt-2">{String(b.name)}</p>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      )}

      {/* Stamps */}
      <div>
        <h2 className="text-xl font-bold mb-4">Stamps</h2>
        {stamps.length === 0 ? (
          <Card>
            <CardContent className="p-8 text-center text-muted-foreground">
              <MapPin className="h-12 w-12 mx-auto mb-4 opacity-30" />
              <p>No stamps yet. Visit attractions to collect stamps!</p>
            </CardContent>
          </Card>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {stamps.map((s, i) => (
              <Card key={i}>
                <CardContent className="p-4">
                  <div className="flex items-center gap-3">
                    <div className="h-10 w-10 rounded-full bg-primary/10 flex items-center justify-center text-lg">
                      {String(s.icon ?? "📌")}
                    </div>
                    <div>
                      <p className="font-medium text-sm">{String(s.name)}</p>
                      <p className="text-xs text-muted-foreground">
                        {s.date ? new Date(String(s.date)).toLocaleDateString() : ""}
                      </p>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
