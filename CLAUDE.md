# Snake — Retro Edition

Classic retro snake game built with Python and Pygame.

## Files

- `snake.py` — entire game (single file)

## Requirements

- Python 3.x
- pygame 2.x (`pip install pygame`)

## Running

```bash
python snake.py
```

## Controls

| Key               | Action               |
|-------------------|----------------------|
| Arrow keys / WASD | Move snake           |
| P                 | Pause / Resume       |
| R                 | Restart (game over)  |
| Q                 | Quit                 |
| Space             | Start (title screen) |

## Game Settings

| Setting     | Value              |
|-------------|--------------------|
| Speed (FPS) | 10 — moderate pace |
| Window      | 640 × 480 px       |
| Cell size   | 20 × 20 px         |
| Grid        | 32 × 24 cells      |
| Points/food | +10                |

## Architecture

- `Snake` — body list, direction handling, collision detection, drawing with eyes
- `Food` — random placement avoiding snake body, apple sprite
- `Game` — main loop, HUD (score + high score), start/pause/game-over overlays
