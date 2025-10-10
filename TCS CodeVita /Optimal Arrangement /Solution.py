from itertools import permutations

def main():
    n = int(input())
    goodies = []
    for i in range(n):
        label, weight = input().strip().split()
        goodies.append((label, int(weight), i+1))
    k = int(input())

    labels = sorted(set(label for label, _, _ in goodies))
    num_labels = len(labels)
    arrangements = []
    min_cost = float('inf')

    for perm in permutations(labels):
        label_to_pos = {label: i+1 for i, label in enumerate(perm)}
        total_cost = sum(weight * abs(pos - label_to_pos[label]) for label, weight, pos in goodies)
        if total_cost < min_cost:
            min_cost = total_cost
            arrangements = [perm]
        elif total_cost == min_cost:
            arrangements.append(perm)

    arrangements.sort()
    if 1 <= k <= len(arrangements):
        print(min_cost)
        print(" ".join(arrangements[k-1]))
    else:
        print(min_cost)
        print()  # Blank or error as preferred

if __name__ == "__main__":
    main()
