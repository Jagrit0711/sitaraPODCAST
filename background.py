import pygame
import random
import math

class Background:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.stars = []
        self.nebula_points = []
        self.camera_x = 0
        self.camera_y = 0
        self.zoom = 1.0
        self.generate_stars(200)
        self.generate_nebula(50)
        
    def generate_stars(self, count):
        self.stars = []
        for _ in range(count):
            self.stars.append({
                'x': random.randint(-self.width, self.width*2),
                'y': random.randint(-self.height, self.height*2),
                'size': random.uniform(1, 3),
                'brightness': random.uniform(0.3, 1.0),
                'twinkle_speed': random.uniform(0.01, 0.05)
            })
            
    def generate_nebula(self, count):
        self.nebula_points = []
        for _ in range(count):
            self.nebula_points.append({
                'x': random.randint(-self.width//2, int(self.width*1.5)),  # Fixed: Convert to int
                'y': random.randint(-self.height//2, int(self.height*1.5)),  # Fixed: Convert to int
                'radius': random.randint(50, 200),
                'color': (random.randint(20, 60), random.randint(20, 60), random.randint(50, 100)),
                'alpha': random.randint(20, 50)
            })
    
    def update(self):
        for star in self.stars:
            star['brightness'] = 0.3 + (math.sin(pygame.time.get_ticks() * star['twinkle_speed']) + 1) * 0.35
            
    def apply_zoom(self, factor):
        self.zoom = max(0.5, min(2.0, self.zoom * factor))
        
    def move_camera(self, dx, dy):
        self.camera_x += dx / self.zoom
        self.camera_y += dy / self.zoom
        
    def draw(self, screen):
        # Draw nebula
        nebula_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        for point in self.nebula_points:
            x = (point['x'] + self.camera_x) * self.zoom
            y = (point['y'] + self.camera_y) * self.zoom
            color = (*point['color'], point['alpha'])
            pygame.draw.circle(nebula_surface, color, (int(x), int(y)), 
                             int(point['radius'] * self.zoom))
        screen.blit(nebula_surface, (0, 0), special_flags=pygame.BLEND_ALPHA_SDL2)
        
        # Draw stars
        for star in self.stars:
            x = (star['x'] + self.camera_x) * self.zoom
            y = (star['y'] + self.camera_y) * self.zoom
            if 0 <= x <= self.width and 0 <= y <= self.height:
                brightness = int(255 * star['brightness'])
                pygame.draw.circle(screen, (brightness, brightness, brightness), 
                                 (int(x), int(y)), int(star['size'] * self.zoom))