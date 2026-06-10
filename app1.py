import pywhatkit as kit
import time

# ================= CONFIG =================
MESSAGE = "Hello {name}! This is a test message from me."
DELAY = 20   # seconds between messages

contacts = [
    {"phone": "+919876543210", "name": "Alice"},
    {"phone": "+918765432109", "name": "Bob"},
    # Add more here ↓
    # {"phone": "+91XXXXXXXXXX", "name": "Your Friend"},
]
# ========================================

print("🚀 Starting Bulk WhatsApp Sender...")

for contact in contacts:
    phone = contact["phone"]
    name = contact["name"]
    msg = MESSAGE.replace("{name}", name)
    
    print(f"Sending to {name} ({phone})...")
    try:
        kit.sendwhatmsg_instantly(phone, msg, wait_time=DELAY, tab_close=True)
        print("✅ Sent")
    except Exception as e:
        print(f"❌ Failed: {e}")
    
    time.sleep(DELAY)

print("🎉 Finished!")