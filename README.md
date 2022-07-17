# LumberJack Telegram Bot 🪵🪓

Bot made for LumberJack telegram game. It recognises a couple of key pixels on your screen and makes lumberjack dodge tree's branches.

*This is a mod to work exclusively on MacOS from the original code from [Enrique Moran](https://github.com/EnriqueMoran/lumberjackBot).*

## How does it works? 🤷

The script searches for the play button anywhere on the screen. Once it is pressed, it tries to locate the most lower branch and take it into account to play the game.

After that, it uses PyAutoGUI to simulate user inputs and play the game.

## Usage example 👀

Here you can check for a video showcase of the bot playing the game (image clickable):

[![Showcase video](https://img.youtube.com/vi/09UVK9AhwZQ/0.jpg)](https://www.youtube.com/watch?v=09UVK9AhwZQ )

First install the requierements through `pip install -r requirements.txt`.

**Optional:** I recommend creating a [virtual enviornment](https://docs.python.org/3/tutorial/venv.html) for testing and development.

After that, just run `python lumberjacBot.py` and place the browser window with the game in focus. Then relax and enjoy beating your friends! 😄
