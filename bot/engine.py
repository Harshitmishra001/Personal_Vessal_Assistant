import time
import signal
from bot.state import BotState

class BotEngine:
    def __init__(self):
        self.state = BotState.STOPPED
        self._running = False

    def start(self):
        print("[PVA] Bot starting...")
        self.state = BotState.RUNNING
        self._running = True
        self._run_loop()

    def _run_loop(self):
        try:
            while self._running:
                time.sleep(2)
        except KeyboardInterrupt:
            self.stop()

    def stop(self):
        if self._running:
            print("[PVA] Bot stopping...")
            self._running = False
            self.state = BotState.STOPPED
            print("[PVA] Bot stopped cleanly.")
