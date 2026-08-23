import type { Metadata } from "next";
import { EventsView, EventItem } from "./events-view";
import { AdminManageBar } from "@/components/layout/admin-manage-bar";

export const metadata: Metadata = {
  title: "Events",
  description: "Upcoming events and festivals in Mangatarem, Pangasinan",
};

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

async function getEvents() {
  try {
    const res = await fetch(`${API_BASE}/api/events`, { next: { revalidate: 60 } });
    if (!res.ok) return { items: [] };
    return res.json();
  } catch {
    return { items: [] };
  }
}

export default async function EventsPage() {
  const data = await getEvents();
  const rawEvents = (data.events ?? data.items ?? []) as EventItem[];

  return (
    <div className="container mx-auto px-4 py-8">
      <AdminManageBar label="Events" href="/admin/events" />
      {/* ── Page Header ── */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold tracking-tight text-foreground">Events</h1>
        <p className="text-muted-foreground mt-1">What&apos;s happening in Mangatarem</p>
      </div>

      {/* ── Interactive Events Hub ── */}
      <EventsView events={rawEvents} />
    </div>
  );
}
