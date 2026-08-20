"use client";

import { useState } from "react";
import Link from "next/link";
import { useParams } from "next/navigation";
import { useAuth } from "@/lib/auth";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { ArrowLeft, ShieldCheck, Clock, XCircle, CheckCircle2, Loader2 } from "lucide-react";

type VerifyStatus = "none" | "pending" | "rejected";

export default function VerifyBusinessPage() {
  const params = useParams<{ id: string }>();
  const id = params.id;
  const { user, loading: authLoading } = useAuth();

  // TODO: FastAPI endpoint not implemented yet — using local placeholder state.
  // No verification/approve endpoint exists; submissions are staged locally only.
  const [status, setStatus] = useState<VerifyStatus>("none");
  const [permitUrl, setPermitUrl] = useState("");
  const [otherUrl, setOtherUrl] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [submitted, setSubmitted] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!permitUrl.trim()) return;
    setSubmitting(true);
    // No backend endpoint — simulate a staged submission locally.
    setTimeout(() => {
      setStatus("pending");
      setSubmitted(true);
      setSubmitting(false);
    }, 600);
  };

  if (authLoading || !user) {
    return (
      <div className="flex justify-center py-16">
        <Loader2 className="h-6 w-6 animate-spin text-muted-foreground" />
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8 max-w-4xl space-y-8">
      <div className="flex items-center justify-between pb-4 border-b border-border/50">
        <div className="space-y-1">
          <Link
            href="/business/dashboard"
            className="text-xs font-bold uppercase tracking-wider text-muted-foreground hover:text-foreground flex items-center gap-1.5 transition-colors"
          >
            <ArrowLeft className="h-3.5 w-3.5" /> Back to Dashboard
          </Link>
          <h1 className="text-xl font-bold tracking-tight text-foreground mt-2">Business Verification</h1>
        </div>
      </div>

      <Card className="overflow-hidden border-border/60">
        <div className="bg-primary p-6">
          <h2 className="text-2xl font-extrabold text-primary-foreground flex items-center gap-2">
            <ShieldCheck className="h-6 w-6" /> Business Verification
          </h2>
          <p className="mt-1 text-sm text-primary-foreground/80">
            Submit your business permits to activate your account.
          </p>
        </div>

        <CardContent className="p-8">
          {status === "pending" && (
            <div className="bg-amber-500/10 border border-amber-500/20 text-amber-700 dark:text-amber-400 px-6 py-5 rounded-xl flex items-start gap-4 mb-8">
              <Clock className="h-6 w-6 mt-1 text-amber-500 shrink-0" />
              <div>
                <h3 className="text-base font-bold">Verification Pending</h3>
                <p className="mt-1 text-sm">
                  Your business documents are being reviewed by an administrator. This usually takes
                  1–2 business days. We&apos;ll notify you once approved.
                </p>
              </div>
            </div>
          )}
          {status === "rejected" && (
            <div className="bg-destructive/10 border border-destructive/20 text-destructive px-6 py-5 rounded-xl flex items-start gap-4 mb-8">
              <XCircle className="h-6 w-6 mt-1 shrink-0" />
              <div>
                <h3 className="text-base font-bold">Verification Rejected</h3>
                <p className="mt-1 text-sm">
                  Your previously submitted documents were not approved. Please submit valid
                  documents below.
                </p>
              </div>
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-6">
            <div className="space-y-1.5">
              <Label className="text-sm font-semibold text-foreground">
                Business Permit Document <span className="text-destructive">*</span>
              </Label>
              <p className="text-xs text-muted-foreground font-medium mb-3">
                Provide a secure link (Google Drive, Dropbox, etc.) to your valid business permit.
              </p>
              <Input
                type="url"
                value={permitUrl}
                onChange={(e) => setPermitUrl(e.target.value)}
                placeholder="https://drive.google.com/..."
                required
                className="rounded-xl"
              />
            </div>

            <div className="space-y-1.5">
              <Label className="text-sm font-semibold text-foreground">Other Supporting Documents</Label>
              <p className="text-xs text-muted-foreground font-medium mb-3">
                Link to BIR registration, DTI certificate, or Mayor&apos;s permit.
              </p>
              <Input
                type="url"
                value={otherUrl}
                onChange={(e) => setOtherUrl(e.target.value)}
                placeholder="https://drive.google.com/..."
                className="rounded-xl"
              />
            </div>

            {submitted && status === "pending" && (
              <div className="flex items-center gap-2 text-sm font-semibold text-emerald-600 bg-emerald-500/10 border border-emerald-500/20 rounded-xl p-3">
                <CheckCircle2 className="h-4 w-4" /> Documents submitted for review.
              </div>
            )}

            <div className="pt-2 flex justify-end">
              <Button type="submit" disabled={submitting} className="gap-2 rounded-xl">
                {submitting ? <Loader2 className="h-4 w-4 animate-spin" /> : <CheckCircle2 className="h-4 w-4" />}
                {status === "pending" ? "Update Documents" : "Submit Documents"}
              </Button>
            </div>
          </form>
        </CardContent>
      </Card>
    </div>
  );
}
