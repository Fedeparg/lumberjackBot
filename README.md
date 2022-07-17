# LumberJack Telegram Bot 🪓

Bot made for LumberJack telegram game. It recognises a couple of key pixels on your screen and makes lumberjack dodge tree's branches.

## How does it works? 🤷

The script searches for the play button anywhere on the screen. Once it is pressed, it tries to locate the most lower branch and take it into account to play the game.

After that, it uses PyAutoGUI to simulate user key inputs and play the game

## Usage example 👀

Just run the python script after the installation of the requirements through `pip install -r requirements.txt` and place the browser window with the game in focus. After that, just relax and enjoy beating your friends!
