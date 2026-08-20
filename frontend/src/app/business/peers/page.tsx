"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useAuth } from "@/lib/auth";
import { fetchAPI } from "@/lib/api";
import { EstablishmentItem } from "@/app/business/business-view";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Loader2, Store, Users, Star, MapPin, ArrowLeft, ExternalLink } from "lucide-react";

export default function BusinessPeersPage() {
  const { user, loading: authLoading } = useAuth();
  const router = useRouter();

  const [peers, setPeers] = useState<EstablishmentItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [myType, setMyType] = useState<string | null>(null);

  useEffect(() => {
    if (!authLoading && (!user || user.role !== "business_owner")) {
      router.push("/dashboard");
    }
  }, [user, authLoading, router]);

  useEffect(() => {
    if (!user || user.role !== "business_owner") return;
    const load = async () => {
      try {
        // Public approved list — used to both find the owner's type and peer businesses.
        const data = await fetchAPI<{ establishments?: EstablishmentItem[] }>(
          "/api/business?per_page=100"
        );
        const all = data.establishments ?? [];
        const mine = all.find(
          (e) => (e as EstablishmentItem & { owner_id?: number }).owner_id === user.id
        );
        const type = mine?.type ?? null;
        setMyType(type);
        setPeers(
          all.filter((e) => e.id !== mine?.id && (!type || e.type === type))
        );
      } catch {
        setPeers([]);
      } finally {
        setLoading(false);
      }
    };
    load();
  }, [user]);

  if (authLoading || !user || user.role !== "business_owner") {
    return (
      <div className="flex justify-center py-16">
        <Loader2 className="h-6 w-6 animate-spin text-muted-foreground" />
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8 max-w-6xl space-y-8">
      <div className="flex items-center justify-between pb-4 border-b border-border/50">
        <div className="space-y-1">
          <Link
            href="/business/dashboard"
            className="text-xs font-bold uppercase tracking-wider text-muted-foreground hover:text-foreground flex items-center gap-1.5 transition-colors"
          >
            <ArrowLeft className="h-3.5 w-3.5" /> Back to Dashboard
          </Link>
          <h1 className="text-xl font-bold tracking-tight text-foreground mt-2">
            Market Overview &amp; Local Peers
          </h1>
          <p className="text-[11px] font-bold text-muted-foreground uppercase tracking-wider">
            {myType ? `Browsing approved ${myType} establishments` : "Approved establishments"}
          </p>
        </div>
      </div>

      <div className="bg-muted/40 border border-border/40 p-6 rounded-2xl flex items-start gap-4">
        <div className="w-10 h-10 rounded-xl bg-card flex items-center justify-center text-primary shrink-0">
          <Users className="h-5 w-5" />
        </div>
        <div>
          <h3 className="text-xs font-bold uppercase text-foreground tracking-wider">
            Shared Stewardship &amp; Local Connectivity
          </h3>
          <p className="text-xs font-medium text-muted-foreground mt-1 leading-relaxed">
            Under the Mangatarem Community-Based Tourism model, peer discoverability encourages
            tourists to experience multiple local spots. Aligning standards collectively strengthens
            the town&apos;s tourism ecosystem.
          </p>
        </div>
      </div>

      {loading ? (
        <div className="flex justify-center py-16">
          <Loader2 className="h-6 w-6 animate-spin text-muted-foreground" />
        </div>
      ) : peers.length > 0 ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {peers.map((peer) => (
            <Card key={peer.id} className="overflow-hidden border-border/60 hover:border-primary/30 transition-all flex flex-col justify-between">
              <div className="h-40 bg-gradient-to-br from-primary/10 via-primary/5 to-muted flex items-center justify-center">
                <Store className="h-10 w-10 text-primary/30" />
              </div>
              <CardContent className="p-5 flex-grow flex flex-col justify-between space-y-4">
                <div>
                  <h3 className="text-sm font-bold text-foreground leading-snug">{peer.name}</h3>
                  <p className="text-xs font-medium text-muted-foreground mt-1 flex items-center gap-1">
                    <MapPin className="h-3.5 w-3.5 shrink-0" /> {peer.address || "Mangatarem, Pangasinan"}
                  </p>
                  <div className="flex items-center gap-3 mt-3 flex-wrap">
                    {peer.rating_avg && peer.rating_avg > 0 && (
                      <div className="flex items-center gap-1">
                        <Star className="h-3.5 w-3.5 fill-amber-400 text-amber-400" />
                        <span className="text-xs font-bold text-foreground">{peer.rating_avg.toFixed(1)}</span>
                        <span className="text-[10px] font-medium text-muted-foreground">({peer.review_count ?? 0})</span>
                      </div>
                    )}
                    <Badge variant="secondary" className="text-[9px] py-0 px-1.5 uppercase">
                      {peer.price_range || "Moderate"}
                    </Badge>
                  </div>
                </div>
                <div className="pt-4 border-t border-border/40 flex items-center justify-between">
                  <span className="text-[9px] font-bold text-muted-foreground uppercase tracking-widest truncate max-w-[150px]">
                    {peer.barangay_name || peer.barangay || "Mangatarem"}
                  </span>
                  <Link
                    href={`/business/${peer.id}`}
                    target="_blank"
                    className="text-[10px] font-bold uppercase text-primary hover:text-emerald-600 transition-colors flex items-center gap-1 shrink-0"
                  >
                    Public Portal <ExternalLink className="h-3 w-3" />
                  </Link>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      ) : (
        <div className="text-center py-20 bg-card border border-border/50 rounded-3xl">
          <div className="inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-muted text-muted-foreground mb-4">
            <Users className="w-8 h-8" />
          </div>
          <h3 className="text-sm font-bold text-foreground">No peers registered</h3>
          <p className="text-xs font-medium text-muted-foreground mt-1 max-w-xs mx-auto">
            You are the pioneering trailblazer for this category in Mangatarem!
          </p>
        </div>
      )}
    </div>
  );
}
