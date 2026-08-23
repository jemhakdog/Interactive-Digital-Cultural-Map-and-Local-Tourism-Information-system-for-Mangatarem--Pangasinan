"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { useAuth } from "@/lib/auth";
import { fetchAPI } from "@/lib/api";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { MapPin, Calendar, Star, Loader2, Compass, Shield, ArrowRight, BookOpen } from "lucide-react";

export default function DashboardPage() {
  const { user, loading: authLoading } = useAuth();
  const router = useRouter();
  const [passport, setPassport] = useState<Record<string, unknown> | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!authLoading) {
      if (!user) {
        router.push("/auth/login");
      } else if (user.role === "admin") {
        router.push("/admin");
      } else if (user.role === "business_owner") {
        router.push("/business/dashboard");
      } else if (user.role === "contributor") {
        router.push("/contributor/dashboard");
      }
    }
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

  const stats = [
    { label: "Role", value: user.role || "User", icon: Shield, color: "text-blue-500 bg-blue-500/10" },
    { label: "Status", value: user.is_approved ? "Approved" : "Pending", icon: Star, color: user.is_approved ? "text-emerald-500 bg-emerald-500/10" : "text-amber-500 bg-amber-500/10" },
    { label: "Stamps", value: loading ? "—" : String((passport?.total_stamps as number) ?? 0), icon: MapPin, color: "text-primary bg-primary/10" },
  ];

  const quickLinks = [
    { href: "/attractions", icon: MapPin, label: "Attractions", desc: "Explore places" },
    { href: "/events", icon: Calendar, label: "Events", desc: "Upcoming events" },
    { href: "/passport", icon: BookOpen, label: "Passport", desc: "Your stamps" },
    { href: "/map", icon: Compass, label: "Map", desc: "Interactive map" },
  ];

  return (
    <div className="container mx-auto px-4 py-8 max-w-5xl">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold tracking-tight">Welcome, {user.name}!</h1>
        <p className="text-muted-foreground mt-1">Your Mangatarem dashboard</p>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-8">
        {stats.map((s) => (
          <Card key={s.label} className="border-border/50">
            <CardContent className="p-5 flex items-center gap-4">
              <div className={`flex h-12 w-12 shrink-0 items-center justify-center rounded-xl ${s.color}`}>
                <s.icon className="h-5 w-5" />
              </div>
              <div>
                <p className="text-xs text-muted-foreground font-medium">{s.label}</p>
                <p className="text-xl font-bold capitalize">{s.value}</p>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Quick links */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        {quickLinks.map(({ href, icon: Icon, label, desc }) => (
          <Link key={href} href={href}>
            <Card className="group border-border/50 hover:shadow-md hover:border-primary/20 transition-all cursor-pointer h-full">
              <CardContent className="p-5">
                <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-primary/10 text-primary mb-3 group-hover:bg-primary group-hover:text-primary-foreground transition-colors">
                  <Icon className="h-5 w-5" />
                </div>
                <p className="font-semibold text-sm">{label}</p>
                <p className="text-xs text-muted-foreground mt-0.5">{desc}</p>
              </CardContent>
            </Card>
          </Link>
        ))}
      </div>

      {/* Admin section */}
      {user.role === "admin" && (
        <div>
          <h2 className="text-lg font-bold mb-4">Admin</h2>
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
            {[
              { href: "/admin", label: "Dashboard", icon: Shield },
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
      )}
    </div>
  );
}
