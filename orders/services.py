import requests
import logging
from django.conf import settings

logger = logging.getLogger(__name__)


def create_cashfree_order(order):

    if not settings.CASHFREE_APP_ID or not settings.CASHFREE_SECRET_KEY:
        logger.error("❌ Cashfree credentials missing")
        return None

    url = f"{settings.CASHFREE_BASE_URL}/orders"

    try:
        amount = round(float(order.total_amount), 2)
        if amount <= 0:
            amount = 1
    except Exception:
        amount = 1

    payload = {
        "order_id": order.public_order_id,
        "order_amount": amount,
        "order_currency": "INR",
        "customer_details": {
            "customer_id": order.public_order_id,
            "customer_name": f"{order.first_name} {order.last_name}".strip(),
            "customer_email": order.email or "test@example.com",
            "customer_phone": str(order.phone)[-10:]
        },
        "order_meta": {
            "return_url": f"{settings.BASE_URL}/payment-result/?order_id={order.public_order_id}",
            "notify_url": f"{settings.BASE_URL}/cashfree/webhook/"
        }
    }

    headers = {
        "x-api-version": "2022-09-01",
        "x-client-id": settings.CASHFREE_APP_ID,
        "x-client-secret": settings.CASHFREE_SECRET_KEY,
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)

        # 🔥 CRITICAL: log response always
        logger.info(f"📡 Cashfree Status: {response.status_code}")
        logger.info(f"📡 Cashfree Response: {response.text}")

        if response.status_code not in [200, 201]:
            logger.error("❌ Cashfree returned non-success response")
            return None

        data = response.json()

        if "payment_session_id" not in data:
            logger.error("❌ payment_session_id missing in response")
            return None

        return data

    except requests.exceptions.Timeout:
        logger.error("❌ Cashfree timeout")
        return None

    except requests.exceptions.RequestException as e:
        logger.error(f"❌ Cashfree request failed: {str(e)}")
        return None

def verify_cashfree_payment(order_id):

    url = f"{settings.CASHFREE_BASE_URL}/orders/{order_id}/payments"

    headers = {
        "x-api-version": "2022-09-01",
        "x-client-id": settings.CASHFREE_APP_ID,
        "x-client-secret": settings.CASHFREE_SECRET_KEY,
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        data = response.json()

        if not data or "data" not in data:
            return None

        logger.info(f"🔍 VERIFY PAYMENT: {data}")
        logger.info(f"📡 VERIFY STATUS: {response.status_code}")
        logger.info(f"📡 VERIFY RESPONSE: {response.text}")

        return data

    except requests.exceptions.RequestException as e:
        logger.error(f"❌ VERIFY ERROR: {str(e)}")
        return None