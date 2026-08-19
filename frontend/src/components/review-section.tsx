"use client";

import { ReviewForm } from "@/components/review-form";

export function ReviewSection({ attractionId }: { attractionId: number }) {
  return <ReviewForm attractionId={attractionId} />;
}
