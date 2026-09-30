# Real-Time Simple Platformer Game

This Pygame platformer is the assigned `44_simple-platformer` Lab 4 project.

## Lab 4 tasks completed

### Task 1 — Refine Collision Detection

Platform landing now uses swept vertical collision detection. The engine checks whether the player's bottom crossed a platform top between the previous and next frame positions rather than checking only the final rectangle. A terminal fall speed also keeps motion bounded.

### Task 2 — Implement Game Over Condition

Touching the red hazard or falling below the screen produces an in-game Game Over screen with the final score and the reason for failure. The game no longer relies on a console-only message.

### Task 3 — Add Replay Option

After Game Over, select a difficulty. Each difficulty now rebuilds a genuinely different level scenario as well as changing movement physics:

- **Easy — Training Meadow:** wider platforms, a shorter route, one small hazard, lighter gravity, and faster horizontal movement.
- **Medium — Bridge Run:** the original four-platform route and central hazard.
- **Hard — Sky Gauntlet:** narrower elevated platforms, more jumps, three hazards, and a higher goal.

Use `1/2/3` or Left/Right to select. The selected scenario updates immediately on the Game Over screen, and Enter (or `R`) starts that exact scenario. `Q` or Esc quits.

### Task 4 — Add Sound Feedback

The game generates three small sound effects at runtime: jump, goal reached, and death. No external binary audio assets are required. If the machine has no usable audio device, gameplay still runs without sound.

## Run

Python 3.10+ is recommended.

```bash
python -m pip install -r requirements.txt
python main.py
```

## Controls

| Action | Keys |
|---|---|
| Move left | `Left` / `A` |
| Move right | `Right` / `D` |
| Jump | `Space` / `Up` / `W` |
| Select replay difficulty | `1` / `2` / `3` or Left/Right |
| Restart after Game Over | `Enter` / `R` / `Space` |
| Quit after Game Over | `Q` / `Esc` |

## Quick logic test

```bash
pytest -q test_game_logic.py
```

A syntax-only check that does not require Pygame to import:

```bash
python -m py_compile main.py game/*.py test_game_logic.py
```

## Lab submission evidence

The course handout requires a 10-second video before changes, a 10-second video after changes, updated code, and chat history. It also states that the assignment is individual, the assigned repo should be cloned/forked, changes should be pushed to the student's personal repo, and no PR should be raised against the `SETAPESU26` main repo.

Record the original code before replacing it, then record this final version showing reliable landing, Game Over, difficulty replay, and sound-triggering actions.
