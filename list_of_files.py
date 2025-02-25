import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By

# Список книг с заголовками и авторами
books = [
    "Программирование на Java - Автор А",
    "Эффективная Java - Джошуа Блох",
    "Чистый код - Роберт Мартин",
    "Алгоритмы: построение и анализ - Томас Кормен",
    "Совершенный код - Стив Макконнелл",
    "Грокаем алгоритмы - Адитья Бхаргава",
    "Искусство программирования - Дональд Кнут",
    "Паттерны проектирования - Эрих Гамма",
    "Java. Эффективное программирование - Джошуа Блох",
    "Spring в действии"
]

# Инициализация веб-драйвера (убедитесь, что ChromeDriver установлен)
driver = webdriver.Chrome()

# Переходим на страницу поиска картинок Google (на русском языке)
driver.get("https://www.google.com/imghp?hl=ru")
time.sleep(2)

for index, query in enumerate(books, start=1):
    # Находим строку поиска и вводим запрос
    search_box = driver.find_element(By.NAME, "q")
    search_box.clear()
    search_box.send_keys(query)
    search_box.submit()
    time.sleep(2)  # Ждем загрузки результатов

    # Получаем список миниатюр изображений
    thumbnails = driver.find_elements(By.CSS_SELECTOR, "img.Q4LuWd")
    if thumbnails:
        try:
            # Нажимаем на первую миниатюру
            thumbnails[0].click()
            time.sleep(2)  # Ждем появления панели с полноразмерным изображением

            # Находим все изображения в правой панели
            images = driver.find_elements(By.CSS_SELECTOR, "img.n3VNCb")
            image_url = None
            for image in images:
                src = image.get_attribute("src")
                # Ищем URL, который начинается с http (исключаем base64)
                if src and src.startswith("http"):
                    image_url = src
                    break

            if image_url:
                # Скачиваем изображение
                img_data = requests.get(image_url).content
                file_name = f"book{index}.jpg"
                with open(file_name, "wb") as f:
                    f.write(img_data)
                print(f"Сохранено: {file_name}")
            else:
                print("URL изображения не найден для запроса:", query)
        except Exception as e:
            print("Ошибка при обработке запроса:", query, "\n", e)
    else:
        print("Изображения не найдены для запроса:", query)

    # Возвращаемся на главную страницу Google Images для следующего запроса
    driver.get("https://www.google.com/imghp?hl=ru")
    time.sleep(2)

driver.quit()
