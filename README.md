# HeatSeek

A 2D hide and seek game where the AI learns your movement patterns and gets smarter every session.

## How it works
You move around a maze with WASD trying to avoid the seeker. The seeker tracks where you spend the most time using a heatmap, then uses BFS pathfinding to hunt you down. The longer you play across sessions, the better it knows your habits.

## Features
- WASD movement with wall collision
- Line of sight detection — seeker catches you if it has a clear view
- Heatmap AI that learns your favorite hiding spots
- BFS pathfinding for shortest route navigation
- 70/30 explore vs exploit balance
- Persistent memory — heatmap saves between sessions

## Run it
```bash
pip install pygame numpy
python HeatSeek.py
```

## Concepts used
- Breadth First Search (BFS)
- Heatmap / pattern learning
- Explore vs exploit tradeoff
- 2D grid collision detection
- NumPy for matrix operations

## Version 2 (planned)
- Random map generation
- Diagonal line of sight
- Score and survival timer
- Game over screen
