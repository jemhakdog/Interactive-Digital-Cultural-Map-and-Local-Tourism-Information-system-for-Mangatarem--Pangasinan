from PIL import Image, ImageDraw


def create_favicon():
    # Create a 32x32 image with a green background
    size = (32, 32)
    image = Image.new("RGBA", size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(image)

    # Draw a simple leaf-like shape
    # Emerald green color from the theme
    draw.ellipse([4, 4, 28, 28], fill=(6, 78, 59))

    image.save(
        r"d:\porjects\Interactive-Digital-Cultural-Map-and-Local-Tourism-Information-system-for-Mangatarem--Pangasinan\static\favicon.ico"
    )
    print("Favicon created at static/favicon.ico")


if __name__ == "__main__":
    create_favicon()
