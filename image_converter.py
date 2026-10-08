from pathlib import Path
from tkinter import Tk, filedialog, messagebox
from PIL import Image, ImageEnhance

WIDTH = 128
HEIGHT = 160
SATURATION = 1.03
CONTRAST = 1.02
BRIGHTNESS = 1.00
USE_DITHER = True
FIT_MODE = "crop"  # "crop" fills the TFT; "fit" preserves the whole image.
PROGRAM_FOLDER = Path(__file__).resolve().parent


def rgb888_to_rgb565(r, g, b):
    return ((r >> 3) << 11) | ((g >> 2) << 5) | (b >> 3)


def prepare_image(img):
    img = img.convert("RGB")
    if FIT_MODE == "fit":
        img.thumbnail((WIDTH, HEIGHT), Image.Resampling.LANCZOS)
        canvas = Image.new("RGB", (WIDTH, HEIGHT), "black")
        canvas.paste(img, ((WIDTH - img.width) // 2, (HEIGHT - img.height) // 2))
        img = canvas
    else:
        # Center-crop to the target aspect ratio before resizing.
        target_ratio = WIDTH / HEIGHT
        ratio = img.width / img.height
        if ratio > target_ratio:
            new_width = round(img.height * target_ratio)
            left = (img.width - new_width) // 2
            img = img.crop((left, 0, left + new_width, img.height))
        elif ratio < target_ratio:
            new_height = round(img.width / target_ratio)
            top = (img.height - new_height) // 2
            img = img.crop((0, top, img.width, top + new_height))
        img = img.resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)

    img = ImageEnhance.Color(img).enhance(SATURATION)
    img = ImageEnhance.Contrast(img).enhance(CONTRAST)
    return ImageEnhance.Brightness(img).enhance(BRIGHTNESS)


def floyd_steinberg_rgb565(img):
    pixels = [list(img.getpixel((x, y))) for y in range(HEIGHT) for x in range(WIDTH)]
    out = []
    for y in range(HEIGHT):
        for x in range(WIDTH):
            idx = y * WIDTH + x
            old = pixels[idx]
            new = [
                (old[0] >> 3) << 3,
                (old[1] >> 2) << 2,
                (old[2] >> 3) << 3,
            ]
            out.append(rgb888_to_rgb565(*new))
            error = [old[i] - new[i] for i in range(3)]
            for dx, dy, weight in ((1, 0, 7), (-1, 1, 3), (0, 1, 5), (1, 1, 1)):
                nx, ny = x + dx, y + dy
                if 0 <= nx < WIDTH and 0 <= ny < HEIGHT:
                    n = ny * WIDTH + nx
                    for channel in range(3):
                        pixels[n][channel] = max(
                            0, min(255, pixels[n][channel] + error[channel] * weight / 16)
                        )
    return out


def write_header(output, pixels):
    with output.open("w", encoding="utf-8", newline="\n") as f:
        f.write("#pragma once\n#include <stdint.h>\n\n")
        f.write(f"#define TFT_IMAGE_WIDTH {WIDTH}\n#define TFT_IMAGE_HEIGHT {HEIGHT}\n")
        f.write(f"const uint16_t image[{WIDTH * HEIGHT}] = {{\n")
        for i, value in enumerate(pixels):
            if i % 8 == 0:
                f.write("    ")
            f.write(f"0x{value:04X}")
            if i != len(pixels) - 1:
                f.write(", ")
            if i % 8 == 7 or i == len(pixels) - 1:
                f.write("\n")
        f.write("};\n")


def convert_image():
    input_file = filedialog.askopenfilename(
        title="Select Image",
        filetypes=[("Image Files", "*.png *.jpg *.jpeg *.bmp *.webp"), ("All Files", "*.*")]
    )
    if not input_file:
        return
    try:
        img = prepare_image(Image.open(input_file))
        pixels = floyd_steinberg_rgb565(img) if USE_DITHER else [
            rgb888_to_rgb565(*img.getpixel((x, y)))
            for y in range(HEIGHT) for x in range(WIDTH)
        ]
        output = PROGRAM_FOLDER / "image.h"
        write_header(output, pixels)
        messagebox.showinfo(
            "Done",
            "image.h was created successfully!\n\n"
            f"Resolution: {WIDTH} × {HEIGHT}\n"
            f"Pixels: {WIDTH * HEIGHT}\n"
            f"Image data: {WIDTH * HEIGHT * 2 / 1024:.1f} KB"
        )
    except (OSError, ValueError) as exc:
        messagebox.showerror("Error", f"Could not convert image:\n\n{exc}")


root = Tk()
root.withdraw()
try:
    convert_image()
finally:
    root.destroy()
