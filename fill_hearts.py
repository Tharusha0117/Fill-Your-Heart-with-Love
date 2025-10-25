import pygame
import random
import math

pygame.init()

WIDTH, HEIGHT = 600, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Let's Fill Our Hearts ❤️")

font = pygame.font.Font(None, 48)
small_font = pygame.font.Font(None, 32)

PINK = (255, 100, 150)
RED = (255, 0, 80)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BG = (255, 228, 225) 

clock = pygame.time.Clock()

def draw_heart_shape(surface, color, x, y, size, angle=0, alpha=255):
    s = pygame.Surface((size*2, size*2), pygame.SRCALPHA)
    points = []
    for t in range(0, 360, 5):
        rad = math.radians(t)
        px = 16 * math.sin(rad)**3
        py = 13 * math.cos(rad) - 5 * math.cos(2*rad) - 2 * math.cos(3*rad) - math.cos(4*rad)
        points.append((size + px * size / 16, size - py * size / 16))

    if angle != 0:
        rotated = []
        for px, py in points:
            dx, dy = px - size, py - size
            rx = dx * math.cos(angle) - dy * math.sin(angle)
            ry = dx * math.sin(angle) + dy * math.cos(angle)
            rotated.append((rx + size, ry + size))
        points = rotated
    pygame.draw.polygon(s, (*color, alpha), points)
    surface.blit(s, (x - size, y - size))

class HeartParticle:
    def __init__(self, x, y, size=None):
        self.x = x
        self.y = y
        self.size = size if size else random.randint(10, 18)
        self.speed_y = random.uniform(-1.5, -3.0)
        self.speed_x = random.uniform(-0.7, 0.7)
        self.alpha = 255
        self.color = random.choice([PINK, RED, (255, 50, 100)])
        self.angle = random.uniform(-0.3, 0.3)  

    def update(self):
        self.y += self.speed_y
        self.x += self.speed_x
        self.alpha -= 3
        return self.alpha > 0

    def draw(self, surface):
        draw_heart_shape(surface, self.color, self.x, self.y, self.size, self.angle, self.alpha)

def heart_point(t, scale=1):
    x = 16 * math.sin(t)**3
    y = 13*math.cos(t) - 5 * math.cos(2*t) - 2*math.cos(3*t) - math.cos(4*t)
    return x*scale, -y*scale

def generate_heart_points(x, y, scale=10, steps=100):
    points = []
    for i in range(steps):
        t = math.pi * 2 * i / steps
        px, py = heart_point(t, scale)
        points.append((x + px, y + py))
    return points

particles = []
heart_particles = []
fill_progress = 0 
running = True
heart_center = (WIDTH // 2, 380)
heart_scale = 10
heart_outline = generate_heart_points(*heart_center, heart_scale)

while running:
    screen.fill(BG)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            for _ in range(15):
                x, y = pygame.mouse.get_pos()
                particles.append(HeartParticle(x, y))
            fill_progress = min(100, fill_progress + 3)

    particles = [p for p in particles if p.update()]
    for p in particles:
        p.draw(screen)

    if fill_progress > 0:
        num_particles = int(fill_progress * 2)
        for _ in range(num_particles):
            t = random.uniform(0, 2*math.pi)
            px, py = heart_point(t, heart_scale)
            hx = heart_center[0] + px + random.randint(-2, 2)
            hy = heart_center[1] + py + random.randint(-2, 2)
            heart_particles.append(HeartParticle(hx, hy, size=6))

    heart_particles = [p for p in heart_particles if p.update()]
    for p in heart_particles:
        p.draw(screen)

    title = font.render("Let's Fill Our Hearts", True, BLACK)
    screen.blit(title, (WIDTH / 2 - title.get_width() / 2, 50))

    pygame.draw.polygon(screen, WHITE, heart_outline, 2)

    pygame.draw.rect(screen, WHITE, (150, 600, 300, 25), 3)
    pygame.draw.rect(screen, RED, (150, 600, 3*fill_progress, 25))
    label = small_font.render(f"Love Level: {int(fill_progress)}%", True, WHITE)
    screen.blit(label, (230, 630))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
