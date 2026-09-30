# Lab 4 VibeCoding Phase Log

This is a concise implementation log. It is not a substitute for exporting the actual ChatGPT/LLM conversation required by the course.

## Phase 1 — Collision fix

Prompt:
> Fix the Pygame platformer's documented platform tunneling bug. Use swept vertical collision detection so a fast downward movement cannot pass through a platform. Keep existing controls and level layout.

Result: added `game/collision.py`, integrated swept landing checks, and bounded terminal fall speed.

## Phase 2 — Game Over

Prompt:
> Add a real in-game Game Over state for hazard contact and falling below the screen. Show the final score and failure reason, and stop normal updates while the Game Over screen is visible.

Result: graphical Game Over overlay with final score and reason.

## Phase 3 — Replay + difficulty

Prompt:
> Add replay after Game Over with Easy, Medium, and Hard gravity/jump settings. Let the user choose using number keys or Left/Right, then restart with Enter. Add Q/Esc to quit.

Result: three difficulty profiles, selection UI, restart logic, and quit handling. Each difficulty is backed by its own platform/hazard layout and scenario name.

## Phase 4 — Sound

Prompt:
> Add sound feedback for jump, reaching the goal, and death without requiring external binary assets. Make audio optional so the game still runs if a sound device is unavailable.

Result: procedural tones in `game/sound_manager.py`.

## Phase 5 — Verification + documentation

No additional feature prompt was needed. Local verification and documentation were added after the four implementation prompts so the feature work remains within the requested three-to-four-attempt workflow.

Result: `test_game_logic.py`, README updates, submission checklist, and this phase log.

## Verification correction — Difficulty scenario rebuild

Observed issue during local testing: changing the replay difficulty altered gravity/jump settings but reused the same platform and hazard layout.

Correction prompt:
> Fix the difficulty selection bug so Easy, Medium, and Hard rebuild different playable platformer scenarios. Keep the movement settings, make Easy materially more forgiving, make Hard use a tighter route with more hazards, and update the selected scenario immediately when the user changes difficulty on the Game Over screen.

Result: added `game/level_data.py`, rebuilt platforms/hazards from the selected configuration, and added tests proving all three layouts are distinct.
