"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { fetchAPI } from "@/lib/api";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { AlertCircle, CheckCircle2, Eye, EyeOff, Loader2, Lock } from "lucide-react";

const schema = z
  .object({
    password: z.string().min(8, "Password must be at least 8 characters"),
    confirm: z.string(),
  })
  .refine((d) => d.password === d.confirm, {
    message: "Passwords do not match",
    path: ["confirm"],
  });

type FormInput = z.infer<typeof schema>;

export function ResetPasswordForm({ token }: { token: string }) {
  const router = useRouter();
  const [error, setError] = useState("");
  const [success, setSuccess] = useState(false);
  const [loading, setLoading] = useState(false);
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirm, setShowConfirm] = useState(false);

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<FormInput>({
    resolver: zodResolver(schema),
  });

  const onSubmit = async (data: FormInput) => {
    setError("");
    setLoading(true);
    try {
      await fetchAPI<{ detail: string }>("/api/auth/reset-password", {
        method: "POST",
        body: JSON.stringify({ token, password: data.password }),
      });
      setSuccess(true);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to reset password. The link may be invalid or expired.");
    } finally {
      setLoading(false);
    }
  };

  if (success) {
    return (
      <div className="space-y-6 text-center py-2">
        <div className="bg-emerald-500/10 border border-emerald-500/20 text-emerald-700 dark:text-emerald-300 rounded-2xl p-6 flex flex-col items-center gap-3">
          <CheckCircle2 className="w-10 h-10 text-emerald-600 dark:text-emerald-400" />
          <div>
            <h3 className="font-bold text-base mb-1">Password updated</h3>
            <p className="text-xs text-muted-foreground">
              Your password has been reset. You can now sign in with your new credentials.
            </p>
          </div>
        </div>
        <Link
          href="/auth/login"
          className="inline-flex w-full items-center justify-center h-11 rounded-xl text-sm font-semibold bg-primary text-primary-foreground hover:bg-primary/90 shadow-sm transition-all"
        >
          Return to Sign in
        </Link>
      </div>
    );
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
      {error && (
        <div className="bg-destructive/10 border border-destructive/20 text-destructive text-sm rounded-xl px-4 py-3 flex items-start gap-3">
          <AlertCircle className="w-5 h-5 shrink-0 mt-0.5" />
          <span>{error}</span>
        </div>
      )}

      {!token && (
        <div className="bg-amber-500/10 border border-amber-500/20 text-amber-700 dark:text-amber-300 text-sm rounded-xl px-4 py-3">
          This password reset link is missing its token. Please use the link from your email.
        </div>
      )}

      <div className="space-y-1.5">
        <Label htmlFor="password" className="text-sm font-semibold">
          New Password
        </Label>
        <div className="relative group">
          <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-muted-foreground group-focus-within:text-primary">
            <Lock className="h-4 w-4" />
          </div>
          <Input
            id="password"
            type={showPassword ? "text" : "password"}
            placeholder="Min. 8 characters"
            autoComplete="new-password"
            className="pl-10 pr-10 h-11 rounded-xl bg-background border-input text-sm"
            {...register("password")}
          />
          <button
            type="button"
            onClick={() => setShowPassword((v) => !v)}
            className="absolute inset-y-0 right-0 pr-3.5 flex items-center text-muted-foreground hover:text-foreground"
            aria-label="Toggle password"
          >
            {showPassword ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
          </button>
        </div>
        {errors.password && <p className="text-xs text-destructive">{errors.password.message}</p>}
      </div>

      <div className="space-y-1.5">
        <Label htmlFor="confirm" className="text-sm font-semibold">
          Confirm New Password
        </Label>
        <div className="relative group">
          <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-muted-foreground group-focus-within:text-primary">
            <Lock className="h-4 w-4" />
          </div>
          <Input
            id="confirm"
            type={showConfirm ? "text" : "password"}
            placeholder="Repeat your password"
            autoComplete="new-password"
            className="pl-10 pr-10 h-11 rounded-xl bg-background border-input text-sm"
            {...register("confirm")}
          />
          <button
            type="button"
            onClick={() => setShowConfirm((v) => !v)}
            className="absolute inset-y-0 right-0 pr-3.5 flex items-center text-muted-foreground hover:text-foreground"
            aria-label="Toggle confirm password"
          >
            {showConfirm ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
          </button>
        </div>
        {errors.confirm && <p className="text-xs text-destructive">{errors.confirm.message}</p>}
      </div>

      <Button
        type="submit"
        disabled={!!loading || !token}
        className="w-full h-11 rounded-xl text-sm font-semibold shadow-sm transition-all"
      >
        {loading ? (
          <>
            <Loader2 className="h-4 w-4 animate-spin mr-2" />
            Resetting...
          </>
        ) : (
          "Reset Password"
        )}
      </Button>

      <div className="pt-2 text-center border-t border-border/60">
        <Link
          href="/auth/login"
          className="inline-flex items-center gap-1.5 text-xs text-muted-foreground hover:text-foreground transition-colors"
        >
          Back to Sign in
        </Link>
      </div>
    </form>
  );
}
