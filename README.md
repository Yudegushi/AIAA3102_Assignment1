# Pythonic Ecosystem Simulator 

## 1.Student Information
- **Name:** **** *****
- **Student ID:** ********

---

## 2. How to Run

Follow these steps to run the simulation from the command line:

```bash
# 1. Ensure Python 3.12 is installed. (Other vesions should also be OK, since no external libraries are required)
# 2. (Optional) Create and activate a virtual environment.
# 3. Unzip the submission .zip file.
# 4. Navigate to the project directory in your terminal.
cd ********_*********_A1
# 5. Run the main script:
python main.py
# No external libraries are required, only the Python standard library (random, time, abc) is used.
```
You will then be prompted to enter:

- Grid width and height (Positive integers)

- Initial number of plants, herbivores, and carnivores (Non-negative integers)

- Number of simulation ticks (Positive integer)

---

## 3. Design Decision Discussion
### Design Choice:

I decided to store all organisms in a **single list** without maintaining a dynamic 2D grid array that stores all the cell's information.

### Reasoning:

Using only one list makes the simulation state much easier to manage at each tick.
- All organisms are stored together in a single data structure, each organism simply carries its own (x, y) position and a alive status.
- When a new organism is born or an existing one dies, I only need to update the main organism list plus the two temporary lists (temp_added_organisms and temp_removed_organisms) that handle births and deaths at the end of each tick.
- This approach keeps the update logic clean and avoids the complexity of maintaining the 2d array with more possible bugs, especially during ticks with birth and death.

- Under this data structure, the **interaction logic** is also intuitive and accords with the OOP concept. A organism will look around and check if its 8 adjacent cells are occupied, instead of having the simulation system directly offering environment information.

### Alternative Considered:

An alternative would be to maintain **both a 2D array and a list** simultaneously, with the 2D array directly storing which organism occupies each cell.
- This design could speed up certain operations such as finding adjacent empty cells or nearby organisms, since it avoids scanning the entire list each time.
- However, this would also make the implementation more complicated. Every time an organism moves, reproduces, or dies, the grid array would need to be updated accordingly.
- Given the small scale of this project and the relatively low number of organisms, the performance gain would be minimal, while the maintenance cost would increase significantly.
  
Therefore, I chose to keep a single list for simplicity and clarity.

---

## 4. Simulation Extension Proposal
### New Feature: Intelligent Movement 
In this extended version, both herbivores and carnivores would exhibit **"intelligent"** decision-making instead of purely random movement.
The new system introduces three interconnected behaviors:

- Predator Hunting Strategy: Carnivores actively move toward the nearest herbivore within their visible range (e.g., within 2 cells).

- Prey Avoidance Strategy: Herbivores detect nearby carnivores and move away from them whenever possible.

- Grouping Behavior: Herbivores prefer to move closer to other herbivores to form small groups.

These behaviors transform the simulation from random motions to mimicing basic animal intelligence, which will greatly enhance visual effect.

### Current Problem:
- Currently, all animals move randomly when they do not eat or reproduce.
- This randomness makes the code simple, but the visual effect is disordered.
- In nature, predators and preys do not wander aimlessly. Predators try to chase, prey animals try to excape and perform grouping behavior for protection.

### Implementation Plan

1. New Constants:

- Define VISION_RANGE = 2 for both Herbivores and Carnivores to limit how far they can “see.”

2. Modify Movement Logic:

- Replace random moves in move() with direction-based movement:

  - Carnivores: Search for the closest herbivore within vision range using Euclidean distance. Move one step toward it (if the cell is empty).

  - Herbivores: If a carnivore is detected nearby, choose a move that increases distance from it. Else if a plant is nearby, choose to move towards it.

  - Otherwise: Herbivores prefer moving closer to nearby herbivores (grouping behavior).

3. Add helper functions in ecosystem:

- Add a function: find_nearest_organism(x, y, target_class, max_distance) to locate the nearest prey or predator.

The implementation won't be too complex, but the visual effect will be much better.


