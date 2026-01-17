import os

# ⚠️ Рекомендуется хранить токен в переменных окружения.
# Windows (PowerShell):
#   setx BOT_TOKEN "123:ABC"
# Linux/Mac:
#   export BOT_TOKEN="123:ABC"
BOT_TOKEN = os.getenv("BOT_TOKEN", "8599629156:AAHkWBgInDYLIoGGQzC3LfD9YLhjbqlDcDQ")

# (опционально) ID админов, если нужно расширять функционал
ADMIN_IDS = [123456789]

DEFAULT_LANGUAGE = "ru"
