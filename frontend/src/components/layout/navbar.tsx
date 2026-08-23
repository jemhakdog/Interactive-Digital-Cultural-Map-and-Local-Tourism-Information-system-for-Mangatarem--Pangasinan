"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useState } from "react";
import { Menu, Search, User, LogOut, Compass, Shield, CalendarCheck, Star, Store, UserCog, BookOpen } from "lucide-react";
import { useAuth } from "@/lib/auth";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Sheet, SheetContent, SheetTrigger } from "@/components/ui/sheet";

const navLinks = [
  { href: "/attractions", label: "Attractions" },
  { href: "/events", label: "Events" },
  { href: "/business", label: "Business" },
  { href: "/map", label: "Map" },
  { href: "/barangays", label: "Barangays" },
  { href: "/heritage", label: "Heritage" },
  { href: "/gallery", label: "Gallery" },
  { href: "/announcements", label: "Announcements" },
];

// Admins land on the full-control section instead of the public browse page.
// Sections without an admin twin keep their public href.
const adminTwins: Record<string, string> = {
  "/attractions": "/admin/attractions",
  "/events": "/admin/events",
  "/business": "/admin/establishments",
  "/heritage": "/admin/heritage",
  "/gallery": "/admin/gallery",
  "/announcements": "/admin/announcements",
  "/barangays": "/admin/barangays",
};

const roleLabels: Record<string, string> = {
  admin: "Admin",
  business_owner: "Owner",
  contributor: "Contributor",
  user: "Explorer",
};

export function Navbar() {
  const pathname = usePathname();
  const { user, logout } = useAuth();
  const [open, setOpen] = useState(false);

  const isOwnerConsole =
    pathname.startsWith("/business/dashboard") ||
    pathname.startsWith("/business/peers") ||
    /\/business\/[^/]+\/(edit|menu|rooms|reviews|verify)/.test(pathname);

  if (pathname.startsWith("/admin") || isOwnerConsole) {
    return null;
  }

  return (
    <header className="sticky top-0 z-50 w-full border-b border-border/50 bg-background/80 backdrop-blur-xl supports-[backdrop-filter]:bg-background/60">
      <div className="container mx-auto flex h-16 items-center justify-between px-4">
        {/* Logo */}
        <Link href="/" className="flex items-center gap-2.5 font-bold text-lg tracking-tight">
          <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-primary text-primary-foreground">
            <Compass className="h-4.5 w-4.5" />
          </div>
          <span>Mangatarem</span>
        </Link>

        {/* Desktop nav */}
        <nav className="hidden lg:flex items-center gap-0.5">
          {navLinks.map((link) => {
            const href = user?.role === "admin" ? (adminTwins[link.href] ?? link.href) : link.href;
            const active = pathname === href || pathname.startsWith(href);
            return (
              <Link
                key={link.href}
                href={href}
                className={`relative px-3 py-2 text-sm font-medium rounded-lg transition-colors ${
                  active
                    ? "text-primary bg-primary/10"
                    : "text-muted-foreground hover:text-foreground hover:bg-muted"
                }`}
              >
                {link.label}
                {active && (
                  <span className="absolute bottom-0 left-3 right-3 h-0.5 rounded-full bg-primary" />
                )}
              </Link>
            );
          })}
        </nav>

        {/* Right side */}
        <div className="flex items-center gap-2">
          <Link href="/search">
            <Button variant="ghost" size="icon" className="text-muted-foreground hover:text-foreground">
              <Search className="h-4.5 w-4.5" />
            </Button>
          </Link>

          {user ? (
            <div className="hidden md:flex items-center gap-2">
              <Link
                href={
                  user.role === "admin"
                    ? "/admin"
                    : user.role === "business_owner"
                    ? "/business/dashboard"
                    : user.role === "contributor"
                    ? "/contributor/dashboard"
                    : "/dashboard"
                }
              >
                <Button variant="ghost" size="sm" className="gap-2 rounded-lg">
                  <div className="flex h-6 w-6 items-center justify-center rounded-full bg-primary/10 text-primary">
                    <User className="h-3.5 w-3.5" />
                  </div>
                  <span className="max-w-[100px] truncate">{user.name}</span>
                  <Badge variant="secondary" className="ml-1 text-[10px] px-1.5 py-0">{roleLabels[user.role]}</Badge>
                </Button>
              </Link>

              {user.role === "admin" && (
                <>
                  <Link href="/admin">
                    <Button variant="outline" size="sm" className="gap-1.5 rounded-lg">
                      <Shield className="h-3.5 w-3.5" /> Admin
                    </Button>
                  </Link>
                  <Link href="/admin/bookings">
                    <Button variant="ghost" size="sm" className="gap-1.5 rounded-lg">
                      <CalendarCheck className="h-3.5 w-3.5" /> Bookings
                    </Button>
                  </Link>
                  <Link href="/admin/reviews">
                    <Button variant="ghost" size="sm" className="gap-1.5 rounded-lg">
                      <Star className="h-3.5 w-3.5" /> Reviews
                    </Button>
                  </Link>
                </>
              )}
              {user.role === "business_owner" && (
                <Link href="/business/dashboard">
                  <Button variant="outline" size="sm" className="gap-1.5 rounded-lg">
                    <Store className="h-3.5 w-3.5" /> My Business
                  </Button>
                </Link>
              )}
              {user.role === "contributor" && (
                <Link href="/contributor/dashboard">
                  <Button variant="outline" size="sm" className="gap-1.5 rounded-lg">
                    <UserCog className="h-3.5 w-3.5" /> Contributor
                  </Button>
                </Link>
              )}
              {user.role === "user" && (
                <Link href="/passport">
                  <Button variant="ghost" size="sm" className="gap-1.5 rounded-lg">
                    <BookOpen className="h-3.5 w-3.5" /> Passport
                  </Button>
                </Link>
              )}

              <Button variant="ghost" size="icon" onClick={logout} className="text-muted-foreground hover:text-foreground">
                <LogOut className="h-4 w-4" />
              </Button>
            </div>
          ) : (
            <div className="hidden md:flex items-center gap-2">
              <Link href="/auth/login">
                <Button variant="ghost" size="sm" className="rounded-lg">Log in</Button>
              </Link>
              <Link href="/auth/register">
                <Button size="sm" className="rounded-lg">Sign up</Button>
              </Link>
            </div>
          )}

          {/* Mobile menu */}
          <Sheet open={open} onOpenChange={setOpen}>
            <SheetTrigger render={<Button variant="ghost" size="icon" className="lg:hidden text-muted-foreground" />}>
              <Menu className="h-5 w-5" />
            </SheetTrigger>
            <SheetContent side="right" className="w-72 p-0">
              <div className="flex flex-col h-full">
                <div className="flex items-center justify-between p-4 border-b">
                  <Link href="/" className="flex items-center gap-2 font-bold" onClick={() => setOpen(false)}>
                    <div className="flex h-7 w-7 items-center justify-center rounded-lg bg-primary text-primary-foreground">
                      <Compass className="h-4 w-4" />
                    </div>
                    Mangatarem
                  </Link>
                </div>
                <nav className="flex-1 p-4 space-y-1">
                  {navLinks.map((link) => {
                    const href = user?.role === "admin" ? (adminTwins[link.href] ?? link.href) : link.href;
                    const active = pathname === href || pathname.startsWith(href);
                    return (
                      <Link
                        key={link.href}
                        href={href}
                        onClick={() => setOpen(false)}
                        className={`block px-3 py-2.5 text-sm font-medium rounded-lg transition-colors ${
                          active
                            ? "text-primary bg-primary/10"
                            : "text-muted-foreground hover:text-foreground hover:bg-muted"
                        }`}
                      >
                        {link.label}
                      </Link>
                    );
                  })}
                </nav>
                <div className="p-4 border-t space-y-2">
                  {user ? (
                    <>
                      <Link
                        href={
                          user.role === "admin"
                            ? "/admin"
                            : user.role === "business_owner"
                            ? "/business/dashboard"
                            : user.role === "contributor"
                            ? "/contributor/dashboard"
                            : "/dashboard"
                        }
                        onClick={() => setOpen(false)}
                      >
                        <Button variant="outline" className="w-full justify-start gap-2 rounded-lg">
                          <User className="h-4 w-4" /> Dashboard
                        </Button>
                      </Link>

                      {user.role === "admin" && (
                        <>
                          <Link href="/admin" onClick={() => setOpen(false)}>
                            <Button variant="outline" className="w-full justify-start gap-2 rounded-lg">
                              <Shield className="h-4 w-4" /> Admin
                            </Button>
                          </Link>
                          <Link href="/admin/bookings" onClick={() => setOpen(false)}>
                            <Button variant="ghost" className="w-full justify-start gap-2 rounded-lg">
                              <CalendarCheck className="h-4 w-4" /> Bookings
                            </Button>
                          </Link>
                          <Link href="/admin/reviews" onClick={() => setOpen(false)}>
                            <Button variant="ghost" className="w-full justify-start gap-2 rounded-lg">
                              <Star className="h-4 w-4" /> Reviews
                            </Button>
                          </Link>
                        </>
                      )}
                      {user.role === "business_owner" && (
                        <Link href="/business/dashboard" onClick={() => setOpen(false)}>
                          <Button variant="outline" className="w-full justify-start gap-2 rounded-lg">
                            <Store className="h-4 w-4" /> My Business
                          </Button>
                        </Link>
                      )}
                      {user.role === "contributor" && (
                        <Link href="/contributor/dashboard" onClick={() => setOpen(false)}>
                          <Button variant="outline" className="w-full justify-start gap-2 rounded-lg">
                            <UserCog className="h-4 w-4" /> Contributor
                          </Button>
                        </Link>
                      )}
                      {user.role === "user" && (
                        <Link href="/passport" onClick={() => setOpen(false)}>
                          <Button variant="ghost" className="w-full justify-start gap-2 rounded-lg">
                            <BookOpen className="h-4 w-4" /> Passport
                          </Button>
                        </Link>
                      )}

                      <Button
                        variant="ghost"
                        className="w-full justify-start gap-2 text-destructive rounded-lg"
                        onClick={() => { logout(); setOpen(false); }}
                      >
                        <LogOut className="h-4 w-4" /> Log out
                      </Button>
                    </>
                  ) : (
                    <>
                      <Link href="/auth/login" onClick={() => setOpen(false)}>
                        <Button variant="outline" className="w-full rounded-lg">Log in</Button>
                      </Link>
                      <Link href="/auth/register" onClick={() => setOpen(false)}>
                        <Button className="w-full rounded-lg">Sign up</Button>
                      </Link>
                    </>
                  )}
                </div>
              </div>
            </SheetContent>
          </Sheet>
        </div>
      </div>
    </header>
  );
}
