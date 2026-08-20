"use client";

import { useEffect, useState } from "react";
import { useAuth } from "@/lib/auth";
import { useRouter, useParams } from "next/navigation";
import { fetchAPI } from "@/lib/api";
import { Loader2, Pencil } from "lucide-react";
import { AttractionForm, type AttractionFormValues } from "@/components/admin/attraction-form";

export default function EditAttractionPage() {
  const { user, loading: authLoading } = useAuth();
  const router = useRouter();
  const params = useParams();
  const id = Number(params.id);

  const [initial, setInitial] = useState<Partial<AttractionFormValues> | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!authLoading && (!user || user.role !== "admin")) router.push("/dashboard");
  }, [user, authLoading, router]);

  useEffect(() => {
    if (!user || !id) return;
    fetchAPI(`/api/attractions/${id}`)
      .then((data) => setInitial(data as Partial<AttractionFormValues>))
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
          <h1 className="text-3xl font-bold tracking-tight">Edit Attraction</h1>
          <p className="text-muted-foreground text-sm mt-0.5">
            Update details for this landmark
          </p>
        </div>
      </div>

      <div className="border rounded-xl border-border/50 p-6">
        <AttractionForm id={id} initial={initial ?? undefined} />
      </div>
    </div>
  );
}
