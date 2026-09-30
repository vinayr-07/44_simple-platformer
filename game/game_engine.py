import pygame

from .collision import swept_vertical_landing_y
from .hazard import Hazard
from .player import Player
from .platform import Platform

WHITE = (255, 255, 255)
BROWN = (150, 100, 60)
RED = (220, 60, 60)
GREEN = (0, 200, 0)
GRAY = (185, 185, 195)


class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.gravity = 0.6

        self.start_x, self.start_y = 40, height - 120
        self.player = Player(self.start_x, self.start_y)

        ground_y = height - 40
        self.platforms = [
            Platform(0, ground_y, 160),
            Platform(220, ground_y, 140),
            Platform(420, ground_y - 60, 120),
            Platform(600, ground_y, 180),
        ]
        self.hazards = [Hazard(240, ground_y - 14, 100)]
        self.goal_x = 740

        self.score = 0
        self.font = pygame.font.SysFont("Arial", 30)
        self.title_font = pygame.font.SysFont("Arial", 52, bold=True)
        self.small_font = pygame.font.SysFont("Arial", 20)
        self.game_over = False
        self.game_over_reason = ""

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key in (
            pygame.K_SPACE,
            pygame.K_UP,
            pygame.K_w,
        ) and not self.game_over:
            self.player.jump()

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
                return

        if self.player.y > self.height:
            self.game_over = True
            self.game_over_reason = "You fell off the level."
            return

        if self.player.x + self.player.width >= self.goal_x:
            self.score += 1
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
        screen.blit(score_text, (10, 10))

        if self.game_over:
            overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 175))
            screen.blit(overlay, (0, 0))

            title = self.title_font.render("GAME OVER", True, WHITE)
            final_score = self.font.render(f"Final score: {self.score}", True, WHITE)
            reason = self.small_font.render(self.game_over_reason, True, GRAY)
            hint = self.small_font.render("Press R to restart or Q/Esc to quit.", True, WHITE)

            screen.blit(title, ((self.width - title.get_width()) // 2, 130))
            screen.blit(final_score, ((self.width - final_score.get_width()) // 2, 205))
            screen.blit(reason, ((self.width - reason.get_width()) // 2, 245))
            screen.blit(hint, ((self.width - hint.get_width()) // 2, 300))

