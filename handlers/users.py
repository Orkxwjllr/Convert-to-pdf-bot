import logging
import os

from aiogram import Router, Bot
from aiogram.types import Message, FSInputFile
from aiogram.filters import CommandStart
from lexicon.lexicon import LEXICON
from service.pdfconvert import latex_to_pdf



logger = logging.getLogger(__name__)

user_router = Router()

@user_router.message(CommandStart())
async def start_message(message: Message):
    await message.answer(text=LEXICON["/start"])

@user_router.message(lambda message: len(message.text)>10)
async def message_to_pdf(message: Message, bot: Bot):
    latex_to_pdf(latex_str=message.text, output_filename=f"{message.text[:10]}.pdf")
    file_path = f"C:/Users/newf/python/VS_code_projects/Convert-to-pdf-bot/{message.text[:10]}.pdf"

    if os.path.exists(file_path):
        file = FSInputFile(file_path)
        await bot.send_document(chat_id=message.chat.id, document=file, caption=LEXICON["comment_pdf"])
        os.remove(file_path)
        await message.answer("Файл был удалён с сервера ✅")
    else:
        await message.answer("Файл не найден ❌")

@user_router.message()
async def start_message(message: Message):
    await message.answer(text=LEXICON["short_mess"])
