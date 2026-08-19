import { notFound } from "next/navigation";
import Link from "next/link";
import { ArrowLeft, Calendar, MapPin } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { Separator } from "@/components/ui/separator";

async function getEvent(id: string) {
  try {
    const res = await fetch(`http://localhost:8000/api/events/${id}`, { next: { revalidate: 60 } });
    if (!res.ok) return null;
    return res.json();
  } catch { return null; }
}

export default async function EventDetailPage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = await params;
  const event = await getEvent(id);
  if (!event) notFound();

  return (
    <div className="container mx-auto px-4 py-8">
      <Link href="/events" className="inline-flex items-center gap-1 text-sm text-muted-foreground hover:text-foreground mb-6">
        <ArrowLeft className="h-4 w-4" /> Back to Events
      </Link>

      {event.image_url && (
        <div className="aspect-[21/9] bg-muted rounded-lg overflow-hidden mb-8">
          <img src={String(event.image_url)} alt={String(event.name)} className="w-full h-full object-cover" />
        </div>
      )}

      <div className="max-w-3xl">
        <h1 className="text-3xl font-bold">{String(event.name)}</h1>
        <div className="flex flex-wrap gap-2 mt-2">
          {event.category && <Badge variant="secondary">{String(event.category)}</Badge>}
          {event.barangay_name && <Badge variant="outline">{String(event.barangay_name)}</Badge>}
        </div>

        <div className="flex flex-wrap gap-4 mt-4 text-sm text-muted-foreground">
          {event.date && (
            <div className="flex items-center gap-1">
              <Calendar className="h-4 w-4" />
              {new Date(String(event.date)).toLocaleDateString("en-PH", { weekday: "long", month: "long", day: "numeric", year: "numeric" })}
            </div>
          )}
          {event.location && (
            <div className="flex items-center gap-1">
              <MapPin className="h-4 w-4" />
              {String(event.location)}
            </div>
          )}
        </div>

        {event.description && (
          <>
            <Separator className="my-6" />
            <p className="text-muted-foreground leading-relaxed">{String(event.description)}</p>
          </>
        )}
      </div>
    </div>
  );
}
