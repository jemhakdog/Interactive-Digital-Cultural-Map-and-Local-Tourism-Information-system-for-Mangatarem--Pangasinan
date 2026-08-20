"use client";

import { useEffect, useState } from "react";
import { useAuth } from "@/lib/auth";
import { useRouter, useParams } from "next/navigation";
import { fetchAPI } from "@/lib/api";
import { Loader2, Pencil } from "lucide-react";
import { HeritageForm, type HeritageFormValues } from "@/components/admin/heritage-form";

export default function EditHeritagePage() {
  const { user, loading: authLoading } = useAuth();
  const router = useRouter();
  const params = useParams();
  const type = String(params.type);
  const id = Number(params.id);

  const [initial, setInitial] = useState<Partial<HeritageFormValues> | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!authLoading && (!user || user.role !== "admin")) router.push("/dashboard");
  }, [user, authLoading, router]);

  useEffect(() => {
    if (!user || !id) return;
    fetchAPI(`/api/heritage/${type}/${id}`)
      .then((data) => setInitial(data as Partial<HeritageFormValues>))
      .catch(() => setInitial({}))
      .finally(() => setLoading(false));
  }, [user, type, id]);

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
          <h1 className="text-3xl font-bold tracking-tight capitalize">Edit {type} Heritage</h1>
          <p className="text-muted-foreground text-sm mt-0.5">
            Update the documentation for this record
          </p>
        </div>
      </div>

      <div className="border rounded-xl border-border/50 p-6">
        <HeritageForm type={type} id={id} initial={initial ?? undefined} />
      </div>
    </div>
  );
}
