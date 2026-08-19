"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/lib/auth";
import { fetchAPI } from "@/lib/api";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Loader2, Award, MapPin, Star } from "lucide-react";

export default function PassportPage() {
  const { user, loading: authLoading } = useAuth();
  const router = useRouter();
  const [passport, setPassport] = useState<Record<string, unknown> | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!authLoading && !user) router.push("/auth/login");
  }, [user, authLoading, router]);

  useEffect(() => {
    if (!user) return;
    fetchAPI("/api/gamification/passport")
      .then((data) => setPassport(data as Record<string, unknown>))
      .catch(() => {})
      .finally(() => setLoading(false));
  }, [user]);

  if (authLoading || !user || loading) {
    return <div className="flex justify-center py-16"><Loader2 className="h-6 w-6 animate-spin text-muted-foreground" /></div>;
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
