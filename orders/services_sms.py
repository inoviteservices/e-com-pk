import requests
from django.conf import settings


# ============================
# COMMON CONFIG
# ============================
BASE_URL = "https://control.msg91.com/api/v5/flow"

HEADERS = {
    "authkey": settings.MSG91_AUTH_KEY,
    "accept": "application/json",
    "content-type": "application/json"
}


# ============================
# ORDER CONFIRMATION SMS
# ============================
def send_order_confirmation_sms(order):

    # 🚫 BLOCK IN LOCAL / STAGING
    if settings.ENVIRONMENT != "PRODUCTION":
        print(f"📵 ORDER SMS BLOCKED ({settings.ENVIRONMENT}): {order.public_order_id}")
        return "BLOCKED"

    payload = {
        "template_id": "69d7790a2a459fa76a090263",  # ✅ ORDER TEMPLATE ID
        "short_url": "0",
        "recipients": [
            {
                "mobiles": "91" + str(order.phone)[-10:],
                "VAR1": order.first_name.strip(),
                "VAR2": order.public_order_id
            }
        ]
    }

    try:
        response = requests.post(BASE_URL, json=payload, headers=HEADERS, timeout=10)

        print("📦 ORDER SMS:", payload)
        print("✅ RESPONSE:", response.text)

        return response.text

    except Exception as e:
        print("❌ ORDER SMS ERROR:", str(e))
        return None


# ============================
# OTP SMS (COD VERIFICATION)
# ============================
def send_cod_otp_sms(phone, otp):

    # 🚫 BLOCK IN LOCAL / STAGING
    if settings.ENVIRONMENT != "PRODUCTION":
        print(f"📵 OTP BLOCKED ({settings.ENVIRONMENT}): {otp}")
        return "BLOCKED"

    payload = {
        "template_id": "69db8bfc88951461260dbbb2",  
        "recipients": [
            {
                "mobiles": "91" + str(phone)[-10:],
                "OTP": str(otp)
            }
        ]
    }

    try:
        response = requests.post(BASE_URL, json=payload, headers=HEADERS, timeout=10)

        print("📲 OTP SMS:", payload)
        print("✅ RESPONSE:", response.text)

        return response.text

    except Exception as e:
        print("❌ OTP SMS ERROR:", str(e))
        return None
    

def send_out_for_delivery_sms(order):

    payload = {
        "template_id": "YOUR_DLT_TEMPLATE_ID",
        "recipients": [
            {
                "mobiles": "91" + str(order.phone)[-10:],
                "NAME": order.first_name,
                "ORDER": order.public_order_id
            }
        ]
    }

    requests.post(BASE_URL, json=payload, headers=HEADERS)


def send_delivered_sms(order):
    # similar structure
    pass