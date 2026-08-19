import { ImageIcon } from "lucide-react";
import { Card, CardContent } from "@/components/ui/card";

interface GalleryItem {
  id: string | number;
  image_url?: string;
  title?: string;
  caption?: string;
}

async function getGallery() {
  try {
    const res = await fetch("http://localhost:8000/api/gallery", { next: { revalidate: 60 } });
    if (!res.ok) return { items: [] };
    return res.json();
  } catch { return { items: [] }; }
}

export default async function GalleryPage() {
  const data = await getGallery();
  const items = (data.items ?? []) as GalleryItem[];

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-2">Gallery</h1>
      <p className="text-muted-foreground mb-8">Photos from Mangatarem</p>

      {items.length === 0 ? (
        <div className="text-center py-16 text-muted-foreground">
          <ImageIcon className="h-12 w-12 mx-auto mb-4 opacity-30" />
          <p>No gallery items yet.</p>
        </div>
      ) : (
        <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-4">
          {items.map((item) => (
            <Card key={item.id} className="overflow-hidden">
              <div className="aspect-square bg-muted">
                {item.image_url ? (
                  <img
                    src={item.image_url}
                    alt={item.title || item.caption || ""}
                    className="w-full h-full object-cover hover:scale-105 transition-transform duration-300"
                  />
                ) : (
                  <div className="w-full h-full flex items-center justify-center">
                    <ImageIcon className="h-8 w-8 text-muted-foreground/30" />
                  </div>
                )}
              </div>
              {item.title && (
                <CardContent className="p-3">
                  <p className="text-sm font-medium line-clamp-1">{item.title}</p>
                </CardContent>
              )}
            </Card>
          ))}
        </div>
      )}
    </div>
  );
}
