

import cv2
import time
import os
import numpy as np
import sys
import threading
import signal
import telebot
from telebot import types
import matplotlib.pyplot as plt
from datetime import datetime

# Import Core Modules
from core.camera import Camera
from core.detector import FaceDetector
from core.antispoof import AntiSpoof
from core.lbph_recognizer import LBPHRecognizer
from core.bot_handler import BotHandler
from core.liveness import LivenessDetector
from core.feedback import FeedbackSystem

# 🔥 CONFIGURATION
TELEGRAM_TOKEN = "8296389928:AAHX3dhadGpBpldT61CgDLdcIrmPam1OFn8"
CHAT_ID = "-5128242687"

# 🔥 THRESHOLD (Adjusted based on your logs)
CONFIDENCE_THRESHOLD = 68

# 📊 ANALYTICS DATA
stats_scores = []
stats_timestamps = []
stats_events = {"Authorized": 0, "Unknown": 0, "Spoof": 0}
session_start_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") # Safe for filenames

# --- 📁 CREATE REPORTS FOLDER ---
if not os.path.exists("reports"):
    os.makedirs("reports")

def get_time_string():
    return datetime.now().strftime("%H:%M:%S")

def get_date_string():
    return datetime.now().strftime("%Y-%m-%d")

# --- 📝 CSV LOGGING (Saves to reports/master_log.csv) ---
def log_to_csv(name, score, status):
    filename = "reports/master_log.csv"
    
    # Create file with headers if it doesn't exist
    if not os.path.exists(filename):
        with open(filename, "w") as f:
            f.write("Date,Time,Name,Score,Status\n")
            
    # Append the new log
    with open(filename, "a") as f:
        f.write(f"{get_date_string()},{get_time_string()},{name},{score},{status}\n")

def generate_analysis_graph():
    """Generates a graph with a UNIQUE timestamp filename"""
    print(f"\n[{get_time_string()}] 📊 Generating Graph...")
    
    if not stats_scores:
        print("⚠️ No data to plot.")
        return

    plt.figure(figsize=(10, 6))

    # 1. Score Trend
    plt.subplot(2, 1, 1)
    plt.plot(stats_timestamps, stats_scores, color='blue', marker='o', linestyle='-', markersize=2)
    plt.axhline(y=CONFIDENCE_THRESHOLD, color='r', linestyle='--', label=f'Limit ({CONFIDENCE_THRESHOLD})')
    plt.title(f"Score Trend (Session: {session_start_str})")
    plt.ylabel("Score")
    plt.xlabel("Time (Seconds)")
    plt.legend()
    plt.grid(True)

    # 2. Access Summary
    plt.subplot(2, 1, 2)
    plt.bar(list(stats_events.keys()), list(stats_events.values()), color=['green', 'red', 'orange'])
    plt.title("Access Summary")
    plt.ylabel("Count")

    plt.tight_layout()
    
    # 🔥 SAVE WITH TIMESTAMP 🔥
    # Example: reports/Graph_2026-02-10_21-30-00.png
    filename = f"reports/Graph_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.png"
    plt.savefig(filename)
    print(f"[{get_time_string()}] ✅ Graph Saved: {filename}")

def train_model():
    print(f"[{get_time_string()}] [SYSTEM] Re-training Model...")
    os.system("python3 universal_train.py")
    return True

def capture_hq_photos(name, count, feedback):
    save_path = f"data/known_faces/{name}" 
    os.makedirs(save_path, exist_ok=True)
    filename = f"{save_path}/{count}.jpg"
    cmd = f"rpicam-jpeg -o {filename} -t 2000 --width 640 --height 480 --nopreview > /dev/null 2>&1"
    os.system(cmd)
    return True

def main():
    print("------------------------------------------------")
    print("   🚀 SECURE FACE ACCESS: REPORT MODE           ")
    print(f"   📂 Saving to: /reports/ folder              ")
    print("------------------------------------------------")

    try:
        feedback = FeedbackSystem()
        cam = Camera()
        detector = FaceDetector()
        antispoof = AntiSpoof()
        liveness = LivenessDetector()
        bot = BotHandler(TELEGRAM_TOKEN, CHAT_ID)
        recognizer = LBPHRecognizer()
        
        if os.path.exists("data/lbph/lbph_model.yml"): 
            recognizer.load()
            print(f"[{get_time_string()}] ✅ Model Loaded.")
        else: 
            print(f"[{get_time_string()}] ⚠️ No Model Found.")
            
    except Exception as e:
        print(f"❌ CRASH: {e}"); return

    CURRENT_STATE = "SCANNING"
    unknown_start_time = None
    UNKNOWN_LIMIT = 10 
    
    blink_counter = 0
    eyes_open_frames = 0
    REQUIRED_BLINKS = 1
    
    unknown_frame_count = 0 
    REQUIRED_UNKNOWN_FRAMES = 5 
    
    alert_sent_time = None
    ADMIN_TIMEOUT = 60
    
    train_name = ""
    train_count = 0
    MAX_TRAIN_IMGS = 30

    start_timer = time.time()

    print(f"\n[{get_time_string()}] ✅ SYSTEM LIVE. Waiting for faces...\n")

    try:
        while True:
            cmd = bot.get_command()
            if cmd:
                action, data = cmd
                if action == "OPEN":
                    print(f"[{get_time_string()}] 🔓 REMOTE OPEN"); feedback.access_granted()
                    CURRENT_STATE = "SCANNING"; unknown_start_time = None
                elif action == "DENY":
                    print(f"[{get_time_string()}] 🔒 REMOTE DENY"); feedback.access_denied()
                    CURRENT_STATE = "SCANNING"; unknown_start_time = None
                elif action == "TRAIN":
                    print(f"[{get_time_string()}] 🆕 STARTING TRAINING: {data}")
                    CURRENT_STATE = "TRAINING"
                    train_name, train_count = data, 0
                    cam.release() 
                    feedback.processing()

            if CURRENT_STATE == "TRAINING":
                try:
                    capture_hq_photos(train_name, train_count, feedback)
                    train_count += 1
                    print(f"[{get_time_string()}] 📸 Captured: {train_count}/{MAX_TRAIN_IMGS}")
                    
                    if train_count >= MAX_TRAIN_IMGS:
                        bot.bot.send_message(CHAT_ID, "⏳ Processing...")
                        feedback.stop_processing()
                        if train_model():
                            recognizer.load()
                            bot.bot.send_message(CHAT_ID, f"✅ Added {train_name}!")
                        
                        cam = Camera()
                        CURRENT_STATE = "SCANNING"
                        unknown_start_time = None 
                        unknown_frame_count = 0
                except:
                    cam = Camera(); CURRENT_STATE = "SCANNING"
                continue 

            ret, frame = cam.read()
            if not ret: continue 
            
            if CURRENT_STATE == "WAITING":
                if time.time() - alert_sent_time > ADMIN_TIMEOUT:
                    print(f"[{get_time_string()}] ⌛ Timeout."); feedback.reset_leds()
                    CURRENT_STATE = "SCANNING"; unknown_start_time = None
                time.sleep(0.5); continue

            small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
            gray_small = cv2.cvtColor(small_frame, cv2.COLOR_BGR2GRAY)
            faces = detector.detect(gray_small)
            
            if len(faces) == 0:
                 blink_counter = 0 
                 feedback.stop_processing()
                 unknown_frame_count = 0 
            
            for (sx, sy, sw, sh) in faces:
                x, y, w, h = sx*2, sy*2, sw*2, sh*2
                
                # 🔥 STRICT ANTI-SPOOF
                if not antispoof.is_live(frame, (x, y, w, h)):
                    print(f"[{get_time_string()}] 🚫 [SPOOF]"); 
                    blink_counter = 0 
                    stats_events["Spoof"] += 1
                    continue 

                try: 
                    gray_full = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    face_roi = gray_full[y:y+h, x:x+w]
                    face_roi_resized = cv2.resize(face_roi, (200, 200))
                    name, conf = recognizer.predict(face_roi_resized)
                except: name, conf = "UNKNOWN", 100

                # 📊 Analytics Log
                elapsed_time = round(time.time() - start_timer, 2)
                stats_scores.append(int(conf))
                stats_timestamps.append(elapsed_time)

                if conf < CONFIDENCE_THRESHOLD and name != "UNKNOWN":
                    unknown_start_time = None; unknown_frame_count = 0
                    feedback.processing()

                    num_eyes = liveness.detect_blink(face_roi)
                    if num_eyes > 0: eyes_open_frames += 1
                    else:
                        if eyes_open_frames > 1: 
                            blink_counter += 1
                            eyes_open_frames = 0
                    
                    if blink_counter >= REQUIRED_BLINKS:
                        print(f"[{get_time_string()}] ✅ ACCESS: {name} ({int(conf)})")
                        feedback.access_granted() 
                        stats_events["Authorized"] += 1
                        
                        # 📝 SAVE TO CSV
                        log_to_csv(name, int(conf), "Authorized")
                        
                        blink_counter = 0 
                        time.sleep(2)
                    else:
                        print(f"[{get_time_string()}] 👀 Verifying {name}... ({int(conf)})")
                    
                else:
                    blink_counter = 0 
                    unknown_frame_count += 1
                    
                    if unknown_frame_count > REQUIRED_UNKNOWN_FRAMES:
                        if unknown_start_time is None:
                            unknown_start_time = time.time()
                            print(f"[{get_time_string()}] ⚠️ UNKNOWN (Score: {int(conf)})")
                            feedback.access_denied()
                            stats_events["Unknown"] += 1
                            
                            # 📝 SAVE TO CSV
                            log_to_csv("Unknown", int(conf), "Denied")
                            
                        else:
                            elapsed = time.time() - unknown_start_time
                            if elapsed >= UNKNOWN_LIMIT:
                                print(f"[{get_time_string()}] 🚨 ALERT SENT")
                                _, buf = cv2.imencode(".jpg", frame)
                                if bot.send_alert(buf.tobytes()):
                                    CURRENT_STATE = "WAITING"
                                    alert_sent_time = time.time()
                                unknown_start_time = None
                    else:
                        print(f"[{get_time_string()}] ❓ Analyzing... ({int(conf)})")

    except KeyboardInterrupt:
        print(f"\n[{get_time_string()}] 🛑 Stopping...")
        feedback.cleanup()
        cam.release()
        generate_analysis_graph()

if __name__ == "__main__":
    main()