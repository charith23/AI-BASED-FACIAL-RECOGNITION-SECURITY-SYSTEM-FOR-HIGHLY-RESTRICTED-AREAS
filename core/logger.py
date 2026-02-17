import csv
import os
from datetime import datetime

# --- CONFIGURATION ---
# Log file ekkada save avvalo path isthunnam
LOG_DIR = "data/logs"
LOG_FILE = os.path.join(LOG_DIR, "access_log.csv")

# Folder lekapothe create chestundi (safety kosam)
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# File lekapothe kothadi create chesi Headers rastundi
if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, mode="w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Date", "Time", "Name", "Confidence_Score", "Access_Status"])

def log_access(name, score, status):
    """
    Logs the entry into the CSV file.
    Args:
        name (str): Person's name (e.g., Charith_nrml)
        score (float): Confidence score (e.g., 45.0)
        status (str): "GRANTED" or "DENIED"
    """
    try:
        # Current Date & Time tiskuntundi
        now = datetime.now()
        date_str = now.strftime("%Y-%m-%d")
        time_str = now.strftime("%H:%M:%S")

        # Data ni list la prepare chestundi
        log_entry = [date_str, time_str, name, f"{score:.2f}", status]

        # CSV file lo append (add) chestundi
        with open(LOG_FILE, mode="a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(log_entry)
        
        # Terminal lo kuda chupistundi confirming ga
        print(f"[LOG] 📝 Entry Saved: {name} | {status} | {time_str}")

    except Exception as e:
        print(f"[ERROR] ❌ Logging Failed: {e}")