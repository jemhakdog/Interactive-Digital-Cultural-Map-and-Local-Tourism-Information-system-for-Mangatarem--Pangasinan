"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { LayoutDashboard, MapPin, CalendarDays, Images, Megaphone, Star, User } from "lucide-react";

const links = [
  { href: "/contributor", label: "Dashboard", icon: LayoutDashboard, exact: true },
  { href: "/contributor/attractions/new", label: "Add Landmark", icon: MapPin },
  { href: "/contributor/events/new", label: "Publish Event", icon: CalendarDays },
  { href: "/contributor/gallery/new", label: "Add Media", icon: Images },
  { href: "/contributor/announcements", label: "Announcements", icon: Megaphone },
  { href: "/contributor/reviews", label: "Reviews", icon: Star },
  { href: "/contributor/profile", label: "Barangay Profile", icon: User },
];

export function ContributorNav() {
  const pathname = usePathname();
  return (
    <aside className="w-full lg:w-64 shrink-0">
      <div className="lg:sticky lg:top-20 space-y-3">
        <div className="flex items-center gap-2 px-3 py-2">
          <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-primary text-primary-foreground">
            <User className="h-4 w-4" />
          </div>
          <div>
            <p className="text-sm font-semibold leading-tight">Barangay Steward</p>
            <p className="text-[10px] uppercase tracking-wider text-muted-foreground">CBIS Console</p>
          </div>
        </div>
        <nav className="flex lg:flex-col gap-1 overflow-x-auto lg:overflow-visible pb-2 lg:pb-0">
          {links.map((link) => {
            const active = link.exact
              ? pathname === link.href
              : pathname === link.href || pathname.startsWith(link.href + "/");
            const Icon = link.icon;
            return (
              <Link
                key={link.href}
                href={link.href}
                className={`flex items-center gap-2.5 rounded-lg px-3 py-2 text-sm font-medium whitespace-nowrap transition-colors ${
                  active
                    ? "bg-primary/10 text-primary"
                    : "text-muted-foreground hover:bg-muted hover:text-foreground"
                }`}
              >
                <Icon className="h-4 w-4" />
                {link.label}
              </Link>
            );
          })}
        </nav>
      </div>
    </aside>
  );
}
