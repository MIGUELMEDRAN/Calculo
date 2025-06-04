import pygame
import math

SLING_X = 120
SLING_Y = 550
MAX_FORCE = 2500

class Slingshot:
    def __init__(self, bird):
        self.bird = bird
        self.dragging = False
        self.start_pos = (SLING_X, SLING_Y)
        self.current_pos = (SLING_X, SLING_Y)
        self.max_length = 100  # distancia máxima de estiramiento

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if not self.bird.launched:
                mouse_x, mouse_y = event.pos
                distance = math.hypot(mouse_x - self.bird.x, mouse_y - self.bird.y)
                if distance < self.bird.radius + 10:
                    self.dragging = True

        elif event.type == pygame.MOUSEBUTTONUP:
            if self.dragging and not self.bird.launched:
                dx = self.start_pos[0] - self.current_pos[0]
                dy = self.start_pos[1] - self.current_pos[1]
                distance = math.sqrt(dx**2 + dy**2)
                force_magnitude = min(distance * 10, MAX_FORCE)
                force_x = (dx / distance) * force_magnitude if distance > 0 else 0
                force_y = (dy / distance) * force_magnitude if distance > 0 else 0
                self.bird.launch(force_x, force_y)
                self.dragging = False
                self.current_pos = self.start_pos

        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                self.current_pos = event.pos

    def draw(self, screen):
        # Base de la resortera
        pygame.draw.line(screen, (100, 50, 20), (SLING_X - 15, SLING_Y), (SLING_X + 15, SLING_Y), 5)
        
        # Banda elástica
        if self.dragging:
            pygame.draw.line(screen, (150, 75, 0), (SLING_X - 10, SLING_Y), self.current_pos, 3)
            pygame.draw.line(screen, (150, 75, 0), (SLING_X + 10, SLING_Y), self.current_pos, 3)