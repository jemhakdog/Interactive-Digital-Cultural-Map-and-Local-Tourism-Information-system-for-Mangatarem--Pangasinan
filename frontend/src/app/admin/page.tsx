"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { useAuth } from "@/lib/auth";
import { fetchAPI } from "@/lib/api";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Loader2, MapPin, Calendar, Building2, Users, ArrowRight, Shield } from "lucide-react";

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
    { label: "Attractions", value: stats?.attractions ?? 0, icon: MapPin, href: "/admin/attractions", color: "text-emerald-500 bg-emerald-500/10" },
    { label: "Events", value: stats?.events ?? 0, icon: Calendar, href: "/admin/events", color: "text-blue-500 bg-blue-500/10" },
    { label: "Businesses", value: stats?.businesses ?? 0, icon: Building2, href: "/admin", color: "text-amber-500 bg-amber-500/10" },
    { label: "Users", value: stats?.users ?? 0, icon: Users, href: "/admin/users", color: "text-purple-500 bg-purple-500/10" },
  ];

  return (
    <div className="container mx-auto px-4 py-8 max-w-5xl">
      <div className="flex items-center gap-3 mb-8">
        <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-primary/10 text-primary">
          <Shield className="h-5 w-5" />
        </div>
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Admin Dashboard</h1>
          <p className="text-muted-foreground text-sm mt-0.5">Manage the Mangatarem tourism platform</p>
        </div>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        {cards.map((c) => (
          <Link key={c.label} href={c.href}>
            <Card className="group border-border/50 hover:shadow-md hover:border-primary/20 transition-all cursor-pointer">
              <CardContent className="p-5 flex items-center gap-4">
                <div className={`flex h-12 w-12 shrink-0 items-center justify-center rounded-xl ${c.color} group-hover:scale-110 transition-transform`}>
                  <c.icon className="h-5 w-5" />
                </div>
                <div>
                  <p className="text-2xl font-bold">{c.value}</p>
                  <p className="text-xs text-muted-foreground">{c.label}</p>
                </div>
              </CardContent>
            </Card>
          </Link>
        ))}
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
        {[
          { href: "/admin/attractions", label: "Manage Attractions", icon: MapPin },
          { href: "/admin/events", label: "Manage Events", icon: Calendar },
        ].map(({ href, label, icon: Icon }) => (
          <Link key={href} href={href}>
            <Button variant="outline" className="w-full justify-start gap-3 h-12 rounded-xl">
              <Icon className="h-4 w-4 text-primary" />
              <span className="flex-1 text-left">{label}</span>
              <ArrowRight className="h-4 w-4 text-muted-foreground" />
            </Button>
          </Link>
        ))}
      </div>
    </div>
  );
}
