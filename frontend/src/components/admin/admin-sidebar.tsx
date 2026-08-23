"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useState, useEffect } from "react";
import { useAuth } from "@/lib/auth";
import {
  LayoutDashboard,
  BarChart3,
  MapPin,
  Calendar,
  Landmark,
  Building2,
  Users,
  BadgeCheck,
  CalendarCheck,
  Star,
  FileText,
  Mail,
  Megaphone,
  Images,
  ClipboardList,
  ExternalLink,
  Menu,
  Shield,
  LogOut,
  Map,
  Sun,
  Moon,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Sheet, SheetContent, SheetTrigger, SheetHeader, SheetTitle } from "@/components/ui/sheet";

interface NavGroup {
  title: string;
  items: {
    href: string;
    label: string;
    icon: React.ComponentType<{ className?: string }>;
    exact?: boolean;
  }[];
}

const navigationGroups: NavGroup[] = [
  {
    title: "Overview",
    items: [
      { href: "/admin", label: "Dashboard", icon: LayoutDashboard, exact: true },
      { href: "/admin/analytics", label: "Analytics", icon: BarChart3 },
      { href: "/admin/visits", label: "Visitor Traffic", icon: Map },
    ],
  },
  {
    title: "Tourism & Heritage",
    items: [
      { href: "/admin/attractions", label: "Attractions", icon: MapPin },
      { href: "/admin/events", label: "Events", icon: Calendar },
      { href: "/admin/heritage", label: "Heritage Sites", icon: Landmark },
      { href: "/admin/establishments", label: "Businesses", icon: Building2 },
      { href: "/admin/barangays", label: "Barangays", icon: Landmark },
      { href: "/admin/gallery", label: "Media Gallery", icon: Images },
    ],
  },
  {
    title: "Content & Moderation",
    items: [
      { href: "/admin/announcements", label: "Announcements", icon: Megaphone },
      { href: "/admin/reviews", label: "Reviews Moderation", icon: Star },
      { href: "/admin/documents", label: "Documents", icon: FileText },
      { href: "/admin/newsletter", label: "Newsletter", icon: Mail },
    ],
  },
  {
    title: "Operations & Users",
    items: [
      { href: "/admin/verify-merchants", label: "Verify Merchants", icon: BadgeCheck },
      { href: "/admin/bookings", label: "Manage Bookings", icon: CalendarCheck },
      { href: "/admin/visitor-registry", label: "Visitor Registry", icon: ClipboardList },
      { href: "/admin/users", label: "User Management", icon: Users },
    ],
  },
];

function NavContent({ onNavigate }: { onNavigate?: () => void }) {
  const pathname = usePathname();
  const { user, logout } = useAuth();
  const [isDark, setIsDark] = useState(false);

  useEffect(() => {
    setIsDark(document.documentElement.classList.contains("dark"));
  }, []);

  const toggleDarkMode = () => {
    const nextDark = !isDark;
    setIsDark(nextDark);
    if (nextDark) {
      document.documentElement.classList.add("dark");
      localStorage.setItem("theme", "dark");
    } else {
      document.documentElement.classList.remove("dark");
      localStorage.setItem("theme", "light");
    }
  };

  return (
    <div className="flex h-full flex-col justify-between">
      <div className="flex-1 overflow-y-auto px-3 py-4 space-y-6">
        {/* Brand */}
        <div className="px-3 pb-2 border-b border-border/50">
          <Link
            href="/admin"
            onClick={onNavigate}
            className="flex items-center gap-3 transition-opacity hover:opacity-90"
          >
            <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-primary text-primary-foreground shadow-sm">
              <Shield className="h-5 w-5" />
            </div>
            <div className="min-w-0">
              <div className="flex items-center gap-2">
                <span className="font-bold text-base tracking-tight truncate">Mangatarem</span>
                <Badge variant="secondary" className="text-[10px] px-1.5 py-0 font-medium">
                  Admin
                </Badge>
              </div>
              <p className="text-xs text-muted-foreground truncate">Tourism & Heritage Portal</p>
            </div>
          </Link>
        </div>

        {/* Navigation Sections */}
        <div className="space-y-5">
          {navigationGroups.map((group) => (
            <div key={group.title} className="space-y-1">
              <p className="px-3 text-[11px] font-semibold uppercase tracking-wider text-muted-foreground/70">
                {group.title}
              </p>
              <div className="space-y-0.5">
                {group.items.map((item) => {
                  const active = item.exact
                    ? pathname === item.href
                    : pathname === item.href || pathname.startsWith(item.href + "/");
                  const Icon = item.icon;

                  return (
                    <Link
                      key={item.href}
                      href={item.href}
                      onClick={onNavigate}
                      className={`flex items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium transition-all ${
                        active
                          ? "bg-primary text-primary-foreground font-semibold shadow-xs"
                          : "text-muted-foreground hover:bg-muted hover:text-foreground"
                      }`}
                    >
                      <Icon
                        className={`h-4 w-4 shrink-0 ${
                          active ? "text-primary-foreground" : "text-muted-foreground"
                        }`}
                      />
                      <span className="truncate">{item.label}</span>
                    </Link>
                  );
                })}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Footer / Account / External Links */}
      <div className="border-t border-border/50 p-3 bg-muted/20 space-y-2">
        <Link
          href="/"
          target="_blank"
          className="flex items-center justify-between gap-2 rounded-lg px-3 py-2 text-xs font-medium text-muted-foreground hover:bg-muted hover:text-foreground transition-colors"
        >
          <span className="flex items-center gap-2">
            <ExternalLink className="h-3.5 w-3.5" />
            View Public Site
          </span>
          <Badge variant="outline" className="text-[10px] px-1 py-0">
            Live
          </Badge>
        </Link>

        {/* Dark Mode Toggle */}
        <button
          type="button"
          onClick={toggleDarkMode}
          className="flex w-full items-center justify-between gap-2 rounded-lg px-3 py-2 text-xs font-medium text-muted-foreground hover:bg-muted hover:text-foreground transition-colors cursor-pointer border border-border/30 bg-card/40"
        >
          <span className="flex items-center gap-2">
            {isDark ? (
              <Moon className="h-3.5 w-3.5 text-primary" />
            ) : (
              <Sun className="h-3.5 w-3.5 text-amber-500" />
            )}
            <span>Dark Mode</span>
          </span>
          <span className="flex items-center gap-1.5 text-[11px] font-medium text-foreground">
            {isDark ? "On" : "Off"}
            <span
              className={`inline-block h-4 w-7 rounded-full transition-colors relative ${
                isDark ? "bg-primary" : "bg-muted-foreground/30"
              }`}
            >
              <span
                className={`inline-block h-3 w-3 rounded-full bg-background shadow-xs transition-transform absolute top-0.5 ${
                  isDark ? "right-0.5" : "left-0.5"
                }`}
              />
            </span>
          </span>
        </button>

        {user && (
          <div className="flex items-center justify-between rounded-lg bg-card/60 p-2 border border-border/40">
            <div className="flex items-center gap-2.5 min-w-0 pr-1">
              <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-primary/10 text-primary font-bold text-xs">
                {user.name?.charAt(0)?.toUpperCase() || "A"}
              </div>
              <div className="min-w-0">
                <p className="text-xs font-medium truncate">{user.name}</p>
                <p className="text-[10px] text-muted-foreground truncate">{user.email}</p>
              </div>
            </div>
            <Button
              variant="ghost"
              size="icon"
              className="h-8 w-8 shrink-0 text-muted-foreground hover:text-destructive hover:bg-destructive/10"
              onClick={logout}
              title="Log out"
            >
              <LogOut className="h-4 w-4" />
            </Button>
          </div>
        )}
      </div>
    </div>
  );
}

export function AdminSidebar() {
  const [open, setOpen] = useState(false);
  const pathname = usePathname();

  const activeItem = navigationGroups
    .flatMap((g) => g.items)
    .find((item) =>
      item.exact
        ? pathname === item.href
        : pathname === item.href || pathname.startsWith(item.href + "/")
    );

  return (
    <>
      {/* Mobile / Tablet Top Header */}
      <header className="lg:hidden sticky top-0 z-40 flex h-14 w-full items-center justify-between border-b border-border/50 bg-background/95 px-4 backdrop-blur-md">
        <div className="flex items-center gap-2.5">
          <Sheet open={open} onOpenChange={setOpen}>
            <SheetTrigger render={<Button variant="ghost" size="icon" className="h-9 w-9" />}>
              <Menu className="h-5 w-5" />
              <span className="sr-only">Toggle Admin Navigation</span>
            </SheetTrigger>
            <SheetContent side="left" className="w-72 p-0 flex flex-col">
              <SheetHeader className="sr-only">
                <SheetTitle>Admin Navigation Menu</SheetTitle>
              </SheetHeader>
              <NavContent onNavigate={() => setOpen(false)} />
            </SheetContent>
          </Sheet>

          <Link href="/admin" className="flex items-center gap-2">
            <div className="flex h-7 w-7 items-center justify-center rounded-lg bg-primary text-primary-foreground">
              <Shield className="h-4 w-4" />
            </div>
            <span className="font-bold text-sm">Admin Console</span>
          </Link>
        </div>

        {activeItem && (
          <Badge variant="outline" className="text-xs max-w-[140px] truncate">
            {activeItem.label}
          </Badge>
        )}
      </header>

      {/* Desktop Sticky Left Sidebar */}
      <aside className="hidden lg:flex w-64 xl:w-72 shrink-0 flex-col border-r border-border/50 bg-card/50 backdrop-blur-md h-screen sticky top-0">
        <NavContent />
      </aside>
    </>
  );
}
