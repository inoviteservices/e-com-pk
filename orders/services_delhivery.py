import requests
import json
from django.conf import settings


def create_delhivery_shipment(order):

    url = "https://track.delhivery.com/api/cmu/create.json"
    # url = "https://staging-express.delhivery.com/api/cmu/create.json"

    # =========================
    # BUILD SHIPMENT
    # =========================
    shipment = {
        "name": f"{order.first_name} {order.last_name}",
        "add": order.address_line_1,
        "city": order.city,
        "state": order.state,
        "pin": order.pincode,
        "country": "India",
        "phone": str(order.phone)[-10:],
        "order": order.public_order_id,
        "total_amount": str(float(order.total_amount)),
        "quantity": "1"
    }

    # =========================
    # 🔥 FIXED PAYMENT LOGIC
    # =========================
    payment_type = str(order.payment_type).strip().upper()

    if payment_type == "COD":
        shipment["payment_mode"] = "COD"
        shipment["cod_amount"] = str(float(order.total_amount))
    else:
        shipment["payment_mode"] = "Prepaid"

    payload = {
        "shipments": [shipment],
        "pickup_location": {
            "name": "Primary"
        }
    }

    print("🚀 SENDING TO DELHIVERY:", payload)
    print("💰 PAYMENT TYPE:", payment_type)
    print("💰 TOTAL:", order.total_amount)

    try:
        response = requests.post(
            url,
            data={
                "format": "json",
                "data": json.dumps(payload)
            },
            headers={
                "Authorization": f"Token {settings.DELHIVERY_API_KEY}"
            },
            timeout=15
        )

        try:
            data = response.json()
        except Exception:
            print("❌ RAW RESPONSE:", response.text)
            return

        print("🚚 DELHIVERY:", data)

        # =========================
        # SUCCESS
        # =========================
        if data.get("success") and data.get("packages"):
            package = data["packages"][0]
            awb = package.get("waybill")

            if awb:
                order.tracking_id = awb
                order.courier_name = "Delhivery"
                order.shipping_status = "SHIPPED"
                order.status = "SHIPPED"
                order.save()
            else:
                print("⚠️ No AWB returned")
                order.shipping_status = "FAILED"
                order.save()

        # =========================
        # FAILURE
        # =========================
        else:
            print("❌ SHIPMENT FAILED:", data.get("rmk") or data)
            order.shipping_status = "FAILED"
            order.save()

    except Exception as e:
        print("❌ DELHIVERY ERROR:", str(e))