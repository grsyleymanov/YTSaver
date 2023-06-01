from aiogram import Bot, types, executor, Dispatcher
import logging
import os
from pytube import YouTube

logging.basicConfig(level=logging.INFO)
bot = Bot(token="...")
dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.reply(
        "Привет! \n \n Я бот, который поможет тебе загрузить видео с хостинга YouTube. Для того, чтобы скачать видео, "
        "отправь мне ссылку на видео через пробел, после команды ""/download_video"". \n \n Пример: \n \n /download_video https://www.youtube.com/... \n "
        "\n Чтобы скачать аудиодорожку от"
        " ролика, необходимо ввести следующую команду: \n /download_audio https://www.youtube.com/...")

@dp.message_handler(commands=["download_video"])
async def video(message: types.Message):
    url = message.get_args()
    if len(url) == 0:
        await message.answer("Ссылка отсутствует. \n \n Пример: \n \n /download_video https://www.youtube.com/...")
    else:
        load = YouTube(url)
        await message.answer("Отправка видео на сервер. \n Пожалуйста, ожидайте...")
        video = load.streams.filter(progressive=True, file_extension="mp4")
        video.get_highest_resolution().download(filename="video.mp4")
        await message.reply(f"Отправка видео. \n Пожалуйста, ожидайте... \n '{load.title}'")
        await message.bot.send_video(chat_id=message.chat.id, video=open("video.mp4", "rb"), caption="Ваше видео:")
        os.remove("video.mp4")

@dp.message_handler(commands=["download_audio"])
async def audio(message: types.Message):
    url = message.get_args()
    if len(url) == 0:
        await message.answer("Ссылка отсутствует. \n \n Пример: \n \n /download_audio https://www.youtube.com/...")
    else:
        yt = YouTube(url)
        await message.answer("Отправка аудио на сервер. \n Пожалуйста, ожидайте...")
        audio = yt.streams.filter(only_audio=True).first()
        audio.download(filename="audio.mp3")
        await message.reply(f"Отправка аудио. \n Пожалуйста, ожидайте... \n '{yt.title}'")
        await message.bot.send_audio(chat_id=message.chat.id, audio=open("audio.mp3", "rb"), caption="Ваше аудио:")
        os.remove("audio.mp3")

if __name__ == "__main__":
    executor.start_polling(dp)
