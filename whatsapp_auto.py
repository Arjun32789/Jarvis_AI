import pywhatkit
import sys
import time

def send_message(phone, message):
    """Send WhatsApp message instantly"""
    try:
        # Phone number format: +919876543210 (country code ke saath)
        print(f"Sending to {phone}: {message}")
        pywhatkit.sendwhatmsg_instantly(
            phone_no=phone,
            message=message,
            wait_time=15,       # 15 sec wait karo WhatsApp Web load hone ka
            tab_close=True,     # Message bhejne ke baad tab band
            close_time=3
        )
        print("Message sent!")
    except Exception as e:
        print(f"Error: {e}")

def send_scheduled(phone, message, hour, minute):
    """Schedule message for later"""
    try:
        pywhatkit.sendwhatmsg(phone, message, hour, minute, wait_time=20, tab_close=True)
        print(f"Scheduled for {hour}:{minute}")
    except Exception as e:
        print(f"Error: {e}")

def play_on_youtube(song):
    """Play YouTube video"""
    pywhatkit.playonyt(song)

def search_google(query):
    """Google search"""
    pywhatkit.search(query)

if __name__ == "__main__":
    action = sys.argv[1] if len(sys.argv) > 1 else ""
    
    if action == "send":
        phone = sys.argv[2] if len(sys.argv) > 2 else ""
        message = sys.argv[3] if len(sys.argv) > 3 else ""
        if phone and message:
            send_message(phone, message)
    
    elif action == "schedule":
        phone = sys.argv[2]
        message = sys.argv[3]
        hour = int(sys.argv[4])
        minute = int(sys.argv[5])
        send_scheduled(phone, message, hour, minute)
    
    elif action == "youtube":
        song = sys.argv[2] if len(sys.argv) > 2 else ""
        play_on_youtube(song)
    
    elif action == "search":
        query = sys.argv[2] if len(sys.argv) > 2 else ""
        search_google(query)
    
    else:
        print("Usage:")
        print("  python whatsapp_auto.py send +919876543210 'Hello'")
        print("  python whatsapp_auto.py schedule +919876543210 'Hello' 14 30")
        print("  python whatsapp_auto.py youtube 'Shape of You'")
        print("  python whatsapp_auto.py search 'python tutorial'")