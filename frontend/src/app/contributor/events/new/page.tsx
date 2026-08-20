import type { Metadata } from "next";
import Link from "next/link";
import { ArrowLeft } from "lucide-react";
import { Button } from "@/components/ui/button";
import { EventForm } from "@/components/contributor/event-form";

export const metadata: Metadata = {
  title: "Publish Event",
};

export default function NewEventPage() {
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold tracking-tight">Publish Local Event</h1>
          <p className="text-sm text-muted-foreground">CBIS tourism events for your barangay.</p>
        </div>
        <Link href="/contributor">
          <Button variant="outline" size="sm" className="gap-1.5 rounded-lg">
            <ArrowLeft className="h-4 w-4" /> Dashboard
          </Button>
        </Link>
      </div>
      <EventForm />
    </div>
  );
}
