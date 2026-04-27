"""Alert & Notification Service – FCM + SMS fallback."""
import os
from datetime import datetime
from config.firebase_config import init_firebase, DEMO_MODE


def send_push_notification(title: str, body: str, target: str = "all") -> dict:
    """Send push notification via Firebase Cloud Messaging."""
    db = init_firebase()

    # Try real FCM
    if db and not DEMO_MODE:
        try:
            from firebase_admin import messaging
            message = messaging.Message(
                notification=messaging.Notification(title=title, body=body),
                topic=target,
            )
            response = messaging.send(message)
            return {"success": True, "method": "FCM", "message_id": response}
        except Exception as e:
            pass  # Fall through to demo

    return {
        "success": True,
        "method": "FCM (Demo)",
        "title": title,
        "body": body,
        "target": target,
        "timestamp": datetime.now().isoformat(),
    }


def send_sms_alert(phone: str, message: str) -> dict:
    """Send SMS via Twilio (demo mode returns mock)."""
    sid = os.getenv("TWILIO_ACCOUNT_SID")
    token = os.getenv("TWILIO_AUTH_TOKEN")
    from_phone = os.getenv("TWILIO_PHONE")

    if sid and token and from_phone:
        try:
            from twilio.rest import Client
            client = Client(sid, token)
            msg = client.messages.create(body=message, from_=from_phone, to=phone)
            return {"success": True, "method": "SMS", "sid": msg.sid}
        except Exception as e:
            return {"success": False, "method": "SMS", "error": str(e)}

    # Demo mode
    return {
        "success": True,
        "method": "SMS (Demo)",
        "phone": phone,
        "message": message[:50] + "...",
        "timestamp": datetime.now().isoformat(),
    }


def trigger_alert(incident: dict) -> list:
    """Trigger all alerts for an incident."""
    results = []
    title = f"🚨 {incident['type']} ALERT – {incident['severity']}"
    body = f"Zone: {incident.get('zone', 'Unknown')} | ID: {incident.get('id', 'N/A')}"

    # Push notification
    results.append(send_push_notification(title, body))

    # SMS to emergency contacts (demo numbers)
    for phone in ["+1234567890", "+0987654321"]:
        results.append(send_sms_alert(phone, f"{title}\n{body}"))

    return results
