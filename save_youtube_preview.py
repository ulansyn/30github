import requests
import os
import re

def extract_video_id(url):
    patterns = [
        r'(?:v=|\/)([0-9A-Za-z_-]{11}).*',
        r'(?:be\/)([0-9A-Za-z_-]{11})',
        r'(?:embed\/)([0-9A-Za-z_-]{11})'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None

def get_thumbnail_url(video_id, quality='maxres'):
    """Генерация URL превью для разных качеств:
       maxres, hq, sd, mq, default"""
    qualities = {
        'maxres': 'maxresdefault.jpg',
        'hq': 'hqdefault.jpg',
        'sd': 'sddefault.jpg',
        'mq': 'mqdefault.jpg',
        'default': 'default.jpg'
    }
    return f'https://img.youtube.com/vi/{video_id}/{qualities[quality]}'

def download_youtube_thumbnail(video_url, save_path='thumbnails', quality='maxres'):
    os.makedirs(save_path, exist_ok=True)
    
    video_id = extract_video_id(video_url)
    if not video_id:
        raise ValueError("Invalid YouTube URL")
    
    thumbnail_url = get_thumbnail_url(video_id, quality)
    response = requests.get(thumbnail_url)
    
    if response.status_code != 200:
        for q in ['hq', 'sd', 'mq', 'default']:
            thumbnail_url = get_thumbnail_url(video_id, q)
            response = requests.get(thumbnail_url)
            if response.status_code == 200:
                break
    
    if response.status_code != 200:
        raise Exception("Failed to download thumbnail")
    
    filename = os.path.join(save_path, f"{video_id}.jpg")
    with open(filename, 'wb') as f:
        f.write(response.content)
    
    return filename

if __name__ == "__main__":
    video_url = input("Введите URL YouTube видео: ")
    try:
        saved_file = download_youtube_thumbnail(video_url)
        print(f"Превью сохранено в: {saved_file}")
    except Exception as e:
        print(f"Ошибка: {e}")
