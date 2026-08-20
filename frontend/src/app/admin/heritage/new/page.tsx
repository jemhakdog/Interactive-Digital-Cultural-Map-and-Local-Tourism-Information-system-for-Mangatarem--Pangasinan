"use client";

import { useEffect, useState } from "react";
import { useAuth } from "@/lib/auth";
import { useRouter } from "next/navigation";
import { Loader2, Plus } from "lucide-react";
import { HeritageForm } from "@/components/admin/heritage-form";

const HERITAGE_TYPES = [
  { value: "built", label: "Built" },
  { value: "natural", label: "Natural" },
  { value: "intangible", label: "Intangible" },
  { value: "movable", label: "Movable" },
  { value: "mixed", label: "Mixed" },
];

export default function NewHeritagePage() {
  const { user, loading: authLoading } = useAuth();
  const router = useRouter();
  const [type, setType] = useState<string>("built");

  useEffect(() => {
    if (!authLoading && (!user || user.role !== "admin")) router.push("/dashboard");
  }, [user, authLoading, router]);

  useEffect(() => {
    // Read ?type= from the URL without useSearchParams (avoids Suspense requirement).
    const params = new URLSearchParams(window.location.search);
    const t = params.get("type");
    if (t && HERITAGE_TYPES.some((h) => h.value === t)) setType(t);
  }, []);

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
          <h1 className="text-3xl font-bold tracking-tight">Add Heritage Entry</h1>
          <p className="text-muted-foreground text-sm mt-0.5">
            Document a new record in the heritage archive
          </p>
        </div>
      </div>

      <div className="border rounded-xl border-border/50 p-6 space-y-4">
        <div className="space-y-2">
          <label className="block text-sm font-medium text-foreground">Heritage Type</label>
          <select
            value={type}
            onChange={(e) => setType(e.target.value)}
            className="w-full rounded-lg border border-border bg-background px-3 py-2 text-sm text-foreground outline-none focus:ring-2 focus:ring-primary/40"
          >
            {HERITAGE_TYPES.map((h) => (
              <option key={h.value} value={h.value}>
                {h.label}
              </option>
            ))}
          </select>
        </div>

        {/* key forces a fresh form when the type changes */}
        <HeritageForm key={type} type={type} />
      </div>
    </div>
  );
}
