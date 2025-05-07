import pygame
import math
import random
from enum import Enum

class StarStage(Enum):
    NEBULA = "Stellar Nebula"
    PROTOSTAR = "Protostar"
    MAIN_SEQUENCE = "Main Sequence"
    RED_SUPERGIANT = "Red Supergiant"
    SUPERNOVA = "Supernova"
    FINAL = "Final Form"

class StarSimulation:
    def __init__(self):
        self.current_stage = StarStage.NEBULA
        self.time = 0
        self.base_size = 150
        self.size = self.base_size
        self.particles = []
        self.mass = 20
        self.metallicity = 0.02
        self.transition_progress = 0
        self.generate_particles(150)
        
        # Enhanced colors with more gradients
        self.colors = {
            StarStage.NEBULA: [(40, 60, 100), (70, 100, 150), (100, 150, 200), (150, 200, 255)],
            StarStage.PROTOSTAR: [(180, 100, 50), (200, 150, 100), (255, 200, 150)],
            StarStage.MAIN_SEQUENCE: [(255, 230, 150), (255, 255, 200), (255, 255, 150)],
            StarStage.RED_SUPERGIANT: [(200, 50, 20), (255, 100, 50), (255, 150, 100)],
            StarStage.SUPERNOVA: [(255, 255, 255), (255, 255, 50), (255, 200, 50), (255, 150, 50)],
            StarStage.FINAL: [(20, 20, 20), (50, 50, 50), (30, 30, 30)]
        }
        
        # Size multipliers for each stage
        self.size_multipliers = {
            StarStage.NEBULA: 2,
            StarStage.PROTOSTAR: 1.5,
            StarStage.MAIN_SEQUENCE: 1,
            StarStage.RED_SUPERGIANT: 3,
            StarStage.SUPERNOVA: 4,
            StarStage.FINAL: 0.5
        }
        
    def generate_particles(self, count):
        self.particles = []
        for _ in range(count):
            self.particles.append(self._create_particle())
    
    def _create_particle(self):
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(0.5, 2)
        distance = random.uniform(self.size * 0.8, self.size * 2.5)
        return {
            'angle': angle,
            'speed': speed,
            'distance': distance,
            'size': random.uniform(2, 6),
            'opacity': random.uniform(0.3, 1.0)
        }
            
    def update(self):
        # Update time and stage
        prev_stage = self.current_stage
        
        if self.time < 0.5:
            self.current_stage = StarStage.NEBULA
        elif self.time < 2:
            self.current_stage = StarStage.PROTOSTAR
        elif self.time < 8:
            self.current_stage = StarStage.MAIN_SEQUENCE
        elif self.time < 11.9:
            self.current_stage = StarStage.RED_SUPERGIANT
        elif self.time < 11.99:
            self.current_stage = StarStage.SUPERNOVA
        else:
            self.current_stage = StarStage.FINAL
            
        # Handle stage transition
        if prev_stage != self.current_stage:
            self.transition_progress = 0
        self.transition_progress = min(1, self.transition_progress + 0.02)
        
        # Update size based on stage and mass
        target_size = self.base_size * self.size_multipliers[self.current_stage] * (self.mass / 20)
        self.size += (target_size - self.size) * 0.1
        
        # Update particles
        for particle in self.particles:
            particle['angle'] += particle['speed'] * 0.02 * (self.mass / 20)
            particle['opacity'] = random.uniform(0.3, 1.0)
            
            # Regenerate particles that get too far
            if random.random() < 0.01:
                particle.update(self._create_particle())
            
    def draw(self, screen):
        center_x = screen.get_width() // 2
        center_y = screen.get_height() // 2
        
        # Draw background glow
        glow_surface = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
        colors = self.colors[self.current_stage]
        for i in range(15):
            alpha = int(100 - i * 6)
            color = (*colors[0][:3], alpha)
            radius = self.size * (1.5 + i * 0.2)
            pygame.draw.circle(glow_surface, color, (center_x, center_y), int(radius))
        screen.blit(glow_surface, (0, 0))
        
        # Draw particles with opacity
        for particle in self.particles:
            x = center_x + math.cos(particle['angle']) * particle['distance']
            y = center_y + math.sin(particle['angle']) * particle['distance']
            color = random.choice(self.colors[self.current_stage])
            particle_surface = pygame.Surface((int(particle['size'] * 2), int(particle['size'] * 2)), pygame.SRCALPHA)
            pygame.draw.circle(particle_surface, (*color, int(255 * particle['opacity'])),
                             (int(particle['size']), int(particle['size'])), int(particle['size']))
            screen.blit(particle_surface, (int(x - particle['size']), int(y - particle['size'])))
        
        # Draw star core with enhanced gradient
        for i in range(int(self.size), 0, -2):
            progress = i / self.size
            color_idx = min(int(progress * len(colors)), len(colors) - 1)
            color = colors[color_idx]
            pygame.draw.circle(screen, color, (center_x, center_y), i)
            
        # Special effects for supernova
        if self.current_stage == StarStage.SUPERNOVA:
            for _ in range(10):
                angle = random.uniform(0, 2 * math.pi)
                distance = random.uniform(0, self.size * 2)
                x = center_x + math.cos(angle) * distance
                y = center_y + math.sin(angle) * distance
                size = random.uniform(2, 8)
                color = random.choice(colors)
                pygame.draw.circle(screen, color, (int(x), int(y)), int(size))