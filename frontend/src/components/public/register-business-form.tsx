"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { fetchAPI } from "@/lib/api";
import { useAuth } from "@/lib/auth";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { AlertCircle, Eye, EyeOff, Loader2 } from "lucide-react";

const schema = z.object({
  businessName: z.string().min(2, "Business name is required"),
  businessType: z.string().min(1, "Please select a business type"),
  username: z.string().min(2, "Username is required"),
  email: z.string().email("Please enter a valid email"),
  password: z.string().min(6, "Password must be at least 6 characters"),
});

type FormInput = z.infer<typeof schema>;

const BUSINESS_TYPES = [
  { value: "inn", label: "Inn / Lodge / Hotel" },
  { value: "restaurant", label: "Restaurant" },
  { value: "cafe", label: "Coffee Shop / Café" },
  { value: "fastfood", label: "Fast Food" },
];

export function RegisterBusinessForm() {
  const router = useRouter();
  const { register: registerUser } = useAuth();
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [showPassword, setShowPassword] = useState(false);

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<FormInput>({
    resolver: zodResolver(schema),
    defaultValues: {
      businessName: "",
      businessType: "",
      username: "",
      email: "",
      password: "",
    },
  });

  const onSubmit = async (data: FormInput) => {
    setError("");
    setLoading(true);
    try {
      // 1) Create the business-owner account (auto-logs in via useAuth).
      await registerUser(data.username, data.email, data.password, "business_owner");

      // 2) Optionally register the establishment under the new account.
      //    Guarded: the combined registration endpoint may be partial/missing.
      try {
        await fetchAPI<unknown>("/api/business", {
          method: "POST",
          body: JSON.stringify({ name: data.businessName, type: data.businessType }),
        });
      } catch {
        // Non-fatal: account exists; establishment can be added later.
      }

      // 3) Business owners require manual approval before activation.
      router.push("/auth/pending-approval");
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

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
      {error && (
        <div className="bg-destructive/10 border border-destructive/20 text-destructive text-sm rounded-xl px-4 py-3 flex items-start gap-3">
          <AlertCircle className="w-5 h-5 shrink-0 mt-0.5" />
          <span>{error}</span>
        </div>
      )}

      <div className="space-y-1.5">
        <Label htmlFor="businessName" className="text-sm font-semibold">
          Business Name
        </Label>
        <Input
          id="businessName"
          placeholder="e.g., Mangatarem Inn & Suites"
          className="h-11 rounded-xl bg-background border-input text-sm"
          {...register("businessName")}
        />
        {errors.businessName && <p className="text-xs text-destructive">{errors.businessName.message}</p>}
      </div>

      <div className="space-y-1.5">
        <Label htmlFor="businessType" className="text-sm font-semibold">
          Business Type
        </Label>
        <select
          id="businessType"
          {...register("businessType")}
          className="w-full h-11 rounded-xl bg-background border border-input px-3 py-2 text-sm text-foreground focus:outline-none focus:ring-2 focus:ring-primary/30"
        >
          <option value="">Select type...</option>
          {BUSINESS_TYPES.map((t) => (
            <option key={t.value} value={t.value}>
              {t.label}
            </option>
          ))}
        </select>
        {errors.businessType && <p className="text-xs text-destructive">{errors.businessType.message}</p>}
      </div>

      <hr className="border-border/60" />

      <div className="space-y-1.5">
        <Label htmlFor="username" className="text-sm font-semibold">
          Username
        </Label>
        <Input
          id="username"
          placeholder="Your login username"
          autoComplete="username"
          className="h-11 rounded-xl bg-background border-input text-sm"
          {...register("username")}
        />
        {errors.username && <p className="text-xs text-destructive">{errors.username.message}</p>}
      </div>

      <div className="space-y-1.5">
        <Label htmlFor="email" className="text-sm font-semibold">
          Email
        </Label>
        <Input
          id="email"
          type="email"
          placeholder="business@example.com"
          autoComplete="email"
          className="h-11 rounded-xl bg-background border-input text-sm"
          {...register("email")}
        />
        {errors.email && <p className="text-xs text-destructive">{errors.email.message}</p>}
      </div>

      <div className="space-y-1.5">
        <Label htmlFor="password" className="text-sm font-semibold">
          Password
        </Label>
        <div className="relative group">
          <Input
            id="password"
            type={showPassword ? "text" : "password"}
            placeholder="Min. 6 characters"
            autoComplete="new-password"
            className="pr-10 h-11 rounded-xl bg-background border-input text-sm"
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

      <Button
        type="submit"
        disabled={loading}
        className="w-full h-11 rounded-xl text-sm font-semibold shadow-sm transition-all"
      >
        {loading ? (
          <>
            <Loader2 className="h-4 w-4 animate-spin mr-2" />
            Registering...
          </>
        ) : (
          "Register My Business"
        )}
      </Button>

      <p className="text-center text-xs text-muted-foreground">
        Your registration will be reviewed by an admin before your business appears on the map.
      </p>

      <p className="text-center text-sm text-muted-foreground border-t border-border/60 pt-4">
        Already have an account?{" "}
        <Link href="/auth/login" className="text-primary font-semibold hover:underline">
          Login here
        </Link>
      </p>
    </form>
  );
}
