import type { Metadata } from "next";
import { Megaphone } from "lucide-react";
import { NewsletterSubscribe } from "@/components/public/newsletter-subscribe";

export const metadata: Metadata = {
  title: "Bulletins & Announcements",
  description:
    "Stay updated with the latest news, notices, and announcements from the Local Government Unit of Mangatarem and our 82 barangays.",
};

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

interface Announcement {
  id?: number;
  title: string;
  content?: string;
  author_name?: string;
  barangay_name?: string;
  barangay_id?: number | null;
  created_at?: string;
}

// TODO: FastAPI endpoint not implemented yet (no GET /api/announcements).
// Falling back to an empty bulletin board with a graceful empty state.
async function getAnnouncements(): Promise<Announcement[]> {
  try {
    const res = await fetch(`${API_BASE}/api/announcements`, { next: { revalidate: 120 } });
    if (!res.ok) return [];
    const data = await res.json();
    return (data.announcements ?? data.items ?? []) as Announcement[];
  } catch {
    return [];
  }
}

export default async function AnnouncementsPage() {
  const announcements = await getAnnouncements();

  return (
    <div className="container mx-auto px-4 py-8 sm:py-10 max-w-4xl space-y-10">
      {/* ── Header ── */}
      <div className="text-center space-y-3">
        <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-primary/10 text-primary text-xs font-semibold">
          <Megaphone className="h-3.5 w-3.5" />
          <span>Community Bulletin</span>
        </div>
        <h1 className="text-3xl sm:text-4xl font-extrabold tracking-tight text-foreground">
          Bulletins & Announcements
        </h1>
        <p className="text-muted-foreground text-sm sm:text-base leading-relaxed max-w-lg mx-auto">
          Official announcements, event updates, and news broadcasts from the central LGU
          Mangatarem and individual barangay offices.
        </p>
      </div>

      {/* ── Timeline ── */}
      <div className="relative border-l-2 border-primary/20 ml-3 md:ml-6 space-y-8">
        {announcements.length > 0 ? (
          announcements.map((ann) => {
            const isLGU = !ann.barangay_id;
            return (
              <div key={ann.id ?? ann.title} className="relative pl-8 md:pl-10">
                <div
                  className={`absolute -left-[9px] top-1.5 w-4 h-4 rounded-full border-4 border-background ${
                    isLGU ? "bg-primary shadow-[0_0_10px_rgba(22,163,74,0.4)]" : "bg-amber-500 shadow-[0_0_10px_rgba(245,158,11,0.4)]"
                  }`}
                />
                <div className="bg-card rounded-2xl p-6 border border-border/60 hover:border-primary/30 transition-colors">
                  <div className="flex flex-wrap items-center justify-between gap-3 mb-3">
                    <span
                      className={`text-[10px] font-extrabold uppercase tracking-widest px-2.5 py-1 rounded-md border ${
                        isLGU
                          ? "bg-primary/10 text-primary border-primary/20"
                          : "bg-amber-500/10 text-amber-700 dark:text-amber-300 border-amber-500/20"
                      }`}
                    >
                      {isLGU ? "LGU Official Notice" : `${ann.barangay_name ?? "Barangay"} Dispatch`}
                    </span>
                    {ann.created_at && (
                      <span className="text-xs text-muted-foreground">
                        {new Date(ann.created_at).toLocaleString("en-US", {
                          month: "long",
                          day: "numeric",
                          year: "numeric",
                        })}
                      </span>
                    )}
                  </div>
                  <h2 className="text-xl font-bold text-foreground mb-2 leading-tight">{ann.title}</h2>
                  {ann.content && (
                    <p className="text-sm text-muted-foreground leading-relaxed whitespace-pre-line">
                      {ann.content}
                    </p>
                  )}
                  <div className="border-t border-border/60 pt-3 mt-4 flex justify-between items-center text-xs text-muted-foreground">
                    <span>
                      Published by <strong>{ann.author_name ?? "LGU Mangatarem"}</strong>
                    </span>
                    <span className="font-semibold uppercase tracking-wider text-[10px] text-primary">
                      {ann.barangay_name ? `${ann.barangay_name} Office` : "Central LGU Office"}
                    </span>
                  </div>
                </div>
              </div>
            );
          })
        ) : (
          <div className="text-center py-16 bg-card border border-dashed border-border rounded-2xl">
            <Megaphone className="h-12 w-12 mx-auto text-muted-foreground/40 mb-4" />
            <p className="text-muted-foreground italic">
              There are no announcements posted on the bulletin board at the moment.
            </p>
          </div>
        )}
      </div>

      {/* ── Newsletter subscribe ── */}
      <div className="space-y-3">
        <h3 className="text-sm font-bold text-foreground uppercase tracking-wider">
          Stay in the loop
        </h3>
        <NewsletterSubscribe />
      </div>
    </div>
  );
}
