import { NewsletterSubscribe } from "@/components/public/newsletter-subscribe";
import { LandingClient } from "./landing-client";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

async function getHome() {
  try {
    const res = await fetch(`${API_BASE}/api/`, { next: { revalidate: 60 } });
    if (!res.ok) return { featured_attractions: [], featured_events: [] };
    return res.json();
  } catch {
    return { featured_attractions: [], featured_events: [] };
  }
}

export default async function HomePage() {
  const data = await getHome();
  const attractions = (data.featured_attractions ?? []) as {
    id: number;
    name: string;
    category?: string;
    image_url?: string;
    barangay_name?: string;
    average_rating?: number;
  }[];
  const events = (data.featured_events ?? []) as {
    id: number;
    name: string;
    category?: string;
    date?: string;
    image_url?: string;
    barangay_name?: string;
  }[];

  return <LandingClient attractions={attractions} events={events} />;
}
