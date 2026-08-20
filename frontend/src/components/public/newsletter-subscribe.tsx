"use client";

import { useState, type FormEvent } from "react";
import { fetchAPI } from "@/lib/api";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Mail, Loader2, CheckCircle2, AlertCircle } from "lucide-react";

export function NewsletterSubscribe() {
  const [email, setEmail] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState(false);

  const onSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setError("");
    setSuccess(false);
    setLoading(true);
    try {
      await fetchAPI<{ detail: string }>("/api/notifications/subscribe", {
        method: "POST",
        body: JSON.stringify({ email }),
      });
      setSuccess(true);
      setEmail("");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Subscription failed. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <form
      onSubmit={onSubmit}
      className="flex flex-col sm:flex-row items-stretch gap-3 bg-card border border-border/60 rounded-2xl p-4 shadow-sm"
    >
      <div className="relative flex-1">
        <Mail className="absolute left-3.5 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
        <Input
          type="email"
          required
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="you@example.com"
          className="pl-10 h-11 rounded-xl bg-background border-input text-sm"
        />
      </div>
      <Button type="submit" disabled={loading} className="h-11 rounded-xl font-semibold">
        {loading ? <Loader2 className="h-4 w-4 animate-spin mr-2" /> : null}
        Subscribe
      </Button>

      {success && (
        <p className="w-full text-xs text-emerald-600 dark:text-emerald-400 flex items-center gap-1.5 pt-1">
          <CheckCircle2 className="h-3.5 w-3.5" /> You&apos;re subscribed to community bulletins.
        </p>
      )}
      {error && (
        <p className="w-full text-xs text-destructive flex items-center gap-1.5 pt-1">
          <AlertCircle className="h-3.5 w-3.5" /> {error}
        </p>
      )}
    </form>
  );
}
