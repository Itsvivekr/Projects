from itertools import permutations

class Goodie:
    def __init__(self, label, weight, position):
        self.label = label
        self.weight = weight
        self.position = position  # position on land (1-based index)

class CargoShipsArrangement:
    def __init__(self, goodies, k):
        self.goodies = goodies
        self.k = k
        self.unique_labels = sorted(set(g.label for g in goodies))

    def calculate_cost(self, arrangement):
        label_to_position = {label: i+1 for i, label in enumerate(arrangement)}
        total_cost = 0
        for good in self.goodies:
            dist = abs(good.position - label_to_position[good.label])
            total_cost += good.weight * dist
        return total_cost

    def find_min_cost_arrangements(self):
        min_cost = float('inf')
        valid_arrangements = []
        for perm in permutations(self.unique_labels):
            cost = self.calculate_cost(perm)
            if cost < min_cost:
                min_cost = cost
                valid_arrangements = [perm]
            elif cost == min_cost:
                valid_arrangements.append(perm)
        valid_arrangements.sort()
        return min_cost, valid_arrangements

    def get_kth_arrangement(self):
        min_cost, arrangements = self.find_min_cost_arrangements()
        kth_arrangement = arrangements[self.k-1]  # Kth arrangement (1-based)
        return min_cost, kth_arrangement

def main():
    n = int(input().strip())
    goodies = []
    for i in range(n):
        label, weight = input().strip().split()
        weight = int(weight)
        goodies.append(Goodie(label, weight, i+1))
    k = int(input().strip())

    solver = CargoShipsArrangement(goodies, k)
    min_cost, arrangement = solver.get_kth_arrangement()

    print(min_cost)
    print(" ".join(arrangement))

if __name__ == "__main__":
    main()
