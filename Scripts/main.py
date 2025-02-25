# def convert_milliseconds(milliseconds):
#     # Calculate total seconds
#     total_seconds = milliseconds // 1000
#
#     # Calculate hours, minutes, and seconds
#     hours = total_seconds // 3600
#     minutes = (total_seconds % 3600) // 60
#     seconds = total_seconds % 60
#
#     print( f"{hours} часов, {minutes} минут, {seconds} секунд")
# import requests
#
# import re
#
# def get_video_length_no_api(video_url):
#     response = requests.get(video_url)
#     html = response.text
#
#     # Ищем продолжительность видео в секундах (ключ "approxDurationMs" в HTML)
#     match = re.search(r'"approxDurationMs":"(\d+)"', html)
#     if match:
#         duration_ms = int(match.group(1))
#         convert_milliseconds(duration_ms)
#         return duration_ms / 1000  # Переводим из миллисекунд в секунды
#     else:
#         return None
# video_url = 'https://www.youtube.com/watch?v=k5z9p6ZEaus&ab_channel=%D0%B0%D0%BF%D0%B2%D0%BE%D1%83%D1%82'
#
# length = get_video_length_no_api(video_url)
#
#
# if length:
#     print(f'Длина видео: {length} секунд')
# else:
#     print('Не удалось получить длину видео')
#
#
# #
# # def get_playlist_video_ids(playlist_url):
# #     response = requests.get(playlist_url)
# #     html = response.text
# #
# #     # Ищем все videoId на странице
# #     video_ids = re.findall(r'"videoId":"([a-zA-Z0-9_-]+)"', html)
# #     return list(set(video_ids))  # Убираем дубликаты
# #
# # def get_playlist_length_no_api(playlist_url):
# #     video_ids = get_playlist_video_ids(playlist_url)
# #     total_seconds = 0
# #
# #     for video_id in video_ids:
# #         video_url = f'https://www.youtube.com/watch?v={video_id}'
# #         length = get_video_length_no_api(video_url)
# #         if length:
# #             total_seconds += length
# #
# #     return total_seconds
# #
# # playlist_url = 'https://www.youtube.com/watch?v=ziOQ8wkmnSE&list=PLAma_mKffTOSUkXp26rgdnC0PicnmnDak'
# # playlist_length = get_playlist_length_no_api(playlist_url)
# # print(f'Общая длина плейлиста: {playlist_length / 3600:.2f} часов')
# import aiohttp
# import asyncio
# import re
#
# async def get_playlist_video_ids(playlist_url):
#     async with aiohttp.ClientSession() as session:
#         async with session.get(playlist_url) as response:
#             html = await response.text()
#
#     # Ищем все videoId на странице
#     video_ids = re.findall(r'"videoId":"([a-zA-Z0-9_-]+)"', html)
#     return list(set(video_ids))  # Убираем дубликаты
#
# async def get_video_length_no_api(session, video_url):
#     async with session.get(video_url) as response:
#         html = await response.text()
#
#     # Ищем продолжительность видео в секундах
#     match = re.search(r'"approxDurationMs":"(\d+)"', html)
#     if match:
#         duration_ms = int(match.group(1))
#         return duration_ms / 1000  # Переводим из миллисекунд в секунды
#     else:
#         return 0
#
# async def get_playlist_length_no_api(playlist_url):
#     video_ids = await get_playlist_video_ids(playlist_url)
#     total_seconds = 0
#
#     async with aiohttp.ClientSession() as session:
#         tasks = [
#             get_video_length_no_api(session, f'https://www.youtube.com/watch?v={video_id}')
#             for video_id in video_ids
#         ]
#         durations = await asyncio.gather(*tasks)  # Одновременное выполнение всех запросов
#
#     total_seconds = sum(durations)
#     return total_seconds
#
# playlist_url = 'https://www.youtube.com/watch?v=ziOQ8wkmnSE&list=PLAma_mKffTOSUkXp26rgdnC0PicnmnDak'
#
# # Запускаем асинхронный код
# loop = asyncio.get_event_loop()
# playlist_length = loop.run_until_complete(get_playlist_length_no_api(playlist_url))
#
# print(f'Общая длина плейлиста: {playlist_length / 3600:.2f} часов')
import aiohttp
import asyncio
import re

# Функция для получения video_id из плейлиста
async def get_playlist_video_ids(playlist_url):
    async with aiohttp.ClientSession() as session:
        async with session.get(playlist_url) as response:
            html = await response.text()

    # Ищем все videoId на странице
    video_ids = re.findall(r'"videoId":"([a-zA-Z0-9_-]+)"', html)
    return list(set(video_ids))  # Убираем дубликаты

# Функция для получения длины видео
async def get_video_length_no_api(session, video_url):
    try:
        async with session.get(video_url) as response:
            html = await response.text()

        # Ищем продолжительность видео в секундах
        match = re.search(r'"approxDurationMs":"(\d+)"', html)
        if match:
            duration_ms = int(match.group(1))
            return duration_ms / 1000  # Переводим из миллисекунд в секунды
    except Exception as e:
        print(f"Ошибка при обработке {video_url}: {e}")
    return 0

# Функция для получения общей длины плейлиста
async def get_playlist_length_no_api(playlist_url):
    video_ids = await get_playlist_video_ids(playlist_url)
    total_seconds = 0

    async with aiohttp.ClientSession() as session:
        # Создаем список задач для асинхронного выполнения
        tasks = [
            get_video_length_no_api(session, f'https://www.youtube.com/watch?v={video_id}')
            for video_id in video_ids
        ]
        durations = await asyncio.gather(*tasks)  # Выполняем все задачи параллельно

    total_seconds = sum(durations)
    return total_seconds

# Основная часть
async def main():
    playlist_url = 'https://www.youtube.com/watch?v=XQehMASQ72k&list=PLpvrYdFr65lcQuMZUNe8A9zlYkyNF5nyy'
    playlist_length = await get_playlist_length_no_api(playlist_url)
    print(f'Общая длина плейлиста: {playlist_length / 3600:.2f} часов')

# Запускаем асинхронный код
if __name__ == "__main__":
    asyncio.run(main())
