from telethon import TelegramClient, events, sync
from telethon.sessions import StringSession

print('Telegram BOT Authenticator, please, follow the instructions...')
api_id = int(input('API ID Number: '))
api_hash = str(input('API HASH: '))

with TelegramClient(StringSession(), api_id, api_hash) as client:
    auth_user = client.session.save()
    with open('auth_user.txt', 'w') as f:
        f.write(auth_user)

