import type { Metadata } from "next";
import Link from "next/link";
import { ArrowLeft } from "lucide-react";
import { Button } from "@/components/ui/button";
import { AttractionForm } from "@/components/contributor/attraction-form";

export const metadata: Metadata = {
  title: "Edit Landmark",
};

export default async function EditAttractionPage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = await params;
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold tracking-tight">Refine Landmark Details</h1>
          <p className="text-sm text-muted-foreground">Update asset records (ID {id}).</p>
        </div>
        <Link href="/contributor">
          <Button variant="outline" size="sm" className="gap-1.5 rounded-lg">
            <ArrowLeft className="h-4 w-4" /> Dashboard
          </Button>
        </Link>
      </div>
      <AttractionForm id={id} />
    </div>
  );
}
