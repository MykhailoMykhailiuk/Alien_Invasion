# Alien Invasion

A 2D arcade shooter built with Python and Pygame. Defeat alien fleets, survive as the difficulty increases, and face a boss every fifth level.

<img width="1168" height="901" alt="Boss" src="https://github.com/user-attachments/assets/dc2d458e-e9c1-4ee9-b7eb-0927f1758f8c" />


## Features

- Alien fleet movement and increasing level difficulty
- Boss battles every fifth level
- Score and persistent high-score tracking
- Three lives per game
- Random falling power-ups
- Boss health bar
- Keyboard controls and click-to-start menu

## Controls

| Action | Control |
|---|---|
| Move left | Left arrow |
| Move right | Right arrow |
| Fire | Space |
| Quit | Q |
| Start game | Click **Play** |

## Power-ups

Power-ups fall in wooden boxes and must be caught by the ship.

| Drop | Effect |
|---|---|
| `x2` | Doubles alien and boss points for 10 seconds |
| `>>` | Adds 5 to the active bullet limit, up to 20 |
| `+1` | Adds one ship |

The bullet limit starts at 5. Each collision with an alien or boss bullet reduces the rapid-fire bonus by 5, with 5 as the minimum.

## Requirements

- Python 3.10 or newer
- Pygame 2.6.1 or newer

## Installation

Clone the repository and enter the project directory:

```bash
git clone <repository-url>
cd Alien_Invasion
```

Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

Install Pygame:

```bash
python -m pip install -r requirements.txt
```

## Run the Game

With the virtual environment active, run:

```bash
python alien_invasion.py
```

Close the window or press `Q` to quit. The high score is stored in `high_score.txt`.

## Project Structure

| File | Purpose |
|---|---|
| `alien_invasion.py` | Main game loop and collision handling |
| `settings.py` | Screen, speed, bullet, boss, and difficulty settings |
| `ship.py` | Player ship |
| `alien.py` | Alien fleet and boss |
| `bullet.py` | Player and boss bullets |
| `drop.py` | Falling power-ups |
| `game_stats.py` | Score, level, lives, and multiplier state |
| `score_board.py` | Score, lives, level, and boss health display |
