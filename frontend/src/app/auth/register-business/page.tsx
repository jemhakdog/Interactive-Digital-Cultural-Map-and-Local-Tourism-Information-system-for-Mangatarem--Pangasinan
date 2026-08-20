import type { Metadata } from "next";
import { Building2 } from "lucide-react";
import { RegisterBusinessForm } from "@/components/public/register-business-form";
import { Card, CardContent } from "@/components/ui/card";

export const metadata: Metadata = {
  title: "Register Your Business — Mangatarem",
};

export default function RegisterBusinessPage() {
  return (
    <div className="container mx-auto px-4 py-8 sm:py-12 max-w-lg space-y-8">
      <div className="text-center space-y-3">
        <div className="inline-flex items-center justify-center w-20 h-20 rounded-3xl bg-primary/10 border border-primary/20 mb-2">
          <Building2 className="h-9 w-9 text-primary" />
        </div>
        <h1 className="text-3xl sm:text-4xl font-extrabold tracking-tight text-foreground">
          Register Your Business
        </h1>
        <p className="text-muted-foreground text-sm leading-relaxed max-w-sm mx-auto">
          List your inn, restaurant, or café on Mangatarem and reach tourists visiting the
          town.
        </p>
      </div>

      <Card className="rounded-3xl border-border/60 bg-card p-6 sm:p-8 shadow-sm">
        <CardContent className="p-0">
          <RegisterBusinessForm />
        </CardContent>
      </Card>
    </div>
  );
}
