"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/lib/auth";
import { fetchAPI } from "@/lib/api";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Loader2, Camera, MapPin, ScanLine, CheckCircle2, XCircle, QrCode } from "lucide-react";

type TargetType = "attraction" | "establishment";

interface CheckinResult {
  success: boolean;
  message?: string;
  unlocked_badges?: { title?: string; description?: string }[];
}

export default function PassportScanPage() {
  const { user, loading: authLoading } = useAuth();
  const router = useRouter();

  const videoRef = useRef<HTMLVideoElement>(null);
  const streamRef = useRef<MediaStream | null>(null);

  const [cameraOn, setCameraOn] = useState(false);
  const [cameraError, setCameraError] = useState("");
  const [targetType, setTargetType] = useState<TargetType>("attraction");
  const [targetId, setTargetId] = useState("");
  const [checking, setChecking] = useState(false);
  const [geoError, setGeoError] = useState("");
  const [result, setResult] = useState<CheckinResult | null>(null);

  // Read optional ?type= & ?id= from the URL (client-only to avoid useSearchParams Suspense).
  useEffect(() => {
    if (typeof window === "undefined") return;
    const sp = new URLSearchParams(window.location.search);
    const t = sp.get("type");
    const id = sp.get("id");
    if (t === "attraction" || t === "establishment") setTargetType(t);
    if (id) setTargetId(id);
  }, []);

  useEffect(() => {
    if (!authLoading && !user) router.push("/auth/login");
  }, [user, authLoading, router]);

  const stopCamera = useCallback(() => {
    streamRef.current?.getTracks().forEach((t) => t.stop());
    streamRef.current = null;
    setCameraOn(false);
  }, []);

  useEffect(() => () => stopCamera(), [stopCamera]);

  const startCamera = useCallback(async () => {
    setCameraError("");
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: "environment" } });
      streamRef.current = stream;
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
        await videoRef.current.play().catch(() => {});
      }
      setCameraOn(true);
    } catch {
      setCameraError("Camera unavailable or permission denied. You can still check in with a code below.");
      setCameraOn(false);
    }
  }, []);

  const getPosition = (): Promise<{ latitude: number; longitude: number }> =>
    new Promise((resolve, reject) => {
      if (!navigator.geolocation) {
        reject(new Error("Geolocation is not supported by this browser."));
        return;
      }
      navigator.geolocation.getCurrentPosition(
        (pos) => resolve({ latitude: pos.coords.latitude, longitude: pos.coords.longitude }),
        (err) => reject(new Error(err.message || "Could not get your location.")),
        { enableHighAccuracy: true, timeout: 15000, maximumAge: 0 }
      );
    });

  const handleCheckin = async () => {
    setResult(null);
    setGeoError("");
    const idNum = Number(targetId);
    if (!targetId || Number.isNaN(idNum)) {
      setGeoError("Enter a valid check-in code / target ID first.");
      return;
    }
    setChecking(true);
    try {
      const { latitude, longitude } = await getPosition();
      // Guarded fetch to the GPS-validated QR check-in endpoint.
      const res = await fetchAPI<Record<string, unknown>>("/api/gamification/checkin", {
        method: "POST",
        body: JSON.stringify({ type: targetType, id: idNum, latitude, longitude }),
      });
      setResult({
        success: true,
        message: (res?.message as string) ?? "Check-in complete!",
        unlocked_badges: (res?.unlocked_badges as { title?: string; description?: string }[]) ?? [],
      });
    } catch (err) {
      setResult({
        success: false,
        message: err instanceof Error ? err.message : "Check-in failed. Please try again.",
      });
    } finally {
      setChecking(false);
    }
  };

  if (authLoading || !user) {
    return (
      <div className="flex justify-center py-16">
        <Loader2 className="h-6 w-6 animate-spin text-muted-foreground" />
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8 max-w-md">
      {/* Page header */}
      <div className="text-center mb-8">
        <div className="mx-auto h-16 w-16 rounded-full bg-primary/10 flex items-center justify-center mb-4">
          <QrCode className="h-8 w-8 text-primary" />
        </div>
        <h1 className="text-3xl font-bold tracking-tight">Passport Check-in</h1>
        <p className="text-muted-foreground mt-1">
          Scan a QR code at the site to collect your stamp
        </p>
      </div>

      {/* Scanner frame */}
      <Card className="border-border/50">
        <CardContent className="p-5">
          <div className="relative aspect-square w-full overflow-hidden rounded-xl bg-muted flex items-center justify-center">
            <video
              ref={videoRef}
              playsInline
              muted
              className={`h-full w-full object-cover ${cameraOn ? "block" : "hidden"}`}
            />
            {!cameraOn && (
              <div className="flex flex-col items-center text-muted-foreground">
                <ScanLine className="h-12 w-12 mb-2 opacity-40" />
                <p className="text-sm">Camera off</p>
              </div>
            )}

            {/* Scanning line */}
            {cameraOn && (
              <div className="pointer-events-none absolute inset-x-6 top-1/2 h-0.5 -translate-y-1/2 animate-pulse rounded-full bg-primary" />
            )}

            {/* Corner guides */}
            <div className="pointer-events-none absolute inset-6 rounded-xl border-2 border-dashed border-primary/40" />
          </div>

          <div className="mt-4 flex gap-2">
            {!cameraOn ? (
              <Button onClick={startCamera} className="w-full rounded-xl gap-2">
                <Camera className="h-4 w-4" /> Start Camera
              </Button>
            ) : (
              <Button onClick={stopCamera} variant="outline" className="w-full rounded-xl gap-2">
                Stop Camera
              </Button>
            )}
          </div>

          {cameraError && <p className="mt-3 text-xs text-amber-500">{cameraError}</p>}
        </CardContent>
      </Card>

      {/* Target / code entry */}
      <Card className="border-border/50 mt-4">
        <CardContent className="p-5 space-y-4">
          <div className="space-y-2">
            <Label>Check in to</Label>
            <div className="flex gap-2">
              {(["attraction", "establishment"] as TargetType[]).map((t) => (
                <Button
                  key={t}
                  type="button"
                  variant={targetType === t ? "default" : "outline"}
                  size="sm"
                  className="rounded-xl capitalize"
                  onClick={() => setTargetType(t)}
                >
                  {t}
                </Button>
              ))}
            </div>
          </div>

          <div className="space-y-2">
            <Label htmlFor="target-id">Check-in code / target ID</Label>
            <Input
              id="target-id"
              inputMode="numeric"
              value={targetId}
              onChange={(e) => setTargetId(e.target.value.replace(/\D/g, ""))}
              placeholder="e.g. 5"
              className="rounded-xl"
            />
          </div>

          <Button onClick={handleCheckin} disabled={checking} className="w-full rounded-xl gap-2">
            {checking ? <Loader2 className="h-4 w-4 animate-spin" /> : <MapPin className="h-4 w-4" />}
            Check in with my location
          </Button>

          {geoError && <p className="text-xs text-destructive">{geoError}</p>}
        </CardContent>
      </Card>

      {/* Result */}
      {result && (
        <Card
          className={`border-border/50 mt-4 ${
            result.success ? "border-primary/40" : "border-destructive/40"
          }`}
        >
          <CardContent className="p-5 text-center">
            <div className="mx-auto mb-3 flex h-12 w-12 items-center justify-center rounded-full">
              {result.success ? (
                <CheckCircle2 className="h-10 w-10 text-primary" />
              ) : (
                <XCircle className="h-10 w-10 text-destructive" />
              )}
            </div>
            <p className="font-medium">{result.message}</p>
            {result.success && result.unlocked_badges && result.unlocked_badges.length > 0 && (
              <div className="mt-3 space-y-2">
                {result.unlocked_badges.map((b, i) => (
                  <div key={i} className="rounded-xl bg-primary/10 p-3 text-left">
                    <p className="text-sm font-semibold text-primary">{b.title}</p>
                    {b.description && (
                      <p className="text-xs text-muted-foreground mt-1">{b.description}</p>
                    )}
                  </div>
                ))}
              </div>
            )}
            {result.success && (
              <Button variant="outline" className="mt-4 rounded-xl" onClick={() => router.push("/passport")}>
                View Passport
              </Button>
            )}
          </CardContent>
        </Card>
      )}
    </div>
  );
}
