import requests
import hashlib
import time
from django.conf import settings


def send_meta_event(email, value=0, event_name="Purchase", event_id=None):

    # 🔒 safety checks
    if not settings.META_PIXEL_ID or not settings.META_ACCESS_TOKEN:
        print("❌ META CONFIG MISSING")
        return None

    if not email:
        print("❌ EMAIL MISSING")
        return None

    url = f"https://graph.facebook.com/v18.0/{settings.META_PIXEL_ID}/events"

    payload = {
        "data": [
            {
                "event_name": event_name,
                "event_time": int(time.time()),
                "event_id": event_id,
                "action_source": "website",

                "user_data": {
                    "em": hashlib.sha256(email.strip().lower().encode()).hexdigest()
                },

                "custom_data": {
                    "currency": "INR",
                    "value": float(value)
                }
            }
        ],
        "access_token": settings.META_ACCESS_TOKEN
    }

    try:
        res = requests.post(url, json=payload, timeout=10)
        data = res.json()

        # ✅ basic logging
        if data.get("events_received"):
            print("✅ META EVENT SENT")
        else:
            print("⚠️ META ISSUE:", data)

        return data

    except Exception as e:
        print("❌ META ERROR:", str(e))
        return None