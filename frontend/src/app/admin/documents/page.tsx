"use client";

import { useEffect, useState } from "react";
import { useAuth } from "@/lib/auth";
import { fetchAPI } from "@/lib/api";
import { useRouter } from "next/navigation";
import { Loader2, FolderOpen, FileText, Upload, Download, Plus } from "lucide-react";
import { Button } from "@/components/ui/button";

interface Folder {
  name: string;
  count: number;
}

interface DocumentRecord {
  id: number;
  title: string;
  category: string;
  content: string | null;
  file_url: string | null;
  created_at: string | null;
}

async function listDocuments(): Promise<DocumentRecord[]> {
  return fetchAPI<DocumentRecord[]>("/api/documents/");
}

function groupByCategory(records: DocumentRecord[]): Folder[] {
  const counts = new Map<string, number>();
  for (const r of records) {
    counts.set(r.category, (counts.get(r.category) ?? 0) + 1);
  }
  return Array.from(counts.entries()).map(([name, count]) => ({ name, count }));
}

export default function AdminDocumentsPage() {
  const { user, loading: authLoading } = useAuth();
  const router = useRouter();
  const [folders, setFolders] = useState<Folder[]>([]);
  const [records, setRecords] = useState<DocumentRecord[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!authLoading && (!user || user.role !== "admin")) router.push("/dashboard");
  }, [user, authLoading, router]);

  useEffect(() => {
    if (!user) return;
    let cancelled = false;
    listDocuments()
      .then((docs) => {
        if (cancelled) return;
        setRecords(docs);
        setFolders(groupByCategory(docs));
        setError(null);
      })
      .catch((err: unknown) => {
        if (!cancelled) setError(err instanceof Error ? err.message : "Failed to load documents.");
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });
    return () => {
      cancelled = true;
    };
  }, [user]);

  async function handleCreateRecord() {
    const title = window.prompt("New record title:");
    if (!title) return;
    try {
      await fetchAPI<DocumentRecord>("/api/documents/", {
        method: "POST",
        body: JSON.stringify({ title }),
      });
      const docs = await listDocuments();
      setRecords(docs);
      setFolders(groupByCategory(docs));
      setError(null);
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "Failed to create record.");
    }
  }

  async function handleEditRecord(record: DocumentRecord) {
    const title = window.prompt("Edit record title:", record.title);
    if (!title || title === record.title) return;
    try {
      await fetchAPI<DocumentRecord>(`/api/documents/${record.id}`, {
        method: "PUT",
        body: JSON.stringify({ title }),
      });
      const docs = await listDocuments();
      setRecords(docs);
      setFolders(groupByCategory(docs));
      setError(null);
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "Failed to update record.");
    }
  }

  async function handleDeleteRecord(record: DocumentRecord) {
    if (!window.confirm(`Delete "${record.title}"? This cannot be undone.`)) return;
    try {
      await fetchAPI(`/api/documents/${record.id}`, { method: "DELETE" });
      const docs = await listDocuments();
      setRecords(docs);
      setFolders(groupByCategory(docs));
      setError(null);
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "Failed to delete record.");
    }
  }

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
          {/* TODO: backend has no import endpoint — add POST /api/documents/import before enabling. */}
          <Button variant="outline" className="gap-2 rounded-xl" disabled title="Import not available yet">
            <Upload className="h-4 w-4" /> Import
          </Button>
          {/* TODO: backend has no backup endpoint — add GET /api/documents/backup before enabling. */}
          <Button variant="outline" className="gap-2 rounded-xl" disabled title="Backup not available yet">
            <Download className="h-4 w-4" /> Backup
          </Button>
        </div>
      </div>

      {error && (
        <p className="text-sm text-destructive bg-destructive/10 border border-destructive/30 rounded-xl px-4 py-3">
          {error}
        </p>
      )}

      <section>
        <h3 className="text-xl font-bold text-foreground flex items-center gap-2 mb-6">
          <span className="w-2 h-8 bg-primary rounded-full" /> Form Categories
        </h3>
        {folders.length === 0 ? (
          <div className="border border-dashed border-border rounded-2xl py-16 text-center">
            <FolderOpen className="h-10 w-10 mx-auto mb-3 text-muted-foreground/40" />
            <p className="font-bold text-foreground">No document folders yet</p>
            <p className="text-xs text-muted-foreground mt-1">
              Create a record to start a category folder.
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
                  {f.count} {f.count === 1 ? "Record" : "Records"}
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
          <Button
            variant="outline"
            size="sm"
            className="gap-1 rounded-xl"
            onClick={handleCreateRecord}
          >
            <Plus className="h-3.5 w-3.5" /> New Record
          </Button>
        </div>
        {records.length === 0 ? (
          <div className="border border-dashed border-border rounded-2xl py-12 text-center">
            <p className="font-bold text-foreground">No structured records found yet.</p>
            <p className="text-xs text-muted-foreground mt-1">
              Use “New Record” to add the first document.
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
                    {r.category}
                  </span>
                </div>
                <h4 className="font-bold text-foreground truncate">{r.title}</h4>
                <div className="flex gap-2 mt-4">
                  <Button
                    variant="outline"
                    size="sm"
                    className="flex-1 rounded-xl"
                    onClick={() => handleEditRecord(r)}
                  >
                    Edit Record
                  </Button>
                  <Button size="sm" className="flex-1 rounded-xl" disabled>
                    {/* TODO: backend has no .docx export/backup/import endpoints yet — add /api/documents/export, /backup and an importer before enabling. */}
                    Export .docx
                  </Button>
                  <Button
                    variant="outline"
                    size="sm"
                    className="rounded-xl text-destructive"
                    onClick={() => handleDeleteRecord(r)}
                  >
                    Delete
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
