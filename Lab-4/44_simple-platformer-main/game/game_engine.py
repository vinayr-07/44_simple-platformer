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
