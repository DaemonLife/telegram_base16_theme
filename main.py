import requests
import re
import traceback
import zipfile
import os
from PIL import Image

# ---------
# CONSTANTS
# ---------

URL_RAW_THEME = "https://raw.githubusercontent.com/DaemonLife/nixos_hyprland/refs/heads/main/modules/telegram-theme.nix"
URL_BASE16_ALL_THEMES = "https://github.com/tinted-theming/schemes/tree/spec-0.11/base16"

# ---------
# FUNCTIONS
# ---------

def download_style(url, colors):

    # Функция для замены цветов
    def replace_colors(string, colors):
        for key, value in colors.items():
            string = string.replace(f"#${{{key}}}", value)
        return string

    # Получаем содержимое файла
    response = requests.get(url)
    file_content = response.text

    # Ищем текст между telegram_style = '' ''
    pattern = r'telegram_style\s*=\s*\'\'\s*(.*?)\s*\'\';'
    matches = re.findall(pattern, file_content, re.DOTALL)

    # Записываем найденные совпадения в файл
    with open('colors.tdesktop-theme', 'w', encoding='utf-8') as output_file:
        for match in matches:
            match = replace_colors(match, colors)
            # Удаляем пробелы в начале строк и записываем в файл
            output_file.write(match.replace('  ', '') + '\n')

    print("Стиль записан в colors.tdesktop-theme")

def read_yaml(yaml_file_path):
    colors = {}

    # Читаем YAML-файл
    with open(yaml_file_path, 'r', encoding='utf-8') as file:
        content = file.read()  # Читаем весь файл

    # Используем регулярное выражение для поиска переменных
    pattern = r'(\s*base[0-9A-Fa-f]{2}:\s*"(.*?)")'
    matches = re.findall(pattern, content)

    # Заполняем словарь переменными
    for match in matches:
        key, value = match[0].split(':', 1)  # Разделяем по двоеточию
        key = key.strip()  # Убираем пробелы вокруг ключа
        value = value.strip().strip('"')  # Убираем пробелы и кавычки вокруг значения
        colors[key] = value  # Сохраняем ключ и значение в словаре

    # print("\nВсе переменные:\n")
    # for k, v in colors.items():
    #     print(f"{k}: {v}")
    # print()

    return colors

def create_theme_file(colors):

    # Удаляем временные файлы
    try:
        os.remove("background.jpg")
    except:
        pass
    try:
        os.remove("telegram-base16.tdesktop-theme")
    except:
        pass

    # Создаем изображение
    image_size = (2960, 2960)
    background_color = colors["base00"];
    image = Image.new("RGB", image_size, background_color)
    image.save("background.jpg")

    # Создаем zip-архив
    with zipfile.ZipFile("telegram-base16.tdesktop-theme", "w") as zipf:
        zipf.write("colors.tdesktop-theme")
        zipf.write("background.jpg")

    # Удаляем временные файлы
    os.remove("background.jpg")
    os.remove("colors.tdesktop-theme")

def find_themes(url):
    print("\nChoose your theme here: https://tinted-theming.github.io/tinted-gallery/")
    theme_name = input("Enter theme name: ")
    print()
    theme_url = f"https://raw.githubusercontent.com/tinted-theming/schemes/refs/heads/spec-0.11/base16/{theme_name}.yaml"

    # Получаем содержимое файла
    response = requests.get(theme_url)
    file_content = response.text

    # Записываем найденные совпадения в файл
    with open('base16.yaml', 'w', encoding='utf-8') as output_file:
        output_file.write(file_content)

def main():
    find_themes(URL_BASE16_ALL_THEMES)
    colors = read_yaml("base16.yaml")
    download_style(URL_RAW_THEME, colors)
    create_theme_file(colors)
    
# ---------
# RUN MAIN!
# ---------

if __name__ == "__main__":
    try:
        main()
    except:
        print(traceback.format_exc())
