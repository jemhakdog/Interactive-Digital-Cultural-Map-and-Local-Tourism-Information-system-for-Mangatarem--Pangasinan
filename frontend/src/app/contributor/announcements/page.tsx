"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { fetchAPI } from "@/lib/api";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Loader2, Plus, PenSquare } from "lucide-react";
import type { Announcement } from "@/components/contributor/types";

export default function ContributorAnnouncementsPage() {
  const [items, setItems] = useState<Announcement[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let cancelled = false;
    (async () => {
      try {
        // TODO: FastAPI endpoint not implemented yet — using local placeholder state.
        const data = await fetchAPI<{ items?: Announcement[] }>("/api/contributor/announcements");
        if (!cancelled) setItems(data.items ?? []);
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

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold tracking-tight">Manage Announcements</h1>
          <p className="text-sm text-muted-foreground">Barangay broadcast updates &amp; bulletins</p>
        </div>
        <Link href="/contributor/announcements/new">
          <Button size="sm" className="gap-1.5 rounded-lg">
            <Plus className="h-4 w-4" /> Create Announcement
          </Button>
        </Link>
      </div>

      <Card className="border-border/50">
        <CardContent className="p-0">
          <div className="flex items-center justify-between px-6 py-4 border-b border-border">
            <h3 className="text-sm font-semibold uppercase tracking-wider">Barangay Bulletins</h3>
            <span className="text-[11px] text-muted-foreground">{items.length} Announcements Total</span>
          </div>
          {loading ? (
            <div className="flex justify-center py-12">
              <Loader2 className="h-5 w-5 animate-spin text-muted-foreground" />
            </div>
          ) : items.length > 0 ? (
            <ul className="divide-y divide-border">
              {items.map((item) => (
                <li
                  key={item.id}
                  className="px-6 py-5 flex flex-col md:flex-row md:items-center justify-between gap-4"
                >
                  <div className="space-y-1.5 max-w-3xl">
                    <div className="flex items-center gap-3">
                      <h4 className="text-base font-semibold">{item.title}</h4>
                      <StatusBadge status={item.status} />
                    </div>
                    <p className="text-xs text-muted-foreground leading-relaxed line-clamp-2">{item.content}</p>
                    {item.created_at && (
                      <p className="text-[10px] uppercase tracking-wider text-muted-foreground">{item.created_at}</p>
                    )}
                  </div>
                  <div className="flex items-center gap-3 self-end md:self-center">
                    <Link href={`/contributor/announcements/${item.id}`}>
                      <Button variant="outline" size="sm" className="gap-1.5 rounded-lg">
                        <PenSquare className="h-3.5 w-3.5" /> Edit
                      </Button>
                    </Link>
                  </div>
                </li>
              ))}
            </ul>
          ) : (
            <div className="px-6 py-16 text-center">
              <div className="w-16 h-16 bg-muted text-muted-foreground rounded-2xl flex items-center justify-center mx-auto mb-4 text-2xl">
                📢
              </div>
              <p className="text-sm font-semibold text-muted-foreground">No announcements posted yet.</p>
              <p className="text-xs text-muted-foreground mt-1">
                Submit bulletins to keep the community and tourists informed.
              </p>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}

function StatusBadge({ status }: { status?: string }) {
  if (status === "approved") return <Badge variant="secondary">Approved</Badge>;
  if (status === "rejected") return <Badge variant="destructive">Rejected</Badge>;
  return <Badge variant="outline">Pending</Badge>;
}
