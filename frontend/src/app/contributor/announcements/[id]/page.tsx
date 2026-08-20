import type { Metadata } from "next";
import Link from "next/link";
import { ArrowLeft } from "lucide-react";
import { Button } from "@/components/ui/button";
import { AnnouncementForm } from "@/components/contributor/announcement-form";

export const metadata: Metadata = {
  title: "Edit Announcement",
};

export default async function EditAnnouncementPage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = await params;
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold tracking-tight">Edit Announcement</h1>
          <p className="text-sm text-muted-foreground">Update broadcast (ID {id}).</p>
        </div>
        <Link href="/contributor/announcements">
          <Button variant="outline" size="sm" className="gap-1.5 rounded-lg">
            <ArrowLeft className="h-4 w-4" /> Announcements
          </Button>
        </Link>
      </div>
      <AnnouncementForm id={id} />
    </div>
  );
}
