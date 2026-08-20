"use client";

import { useEffect, useState, useCallback } from "react";
import { useAuth } from "@/lib/auth";
import { useRouter } from "next/navigation";
import { api } from "@/lib/api";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Loader2, BadgeCheck, X } from "lucide-react";

interface Establishment {
  id: number;
  name: string;
  type?: string;
  barangay?: string | null;
  owner_name?: string | null;
  status?: string;
}

export default function AdminVerifyMerchantsPage() {
  const { user, loading: authLoading } = useAuth();
  const router = useRouter();
  const [items, setItems] = useState<Establishment[]>([]);
  const [loading, setLoading] = useState(true);
  // TODO: FastAPI merchant-verification endpoint not implemented yet — using local placeholder handlers.
  const [info, setInfo] = useState<string | null>(null);

  const load = useCallback(() => {
    return api
      .business("status=pending")
      .then((data) => setItems((data.items as Establishment[]) ?? []))
      .catch(() => {});
  }, []);

  useEffect(() => {
    if (!authLoading && (!user || user.role !== "admin")) router.push("/dashboard");
  }, [user, authLoading, router]);

  useEffect(() => {
    if (!user) return;
    load().finally(() => setLoading(false));
  }, [user, load]);

  // Placeholder handler — backend verification endpoint is missing.
  const handleVerify = (est: Establishment, action: "approve" | "reject") => {
    setInfo(
      `Verification for "${est.name}" (${action}) is not implemented on the backend yet.`
    );
  };

  if (authLoading || !user || loading) {
    return (
      <div className="flex justify-center py-16">
        <Loader2 className="h-6 w-6 animate-spin text-muted-foreground" />
      </div>
    );
  }

  const pending = items.filter((e) => e.status === "pending").length;

  return (
    <div className="container mx-auto px-4 py-8 max-w-5xl">
      <div className="flex items-center gap-3 mb-6">
        <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-primary/10 text-primary">
          <BadgeCheck className="h-5 w-5" />
        </div>
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Verify Merchants</h1>
          <p className="text-muted-foreground text-sm mt-0.5">
            Approve or reject business registration requests
          </p>
        </div>
      </div>

      {info && (
        <div className="mb-4 rounded-lg border border-border bg-muted px-4 py-3 text-sm text-muted-foreground">
          {info}
        </div>
      )}

      {pending === 0 ? (
        <div className="border border-dashed border-border rounded-2xl py-20 text-center">
          <BadgeCheck className="h-12 w-12 mx-auto mb-3 text-muted-foreground/40" />
          <p className="font-bold text-foreground">No pending merchants</p>
          <p className="text-xs text-muted-foreground mt-1">
            You&apos;re all caught up — no business listings are waiting for review.
          </p>
        </div>
      ) : (
        <div className="flex flex-col gap-4">
          {items.map((est) => (
            <div
              key={est.id}
              className="border border-border/50 rounded-2xl p-5 flex flex-col md:flex-row md:items-center justify-between gap-4"
            >
              <div>
                <h3 className="font-bold text-foreground">{est.name}</h3>
                <div className="flex flex-wrap items-center gap-2 text-xs text-muted-foreground mt-1">
                  <Badge variant="secondary" className="capitalize">{est.type ?? "Business"}</Badge>
                  {est.barangay && <span>Brgy. {est.barangay}</span>}
                  {est.owner_name && <span>Owner: {est.owner_name}</span>}
                </div>
              </div>
              <div className="flex items-center gap-2 flex-shrink-0">
                <Button className="gap-1 rounded-lg" onClick={() => handleVerify(est, "approve")}>
                  <BadgeCheck className="h-3.5 w-3.5" /> Approve
                </Button>
                <Button
                  variant="outline"
                  className="gap-1 rounded-lg text-destructive"
                  onClick={() => handleVerify(est, "reject")}
                >
                  <X className="h-3.5 w-3.5" /> Reject
                </Button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
