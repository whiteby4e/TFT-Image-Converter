
from PIL import Image, ImageEnhance
from tkinter import Tk, filedialog, messagebox
import os
import random

WIDTH = 128
HEIGHT = 160

# Image adjustment
SATURATION = 1.03
CONTRAST = 1.02
BRIGHTNESS = 1.00

# Dithering
USE_DITHER = True

# Save image.h in the same folder as this Python script
PROGRAM_FOLDER = os.path.dirname(os.path.abspath(__file__))


def rgb888_to_rgb565(r, g, b):
    """
    Convert RGB888 to RGB565.
    """
    r5 = r >> 3
    g6 = g >> 2
    b5 = b >> 3

    return (r5 << 11) | (g6 << 5) | b5


def convert_image():

    input_file = filedialog.askopenfilename(
        title="Select Image",
        filetypes=[
            ("Image Files", "*.png *.jpg *.jpeg *.bmp *.webp"),
            ("All Files", "*.*")
        ]
    )

    if not input_file:
        return

    try:
        # Open image
        img = Image.open(input_file).convert("RGB")

        # Resize to TFT resolution
        img = img.resize(
            (WIDTH, HEIGHT),
            Image.Resampling.LANCZOS
        )

        # Apply very mild image adjustments
        img = ImageEnhance.Color(img).enhance(SATURATION)
        img = ImageEnhance.Contrast(img).enhance(CONTRAST)
        img = ImageEnhance.Brightness(img).enhance(BRIGHTNESS)

        # Convert pixels to RGB565
        pixels = []

        for y in range(HEIGHT):

            for x in range(WIDTH):

                r, g, b = img.getpixel((x, y))

                # Very mild dithering
                if USE_DITHER:
                    noise = random.choice([-1, 0, 0, 0, 1])

                    r = max(0, min(255, r + noise))
                    g = max(0, min(255, g + noise))
                    b = max(0, min(255, b + noise))

                rgb565 = rgb888_to_rgb565(r, g, b)

                pixels.append(rgb565)

        # Output file
        output_file = os.path.join(
            PROGRAM_FOLDER,
            "image.h"
        )

        # Create C header file
        with open(output_file, "w", encoding="utf-8") as f:

            f.write("#pragma once\n")
            f.write("#include <stdint.h>\n\n")

            f.write(
                f"const uint16_t image[{WIDTH * HEIGHT}] = {{\n"
            )

            for i, value in enumerate(pixels):

                if i % 8 == 0:
                    f.write("    ")

                f.write(f"0x{value:04X}")

                if i != len(pixels) - 1:
                    f.write(", ")

                if i % 8 == 7:
                    f.write("\n")

            f.write("};\n")

        messagebox.showinfo(
            "Done",
            "image.h was created successfully!\n\n"
            f"Resolution: {WIDTH} × {HEIGHT}\n"
            f"Pixels: {WIDTH * HEIGHT}\n"
            f"Image data: {WIDTH * HEIGHT * 2 / 1024:.1f} KB"
        )

    except Exception as e:

        messagebox.showerror(
            "Error",
            f"Something went wrong:\n\n{e}"
        )


root = Tk()
root.withdraw()

convert_image()

root.destroy()

