import requests
import logging
from django.conf import settings

logger = logging.getLogger(__name__)


def create_cashfree_order(order):

    url = f"{settings.CASHFREE_BASE_URL}/pg/orders"

    # Ensure valid amount
    try:
        amount = round(float(order.total_amount), 2)
    except Exception:
        amount = 1

    if amount <= 0:
        amount = 1

    payload = {
        "order_id": order.public_order_id,
        "order_amount": amount,
        "order_currency": "INR",

        "customer_details": {
            "customer_id": order.public_order_id,
            "customer_name": f"{order.first_name} {order.last_name}".strip(),
            "customer_email": order.email if order.email else "test@example.com",
            "customer_phone": str(order.phone)[-10:]
        },

        "order_meta": {
            "return_url": f"{settings.BASE_URL}/payment-result/?order_id={{order_id}}",
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
        response = requests.post(
            url,
            json=payload,
            headers=headers,
            timeout=10
        )

        response.raise_for_status()
        data = response.json()

        logger.info(f"✅ CASHFREE RESPONSE: {data}")

        return data

    except requests.exceptions.RequestException as e:
        logger.error(f"❌ CASHFREE API ERROR: {str(e)}")
        return None


def verify_cashfree_payment(order_id):

    url = f"{settings.CASHFREE_BASE_URL}/pg/orders/{order_id}/payments"

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

        return data

    except requests.exceptions.RequestException as e:
        logger.error(f"❌ VERIFY ERROR: {str(e)}")
        return None