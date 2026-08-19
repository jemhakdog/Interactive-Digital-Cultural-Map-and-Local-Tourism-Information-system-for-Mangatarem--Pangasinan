"use client";

import { useEffect, useRef, useState } from "react";
import Script from "next/script";
import { useAuth } from "@/lib/auth";
import { Loader2 } from "lucide-react";
import { Button } from "@/components/ui/button";

interface GoogleAuthButtonProps {
  mode?: "signin" | "signup";
  role?: string;
  onSuccess?: () => void;
  onError?: (error: string) => void;
  className?: string;
}

const GOOGLE_CLIENT_ID =
  process.env.NEXT_PUBLIC_GOOGLE_CLIENT_ID ||
  "794547070676-80dbt1j3a724hacci5684s7b7v93j1fh.apps.googleusercontent.com";

declare global {
  interface Window {
    google?: {
      accounts: {
        id: {
          initialize: (config: {
            client_id: string;
            callback: (response: { credential: string }) => void;
            auto_select?: boolean;
            cancel_on_tap_outside?: boolean;
          }) => void;
          renderButton: (
            parent: HTMLElement,
            options: {
              type?: "standard" | "icon";
              theme?: "outline" | "filled_black" | "filled_blue";
              size?: "large" | "medium" | "small";
              text?: "signin_with" | "signup_with" | "continue_with";
              shape?: "rectangular" | "pill" | "circle" | "square";
              logo_alignment?: "left" | "center";
              width?: number | string;
            }
          ) => void;
          prompt: () => void;
        };
      };
    };
  }
}

export function GoogleAuthButton({
  mode = "signin",
  role = "user",
  onSuccess,
  onError,
  className = "",
}: GoogleAuthButtonProps) {
  const { googleLogin } = useAuth();
  const [loading, setLoading] = useState(false);
  const [scriptLoaded, setScriptLoaded] = useState(false);
  const buttonContainerRef = useRef<HTMLDivElement>(null);

  const handleCredentialResponse = async (response: { credential: string }) => {
    if (!response.credential) {
      onError?.("No credential received from Google");
      return;
    }
    setLoading(true);
    try {
      await googleLogin(response.credential, role);
      onSuccess?.();
    } catch (err) {
      const msg = err instanceof Error ? err.message : "Google authentication failed";
      onError?.(msg);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (!scriptLoaded || typeof window === "undefined" || !window.google?.accounts?.id) {
      return;
    }

    try {
      window.google.accounts.id.initialize({
        client_id: GOOGLE_CLIENT_ID,
        callback: handleCredentialResponse,
        cancel_on_tap_outside: true,
      });

      if (buttonContainerRef.current) {
        buttonContainerRef.current.innerHTML = "";
        const containerWidth = buttonContainerRef.current.offsetWidth || 340;

        window.google.accounts.id.renderButton(buttonContainerRef.current, {
          type: "standard",
          theme: "outline",
          size: "large",
          text: mode === "signup" ? "signup_with" : "signin_with",
          shape: "rectangular",
          logo_alignment: "left",
          width: Math.min(420, Math.max(280, containerWidth)),
        });
      }
    } catch (e) {
      console.warn("Failed to initialize Google Sign-In button:", e);
    }
  }, [scriptLoaded, mode, role]);

  const handleManualClick = () => {
    if (loading) return;
    if (window.google?.accounts?.id) {
      try {
        window.google.accounts.id.prompt();
      } catch {
        onError?.("Unable to launch Google Sign-In prompt. Please try again.");
      }
    } else {
      onError?.("Google Sign-In is initializing. Please wait a moment.");
    }
  };

  return (
    <>
      <Script
        src="https://accounts.google.com/gsi/client"
        strategy="afterInteractive"
        onLoad={() => setScriptLoaded(true)}
      />

      <div className={`w-full flex flex-col items-center justify-center ${className}`}>
        {/* Render container for official GSI button */}
        <div
          ref={buttonContainerRef}
          className="w-full flex justify-center min-h-[44px]"
          id="google-btn-container"
        />

        {/* Fallback button if GSI has not rendered yet or for instant click */}
        {(!scriptLoaded || loading) && (
          <Button
            type="button"
            variant="outline"
            onClick={handleManualClick}
            disabled={loading}
            className="w-full h-11 rounded-xl border-border/80 bg-background hover:bg-muted/60 text-foreground text-sm font-medium transition-all shadow-xs"
          >
            {loading ? (
              <Loader2 className="h-4 w-4 animate-spin mr-2" />
            ) : (
              <svg className="h-4 w-4 mr-2.5 shrink-0" viewBox="0 0 24 24">
                <path
                  fill="#4285F4"
                  d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"
                />
                <path
                  fill="#34A853"
                  d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"
                />
                <path
                  fill="#FBBC05"
                  d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.06H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.94l2.85-2.22.81-.63z"
                />
                <path
                  fill="#EA4335"
                  d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.06l3.66 2.84c.87-2.6 3.3-4.52 6.16-4.52z"
                />
              </svg>
            )}
            <span>{mode === "signup" ? "Sign up with Google" : "Continue with Google"}</span>
          </Button>
        )}
      </div>
    </>
  );
}
