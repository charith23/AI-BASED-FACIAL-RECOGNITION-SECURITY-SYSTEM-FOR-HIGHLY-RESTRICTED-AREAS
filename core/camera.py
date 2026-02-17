import subprocess
import numpy as np
import cv2
import threading
import time

class Camera:
    def __init__(self):
        # MJPEG Stream is safer than Raw YUV for syncing
        # -t 0: No timeout
        # --width 640 --height 480: Standard Res
        # --framerate 15: Lower FPS helps CPU sync better
        # --codec mjpeg: Easier to find frame boundaries
        self.cmd = [
            "rpicam-vid",
            "-t", "0",
            "--inline", 
            "--width", "640",
            "--height", "480",
            "--framerate", "15", 
            "--codec", "mjpeg",
            "-o", "-"
        ]

        self.proc = subprocess.Popen(self.cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, bufsize=10**8)
        self.running = True
        self.latest_frame = None
        self.lock = threading.Lock()
        
        # Start reading thread
        self.thread = threading.Thread(target=self.update, daemon=True)
        self.thread.start()
        
        # Wait for camera to warm up
        time.sleep(1)

    def update(self):
        # Reads stream byte-by-byte looking for JPEG Start/End markers
        stream_bytes = b''
        while self.running:
            try:
                # Read small chunks
                chunk = self.proc.stdout.read(4096)
                if not chunk:
                    break
                stream_bytes += chunk
                
                # JPEG Start: 0xff 0xd8
                # JPEG End: 0xff 0xd9
                a = stream_bytes.find(b'\xff\xd8')
                b = stream_bytes.find(b'\xff\xd9')
                
                if a != -1 and b != -1:
                    # We found a complete frame!
                    jpg = stream_bytes[a:b+2]
                    stream_bytes = stream_bytes[b+2:] # Keep remaining bytes for next frame
                    
                    # Decode
                    frame = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
                    
                    if frame is not None:
                        with self.lock:
                            self.latest_frame = frame
            except Exception as e:
                pass

    def read(self):
        with self.lock:
            if self.latest_frame is not None:
                return True, self.latest_frame.copy()
            return False, None

    def release(self):
        self.running = False
        try:
            self.proc.terminate()
            self.proc.wait()
        except:
            pass