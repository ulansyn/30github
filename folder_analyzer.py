import os
import subprocess
import statistics


def get_video_duration(file_path):
    """Получает длительность видео через ffprobe из видео-потока."""
    try:
        result = subprocess.run(
            [
                'ffprobe',
                '-v', 'error',
                '-select_streams', 'v:0',
                '-show_entries', 'stream=duration',
                '-of', 'default=noprint_wrappers=1:nokey=1',
                file_path
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        duration_str = result.stdout.strip()
        # Если значение отсутствует или равно 'N/A', выводим предупреждение и возвращаем 0
        if not duration_str or duration_str.upper() == 'N/A':
            print(f"Предупреждение: Неверное значение длительности для {file_path}: '{duration_str}'")
            return 0
        return float(duration_str)
    except subprocess.CalledProcessError as e:
        print(f"Ошибка ffprobe для {file_path}:\n{e.stderr}")
    except Exception as e:
        print(f"Общая ошибка при обработке {file_path}: {str(e)}")
    return 0


def format_duration(seconds):
    """Форматирует длительность в ЧЧ:ММ:СС с округлением."""
    total_seconds = round(seconds)
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours:02}:{minutes:02}:{seconds:02}"


def check_ffprobe_available():
    """Проверяет доступность ffprobe в системе."""
    try:
        subprocess.run(
            ['ffprobe', '-version'],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True
        )
        return True
    except Exception:
        return False


def analyze_folder(folder_path):
    """
    Анализирует конкретную папку (только файлы в данной папке, без рекурсии)
    и возвращает статистику по видео в ней.
    """
    video_extensions = {'.mp4', '.avi', '.mkv', '.mov', '.flv', '.wmv', '.mpg', '.mpeg', '.m4v', '.webm'}
    videos = []

    # Анализируем только файлы непосредственно в этой папке
    try:
        for file in os.listdir(folder_path):
            full_path = os.path.join(folder_path, file)
            if os.path.isfile(full_path):
                ext = os.path.splitext(file)[1].lower()
                if ext in video_extensions:
                    duration = get_video_duration(full_path)
                    if duration > 0:
                        videos.append({
                            'name': file,
                            'duration': duration,
                            'path': full_path
                        })
    except Exception as e:
        print(f"Ошибка при анализе папки {folder_path}: {str(e)}")
        return None

    if not videos:
        return None

    durations = [v['duration'] for v in videos]
    longest_video = max(videos, key=lambda v: v['duration'])
    shortest_video = min(videos, key=lambda v: v['duration'])

    return {
        'folder_name': os.path.basename(folder_path),
        'folder_path': folder_path,
        'total_videos': len(videos),
        'total_duration': sum(durations),
        'average': statistics.mean(durations),
        'median': statistics.median(durations),
        'min_duration': min(durations),
        'max_duration': max(durations),
        'videos': videos,
        'longest_video': longest_video,
        'shortest_video': shortest_video
    }


def analyze_all_folders(main_folder):
    """
    Рекурсивно анализирует главную папку и все вложенные папки.
    Возвращает список статистик для каждой папки, в которой найдены видео.
    """
    folders_stats = []
    for root, _, _ in os.walk(main_folder):
        stats = analyze_folder(root)
        if stats:
            # Отображаемое имя – путь относительно главной папки
            rel_path = os.path.relpath(root, main_folder)
            stats['display_name'] = os.path.basename(main_folder) if rel_path == "." else rel_path
            folders_stats.append(stats)
    return folders_stats


def print_folder_report(folder_stats):
    """Выводит подробный отчёт по выбранной папке."""
    print("\n" + "=" * 60)
    print(f"Папка: {folder_stats.get('display_name', folder_stats['folder_name'])}")
    print("-" * 60)
    print(f"Видео найдено       : {folder_stats['total_videos']}")
    print(f"Общая длительность    : {format_duration(folder_stats['total_duration'])}")
    print("-" * 60)
    print("Список видео:")
    for i, video in enumerate(folder_stats['videos'], start=1):
        video_name = video['name'] if len(video['name']) <= 30 else video['name'][:27] + "..."
        print(f"{i:02d}. {video_name.ljust(30)} - {format_duration(video['duration'])}")
    print("-" * 60)
    print("Статистика:")
    print(f"  Среднее время       : {format_duration(folder_stats['average'])}")
    print(f"  Медианное время     : {format_duration(folder_stats['median'])}")
    print(f"  Минимальное время   : {format_duration(folder_stats['min_duration'])}")
    print(f"  Максимальное время  : {format_duration(folder_stats['max_duration'])}")
    print(
        f"  Самое короткое видео: {folder_stats['shortest_video']['name']} ({format_duration(folder_stats['shortest_video']['duration'])})")
    print(
        f"  Самое длинное видео : {folder_stats['longest_video']['name']} ({format_duration(folder_stats['longest_video']['duration'])})")
    print("=" * 60)


def print_all_videos(folders_stats):
    """Выводит список всех видео с указанием папки."""
    all_videos = []
    for stats in folders_stats:
        for video in stats['videos']:
            video_copy = video.copy()
            video_copy['folder'] = stats.get('display_name', stats['folder_name'])
            all_videos.append(video_copy)
    if not all_videos:
        print("Видео не найдены.")
        return

    print("\n" + "=" * 60)
    print("Список всех видео:")
    for i, video in enumerate(all_videos, start=1):
        print(
            f"{i:02d}. {video['name'][:30].ljust(30)} - {format_duration(video['duration'])} (Папка: {video['folder']})")
    print("=" * 60)


def print_all_folders_summary(folders_stats):
    """Выводит краткую сводку по каждой папке."""
    print("\n" + "=" * 60)
    print("Сводка по папкам:")
    for i, stats in enumerate(folders_stats, start=1):
        print(f"{i:02d}. {stats.get('display_name', stats['folder_name'])}")
        print(f"    Видео: {stats['total_videos']}, Длительность: {format_duration(stats['total_duration'])}")
    print("=" * 60)


def print_global_summary(folders_stats):
    """Выводит глобальную статистику по всем папкам."""
    if not folders_stats:
        print("Нет данных для глобальной статистики.")
        return

    total_duration = sum(s['total_duration'] for s in folders_stats)
    total_videos = sum(s['total_videos'] for s in folders_stats)
    folder_durations = [s['total_duration'] for s in folders_stats]
    longest_folder = max(folders_stats, key=lambda s: s['total_duration'])
    shortest_folder = min(folders_stats, key=lambda s: s['total_duration'])

    print("\n" + "=" * 60)
    print("Глобальная статистика:")
    print("-" * 60)
    print(f"Папок проанализировано : {len(folders_stats)}")
    print(f"Всего видео           : {total_videos}")
    print(f"Общее время           : {format_duration(total_duration)}")
    print(f"Среднее время на папку : {format_duration(statistics.mean(folder_durations))}")
    print(f"Медианное время папки  : {format_duration(statistics.median(folder_durations))}")
    print(
        f"Папка с минимальным временем: {shortest_folder.get('display_name', shortest_folder['folder_name'])} ({format_duration(shortest_folder['total_duration'])})")
    print(
        f"Папка с максимальным временем: {longest_folder.get('display_name', longest_folder['folder_name'])} ({format_duration(longest_folder['total_duration'])})")
    print("=" * 60)


def interactive_menu(folders_stats):
    """Интерактивное меню для просмотра отчётов."""
    while True:
        print("\nВыберите действие:")
        print("1. Показать список всех видео")
        print("2. Показать отчёт по одной папке")
        print("3. Показать сводку по всем папкам")
        print("4. Показать глобальную статистику")
        print("5. Выход")
        choice = input("Введите номер действия: ").strip()

        if choice == "1":
            print_all_videos(folders_stats)
        elif choice == "2":
            print_all_folders_summary(folders_stats)
            num = input("Введите номер папки для детального отчёта: ").strip()
            try:
                idx = int(num) - 1
                if 0 <= idx < len(folders_stats):
                    print_folder_report(folders_stats[idx])
                else:
                    print("Неверный номер папки.")
            except ValueError:
                print("Введите корректный номер.")
        elif choice == "3":
            print_all_folders_summary(folders_stats)
        elif choice == "4":
            print_global_summary(folders_stats)
        elif choice == "5":
            print("Выход из программы.")
            break
        else:
            print("Неверный выбор. Попробуйте ещё раз.")


def main():
    if not check_ffprobe_available():
        print("Ошибка: ffprobe не найден! Установите ffmpeg и добавьте его в PATH.")
        exit(1)

    path = input("Введите путь к главной папке: ").strip()
    if not os.path.exists(path):
        print("Указанная папка не существует!")
        exit(1)

    folders_stats = analyze_all_folders(path)
    if not folders_stats:
        print("Видео не найдены в указанной папке и её вложенных папках.")
        exit(0)

    interactive_menu(folders_stats)


if __name__ == "__main__":
    main()
