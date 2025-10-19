"""
UI System for Mini Clans
Handles all rendering and user interface
"""

import pygame
from config import *

class Button:
    def __init__(self, x, y, width, height, text, action):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action
        self.hovered = False
        
    def draw(self, screen, font):
        color = BUTTON_HOVER if self.hovered else BUTTON_COLOR
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, UI_TEXT_COLOR, self.rect, 2)
        
        text_surf = font.render(self.text, True, UI_TEXT_COLOR)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)
        
    def check_hover(self, pos):
        self.hovered = self.rect.collidepoint(pos)
        
    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

class UI:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 32)
        self.small_font = pygame.font.Font(None, 24)
        self.title_font = pygame.font.Font(None, 64)
        
        # Menu buttons
        self.menu_buttons = [
            Button(450, 300, 300, 60, "HOST GAME", "HOST"),
            Button(450, 380, 300, 60, "JOIN GAME", "JOIN"),
            Button(450, 460, 300, 60, "QUIT", "QUIT")
        ]
        
        # Build mode buttons
        self.build_buttons = [
            Button(850, 50, 150, 40, "Gold Mine", "BUILD_GOLDMINE"),
            Button(850, 100, 150, 40, "Elixir Coll.", "BUILD_ELIXIR"),
            Button(850, 150, 150, 40, "Cannon", "BUILD_CANNON"),
            Button(850, 200, 150, 40, "Storage", "BUILD_STORAGE"),
            Button(850, 300, 150, 40, "ATTACK!", "ATTACK")
        ]
        
        # Attack mode buttons
        self.troop_buttons = [
            Button(850, 50, 150, 40, "Barbarian", "TROOP_BARBARIAN"),
            Button(850, 100, 150, 40, "Archer", "TROOP_ARCHER")
        ]
        
    def draw_menu(self):
        """Draw main menu"""
        title = self.title_font.render("MINI CLANS", True, UI_TEXT_COLOR)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 150))
        self.screen.blit(title, title_rect)
        
        subtitle = self.font.render("2-Player Strategy Game", True, UI_TEXT_COLOR)
        subtitle_rect = subtitle.get_rect(center=(SCREEN_WIDTH // 2, 220))
        self.screen.blit(subtitle, subtitle_rect)
        
        mouse_pos = pygame.mouse.get_pos()
        for button in self.menu_buttons:
            button.check_hover(mouse_pos)
            button.draw(self.screen, self.font)
            
    def draw_waiting(self):
        """Draw waiting screen"""
        text = self.title_font.render("Waiting for player...", True, UI_TEXT_COLOR)
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(text, text_rect)
        
    def draw_build_mode(self, game_state):
        """Draw build mode interface"""
        # Draw grid
        self.draw_grid()
        
        # Draw player buildings
        for building in game_state.player_base.buildings:
            self.draw_building(building, (0, 255, 0))
            
        # Draw placing preview
        if game_state.placing_building:
            mouse_pos = pygame.mouse.get_pos()
            grid_pos = self.screen_to_grid(mouse_pos)
            size = BUILDINGS[game_state.placing_building]["size"]
            color = BUILDINGS[game_state.placing_building]["color"]
            self.draw_building_preview(grid_pos, size, color)
            
        # Draw UI panel
        self.draw_ui_panel(game_state.player_base)
        
        # Draw build buttons
        mouse_pos = pygame.mouse.get_pos()
        for button in self.build_buttons:
            button.check_hover(mouse_pos)
            button.draw(self.screen, self.small_font)
            
        # Draw building costs
        y_offset = 50
        for button in self.build_buttons[:4]:
            building_type = button.action.split("_")[1]
            cost = BUILDINGS[building_type]
            cost_text = f"G:{cost['cost_gold']} E:{cost['cost_elixir']}"
            text_surf = self.small_font.render(cost_text, True, UI_TEXT_COLOR)
            self.screen.blit(text_surf, (1010, y_offset + 10))
            y_offset += 50
            
    def draw_attack_mode(self, game_state):
        """Draw attack mode interface"""
        # Draw grid
        self.draw_grid()
        
        # Draw opponent buildings
        for building in game_state.opponent_base.buildings:
            self.draw_building(building, (255, 0, 0))
            
        # Draw player troops
        for troop in game_state.player_troops:
            self.draw_troop(troop, (0, 255, 0))
            
        # Draw opponent troops
        for troop in game_state.opponent_troops:
            self.draw_troop(troop, (255, 0, 0))
            
        # Draw UI panel
        self.draw_ui_panel(game_state.player_base)
        
        # Draw troop selection buttons
        mouse_pos = pygame.mouse.get_pos()
        for button in self.troop_buttons:
            button.check_hover(mouse_pos)
            button.draw(self.screen, self.small_font)
            
        # Draw troop costs
        y_offset = 50
        for button in self.troop_buttons:
            troop_type = button.action.split("_")[1]
            cost = TROOPS[troop_type]["cost_elixir"]
            cost_text = f"E:{cost}"
            text_surf = self.small_font.render(cost_text, True, UI_TEXT_COLOR)
            self.screen.blit(text_surf, (1010, y_offset + 10))
            y_offset += 50
            
        # Draw instructions
        inst_text = self.small_font.render("Click to deploy troops", True, UI_TEXT_COLOR)
        self.screen.blit(inst_text, (850, 200))
            
    def draw_grid(self):
        """Draw the game grid"""
        for x in range(GRID_WIDTH + 1):
            start_pos = (GRID_OFFSET_X + x * GRID_SIZE, GRID_OFFSET_Y)
            end_pos = (GRID_OFFSET_X + x * GRID_SIZE, GRID_OFFSET_Y + GRID_HEIGHT * GRID_SIZE)
            pygame.draw.line(self.screen, GRID_COLOR, start_pos, end_pos, 1)
            
        for y in range(GRID_HEIGHT + 1):
            start_pos = (GRID_OFFSET_X, GRID_OFFSET_Y + y * GRID_SIZE)
            end_pos = (GRID_OFFSET_X + GRID_WIDTH * GRID_SIZE, GRID_OFFSET_Y + y * GRID_SIZE)
            pygame.draw.line(self.screen, GRID_COLOR, start_pos, end_pos, 1)
            
    def draw_building(self, building, outline_color):
        """Draw a building on the grid"""
        x = GRID_OFFSET_X + building.position[0] * GRID_SIZE
        y = GRID_OFFSET_Y + building.position[1] * GRID_SIZE
        size = building.stats["size"] * GRID_SIZE
        
        # Draw building
        rect = pygame.Rect(x + 2, y + 2, size - 4, size - 4)
        pygame.draw.rect(self.screen, building.stats["color"], rect)
        pygame.draw.rect(self.screen, outline_color, rect, 2)
        
        # Draw HP bar
        hp_percent = building.hp / building.max_hp
        hp_bar_width = size - 8
        hp_bar_height = 4
        
        pygame.draw.rect(self.screen, (255, 0, 0), 
                        pygame.Rect(x + 4, y - 8, hp_bar_width, hp_bar_height))
        pygame.draw.rect(self.screen, (0, 255, 0), 
                        pygame.Rect(x + 4, y - 8, int(hp_bar_width * hp_percent), hp_bar_height))
                        
        # Draw level
        level_text = self.small_font.render(str(building.level), True, (255, 255, 255))
        level_rect = level_text.get_rect(center=(x + size // 2, y + size // 2))
        self.screen.blit(level_text, level_rect)
        
    def draw_building_preview(self, position, size, color):
        """Draw preview of building placement"""
        x = GRID_OFFSET_X + position[0] * GRID_SIZE
        y = GRID_OFFSET_Y + position[1] * GRID_SIZE
        pixel_size = size * GRID_SIZE
        
        rect = pygame.Rect(x + 2, y + 2, pixel_size - 4, pixel_size - 4)
        
        # Draw semi-transparent preview
        s = pygame.Surface((pixel_size - 4, pixel_size - 4))
        s.set_alpha(128)
        s.fill(color)
        self.screen.blit(s, (x + 2, y + 2))
        pygame.draw.rect(self.screen, GRID_HIGHLIGHT, rect, 3)
        
    def draw_troop(self, troop, color):
        """Draw a troop on the grid"""
        x = GRID_OFFSET_X + int(troop.position[0] * GRID_SIZE)
        y = GRID_OFFSET_Y + int(troop.position[1] * GRID_SIZE)
        
        # Draw troop as circle
        pygame.draw.circle(self.screen, troop.stats["color"], (x, y), 8)
        pygame.draw.circle(self.screen, color, (x, y), 8, 2)
        
        # Draw HP bar
        hp_percent = troop.hp / troop.stats["hp"]
        hp_bar_width = 16
        hp_bar_height = 3
        
        pygame.draw.rect(self.screen, (255, 0, 0), 
                        pygame.Rect(x - 8, y - 15, hp_bar_width, hp_bar_height))
        pygame.draw.rect(self.screen, (0, 255, 0), 
                        pygame.Rect(x - 8, y - 15, int(hp_bar_width * hp_percent), hp_bar_height))
        
    def draw_ui_panel(self, base):
        """Draw resource display panel"""
        panel_rect = pygame.Rect(850, 400, 330, 350)
        pygame.draw.rect(self.screen, UI_BG_COLOR, panel_rect)
        pygame.draw.rect(self.screen, UI_TEXT_COLOR, panel_rect, 2)
        
        # Draw resources
        gold_text = self.font.render(f"Gold: {int(base.gold)}", True, GOLD_MINE_COLOR)
        self.screen.blit(gold_text, (870, 420))
        
        elixir_text = self.font.render(f"Elixir: {int(base.elixir)}", True, ELIXIR_COLLECTOR_COLOR)
        self.screen.blit(elixir_text, (870, 460))
        
        # Draw building count
        building_text = self.small_font.render(f"Buildings: {len(base.buildings)}", True, UI_TEXT_COLOR)
        self.screen.blit(building_text, (870, 520))
        
        # Draw tips
        tip_lines = [
            "Build gold mines and",
            "elixir collectors to",
            "generate resources.",
            "",
            "Build defenses to",
            "protect your base!"
        ]
        
        y_pos = 570
        for line in tip_lines:
            tip_text = self.small_font.render(line, True, (200, 200, 200))
            self.screen.blit(tip_text, (870, y_pos))
            y_pos += 25
        
    def handle_menu_click(self, pos):
        """Handle menu button clicks"""
        for button in self.menu_buttons:
            if button.is_clicked(pos):
                if button.action == "QUIT":
                    import sys
                    pygame.quit()
                    sys.exit()
                return button.action
        return None
        
    def handle_build_click(self, pos):
        """Handle build mode button clicks"""
        for button in self.build_buttons:
            if button.is_clicked(pos):
                return button.action
        return None
        
    def handle_attack_click(self, pos):
        """Handle attack mode button clicks"""
        for button in self.troop_buttons:
            if button.is_clicked(pos):
                return button.action
        return None
        
    def screen_to_grid(self, screen_pos):
        """Convert screen coordinates to grid coordinates"""
        grid_x = (screen_pos[0] - GRID_OFFSET_X) // GRID_SIZE
        grid_y = (screen_pos[1] - GRID_OFFSET_Y) // GRID_SIZE
        return (max(0, min(GRID_WIDTH - 1, grid_x)), 
                max(0, min(GRID_HEIGHT - 1, grid_y)))
        
    def get_ip_input(self):
        """Get IP address input from user (simple version)"""
        # For simplicity, return localhost
        # In a full version, you'd show an input dialog
        return DEFAULT_HOST