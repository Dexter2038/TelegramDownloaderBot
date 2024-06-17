from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, FSInputFile, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from asyncio import create_subprocess_exec
from asyncio.subprocess import PIPE
from hashlib import sha256
from yt_dlp import YoutubeDL

router = Router(name="youtube-handler")


@router.message()
async def youtube_search(message: Message):
    #if not message.text.startswith(
    #        "https://www.youtu") and not message.text.startswith(
    #            "https://youtu"):
    #    await message.answer("Введите ссылку на видео из YouTube!")
    #    return
    builder = InlineKeyboardBuilder()
    with YoutubeDL({"quiet": True}) as ydl:
        try:
            info_dict = ydl.extract_info(message.text, download=False)
        except:
            await message.answer(
                "Ссылка недоступна. Введите ссылку на видео из YouTube!")
            return
        answer = f"Видео найдено!\n{info_dict["title"]}\n\n"
        audio_weight = int(list(filter(lambda x: x.get("height", 0) == None, info_dict["formats"]))[-1]["filesize"])
        for idx in range(len(info_dict["formats"]) - 1):
            _cur = info_dict["formats"][idx].get("height", 0)
            _next = info_dict["formats"][idx + 1].get("height", 0)
            if _cur is None or _next is None:
                continue
            _cur = int(_cur)
            _next = int(_next)
            if _next > _cur and _cur > 239:
                builder.add(InlineKeyboardButton(text=f"{info_dict["formats"][idx]["format_note"]}", callback_data=f"Youtube${message.text}${_cur}"))
                video_weight = (int(info_dict["formats"][idx]["filesize_approx"])+audio_weight)//1048576
                if video_weight > 1000:
                    video_weight = f"{video_weight/1024:.1f}"
                    weight = "Gb"
                else:
                    weight = "Mb"
                answer += f"{info_dict["formats"][idx]["format_note"]} ≈ {video_weight}{weight}\n"
        minus = -1
        while True:
            if info_dict["formats"][minus].get("format_note", 0) in answer:
                break
            if info_dict["formats"][minus].get("filesize"):
                builder.add(InlineKeyboardButton(text=f"{info_dict["formats"][minus]["format_note"]}", callback_data=f"Youtube${message.text}${info_dict["formats"][minus]["height"]}"))
                video_weight = (int(info_dict["formats"][minus]["filesize"])+audio_weight)//1048576
                if video_weight > 1000:
                    video_weight = f"{video_weight/1024:.1f}"
                    weight = "Gb"
                else:
                    weight = "Mb"
                answer += f"{info_dict["formats"][minus]["format_note"]} ≈ {video_weight}{weight}"
                break
            else:
                minus -= 1
    await message.answer(answer, reply_markup=builder.as_markup())


@router.callback_query(F.data.startswith("Youtube$"))
async def youtube_download(callback: CallbackQuery):
    _, url, res = callback.data.split("$")
    idd = sha256(f"{url}{res}".encode('utf-8')).hexdigest()
    process = await create_subprocess_exec(
        "yt-dlp",
        "--merge-output-format",
        "mp4",
        f"-f bestvideo[height={res}][ext=mp4]+bestaudio",
        "--abort-on-error",
        "--no-simulate",
        f"-oyoutube/{idd}.%(ext)s",
        "-O '%(duration)s'",
        url,
        stdout=PIPE,
        stderr=PIPE)
    await process.wait()
    duration, err = await process.communicate()
    duration = int(duration.decode("utf-8")[2:-2])
    if err:
        print(err)
        await callback.message.answer(
            "Ссылка недоступна. Введите ссылку на видео из YouTube!")
        print(err)
        return
    print("Готово")
    await callback.message.answer_video(
        FSInputFile(f"youtube/{idd}.mp4"),
        duration,
        1920,
        1080,
        supports_streaming=True,
        protect_content=False,
        caption="Скачано с помощью @pribvet_bot!")
