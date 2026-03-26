import requests
import base64
from datetime import datetime
from decouple import config

CONSUMER_KEY = config("MPESA_CONSUMER_KEY")
CONSUMER_SECRET = config("MPESA_CONSUMER_SECRET")
SHORTCODE = config("MPESA_SHORTCODE")
PASSKEY = config("MPESA_PASSKEY")

def get_access_token():
    url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    response = requests.get(url, auth=(CONSUMER_KEY, CONSUMER_SECRET))
    return response.json().get("access_token")

def generate_password():
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    data = SHORTCODE + PASSKEY + timestamp
    password = base64.b64encode(data.encode()).decode("utf-8")
    return password, timestamp

def stk_push(phone, amount):
    access_token = get_access_token()
    password, timestamp = generate_password()

    url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    payload = {
        "BusinessShortCode": SHORTCODE,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": int(amount),
        "PartyA": phone,
        "PartyB": SHORTCODE,
        "PhoneNumber": phone,
        "CallBackURL": config("MPESA_CALLBACK_URL"),
        "AccountReference": "FoodieHub",
        "TransactionDesc": "Food Payment"
    }

    response = requests.post(url, json=payload, headers=headers)
    return response.json()