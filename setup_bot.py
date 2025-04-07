import json
import os

CONFIG_FILE = "config.json"

def create_config():
    print("🛠️ Configuration de l'application Twitch (RoueCoach)")

    client_id = input("🔑 Entre ton Client ID Twitch : ").strip()
    client_secret = input("🔐 Entre ton Client Secret : ").strip()
    refresh_token = input("♻️  Entre ton Refresh Token : ").strip()

    config = {
        "client_id": client_id,
        "client_secret": client_secret,
        "refresh_token": refresh_token
    }

    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)

    print(f"\n✅ Fichier {CONFIG_FILE} créé avec succès !")

def main():
    if os.path.exists(CONFIG_FILE):
        print(f"⚠️  Un fichier {CONFIG_FILE} existe déjà.")
        choice = input("Voulez-vous le remplacer ? (o/N) : ").lower()
        if choice != 'o':
            print("❌ Annulé.")
            return

    create_config()

if __name__ == "__main__":
    main()
