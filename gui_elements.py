import pygame
import pygame.font

class Timeline:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.current_time = 0
        self.slider_rect = pygame.Rect(100, height - 50, width - 200, 20)
        self.auto_button = pygame.Rect(width - 80, height - 50, 60, 20)
        self.auto_play = False  # Added this line
        
        # Phase markers
        self.phases = [
            (0, "Nebula"),
            (2, "Protostar"),
            (4, "Main Sequence"),
            (8, "Red Supergiant"),
            (11, "Supernova"),
            (12, "Final")
        ]
        
    def draw(self, screen):
        # Draw timeline base
        pygame.draw.rect(screen, (100, 100, 150), self.slider_rect)
        
        # Draw phase markers
        font = pygame.font.Font(None, 20)
        for time, phase in self.phases:
            x = self.slider_rect.x + (time / 12) * self.slider_rect.width
            pygame.draw.line(screen, (200, 200, 250), (x, self.slider_rect.y), (x, self.slider_rect.y + self.slider_rect.height), 2)
            text = font.render(phase, True, (200, 200, 250))
            screen.blit(text, (x - 20, self.slider_rect.y + 25))
        
        # Draw current time marker
        pos_x = self.slider_rect.x + (self.current_time / 12) * self.slider_rect.width
        pygame.draw.circle(screen, (255, 255, 100), (int(pos_x), self.slider_rect.centery), 8)
        
        # Draw year text
        year_text = font.render(f"Time: {self.current_time:.1f} billion years", True, (200, 200, 250))
        screen.blit(year_text, (self.slider_rect.x, self.slider_rect.y - 25))
        
        # Draw auto-play button
        color = (100, 200, 100) if self.auto_play else (150, 150, 150)
        pygame.draw.rect(screen, color, self.auto_button)
        auto_text = font.render("Auto", True, (0, 0, 0))
        screen.blit(auto_text, (self.auto_button.x + 5, self.auto_button.y + 2))
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.slider_rect.collidepoint(event.pos):
                # Update time based on click position
                rel_x = event.pos[0] - self.slider_rect.x
                self.current_time = (rel_x / self.slider_rect.width) * 12
                self.current_time = max(0, min(12, self.current_time))
                # Check if clicked near a phase marker
                for time, _ in self.phases:
                    marker_x = self.slider_rect.x + (time / 12) * self.slider_rect.width
                    if abs(event.pos[0] - marker_x) < 10:
                        self.current_time = time
                        break
            elif self.auto_button.collidepoint(event.pos):
                self.auto_play = not self.auto_play
                
        elif event.type == pygame.MOUSEMOTION and event.buttons[0]:
            if self.slider_rect.collidepoint(event.pos):
                # Update time while dragging
                rel_x = event.pos[0] - self.slider_rect.x
                self.current_time = (rel_x / self.slider_rect.width) * 12
                self.current_time = max(0, min(12, self.current_time))
class ParameterControls:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.font = pygame.font.Font(None, 32)
        self.parameters = {
            "Mass (Solar Masses)": 20,
            "Metallicity": 0.02
        }
        self.min_values = {"Mass (Solar Masses)": 8, "Metallicity": 0.001}
        self.max_values = {"Mass (Solar Masses)": 50, "Metallicity": 0.03}
        self.dragging = None
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            for i, param in enumerate(self.parameters):
                slider_rect = self._get_slider_rect(i)
                if slider_rect.collidepoint(mouse_pos):
                    self.dragging = param
                    # Update value immediately on click
                    self._update_value(mouse_pos[0], param)
                    
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = None
            
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            self._update_value(pygame.mouse.get_pos()[0], self.dragging)
    
    def _update_value(self, mouse_x, param):
        slider_x = max(50, min(mouse_x, self.width - 250))
        param_range = self.max_values[param] - self.min_values[param]
        value = self.min_values[param] + (slider_x - 50) / (self.width - 300) * param_range
        self.parameters[param] = round(value, 3)
        
    def _get_slider_rect(self, index):
        return pygame.Rect(50, 50 + index * 60, self.width - 300, 20)
        
    def draw(self, screen):
        for i, (param, value) in enumerate(self.parameters.items()):
            # Draw parameter name
            text = self.font.render(f"{param}: {value:.2f}", True, (200, 200, 250))
            screen.blit(text, (50, 20 + i * 60))
            
            # Draw slider
            slider_rect = self._get_slider_rect(i)
            pygame.draw.rect(screen, (100, 100, 150), slider_rect)
            
            # Draw slider handle
            handle_x = 50 + (value - self.min_values[param]) / \
                (self.max_values[param] - self.min_values[param]) * (self.width - 300)
            pygame.draw.circle(screen, (255, 255, 100), 
                             (int(handle_x), slider_rect.centery), 15)