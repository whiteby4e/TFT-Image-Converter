# TFT Image Converter

Convert images to RGB565 C/C++ arrays for storing in microcontroller flash memory and displaying on TFT screens.

## Features

* Converts common image formats such as PNG, JPG, JPEG, BMP, and WEBP
* Resizes images to 128×160
* Converts RGB888 images to RGB565
* Generates a ready-to-use `image.h` C/C++ header file
* Designed for ESP32 and other microcontroller-based TFT projects
* No SD card is required for displaying the converted image

## How It Works

The converter takes a regular image and processes it into raw RGB565 pixel data.

```text
Input Image
    ↓
Resize to 128×160
    ↓
RGB888 → RGB565
    ↓
Generate image.h
    ↓
Store in microcontroller flash
    ↓
Display on TFT
```

The generated `image.h` contains the image as a C/C++ array that can be included directly in an embedded project.

## Example

After converting an image, the program generates:

```cpp
#include "image.h"

tft.pushImage(0, 0, 128, 160, image);
```

The image data is stored directly in the microcontroller's program flash memory.

A 128×160 RGB565 image requires:

```text
128 × 160 × 2 bytes = 40,960 bytes
≈ 40 KB
```

## Requirements

* Python 3.x
* Pillow

Install Pillow with:

```bash
pip install Pillow
```

## Supported Input Formats

* PNG
* JPG / JPEG
* BMP
* WEBP

## Hardware

The generated image data can be used with microcontrollers such as:

* ESP32
* ESP8266
* Raspberry Pi Pico
* Other embedded systems with compatible TFT libraries

The converter itself is hardware-independent; it only generates the image data.

## License

This project is licensed under the MIT License.

## Author

**WhiteByte**

If you find this project useful, feel free to use it, modify it, or build something with it.
