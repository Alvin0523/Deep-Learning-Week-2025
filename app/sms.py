from twilio.rest import Client

# Twilio credentials (replace with your actual credentials)
ACCOUNT_SID = "ACce77df918517a6175650111a989d81c2"
AUTH_TOKEN = "a463ba3cdca665fd488df4f2b5170f99"
TWILIO_PHONE_NUMBER = "+17177947365"  # Example: "+14155238886"
TO_PHONE_NUMBER = "+6588252349"  # Singapore number with +65 prefix

def emergency(message="🚨 Emergency Alert: Immediate assistance needed!"):
    """
    Sends an SMS alert via Twilio.
    
    :param message: The message to send.
    """
    try:
        client = Client(ACCOUNT_SID, AUTH_TOKEN)
        
        sms = client.messages.create(
            body=message,
            from_=TWILIO_PHONE_NUMBER,
            to=TO_PHONE_NUMBER
        )
        
        print(f"✅ Emergency SMS sent successfully! SID: {sms.sid}")
        return sms.sid

    except Exception as e:
        print(f"❌ Failed to send SMS: {e}")
        return None