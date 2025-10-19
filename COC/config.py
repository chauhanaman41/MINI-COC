"""
Configuration file for Mini Clans
Contains all game constants and settings
"""

# Screen settings
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
FPS = 60

# Grid settings
GRID_SIZE = 20
GRID_WIDTH = 15
GRID_HEIGHT = 15
GRID_OFFSET_X = 50
GRID_OFFSET_Y = 50

# Colors
BACKGROUND_COLOR = (34, 139, 34)  # Forest green
GRID_COLOR = (100, 100, 100)
GRID_HIGHLIGHT = (255, 255, 0)
UI_BG_COLOR = (50, 50, 50)
UI_TEXT_COLOR = (255, 255, 255)
BUTTON_COLOR = (70, 130, 180)
BUTTON_HOVER = (100, 160, 210)

# Building colors
TOWN_HALL_COLOR = (184, 134, 11)
GOLD_MINE_COLOR = (255, 215, 0)
ELIXIR_COLLECTOR_COLOR = (255, 105, 180)
DEFENSE_COLOR = (139, 0, 0)
STORAGE_COLOR = (160, 82, 45)

# Troop colors
BARBARIAN_COLOR = (255, 140, 0)
ARCHER_COLOR = (138, 43, 226)

# Network settings
DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 5555

# Game balance
STARTING_GOLD = 1000
STARTING_ELIXIR = 1000

# Building costs and stats
BUILDINGS = {
    "TOWNHALL": {
        "cost_gold": 0,
        "cost_elixir": 0,
        "hp": 2000,
        "size": 3,
        "color": TOWN_HALL_COLOR,
        "max_level": 5
    },
    "GOLDMINE": {
        "cost_gold": 100,
        "cost_elixir": 0,
        "hp": 500,
        "size": 2,
        "production_rate": 10,  # per second
        "color": GOLD_MINE_COLOR,
        "max_level": 10
    },
    "ELIXIR": {
        "cost_gold": 0,
        "cost_elixir": 100,
        "hp": 500,
        "size": 2,
        "production_rate": 10,
        "color": ELIXIR_COLLECTOR_COLOR,
        "max_level": 10
    },
    "CANNON": {
        "cost_gold": 200,
        "cost_elixir": 0,
        "hp": 600,
        "size": 2,
        "damage": 20,
        "range": 5,
        "attack_speed": 1.0,
        "color": DEFENSE_COLOR,
        "max_level": 10
    },
    "STORAGE": {
        "cost_gold": 150,
        "cost_elixir": 150,
        "hp": 800,
        "size": 2,
        "capacity": 5000,
        "color": STORAGE_COLOR,
        "max_level": 5
    }
}

# Troop stats
TROOPS = {
    "BARBARIAN": {
        "cost_elixir": 50,
        "training_time": 5,
        "hp": 100,
        "damage": 15,
        "speed": 2.0,
        "range": 1,
        "color": BARBARIAN_COLOR
    },
    "ARCHER": {
        "cost_elixir": 75,
        "training_time": 10,
        "hp": 50,
        "damage": 10,
        "speed": 1.5,
        "range": 4,
        "color": ARCHER_COLOR
    }
}