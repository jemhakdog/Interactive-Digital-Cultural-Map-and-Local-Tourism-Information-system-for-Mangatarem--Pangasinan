"use client";

import { useState, useRef } from "react";
import { Button } from "@/components/ui/button";
import { API_BASE } from "@/lib/api";
import { Upload, X, ImageIcon } from "lucide-react";

interface ImageUploadProps {
  onUpload: (urls: string[]) => void;
  multiple?: boolean;
  accept?: string;
}

export function ImageUpload({ onUpload, multiple = false, accept = "image/*" }: ImageUploadProps) {
  const [previews, setPreviews] = useState<string[]>([]);
  const [uploading, setUploading] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = Array.from(e.target.files || []);
    if (files.length === 0) return;

    // Create previews
    const newPreviews = files.map((file) => URL.createObjectURL(file));
    setPreviews((prev) => [...prev, ...newPreviews]);

    // Upload to server
    setUploading(true);
    const uploadedUrls: string[] = [];

    Promise.all(
      files.map(async (file) => {
        const formData = new FormData();
        formData.append("file", file);

        try {
          const res = await fetch(`${API_BASE}/api/uploads/single`, {
            method: "POST",
            body: formData,
          });

          if (res.ok) {
            const data = await res.json();
            uploadedUrls.push(data.url || data.path);
          }
        } catch (err) {
          console.error("Upload failed:", err);
        }
      })
    ).finally(() => {
      setUploading(false);
      if (uploadedUrls.length > 0) {
        onUpload(uploadedUrls);
      }
    });
  };

  const removePreview = (index: number) => {
    setPreviews((prev) => prev.filter((_, i) => i !== index));
  };

  return (
    <div className="space-y-4">
      <input
        ref={fileInputRef}
        type="file"
        accept={accept}
        multiple={multiple}
        onChange={handleFileChange}
        className="hidden"
      />

      <Button
        type="button"
        variant="outline"
        onClick={() => fileInputRef.current?.click()}
        disabled={uploading}
        className="w-full"
      >
        <Upload className="h-4 w-4 mr-2" />
        {uploading ? "Uploading..." : "Upload Images"}
      </Button>

      {previews.length > 0 && (
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
          {previews.map((preview, i) => (
            <div key={i} className="relative aspect-square rounded-lg overflow-hidden border bg-muted group">
              <img src={preview} alt="" className="w-full h-full object-cover" />
              <button
                type="button"
                onClick={() => removePreview(i)}
                className="absolute top-1 right-1 h-6 w-6 bg-black/50 text-white rounded-full flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity"
              >
                <X className="h-3 w-3" />
              </button>
            </div>
          ))}
        </div>
      )}

      {previews.length === 0 && (
        <div className="border-2 border-dashed rounded-lg p-8 text-center text-muted-foreground">
          <ImageIcon className="h-8 w-8 mx-auto mb-2 opacity-30" />
          <p className="text-sm">No images selected</p>
        </div>
      )}
    </div>
  );
}
