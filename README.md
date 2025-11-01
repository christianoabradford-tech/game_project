# game_project

Star Trader is a lightweight, terminal-based space trading adventure. Earn 100 credits before your fuel or health are depleted by exploring the surrounding sectors, resting, and dealing with random encounters.

## Running the game

```bash
python -m game.space_adventure
```

You will be prompted to enter a captain name and then can issue commands each turn:

- `north`, `south`, `east`, `west` &mdash; travel between sectors (moving costs fuel)
- `status` &mdash; review the current turn, location, health, fuel, and credits
- `rest` &mdash; recover a small amount of health at the cost of a little fuel
- `quit` &mdash; leave the game early

Plan your routes carefully to discover profitable events, avoid hazards, and reach 100 credits before your ship runs out of fuel or falls apart.
