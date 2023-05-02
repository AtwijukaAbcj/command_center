import africastalking
from config import sanitize_sms
africastalking.initialize(
    username='',
    api_key=''
)
sms = africastalking.SMS

def sms_send(message, phone):
    response = sms.send(message, [sanitize_sms(phone)])
    if response:
        return 'SMS sent'
    else:
        return 'SMS not sent'
