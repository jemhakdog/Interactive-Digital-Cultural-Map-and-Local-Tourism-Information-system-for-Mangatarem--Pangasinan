"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useAuth } from "@/lib/auth";
import { fetchAPI } from "@/lib/api";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Loader2, Star, MessageSquareText, MapPin, Store } from "lucide-react";

interface MyReview {
  id: number | string;
  target_type?: string;
  target_name?: string;
  rating?: number;
  comment?: string;
  created_at?: string;
}

export default function MyReviewsPage() {
  const { user, loading: authLoading } = useAuth();
  const router = useRouter();
  const [reviews, setReviews] = useState<MyReview[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!authLoading && !user) router.push("/auth/login");
  }, [user, authLoading, router]);

  useEffect(() => {
    if (!user) return;
    // TODO: FastAPI endpoint for "my reviews" not implemented yet — using local placeholder state.
    fetchAPI<{ reviews?: MyReview[]; items?: MyReview[] }>("/api/reviews/me")
      .then((d) => setReviews((d?.reviews ?? d?.items ?? []) as MyReview[]))
      .catch(() => setReviews([]))
      .finally(() => setLoading(false));
  }, [user]);

  if (authLoading || !user) {
    return (
      <div className="flex justify-center py-16">
        <Loader2 className="h-6 w-6 animate-spin text-muted-foreground" />
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold tracking-tight">My Reviews</h1>
        <p className="text-muted-foreground mt-1">
          Reviews you've written across attractions and businesses
        </p>
      </div>

      {loading ? (
        <div className="flex justify-center py-16">
          <Loader2 className="h-6 w-6 animate-spin text-muted-foreground" />
        </div>
      ) : reviews.length === 0 ? (
        <Card>
          <CardContent className="p-8 text-center text-muted-foreground">
            <MessageSquareText className="h-12 w-12 mx-auto mb-4 opacity-30" />
            <p className="mb-4">You haven't written any reviews yet.</p>
            <div className="flex flex-wrap justify-center gap-3">
              <Link href="/attractions">
                <Button variant="outline" className="rounded-xl gap-2">
                  <MapPin className="h-4 w-4" /> Explore Attractions
                </Button>
              </Link>
              <Link href="/business">
                <Button variant="outline" className="rounded-xl gap-2">
                  <Store className="h-4 w-4" /> Browse Businesses
                </Button>
              </Link>
            </div>
          </CardContent>
        </Card>
      ) : (
        <div className="space-y-4">
          {reviews.map((r) => (
            <Card key={String(r.id)} className="border-border/50">
              <CardContent className="p-5">
                <div className="flex items-start justify-between gap-4">
                  <div>
                    <p className="font-semibold">{r.target_name ?? "Review"}</p>
                    {r.target_type && (
                      <Badge variant="secondary" className="mt-1 text-xs capitalize">
                        {r.target_type}
                      </Badge>
                    )}
                  </div>
                  <div className="flex items-center gap-0.5 shrink-0">
                    {[1, 2, 3, 4, 5].map((s) => (
                      <Star
                        key={s}
                        className={`h-4 w-4 ${
                          s <= (r.rating ?? 0) ? "fill-primary text-primary" : "text-muted-foreground"
                        }`}
                      />
                    ))}
                  </div>
                </div>
                {r.comment && (
                  <p className="text-sm text-muted-foreground mt-3 leading-relaxed">{r.comment}</p>
                )}
                {r.created_at && (
                  <p className="text-xs text-muted-foreground mt-2">
                    {new Date(r.created_at).toLocaleDateString()}
                  </p>
                )}
              </CardContent>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
}
