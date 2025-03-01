import base64
import requests

# DO NOT DELETE WE NEED TO BOOTSTRAP THE SERVER TO RUN

# Replace with your actual values
CLIENT_ID = '23Q36Q'
CLIENT_SECRET = '9f204f546d248fb638926af97aaf0993'
REDIRECT_URI = 'https://427d-155-69-193-63.ngrok-free.app'
authorization_code = '3144e4fd06f2a9703787a9df6e5a8fd1283f873e'

token_url = 'https://api.fitbit.com/oauth2/token'

# Prepare the Basic Auth header (server-type application)
credentials = f"{CLIENT_ID}:{CLIENT_SECRET}"
encoded_credentials = base64.b64encode(credentials.encode()).decode()
headers = {
    "Authorization": f"Basic {encoded_credentials}",
    "Content-Type": "application/x-www-form-urlencoded"
}

# Request payload
data = {
    "client_id": CLIENT_ID,
    "grant_type": "authorization_code",
    "redirect_uri": REDIRECT_URI,
    "code": authorization_code,
}

response = requests.post(token_url, headers=headers, data=data)

if response.status_code == 200:
    tokens = response.json()
    access_token = tokens["access_token"]
    refresh_token = tokens["refresh_token"]
    print("Access Token:", access_token)
    print("Refresh Token:", refresh_token)
else:
    print("Failed to obtain tokens:", response.text)
