# Snake Game

A terminal-based Snake game built with Python and curses.

## Features
- Classic Snake gameplay
- Score tracking with high score persistence
- Multiple snake shapes (single → quadruple)
- Difficulty levels
- Colorful terminal display

## Requirements
- Python 3.x
- `curses` library (included in Python standard library)

## Usage

### On Linux/Unix/macOS Terminal:
```bash
python3 snake.py
```

### Controls:
- Arrow keys: Move the snake
- Q: Quit the game

### Building APK for Android:
This project includes files for building an APK using [Buildozer](https://buildozer.readthedocs.io/):

```bash
# Install buildozer
pip install buildozer

# Initialize buildozer
buildozer init

# Build APK
buildozer -v android debug
```

## Project Structure
```
snake-game/
├── snake.py          # Main game file (terminal version)
├── main.py           # Android app entry point
├── AndroidManifest.xml
├── buildozer.spec
├── assets/
│   └── icon.png
└── README.md
```

## Android Build Instructions
1. Install Python 3 and buildozer on Linux
2. Run `pip install buildozer`
3. Run `buildozer init` to generate buildozer.spec
4. Update version, title, package name in buildozer.spec
5. Run `buildozer -v android debug` to build APK
6. APK will be in `bin/` directory

## License
MIT License - Feel free to use and modify