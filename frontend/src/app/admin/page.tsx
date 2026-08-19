"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { useAuth } from "@/lib/auth";
import { fetchAPI } from "@/lib/api";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Loader2, MapPin, Calendar, Building2, Users } from "lucide-react";

export default function AdminPage() {
  const { user, loading: authLoading } = useAuth();
  const router = useRouter();
  const [stats, setStats] = useState<{ attractions: number; events: number; businesses: number; users: number } | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!authLoading && (!user || user.role !== "admin")) router.push("/dashboard");
  }, [user, authLoading, router]);

  useEffect(() => {
    if (!user || user.role !== "admin") return;
    // Fetch counts from list endpoints
    Promise.all([
      fetchAPI("/api/attractions").then((d) => (d as { items: unknown[] }).items?.length ?? 0),
      fetchAPI("/api/events").then((d) => (d as { items: unknown[] }).items?.length ?? 0),
      fetchAPI("/api/business").then((d) => (d as { items: unknown[] }).items?.length ?? 0),
    ])
      .then(([attractions, events, businesses]) =>
        setStats({ attractions, events, businesses, users: 0 })
      )
      .catch(() => {})
      .finally(() => setLoading(false));
  }, [user]);

  if (authLoading || !user || loading) {
    return <div className="flex justify-center py-16"><Loader2 className="h-6 w-6 animate-spin text-muted-foreground" /></div>;
  }

  const cards = [
    { label: "Attractions", value: stats?.attractions ?? 0, icon: MapPin, href: "/admin/attractions" },
    { label: "Events", value: stats?.events ?? 0, icon: Calendar, href: "/admin/events" },
    { label: "Businesses", value: stats?.businesses ?? 0, icon: Building2, href: "/admin" },
    { label: "Users", value: stats?.users ?? 0, icon: Users, href: "/admin/users" },
  ];

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-2">Admin Dashboard</h1>
      <p className="text-muted-foreground mb-8">Manage the Mangatarem tourism platform</p>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        {cards.map((c) => (
          <Link key={c.label} href={c.href}>
            <Card className="hover:shadow-md transition-shadow cursor-pointer">
              <CardContent className="p-4 flex items-center gap-3">
                <c.icon className="h-8 w-8 text-primary" />
                <div>
                  <p className="text-2xl font-bold">{c.value}</p>
                  <p className="text-xs text-muted-foreground">{c.label}</p>
                </div>
              </CardContent>
            </Card>
          </Link>
        ))}
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        <Link href="/admin/attractions">
          <Button variant="outline" className="w-full justify-start gap-2">🏛️ Manage Attractions</Button>
        </Link>
        <Link href="/admin/events">
          <Button variant="outline" className="w-full justify-start gap-2">📅 Manage Events</Button>
        </Link>
      </div>
    </div>
  );
}
