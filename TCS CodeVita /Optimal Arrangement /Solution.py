class Goodie:
    def __init__(self, label, weight, position):
        self.label = label
        self.weight = weight
        self.position = position  # Position on land (1-indexed)

class CargoShipsArrangement:
    def __init__(self, goodies, k):
        self.goodies = goodies
        self.k = k
        # Unique sorted labels of cargo ships
        self.unique_labels = sorted(set(g.label for g in goodies))
        self.label_count = len(self.unique_labels)
        # Map from label to index for quick lookup
        self.label_indices = {label: i for i, label in enumerate(self.unique_labels)}
        # Group goodies by their cargo ship label index
        self.goodies_by_label = [[] for _ in range(self.label_count)]
        for good in goodies:
            idx = self.label_indices[good.label]
            self.goodies_by_label[idx].append(good)

        self.used = [False] * self.label_count
        self.current_arrangement = [None] * self.label_count
        self.min_cost = float('inf')
        self.kth_arrangement = None
        self.count = 0  # count of minimum cost arrangements found

    def backtrack(self, pos=0, current_cost=0):
        # If full arrangement formed
        if pos == self.label_count:
            if current_cost < self.min_cost:
                self.min_cost = current_cost
                self.count = 1
                self.kth_arrangement = self.current_arrangement[:]
            elif current_cost == self.min_cost:
                self.count += 1
                if self.count == self.k:
                    self.kth_arrangement = self.current_arrangement[:]
            return

        # Prune if current cost exceeds minimum found
        if current_cost > self.min_cost:
            return

        for i in range(self.label_count):
            if not self.used[i]:
                label = self.unique_labels[i]
                # Calculate incremental cost for placing label at position pos
                added_cost = 0
                for good in self.goodies_by_label[i]:
                    dist = abs(good.position - (pos + 1))
                    added_cost += good.weight * dist

                new_cost = current_cost + added_cost
                if new_cost <= self.min_cost:
                    self.used[i] = True
                    self.current_arrangement[pos] = label
                    self.backtrack(pos + 1, new_cost)
                    self.used[i] = False
                    self.current_arrangement[pos] = None

def main():
    n = int(input().strip())
    goodies = []
    for i in range(n):
        label, weight = input().strip().split()
        weight = int(weight)
        goodies.append(Goodie(label, weight, i + 1))
    k = int(input().strip())

    solver = CargoShipsArrangement(goodies, k)
    solver.backtrack()

    print(solver.min_cost)
    print(" ".join(solver.kth_arrangement))


if __name__ == "__main__":
    main()
