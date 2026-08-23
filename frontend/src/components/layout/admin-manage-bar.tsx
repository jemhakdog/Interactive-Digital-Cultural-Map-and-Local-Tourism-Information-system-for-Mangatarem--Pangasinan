"use client";

import Link from "next/link";
import { ArrowRight, Shield } from "lucide-react";
import { useAuth } from "@/lib/auth";

/**
 * Renders a slim admin-only banner on public pages linking to the
 * corresponding full-control management section. Invisible to everyone else.
 */
export function AdminManageBar({
  label,
  href = "/admin",
  note,
}: {
  label: string;
  href?: string;
  note?: string;
}) {
  const { user } = useAuth();
  if (!user || user.role !== "admin") return null;

  return (
    <div className="container mx-auto px-4 pt-4">
      <Link
        href={href}
        className="flex items-center gap-2 rounded-xl border border-primary/20 bg-primary/5 px-4 py-2.5 text-sm font-medium text-foreground transition-colors hover:bg-primary/10"
      >
        <Shield className="h-4 w-4 shrink-0 text-primary" />
        <span className="truncate">
          Admin mode — manage {label}
          {note && <span className="ml-2 hidden text-xs font-normal text-muted-foreground sm:inline">{note}</span>}
        </span>
        <ArrowRight className="ml-auto h-4 w-4 shrink-0 text-primary" />
      </Link>
    </div>
  );
}
