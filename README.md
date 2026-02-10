# Telegram Base16 theme generator 🎨
## Description
This program creates a Base16 theme for the Telegram Desktop using a template with [parameters](https://github.com/DaemonLife/nixos/blob/main/modules/telegram/telegram_base16_theme.nix) from my NixOS repository and substituting colors from the [Base16 palette](https://github.com/tinted-theming/schemes/tree/spec-0.11/base16) you choose.

## Install
1. Download zip and unzip it or use command:\
`git clone https://github.com/DaemonLife/telegram_base16_theme.git`
2. Open directory telegram_base16_theme-main.
3. If you are using NixOS run `nix-shell` for acivating virtual environment and skip the other steps.
4. Create virtual environment: `python -m venv venv`

5. Activate the virtual environment.\
For Windows: `venv\Scripts\activate.bat`\
For Linux and MacOS: `source venv/bin/activate`

6. Install requirements: `pip install -r requirements.txt`

## Run
1. Activate the virtual environment again if you have exited.
2. And run: `python main.py -b [BASE16_THEME]`

If you don't know the names of the themes, look at Help or this: https://tinted-theming.github.io/tinted-gallery/

To use your local template, you should not use the -u option, it updates the template. To use a local palette, simply do not use the -b option or use it with the value 'local'.

## Help
```
usage: main.py [-h] [-u] [-b BASE16_THEME]                                    

Telegram desktop base16 theme generator.

You can easily find all themes in gallery:
  https://tinted-theming.github.io/tinted-gallery/
The current link to the gallery is always stored in this repository:
  https://github.com/tinted-theming/schemes?tab=readme-ov-file
Or you can find themes in this directory:
  https://github.com/tinted-theming/schemes/tree/spec-0.11/base16.

options:
  -h, --help            show this help message and exit
  -u, --update-theme-pattern
                        Rewrite and update theme template file. Default is 'False'.
  -b BASE16_THEME, --base16-theme BASE16_THEME
                        Base16 theme name to use. Default is 'local'.
```
