import logging
import os.path

from aiogram import Bot, Dispatcher, executor, types
from datetime import datetime

from google_class import GoogleSheet
# Токен от вашего бота
from ENV import API_TOKEN_BOT


logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN_BOT)
dp = Dispatcher(bot)

# id листа в google sheets
sheet_id = '1c5wIiqpQ8sHW6CppC5tVX9ks9gVAm1shqrfal0f58gg'

# путь до OAuth 2.0 Client IDs из https://console.cloud.google.com/apis/credentials
cred_path = 'creds_app.json'

# путь до файла, который создаётся при первом запуске
token_path = 'token.json'

sheet = GoogleSheet(sheet_id=sheet_id, cred_path=cred_path, token_path=token_path)

@dp.message_handler()
async def test(message: types.Message):
    sheet_line = ''
    try:
        if not os.path.exists('sheet_line.txt'):
            with open('sheet_line.txt', 'w') as line:
                line.write('2')
        with open('sheet_line.txt', 'r', encoding='utf-8') as lines:
            for l in lines:
                sheet_line = l
        sheet.add_value(range=f'test!A{sheet_line}:C',
                        value=[[message.from_user.username, message.text, str(message.date)]])
        with open('sheet_line.txt', 'w') as line:
            line.write(str(int(sheet_line) + 1))
    except Exception as err:
        sheet.add_value(range=f'test!A{sheet_line}:C',
                        value=[['error', str(err), str(datetime.now()).split('.')[0]]])
        with open('sheet_line.txt', 'w') as line:
            line.write(str(int(sheet_line) + 1))


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)