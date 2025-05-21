# Description
This program creates a Base16 theme for the Telegram Desktop using a template with parameters from my NIXOS repository and substituting colors from the Base16 palette you choose using https://github.com/tinted-theming/schemes/tree/spec-0.11/base16.

To use your local template, you should not use the -u option, it updates the template. To use a local palette, simply do not use the -b option or use it with the value 'local'.

# Install
Download: `git clone https://github.com/DaemonLife/telegram_base16_theme.git`\
Create virtual environment: `python -m venv venv`

Activate the virtual environment.\
For Windows: `venv\Scripts\activate.bat`\
For Linux and MacOS: `source venv/bin/activate`

Install requirements: `pip install -r requirements.txt`

# Run
Activate the virtual environment again if you have exited.\
And run: `python main.py -b [THEME_NAME]`\
If you don't know the names of the themes, look at Help or this: https://tinted-theming.github.io/tinted-gallery/

# Help
```
usage: main.py [-h] [-u] [-b BASE16_THEME]                                    

Telegram desktop base16 theme generator.
You can easily find all themes in gallery:
https://tinted-theming.github.io/tinted-gallery/
Or in repository directory:
https://github.com/tinted-theming/schemes/tree/spec-0.11/base16.

options:
  -h, --help            show this help message and exit
  -u, --update-theme-pattern
                        Rewrite and update theme template file. Default is 'False'.
  -b BASE16_THEME, --base16-theme BASE16_THEME
                        Base16 theme name to use. Default is 'local'.
```
