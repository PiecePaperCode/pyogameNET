from threading import Thread
from pyogame import settings as djangosettings


import datetime


def scheduler():
    while djangosettings.BOT:
        # DeprecationWarning("SCHEDULER CODE COMES IN HERE")
        pass


if __name__ == "pyogame.services.bot.scheduler":
    t = Thread(target=scheduler)
    t.daemon = True
    t.start()

