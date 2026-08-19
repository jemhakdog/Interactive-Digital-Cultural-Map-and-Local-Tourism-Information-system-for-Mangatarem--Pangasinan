"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { useAuth } from "@/lib/auth";
import { fetchAPI } from "@/lib/api";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { MapPin, Calendar, Star, Loader2 } from "lucide-react";

export default function DashboardPage() {
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

  if (authLoading || !user) {
    return <div className="flex justify-center py-16"><Loader2 className="h-6 w-6 animate-spin text-muted-foreground" /></div>;
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-2">Welcome, {user.name}!</h1>
      <p className="text-muted-foreground mb-8">Your Mangatarem dashboard</p>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">Role</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-2xl font-bold capitalize">{user.role || "User"}</p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">Status</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-2xl font-bold">{user.is_approved ? "✅ Approved" : "⏳ Pending"}</p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">Passport Stamps</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-2xl font-bold">
              {loading ? "—" : (passport?.total_stamps as number) ?? 0}
            </p>
          </CardContent>
        </Card>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <Link href="/attractions">
          <Card className="hover:shadow-md transition-shadow cursor-pointer">
            <CardContent className="flex items-center gap-3 p-4">
              <MapPin className="h-8 w-8 text-primary" />
              <div>
                <p className="font-semibold">Attractions</p>
                <p className="text-xs text-muted-foreground">Explore places</p>
              </div>
            </CardContent>
          </Card>
        </Link>
        <Link href="/events">
          <Card className="hover:shadow-md transition-shadow cursor-pointer">
            <CardContent className="flex items-center gap-3 p-4">
              <Calendar className="h-8 w-8 text-primary" />
              <div>
                <p className="font-semibold">Events</p>
                <p className="text-xs text-muted-foreground">Upcoming events</p>
              </div>
            </CardContent>
          </Card>
        </Link>
        <Link href="/passport">
          <Card className="hover:shadow-md transition-shadow cursor-pointer">
            <CardContent className="flex items-center gap-3 p-4">
              <Star className="h-8 w-8 text-primary" />
              <div>
                <p className="font-semibold">Passport</p>
                <p className="text-xs text-muted-foreground">Your stamps</p>
              </div>
            </CardContent>
          </Card>
        </Link>
        <Link href="/map">
          <Card className="hover:shadow-md transition-shadow cursor-pointer">
            <CardContent className="flex items-center gap-3 p-4">
              <MapPin className="h-8 w-8 text-primary" />
              <div>
                <p className="font-semibold">Map</p>
                <p className="text-xs text-muted-foreground">Interactive map</p>
              </div>
            </CardContent>
          </Card>
        </Link>
      </div>

      {user.role === "admin" && (
        <div className="mt-8">
          <h2 className="text-xl font-bold mb-4">Admin</h2>
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
            <Link href="/admin">
              <Button variant="outline" className="w-full justify-start gap-2">📊 Dashboard</Button>
            </Link>
            <Link href="/admin/attractions">
              <Button variant="outline" className="w-full justify-start gap-2">🏛️ Manage Attractions</Button>
            </Link>
            <Link href="/admin/events">
              <Button variant="outline" className="w-full justify-start gap-2">📅 Manage Events</Button>
            </Link>
          </div>
        </div>
      )}
    </div>
  );
}
