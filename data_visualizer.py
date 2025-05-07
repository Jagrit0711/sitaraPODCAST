import pygame
import random
import math
import time

class DataVisualizer:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.data = {
            'Temperature (K)': [],
            'Mass (Solar)': [],
            'Luminosity (Solar)': []
        }
        self.max_points = 100
        self.colors = {
            'Temperature (K)': (255, 100, 100),
            'Mass (Solar)': (100, 255, 100),
            'Luminosity (Solar)': (100, 100, 255)
        }
        
    def update(self, simulation):
        try:
            # Simple data collection without stage checks
            temp = 3000 + (simulation.time * 1000)  # Temperature increases with time
            mass = simulation.mass
            lum = mass * (1 + simulation.time)  # Luminosity increases with time
            
            # Add small variations
            temp += random.uniform(-100, 100)
            mass += random.uniform(-0.05, 0.05)
            lum += random.uniform(-0.1, 0.1)
            
            # Update data points
            self._update_data('Temperature (K)', temp)
            self._update_data('Mass (Solar)', mass)
            self._update_data('Luminosity (Solar)', lum)
        except Exception as e:
            print(f"Debug - Graph update error: {e}")
    
    def draw(self, screen):
        try:
            # Draw semi-transparent background
            graph_surface = pygame.Surface((400, 500), pygame.SRCALPHA)
            pygame.draw.rect(graph_surface, (20, 20, 40, 200), (0, 0, 400, 500))
            screen.blit(graph_surface, (20, 20))
            
            # Create a separate area for labels and graphs
            y_offset = 40
            graph_height = 120
            total_section_height = 160  # Total height for each section (label + graph)
            
            for key, values in self.data.items():
                if not values:
                    continue
                
                # Draw label in a fixed position above the graph area
                font = pygame.font.Font(None, 28)
                title = font.render(f"{key}: {values[-1]:.1f}", True, self.colors[key])
                label_y = y_offset
                screen.blit(title, (30, label_y))
                
                # Draw graph in its own dedicated area below the label
                if len(values) > 1:
                    points = []
                    max_val = max(values)
                    min_val = min(values)
                    range_val = max(max_val - min_val, 0.001)
                    
                    graph_y = label_y + 30  # Start graph 30 pixels below label
                    
                    for i, val in enumerate(values):
                        x = 30 + (i / self.max_points) * 360
                        y = graph_y + ((val - min_val) / range_val) * graph_height
                        points.append((int(x), int(y)))
                    
                    pygame.draw.lines(screen, self.colors[key], False, points, 2)
                
                y_offset += total_section_height  # Move to next section
                
        except Exception as e:
            print(f"Debug - Graph draw error: {e}")
    
    def _get_stage_temperature(self, stage):
        temps = {
            'Stellar Nebula': 2000,
            'Protostar': 3000,
            'Main Sequence': 5000,
            'Red Supergiant': 3500,
            'Supernova': 100000,
            'Final Form': 1000
        }
        # Get the stage value from enum
        stage_str = stage.value
        return temps.get(stage_str, 3000)
    
    def _calculate_luminosity(self, simulation):
        stage_multipliers = {
            'Stellar Nebula': 0.1,
            'Protostar': 0.5,
            'Main Sequence': 1.0,
            'Red Supergiant': 5.0,
            'Supernova': 100.0,
            'Final Form': 0.01
        }
        # Get the stage value from enum
        stage_str = simulation.current_stage.value
        mult = stage_multipliers.get(stage_str, 1.0)
        
        # Calculate base luminosity from mass
        base = simulation.mass ** 3.5
        return base * mult
    
    def _update_data(self, key, value):
        self.data[key].append(value)
        if len(self.data[key]) > self.max_points:
            self.data[key].pop(0)
