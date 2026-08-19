"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { useAuth } from "@/lib/auth";
import { loginSchema, type LoginInput } from "@/lib/validations";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { GoogleAuthButton } from "@/components/auth/google-auth-button";
import {
  Compass,
  Mail,
  Lock,
  Eye,
  EyeOff,
  ArrowLeft,
  Loader2,
  AlertCircle,
  MapPin,
  Landmark,
  Calendar,
  Building,
  Sparkles,
  ArrowRight,
} from "lucide-react";

export default function LoginPage() {
  const router = useRouter();
  const { login } = useAuth();
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [showPassword, setShowPassword] = useState(false);

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<LoginInput>({
    resolver: zodResolver(loginSchema),
    defaultValues: {
      email: "",
      password: "",
      remember: true,
    },
  });

  const onSubmit = async (data: LoginInput) => {
    setError("");
    setLoading(true);
    try {
      await login(data.email, data.password);
      router.push("/dashboard");
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Login failed. Please verify your credentials and try again."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container mx-auto px-4 py-8 sm:py-12 max-w-5xl space-y-8">
      {/* ── Page Header ── */}
      <div className="space-y-2 max-w-2xl">
        <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-primary/10 text-primary text-xs font-semibold">
          <Compass className="h-3.5 w-3.5" />
          <span>Tourism & Heritage Portal</span>
        </div>
        <h1 className="text-3xl sm:text-4xl font-extrabold tracking-tight text-foreground">
          Sign in to Mangatarem
        </h1>
        <p className="text-muted-foreground text-sm sm:text-base leading-relaxed">
          Access your explorer dashboard, bookmark heritage landmarks, track cultural events, or manage your local business.
        </p>
      </div>

      {/* ── Main Layout: Showcase + Sign In Card ── */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
        {/* Left Column: Portal Highlights Card (Matching Attractions/Events styling) */}
        <div className="lg:col-span-5 space-y-6">
          <Card className="rounded-3xl border-border/60 bg-gradient-to-br from-card via-card/95 to-primary/5 p-6 sm:p-7 shadow-sm">
            <CardContent className="p-0 space-y-6">
              <div className="space-y-2">
                <div className="flex items-center gap-2">
                  <Badge variant="secondary" className="bg-primary/10 text-primary font-semibold">
                    <Sparkles className="h-3 w-3 mr-1" />
                    Explorer Network
                  </Badge>
                </div>
                <h2 className="text-xl font-bold text-foreground">
                  Your Gateway to Mangatarem
                </h2>
                <p className="text-xs text-muted-foreground leading-relaxed">
                  Join visitors, local guardians, and entrepreneurs in celebrating the rich cultural tapestry of Mangatarem, Pangasinan.
                </p>
              </div>

              {/* Feature items matching site categories */}
              <div className="space-y-3.5 pt-1">
                <div className="flex items-start gap-3 p-3 rounded-2xl bg-background/60 border border-border/40">
                  <div className="p-2 rounded-xl bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 shrink-0">
                    <MapPin className="h-4 w-4" />
                  </div>
                  <div>
                    <h3 className="text-xs font-bold text-foreground">Interactive Map & Trails</h3>
                    <p className="text-[11px] text-muted-foreground">
                      Explore Manleluag Hot Springs, waterfalls, and scenic bike trails.
                    </p>
                  </div>
                </div>

                <div className="flex items-start gap-3 p-3 rounded-2xl bg-background/60 border border-border/40">
                  <div className="p-2 rounded-xl bg-amber-500/10 text-amber-600 dark:text-amber-400 shrink-0">
                    <Landmark className="h-4 w-4" />
                  </div>
                  <div>
                    <h3 className="text-xs font-bold text-foreground">Cultural Heritage Registry</h3>
                    <p className="text-[11px] text-muted-foreground">
                      Discover historical belfries, ancestral traditions, and local crafts.
                    </p>
                  </div>
                </div>

                <div className="flex items-start gap-3 p-3 rounded-2xl bg-background/60 border border-border/40">
                  <div className="p-2 rounded-xl bg-sky-500/10 text-sky-600 dark:text-sky-400 shrink-0">
                    <Calendar className="h-4 w-4" />
                  </div>
                  <div>
                    <h3 className="text-xs font-bold text-foreground">Festivals & Celebrations</h3>
                    <p className="text-[11px] text-muted-foreground">
                      Keep up with the Tupig Festival, barangay fiestas, and cultural activities.
                    </p>
                  </div>
                </div>

                <div className="flex items-start gap-3 p-3 rounded-2xl bg-background/60 border border-border/40">
                  <div className="p-2 rounded-xl bg-teal-500/10 text-teal-600 dark:text-teal-400 shrink-0">
                    <Building className="h-4 w-4" />
                  </div>
                  <div>
                    <h3 className="text-xs font-bold text-foreground">Local Business Directory</h3>
                    <p className="text-[11px] text-muted-foreground">
                      Find certified restaurants, transient stays, resorts, and stores.
                    </p>
                  </div>
                </div>
              </div>

              {/* Public explorer shortcut */}
              <div className="pt-2 border-t border-border/60 flex items-center justify-between">
                <span className="text-xs text-muted-foreground">Looking to explore first?</span>
                <Link
                  href="/map"
                  className="inline-flex items-center gap-1 text-xs font-semibold text-primary hover:underline"
                >
                  View Map <ArrowRight className="h-3.5 w-3.5" />
                </Link>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Right Column: Sign In Form Card */}
        <div className="lg:col-span-7">
          <Card className="rounded-3xl border-border/60 bg-card p-6 sm:p-8 shadow-sm">
            <CardContent className="p-0 space-y-6">
              {/* Form Title */}
              <div className="space-y-1">
                <h2 className="text-2xl font-bold tracking-tight text-foreground">
                  Sign in to your account
                </h2>
                <p className="text-sm text-muted-foreground">
                  Enter your email and password or continue with Google
                </p>
              </div>

              {/* Error Banner */}
              {error && (
                <div className="bg-destructive/10 border border-destructive/20 text-destructive text-sm rounded-xl px-4 py-3 flex items-start gap-3">
                  <AlertCircle className="w-5 h-5 shrink-0 mt-0.5" />
                  <span>{error}</span>
                </div>
              )}

              {/* Form Fields */}
              <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
                {/* Email */}
                <div className="space-y-1.5">
                  <Label htmlFor="email" className="text-sm font-semibold">
                    Email Address
                  </Label>
                  <div className="relative group">
                    <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-muted-foreground group-focus-within:text-primary">
                      <Mail className="h-4 w-4" />
                    </div>
                    <Input
                      id="email"
                      type="email"
                      placeholder="you@example.com"
                      autoComplete="email"
                      className="pl-10 h-11 rounded-xl bg-background border-input text-sm"
                      {...register("email")}
                    />
                  </div>
                  {errors.email && (
                    <p className="text-xs text-destructive">{errors.email.message}</p>
                  )}
                </div>

                {/* Password */}
                <div className="space-y-1.5">
                  <div className="flex items-center justify-between">
                    <Label htmlFor="password" className="text-sm font-semibold">
                      Password
                    </Label>
                    <Link
                      href="/auth/forgot-password"
                      className="text-xs font-semibold text-primary hover:underline"
                    >
                      Forgot password?
                    </Link>
                  </div>
                  <div className="relative group">
                    <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-muted-foreground group-focus-within:text-primary">
                      <Lock className="h-4 w-4" />
                    </div>
                    <Input
                      id="password"
                      type={showPassword ? "text" : "password"}
                      placeholder="••••••••"
                      autoComplete="current-password"
                      className="pl-10 pr-10 h-11 rounded-xl bg-background border-input text-sm"
                      {...register("password")}
                    />
                    <button
                      type="button"
                      onClick={() => setShowPassword(!showPassword)}
                      className="absolute inset-y-0 right-0 pr-3.5 flex items-center text-muted-foreground hover:text-foreground cursor-pointer"
                      aria-label={showPassword ? "Hide password" : "Show password"}
                    >
                      {showPassword ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                    </button>
                  </div>
                  {errors.password && (
                    <p className="text-xs text-destructive">{errors.password.message}</p>
                  )}
                </div>

                {/* Remember Me */}
                <div className="flex items-center pt-0.5">
                  <input
                    id="remember"
                    type="checkbox"
                    className="h-4 w-4 rounded border-input text-primary focus:ring-primary cursor-pointer accent-primary"
                    {...register("remember")}
                  />
                  <label
                    htmlFor="remember"
                    className="ml-2 block text-xs text-muted-foreground cursor-pointer select-none"
                  >
                    Remember me on this device
                  </label>
                </div>

                {/* Submit Button */}
                <Button
                  type="submit"
                  disabled={loading}
                  className="w-full h-11 rounded-xl text-sm font-semibold shadow-sm transition-all"
                >
                  {loading ? (
                    <>
                      <Loader2 className="h-4 w-4 animate-spin mr-2" />
                      Signing in...
                    </>
                  ) : (
                    "Sign in"
                  )}
                </Button>
              </form>

              {/* Divider */}
              <div className="relative py-1 flex items-center">
                <div className="flex-grow border-t border-border" />
                <span className="flex-shrink mx-4 text-muted-foreground text-xs font-semibold uppercase tracking-wider">
                  Or continue with
                </span>
                <div className="flex-grow border-t border-border" />
              </div>

              {/* Google Sign-in */}
              <div className="w-full">
                <GoogleAuthButton
                  mode="signin"
                  onSuccess={() => router.push("/dashboard")}
                  onError={(msg) => setError(msg)}
                />
              </div>

              {/* Footer Links */}
              <div className="pt-2 text-center space-y-4 border-t border-border/60">
                <p className="text-sm text-muted-foreground">
                  Don&apos;t have an account yet?{" "}
                  <Link
                    href="/auth/register"
                    className="text-primary font-semibold hover:underline"
                  >
                    Create an account
                  </Link>
                </p>

                <div>
                  <Link
                    href="/map"
                    className="inline-flex items-center gap-1.5 text-xs text-muted-foreground hover:text-foreground transition-colors group"
                  >
                    <ArrowLeft className="h-3.5 w-3.5 transform group-hover:-translate-x-0.5 transition-transform" />
                    Back to Tourism Map
                  </Link>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}
