# ---------
#  IMPORT
# ---------

import requests
import re
import traceback
import zipfile
import os
from PIL import Image
import argparse
import yaml

# ---------
# CONSTANTS
# ---------

URL_THEME_PATTERN = "https://raw.githubusercontent.com/DaemonLife/nixos_hyprland/refs/heads/main/modules/telegram-theme.nix"
URL_BASE16_ALL_THEMES = "https://github.com/tinted-theming/schemes/tree/spec-0.11/base16"
URL_BASE16_YAML_PATH = "base16.yaml"
PATH_THEME_TEMPLATE = "base16_theme_template.txt"
PATH_OUTPUT_DIRECTORY = "Out theme file"
LOCAL_THEME = "local"

# ---------
# FUNCTIONS
# ---------

def download_theme_pattern(url, colors):
    # Получаем содержимое файла
    response = requests.get(url)
    file_content = response.text

    # Ищем текст между telegram_style = '' ''
    pattern = r'telegram_style\s*=\s*\'\'\s*(.*?)\s*\'\';'
    matches = re.findall(pattern, file_content, re.DOTALL)

    # Записываем найденные совпадения в файл
    with open(PATH_THEME_TEMPLATE, 'w', encoding='utf-8') as output_file:
        for match in matches:
            output_file.write(match.replace('  ', '') + '\n')
    print("Downloaded theme template file.")

def download_base16_yaml(url):
    while True:
        if args.base16_theme == None or args.base16_theme == "local":
            theme_name = input("Enter theme name: ")
            print()
        else:
            theme_name = args.base16_theme
        
        # Получаем содержимое файла
        theme_url = f"https://raw.githubusercontent.com/tinted-theming/schemes/refs/heads/spec-0.11/base16/{theme_name}.yaml"
        response = requests.get(theme_url)

        if response.status_code == 200:
            break
        else:
            print(f"Error. Theme '{theme_name}' does not exist. Please repeat.")
            args.base16_theme = None

    # Записываем найденные совпадения в файл
    file_content = response.text
    with open(URL_BASE16_YAML_PATH, 'w', encoding='utf-8') as output_file:
        output_file.write(file_content)

def read_base16_yaml(filepath):
    try:
        with open(filepath, 'r') as file:
            data = yaml.safe_load(file)
        return data
    except FileNotFoundError:
        print(f"Ошибка: Файл '{filepath}' не найден.")
        return None
    except yaml.YAMLError as e:
        print(f"Ошибка при чтении YAML файла '{filepath}': {e}")
        return None

def add_colors_to_theme_template(theme_template, colors):
    def add_color_to_line(line, colors):
        for key, value in colors.items():
            line = line.replace(f"#${{{key}}}", value)
        return line

    try:
        with open(theme_template, 'r') as file:
            lines = file.readlines()
    except FileNotFoundError:
        print(f"Файл '{theme_template}' не найден.")
        return

    processed_lines = [add_color_to_line(line, colors) for line in lines]   

    try:
        with open(theme_template, 'w') as file:
            file.writelines(processed_lines)
        print(f"Файл '{theme_template}' успешно обработан и перезаписан.")
    except Exception as e:
        print(f"Произошла ошибка при записи в файл '{theme_template}': {e}")

def create_tdesktop_theme(colors):
    background_color = colors.get('base00') # chat bg img
    if not background_color:
        print("No base00 color.")
        return

    image_size = (2960, 2960)

    try: 
        image = Image.new("RGB", image_size, background_color)
        image.save("background.jpg")
        print("Created background.jpg.")

        # copy PATH_THEME_TEMPLATE to colors.tdesktop-theme
        with open(PATH_THEME_TEMPLATE, 'rb') as src, open("colors.tdesktop-theme", 'wb') as dst:
            for line in src:
                dst.write(line)
        print(f"File {PATH_THEME_TEMPLATE} copied to colors.tdesktop-theme.")

        # rewrite template copy with colors
        add_colors_to_theme_template("colors.tdesktop-theme", colors)

        try:
            os.mkdir(PATH_OUTPUT_DIRECTORY)
            print(f"Created '{PATH_OUTPUT_DIRECTORY}' directory.")
        except FileExistsError:
            pass
        except Exception as e:
            print(f"Error with create directory: {e}")

        path = os.path.join(PATH_OUTPUT_DIRECTORY, "telegram-base16.tdesktop-theme")

        # Create theme archive
        with zipfile.ZipFile(path, "w") as zipf:
            zipf.write("colors.tdesktop-theme")
            zipf.write("background.jpg")
        print(f"Theme archive 'telegram-base16.tdesktop-theme' created in {PATH_OUTPUT_DIRECTORY} directory.")
        
    except Exception as e:
        print(f"Archive creation error: {e}")
        return
    
    finally:
        # Remove temp files
        for temp_file in ["background.jpg", "colors.tdesktop-theme"]:
            try:
                os.remove(temp_file)
            except FileNotFoundError:
                pass
        print("Removed temp files.")

def main():
    # yaml check
    if not os.path.exists(URL_BASE16_YAML_PATH):
        print(f"File '{URL_BASE16_YAML_PATH}' not found.")
        print("Please choose your theme here: https://tinted-theming.github.io/tinted-gallery/")
        print("For example, nord.")
        download_base16_yaml(URL_BASE16_ALL_THEMES) # if not
    elif args.base16_theme == LOCAL_THEME: # if yes
        print("Use local theme file.")
    else:
        download_base16_yaml(URL_BASE16_ALL_THEMES)

    # create dict with color pallete from yaml
    colors = read_base16_yaml(URL_BASE16_YAML_PATH)
    colors = colors.get('palette', {})

    # download my pattern for theme
    if (not os.path.exists(PATH_THEME_TEMPLATE)) or (args.update_theme_pattern == True) :
        download_theme_pattern(URL_THEME_PATTERN, colors)

    # creating theme archive
    create_tdesktop_theme(colors)

    print("\nComplited.")
    
# ---------
# RUIN MAIN
# ---------

if __name__ == "__main__":
    # Program options
    parser = argparse.ArgumentParser(description=f"Telegram desktop base16 theme generator. You can find all themes in https://tinted-theming.github.io/tinted-gallery/.")
    parser.add_argument("-u", "--update-theme-pattern", action='store_true', help="Rewrite and update theme template file. Default is 'False'.")
    parser.add_argument("-b", "--base16-theme", type=str, default="local", help="Base16 theme name to use. Default is 'local'.")

    # Add options in args value
    args = parser.parse_args()

    try:
        main()
    except:
        print(traceback.format_exc())
