"use client";

import { useEffect, useState } from "react";
import { useAuth } from "@/lib/auth";
import { useRouter } from "next/navigation";
import { Loader2, FolderOpen, FileText, Upload, Download, Plus } from "lucide-react";
import { Button } from "@/components/ui/button";

interface Folder {
  name: string;
  count: number;
  total_size: string;
}

interface RecordItem {
  id: number;
  name_of_asset: string;
  asset_type: string;
  created_at: string;
  size: string;
}

export default function AdminDocumentsPage() {
  const { user, loading: authLoading } = useAuth();
  const router = useRouter();
  // TODO: FastAPI /api/documents router not implemented yet — using local placeholder state.
  const [folders] = useState<Folder[]>([]);
  const [records] = useState<RecordItem[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!authLoading && (!user || user.role !== "admin")) router.push("/dashboard");
  }, [user, authLoading, router]);

  useEffect(() => {
    if (!user) return;
    // No documents backend yet; placeholder lists stay empty.
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
    <div className="container mx-auto px-4 py-8 max-w-5xl space-y-10">
      <div className="flex items-center justify-between gap-4">
        <div className="flex items-center gap-3">
          <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-primary/10 text-primary">
            <FileText className="h-5 w-5" />
          </div>
          <div>
            <h1 className="text-3xl font-bold tracking-tight">Document Vault</h1>
            <p className="text-muted-foreground text-sm mt-0.5">
              Tourism data architecture &amp; form management
            </p>
          </div>
        </div>
        <div className="flex gap-2">
          <Button variant="outline" className="gap-2 rounded-xl" disabled title="Import not available yet">
            <Upload className="h-4 w-4" /> Import
          </Button>
          <Button variant="outline" className="gap-2 rounded-xl" disabled title="Backup not available yet">
            <Download className="h-4 w-4" /> Backup
          </Button>
        </div>
      </div>

      <section>
        <h3 className="text-xl font-bold text-foreground flex items-center gap-2 mb-6">
          <span className="w-2 h-8 bg-primary rounded-full" /> Form Categories
        </h3>
        {folders.length === 0 ? (
          <div className="border border-dashed border-border rounded-2xl py-16 text-center">
            <FolderOpen className="h-10 w-10 mx-auto mb-3 text-muted-foreground/40" />
            <p className="font-bold text-foreground">No document folders yet</p>
            <p className="text-xs text-muted-foreground mt-1">
              The document management backend is not implemented yet.
            </p>
          </div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
            {folders.map((f) => (
              <div
                key={f.name}
                className="border border-border/50 rounded-2xl p-6 hover:border-primary/50 transition-colors"
              >
                <div className="w-16 h-16 bg-muted rounded-2xl flex items-center justify-center mb-4">
                  <FolderOpen className="h-8 w-8 text-primary" />
                </div>
                <h4 className="font-bold text-foreground">{f.name}</h4>
                <p className="text-[10px] uppercase tracking-widest text-muted-foreground mt-1">
                  {f.count} Structures • {f.total_size}
                </p>
              </div>
            ))}
          </div>
        )}
      </section>

      <section>
        <div className="flex items-center justify-between mb-6">
          <h3 className="text-xl font-bold text-foreground flex items-center gap-2">
            <span className="w-2 h-8 bg-amber-500 rounded-full" /> Structured Records
          </h3>
          <Button variant="outline" size="sm" className="gap-1 rounded-xl" disabled title="New record not available yet">
            <Plus className="h-3.5 w-3.5" /> New Record
          </Button>
        </div>
        {records.length === 0 ? (
          <div className="border border-dashed border-border rounded-2xl py-12 text-center">
            <p className="font-bold text-foreground">No structured records found yet.</p>
            <p className="text-xs text-muted-foreground mt-1">
              Use the document backend once it is implemented to start. (Pending.)
            </p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {records.map((r) => (
              <div key={r.id} className="border border-border/50 rounded-2xl p-6">
                <div className="flex justify-between items-start mb-4">
                  <div className="p-3 bg-amber-50 rounded-2xl text-amber-600">
                    <FileText className="h-6 w-6" />
                  </div>
                  <span className="text-[8px] font-black uppercase tracking-widest text-amber-400">
                    {r.asset_type}
                  </span>
                </div>
                <h4 className="font-bold text-foreground truncate">{r.name_of_asset}</h4>
                <div className="flex gap-2 mt-4">
                  <Button variant="outline" size="sm" className="flex-1 rounded-xl" disabled>
                    Edit Record
                  </Button>
                  <Button size="sm" className="flex-1 rounded-xl" disabled>
                    Export .docx
                  </Button>
                </div>
              </div>
            ))}
          </div>
        )}
      </section>
    </div>
  );
}
