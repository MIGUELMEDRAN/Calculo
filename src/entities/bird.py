import math
import numpy as np
from scipy.integrate import odeint

GROUND_Y = 700 - 50  # Ajuste fijo desde main.py

class Bird:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.radius = 15
        self.mass = 0.4
        self.launched = False
        self.trail = []
        self.bounce_count = 0
        self.total_distance = 0
        self.flight_time = 0

    def physics_system(self, state, t):
        x, y, vx, vy = state
        v_total = math.sqrt(vx**2 + vy**2)
        dxdt = vx
        dydt = vy
        dvxdt = -0.001 * vx * v_total / self.mass
        dvydt = 150 - 0.001 * vy * v_total / self.mass
        return [dxdt, dydt, dvxdt, dvydt]

    def launch(self, force_x, force_y):
        self.vx = force_x / self.mass
        self.vy = -force_y / self.mass
        self.launched = True
        self.trail = []
        self.total_distance = 0
        self.flight_time = 0

    def update(self, dt):
        if not self.launched:
            return

        state = [self.x, self.y, self.vx, self.vy]
        t = [0, dt]
        solution = odeint(self.physics_system, state, t)
        x1, y1, vx1, vy1 = solution[-1]

        dx = x1 - self.x
        dy = y1 - self.y
        self.total_distance += math.sqrt(dx**2 + dy**2)

        self.x, self.y, self.vx, self.vy = x1, y1, vx1, vy1
        self.flight_time += dt

        # Comportamiento cuando toca el suelo
        if self.approach_ground_limit():
            if abs(self.vy) < 1:
                self.vy = 0
                self.vx = 0
                self.y = GROUND_Y - self.radius
                self.launched = False
            else:
                self.y = GROUND_Y - self.radius
                self.vy = -self.vy * 0.6
                self.vx *= 0.85

    def approach_ground_limit(self):
        return self.y + self.radius >= GROUND_Y

    def draw(self, screen):
        import pygame
        velocity = math.sqrt(self.vx**2 + self.vy**2)
        for i, pos in enumerate(self.trail):
            alpha = i / len(self.trail)
            intensity = min(255, int(velocity * 0.5))
            color = (intensity, int(255 * alpha * 0.3), int(255 * alpha * 0.1))
            pygame.draw.circle(screen, color, pos, max(1, int(self.radius * alpha * 0.7)))

        if velocity > 300:
            color = (255, 100, 0)
        elif velocity > 150:
            color = (255, 200, 0)
        else:
            color = (255, 0, 0)

        pygame.draw.circle(screen, color, (int(self.x), int(self.y)), self.radius)
        pygame.draw.circle(screen, (0, 0, 0), (int(self.x), int(self.y)), self.radius, 2)
