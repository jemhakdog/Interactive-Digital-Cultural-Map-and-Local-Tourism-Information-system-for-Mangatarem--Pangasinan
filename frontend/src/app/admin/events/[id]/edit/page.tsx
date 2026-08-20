"use client";

import { useEffect, useState } from "react";
import { useAuth } from "@/lib/auth";
import { useRouter, useParams } from "next/navigation";
import { fetchAPI } from "@/lib/api";
import { Loader2, Pencil } from "lucide-react";
import { EventForm, type EventFormValues } from "@/components/admin/event-form";

export default function EditEventPage() {
  const { user, loading: authLoading } = useAuth();
  const router = useRouter();
  const params = useParams();
  const id = Number(params.id);

  const [initial, setInitial] = useState<Partial<EventFormValues> | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!authLoading && (!user || user.role !== "admin")) router.push("/dashboard");
  }, [user, authLoading, router]);

  useEffect(() => {
    if (!user || !id) return;
    fetchAPI(`/api/events/${id}`)
      .then((data) => setInitial(data as Partial<EventFormValues>))
      .catch(() => setInitial({}))
      .finally(() => setLoading(false));
  }, [user, id]);

  if (authLoading || !user || loading) {
    return (
      <div className="flex justify-center py-16">
        <Loader2 className="h-6 w-6 animate-spin text-muted-foreground" />
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8 max-w-3xl">
      <div className="flex items-center gap-3 mb-6">
        <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-primary/10 text-primary">
          <Pencil className="h-5 w-5" />
        </div>
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Edit Event</h1>
          <p className="text-muted-foreground text-sm mt-0.5">
            Update the narrative and metadata for this event
          </p>
        </div>
      </div>

      <div className="border rounded-xl border-border/50 p-6">
        <EventForm id={id} initial={initial ?? undefined} />
      </div>
    </div>
  );
}
