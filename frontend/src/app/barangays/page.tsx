import type { Metadata } from "next";
import Link from "next/link";
import { MapPin, Compass, Building2, Trees, Sparkles, Navigation, Layers } from "lucide-react";
import { BarangayExplorer, type BarangayItem } from "@/components/public/barangay-explorer";
import { MANGATAREM_BARANGAYS } from "@/app/auth/auth-constants";
import { AdminManageBar } from "@/components/layout/admin-manage-bar";

export const metadata: Metadata = {
  title: "Barangays of Mangatarem | Cultural & Tourism Directory",
  description:
    "Explore the 82 barangays of Mangatarem, Pangasinan. Discover Spanish-era heritage, Daang Kalikasan eco-corridors, rich agrarian valleys, and local cultural assets.",
};

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

// Upland & Eco-Corridor Barangays (Manleluag Protected Landscape, Daang Kalikasan corridor, western foothills)
const UPLAND_ECO_BARANGAYS = new Set([
  "Pacalat",
  "Malabobo",
  "Cacaoiten",
  "Catarataraan",
  "Baracbac",
  "Malibong",
  "Sonson Ongkit",
  "Bantocaling",
  "Suaco",
  "Takipan",
  "Talogtog",
  "Cabayaoasan",
  "Historia",
  "Lawak Langka",
]);

const THEMATIC_CATEGORIES = ["Nature & Eco", "Heritage & History", "Agriculture & Food", "Traditions & Fiestas"];

function isPoblacionBarangay(name: string): boolean {
  const n = name.toLowerCase();
  return n.includes("(poblacion)") || n.includes("(pob)") || n.includes("poblacion");
}

function getBarangayDistrict(name: string): "poblacion" | "upland" | "valley" {
  if (isPoblacionBarangay(name)) return "poblacion";
  if (UPLAND_ECO_BARANGAYS.has(name)) return "upland";
  return "valley";
}

function buildCuratedBarangays(): BarangayItem[] {
  return MANGATAREM_BARANGAYS.map((name, i) => {
    const district = getBarangayDistrict(name);
    const category =
      district === "poblacion"
        ? "Heritage & History"
        : district === "upland"
        ? "Nature & Eco"
        : THEMATIC_CATEGORIES[i % THEMATIC_CATEGORIES.length];

    const tags = [category];
    if (district === "poblacion") tags.push("Historic Core");
    else if (district === "upland") tags.push("Eco-Tourism");
    else tags.push("Agrarian Basin");

    return {
      name,
      district,
      category,
      tags,
      attraction_count: district === "poblacion" ? 3 : district === "upland" ? 2 : 1,
    };
  });
}

async function getBarangays(): Promise<BarangayItem[]> {
  try {
    const res = await fetch(`${API_BASE}/api/barangays`, { next: { revalidate: 300 } });
    if (!res.ok) return buildCuratedBarangays();
    const data = await res.json();
    const items = (data.barangays ?? data.items ?? []) as BarangayItem[];
    if (!items.length) return buildCuratedBarangays();

    return items.map((b, i) => {
      const district = b.district ?? getBarangayDistrict(b.name);
      const category =
        b.category ||
        (district === "poblacion"
          ? "Heritage & History"
          : district === "upland"
          ? "Nature & Eco"
          : THEMATIC_CATEGORIES[i % THEMATIC_CATEGORIES.length]);

      return {
        ...b,
        district,
        category,
        tags: b.tags && b.tags.length > 0 ? b.tags : [category, district === "poblacion" ? "Historic Core" : district === "upland" ? "Eco-Tourism" : "Agrarian Basin"],
      };
    });
  } catch {
    return buildCuratedBarangays();
  }
}

export default async function BarangaysPage() {
  const barangays = await getBarangays();

  const poblacionCount = barangays.filter((b) => b.district === "poblacion" || isPoblacionBarangay(b.name)).length;
  const uplandCount = barangays.filter((b) => b.district === "upland" || UPLAND_ECO_BARANGAYS.has(b.name)).length;
  const valleyCount = barangays.length - poblacionCount - uplandCount;

  return (
    <div className="min-h-screen bg-gradient-to-b from-background via-muted/20 to-background pb-16">
      <div className="container mx-auto px-4 py-6 sm:py-10 space-y-8 max-w-7xl">
        <AdminManageBar label="Barangays" href="/admin/barangays" note="(manage barangay directory)" />

        {/* ── Cultural Hero & Telemetry Banner ── */}
        <section className="relative overflow-hidden rounded-3xl border border-border/70 bg-card/70 backdrop-blur-xl p-6 sm:p-10 shadow-sm">
          {/* Aurora Ambient Decorative Glow */}
          <div
            aria-hidden="true"
            className="pointer-events-none absolute -top-32 -right-32 h-96 w-96 rounded-full bg-primary/15 blur-3xl"
          />
          <div
            aria-hidden="true"
            className="pointer-events-none absolute -bottom-32 -left-32 h-96 w-96 rounded-full bg-emerald-500/10 blur-3xl"
          />

          <div className="relative z-10 flex flex-col lg:flex-row items-start lg:items-center justify-between gap-8">
            <div className="space-y-4 max-w-2xl">
              <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-primary/10 border border-primary/20 text-primary text-xs font-semibold tracking-wide">
                <MapPin className="h-3.5 w-3.5" />
                <span>Mangatarem, Pangasinan • 82 Distinct Communities</span>
              </div>
              <h1 className="text-3xl sm:text-4xl md:text-5xl font-extrabold tracking-tight text-foreground">
                Barangays of Mangatarem
              </h1>
              <p className="text-muted-foreground text-sm sm:text-base leading-relaxed">
                From the colonial heritage centers of the Poblacion grid to the lush Daang Kalikasan mountain eco-corridors and fertile river valleys, discover the living traditions, cultural assets, and attractions across all 82 barangays.
              </p>

              {/* Quick links */}
              <div className="flex flex-wrap items-center gap-3 pt-1">
                <Link
                  href="/map"
                  className="inline-flex items-center gap-2 px-4 py-2 rounded-xl bg-primary text-primary-foreground text-xs font-semibold hover:bg-primary/90 transition-all shadow-xs"
                >
                  <Navigation className="h-3.5 w-3.5" />
                  <span>Open Interactive Digital Map</span>
                </Link>
                <Link
                  href="/attractions"
                  className="inline-flex items-center gap-2 px-4 py-2 rounded-xl bg-muted border border-border text-foreground text-xs font-semibold hover:bg-muted/80 transition-all"
                >
                  <Sparkles className="h-3.5 w-3.5 text-primary" />
                  <span>Explore Cultural Spots</span>
                </Link>
              </div>
            </div>

            {/* Quick Stats Grid */}
            <div className="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-2 xl:grid-cols-4 gap-3 w-full lg:w-auto shrink-0">
              <div className="p-4 rounded-2xl bg-background/85 border border-border/80 text-center shadow-xs">
                <div className="text-2xl sm:text-3xl font-extrabold text-foreground tracking-tight">
                  {barangays.length}
                </div>
                <div className="text-[11px] font-medium text-muted-foreground uppercase tracking-wider mt-0.5">
                  Total Barangays
                </div>
              </div>
              <div className="p-4 rounded-2xl bg-background/85 border border-border/80 text-center shadow-xs">
                <div className="text-2xl sm:text-3xl font-extrabold text-primary tracking-tight">
                  {poblacionCount}
                </div>
                <div className="text-[11px] font-medium text-muted-foreground uppercase tracking-wider mt-0.5">
                  Poblacion Core
                </div>
              </div>
              <div className="p-4 rounded-2xl bg-background/85 border border-border/80 text-center shadow-xs">
                <div className="text-2xl sm:text-3xl font-extrabold text-emerald-600 dark:text-emerald-400 tracking-tight">
                  {uplandCount}
                </div>
                <div className="text-[11px] font-medium text-muted-foreground uppercase tracking-wider mt-0.5">
                  Eco & Upland
                </div>
              </div>
              <div className="p-4 rounded-2xl bg-background/85 border border-border/80 text-center shadow-xs">
                <div className="text-2xl sm:text-3xl font-extrabold text-teal-600 dark:text-teal-400 tracking-tight">
                  {valleyCount}
                </div>
                <div className="text-[11px] font-medium text-muted-foreground uppercase tracking-wider mt-0.5">
                  Agrarian Valley
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* ── Interactive Explorer ── */}
        <BarangayExplorer barangays={barangays} />
      </div>
    </div>
  );
}
