"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { fetchAPI } from "@/lib/api";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { MapPin, CalendarDays, Images, Star, Loader2, Plus, Megaphone, User } from "lucide-react";

interface Stats {
  total: number;
  approved: number;
  pending: number;
  rejected: number;
  reviews: number;
}

interface ActivityItem {
  id: number;
  name: string;
  type: string;
  status: string;
  date?: string;
  href?: string;
}

export default function ContributorDashboardPage() {
  const [stats, setStats] = useState<Stats>({ total: 0, approved: 0, pending: 0, rejected: 0, reviews: 0 });
  const [activity, setActivity] = useState<ActivityItem[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let cancelled = false;
    (async () => {
      try {
        // TODO: FastAPI endpoint not implemented yet — using local placeholder state.
        const data = await fetchAPI<Stats>("/api/contributor/stats");
        if (!cancelled) setStats(data);
      } catch {
        /* keep placeholder */
      }
      try {
        // TODO: FastAPI endpoint not implemented yet — using local placeholder state.
        const data = await fetchAPI<{ items?: ActivityItem[] }>("/api/contributor/activity");
        if (!cancelled) setActivity(data.items ?? []);
      } catch {
        /* keep placeholder */
      } finally {
        if (!cancelled) setLoading(false);
      }
    })();
    return () => {
      cancelled = true;
    };
  }, []);

  const statCards = [
    { label: "Mapped Assets", value: stats.total, icon: MapPin },
    { label: "Verified & Public", value: stats.approved, icon: Star },
    { label: "Awaiting Review", value: stats.pending, icon: CalendarDays },
    { label: "Needs Correction", value: stats.rejected, icon: Images },
    { label: "Total Reviews", value: stats.reviews, icon: Megaphone },
  ];

  return (
    <div className="space-y-8">
      <div className="flex items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold tracking-tight">Barangay Command Center</h1>
          <p className="text-sm text-muted-foreground">Stewardship of the Community-Based Information System (CBIS)</p>
        </div>
        <Badge variant="secondary" className="gap-1.5">
          <span className="h-1.5 w-1.5 rounded-full bg-primary" /> Barangay Steward Active
        </Badge>
      </div>

      <div className="grid grid-cols-2 lg:grid-cols-5 gap-4">
        {statCards.map((c) => {
          const Icon = c.icon;
          return (
            <Card key={c.label} className="border-border/50">
              <CardContent className="p-5 flex flex-col gap-3">
                <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-primary/10 text-primary">
                  <Icon className="h-5 w-5" />
                </div>
                <div>
                  <p className="text-3xl font-bold tracking-tight">{loading ? "—" : c.value}</p>
                  <p className="text-[11px] uppercase tracking-wider text-muted-foreground mt-1">{c.label}</p>
                </div>
              </CardContent>
            </Card>
          );
        })}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="lg:col-span-2">
          <Card className="border-border/50">
            <CardContent className="p-0">
              <div className="flex items-center justify-between px-6 py-4 border-b border-border">
                <h3 className="text-sm font-semibold uppercase tracking-wider">Community Activity Feed</h3>
                <span className="text-[11px] text-muted-foreground">Last 5 updates</span>
              </div>
              {loading ? (
                <div className="flex justify-center py-12">
                  <Loader2 className="h-5 w-5 animate-spin text-muted-foreground" />
                </div>
              ) : activity.length > 0 ? (
                <ul className="divide-y divide-border">
                  {activity.slice(0, 5).map((item) => (
                    <li key={item.id} className="flex items-center justify-between gap-4 px-6 py-4">
                      <div className="flex items-center gap-3">
                        <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-primary/10 text-primary">
                          {item.type === "Attraction" ? "🏰" : "📅"}
                        </div>
                        <div>
                          <p className="text-sm font-semibold">{item.name}</p>
                          <p className="text-[11px] uppercase tracking-wider text-muted-foreground">
                            {item.type}
                            {item.date ? ` • ${item.date}` : ""}
                          </p>
                        </div>
                      </div>
                      <StatusBadge status={item.status} />
                    </li>
                  ))}
                </ul>
              ) : (
                <div className="px-6 py-12 text-center">
                  <p className="text-sm font-semibold text-muted-foreground">No submissions registered yet.</p>
                  <p className="text-xs text-muted-foreground mt-1">
                    Cultural landmarks and local events managed under CBIS will appear here.
                  </p>
                </div>
              )}
            </CardContent>
          </Card>
        </div>

        <div className="space-y-6">
          <Card className="border-border/50 bg-primary text-primary-foreground">
            <CardContent className="p-6 space-y-3">
              <h3 className="text-lg font-bold tracking-tight">Contribute Heritage</h3>
              <p className="text-sm text-primary-foreground/80">
                Map a new cultural asset or publish local events under CBIS stewardship.
              </p>
              <div className="space-y-2 pt-1">
                <Link href="/contributor/attractions/new" className="block">
                  <Button variant="secondary" size="sm" className="w-full gap-1.5 rounded-lg">
                    <Plus className="h-4 w-4" /> Add Landmark
                  </Button>
                </Link>
                <Link href="/contributor/events/new" className="block">
                  <Button variant="secondary" size="sm" className="w-full gap-1.5 rounded-lg">
                    <Plus className="h-4 w-4" /> Publish Event
                  </Button>
                </Link>
              </div>
            </CardContent>
          </Card>

          <Card className="border-border/50">
            <CardContent className="p-6 space-y-2">
              <h3 className="text-sm font-semibold uppercase tracking-wider">Quick Links</h3>
              <Link href="/contributor/gallery/new">
                <Button variant="outline" size="sm" className="w-full justify-start gap-2 rounded-lg">
                  <Images className="h-4 w-4 text-primary" /> Add Media
                </Button>
              </Link>
              <Link href="/contributor/announcements">
                <Button variant="outline" size="sm" className="w-full justify-start gap-2 rounded-lg">
                  <Megaphone className="h-4 w-4 text-primary" /> Announcements
                </Button>
              </Link>
              <Link href="/contributor/profile">
                <Button variant="outline" size="sm" className="w-full justify-start gap-2 rounded-lg">
                  <User className="h-4 w-4 text-primary" /> Barangay Profile
                </Button>
              </Link>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}

function StatusBadge({ status }: { status?: string }) {
  if (status === "approved") return <Badge variant="secondary">Approved</Badge>;
  if (status === "rejected") return <Badge variant="destructive">Correction Required</Badge>;
  return <Badge variant="outline">Pending</Badge>;
}
