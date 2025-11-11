"""
Game State Management
Handles all game logic, buildings, troops, and resources
"""

import json
import time
from config import *

class Building:
    def __init__(self, building_type, position, level=1):
        self.type = building_type
        self.position = position  
        self.level = level
        self.hp = BUILDINGS[building_type]["hp"]
        self.max_hp = self.hp
        self.stats = BUILDINGS[building_type].copy()
        
    def to_dict(self):
        return {
            "type": self.type,
            "position": self.position,
            "level": self.level,
            "hp": self.hp
        }
        
    @staticmethod
    def from_dict(data):
        b = Building(data["type"], tuple(data["position"]), data["level"])
        b.hp = data["hp"]
        return b
        
    def upgrade(self):
        if self.level < self.stats["max_level"]:
            self.level += 1
            self.max_hp = int(self.hp * 1.2)
            self.hp = self.max_hp
            return True
        return False
        
    def take_damage(self, damage):
        self.hp -= damage
        return self.hp <= 0

class Troop:
    def __init__(self, troop_type, position):
        self.type = troop_type
        self.position = list(position) 
        self.stats = TROOPS[troop_type].copy()
        self.hp = self.stats["hp"]
        self.target = None
        
    def update(self, dt, buildings):
        if not self.target or self.target.hp <= 0:
          
            self.target = self.find_nearest_building(buildings)
            
        if self.target:
            
            dx = self.target.position[0] - self.position[0]
            dy = self.target.position[1] - self.position[1]
            dist = (dx**2 + dy**2)**0.5
            
            if dist <= self.stats["range"]:
                
                self.attack(self.target, dt)
            else:
                
                if dist > 0:
                    self.position[0] += (dx / dist) * self.stats["speed"] * dt
                    self.position[1] += (dy / dist) * self.stats["speed"] * dt
                    
    def find_nearest_building(self, buildings):
        nearest = None
        min_dist = float('inf')
        for building in buildings:
            if building.hp > 0:
                dx = building.position[0] - self.position[0]
                dy = building.position[1] - self.position[1]
                dist = (dx**2 + dy**2)**0.5
                if dist < min_dist:
                    min_dist = dist
                    nearest = building
        return nearest
        
    def attack(self, target, dt):
        
        target.take_damage(self.stats["damage"] * dt)
        
    def take_damage(self, damage):
        self.hp -= damage
        return self.hp <= 0

class Base:
    def __init__(self):
        self.buildings = []
        self.gold = STARTING_GOLD
        self.elixir = STARTING_ELIXIR
        self.last_resource_update = time.time()
        
        
        self.add_building(Building("TOWNHALL", (7, 7)))
        
    def add_building(self, building):
        self.buildings.append(building)
        
    def add_building_from_dict(self, data):
        self.buildings.append(Building.from_dict(data))
        
    def update_resources(self):
        current_time = time.time()
        dt = current_time - self.last_resource_update
        self.last_resource_update = current_time
        
        
        for building in self.buildings:
            if building.type == "GOLDMINE" and building.hp > 0:
                self.gold += building.stats["production_rate"] * dt
            elif building.type == "ELIXIR" and building.hp > 0:
                self.elixir += building.stats["production_rate"] * dt
                
    def can_afford_building(self, building_type):
        cost_gold = BUILDINGS[building_type]["cost_gold"]
        cost_elixir = BUILDINGS[building_type]["cost_elixir"]
        return self.gold >= cost_gold and self.elixir >= cost_elixir
        
    def purchase_building(self, building_type):
        if self.can_afford_building(building_type):
            self.gold -= BUILDINGS[building_type]["cost_gold"]
            self.elixir -= BUILDINGS[building_type]["cost_elixir"]
            return True
        return False
        
    def can_place_building(self, position, size):
        
        if position[0] < 0 or position[0] + size > GRID_WIDTH:
            return False
        if position[1] < 0 or position[1] + size > GRID_HEIGHT:
            return False
            
        
        for building in self.buildings:
            b_size = building.stats["size"]
            if self.rectangles_overlap(
                position, size,
                building.position, b_size
            ):
                return False
        return True
        
    @staticmethod
    def rectangles_overlap(pos1, size1, pos2, size2):
        return not (pos1[0] + size1 <= pos2[0] or
                    pos2[0] + size2 <= pos1[0] or
                    pos1[1] + size1 <= pos2[1] or
                    pos2[1] + size2 <= pos1[1])
                    
    def to_dict(self):
        return {
            "buildings": [b.to_dict() for b in self.buildings],
            "gold": self.gold,
            "elixir": self.elixir
        }
        
    @staticmethod
    def from_dict(data):
        base = Base()
        base.buildings = [Building.from_dict(b) for b in data["buildings"]]
        base.gold = data["gold"]
        base.elixir = data["elixir"]
        return base

class GameState:
    def __init__(self):
        self.player_base = Base()
        self.opponent_base = Base()
        self.player_troops = []
        self.opponent_troops = []
        
        self.placing_building = None
        self.selected_troop = "BARBARIAN"
        
    def start_placing_building(self, building_type):
        if self.player_base.can_afford_building(building_type):
            self.placing_building = building_type
            
    def place_building(self, position):
        if self.placing_building:
            size = BUILDINGS[self.placing_building]["size"]
            if self.player_base.can_place_building(position, size):
                if self.player_base.purchase_building(self.placing_building):
                    building = Building(self.placing_building, position)
                    self.player_base.add_building(building)
                    self.placing_building = None
                    return True
        return False
        
    def deploy_troop(self, position):
        if self.player_base.elixir >= TROOPS[self.selected_troop]["cost_elixir"]:
            self.player_base.elixir -= TROOPS[self.selected_troop]["cost_elixir"]
            troop = Troop(self.selected_troop, position)
            self.player_troops.append(troop)
            return True
        return False
        
    def add_opponent_troop(self, position, troop_type):
        troop = Troop(troop_type, position)
        self.opponent_troops.append(troop)
        
    def update(self, dt):
        
        self.player_base.update_resources()
        self.opponent_base.update_resources()
        
        
        for troop in self.player_troops[:]:
            troop.update(dt, self.opponent_base.buildings)
            if troop.hp <= 0:
                self.player_troops.remove(troop)
                
        
        for troop in self.opponent_troops[:]:
            troop.update(dt, self.player_base.buildings)
            if troop.hp <= 0:
                self.opponent_troops.remove(troop)
                
    def save_game(self, filename="savegame.json"):
        data = {
            "player_base": self.player_base.to_dict(),
            "opponent_base": self.opponent_base.to_dict()
        }
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
            
    def load_game(self, filename="savegame.json"):
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
            self.player_base = Base.from_dict(data["player_base"])
            self.opponent_base = Base.from_dict(data["opponent_base"])
            return True
        except FileNotFoundError:

            return False
