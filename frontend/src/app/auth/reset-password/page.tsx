import type { Metadata } from "next";
import { ShieldCheck } from "lucide-react";
import { ResetPasswordForm } from "@/components/public/reset-password-form";
import { Card, CardContent } from "@/components/ui/card";

export const metadata: Metadata = {
  title: "Reset Password — Mangatarem",
};

export default function ResetPasswordPage({
  searchParams,
}: {
  searchParams: { token?: string };
}) {
  const token = searchParams.token ?? "";

  return (
    <div className="container mx-auto px-4 py-8 sm:py-12 max-w-lg space-y-8">
      <div className="text-center space-y-3">
        <div className="inline-flex items-center justify-center w-20 h-20 rounded-3xl bg-primary/10 border border-primary/20 mb-2">
          <ShieldCheck className="h-9 w-9 text-primary" />
        </div>
        <h1 className="text-3xl sm:text-4xl font-extrabold tracking-tight text-foreground">
          New Password
        </h1>
        <p className="text-muted-foreground text-sm leading-relaxed">
          Choose a strong password for your account.
        </p>
      </div>

      <Card className="rounded-3xl border-border/60 bg-card p-6 sm:p-8 shadow-sm">
        <CardContent className="p-0">
          <ResetPasswordForm token={token} />
        </CardContent>
      </Card>
    </div>
  );
}
