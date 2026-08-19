import { notFound } from "next/navigation";
import Link from "next/link";
import { MapPin, ArrowLeft, Star } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { Separator } from "@/components/ui/separator";
import { ReviewSection } from "@/components/review-section";

async function getAttraction(id: string) {
  try {
    const res = await fetch(`http://localhost:8000/api/attractions/${id}`, { next: { revalidate: 60 } });
    if (!res.ok) return null;
    return res.json();
  } catch { return null; }
}

async function getReviews(id: string) {
  try {
    const res = await fetch(`http://localhost:8000/api/attractions/${id}/reviews`, { next: { revalidate: 60 } });
    if (!res.ok) return { reviews: [], summary: null };
    return res.json();
  } catch { return { reviews: [], summary: null }; }
}

export default async function AttractionDetailPage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = await params;
  const [attraction, reviewData] = await Promise.all([getAttraction(id), getReviews(id)]);

  if (!attraction) notFound();

  const attractionId = Number(id);

  return (
    <div className="container mx-auto px-4 py-8">
      <Link href="/attractions" className="inline-flex items-center gap-1 text-sm text-muted-foreground hover:text-foreground mb-6">
        <ArrowLeft className="h-4 w-4" /> Back to Attractions
      </Link>

      {/* Hero image */}
      {attraction.image_url && (
        <div className="aspect-[21/9] bg-muted rounded-lg overflow-hidden mb-8">
          <img src={String(attraction.image_url)} alt={String(attraction.name)} className="w-full h-full object-cover" />
        </div>
      )}

      <div className="max-w-3xl">
        <div className="flex items-start justify-between gap-4">
          <div>
            <h1 className="text-3xl font-bold">{String(attraction.name)}</h1>
            <div className="flex flex-wrap gap-2 mt-2">
              {attraction.category && <Badge variant="secondary">{String(attraction.category)}</Badge>}
              {attraction.barangay_name && <Badge variant="outline">{String(attraction.barangay_name)}</Badge>}
            </div>
          </div>
          {attraction.average_rating != null && (
            <div className="flex items-center gap-1 text-sm">
              <Star className="h-4 w-4 fill-primary text-primary" />
              <span className="font-semibold">{Number(attraction.average_rating).toFixed(1)}</span>
              {attraction.review_count != null && (
                <span className="text-muted-foreground">({attraction.review_count})</span>
              )}
            </div>
          )}
        </div>

        {attraction.description && (
          <p className="mt-6 text-muted-foreground leading-relaxed">{String(attraction.description)}</p>
        )}

        {attraction.latitude && attraction.longitude && (
          <div className="mt-4 flex items-center gap-2 text-sm text-muted-foreground">
            <MapPin className="h-4 w-4" />
            <span>{Number(attraction.latitude).toFixed(5)}, {Number(attraction.longitude).toFixed(5)}</span>
          </div>
        )}

        <Separator className="my-8" />

        {/* Reviews */}
        <h2 className="text-xl font-bold mb-4">Reviews</h2>

        {/* Review form */}
        <div className="mb-6">
          <ReviewSection attractionId={attractionId} />
        </div>

        {/* Existing reviews */}
        {reviewData.reviews.length > 0 && (
          <div className="space-y-4">
            {(reviewData.reviews as Record<string, unknown>[]).map((r, i) => (
              <div key={i} className="border rounded-lg p-4">
                <div className="flex items-center gap-2 mb-2">
                  <span className="font-medium text-sm">{String(r.user_name ?? "Anonymous")}</span>
                  {r.rating != null && (
                    <span className="text-xs text-primary">{"★".repeat(Number(r.rating))}</span>
                  )}
                </div>
                <p className="text-sm text-muted-foreground">{String(r.comment ?? "")}</p>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
