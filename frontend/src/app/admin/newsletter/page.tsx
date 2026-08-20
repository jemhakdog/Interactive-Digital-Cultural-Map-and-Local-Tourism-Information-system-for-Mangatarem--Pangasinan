"use client";

import { useEffect, useState } from "react";
import { useAuth } from "@/lib/auth";
import { useRouter } from "next/navigation";
import { Loader2, Mail, PenSquare, History, Download, Trash2 } from "lucide-react";
import { Button } from "@/components/ui/button";

interface Subscriber {
  id: number;
  email: string;
  is_active: boolean;
  created_at: string;
}

export default function AdminNewsletterPage() {
  const { user, loading: authLoading } = useAuth();
  const router = useRouter();
  // TODO: FastAPI newsletter management (admin send/list/unsubscribe) not implemented yet — using local placeholder state.
  const [subscribers] = useState<Subscriber[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!authLoading && (!user || user.role !== "admin")) router.push("/dashboard");
  }, [user, authLoading, router]);

  useEffect(() => {
    if (!user) return;
    // No admin subscriber list endpoint exists yet; placeholder list stays empty.
    setLoading(false);
  }, [user]);

  if (authLoading || !user || loading) {
    return (
      <div className="flex justify-center py-16">
        <Loader2 className="h-6 w-6 animate-spin text-muted-foreground" />
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8 max-w-5xl space-y-8">
      <div className="flex items-center gap-3">
        <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-primary/10 text-primary">
          <Mail className="h-5 w-5" />
        </div>
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Newsletter Center</h1>
          <p className="text-muted-foreground text-sm mt-0.5">
            Reach out to subscribers with updates and features
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="border rounded-3xl border-border/50 p-6 flex flex-col justify-between">
          <div className="p-3 bg-primary/10 text-primary rounded-2xl w-fit">
            <Mail className="h-6 w-6" />
          </div>
          <div className="mt-4">
            <p className="text-3xl font-black text-foreground tracking-tight leading-none">
              {subscribers.filter((s) => s.is_active).length}
            </p>
            <h3 className="text-muted-foreground font-bold uppercase tracking-wider text-[10px] mt-1.5">
              Active Subscribers
            </h3>
          </div>
        </div>

        <Button
          variant="outline"
          className="border border-primary/20 bg-gradient-to-br from-white to-primary/5 flex-col items-start justify-center gap-1 h-auto py-6 rounded-3xl"
          disabled
          title="Compose not available yet"
        >
          <div className="p-3 bg-primary/10 text-primary rounded-2xl">
            <PenSquare className="h-6 w-6" />
          </div>
          <div className="text-left mt-2">
            <p className="text-xs font-black text-foreground uppercase tracking-wider">Compose Dispatch</p>
            <p className="text-[9px] text-muted-foreground">Broadcast custom news &amp; updates</p>
          </div>
        </Button>

        <div className="border rounded-3xl border-border/50 p-6 flex flex-col justify-between">
          <div className="flex gap-2">
            <div className="flex-1 p-3 bg-muted hover:bg-muted/70 rounded-2xl border border-border text-muted-foreground flex flex-col items-center text-center transition-colors">
              <History className="h-5 w-5" />
              <span className="text-[8px] font-black uppercase tracking-wider mt-1.5">History</span>
            </div>
            <div className="flex-1 p-3 bg-muted hover:bg-muted/70 rounded-2xl border border-border text-muted-foreground flex flex-col items-center text-center transition-colors">
              <Download className="h-5 w-5" />
              <span className="text-[8px] font-black uppercase tracking-wider mt-1.5">Export CSV</span>
            </div>
          </div>
          <div className="mt-4">
            <p className="text-xs font-black text-foreground uppercase tracking-wider">Reports &amp; Archive</p>
            <p className="text-[9px] text-muted-foreground">Manage subscriber lists &amp; dispatches</p>
          </div>
        </div>
      </div>

      <div className="border rounded-xl border-border/50 overflow-hidden">
        <div className="px-6 py-4 bg-muted/50 border-b flex justify-between items-center">
          <div>
            <h3 className="font-bold text-foreground">Subscriber Directory</h3>
            <p className="text-[10px] font-bold uppercase tracking-wider text-muted-foreground mt-1">
              Full recipient roster
            </p>
          </div>
        </div>
        <table className="w-full text-left">
          <thead>
            <tr className="bg-muted/40 text-[10px] uppercase text-muted-foreground">
              <th className="px-8 py-4">Subscriber Email</th>
              <th className="px-6 py-4">Status</th>
              <th className="px-6 py-4">Joined Date</th>
              <th className="px-8 py-4 text-right">Actions</th>
            </tr>
          </thead>
          <tbody>
            {subscribers.length === 0 ? (
              <tr>
                <td colSpan={4} className="text-center text-muted-foreground py-16">
                  <Mail className="h-10 w-10 mx-auto mb-3 text-muted-foreground/40" />
                  <p className="font-bold text-foreground">No subscribers found yet</p>
                  <p className="text-xs text-muted-foreground mt-1">
                    Subscribers will appear here once the newsletter backend is implemented.
                  </p>
                </td>
              </tr>
            ) : (
              subscribers.map((sub) => (
                <tr key={sub.id} className="border-t border-border">
                  <td className="px-8 py-4 font-bold text-sm">{sub.email}</td>
                  <td className="px-6 py-4">
                    <span
                      className={`text-[8px] font-black uppercase px-2.5 py-1 rounded-full border tracking-wider ${
                        sub.is_active
                          ? "bg-sky-50 text-sky-600 border-sky-200"
                          : "bg-muted text-muted-foreground border-border"
                      }`}
                    >
                      {sub.is_active ? "Active" : "Inactive"}
                    </span>
                  </td>
                  <td className="px-6 py-4 text-muted-foreground text-xs">{sub.created_at}</td>
                  <td className="px-8 py-4 text-right">
                    <Button
                      variant="ghost"
                      size="icon"
                      className="h-9 w-9 text-destructive"
                      disabled
                      title="Remove not available yet"
                    >
                      <Trash2 className="h-4 w-4" />
                    </Button>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
