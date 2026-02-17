# 🛡️ AI-Based Secure Facial Access System

![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python)
![Platform](https://img.shields.io/badge/Platform-Raspberry%20Pi-red?style=for-the-badge&logo=raspberrypi)
![Status](https://img.shields.io/badge/Status-Completed-success?style=for-the-badge)

## 📌 Project Overview
[cite_start]This project is a **robust facial recognition security system** designed for highly restricted areas[cite: 111]. Unlike traditional CCTV or key-based systems, this solution proactively verifies identity in real-time.

[cite_start]It integrates **Anti-Spoofing (Liveness Detection)** to prevent unauthorized access via photos or videos [cite: 270] [cite_start]and uses a **Telegram Bot** for remote monitoring and alerts[cite: 140].

## 🚀 Key Features
* [cite_start]**Real-Time Face Recognition:** Identifies authorized personnel instantly using LBPH and Computer Vision[cite: 27].
* [cite_start]**Anti-Spoofing (Liveness Check):** Distinguishes between a real 3D face and a 2D photo using Laplacian variance and eye-blink detection[cite: 28, 59].
* **Smart Voting Logic:** Uses a 10-second temporal voting mechanism to ensure high accuracy (Threshold: 68).
* [cite_start]**Telegram Alerts:** Sends instant photo alerts to the admin's mobile for unauthorized attempts[cite: 29].
* **Remote Control:** Admin can unlock the door or train new users remotely via Telegram commands.
* [cite_start]**Automated Logging:** Maintains a secure CSV log of every entry and rejection[cite: 30].

## 🛠️ Hardware Requirements
* [cite_start]**Raspberry Pi 4 Model B** (8GB RAM) [cite: 67]
* [cite_start]**Pi Camera Module** (IMX-708) [cite: 68]
* [cite_start]**Servo Motor (MG996R)** (For door locking mechanism) [cite: 312]
* [cite_start]**Output Modules:** Buzzer, LEDs (Green/Red/Yellow) [cite: 314]
* [cite_start]**Power Supply:** 5V 3A USB-C [cite: 69]

## 💻 Software Stack
* [cite_start]**OS:** Raspberry Pi OS (64-bit) [cite: 77]
* [cite_start]**Language:** Python 3 [cite: 78]
* [cite_start]**Libraries:** OpenCV, RPi.GPIO, Telebot, NumPy, Matplotlib [cite: 79, 320]

## 📂 Project Structure
```text
/SECURE_FACE_ACCESS
├── core/                  # Main logic (Camera, Detector, Servo, Bot)
├── config/                # Configuration files (Tokens, Thresholds)
├── data/                  # Trained models and encodings
├── reports/               # Auto-generated Access Logs & Graphs
├── surveillance_run.py    # MAIN SCRIPT to run the system
├── universal_train.py     # Script to train new faces
├── requirements.txt       # Python dependencies
└── README.md              # Project Documentation