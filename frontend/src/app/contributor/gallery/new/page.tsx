import type { Metadata } from "next";
import Link from "next/link";
import { ArrowLeft } from "lucide-react";
import { Button } from "@/components/ui/button";
import { GalleryForm } from "@/components/contributor/gallery-form";

export const metadata: Metadata = {
  title: "Add Media",
};

export default function NewGalleryPage() {
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold tracking-tight">Upload Gallery Item</h1>
          <p className="text-sm text-muted-foreground">Add visual assets to your barangay gallery catalog.</p>
        </div>
        <Link href="/contributor">
          <Button variant="outline" size="sm" className="gap-1.5 rounded-lg">
            <ArrowLeft className="h-4 w-4" /> Dashboard
          </Button>
        </Link>
      </div>
      <GalleryForm />
    </div>
  );
}
