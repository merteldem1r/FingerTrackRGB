# FingerTrackRGB - Computer Vision + Embedded STM32

**FingerTrackRGB** is an **Embedded Vision** project which enables **real-time control of RGB LED colors and brightness using hand gesture recognition**. It combines Computer Vision (OpenCV + MediaPipe) to detect index finger positions and STM32 microcontroller for hardware control, featuring a **16x2 I2C LCD**, **Red-Green-Blue LEDs**, and a **buzzer**. RGB values are updated via **UART communication** (in interrupt mode), and the system supports gesture-based **reset RGB values** with visual and audio feedback.

**IMPORTANT NOTE**: If you only want to test **Computer Vision part** please make the all `ser` keywords in the `main.py` file as comment lines. 

## App Preview

<img width="1710" height="909" alt="image" src="https://github.com/user-attachments/assets/52c399b3-44ef-460a-944e-05c2e5e837ef" />

<img width="1710" height="907" alt="image" src="https://github.com/user-attachments/assets/c91f0bbc-b2f0-447e-8bdc-643024515088" />

<img width="1710" height="910" alt="image" src="https://github.com/user-attachments/assets/43c49444-3862-4bf1-91d6-23eb93caef2d" />

<img width="1710" height="908" alt="image" src="https://github.com/user-attachments/assets/79a76447-5465-47b3-af9b-1562eb3060fb" />

## Overview

This project combines real-time hand tracking with embedded hardware to control an RGB LED via hand gestures. It includes two major parts:

* **Computer Vision Module**: Built using **Python, OpenCV, and Google's MediaPipe Hand Landmarker**
* **STM32 Embedded Module**: Developed using STM32CubeIDE with **UART interrupt**, **PWM for RGB LEDs**, **I2C-driven LCD**, and **buzzer control**

The system allows the user to control **RGB values** through visual interaction, transmit the values over **UART**, and reflect the **updates on hardware in real time.**

## Features

### Computer Vision

* Real-time hand tracking with MediaPipe Hand Landmarker
* Detection of index finger position
* Three interactive color boxes (Red, Green, Blue)
* Dynamic RGB value update based on finger position
* Reset gesture to reset all colors and trigger buzzer
* FPS display and live RGB preview

### STM32 Microcontroller

* RGB LED control using PWM on TIM2
* UART communication via USB-to-TTL converter (FT232RL)
* LCD 16x2 display via I2C (PCF8574T) to show RGB and HEX values
* Buzzer trigger on reset event
* Interrupt-based UART reception with circular (ring) buffer for high-frequency message handling

## Hardware Requirements

* STM32F407G-DISC1 Microcontroller
* USB-to-TTL serial adapter (FT232RL)
* RGB LED connected to PWM outputs
* 16x2 LCD with I2C module (PCF8574T)
* Buzzer module
* Breadboard and jumper wires
* Webcam

## Software Requirements

### Computer Vision (Python)

* Python 3.10
* pip 3.10

Install required Python libraries:

```bash
pip3.10 install opencv-python mediapipe numpy pyserial
```

### Embedded Development

* STM32CubeIDE
* STM32 HAL libraries

Peripheral Configuration:

* UART in interrupt mode (baudrate: 115200)
* TIM2 PWM for RGB output
* I2C for LCD
* GPIO for buzzer

## How It Works

1. **Computer Vision Module**:

   * Captures **frames** as **LIVE STREAM**
   * Detects hand **landmarks and draw skeleton**
   * Identifies **index finger** and checks its position over **RGB boxes**
   * Updates RGB values and sends them via UART in format: `S R G B\n`
   * Sends reset command as `R\n` when finger is on the reset button coordinates

2. **STM32 Module**:

   * Receives UART messages via interrupt
   * Buffers incoming messages using a ring buffer to prevent data collision
   * Parses and applies RGB values to LED
   * Updates the LCD with RGB and HEX
   * Activates buzzer on reset

## UART Communication Protocol

* **RGB Set Command**: `S R G B\n`

  * Example: `S 255 100 50\n`
* **Reset Command**: `R\n`

## How to Run

1. Create .venv and install all packages on `requirements.txt`

2. Run main file
```bash
python3.10 main.py
```

Ensure the correct serial port is configured in `config.py` if you test it with STM32 and all other components.

## Project Structure

```html
├── Computer-Vision/
│   ├── hand_tracking/
|   |   └── hand_tracker.py
│   ├── models/
│   │   └── hand_landmarker.task
│   ├── serial_com/
│   │   ├── __pycache__/
│   │   └── serial.py
│   ├── utils/
│   │   ├── __pycache__/
│   │   ├── coordinates.py
│   │   └── frame_util.py
│   ├── config.py
│   ├── main.py
│   └── requirements.txt
│
├── STM32/
│   ├── .settings/
│   ├── Core/
│   ├── Debug/
│   ├── Drivers/
│   ├── Middleware/
│   ├── USB_HOST/
│   ├── .cproject
│   ├── .mxproject
│   ├── .project
│   ├── STM32-RGB Debug.launch
│   ├── STM32-RGB.ioc
│   ├── STM32F407VGTX_FLASH._
```

## Notes

* Python 3.10 is recommended due to MediaPipe compatibility issues on other versions
* Ring buffer usage on STM32 ensures stability under high-frequency UART messages
* Ensure proper grounding between STM32 board and USB-TTL adapter

