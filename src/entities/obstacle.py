import pygame
import math

class Obstacle:
    def __init__(self, x, y, w, h, mass=2.0):
        self.rect = pygame.Rect(x, y, w, h)
        self.mass = mass
        self.fallen = False

    def check_collision(self, bird):
        if self.fallen:
            return

        circle = pygame.Rect(
            bird.x - bird.radius, bird.y - bird.radius,
            bird.radius * 2, bird.radius * 2
        )

        if self.rect.colliderect(circle):
            m1 = bird.mass
            v1 = math.sqrt(bird.vx**2 + bird.vy**2)
            m2 = self.mass

            # Colisión perfectamente elástica
            v2_final = (2 * m1 * v1) / (m1 + m2)

            print("------ COLISIÓN ------")
            print(f"Masa pelota (m1): {m1} kg")
            print(f"Velocidad pelota: {v1:.2f} px/s")
            print(f"Masa obstáculo (m2): {m2} kg")
            print(f"Velocidad resultado obstáculo: {v2_final:.2f} px/s")
            print("-----------------------")

            # Efecto visual: se cae
            self.fallen = True

            # Disminuir velocidad del bird
            bird.vx *= 0.2
            bird.vy *= 0.2

    def draw(self, screen):
        color = (120, 120, 120) if self.fallen else (0, 150, 255)
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 2)