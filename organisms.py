"""
organisms.py

This file defines all organism classes used in the Ecosystem Simulator.
The structure follows an OOP hierarchy:
- Organism
  - Plant
  - Animal
    - Herbivore
    - Carnivore
"""

import random
from abc import ABC, abstractmethod


# Plant behavior constants
PLANT_SYMBOL = '☘'
PLANT_REPRODUCTION_CHANCE = 0.10

# Animal base class constants
METABOLIC_ENERGY_COST = 1

# Herbivore behavior constants
HERBIVORE_SYMBOL = '🐇'
HERBIVORE_INITIAL_ENERGY = 15
HERBIVORE_EAT_GAIN = 10
HERBIVORE_REPRODUCTION_ENERGY_THRESHOLD = 20
HERBIVORE_REPRODUCTION_CHANCE = 0.15
HERBIVORE_REPRODUCTION_COST = 8
HERBIVORE_CHILD_ENERGY = 10

# Carnivore behavior constants
CARNIVORE_SYMBOL = '🐅'
CARNIVORE_INITIAL_ENERGY = 25
CARNIVORE_EAT_GAIN = 15
CARNIVORE_REPRODUCTION_ENERGY_THRESHOLD = 40
CARNIVORE_REPRODUCTION_CHANCE = 0.10
CARNIVORE_REPRODUCTION_COST = 20
CARNIVORE_CHILD_ENERGY = 20

class Organism(ABC):
    """Base class for all organisms in the ecosystem."""

    def __init__(self, x:int, y:int, symbol:str):
        self.x = x
        self.y = y
        self.symbol = symbol
        self.alive = True

    @abstractmethod
    def update(self, x, y, ecosystem):
        """Specific simulation behavior is to be defined in subclasses."""
        pass

class Plant(Organism):
    """Class representing a plant in the ecosystem."""

    def __init__(self, x:int, y:int):
        super().__init__(x, y, PLANT_SYMBOL)

    def update(self, ecosystem):
        """Plants try to reproduce based on chance."""
        if random.random() < PLANT_REPRODUCTION_CHANCE:
            empty_cells = ecosystem.get_adjacent_empty_cells(self.x, self.y)
            if empty_cells:
                new_x, new_y = random.choice(empty_cells)
                new_plant = Plant(new_x, new_y)
                ecosystem.add_organism(new_plant)

class Animal(Organism, ABC):
    """Base class for all animals in the ecosystem."""

    def __init__(self, x:int, y:int, symbol:str, initial_energy:int):
        super().__init__(x, y, symbol)
        self.energy = initial_energy

    def update(self, ecosystem):
        """Update metabolic cost."""
        self.energy -= METABOLIC_ENERGY_COST

    # Define common animal behaviors below.
    def move(self, ecosystem):
        """Move to a random adjacent empty cell."""
        empty_cells = ecosystem.get_adjacent_empty_cells(self.x, self.y)
        if empty_cells:
            new_x, new_y = random.choice(empty_cells)
            ecosystem.move_organism(self, new_x, new_y)

    def eat(self, ecosystem, prey_class, eat_gain):
        """Try to eat a prey organism in adjacent cells."""
        prey_list = ecosystem.get_adjacent_organisms(self.x, self.y, prey_class)
        if prey_list:
            prey = random.choice(prey_list)
            ecosystem.move_organism(self, prey.x, prey.y)
            ecosystem.remove_organism(prey)
            self.energy += eat_gain
            return True
        return False
    
    def reproduce(self, ecosystem, reproduction_energy_threshold, reproduction_chance, reproduction_cost, child_class, child_energy):
        """Try to reproduce if energy and chance conditions are met."""
        if self.energy >= reproduction_energy_threshold and random.random() < reproduction_chance:
            empty_cells = ecosystem.get_adjacent_empty_cells(self.x, self.y)
            if empty_cells:
                new_x, new_y = random.choice(empty_cells)
                new_child = child_class(new_x, new_y)
                new_child.energy = child_energy
                ecosystem.add_organism(new_child)
                self.energy -= reproduction_cost
                return True
        return False
    
    def survive(self, ecosystem):
        """Check if the animal survives; remove if energy ≤ 0."""
        if self.energy <= 0:
            ecosystem.remove_organism(self)
            return False
        return True

class Herbivore(Animal):
    """Class representing a herbivore in the ecosystem."""

    def __init__(self, x:int, y:int):
        super().__init__(x, y, HERBIVORE_SYMBOL, HERBIVORE_INITIAL_ENERGY)

    def update(self, ecosystem):
        """Behavior order: update -> eat -> reproduce -> move -> survive"""
        
        # 1. Metabolic cost
        super().update(ecosystem)

        # 2. Try to act (eat, reproduce, move) in order.
        acted = False
        if not acted and self.eat(ecosystem, Plant, HERBIVORE_EAT_GAIN):
            acted = True
        if not acted and self.reproduce(ecosystem, HERBIVORE_REPRODUCTION_ENERGY_THRESHOLD, HERBIVORE_REPRODUCTION_CHANCE, HERBIVORE_REPRODUCTION_COST, Herbivore, HERBIVORE_CHILD_ENERGY):
            acted = True
        if not acted:
            self.move(ecosystem)

        # 3. Check survival
        self.survive(ecosystem)

class Carnivore(Animal):
    """Class representing a carnivore in the ecosystem."""

    def __init__(self, x:int, y:int):
        super().__init__(x, y, CARNIVORE_SYMBOL, CARNIVORE_INITIAL_ENERGY)

    def update(self, ecosystem):
        """Behavior order: update -> eat -> reproduce -> move -> survive"""
        
        # 1. Metabolic cost
        super().update(ecosystem)

        # 2. Try to act (eat, reproduce, move) in order.
        acted = False
        if not acted and  self.eat(ecosystem, Herbivore, CARNIVORE_EAT_GAIN):
            acted = True
        if not acted and self.reproduce(ecosystem, CARNIVORE_REPRODUCTION_ENERGY_THRESHOLD, CARNIVORE_REPRODUCTION_CHANCE, CARNIVORE_REPRODUCTION_COST, Carnivore, CARNIVORE_CHILD_ENERGY):
            acted = True
        if not acted:
            self.move(ecosystem)

        # 3. Check survival
        self.survive(ecosystem)
