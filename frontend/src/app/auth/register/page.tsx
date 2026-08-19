"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { useAuth } from "@/lib/auth";
import { registerSchema, type RegisterInput } from "@/lib/validations";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { GoogleAuthButton } from "@/components/auth/google-auth-button";
import { MANGATAREM_BARANGAYS, AUTH_ROLES } from "@/app/auth/auth-constants";
import {
  Compass,
  User,
  Mail,
  Lock,
  Eye,
  EyeOff,
  ArrowLeft,
  Loader2,
  AlertCircle,
  ShieldCheck,
  Store,
  Sparkles,
  CheckCircle2,
} from "lucide-react";

export default function RegisterPage() {
  const router = useRouter();
  const { register: registerUser } = useAuth();
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);

  const {
    register,
    handleSubmit,
    watch,
    setValue,
    formState: { errors },
  } = useForm<RegisterInput>({
    resolver: zodResolver(registerSchema),
    defaultValues: {
      name: "",
      email: "",
      password: "",
      confirm: "",
      role: "user",
      barangay: "",
    },
  });

  const selectedRole = watch("role");

  const onSubmit = async (data: RegisterInput) => {
    setError("");
    setLoading(true);
    try {
      await registerUser(
        data.name,
        data.email,
        data.password,
        data.role,
        data.role === "contributor" ? data.barangay : undefined
      );
      router.push("/dashboard");
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Registration failed. Please verify your information and try again."
      );
    } finally {
      setLoading(false);
    }
  };

  const getRoleIcon = (roleId: string) => {
    switch (roleId) {
      case "contributor":
        return <ShieldCheck className="h-4 w-4 text-teal-600 dark:text-teal-400" />;
      case "business_owner":
        return <Store className="h-4 w-4 text-amber-600 dark:text-amber-400" />;
      default:
        return <Compass className="h-4 w-4 text-primary" />;
    }
  };

  return (
    <div className="container mx-auto px-4 py-8 sm:py-12 max-w-5xl space-y-8">
      {/* ── Page Header ── */}
      <div className="space-y-2 max-w-2xl">
        <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-primary/10 text-primary text-xs font-semibold">
          <Compass className="h-3.5 w-3.5" />
          <span>Join the Community</span>
        </div>
        <h1 className="text-3xl sm:text-4xl font-extrabold tracking-tight text-foreground">
          Create your account
        </h1>
        <p className="text-muted-foreground text-sm sm:text-base leading-relaxed">
          Register as an explorer, barangay heritage steward, or local business owner to unlock digital cultural tools and records.
        </p>
      </div>

      {/* ── Main Layout: Role Showcase + Registration Form Card ── */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
        {/* Left Column: Community Roles & Benefits Showcase */}
        <div className="lg:col-span-5 space-y-6">
          <Card className="rounded-3xl border-border/60 bg-gradient-to-br from-card via-card/95 to-primary/5 p-6 sm:p-7 shadow-sm">
            <CardContent className="p-0 space-y-6">
              <div className="space-y-2">
                <div className="flex items-center gap-2">
                  <Badge variant="secondary" className="bg-primary/10 text-primary font-semibold">
                    <Sparkles className="h-3 w-3 mr-1" />
                    Membership Pathways
                  </Badge>
                </div>
                <h2 className="text-xl font-bold text-foreground">
                  Choose Your Heritage Journey
                </h2>
                <p className="text-xs text-muted-foreground leading-relaxed">
                  Tailor your platform experience based on how you interact with Mangatarem&apos;s tourism and cultural community.
                </p>
              </div>

              {/* Role descriptions */}
              <div className="space-y-3.5 pt-1">
                <div
                  onClick={() => setValue("role", "user")}
                  className={`p-3.5 rounded-2xl border transition-all cursor-pointer ${
                    selectedRole === "user"
                      ? "border-primary bg-primary/5 shadow-xs ring-1 ring-primary/20"
                      : "border-border/40 bg-background/60 hover:bg-background/90"
                  }`}
                >
                  <div className="flex items-center gap-2.5 mb-1.5">
                    <div className="p-1.5 rounded-lg bg-primary/10 text-primary">
                      <Compass className="h-4 w-4" />
                    </div>
                    <h3 className="text-xs font-bold text-foreground">Explorer (Tourist)</h3>
                    <Badge variant="outline" className="ml-auto text-[10px] bg-primary/5 text-primary border-primary/20">
                      Instant Access
                    </Badge>
                  </div>
                  <p className="text-[11px] text-muted-foreground leading-relaxed">
                    Collect digital passport check-in stamps, write verified reviews, and save trails.
                  </p>
                </div>

                <div
                  onClick={() => setValue("role", "contributor")}
                  className={`p-3.5 rounded-2xl border transition-all cursor-pointer ${
                    selectedRole === "contributor"
                      ? "border-teal-500 bg-teal-500/5 shadow-xs ring-1 ring-teal-500/20"
                      : "border-border/40 bg-background/60 hover:bg-background/90"
                  }`}
                >
                  <div className="flex items-center gap-2.5 mb-1.5">
                    <div className="p-1.5 rounded-lg bg-teal-500/10 text-teal-600 dark:text-teal-400">
                      <ShieldCheck className="h-4 w-4" />
                    </div>
                    <h3 className="text-xs font-bold text-foreground">Heritage Guardian</h3>
                    <Badge variant="outline" className="ml-auto text-[10px] bg-teal-500/5 text-teal-700 dark:text-teal-300 border-teal-500/20">
                      Barangay Rep
                    </Badge>
                  </div>
                  <p className="text-[11px] text-muted-foreground leading-relaxed">
                    Document historical landmarks, update municipal cultural profiles, and publish events.
                  </p>
                </div>

                <div
                  onClick={() => setValue("role", "business_owner")}
                  className={`p-3.5 rounded-2xl border transition-all cursor-pointer ${
                    selectedRole === "business_owner"
                      ? "border-amber-500 bg-amber-500/5 shadow-xs ring-1 ring-amber-500/20"
                      : "border-border/40 bg-background/60 hover:bg-background/90"
                  }`}
                >
                  <div className="flex items-center gap-2.5 mb-1.5">
                    <div className="p-1.5 rounded-lg bg-amber-500/10 text-amber-600 dark:text-amber-400">
                      <Store className="h-4 w-4" />
                    </div>
                    <h3 className="text-xs font-bold text-foreground">Merchant / Business Owner</h3>
                    <Badge variant="outline" className="ml-auto text-[10px] bg-amber-500/5 text-amber-700 dark:text-amber-300 border-amber-500/20">
                      Establishment
                    </Badge>
                  </div>
                  <p className="text-[11px] text-muted-foreground leading-relaxed">
                    Showcase resorts, restaurants, cafes, and transient rooms in the Business Directory.
                  </p>
                </div>
              </div>

              {/* Assurance footnote */}
              <div className="pt-2 border-t border-border/60 flex items-center gap-2 text-xs text-muted-foreground">
                <CheckCircle2 className="h-4 w-4 text-emerald-600 dark:text-emerald-400 shrink-0" />
                <span>Protected by municipal heritage data guidelines.</span>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Right Column: Registration Form Card */}
        <div className="lg:col-span-7">
          <Card className="rounded-3xl border-border/60 bg-card p-6 sm:p-8 shadow-sm">
            <CardContent className="p-0 space-y-6">
              {/* Form Title */}
              <div className="space-y-1">
                <h2 className="text-2xl font-bold tracking-tight text-foreground">
                  Create your account
                </h2>
                <p className="text-sm text-muted-foreground">
                  Fill in your details below to register
                </p>
              </div>

              {/* Error Banner */}
              {error && (
                <div className="bg-destructive/10 border border-destructive/20 text-destructive text-sm rounded-xl px-4 py-3 flex items-start gap-3">
                  <AlertCircle className="w-5 h-5 shrink-0 mt-0.5" />
                  <span>{error}</span>
                </div>
              )}

              <form onSubmit={handleSubmit(onSubmit)} className="space-y-5">
                {/* Role selection tab row */}
                <div className="space-y-2">
                  <Label className="text-xs font-bold text-muted-foreground uppercase tracking-wider">
                    I am registering as:
                  </Label>
                  <div className="grid grid-cols-3 gap-2">
                    {AUTH_ROLES.map((r) => {
                      const isSelected = selectedRole === r.id;
                      return (
                        <button
                          key={r.id}
                          type="button"
                          onClick={() => setValue("role", r.id as "user" | "contributor" | "business_owner")}
                          className={`p-2.5 rounded-xl border text-center flex flex-col items-center justify-center gap-1 transition-all cursor-pointer ${
                            isSelected
                              ? "border-primary bg-primary/10 font-bold text-foreground ring-1 ring-primary/30"
                              : "border-border/60 bg-background/60 hover:bg-background text-muted-foreground"
                          }`}
                        >
                          {getRoleIcon(r.id)}
                          <span className="text-xs font-semibold">{r.title}</span>
                        </button>
                      );
                    })}
                  </div>
                </div>

                {/* Conditional Barangay Dropdown for Guardians */}
                {selectedRole === "contributor" && (
                  <div className="space-y-2 p-3.5 rounded-2xl bg-teal-500/5 border border-teal-500/20 animate-in fade-in slide-in-from-top-2 duration-300">
                    <div className="flex items-center justify-between">
                      <Label htmlFor="barangay" className="text-xs font-bold text-teal-800 dark:text-teal-300 uppercase tracking-wider">
                        Designated Barangay
                      </Label>
                      <Badge variant="outline" className="bg-teal-500/10 text-teal-700 dark:text-teal-300 text-[10px] border-teal-500/30">
                        Verification Required
                      </Badge>
                    </div>
                    <select
                      id="barangay"
                      {...register("barangay")}
                      className="w-full h-11 rounded-xl bg-background border border-input px-3 py-2 text-sm text-foreground focus:outline-none focus:ring-2 focus:ring-teal-500/20 focus:border-teal-500 cursor-pointer"
                    >
                      <option value="" disabled>
                        Select your barangay territory...
                      </option>
                      {MANGATAREM_BARANGAYS.map((b) => (
                        <option key={b} value={b}>
                          {b}
                        </option>
                      ))}
                    </select>
                    {errors.barangay && (
                      <p className="text-xs text-destructive">{errors.barangay.message}</p>
                    )}
                  </div>
                )}

                {/* Name & Email */}
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  {/* Name */}
                  <div className="space-y-1.5">
                    <Label htmlFor="name" className="text-sm font-semibold">
                      Full Name
                    </Label>
                    <div className="relative group">
                      <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-muted-foreground group-focus-within:text-primary">
                        <User className="h-4 w-4" />
                      </div>
                      <Input
                        id="name"
                        placeholder="Juan Dela Cruz"
                        autoComplete="name"
                        className="pl-10 h-11 rounded-xl bg-background border-input text-sm"
                        {...register("name")}
                      />
                    </div>
                    {errors.name && (
                      <p className="text-xs text-destructive">{errors.name.message}</p>
                    )}
                  </div>

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
                </div>

                {/* Password & Confirm Password */}
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  {/* Password */}
                  <div className="space-y-1.5">
                    <Label htmlFor="password" className="text-sm font-semibold">
                      Password
                    </Label>
                    <div className="relative group">
                      <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-muted-foreground group-focus-within:text-primary">
                        <Lock className="h-4 w-4" />
                      </div>
                      <Input
                        id="password"
                        type={showPassword ? "text" : "password"}
                        placeholder="••••••••"
                        autoComplete="new-password"
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

                  {/* Confirm Password */}
                  <div className="space-y-1.5">
                    <Label htmlFor="confirm" className="text-sm font-semibold">
                      Confirm Password
                    </Label>
                    <div className="relative group">
                      <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-muted-foreground group-focus-within:text-primary">
                        <Lock className="h-4 w-4" />
                      </div>
                      <Input
                        id="confirm"
                        type={showConfirmPassword ? "text" : "password"}
                        placeholder="••••••••"
                        autoComplete="new-password"
                        className="pl-10 pr-10 h-11 rounded-xl bg-background border-input text-sm"
                        {...register("confirm")}
                      />
                      <button
                        type="button"
                        onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                        className="absolute inset-y-0 right-0 pr-3.5 flex items-center text-muted-foreground hover:text-foreground cursor-pointer"
                        aria-label={showConfirmPassword ? "Hide password" : "Show password"}
                      >
                        {showConfirmPassword ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                      </button>
                    </div>
                    {errors.confirm && (
                      <p className="text-xs text-destructive">{errors.confirm.message}</p>
                    )}
                  </div>
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
                      Creating account...
                    </>
                  ) : (
                    "Create account"
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

              {/* Google Sign-up */}
              <div className="w-full">
                <GoogleAuthButton
                  mode="signup"
                  role={selectedRole}
                  onSuccess={() => router.push("/dashboard")}
                  onError={(msg) => setError(msg)}
                />
              </div>

              {/* Footer Links */}
              <div className="pt-2 text-center space-y-4 border-t border-border/60">
                <p className="text-sm text-muted-foreground">
                  Already have an account?{" "}
                  <Link
                    href="/auth/login"
                    className="text-primary font-semibold hover:underline"
                  >
                    Log in
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
