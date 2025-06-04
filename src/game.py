import pygame
import math
from entities.bird import Bird
from entities.slingshot import Slingshot
from entities.obstacle import Obstacle

WIDTH, HEIGHT = 1200, 700
GROUND_Y = HEIGHT - 50
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BROWN = (139, 69, 19)
GRAY = (200, 200, 200)

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Pelota - Colisión Física")
        self.clock = pygame.time.Clock()

        # Entradas
        self.mass_input = "0.4"
        self.ob1_mass_input = "2.0"
        self.ob2_mass_input = "3.0"

        self.bird = Bird(120, GROUND_Y - 100)
        self.slingshot = Slingshot(self.bird)
        self.obstacles = [
            Obstacle(700, GROUND_Y - 100, 50, 100, mass=float(self.ob1_mass_input)),
            Obstacle(900, GROUND_Y - 100, 50, 100, mass=float(self.ob2_mass_input))
        ]

        self.restart_button = pygame.Rect(WIDTH - 150, HEIGHT - 50, 120, 35)
        self.font = pygame.font.Font(None, 26)

        self.running = True
        self.last_collision_data = None
        self.collision_timer = 0
        self.active_input = None

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            self.slingshot.handle_event(event)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.restart_button.collidepoint(event.pos):
                    self.reset_game()
                # Detectar campo de texto activo
                self.active_input = None
                for i, rect in enumerate(self.input_boxes()):
                    if rect.collidepoint(event.pos):
                        self.active_input = i
                        break

            elif event.type == pygame.KEYDOWN:
                if self.active_input is not None:
                    if event.key == pygame.K_BACKSPACE:
                        self.edit_input(self.active_input, backspace=True)
                    elif event.unicode.isdigit() or event.unicode == ".":
                        self.edit_input(self.active_input, char=event.unicode)

    def edit_input(self, field_index, char="", backspace=False):
        fields = [self.mass_input, self.ob1_mass_input, self.ob2_mass_input]
        if backspace:
            fields[field_index] = fields[field_index][:-1]
        else:
            if len(fields[field_index]) < 6:
                fields[field_index] += char

        self.mass_input, self.ob1_mass_input, self.ob2_mass_input = fields

    def reset_game(self):
        self.bird = Bird(120, GROUND_Y - 100)
        self.bird.mass = float(self.mass_input)
        self.slingshot = Slingshot(self.bird)
        self.obstacles = [
            Obstacle(700, GROUND_Y - 100, 50, 100, mass=float(self.ob1_mass_input)),
            Obstacle(900, GROUND_Y - 100, 50, 100, mass=float(self.ob2_mass_input))
        ]
        self.last_collision_data = None
        self.collision_timer = 0

    def update(self, dt):
        self.bird.update(dt)

        for obs in self.obstacles:
            data = obs.check_collision(self.bird)
            if data:
                self.last_collision_data = data
                self.collision_timer = 3  # 3 segundos para mostrar datos

        if self.collision_timer > 0:
            self.collision_timer -= dt
            if self.collision_timer <= 0:
                self.last_collision_data = None

        if self.bird.approach_ground_limit():
            speed = math.sqrt(self.bird.vx**2 + self.bird.vy**2)
            if speed < 1:
                self.bird.vx = 0
                self.bird.vy = 0
                self.bird.launched = False

    def input_boxes(self):
        base_x = WIDTH - 190
        return [
            pygame.Rect(base_x, 205, 80, 30),
            pygame.Rect(base_x, 240, 80, 30),
            pygame.Rect(base_x, 275, 80, 30)
        ]

    def draw(self):
        self.screen.fill(WHITE)
        pygame.draw.line(self.screen, BROWN, (0, GROUND_Y), (WIDTH, GROUND_Y), 5)

        for obs in self.obstacles:
            obs.draw(self.screen)

        self.slingshot.draw(self.screen)
        self.bird.draw(self.screen)

        # Panel lateral
        panel_x = WIDTH - 320
        pygame.draw.rect(self.screen, (240, 240, 240), (panel_x, 10, 310, 350))
        pygame.draw.rect(self.screen, BLACK, (panel_x, 10, 310, 350), 2)

        velocity = math.sqrt(self.bird.vx**2 + self.bird.vy**2)
        velocity_kmh = velocity * 3.6

        stats = [
            f"Masa pelota: {self.bird.mass} kg",
            f"Velocidad: {velocity_kmh:.1f} km/h",
            f"Posición: ({int(self.bird.x)}, {int(self.bird.y)})",
            f"Tiempo vuelo: {self.bird.flight_time:.2f} s",
            f"Distancia: {self.bird.total_distance:.1f} px",
        ]
        for i, txt in enumerate(stats):
            rendered = self.font.render(txt, True, BLACK)
            self.screen.blit(rendered, (panel_x + 10, 20 + i * 30))

        labels = ["Masa (pelota):", "Masa obst. 1:", "Masa obst. 2:"]
        inputs = [self.mass_input, self.ob1_mass_input, self.ob2_mass_input]

        for i, (label, text) in enumerate(zip(labels, inputs)):
            y = 210 + i * 35
            label_r = self.font.render(label, True, BLACK)
            self.screen.blit(label_r, (panel_x + 10, y))

            box = self.input_boxes()[i]
            pygame.draw.rect(self.screen, WHITE, box)
            pygame.draw.rect(self.screen, BLACK, box, 2)
            input_r = self.font.render(text, True, BLACK)
            self.screen.blit(input_r, (box.x + 5, box.y + 5))

        pygame.draw.rect(self.screen, GRAY, self.restart_button)
        pygame.draw.rect(self.screen, BLACK, self.restart_button, 2)
        restart_text = self.font.render("Reiniciar", True, BLACK)
        self.screen.blit(restart_text, (self.restart_button.x + 10, self.restart_button.y + 5))

        if self.last_collision_data:
            pygame.draw.rect(self.screen, (255, 255, 200), (panel_x, 320, 310, 80))
            pygame.draw.rect(self.screen, BLACK, (panel_x, 320, 310, 80), 2)
            datos = self.last_collision_data
            col_texts = [
                f"Colisión: m1={datos['m1']} kg, v1={datos['v1']:.2f} px/s",
                f"            m2={datos['m2']} kg, v2'={datos['v2_final']:.2f} px/s"
            ]
            for i, text in enumerate(col_texts):
                rendered = self.font.render(text, True, BLACK)
                self.screen.blit(rendered, (panel_x + 10, 330 + i * 25))

        pygame.display.flip()

    def run(self):
        while self.running:
            dt = self.clock.tick(60) / 1000.0
            self.handle_events()
            self.update(dt)
            self.draw()

        pygame.quit()

if __name__ == "__main__":
    Game().run()
