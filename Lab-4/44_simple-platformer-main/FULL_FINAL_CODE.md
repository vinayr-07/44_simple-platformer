# Full Final Source Code

## `{rel}`

```python
import pygame
from game.game_engine import GameEngine

# Initialize pygame/Start application
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 500
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simple Platformer - Pygame Version")

# Colors
SKY = (100, 160, 220)

# Clock
clock = pygame.time.Clock()
FPS = 60

# Game loop
engine = GameEngine(WIDTH, HEIGHT)

def main():
    running = True
    while running:
        SCREEN.fill(engine.background_color)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if engine.handle_event(event):
                running = False

        engine.handle_input()
        engine.update()
        engine.render(SCREEN)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
```

## `{rel}`

```python
def swept_vertical_landing_y(
    previous_y: float,
    next_y: float,
    player_height: int,
    player_x: float,
    player_width: int,
    platform_x: int,
    platform_y: int,
    platform_width: int,
) -> float | None:
    """Return the platform top if the player's downward path crosses it."""
    if next_y < previous_y:
        return None

    horizontal_overlap = (
        player_x + player_width > platform_x
        and player_x < platform_x + platform_width
    )
    if not horizontal_overlap:
        return None

    previous_bottom = previous_y + player_height
    next_bottom = next_y + player_height
    if previous_bottom <= platform_y <= next_bottom:
        return float(platform_y)
    return None
```

## `{rel}`

```python
import pygame

from .collision import swept_vertical_landing_y
from .hazard import Hazard
from .level_data import DIFFICULTIES
from .player import Player
from .platform import Platform
from .sound_manager import SoundManager

WHITE = (255, 255, 255)
BROWN = (150, 100, 60)
RED = (220, 60, 60)
GREEN = (0, 200, 0)
GRAY = (185, 185, 195)
GOLD = (245, 205, 70)


class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.start_x, self.start_y = 40, height - 120
        self.player = Player(self.start_x, self.start_y)

        self.score = 0
        self.font = pygame.font.SysFont("Arial", 30)
        self.title_font = pygame.font.SysFont("Arial", 52, bold=True)
        self.small_font = pygame.font.SysFont("Arial", 20)
        self.game_over = False
        self.game_over_reason = ""
        self.selected_difficulty = 1
        self.sound = SoundManager()

        self.gravity = 0.6
        self.goal_x = 0
        self.level_name = ""
        self.background_color = (100, 160, 220)
        self.platforms = []
        self.hazards = []

        self._apply_difficulty()
        self._build_level()

    @property
    def difficulty_name(self):
        return DIFFICULTIES[self.selected_difficulty]["name"]

    @property
    def scenario_name(self):
        return self.level_name

    def _apply_difficulty(self):
        config = DIFFICULTIES[self.selected_difficulty]
        self.gravity = config["gravity"]
        self.player.jump_strength = config["jump_strength"]
        self.player.speed = config["speed"]
        self.player.max_fall_speed = config["max_fall_speed"]
        self.goal_x = config["goal_x"]
        self.level_name = config["scenario"]
        self.background_color = config["background"]

    def _build_level(self):
        """Build the selected difficulty's platforms and hazards."""
        config = DIFFICULTIES[self.selected_difficulty]
        ground_y = self.height - 40

        self.platforms = [
            Platform(x, ground_y + y_offset, width, height)
            for x, y_offset, width, height in config["platforms"]
        ]
        self.hazards = [
            Hazard(x, ground_y + y_offset - height, width, height)
            for x, y_offset, width, height in config["hazards"]
        ]

    def _select_difficulty(self, index):
        self.selected_difficulty = index % len(DIFFICULTIES)
        self._apply_difficulty()
        # Rebuild immediately so the selected level/scenario is also visible
        # behind the Game Over overlay before the user presses Enter.
        self._build_level()

    def reset_game(self):
        self._apply_difficulty()
        self._build_level()
        self.player.reset(self.start_x, self.start_y)
        self.score = 0
        self.game_over = False
        self.game_over_reason = ""

    def handle_event(self, event):
        if not self.game_over and event.type == pygame.KEYDOWN and event.key in (
            pygame.K_SPACE, pygame.K_UP, pygame.K_w
        ):
            if self.player.jump():
                self.sound.play_jump()
            return False

        if self.game_over and event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_LEFT, pygame.K_a):
                self._select_difficulty(self.selected_difficulty - 1)
            elif event.key in (pygame.K_RIGHT, pygame.K_d):
                self._select_difficulty(self.selected_difficulty + 1)
            elif event.key == pygame.K_1:
                self._select_difficulty(0)
            elif event.key == pygame.K_2:
                self._select_difficulty(1)
            elif event.key == pygame.K_3:
                self._select_difficulty(2)
            elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_r, pygame.K_SPACE):
                self.reset_game()
            elif event.key in (pygame.K_ESCAPE, pygame.K_q):
                return True
        return False

    def handle_input(self):
        if self.game_over:
            self.player.vx = 0
            return

        keys = pygame.key.get_pressed()
        self.player.vx = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.player.vx = -self.player.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.player.vx = self.player.speed

    def update(self):
        if self.game_over:
            return

        self.player.vy = min(self.player.vy + self.gravity, self.player.max_fall_speed)
        self.player.x = max(0, self.player.x + self.player.vx)

        previous_y = self.player.y
        next_y = self.player.y + self.player.vy
        self.player.on_ground = False

        if self.player.vy >= 0:
            landing_y = None
            for platform in self.platforms:
                candidate = swept_vertical_landing_y(
                    previous_y,
                    next_y,
                    self.player.height,
                    self.player.x,
                    self.player.width,
                    platform.x,
                    platform.y,
                    platform.width,
                )
                if candidate is not None and (landing_y is None or candidate < landing_y):
                    landing_y = candidate

            if landing_y is not None:
                self.player.y = landing_y - self.player.height
                self.player.vy = 0
                self.player.on_ground = True
            else:
                self.player.y = next_y
        else:
            self.player.y = next_y

        for hazard in self.hazards:
            if self.player.rect().colliderect(hazard.rect()):
                self.game_over = True
                self.game_over_reason = "You hit the hazard."
                self.sound.play_death()
                return

        if self.player.y > self.height:
            self.game_over = True
            self.game_over_reason = "You fell off the level."
            self.sound.play_death()
            return

        if self.player.x + self.player.width >= self.goal_x:
            self.score += 1
            self.sound.play_goal()
            self.player.reset(self.start_x, self.start_y)

    def render(self, screen):
        for platform in self.platforms:
            pygame.draw.rect(screen, BROWN, platform.rect())
        for hazard in self.hazards:
            pygame.draw.rect(screen, RED, hazard.rect())

        goal_rect = pygame.Rect(self.goal_x, 0, 6, self.height)
        pygame.draw.rect(screen, GREEN, goal_rect)
        pygame.draw.rect(screen, WHITE, self.player.rect())

        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        difficulty_text = self.small_font.render(
            f"{self.scenario_name} | Difficulty: {self.difficulty_name}",
            True,
            WHITE,
        )
        screen.blit(score_text, (10, 10))
        screen.blit(difficulty_text, (10, 45))

        if self.game_over:
            overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 175))
            screen.blit(overlay, (0, 0))

            title = self.title_font.render("GAME OVER", True, WHITE)
            final_score = self.font.render(f"Final score: {self.score}", True, WHITE)
            reason = self.small_font.render(self.game_over_reason, True, GRAY)
            prompt = self.font.render(
                f"Choose difficulty for replay: {self.scenario_name}",
                True,
                WHITE,
            )
            hint = self.small_font.render(
                "1/2/3 or Left/Right, then Enter. Q/Esc to quit.",
                True,
                GRAY,
            )

            screen.blit(title, ((self.width - title.get_width()) // 2, 70))
            screen.blit(final_score, ((self.width - final_score.get_width()) // 2, 140))
            screen.blit(reason, ((self.width - reason.get_width()) // 2, 185))
            screen.blit(prompt, ((self.width - prompt.get_width()) // 2, 230))

            option_y = 275
            option_gap = 135
            for index, difficulty in enumerate(DIFFICULTIES):
                option = self.font.render(
                    difficulty["name"],
                    True,
                    GOLD if index == self.selected_difficulty else WHITE,
                )
                x = (self.width // 2) - option_gap + index * option_gap
                screen.blit(option, (x - option.get_width() // 2, option_y))

            screen.blit(hint, ((self.width - hint.get_width()) // 2, 340))
```

## `{rel}`

```python
import pygame

class Hazard:
    def __init__(self, x, y, width, height=14):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
```

## `{rel}`

```python
"""Difficulty-specific level configurations for the platformer."""

DIFFICULTIES = (
    {
        "name": "Easy",
        "scenario": "Training Meadow",
        "gravity": 0.42,
        "jump_strength": -11.5,
        "speed": 4.5,
        "max_fall_speed": 13.0,
        "goal_x": 700,
        "background": (116, 178, 232),
        # (x, y offset from ground, width, height)
        "platforms": (
            (0, 0, 210, 14),
            (230, 0, 150, 14),
            (400, -50, 170, 14),
            (590, -20, 150, 14),
        ),
        # (x, platform y offset from ground, width, height)
        "hazards": (
            (300, 0, 36, 14),
        ),
    },
    {
        "name": "Medium",
        "scenario": "Bridge Run",
        "gravity": 0.60,
        "jump_strength": -12.0,
        "speed": 4.0,
        "max_fall_speed": 15.0,
        "goal_x": 740,
        "background": (100, 160, 220),
        "platforms": (
            (0, 0, 160, 14),
            (220, 0, 140, 14),
            (420, -60, 120, 14),
            (600, 0, 180, 14),
        ),
        "hazards": (
            (240, 0, 100, 14),
        ),
    },
    {
        "name": "Hard",
        "scenario": "Sky Gauntlet",
        "gravity": 0.80,
        "jump_strength": -13.5,
        "speed": 4.0,
        "max_fall_speed": 17.0,
        "goal_x": 775,
        "background": (68, 108, 168),
        "platforms": (
            (0, 0, 140, 14),
            (180, -40, 110, 14),
            (330, -90, 105, 14),
            (475, -30, 110, 14),
            (625, -80, 100, 14),
            (755, 0, 45, 14),
        ),
        "hazards": (
            (205, -40, 28, 14),
            (350, -90, 25, 14),
            (500, -30, 28, 14),
        ),
    },
)
```

## `{rel}`

```python
import pygame


class Player:
    def __init__(self, x, y, width=24, height=32):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vx = 0
        self.vy = 0
        self.speed = 4
        self.jump_strength = -12
        self.max_fall_speed = 15
        self.on_ground = False

    def rect(self):
        return pygame.Rect(int(self.x), int(self.y), self.width, self.height)

    def jump(self) -> bool:
        if not self.on_ground:
            return False
        self.vy = self.jump_strength
        self.on_ground = False
        return True

    def reset(self, x, y) -> None:
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.on_ground = False
```

## `{rel}`

```python
import pygame

class Platform:
    def __init__(self, x, y, width, height=14):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
```

## `{rel}`

```python
import io
import math
import struct
import wave

import pygame


class SoundManager:
    """Generate lightweight jump, goal, and death effects without asset files."""

    SAMPLE_RATE = 22050

    def __init__(self):
        self.enabled = False
        self.jump = None
        self.goal = None
        self.death = None

        try:
            if pygame.mixer.get_init() is None:
                pygame.mixer.init(frequency=self.SAMPLE_RATE, size=-16, channels=1, buffer=512)
            self.jump = self._make_tone(((660, 0.08), (880, 0.10)))
            self.goal = self._make_tone(((523, 0.10), (659, 0.10), (784, 0.16)))
            self.death = self._make_tone(((392, 0.12), (330, 0.12), (262, 0.22)))
            self.enabled = True
        except pygame.error:
            pass

    def _make_tone(self, notes):
        samples = []
        for frequency, duration in notes:
            count = int(self.SAMPLE_RATE * duration)
            attack = max(1, int(self.SAMPLE_RATE * 0.01))
            release = max(1, int(self.SAMPLE_RATE * 0.03))
            for index in range(count):
                t = index / self.SAMPLE_RATE
                envelope = min(1.0, index / attack)
                envelope *= min(1.0, (count - index) / release)
                value = int(12000 * envelope * math.sin(2 * math.pi * frequency * t))
                samples.append(struct.pack("<h", value))

        buffer = io.BytesIO()
        with wave.open(buffer, "wb") as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)
            wav_file.setframerate(self.SAMPLE_RATE)
            wav_file.writeframes(b"".join(samples))
        buffer.seek(0)
        return pygame.mixer.Sound(file=buffer)

    def _play(self, sound):
        if self.enabled and sound is not None:
            sound.play()

    def play_jump(self):
        self._play(self.jump)

    def play_goal(self):
        self._play(self.goal)

    def play_death(self):
        self._play(self.death)
```

## `{rel}`

```python
from game.collision import swept_vertical_landing_y
from game.level_data import DIFFICULTIES


def test_fast_fall_crossing_platform_lands():
    assert swept_vertical_landing_y(20, 90, 32, 50, 24, 0, 70, 200) == 70


def test_upward_motion_cannot_land():
    assert swept_vertical_landing_y(90, 20, 32, 50, 24, 0, 70, 200) is None


def test_no_land_without_horizontal_overlap():
    assert swept_vertical_landing_y(20, 90, 32, 220, 24, 0, 70, 200) is None


def test_each_difficulty_has_a_distinct_scenario():
    scenarios = [difficulty["scenario"] for difficulty in DIFFICULTIES]
    layouts = [difficulty["platforms"] for difficulty in DIFFICULTIES]

    assert len(set(scenarios)) == 3
    assert len(set(layouts)) == 3


def test_difficulty_layouts_have_valid_goals_and_platforms():
    for difficulty in DIFFICULTIES:
        assert 0 < difficulty["goal_x"] < 800
        assert difficulty["platforms"]
        assert difficulty["platforms"][0][0] == 0
        assert all(width > 0 and height > 0 for _, _, width, height in difficulty["platforms"])
```
