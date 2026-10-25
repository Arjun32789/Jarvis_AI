import cv2
import base64
import os
import time
import pyautogui
from datetime import datetime

def capture_camera():
    """Take a photo from webcam and return base64"""
    try:
        cap = cv2.VideoCapture(0)
        time.sleep(2)  # Warm up
        ret, frame = cap.read()
        cap.release()
        if ret:
            _, buffer = cv2.imencode('.jpg', frame)
            return base64.b64encode(buffer).decode('utf-8')
    except Exception as e:
        print(f"Camera error: {e}")
    return None

def capture_screen():
    """Take a screenshot and return base64"""
    try:
        screenshot = pyautogui.screenshot()
        # Save temp
        temp_path = os.path.join(os.path.expanduser('~'), 'Desktop', 'jarvis_screen_temp.png')
        screenshot.save(temp_path)
        with open(temp_path, 'rb') as f:
            data = base64.b64encode(f.read()).decode('utf-8')
        os.remove(temp_path)
        return data
    except Exception as e:
        print(f"Screen capture error: {e}")
    return None

def save_camera_photo():
    """Take photo and save to Desktop"""
    try:
        cap = cv2.VideoCapture(0)
        time.sleep(2)
        ret, frame = cap.read()
        cap.release()
        if ret:
            desktop = os.path.join(os.path.expanduser('~'), 'Desktop')
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filepath = os.path.join(desktop, f"jarvis_photo_{timestamp}.jpg")
            cv2.imwrite(filepath, frame)
            return filepath
    except Exception as e:
        print(f"Photo save error: {e}")
    return None

if __name__ == "__main__":
    import sys
    action = sys.argv[1] if len(sys.argv) > 1 else ""
    if action == "photo":
        path = save_camera_photo()
        print(f"Saved: {path}" if path else "Failed")