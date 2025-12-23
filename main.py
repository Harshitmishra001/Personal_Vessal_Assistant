from storage.db import initialize_db
from storage.models import initialize_app_meta
from bot.engine import BotEngine

def main():
    print("[PVA] Initializing application...")
    initialize_db()
    initialize_app_meta()

    bot = BotEngine()
    bot.start()

if __name__ == "__main__":
    main()
