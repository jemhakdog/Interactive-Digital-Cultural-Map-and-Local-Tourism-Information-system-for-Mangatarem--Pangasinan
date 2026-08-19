import Link from "next/link";
import { Landmark } from "lucide-react";
import { Card, CardContent } from "@/components/ui/card";

async function getHeritageTypes() {
  try {
    const res = await fetch("http://localhost:8000/api/heritage/types", { next: { revalidate: 60 } });
    if (!res.ok) return [];
    const data = await res.json();
    return (data.types ?? data) as Record<string, unknown>[];
  } catch { return []; }
}

const typeIcons: Record<string, string> = {
  built: "🏛️",
  natural: "🌿",
  intangible: "🎭",
  movable: "🏺",
  mixed: "🔀",
};

export default async function HeritagePage() {
  const types = await getHeritageTypes();

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-2">Heritage</h1>
      <p className="text-muted-foreground mb-8">Cultural heritage of Mangatarem</p>

      {types.length === 0 ? (
        <div className="text-center py-16 text-muted-foreground">
          <Landmark className="h-12 w-12 mx-auto mb-4 opacity-30" />
          <p>No heritage types found.</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {(types as Record<string, unknown>[]).map((t) => {
            const typeKey = String(t.type ?? t.name ?? "").toLowerCase();
            const typeName = String(t.type ?? t.name ?? "Unknown");
            const count = t.count ?? t.total ?? 0;
            return (
              <Link key={typeKey} href={`/heritage/${typeKey}`}>
                <Card className="hover:shadow-md transition-shadow cursor-pointer h-full">
                  <CardContent className="p-6 text-center">
                    <span className="text-4xl">{typeIcons[typeKey] || "📜"}</span>
                    <h3 className="font-semibold mt-3 capitalize">{typeName}</h3>
                    <p className="text-sm text-muted-foreground mt-1">{Number(count)} items</p>
                  </CardContent>
                </Card>
              </Link>
            );
          })}
        </div>
      )}
    </div>
  );
}
