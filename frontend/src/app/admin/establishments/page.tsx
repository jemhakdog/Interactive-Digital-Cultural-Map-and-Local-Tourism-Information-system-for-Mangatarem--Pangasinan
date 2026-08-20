"use client";

import { useEffect, useState, useCallback } from "react";
import { useAuth } from "@/lib/auth";
import { useRouter } from "next/navigation";
import { fetchAPI, api } from "@/lib/api";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Loader2, Store, Check, X, Trash2 } from "lucide-react";

interface Establishment {
  id: number;
  name: string;
  type?: string;
  status?: string;
  barangay?: string | null;
  owner_name?: string | null;
  cover_image_url?: string | null;
  created_at?: string;
}

const TYPE_LABEL: Record<string, string> = {
  inn: "Inn",
  restaurant: "Restaurant",
  cafe: "Café",
  fastfood: "Fast Food",
};

const STATUS_CLASS: Record<string, string> = {
  pending: "bg-yellow-50 border-yellow-200 text-yellow-600",
  approved: "bg-sky-50 border-sky-200 text-sky-600",
  rejected: "bg-red-50 border-red-200 text-red-600",
};

export default function AdminEstablishmentsPage() {
  const { user, loading: authLoading } = useAuth();
  const router = useRouter();
  const [items, setItems] = useState<Establishment[]>([]);
  const [loading, setLoading] = useState(true);
  // TODO: FastAPI verify/approve endpoint not implemented yet — using local placeholder handlers.
  const [info, setInfo] = useState<string | null>(null);

  const load = useCallback(() => {
    return api
      .business()
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
      `Verification endpoint for "${est.name}" (${action}) is not implemented on the backend yet.`
    );
  };

  const handleDelete = async (est: Establishment) => {
    if (!window.confirm(`Delete "${est.name}"?`)) return;
    try {
      await fetchAPI(`/api/business/${est.id}`, { method: "DELETE" });
      setItems((prev) => prev.filter((e) => e.id !== est.id));
    } catch {
      setInfo(`Could not delete "${est.name}".`);
    }
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
          <Store className="h-5 w-5" />
        </div>
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Business Directory</h1>
          <p className="text-muted-foreground text-sm mt-0.5">
            {pending > 0 ? (
              <span className="text-amber-600 font-semibold">{pending} pending approval</span>
            ) : (
              "All caught up"
            )}
          </p>
        </div>
      </div>

      {info && (
        <div className="mb-4 rounded-lg border border-border bg-muted px-4 py-3 text-sm text-muted-foreground">
          {info}
        </div>
      )}

      {items.length === 0 ? (
        <div className="border border-dashed border-border rounded-2xl py-20 text-center">
          <Store className="h-12 w-12 mx-auto mb-3 text-muted-foreground/40" />
          <p className="font-bold text-foreground">No establishments yet</p>
          <p className="text-xs text-muted-foreground mt-1">
            Business listings will appear here once registered.
          </p>
        </div>
      ) : (
        <div className="flex flex-col gap-4">
          {items.map((est) => {
            const status = (est.status ?? "pending").toLowerCase();
            return (
              <div
                key={est.id}
                className="border border-border/50 rounded-2xl p-5 flex flex-col md:flex-row md:items-center justify-between gap-4"
              >
                <div className="flex items-center gap-4">
                  {est.cover_image_url ? (
                    // eslint-disable-next-line @next/next/no-img-element
                    <img
                      src={est.cover_image_url}
                      alt={est.name}
                      className="w-14 h-14 rounded-2xl object-cover border border-border"
                    />
                  ) : (
                    <div className="w-14 h-14 rounded-2xl bg-muted border border-border flex items-center justify-center text-xl">
                      {est.type === "inn" ? "🏨" : est.type === "restaurant" ? "🍽️" : est.type === "cafe" ? "☕" : est.type === "fastfood" ? "🍔" : "🏪"}
                    </div>
                  )}
                  <div>
                    <h3 className="font-bold text-foreground">{est.name}</h3>
                    <div className="flex flex-wrap items-center gap-2 text-xs text-muted-foreground mt-1">
                      <span className="text-primary bg-primary/10 px-2 py-0.5 rounded">
                        {TYPE_LABEL[est.type ?? ""] ?? est.type ?? "Business"}
                      </span>
                      {est.barangay && <span>Brgy. {est.barangay}</span>}
                      {est.owner_name && <span>Owner: {est.owner_name}</span>}
                    </div>
                  </div>
                </div>

                <div className="flex items-center gap-2 flex-shrink-0">
                  <Badge
                    variant="outline"
                    className={`text-xs capitalize ${STATUS_CLASS[status] ?? ""}`}
                  >
                    {status}
                  </Badge>
                  {status === "pending" && (
                    <>
                      <Button
                        size="sm"
                        className="gap-1 rounded-lg"
                        onClick={() => handleVerify(est, "approve")}
                      >
                        <Check className="h-3.5 w-3.5" /> Approve
                      </Button>
                      <Button
                        size="sm"
                        variant="outline"
                        className="gap-1 rounded-lg"
                        onClick={() => handleVerify(est, "reject")}
                      >
                        <X className="h-3.5 w-3.5" /> Reject
                      </Button>
                    </>
                  )}
                  <Button
                    size="icon"
                    variant="ghost"
                    className="h-8 w-8 text-destructive"
                    onClick={() => handleDelete(est)}
                  >
                    <Trash2 className="h-3.5 w-3.5" />
                  </Button>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
