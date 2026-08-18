import os
from PIL import Image

def compress_images(directory, quality=75):
    """
    Traverse a directory and compress all JPG/PNG images.
    Converts to WebP for maximum efficiency.
    """
    if not os.path.exists(directory):
        print(f"Directory {directory} does not exist.")
        return

    print(f"Starting compression in {directory}...")
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                filepath = os.path.join(root, file)
                filename_no_ext = os.path.splitext(file)[0]
                output_path = os.path.join(root, f"{filename_no_ext}.webp")
                
                try:
                    with Image.open(filepath) as img:
                        # Convert RGBA to RGB if saving as JPG-like WebP
                        if img.mode in ("RGBA", "P"):
                            img = img.convert("RGB")
                        
                        img.save(output_path, "WEBP", quality=quality, optimize=True)
                        original_size = os.path.getsize(filepath)
                        new_size = os.path.getsize(output_path)
                        reduction = (original_size - new_size) / original_size * 100
                        
                        print(f"Compressed {file} -> {filename_no_ext}.webp ({reduction:.1f}% reduction)")
                        
                        # Optionally: If the reduction is significant, we could delete the original
                        # but for safety, we keep it for now.
                except Exception as e:
                    print(f"Failed to compress {file}: {e}")

if __name__ == "__main__":
    # Target common image directories
    static_img_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "static", "img"))
    compress_images(static_img_dir)
