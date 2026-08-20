"use client";

import { useEffect, useState } from "react";
import { fetchAPI } from "@/lib/api";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Loader2, MessageSquare, Star } from "lucide-react";
import type { Review } from "@/components/contributor/types";

export default function ContributorReviewsPage() {
  const [reviews, setReviews] = useState<Review[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let cancelled = false;
    (async () => {
      try {
        // TODO: FastAPI endpoint not implemented yet — using local placeholder state.
        const data = await fetchAPI<{ items?: Review[] }>("/api/contributor/reviews");
        if (!cancelled) setReviews(data.items ?? []);
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

  const rated = reviews.filter((r) => r.rating != null);
  const avg = rated.length
    ? (rated.reduce((s, r) => s + (r.rating ?? 0), 0) / rated.length).toFixed(1)
    : "0.0";

  return (
    <div className="space-y-6 max-w-4xl">
      <div>
        <h1 className="text-2xl font-bold tracking-tight">Attraction Feedback &amp; Testimonials</h1>
        <p className="text-sm text-muted-foreground">{reviews.length} reviews registered</p>
      </div>

      {!loading && rated.length > 0 && (
        <Card className="border-border/50">
          <CardContent className="p-6 grid grid-cols-1 md:grid-cols-3 gap-6 items-center">
            <div className="text-center md:border-r md:border-border">
              <p className="text-5xl font-bold tracking-tight">{avg}</p>
              <div className="flex justify-center mt-2 text-primary">
                {[1, 2, 3, 4, 5].map((i) => (
                  <Star
                    key={i}
                    className={`h-4 w-4 ${i <= Math.round(Number(avg)) ? "fill-primary" : "text-muted-foreground"}`}
                  />
                ))}
              </div>
              <p className="text-[11px] uppercase tracking-wider text-muted-foreground mt-2">Average Rating</p>
            </div>
            <div className="md:col-span-2 space-y-2">
              <h3 className="text-xs font-semibold uppercase tracking-wider mb-2">Rating Distribution</h3>
              {[5, 4, 3, 2, 1].map((star) => {
                const count = rated.filter((r) => r.rating === star).length;
                const pct = rated.length ? Math.round((count / rated.length) * 100) : 0;
                return (
                  <div key={star} className="flex items-center gap-3 text-[11px] text-muted-foreground">
                    <span className="w-10 text-right">{star} Star</span>
                    <div className="flex-grow h-2 bg-muted rounded-full overflow-hidden">
                      <div className="h-full bg-primary rounded-full" style={{ width: `${pct}%` }} />
                    </div>
                    <span className="w-8 text-right">{count}</span>
                  </div>
                );
              })}
            </div>
          </CardContent>
        </Card>
      )}

      {loading ? (
        <div className="flex justify-center py-12">
          <Loader2 className="h-5 w-5 animate-spin text-muted-foreground" />
        </div>
      ) : reviews.length > 0 ? (
        <div className="space-y-4">
          {reviews.map((review) => (
            <ReviewCard key={review.id} review={review} />
          ))}
        </div>
      ) : (
        <Card className="border-border/50">
          <CardContent className="py-16 text-center">
            <div className="inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-muted text-muted-foreground mb-4">
              <MessageSquare className="h-7 w-7" />
            </div>
            <h3 className="text-sm font-semibold">No Visitor Feedback Yet</h3>
            <p className="text-xs text-muted-foreground mt-1 max-w-xs mx-auto">
              Reviews and rating metrics left by visitors on your mapped barangay attractions will appear here.
            </p>
          </CardContent>
        </Card>
      )}
    </div>
  );
}

function ReviewCard({ review }: { review: Review }) {
  const [replying, setReplying] = useState(false);
  const [comment, setComment] = useState("");
  const [busy, setBusy] = useState(false);

  async function submitReply(e: React.FormEvent) {
    e.preventDefault();
    setBusy(true);
    try {
      // TODO: FastAPI endpoint not implemented yet — contributor reply endpoint missing.
      await fetchAPI(`/api/contributor/reviews/${review.id}/reply`, {
        method: "POST",
        body: JSON.stringify({ comment }),
      });
      setReplying(false);
      setComment("");
    } catch {
      /* keep local */
    } finally {
      setBusy(false);
    }
  }

  return (
    <Card className="border-border/50">
      <CardContent className="p-6 flex items-start gap-4">
        <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-primary/10 text-primary font-semibold shrink-0">
          {(review.user?.username ?? "V")[0]?.toUpperCase()}
        </div>
        <div className="flex-grow space-y-2">
          <div className="flex items-start justify-between gap-4 flex-wrap">
            <div>
              <h3 className="text-sm font-semibold">{review.user?.username ?? "Anonymous Visitor"}</h3>
              <p className="text-[10px] uppercase tracking-wider text-muted-foreground">{review.created_at ?? ""}</p>
            </div>
            <div className="flex items-center text-primary">
              {[1, 2, 3, 4, 5].map((i) => (
                <Star
                  key={i}
                  className={`h-3.5 w-3.5 ${i <= (review.rating ?? 0) ? "fill-primary" : "text-muted-foreground"}`}
                />
              ))}
            </div>
          </div>
          {review.attraction?.name && (
            <div className="inline-flex items-center gap-1 bg-muted text-[10px] font-semibold px-2 py-1 rounded-lg">
              <span className="uppercase tracking-wider text-muted-foreground">Landmark:</span>
              <span className="text-foreground">{review.attraction.name}</span>
            </div>
          )}
          {review.comment && <p className="text-sm text-muted-foreground leading-relaxed">{review.comment}</p>}
          <div className="flex justify-end">
            <Button
              variant="ghost"
              size="sm"
              onClick={() => setReplying((v) => !v)}
              className="gap-1.5 rounded-lg"
            >
              <MessageSquare className="h-3.5 w-3.5" /> Respond
            </Button>
          </div>
          {replying && (
            <form onSubmit={submitReply} className="space-y-3 pt-3 border-t border-border">
              <textarea
                value={comment}
                onChange={(e) => setComment(e.target.value)}
                required
                rows={3}
                placeholder="Write a professional, welcoming response..."
                className="w-full rounded-lg border border-input bg-transparent p-3 text-sm outline-none focus-visible:border-ring focus-visible:ring-3 focus-visible:ring-ring/50"
              />
              <div className="flex justify-end gap-2">
                <Button type="button" variant="ghost" size="sm" onClick={() => setReplying(false)} className="rounded-lg">
                  Cancel
                </Button>
                <Button type="submit" size="sm" disabled={busy} className="rounded-lg">
                  {busy ? "Sending..." : "Submit Response"}
                </Button>
              </div>
            </form>
          )}
        </div>
      </CardContent>
    </Card>
  );
}
