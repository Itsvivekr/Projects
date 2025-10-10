from itertools import permutations
from collections import defaultdict

class Goodie:
    def __init__(self, label, weight, position):
        self.label = label
        self.weight = weight
        self.position = position  # land position (1 km, 2 km, ...)

class CargoShip:
    def __init__(self, label, position):
        self.label = label
        self.position = position  # sea position (1 km, 2 km, ...)

class ArrangementOptimizer:
    def __init__(self, goodies, K):
        self.goodies = goodies
        self.K = K
        # Extract unique cargo ship labels
        self.unique_labels = sorted(set(g.label for g in goodies))

    def calculate_cost(self, arrangement):
        """Calculate total transport cost for a given arrangement of ships."""
        label_to_position = {label: idx+1 for idx, label in enumerate(arrangement)}
        total_cost = 0
        for g in self.goodies:
            ship_pos = label_to_position[g.label]
            distance = abs(g.position - ship_pos)
            total_cost += g.weight * distance
        return total_cost

    def find_optimal_arrangement(self):
        """Find the minimum cost arrangement and return the Kth alphabetical one."""
        min_cost = float('inf')
        valid_arrangements = []

        # Try all permutations of cargo ships
        for perm in permutations(self.unique_labels):
            cost = self.calculate_cost(perm)
            if cost < min_cost:
                min_cost = cost
                valid_arrangements = [perm]
            elif cost == min_cost:
                valid_arrangements.append(perm)

        # Sort alphabetically and pick Kth
        valid_arrangements.sort()
        kth_arrangement = valid_arrangements[self.K - 1]
        return min_cost, kth_arrangement

    @staticmethod
    def from_input():
        """Helper to read input in required format."""
        N = int(input().strip())
        goodies = []
        for i in range(N):
            label, weight = input().split()
            goodies.append(Goodie(label, int(weight), i+1))
        K = int(input().strip())
        return ArrangementOptimizer(goodies, K)

def main():
    optimizer = ArrangementOptimizer.from_input()
    min_cost, arrangement = optimizer.find_optimal_arrangement()
    print(min_cost)
    print(" ".join(arrangement))

if __name__ == "__main__":
    main()
