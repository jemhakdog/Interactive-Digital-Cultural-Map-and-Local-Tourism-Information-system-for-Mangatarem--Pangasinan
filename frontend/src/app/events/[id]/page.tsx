import { notFound } from "next/navigation";
import type { Metadata } from "next";
import { EventDetailView } from "./event-detail-view";
import { EventItem } from "../events-view";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

async function getEvent(id: string): Promise<EventItem | null> {
  try {
    const res = await fetch(`${API_BASE}/api/events/${id}`, { next: { revalidate: 60 } });
    if (!res.ok) return null;
    return res.json();
  } catch {
    return null;
  }
}

async function getAllEvents(): Promise<EventItem[]> {
  try {
    const res = await fetch(`${API_BASE}/api/events`, { next: { revalidate: 60 } });
    if (!res.ok) return [];
    const data = await res.json();
    return (data.events ?? data.items ?? []) as EventItem[];
  } catch {
    return [];
  }
}

export async function generateMetadata({
  params,
}: {
  params: Promise<{ id: string }>;
}): Promise<Metadata> {
  const { id } = await params;
  const event = await getEvent(id);
  if (!event) {
    return {
      title: "Event Not Found",
    };
  }
  return {
    title: `${event.name} | Mangatarem Tourism`,
    description: event.description || `Details about ${event.name} in Mangatarem, Pangasinan.`,
  };
}

export default async function EventDetailPage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = await params;
  const [event, allEvents] = await Promise.all([getEvent(id), getAllEvents()]);

  if (!event) notFound();

  // Filter out current event from related
  const relatedEvents = allEvents.filter((e) => String(e.id) !== id);

  return (
    <div className="container mx-auto px-4 py-8">
      <EventDetailView event={event} relatedEvents={relatedEvents} />
    </div>
  );
}
