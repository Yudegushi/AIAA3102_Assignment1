"""
main.py

This file is the entry point for the Pythonic Ecosystem Simulator.
Handles:
- User input and validation
- Ecosystem initialization
- Running the simulation

"""
from ecosystem import Ecosystem

def get_simulation_parameters():
    """
    Prompt the user step-by-step for simulation parameters.
    Following parameters are requested in order:
    - Grid width (positive integer)
    - Grid height (positive integer)
    - Initial number of plants (non-negative integer)
    - Initial number of herbivores (non-negative integer)
    - Initial number of carnivores (non-negative integer)
    - Number of simulation ticks (positive integer)
    Validates input and ensures total organisms ≤ grid capacity.
    """
    
    print("\nWelcome to the Pythonic Ecosystem Simulator Setup!\n"
          "Please enter simulation parameters one by one:\n")

    # Grid dimensions
    width = get_positive_integer("Enter grid width (>0): ")
    height = get_positive_integer("Enter grid height (>0): ")
    max_capacity = width * height
    print(f"Grid capacity: {max_capacity} cells\n")

    # Initial organism counts
    plants = get_positive_integer("Enter initial number of plants (≥0): ", allow_zero=True)
    herbivores = get_positive_integer("Enter initial number of herbivores (≥0): ", allow_zero=True)
    carnivores = get_positive_integer("Enter initial number of carnivores (≥0): ", allow_zero=True)

    # Check if total exceeds grid capacity
    try:
        total = plants + herbivores + carnivores
        if total > max_capacity:
            raise ValueError(f"Total organisms ({total}) exceed grid capacity ({max_capacity}).")
    except ValueError as e:
        print(f"{e} Please re-enter all parameters.\n")
        return get_simulation_parameters()  # Restart input process if invalid

    # Simulation ticks
    ticks = get_positive_integer("Enter number of simulation ticks (>0): ")

    # Success message
    print(f"\n   Simulation parameters accepted:"
          f"\n   Grid size: {width} ×s {height}"
          f"\n   Plants: {plants}"
          f"\n   Herbivores: {herbivores}"
          f"\n   Carnivores: {carnivores}"
          f"\n   Simulation ticks: {ticks}\n")

    return width, height, plants, herbivores, carnivores, ticks

def get_positive_integer(prompt, allow_zero=False):
    """ Helper function to get a positive integer from user input. """
    while True:
        try:
            user_input = input(prompt).strip()
            value = int(user_input)
            
            if value < 0 or (not allow_zero and value == 0):
                raise ValueError("Value must be positive." if not allow_zero else "Value cannot be negative.")
            return value
        except ValueError as e:
            print(f"Invalid input: {e} Please enter a valid integer (digits only).")
        except Exception as e:
            print(f"Unexpected error: {e}")

def main():
    """Get parameters, initialize ecosystem, and run simulation."""
    width, height, plants, herbivores, carnivores, ticks = get_simulation_parameters()
    ecosystem = Ecosystem(width, height, plants, herbivores, carnivores, ticks)
    ecosystem.run()
    print("Simulation ended.")

if __name__ == "__main__":
    main()
