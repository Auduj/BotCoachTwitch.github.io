from twitchio.ext import commands
from flask import Flask, jsonify, render_template
from token_manager import get_valid_token
import threading

# Remplace ces valeurs par les tiennes
TOKEN = get_valid_token()
NICK = 'auduj08'
CHANNEL = 'Yendo_Jr'

# --- Flask ---
app = Flask(__name__)
participants = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/participants')
def get_participants():
    return jsonify(participants)

# --- Twitch Bot ---
class Bot(commands.Bot):
    def __init__(self):
        super().__init__(token=TOKEN, prefix='!', initial_channels=[CHANNEL])

    async def event_ready(self):
        print(f'✅ Bot connecté en tant que {self.nick}')

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
            await ctx.send(f"{user} a été ajouté à la liste avec l'ID de game {game_id} !")
        else:
            await ctx.send("Utilisation : !coachme ID_GAME")

# --- Thread Flask ---
def run_flask():
    app.run(host='0.0.0.0', port=5000)

# --- Lancer ---
if __name__ == '__main__':
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()

    bot = Bot()
    bot.run()