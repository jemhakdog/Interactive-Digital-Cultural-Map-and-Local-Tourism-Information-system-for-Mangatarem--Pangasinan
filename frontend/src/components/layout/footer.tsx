import Link from "next/link";
import { Compass } from "lucide-react";

const footerLinks = {
  explore: [
    { href: "/attractions", label: "Attractions" },
    { href: "/events", label: "Events" },
    { href: "/business", label: "Businesses" },
    { href: "/heritage", label: "Heritage" },
    { href: "/map", label: "Interactive Map" },
  ],
  community: [
    { href: "/gallery", label: "Gallery" },
    { href: "/chat", label: "Chat Rooms" },
    { href: "/passport", label: "Tourist Passport" },
  ],
  account: [
    { href: "/auth/login", label: "Log in" },
    { href: "/auth/register", label: "Sign up" },
    { href: "/dashboard", label: "Dashboard" },
  ],
};

export function Footer() {
  return (
    <footer className="border-t border-border/50 bg-muted/30">
      <div className="container mx-auto px-4 py-12">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
          {/* Brand */}
          <div className="col-span-2 md:col-span-1 space-y-3">
            <Link href="/" className="flex items-center gap-2 font-bold text-lg">
              <div className="flex h-7 w-7 items-center justify-center rounded-lg bg-primary text-primary-foreground">
                <Compass className="h-4 w-4" />
              </div>
              Mangatarem
            </Link>
            <p className="text-sm text-muted-foreground leading-relaxed">
              Interactive Digital Cultural Map and Local Tourism Information System
              for Mangatarem, Pangasinan.
            </p>
          </div>

          {Object.entries(footerLinks).map(([section, links]) => (
            <div key={section} className="space-y-3">
              <h3 className="font-semibold text-sm capitalize">{section}</h3>
              <ul className="space-y-2">
                {links.map((link) => (
                  <li key={link.href}>
                    <Link
                      href={link.href}
                      className="text-sm text-muted-foreground hover:text-foreground transition-colors"
                    >
                      {link.label}
                    </Link>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>

        <div className="mt-8 pt-8 border-t border-border/50 text-center text-xs text-muted-foreground">
          © {new Date().getFullYear()} Mangatarem Tourism System. All rights reserved.
        </div>
      </div>
    </footer>
  );
}
