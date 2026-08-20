import type { Metadata } from "next";
import Link from "next/link";
import { Clock, Mail, ArrowRight } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";

export const metadata: Metadata = {
  title: "Account Pending Approval — Mangatarem",
};

export default function PendingApprovalPage() {
  return (
    <div className="container mx-auto px-4 py-8 sm:py-12 max-w-lg space-y-8">
      <div className="flex justify-center">
        <div className="relative w-24 h-24">
          <div className="absolute inset-0 rounded-full bg-primary/20 animate-pulse scale-150" />
          <div className="w-24 h-24 rounded-full bg-primary/10 border border-primary/30 flex items-center justify-center shadow-[0_0_30px_rgba(22,163,74,0.3)] relative z-10">
            <Clock className="h-12 w-12 text-primary" />
          </div>
        </div>
      </div>

      <div className="text-center space-y-3">
        <h1 className="text-3xl sm:text-4xl font-extrabold tracking-tight text-foreground">
          Account Pending Review
        </h1>
        <p className="text-muted-foreground text-sm sm:text-base leading-relaxed max-w-md mx-auto">
          Thank you for registering. Your account is currently under review by our
          administrators and will be activated shortly.
        </p>
      </div>

      <Card className="rounded-2xl border-border/60 bg-card shadow-sm">
        <CardContent className="p-6 space-y-4">
          <div className="bg-primary/5 border border-primary/20 rounded-xl p-4">
            <p className="text-sm text-muted-foreground leading-relaxed">
              To maintain the quality and authenticity of our cultural heritage platform,
              business owner and barangay contributor accounts require manual verification.
              This process typically takes <strong className="text-foreground">24–48 hours</strong>.
            </p>
          </div>
          <div className="flex items-start gap-3 text-left p-3 rounded-xl bg-muted">
            <div className="bg-primary/10 p-2 rounded-lg mt-0.5 shrink-0">
              <Mail className="h-5 w-5 text-primary" />
            </div>
            <div>
              <h3 className="font-bold text-foreground text-sm mb-0.5">What happens next?</h3>
              <p className="text-xs text-muted-foreground leading-relaxed">
                You&apos;ll receive an email notification as soon as your account is approved.
                Once approved, you can sign in and start contributing.
              </p>
            </div>
          </div>
        </CardContent>
      </Card>

      <div className="space-y-3">
        <Link href="/" className="block">
          <Button className="w-full h-11 rounded-xl font-semibold">
            Return to Home Page <ArrowRight className="h-4 w-4 ml-1.5" />
          </Button>
        </Link>
        <Link href="/auth/login">
          <Button variant="outline" className="w-full h-11 rounded-xl">
            Try Logging In Again
          </Button>
        </Link>
      </div>
    </div>
  );
}
