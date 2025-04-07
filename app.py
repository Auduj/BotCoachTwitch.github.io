from twitchio.ext import commands
from flask import Flask, jsonify
import requests
import threading
import json
import time

# --- Flask Setup ---
app = Flask(__name__)
participants = {}

@app.route('/')
def home():
    return jsonify({"status": "BotCoachTwitch API is running"})

@app.route('/participants')
def get_participants():
    return jsonify(participants)

# --- Token Manager ---
CONFIG_FILE = "config.json"
TOKEN_URL = "https://id.twitch.tv/oauth2/token"
CLIENT_ID = "gp762nuuoqcoxypju8c569th9wz7q5"  # Public client_id utilisé par TwitchTokenGenerator

with open(CONFIG_FILE, "r") as f:
    config = json.load(f)

access_token = config["access_token"]
refresh_token = config["refresh_token"]
token_expiry = time.time() + 3600  # expiration approximative 1h

def refresh_access_token():
    global access_token, refresh_token, token_expiry
    print("🔁 Rafraîchissement du token...")

    params = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
        "client_id": CLIENT_ID
    }

    response = requests.post(TOKEN_URL, params=params)
    data = response.json()

    if "access_token" in data:
        access_token = f"oauth:{data['access_token']}"
        refresh_token = data["refresh_token"]
        token_expiry = time.time() + data["expires_in"]

        config["access_token"] = access_token
        config["refresh_token"] = refresh_token
        with open(CONFIG_FILE, "w") as f:
            json.dump(config, f, indent=4)

        print("✅ Nouveau token enregistré.")
    else:
        print("❌ Erreur lors du rafraîchissement :", data)

def get_valid_token():
    if time.time() >= token_expiry:
        refresh_access_token()
    return access_token

# --- Twitch Bot ---
class Bot(commands.Bot):
    def __init__(self):
        super().__init__(
            token=get_valid_token(),
            prefix='!',
            initial_channels=['Yendo_Jr']  # <-- remplace par ton nom de chaîne
        )

    async def event_ready(self):
        print(f"✅ Bot connecté en tant que {self.nick}")

    async def event_message(self, message):
        if message.echo:
            return
        await self.handle_commands(message)

    @commands.command(name='coachme')
    async def coachme(self, ctx):
        parts = ctx.message.content.strip().split()
        if len(parts) == 2:
            game_id = parts[1]
            user = ctx.author.name
            participants[user] = game_id
            await ctx.send(f"{user} a été ajouté avec l'ID de game : {game_id}")
        else:
            await ctx.send("❗ Utilisation correcte : !coachme ID_DE_GAME")

# --- Démarrage Flask + Bot ---
def start_flask():
    app.run(host='0.0.0.0', port=5000)

if __name__ == '__main__':
    threading.Thread(target=start_flask).start()
    bot = Bot()
    bot.run()
