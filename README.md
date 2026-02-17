# 🛡️ AI-Based Secure Facial Access System

![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python)
![Platform](https://img.shields.io/badge/Platform-Raspberry%20Pi-red?style=for-the-badge&logo=raspberrypi)
![Status](https://img.shields.io/badge/Status-Completed-success?style=for-the-badge)

## 📌 Project Overview
This project is a **robust facial recognition security system** designed for highly restricted areas. Unlike traditional CCTV or key-based systems, this solution proactively verifies identity in real-time.

It integrates **Anti-Spoofing (Liveness Detection)** to prevent unauthorized access via photos or videos and uses a **Telegram Bot** for remote monitoring and alerts.

## 🚀 Key Features
* **Real-Time Face Recognition:** Identifies authorized personnel instantly using LBPH and Computer Vision.
* **Anti-Spoofing (Liveness Check):** Distinguishes between a real 3D face and a 2D photo using Laplacian variance and eye-blink detection.
* **Smart Voting Logic:** Uses a 10-second temporal voting mechanism to ensure high accuracy (Threshold: 68).
* **Telegram Alerts:** Sends instant photo alerts to the admin's mobile for unauthorized attempts.
* **Remote Control:** Admin can unlock the door or train new users remotely via Telegram commands.
* **Automated Logging:** Maintains a secure CSV log of every entry and rejection.

## 🛠️ Hardware Requirements
* **Raspberry Pi 4 Model B** (8GB RAM) 
* **Pi Camera Module** (IMX-708) 
* **Servo Motor (MG996R)** (For door locking mechanism)
* **Output Modules:** Buzzer, LEDs (Green/Red/Yellow) 
* **Power Supply:** 5V 3A USB-C 

## 💻 Software Stack
* **OS:** Raspberry Pi OS (64-bit) 
* **Language:** Python 3 
* **Libraries:** OpenCV, RPi.GPIO, Telebot, NumPy, Matplotlib

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
