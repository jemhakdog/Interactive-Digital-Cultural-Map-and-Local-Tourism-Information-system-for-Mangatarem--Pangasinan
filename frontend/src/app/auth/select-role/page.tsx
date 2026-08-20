import type { Metadata } from "next";
import type { ReactNode } from "react";
import Link from "next/link";
import { Compass, Store, ShieldCheck, ArrowRight, LogIn } from "lucide-react";
import { AUTH_ROLES } from "@/app/auth/auth-constants";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent } from "@/components/ui/card";

export const metadata: Metadata = {
  title: "Complete Registration — Mangatarem",
};

const ROLE_ICON: Record<string, ReactNode> = {
  user: <Compass className="h-7 w-7 text-primary" />,
  business_owner: <Store className="h-7 w-7 text-amber-600 dark:text-amber-400" />,
  contributor: <ShieldCheck className="h-7 w-7 text-teal-600 dark:text-teal-400" />,
};

export default function SelectRolePage() {
  return (
    <div className="container mx-auto px-4 py-8 sm:py-12 max-w-4xl space-y-8">
      <div className="text-center space-y-3">
        <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-primary/10 text-primary text-xs font-semibold">
          <Compass className="h-3.5 w-3.5" />
          <span>Almost There!</span>
        </div>
        <h1 className="text-3xl sm:text-4xl font-extrabold tracking-tight text-foreground">
          Choose your account type
        </h1>
        <p className="text-muted-foreground text-sm sm:text-base leading-relaxed max-w-xl mx-auto">
          Select the role that best fits how you&apos;ll engage with Mangatarem&apos;s tourism
          and cultural community, then complete your sign-up.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {AUTH_ROLES.map((role) => (
          <Link key={role.id} href="/auth/register" className="group block">
            <Card className="rounded-2xl border-border/60 h-full hover:border-primary/40 hover:shadow-md transition-all">
              <CardContent className="p-6 flex flex-col justify-between h-full space-y-4">
                <div className="space-y-3">
                  <div className="flex items-center justify-between">
                    <div className="w-14 h-14 rounded-2xl bg-primary/10 flex items-center justify-center">
                      {ROLE_ICON[role.id]}
                    </div>
                  </div>
                  <div>
                    <h2 className="text-lg font-bold text-foreground">{role.title}</h2>
                    <p className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">
                      {role.subtitle}
                    </p>
                  </div>
                  <p className="text-sm text-muted-foreground leading-relaxed">{role.description}</p>
                </div>
                <div className="flex items-center justify-between gap-2">
                  <Badge variant="outline" className="text-[10px] bg-primary/5 text-primary border-primary/20">
                    {role.badge}
                  </Badge>
                  <span className="inline-flex items-center gap-1 text-xs font-bold text-primary group-hover:translate-x-1 transition-transform">
                    Select <ArrowRight className="h-3.5 w-3.5" />
                  </span>
                </div>
              </CardContent>
            </Card>
          </Link>
        ))}
      </div>

      <div className="text-center">
        <Link
          href="/auth/login"
          className="inline-flex items-center gap-1.5 text-xs text-muted-foreground hover:text-foreground transition-colors"
        >
          <LogIn className="h-3.5 w-3.5" /> Already have an account? Sign in
        </Link>
      </div>
    </div>
  );
}
