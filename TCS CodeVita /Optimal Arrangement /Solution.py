from collections import defaultdict
import itertools

class Goodie:
    def __init__(self, label, weight, position):
        self.label = label
        self.weight = weight
        self.position = position  # land position (1,2,...)

class CargoShip:
    def __init__(self, label):
        self.label = label
        self.position = None  # assigned later

class Optimizer:
    def __init__(self, goodies, K):
        self.goodies = goodies
        self.K = K
        self.labels = sorted(set(g.label for g in goodies))
        self.num_ships = len(self.labels)

    def build_cost_matrix(self):
        """
        Build cost matrix where cost[i][j] = total cost of assigning
        ship i (label) to sea position j (1-based).
        """
        label_to_goodies = defaultdict(list)
        for g in self.goodies:
            label_to_goodies[g.label].append(g)

        cost_matrix = []
        for label in self.labels:
            row = []
            for pos in range(1, self.num_ships + 1):
                cost = 0
                for g in label_to_goodies[label]:
                    distance = abs(g.position - pos)
                    cost += g.weight * distance
                row.append(cost)
            cost_matrix.append(row)
        return cost_matrix

    def hungarian(self, cost_matrix):
        """
        Pure Python Hungarian Algorithm implementation.
        Returns minimal cost and assignment.
        """
        n = len(cost_matrix)
        m = len(cost_matrix[0])
        u = [0] * (n+1)
        v = [0] * (m+1)
        p = [0] * (m+1)
        way = [0] * (m+1)

        for i in range(1, n+1):
            p[0] = i
            j0 = 0
            minv = [float('inf')] * (m+1)
            used = [False] * (m+1)
            while True:
                used[j0] = True
                i0 = p[j0]
                delta = float('inf')
                j1 = 0
                for j in range(1, m+1):
                    if not used[j]:
                        cur = cost_matrix[i0-1][j-1] - u[i0] - v[j]
                        if cur < minv[j]:
                            minv[j] = cur
                            way[j] = j0
                        if minv[j] < delta:
                            delta = minv[j]
                            j1 = j
                for j in range(m+1):
                    if used[j]:
                        u[p[j]] += delta
                        v[j] -= delta
                    else:
                        minv[j] -= delta
                j0 = j1
                if p[j0] == 0:
                    break
            while True:
                j1 = way[j0]
                p[j0] = p[j1]
                j0 = j1
                if j0 == 0:
                    break

        assignment = {}
        for j in range(1, m+1):
            if p[j] != 0:
                assignment[self.labels[p[j]-1]] = j
        min_cost = -v[0]
        return min_cost, assignment

    def find_arrangements(self):
        cost_matrix = self.build_cost_matrix()
        min_cost, assignment = self.hungarian(cost_matrix)

        # Generate all permutations that achieve min_cost
        valid_arrangements = []
        for perm in itertools.permutations(self.labels):
            total = 0
            for g in self.goodies:
                ship_pos = perm.index(g.label) + 1
                total += g.weight * abs(g.position - ship_pos)
            if total == min_cost:
                valid_arrangements.append(perm)

        valid_arrangements = sorted(set(valid_arrangements))
        return min_cost, valid_arrangements

    def solve(self):
        min_cost, arrangements = self.find_arrangements()
        kth_arrangement = arrangements[self.K - 1]
        return min_cost, kth_arrangement


def main():
    N = int(input().strip())
    goodies = []
    for i in range(N):
        label, weight = input().split()
        goodies.append(Goodie(label, int(weight), i+1))
    K = int(input().strip())

    optimizer = Optimizer(goodies, K)
    min_cost, arrangement = optimizer.solve()
    print(min_cost)
    print(" ".join(arrangement))


if __name__ == "__main__":
    main()
