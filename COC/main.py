"""
Mini Clans - 2-Player Strategy Game
Main entry point and game initialization
"""

import pygame
import sys
from enum import Enum
from game_state import GameState
from network import NetworkManager
from ui import UI
from config import *

class GameMode(Enum):
    MENU = 0
    BUILD = 1
    ATTACK = 2
    WAITING = 3

class MiniClans:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Mini Clans - 2-Player Strategy")
        self.clock = pygame.time.Clock()
        
        self.game_state = GameState()
        self.network = NetworkManager()
        self.ui = UI(self.screen)
        
        self.mode = GameMode.MENU
        self.running = True
        self.is_host = False
        self.connected = False
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                
            if self.mode == GameMode.MENU:
                self.handle_menu_events(event)
            elif self.mode == GameMode.BUILD:
                self.handle_build_events(event)
            elif self.mode == GameMode.ATTACK:
                self.handle_attack_events(event)
                
    def handle_menu_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            action = self.ui.handle_menu_click(event.pos)
            if action == "HOST":
                self.is_host = True
                self.network.start_host()
                self.mode = GameMode.WAITING
                print("Waiting for player to join...")
            elif action == "JOIN":
                self.is_host = False
                ip = self.ui.get_ip_input()
                if self.network.join_game(ip):
                    self.connected = True
                    self.mode = GameMode.BUILD
                    print("Connected to host!")
                    
    def handle_build_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            action = self.ui.handle_build_click(event.pos)
            if action == "ATTACK":
                self.mode = GameMode.ATTACK
                
                self.network.send_data({"action": "ready_to_attack"})
            elif action and action.startswith("BUILD_"):
                building_type = action.split("_")[1]
                self.game_state.start_placing_building(building_type)
            elif self.game_state.placing_building:
                
                grid_pos = self.ui.screen_to_grid(event.pos)
                if self.game_state.place_building(grid_pos):
                    
                    self.network.send_data({
                        "action": "place_building",
                        "building": self.game_state.player_base.buildings[-1].to_dict()
                    })
                    
    def handle_attack_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  
                grid_pos = self.ui.screen_to_grid(event.pos)
                if self.game_state.deploy_troop(grid_pos):
                    
                    self.network.send_data({
                        "action": "deploy_troop",
                        "position": grid_pos,
                        "troop_type": self.game_state.selected_troop
                    })
                    
    def update(self, dt):
        
        self.game_state.update(dt)
        
        
        if self.connected or self.is_host:
            data = self.network.receive_data()
            if data:
                self.process_network_data(data)
                
        
        if self.is_host and not self.connected and self.mode == GameMode.WAITING:
            if self.network.check_connection():
                self.connected = True
                self.mode = GameMode.BUILD
                print("Player joined!")
                
    def process_network_data(self, data):
        action = data.get("action")
        if action == "place_building":
            
            building_data = data.get("building")
            self.game_state.opponent_base.add_building_from_dict(building_data)
        elif action == "deploy_troop":
            
            pos = data.get("position")
            troop_type = data.get("troop_type")
            self.game_state.add_opponent_troop(pos, troop_type)
        elif action == "ready_to_attack":
            
            pass
            
    def render(self):
        self.screen.fill(BACKGROUND_COLOR)
        
        if self.mode == GameMode.MENU:
            self.ui.draw_menu()
        elif self.mode == GameMode.WAITING:
            self.ui.draw_waiting()
        elif self.mode == GameMode.BUILD:
            self.ui.draw_build_mode(self.game_state)
        elif self.mode == GameMode.ATTACK:
            self.ui.draw_attack_mode(self.game_state)
            
        pygame.display.flip()
        
    def run(self):
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0
            self.handle_events()
            self.update(dt)
            self.render()
            
        self.cleanup()
        
    def cleanup(self):
        self.network.close()
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = MiniClans()

    game.run()
