"use client";

import { useState } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { MessageSquare, X, Compass, ExternalLink, HelpCircle, Phone } from "lucide-react";
import { Button } from "@/components/ui/button";

export function ConciergeChatBubble() {
  const [isOpen, setIsOpen] = useState(false);
  const pathname = usePathname();

  // Hide inside admin, full-screen map, and chat room itself
  if (pathname.startsWith("/admin") || pathname.startsWith("/chat")) {
    return null;
  }

  return (
    <div className="fixed bottom-6 right-6 z-40 print:hidden">
      {isOpen ? (
        <div className="mb-3 w-80 sm:w-96 rounded-2xl border bg-card/95 backdrop-blur-xl p-5 shadow-2xl transition-all animate-in fade-in slide-in-from-bottom-5">
          <div className="flex items-center justify-between pb-3 border-b mb-3">
            <div className="flex items-center gap-2">
              <div className="h-8 w-8 rounded-full bg-primary/10 flex items-center justify-center text-primary">
                <Compass className="h-4.5 w-4.5" />
              </div>
              <div>
                <h4 className="font-semibold text-sm">Tourist Concierge</h4>
                <p className="text-[11px] text-muted-foreground">Mangatarem Visitor Guide</p>
              </div>
            </div>
            <Button
              variant="ghost"
              size="icon"
              className="h-7 w-7 text-muted-foreground"
              onClick={() => setIsOpen(false)}
              aria-label="Close concierge"
            >
              <X className="h-4 w-4" />
            </Button>
          </div>

          <p className="text-xs text-muted-foreground mb-4">
            Need directions, travel tips, or assistance while exploring Mangatarem?
          </p>

          <div className="space-y-2 mb-4">
            <Link
              href="/chat"
              onClick={() => setIsOpen(false)}
              className="flex items-center justify-between p-2.5 rounded-xl border bg-background hover:bg-muted/60 transition-colors text-xs font-medium"
            >
              <span className="flex items-center gap-2">
                <MessageSquare className="h-4 w-4 text-primary" />
                Live Community Tourism Chat
              </span>
              <ExternalLink className="h-3.5 w-3.5 text-muted-foreground" />
            </Link>

            <Link
              href="/map"
              onClick={() => setIsOpen(false)}
              className="flex items-center justify-between p-2.5 rounded-xl border bg-background hover:bg-muted/60 transition-colors text-xs font-medium"
            >
              <span className="flex items-center gap-2">
                <Compass className="h-4 w-4 text-primary" />
                Interactive Cultural Map & Trails
              </span>
              <ExternalLink className="h-3.5 w-3.5 text-muted-foreground" />
            </Link>

            <Link
              href="/passport"
              onClick={() => setIsOpen(false)}
              className="flex items-center justify-between p-2.5 rounded-xl border bg-background hover:bg-muted/60 transition-colors text-xs font-medium"
            >
              <span className="flex items-center gap-2">
                <HelpCircle className="h-4 w-4 text-primary" />
                Digital Passport & Stamps
              </span>
              <ExternalLink className="h-3.5 w-3.5 text-muted-foreground" />
            </Link>
          </div>

          <div className="pt-3 border-t text-[11px] text-muted-foreground flex items-center justify-between">
            <span className="flex items-center gap-1">
              <Phone className="h-3 w-3" /> Tourism Office: (075) 546-2134
            </span>
            <span>Mon–Fri 8AM–5PM</span>
          </div>
        </div>
      ) : null}

      <Button
        onClick={() => setIsOpen(!isOpen)}
        size="lg"
        className="h-12 w-12 rounded-full shadow-lg gap-0 p-0 bg-primary text-primary-foreground hover:bg-primary/90"
        aria-label="Open Tourist Assistance Concierge"
      >
        <MessageSquare className="h-5 w-5" />
      </Button>
    </div>
  );
}
