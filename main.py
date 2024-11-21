
from aiogram import Bot, Dispatcher
from aiogram.types import FSInputFile, Message
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
import asyncio
import os

from audio_worker import audio_to_text

# Вставьте ваш токен бота
BOT_TOKEN = os.environ['TOKEN']

# Создаем экземпляры бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# Команда /start
@dp.message(Command("start"))
async def start_command(message: Message):
    await message.answer("Привет! Я умею перводить голосовые сообщения в текст. \n \n Отправь мне голосовое сообщение, и я переведу его")


# Обработка аудиофайлов
@dp.message(lambda message: message.audio or message.voice)
async def handle_audio(message: Message):
    if message.audio:
        file_id = message.audio.file_id
        file_type = "аудиофайл"
    elif message.voice:
        file_id = message.voice.file_id
        file_type = "голосовое сообщение"
    await message.answer('Пару секунд, Обрабатываю сообщение...')
    
    # Скачиваем файл
    file = await bot.download(file_id)
    file_path = f"{file_id}.ogg"  # Сохраняем как временный файл
    with open(file_path, "wb") as f:
        f.write(file.read())
    
    result = ' '.join(audio_to_text(file_path))
    
    print(f"Файл скачан и сохранен как {file_path}")

    # Ответ пользователю
    await message.answer(f"Вот текст из сообщения: \n \n {result}")
    # Отправляем файл обратно (пример echo-ответа)
    #await bot.send_audio(chat_id=message.chat.id, audio=FSInputFile(file_path))

    # Удаляем временный файл после отправки
    os.remove(file_path)

# Обработка остальных типов сообщений
@dp.message()
async def handle_other_messages(message: Message):
    await message.answer("Я понимаю только аудиофайлы или голосовые сообщения. Попробуй отправить один из них!")

# Основная функция
async def main():
    print("Бот запускается...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
