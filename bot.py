from telegram.bot_telegram import main_run
from telegram.utils.config_types import readconfig

if __name__ == "__main__":
    main_run(readconfig())
