# 🏰 Mini Clans - 2-Player Strategy Game

A 2D base-building and attack strategy game inspired by Clash of Clans, built entirely in Python for local/LAN multiplayer.

## 🎮 Features

- **Base Building**: Place and upgrade buildings on a grid
- **Resource Management**: Generate gold and elixir over time
- **Multiplayer**: 2-player over localhost or LAN
- **Attack System**: Deploy troops to attack opponent's base
- **Real-time Combat**: Troops automatically target and destroy buildings
- **Save/Load**: Persistent game state

## 📋 Requirements

- Python 3.7+
- Pygame library

## 🚀 Installation

1. Install Python (if not already installed)
2. Install Pygame:
```bash
pip install pygame
```

3. Download all game files:
   - `main.py`
   - `config.py`
   - `game_state.py`
   - `network.py`
   - `ui.py`

4. Place all files in the same directory

## 🎯 How to Play

### Starting a Game

**Player 1 (Host):**
1. Run `python main.py`
2. Click "HOST GAME"
3. Wait for Player 2 to join
4. Note: Your IP address will be `127.0.0.1` for localhost or your LAN IP

**Player 2 (Client):**
1. Run `python main.py` on another terminal/computer
2. Click "JOIN GAME"
3. Game will connect to `127.0.0.1` by default (localhost)
4. For LAN: Modify the `get_ip_input()` method in `ui.py` to return the host's LAN IP

### Build Mode

1. **View Resources**: Check your gold and elixir in the right panel
2. **Place Buildings**:
   - Click building buttons on the right
   - Click on the grid to place
   - Buildings cost resources
3. **Building Types**:
   - **Gold Mine**: Generates gold over time (Cost: 100 gold)
   - **Elixir Collector**: Generates elixir over time (Cost: 100 elixir)
   - **Cannon**: Defensive tower (Cost: 200 gold)
   - **Storage**: Increases resource capacity (Cost: 150 gold, 150 elixir)
4. **Ready to Attack**: Click "ATTACK!" button when ready

### Attack Mode

1. **Select Troops**: Click on Barbarian or Archer button
2. **Deploy Troops**: Click anywhere on the grid to deploy
3. **Watch the Battle**: Troops automatically move and attack buildings
4. **Victory Conditions**: 
   - Destroy opponent's Town Hall
   - Achieve higher destruction percentage

### Buildings

| Building | Cost | Function |
|----------|------|----------|
| Town Hall | Free (starts placed) | Main building - protect it! |
| Gold Mine | 100 Gold | Produces 10 gold/second |
| Elixir Collector | 100 Elixir | Produces 10 elixir/second |
| Cannon | 200 Gold | Defensive tower |
| Storage | 150 Gold, 150 Elixir | Stores resources |

### Troops

| Troop | Cost | HP | Damage | Range | Speed |
|-------|------|----|----|-------|-------|
| Barbarian | 50 Elixir | 100 | 15 | Melee (1) | Fast (2.0) |
| Archer | 75 Elixir | 50 | 10 | Ranged (4) | Medium (1.5) |

## 🎨 Game Controls

- **Left Click**: Place buildings, deploy troops, click buttons
- **Mouse**: Move cursor to see building previews

## 🔧 Configuration

Edit `config.py` to customize:

- Screen size
- Grid dimensions
- Building costs and stats
- Troop stats
- Resource generation rates
- Network settings (IP and port)

## 🌐 Network Setup

### Same Computer (Localhost)
- Default setting works automatically
- Both players use `127.0.0.1`

### Different Computers (LAN)
1. Find host's local IP:
   - Windows: `ipconfig` in cmd
   - Mac/Linux: `ifconfig` in terminal
2. Modify `ui.py` → `get_ip_input()` method to return the host's IP
3. Ensure both computers are on same network
4. Check firewall allows port 5555

## 📁 File Structure

```
mini-clans/
├── main.py           # Main game loop and initialization
├── config.py         # All game constants and settings
├── game_state.py     # Game logic, buildings, troops
├── network.py        # Multiplayer networking
├── ui.py            # User interface and rendering
└── savegame.json    # Auto-generated save file
```

## 🐛 Troubleshooting

**Connection Failed**
- Check both players are on same network
- Verify firewall isn't blocking port 5555
- Try running both instances on same computer first

**Game Lag**
- Reduce FPS in `config.py`
- Close other applications
- Use localhost instead of LAN

**Buildings Won't Place**
- Check you have enough resources
- Ensure position doesn't overlap existing buildings
- Make sure building fits within grid

## 🎓 Learning Resources

This game demonstrates:
- **Pygame**: 2D graphics and game loops
- **Socket Programming**: Client-server architecture
- **Threading**: Concurrent network communication
- **Object-Oriented Design**: Classes for game entities
- **JSON Serialization**: Save/load game state

## 🔮 Future Enhancements

- [ ] AI opponent for single-player
- [ ] More building types (barracks, walls, traps)
- [ ] Additional troop types
- [ ] Upgrade system for buildings
- [ ] Sound effects and music
- [ ] Better UI with input dialogs
- [ ] Replay system
- [ ] Tournament mode
- [ ] Cloud saves

## 📝 Code Structure

### Main Components

1. **GameState**: Manages all game logic
2. **Base**: Holds buildings and resources
3. **Building**: Individual structures
4. **Troop**: Combat units
5. **NetworkManager**: Handles multiplayer
6. **UI**: Rendering and user interface

## 🤝 Contributing

Ideas for improvements:
- Add new building types
- Create new troop classes
- Improve AI targeting
- Add animations
- Create better networking with lobby system

## 📜 License

Free to use and modify for educational purposes.

## 🎉 Credits

Inspired by Clash of Clans by Supercell
Built with Python and Pygame

---

**Enjoy building your base and crushing your opponent! 🏰⚔️**
