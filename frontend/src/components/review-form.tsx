"use client";

import { useState } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { reviewSchema, type ReviewInput } from "@/lib/validations";
import { fetchAPI } from "@/lib/api";
import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { Loader2, Star } from "lucide-react";

interface ReviewFormProps {
  attractionId: number;
  onReviewSubmitted?: () => void;
}

export function ReviewForm({ attractionId, onReviewSubmitted }: ReviewFormProps) {
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);
  const [error, setError] = useState("");
  const [hoveredStar, setHoveredStar] = useState(0);

  const { register, handleSubmit, formState: { errors }, setValue, watch } = useForm<ReviewInput>({
    resolver: zodResolver(reviewSchema),
    defaultValues: { rating: 0, comment: "" },
  });

  const rating = watch("rating");

  const onSubmit = async (data: ReviewInput) => {
    setLoading(true);
    setError("");
    try {
      await fetchAPI(`/api/attractions/${attractionId}/reviews`, {
        method: "POST",
        body: JSON.stringify(data),
      });
      setSuccess(true);
      onReviewSubmitted?.();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to submit review");
    } finally {
      setLoading(false);
    }
  };

  if (success) {
    return (
      <div className="bg-primary/10 text-primary rounded-lg p-4 text-center">
        <p className="font-medium">Review submitted! Thank you for your feedback.</p>
      </div>
    );
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-4 border rounded-lg p-4">
      <h3 className="font-semibold">Write a Review</h3>

      {error && (
        <div className="bg-destructive/10 text-destructive text-sm rounded-md px-3 py-2">
          {error}
        </div>
      )}

      <div className="space-y-2">
        <Label>Rating</Label>
        <div className="flex gap-1">
          {[1, 2, 3, 4, 5].map((star) => (
            <button
              key={star}
              type="button"
              onClick={() => setValue("rating", star, { shouldValidate: true })}
              onMouseEnter={() => setHoveredStar(star)}
              onMouseLeave={() => setHoveredStar(0)}
              className="p-0.5"
            >
              <Star
                className={`h-6 w-6 transition-colors ${
                  star <= (hoveredStar || rating)
                    ? "fill-primary text-primary"
                    : "text-muted-foreground"
                }`}
              />
            </button>
          ))}
        </div>
        {errors.rating && (
          <p className="text-sm text-destructive">{errors.rating.message}</p>
        )}
      </div>

      <div className="space-y-2">
        <Label htmlFor="comment">Your Review</Label>
        <Textarea
          id="comment"
          placeholder="Share your experience..."
          {...register("comment")}
          rows={3}
        />
        {errors.comment && (
          <p className="text-sm text-destructive">{errors.comment.message}</p>
        )}
      </div>

      <Button type="submit" disabled={loading}>
        {loading ? <Loader2 className="h-4 w-4 animate-spin mr-2" /> : null}
        Submit Review
      </Button>
    </form>
  );
}
