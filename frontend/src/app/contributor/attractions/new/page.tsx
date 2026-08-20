import type { Metadata } from "next";
import Link from "next/link";
import { ArrowLeft } from "lucide-react";
import { Button } from "@/components/ui/button";
import { AttractionForm } from "@/components/contributor/attraction-form";

export const metadata: Metadata = {
  title: "Add Landmark",
};

export default function NewAttractionPage() {
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold tracking-tight">Add Community Landmark</h1>
          <p className="text-sm text-muted-foreground">Map a cultural asset under CBIS stewardship.</p>
        </div>
        <Link href="/contributor">
          <Button variant="outline" size="sm" className="gap-1.5 rounded-lg">
            <ArrowLeft className="h-4 w-4" /> Dashboard
          </Button>
        </Link>
      </div>
      <AttractionForm />
    </div>
  );
}
