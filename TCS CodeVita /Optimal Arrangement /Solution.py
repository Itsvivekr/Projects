from itertools import permutations

class Goodie:
    def __init__(self, label, weight, position):
        self.label = label
        self.weight = weight
        self.position = position

def main():
    n = int(input())
    goodies = []
    for i in range(n):
        label, weight = input().strip().split()
        goodies.append((label, int(weight), i+1))
    k = int(input())

    # Find all unique cargo ship labels
    unique_labels = sorted(set(label for label, _, _ in goodies))
    label_count = len(unique_labels)
    min_cost = float('inf')
    arrangements = []

    # Try all arrangements of cargo ship labels
    for perm in permutations(unique_labels):
        label_to_pos = {label: i+1 for i, label in enumerate(perm)}
        total_cost = sum(weight * abs(pos - label_to_pos[label]) for label, weight, pos in goodies)
        if total_cost < min_cost:
            min_cost = total_cost
            arrangements = [perm]
        elif total_cost == min_cost:
            arrangements.append(perm)

    # Sort minimum arrangements lexicographically and get k-th (1-based)
    arrangements.sort()
    print(min_cost)
    print(" ".join(arrangements[k-1]))

if __name__ == "__main__":
    main()
