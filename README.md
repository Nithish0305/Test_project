# Snake — Retro Edition

A classic retro Snake game built with Python and Pygame. Features smooth gameplay at a moderate speed, a retro dark-grid aesthetic, an animated snake with directional eyes, and a session high-score tracker.

## Features

- Retro dark-grid visual style
- Snake head with directional eyes and gradient tail shading
- Apple food sprite with shine highlight
- Live score + session high-score HUD
- Title screen, pause screen, and game-over overlay
- New High Score detection

## Requirements

- Python 3.x
- pygame 2.x

```bash
pip install pygame
```

## Running

```bash
python snake.py
```

## Controls

| Key               | Action               |
|-------------------|----------------------|
| Arrow keys / WASD | Move the snake       |
| Space             | Start (title screen) |
| P                 | Pause / Resume       |
| R                 | Restart after death  |
| Q                 | Quit                 |

## Game Settings

| Setting     | Value             |
|-------------|-------------------|
| Speed       | 10 FPS (moderate) |
| Window size | 640 × 480 px      |
| Cell size   | 20 × 20 px        |
| Grid        | 32 × 24 cells     |
| Points/food | +10               |

## Project Structure

```
snake.py     # Full game — single file
CLAUDE.md    # Dev notes for Claude Code
README.md    # This file
```

## License

MIT
