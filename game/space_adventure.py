"""Interactive terminal-based space trading adventure game."""
from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Dict, Tuple


Coordinate = Tuple[int, int]


@dataclass
class Player:
    """State for the player's ship."""

    name: str
    health: int = 100
    fuel: int = 50
    credits: int = 0
    position: Coordinate = (0, 0)

    def adjust_health(self, amount: int) -> None:
        self.health = max(0, min(100, self.health + amount))

    def adjust_fuel(self, amount: int) -> None:
        self.fuel = max(0, self.fuel + amount)

    def adjust_credits(self, amount: int) -> None:
        self.credits = max(0, self.credits + amount)

    def move(self, direction: str) -> bool:
        row, col = self.position
        deltas = {"north": (-1, 0), "south": (1, 0), "west": (0, -1), "east": (0, 1)}
        if direction not in deltas:
            return False

        delta_row, delta_col = deltas[direction]
        new_position = (row + delta_row, col + delta_col)
        if any(abs(value) > 2 for value in new_position):
            return False

        self.position = new_position
        self.adjust_fuel(-2)
        return True


class Game:
    """Main game logic for the space adventure."""

    def __init__(self, player: Player) -> None:
        self.player = player
        self.planet_events: Dict[Coordinate, str] = {}
        self.turn = 1

    def _generate_event(self) -> str:
        events = (
            "You discovered ancient ruins and sold artifacts.",
            "You helped a stranded miner and were rewarded.",
            "Pirates ambushed you!",
            "Radiation storms damaged your ship.",
            "A prosperous trade route netted you a tidy profit.",
            "You found a fuel depot just in time.",
        )
        return random.choice(events)

    def _apply_event(self, event: str) -> None:
        if "Pirates" in event:
            self.player.adjust_health(-20)
            self.player.adjust_credits(-10)
        elif "Radiation" in event:
            self.player.adjust_health(-15)
        elif "fuel depot" in event:
            self.player.adjust_fuel(10)
        else:
            credits = random.randint(5, 25)
            self.player.adjust_credits(credits)

    def _describe_location(self) -> str:
        row, col = self.player.position
        return f"Planet sector ({row}, {col})"

    def _check_game_over(self) -> bool:
        if self.player.health <= 0:
            print("Your ship can no longer operate. Game over!")
            return True
        if self.player.fuel <= 0:
            print("You've run out of fuel and drift into the void. Game over!")
            return True
        if self.player.credits >= 100:
            print("You amassed enough credits to retire comfortably. You win!")
            return True
        return False

    def take_turn(self, command: str) -> bool:
        command = command.lower().strip()
        if command in {"north", "south", "east", "west"}:
            if self.player.move(command):
                location = self.player.position
                if location not in self.planet_events:
                    event = self._generate_event()
                    self.planet_events[location] = event
                    print(event)
                    self._apply_event(event)
                else:
                    print("You've been here before and nothing has changed.")
            else:
                print("You can't travel that way.")
        elif command == "status":
            self.print_status()
        elif command == "rest":
            self.player.adjust_health(5)
            self.player.adjust_fuel(-1)
            print("You take some time to recover.")
        elif command == "quit":
            print("Thanks for playing!")
            return False
        else:
            print("Unknown command. Try north, south, east, west, status, rest, or quit.")

        self.turn += 1
        self.player.adjust_fuel(-1)
        return not self._check_game_over()

    def print_status(self) -> None:
        position = self.player.position
        print(
            f"Turn {self.turn}: {self.player.name} | Health: {self.player.health} "
            f"Fuel: {self.player.fuel} | Credits: {self.player.credits} | "
            f"Location: {position}"
        )


def greet_player() -> str:
    print(
        "Welcome to Star Trader!\n"
        "Earn 100 credits before you run out of fuel or health.\n"
        "Commands: north, south, east, west, status, rest, quit.\n"
    )
    name = input("What is your captain's name? ").strip() or "Captain"
    return name


def main() -> None:
    """Entry point for the game."""

    name = greet_player()
    player = Player(name=name)
    game = Game(player)
    game.print_status()

    running = True
    while running:
        command = input("\nEnter command: ")
        running = game.take_turn(command)


if __name__ == "__main__":
    main()
