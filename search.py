from youtube_search import YoutubeSearch as YS

from config import TOKEN
from aiogram import Bot,types,Dispatcher,utils
from aiogram.utils import executor
from aiogram.types import InputTextMessageContent,InlineQueryResultArticle, ReplyKeyboardMarkup,KeyboardButton
import hashlib

async def on_startup(_):
    print("Bot is online.")



def searcher(text):
    res = YS(text,max_results=20).to_dict()
    return res

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
@dp.message_handler(commands=["start"])
async def send_welcome(message: types.Message):
    username = message.from_user.username
    #b1 = KeyboardButton("@ytlook_bot ")
    #main = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(b1)
    await bot.send_message(message.from_user.id,f"Hi  {username}")#, reply_markup=main


@dp.inline_handler()
async def inline_handler(query: types.InlineQuery):
    text = query.query or "video"
    links = searcher(text)

    articles = [types.InlineQueryResultArticle(
        id = hashlib.md5(f'{link["id"]}'.encode()).hexdigest(),
        title = f'{link["title"]}',
        url = f'https://www.youtube.com/watch?v={link["id"]}',
        thumb_url = f'{link["thumbnails"][0]}',
        input_message_content=types.InputTextMessageContent(
            message_text=f'via @YTlook_BOT\nhttps://www.youtube.com/watch?v={link["id"]}')
    ) for link in links] 

    await query.answer(articles,cache_time=60,is_personal=True)


if __name__ == "__main__":
    executor.start_polling(dp,skip_updates=True,on_startup=on_startup)