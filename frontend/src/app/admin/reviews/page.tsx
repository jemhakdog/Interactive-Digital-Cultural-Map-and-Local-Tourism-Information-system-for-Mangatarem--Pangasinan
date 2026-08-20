"use client";

import { useEffect, useState } from "react";
import { useAuth } from "@/lib/auth";
import { useRouter } from "next/navigation";
import { Loader2, MessageSquare, Star, Check, X } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";

interface Review {
  id: number;
  user_name: string;
  rating?: number;
  comment?: string;
  status: string;
  location?: string;
  created_at?: string;
}

const FILTERS = ["pending", "approved", "all"] as const;

const STATUS_CLASS: Record<string, string> = {
  pending: "bg-yellow-50 border-yellow-200 text-yellow-600",
  approved: "bg-sky-50 border-sky-200 text-sky-600",
  rejected: "bg-red-50 border-red-200 text-red-600",
};

export default function AdminReviewsPage() {
  const { user, loading: authLoading } = useAuth();
  const router = useRouter();
  // TODO: FastAPI admin review-moderation endpoint not implemented yet — using local placeholder state.
  const [reviews] = useState<Review[]>([]);
  const [filter, setFilter] = useState<(typeof FILTERS)[number]>("all");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!authLoading && (!user || user.role !== "admin")) router.push("/dashboard");
  }, [user, authLoading, router]);

  useEffect(() => {
    if (!user) return;
    // No moderation read endpoint exists yet; placeholder list stays empty.
    setLoading(false);
  }, [user]);

  if (authLoading || !user || loading) {
    return (
      <div className="flex justify-center py-16">
        <Loader2 className="h-6 w-6 animate-spin text-muted-foreground" />
      </div>
    );
  }

  const pending = reviews.filter((r) => r.status === "pending").length;

  return (
    <div className="container mx-auto px-4 py-8 max-w-5xl space-y-6">
      <div className="flex items-center gap-3">
        <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-primary/10 text-primary">
          <MessageSquare className="h-5 w-5" />
        </div>
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Review Moderation</h1>
          <p className="text-muted-foreground text-sm mt-0.5">
            Manage visitor reviews and comments for all locations
          </p>
        </div>
      </div>

      <div className="flex gap-2 flex-wrap">
        {FILTERS.map((f) => (
          <button
            key={f}
            onClick={() => setFilter(f)}
            className={`px-5 py-2.5 rounded-2xl font-black text-[10px] uppercase tracking-wider transition-all border ${
              filter === f
                ? "bg-primary border-primary text-primary-foreground shadow-md shadow-primary/10"
                : "bg-muted border-border text-muted-foreground hover:bg-muted/70"
            }`}
          >
            {f}
            {f === "pending" && pending > 0 && (
              <span className="ml-1.5 bg-yellow-500 text-white text-[9px] px-2 py-0.5 rounded-full">
                {pending}
              </span>
            )}
          </button>
        ))}
      </div>

      {reviews.length === 0 ? (
        <div className="border border-dashed border-border rounded-2xl py-20 text-center">
          <MessageSquare className="h-12 w-12 mx-auto mb-3 text-muted-foreground/40" />
          <p className="font-bold text-foreground">No reviews found</p>
          <p className="text-xs text-muted-foreground mt-1">
            Review moderation requires a backend endpoint that is not implemented yet.
          </p>
        </div>
      ) : (
        <div className="flex flex-col gap-4">
          {reviews
            .filter((r) => filter === "all" || r.status === filter)
            .map((r) => (
              <div key={r.id} className="border border-border/50 rounded-2xl p-5">
                <div className="flex items-start justify-between gap-4">
                  <div>
                    <div className="flex items-center gap-2">
                      <span className="font-bold text-foreground">{r.user_name}</span>
                      {r.rating ? (
                        <span className="flex items-center gap-0.5 text-amber-500">
                          {Array.from({ length: r.rating }).map((_, i) => (
                            <Star key={i} className="h-3.5 w-3.5 fill-current" />
                          ))}
                        </span>
                      ) : null}
                      <Badge
                        variant="outline"
                        className={`text-[8px] font-black uppercase tracking-wider ${STATUS_CLASS[r.status] ?? ""}`}
                      >
                        {r.status}
                      </Badge>
                    </div>
                    {r.location && (
                      <p className="text-xs text-muted-foreground mt-1">{r.location}</p>
                    )}
                    {r.comment && <p className="text-sm text-foreground mt-2">{r.comment}</p>}
                  </div>
                  <div className="flex gap-2 flex-shrink-0">
                    <Button size="sm" className="gap-1 rounded-lg">
                      <Check className="h-3.5 w-3.5" /> Approve
                    </Button>
                    <Button
                      size="sm"
                      variant="outline"
                      className="gap-1 rounded-lg text-destructive"
                    >
                      <X className="h-3.5 w-3.5" /> Reject
                    </Button>
                  </div>
                </div>
              </div>
            ))}
        </div>
      )}
    </div>
  );
}
