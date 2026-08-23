"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { useParams } from "next/navigation";
import { useAuth } from "@/lib/auth";
import { fetchAPI } from "@/lib/api";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Textarea } from "@/components/ui/textarea";
import { BusinessLayout } from "@/components/business/business-layout";
import { Loader2, ArrowLeft, MessageSquare, ShieldCheck, Star, Send } from "lucide-react";

interface ReviewReplyItem {
  id: number;
  username?: string;
  comment?: string;
  created_at?: string | null;
}

interface ReviewItem {
  id: number;
  username?: string;
  rating?: number | null;
  comment?: string | null;
  status?: string;
  created_at?: string | null;
  replies?: ReviewReplyItem[];
}

export default function BusinessReviewsPage() {
  const params = useParams<{ id: string }>();
  const id = params.id;
  const { user, loading: authLoading } = useAuth();

  const [estName, setEstName] = useState("");
  const [reviews, setReviews] = useState<ReviewItem[]>([]);
  const [loading, setLoading] = useState(true);

  const [replyTo, setReplyTo] = useState<number | null>(null);
  const [replyText, setReplyText] = useState("");
  const [sending, setSending] = useState(false);

  const load = async () => {
    try {
      // TODO: FastAPI has no owner-scoped "list all reviews" endpoint. Reusing the
      // public detail payload (approved reviews only) as a placeholder source.
      const data = await fetchAPI<{ establishment?: { name?: string }; reviews?: ReviewItem[] }>(
        `/api/business/${id}`
      );
      setEstName(data.establishment?.name ?? "");
      setReviews(data.reviews ?? []);
    } catch {
      setReviews([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (authLoading || !user) return;
    load();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [user, authLoading, id]);

  const handleReply = async (reviewId: number) => {
    if (!replyText.trim()) return;
    setSending(true);
    try {
      await fetchAPI(`/api/business/reviews/${reviewId}/reply`, {
        method: "POST",
        body: JSON.stringify({ comment: replyText }),
      });
      setReplyText("");
      setReplyTo(null);
      await load();
    } catch {
      /* graceful */
    } finally {
      setSending(false);
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center py-16">
        <Loader2 className="h-6 w-6 animate-spin text-muted-foreground" />
      </div>
    );
  }

  return (
    <BusinessLayout>
      <div className="container mx-auto px-4 py-8 max-w-4xl space-y-8">
      <div className="flex items-center justify-between pb-4 border-b border-border/50">
        <div className="space-y-1">
          <Link
            href="/business/dashboard"
            className="text-xs font-bold uppercase tracking-wider text-muted-foreground hover:text-foreground flex items-center gap-1.5 transition-colors"
          >
            <ArrowLeft className="h-3.5 w-3.5" /> Back to Dashboard
          </Link>
          <h1 className="text-xl font-bold tracking-tight text-foreground mt-2">Customer Testimonials</h1>
          <p className="text-[11px] font-bold text-muted-foreground uppercase tracking-wider">
            {estName || "Your establishment"} — {reviews.length} reviews registered
          </p>
        </div>
      </div>

      {reviews.length > 0 ? (
        <div className="space-y-4">
          {reviews.map((review) => (
            <Card key={review.id} className="p-6 border-border/60 flex items-start gap-4">
              <div className="w-10 h-10 rounded-xl bg-primary/10 flex items-center justify-center font-bold text-primary shrink-0">
                {(review.username || "V")[0].toUpperCase()}
              </div>
              <div className="flex-grow space-y-2">
                <div className="flex items-start justify-between gap-4 flex-wrap">
                  <div>
                    <h3 className="text-xs font-bold text-foreground">{review.username || "Anonymous Visitor"}</h3>
                    <p className="text-[9px] font-bold text-muted-foreground uppercase tracking-wider">
                      {review.created_at
                        ? new Date(review.created_at).toLocaleDateString("en-PH", {
                            month: "short",
                            day: "numeric",
                            year: "numeric",
                          })
                        : "Verified Guest"}
                    </p>
                  </div>
                  <div className="flex items-center gap-2">
                    <span className={`px-2 py-0.5 text-[8px] font-bold uppercase rounded ${
                      review.status === "approved"
                        ? "bg-emerald-500/10 text-emerald-600"
                        : review.status === "pending"
                        ? "bg-amber-500/10 text-amber-600"
                        : "bg-destructive/10 text-destructive"
                    }`}>
                      {review.status}
                    </span>
                    <div className="flex items-center text-amber-500 text-xs">
                      {[1, 2, 3, 4, 5].map((s) => (
                        <Star key={s} className={`h-3 w-3 ${s <= (review.rating ?? 0) ? "fill-amber-400 text-amber-400" : "text-muted-foreground/20"}`} />
                      ))}
                    </div>
                  </div>
                </div>

                {review.comment ? (
                  <p className="text-xs font-medium text-muted-foreground leading-relaxed border-t border-border/40 pt-2.5">
                    {review.comment}
                  </p>
                ) : (
                  <p className="text-xs font-medium text-muted-foreground italic pt-2.5">
                    No comments written. Checked in with a {review.rating}-star rating.
                  </p>
                )}

                {review.replies && review.replies.length > 0 && (
                  <div className="mt-4 pt-4 border-t border-border/40 pl-4 space-y-3">
                    <p className="text-[9px] font-bold text-muted-foreground uppercase tracking-wider mb-2">
                      Establishment Responses:
                    </p>
                    {review.replies.map((reply) => (
                      <div key={reply.id} className="bg-muted/50 p-4 rounded-2xl border border-border/40 flex items-start gap-3">
                        <div className="w-8 h-8 rounded-lg bg-primary/10 text-primary flex items-center justify-center font-bold text-xs shrink-0">
                          {(reply.username || "O")[0].toUpperCase()}
                        </div>
                        <div className="flex-grow space-y-1">
                          <div className="flex items-center gap-2">
                            <span className="text-xs font-bold text-foreground">{reply.username || "Business Owner"}</span>
                            <span className="text-[9px] font-bold text-muted-foreground uppercase tracking-wider">
                              {reply.created_at
                                ? new Date(reply.created_at).toLocaleDateString("en-PH", { month: "short", day: "numeric", year: "numeric" })
                                : ""}
                            </span>
                          </div>
                          <p className="text-xs font-medium text-muted-foreground leading-relaxed pt-1">{reply.comment}</p>
                        </div>
                      </div>
                    ))}
                  </div>
                )}

                <div className="mt-4 pt-3 flex justify-end">
                  <Button
                    variant="outline"
                    size="sm"
                    className="gap-1.5 rounded-xl text-xs"
                    onClick={() => setReplyTo(replyTo === review.id ? null : review.id)}
                  >
                    <ShieldCheck className="h-3.5 w-3.5" /> Respond
                  </Button>
                </div>

                {replyTo === review.id && (
                  <div className="mt-3 pt-3 border-t border-border/40 rounded-2xl p-3 bg-muted/30 space-y-3">
                    <Textarea
                      value={replyText}
                      onChange={(e) => setReplyText(e.target.value)}
                      rows={3}
                      placeholder="Write a welcoming response to this testimonial..."
                      className="rounded-xl"
                    />
                    <div className="flex justify-end gap-2">
                      <Button variant="ghost" size="sm" className="rounded-xl text-xs" onClick={() => setReplyTo(null)}>
                        Cancel
                      </Button>
                      <Button size="sm" className="gap-1.5 rounded-xl text-xs" disabled={sending} onClick={() => handleReply(review.id)}>
                        {sending ? <Loader2 className="h-3.5 w-3.5 animate-spin" /> : <Send className="h-3.5 w-3.5" />}
                        Submit Response
                      </Button>
                    </div>
                  </div>
                )}
              </div>
            </Card>
          ))}
        </div>
      ) : (
        <div className="text-center py-20 bg-card border border-border/50 rounded-3xl">
          <div className="inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-muted text-muted-foreground mb-4">
            <MessageSquare className="w-8 h-8" />
          </div>
          <h3 className="text-sm font-bold text-foreground">No customer testimonials</h3>
          <p className="text-xs font-medium text-muted-foreground mt-1 max-w-xs mx-auto">
            Your customers&apos; reviews and rating metrics will populate here once they share their experiences.
          </p>
        </div>
      )}
    </div>
    </BusinessLayout>
  );
}
