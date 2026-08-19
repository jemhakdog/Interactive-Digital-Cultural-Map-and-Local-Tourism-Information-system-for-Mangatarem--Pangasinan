import Link from "next/link";
import { MapPin } from "lucide-react";

export function Footer() {
  return (
    <footer className="border-t border-border bg-muted/50">
      <div className="container mx-auto px-4 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          {/* Brand */}
          <div className="space-y-3">
            <Link href="/" className="flex items-center gap-2 font-bold text-lg">
              <MapPin className="h-5 w-5 text-primary" />
              <span className="text-primary">Mangatarem</span>
            </Link>
            <p className="text-sm text-muted-foreground">
              Interactive Digital Cultural Map and Local Tourism Information System
              for Mangatarem, Pangasinan.
            </p>
          </div>

          {/* Explore */}
          <div className="space-y-3">
            <h3 className="font-semibold text-sm">Explore</h3>
            <ul className="space-y-2 text-sm text-muted-foreground">
              <li><Link href="/attractions" className="hover:text-foreground transition-colors">Attractions</Link></li>
              <li><Link href="/events" className="hover:text-foreground transition-colors">Events</Link></li>
              <li><Link href="/business" className="hover:text-foreground transition-colors">Businesses</Link></li>
              <li><Link href="/heritage" className="hover:text-foreground transition-colors">Heritage</Link></li>
              <li><Link href="/map" className="hover:text-foreground transition-colors">Map</Link></li>
            </ul>
          </div>

          {/* Community */}
          <div className="space-y-3">
            <h3 className="font-semibold text-sm">Community</h3>
            <ul className="space-y-2 text-sm text-muted-foreground">
              <li><Link href="/gallery" className="hover:text-foreground transition-colors">Gallery</Link></li>
              <li><Link href="/chat" className="hover:text-foreground transition-colors">Chat</Link></li>
              <li><Link href="/passport" className="hover:text-foreground transition-colors">Tourist Passport</Link></li>
            </ul>
          </div>

          {/* Account */}
          <div className="space-y-3">
            <h3 className="font-semibold text-sm">Account</h3>
            <ul className="space-y-2 text-sm text-muted-foreground">
              <li><Link href="/auth/login" className="hover:text-foreground transition-colors">Log in</Link></li>
              <li><Link href="/auth/register" className="hover:text-foreground transition-colors">Sign up</Link></li>
              <li><Link href="/dashboard" className="hover:text-foreground transition-colors">Dashboard</Link></li>
            </ul>
          </div>
        </div>

        <div className="mt-8 pt-8 border-t text-center text-sm text-muted-foreground">
          © {new Date().getFullYear()} Mangatarem Tourism System. All rights reserved.
        </div>
      </div>
    </footer>
  );
}
