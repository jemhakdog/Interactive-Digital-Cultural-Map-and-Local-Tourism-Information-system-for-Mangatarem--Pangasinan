import os
from PIL import Image


def convert_to_webp(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".png"):
            png_path = os.path.join(directory, filename)
            webp_path = os.path.join(directory, os.path.splitext(filename)[0] + ".webp")

            with Image.open(png_path) as img:
                # RGB conversion for transparency if needed, but WebP handles it
                # Using quality=80 for a good balance of size and quality
                img.save(webp_path, "WEBP", quality=80)
                print(
                    f"Converted {filename} to WebP. Size: {os.path.getsize(webp_path)} bytes."
                )


if __name__ == "__main__":
    img_dir = r"d:\porjects\Interactive-Digital-Cultural-Map-and-Local-Tourism-Information-system-for-Mangatarem--Pangasinan\static\img"
    convert_to_webp(img_dir)
