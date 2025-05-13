from os import path, rename
from tempfile import TemporaryDirectory

from aiogram import Router
from aiogram.types import Message
from aiogram.types.input_file import FSInputFile
from yt_dlp import YoutubeDL

from config import Config
from filters import Is_YT_URL_Filter
from keyboards import audio_menu_keyboard
from utils import MESSAGES, get_ydl_opts, sanitize_filename
from tasks.tasks import split_file


router = Router(name="main_router")


@router.message(Is_YT_URL_Filter())
async def youtube_audio_handler(message: Message):
    """
    Главный обработчик. Принимает ссылку на ютуб.
    Если ссылка корректна - вычленяет аудио с помощью
    YoutubeDL и отправляет его целиком или по частям.
    """

    url = message.text.strip()
    with TemporaryDirectory(dir="/tmpdir") as tmpdir:
        try:
            await message.answer(MESSAGES["FIRST_MSG"])
            with YoutubeDL(get_ydl_opts(tmpdir)) as ydl:
                info = ydl.extract_info(url, download=False)
                if info.get("is_live"):
                    await message.answer(MESSAGES["STREAM_MSG"])
                    return
                info = ydl.extract_info(url, download=True)
                title = info.get("title", "audio")
                file_ext = info.get("ext", "webm")
                safe_title = sanitize_filename(title)

                full_title = f"{safe_title}.{file_ext}"
                filepath = path.join(tmpdir, full_title)
                rename(
                    ydl.prepare_filename(info),
                    filepath
                )
            if path.getsize(filepath) <= Config.MAX_SIZE:
                await message.answer_audio(
                    FSInputFile(filepath),
                    title=f"{title[:37]}...",
                    reply_markup=audio_menu_keyboard()
                )
            else:  # ТГ запрещает отправлять аудио больше 50МБ
                await message.answer(MESSAGES["SECOND_MSG"])

                task = split_file.delay(
                        filepath=filepath,
                        output_dir=tmpdir,
                        max_size=Config.MAX_SIZE,
                        title=full_title,
                    )
                parts = task.get(timeout=180)
                for i, part_path in enumerate(
                    parts, 1
                ):
                    await message.answer_audio(
                        FSInputFile(part_path),
                        title=f"{title[:32]}... (ч.{i})",
                        reply_markup=audio_menu_keyboard()
                    )
            await message.answer(MESSAGES["SUCCESS_MSG"])
        except Exception as e:
            await message.answer(f"Ошибка при скачивании: {str(e)}")


@router.message()
async def another_message_handler(message: Message):
    await message.answer("Я работаю только с ссылками на ютуб =(")
