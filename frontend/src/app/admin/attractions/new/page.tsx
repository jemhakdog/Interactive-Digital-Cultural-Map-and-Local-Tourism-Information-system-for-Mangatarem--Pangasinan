"use client";

import { useEffect } from "react";
import { useAuth } from "@/lib/auth";
import { useRouter } from "next/navigation";
import { Loader2, Plus } from "lucide-react";
import { AttractionForm } from "@/components/admin/attraction-form";

export default function NewAttractionPage() {
  const { user, loading: authLoading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!authLoading && (!user || user.role !== "admin")) router.push("/dashboard");
  }, [user, authLoading, router]);

  if (authLoading || !user) {
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
          <Plus className="h-5 w-5" />
        </div>
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Add Attraction</h1>
          <p className="text-muted-foreground text-sm mt-0.5">
            Create a new landmark in the Mangatarem archive
          </p>
        </div>
      </div>

      <div className="border rounded-xl border-border/50 p-6">
        <AttractionForm />
      </div>
    </div>
  );
}
