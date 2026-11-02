<div align="center">

# TFT Image Converter

**Turn ordinary images into embedded display graphics.**

Convert PNG, JPEG, BMP, or WEBP images into compact RGB565 C/C++ arrays for TFT projects.

![Python](https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)
![Output](https://img.shields.io/badge/Output-RGB565-orange)

</div>

---

## ✨ Why use it?

Microcontrollers often have limited storage and no filesystem available for image assets. TFT Image Converter prepares an image as a C/C++ header so it can be compiled directly into your firmware.

## 🚀 Features

- Supports PNG, JPG/JPEG, BMP, and WEBP.
- Resizes images to **128 × 160**.
- Converts RGB888 pixels to RGB565.
- Generates an `image.h` header.
- Includes dithering and image-adjustment settings in the converter.
- Works on your PC; the generated header can be used by ESP32, ESP8266, Raspberry Pi Pico, and other compatible projects.

## ⚡ Quick start

### 1. Install

Requirements: Python 3 and Pillow.

```bash
git clone https://github.com/whiteby4e/TFT-Image-Converter.git
cd TFT-Image-Converter
python -m pip install -r requirements.txt
```

### 2. Convert an image

```bash
python image_converter.py
```

Choose an image in the file dialog. The converter creates `image.h` in the project folder.

### 3. Include it in your sketch

```cpp
#include "image.h"

// Example for a compatible TFT_eSPI display:
tft.pushImage(0, 0, TFT_IMAGE_WIDTH, TFT_IMAGE_HEIGHT, image);
```

See the included [Arduino example](examples/Arduino_Example) and [ESP32 example](examples/ESP32_Example).

## 🧠 How conversion works

```text
Input image
    ↓
Crop or fit to 128 × 160
    ↓
Image adjustment / dithering
    ↓
RGB888 → RGB565
    ↓
Generate image.h
    ↓
Compile into firmware flash
    ↓
Draw on the TFT
```

A 128 × 160 RGB565 image contains 20,480 pixels and requires **40,960 bytes (40 KiB)** of raw pixel data, excluding small header and alignment overhead.

## 🖼️ Supported formats

| Format | Extensions |
|---|---|
| PNG | `.png` |
| JPEG | `.jpg`, `.jpeg` |
| Bitmap | `.bmp` |
| WebP | `.webp` |

## 🔧 Customization

The converter's image settings are defined near the top of `image_converter.py`, including target dimensions, saturation, contrast, brightness, dithering, and fit mode.

The current output target is 128 × 160. If you change the dimensions, make sure your display code uses the matching generated width and height.

## 📁 Repository contents

- `image_converter.py` — desktop conversion tool.
- `requirements.txt` — Python dependency list.
- `examples/` — Arduino and ESP32 usage examples.
- `examples/image.h` — sample generated image header.

## 📄 License

MIT — see [LICENSE](LICENSE).
