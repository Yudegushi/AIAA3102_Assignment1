"""
ecosystem.py

This file defines the Ecosystem class of the Pythonic Ecosystem Simulator.

Responsibilities:
- Manage world state and control the simulation loop.
- Provide helper methods for organism interaction.
- Handle updates, births, deaths, movements.

"""

import random
import time
from organisms import Plant, Herbivore, Carnivore, PLANT_SYMBOL

random.seed(42)  # For reproducibility during testing

# General constants
CELL_WIDTH = 2
EMPTY_SYMBOL = '.'
DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
TICK_DELAY = 1

class Ecosystem:
    """Class representing the ecosystem simulation, including the 2D grid and the loop."""

    def __init__(self, width:int, height:int, initial_plants:int, initial_herbivores:int, initial_carnivores:int, total_ticks:int):
        # Initialize ecosystem parameters
        self.width = width
        self.height = height
        self.organisms = []
        self.total_ticks = total_ticks
        self.initial_helper_set = set() # Only used during initial population to avoid overlaps
        #self.generation = 0

        # Populate initial organisms
        self.populate(Plant, initial_plants)
        self.populate(Herbivore, initial_herbivores)
        self.populate(Carnivore, initial_carnivores)
        self.initial_helper_set.clear()

        # Temporary queue for new born and dead organisms during updates
        self.temp_added_organisms = []
        self.temp_removed_organisms = []

        # Display initial state
        print("Ecosystem simulation starting...")
        print("\n" + "=" * (self.width * (CELL_WIDTH+1)) + "\n")

        self.display(tick=0)
    
    # helper functions for ecosystem initialization
    def populate(self, organism_class, count):
        """Populate the ecosystem with a given number of organisms of a specific class."""
        for _ in range(count):
            (x, y) = self.random_empty_cell()
            if (x, y):
                organism = organism_class(x, y)
                self.organisms.append(organism)

    def random_empty_cell(self):
        """Return a single empty cell in the grid."""
        while True:
            x, y = random.randint(0, self.width-1), random.randint(0, self.height-1)
            if (x, y) not in self.initial_helper_set:
                self.initial_helper_set.add((x, y))
                return (x, y)
            
    # Define the helper functions for organism interactions below.
    def get_organism_at(self, x, y):
        """Return a specific organism at (x, y)."""
        return [org for org in self.organisms + self.temp_added_organisms if org.x == x and org.y == y and org.alive]


    def get_adjacent_cells(self, x, y):
        """Return a list of valid adjacent cells around (x, y)."""
        adjacent = []
        for dx, dy in DIRECTIONS:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.width and 0 <= ny < self.height:
                adjacent.append((nx, ny))
        return adjacent
    
    def get_adjacent_empty_cells(self, x, y):
        """Return a list of adjacent empty cells around (x, y)."""
        adjacent = self.get_adjacent_cells(x, y)
        return [(nx, ny) for (nx, ny) in adjacent if not self.get_organism_at(nx, ny)]
    
    def get_adjacent_organisms(self, x, y, target_organism_type):
        """Return a list of adjacent organisms around (x, y) by type."""
        adjacent = self.get_adjacent_cells(x, y)
        result = []
        for (nx, ny) in adjacent:
            for org in self.organisms + self.temp_added_organisms:
                if org.x == nx and org.y == ny and isinstance(org, target_organism_type) and org.alive:
                    result.append(org)
        return result
    
    def add_organism(self, organism):
        """Add a new organism to the ecosystem."""
        self.temp_added_organisms.append(organism)
    
    def remove_organism(self, organism):
        """Remove an organism from the ecosystem."""
        organism.alive = False
        self.temp_removed_organisms.append(organism)

    def move_organism(self, organism, new_x, new_y):
        """Move an organism to a new position."""
        organism.x = new_x
        organism.y = new_y

    # Main simulation loop and display functions
    def run(self):
        """
        Main simulation loop:
        - Shuffles organism list and make a copy.
        - Calls update() on each organism.
        - Processes births and deaths after all updates.
        - Displays the grid each tick.
        """
        for tick in range(self.total_ticks):
            tick += 1

            # Shuffle and copy organism list to avoid modification during iteration
            organisms = self.organisms.copy()
            random.shuffle(organisms)
            
            # Update each organism
            for org in list(organisms):
                if org.alive:
                    org.update(self)

            # Process births and deaths after all updates
            # Notice that newly born organisms might also be eaten in the same tick
            for org in self.temp_added_organisms:
                if org.alive:
                    self.organisms.append(org)


            for org in self.temp_removed_organisms:
                if org in self.organisms:
                    self.organisms.remove(org)
            self.temp_added_organisms.clear()
            self.temp_removed_organisms.clear()

            # Display the current state of the ecosystem
            self.display(tick)

            # Delay for visualization
            time.sleep(TICK_DELAY)
    
    def display(self, tick):
        """Display the current state of the ecosystem grid in aligned columns."""

        # Create empty grid
        grid = [[EMPTY_SYMBOL for _ in range(self.width)] for _ in range(self.height)]

        # Place organisms in the grid
        for org in self.organisms:
            if org.alive:
                grid[org.y][org.x] = org.symbol

        # Display summary statistics
        print(f"Tick: {tick}, "
            f"Plants: {sum(isinstance(o, Plant) and o.alive for o in self.organisms)}, "
            f"Herbivores: {sum(isinstance(o, Herbivore) and o.alive for o in self.organisms)}, "
            f"Carnivores: {sum(isinstance(o, Carnivore) and o.alive for o in self.organisms)}")

        # Display the grid with aligned columns
        for row in grid:
            for cell in row:
                if cell == EMPTY_SYMBOL or cell == PLANT_SYMBOL: # Empty and Plant cells get extra space for alignment
                    print(cell.center(CELL_WIDTH), end=' ')
                else:
                    print(cell.center(CELL_WIDTH), end='')
            print()

        print("\n" + "=" * (self.width * (CELL_WIDTH+1)) + "\n")

    

    
