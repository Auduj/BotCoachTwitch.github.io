import requests
import json
import os
import time

CONFIG_FILE = 'config.json'
TOKEN_FILE = 'token.json'

# Lecture des clés (client ID, secret, refresh token)
with open(CONFIG_FILE, 'r') as f:
    config = json.load(f)

CLIENT_ID = config['client_id']
CLIENT_SECRET = config['client_secret']
REFRESH_TOKEN = config['refresh_token']

# Chargement ou initialisation du token
if os.path.exists(TOKEN_FILE):
    with open(TOKEN_FILE, 'r') as f:
        token_data = json.load(f)
else:
    token_data = {
        "access_token": "",
        "expires_at": 0
    }

def refresh_token():
    print("🔁 Rafraîchissement du token Twitch...")
    url = "https://id.twitch.tv/oauth2/token"
    params = {
        "grant_type": "refresh_token",
        "refresh_token": REFRESH_TOKEN,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    }

    response = requests.post(url, params=params)
    data = response.json()

    if "access_token" in data:
        access_token = data["access_token"]
        expires_in = data["expires_in"]

        token_data["access_token"] = f"oauth:{access_token}"
        token_data["expires_at"] = time.time() + expires_in

        with open(TOKEN_FILE, "w") as f:
            json.dump(token_data, f)

        print("✅ Nouveau token enregistré.")
        return token_data["access_token"]
    else:
        print(f"❌ Erreur : {data}")
        raise Exception("Impossible de rafraîchir le token.")

def get_valid_token():
    if time.time() >= token_data["expires_at"]:
        return refresh_token()
    return token_data["access_token"]