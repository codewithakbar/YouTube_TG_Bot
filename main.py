from email.mime import message
from youtube_search import YoutubeSearch

from config import TOKEN

from aiogram import Bot, types, utils
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import InputTextMessageContent, InlineQueryResultArticle

import hashlib
import csv


bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

MESSAGE = """
Bu bot sizga videolarni topish va ulashishda yordam beradi. U avtomatik ravishda ishlaydi, uni hech qanday joyga qo'shish shart emas. Shunchaki istalgan suhbatingizni oching va xabarlar maydoniga @yt_uzbot  biror narsa yozing. 

Masalan, bu yerda @yt_uzbot happy dog so‘zini yozib ko‘ring.
"""


def searcher(text):
    res = YoutubeSearch(text, max_results=50).to_dict()
    return res


@dp.inline_handler()
async def inline_handler(query: types.InlineQuery):
    text = query.query or "Java"
    links = searcher(text)

    articles = [types.InlineQueryResultArticle(
        id=hashlib.md5(f'{link["id"]}'.encode()).hexdigest(),
        title=f'{link["title"]}',
        url=f'https://www.youtube.com/watch?v={link["id"]}',
        thumb_url=f'{link["thumbnails"][0]}',
        input_message_content=types.InputTextMessageContent(
            message_text=f'https://www.youtube.com/watch?v={link["id"]}'
        )
    ) for link in links]

    await query.answer(articles, cache_time=60, is_personal=True)

@dp.message_handler(commands=['start'])
async def user_auth(message: types.Message):
    USER_DICT = {}
    if message.text == '/start':
        USER_DICT.update(
            {
                "ID": message.from_user.id,
                "Name": message.from_user.full_name,
                "Link_Bio": f"@{message.from_user.username}"

            }
        )
    
        # for x, y in USER_DICT.items():
        #     print(f"{x}: {y}")
    print(USER_DICT)
    

    field_names = ['ID','Name','Link_Bio']
    with open('output.csv', 'a', encoding='utf-8') as file:
        writer_object = csv.DictWriter(file, fieldnames=field_names)

        
        writer_object.writerow(USER_DICT)
        file.close()

executor.start_polling(dp, skip_updates=True)