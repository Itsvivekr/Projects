from collections import Counter, deque
import sys

class WoodenPiece:
    def __init__(self, text, cost):
        self.text = text
        self.cost = cost
        self.counter = Counter(text)

class StrangeStringSolver:
    def __init__(self, target, pieces, costs):
        self.target = target
        self.pieces = [WoodenPiece(pieces[i], costs[i]) for i in range(len(pieces))]

    def min_cost_with_rearrangement(self):
        # DP[i] = min cost to form first i characters of target
        dp = [float('inf')] * (len(self.target) + 1)
        dp[0] = 0

        for i in range(len(self.target) + 1):
            for piece in self.pieces:
                need = Counter(self.target[i:])
                can_use = piece.counter & need
                if not can_use:
                    continue
                used = sum(can_use.values())
                if i + used <= len(self.target):
                    dp[i + used] = min(dp[i + used], dp[i] + piece.cost)
        return dp[len(self.target)]

    def min_cost_without_rearrangement(self):
        dp = [float('inf')] * (len(self.target) + 1)
        dp[0] = 0

        for i in range(len(self.target) + 1):
            for piece in self.pieces:
                j = i
                k = 0
                while j < len(self.target) and k < len(piece.text):
                    if self.target[j] == piece.text[k]:
                        j += 1
                    k += 1
                if j > i:
                    dp[j] = min(dp[j], dp[i] + piece.cost)
        return dp[len(self.target)]

def main():
    input_lines = [line.strip() for line in sys.stdin if line.strip()]
    target = input_lines[0]
    n = int(input_lines[1])
    pieces = input_lines[2].split()
    costs = list(map(int, input_lines[3].split()))

    solver = StrangeStringSolver(target, pieces, costs)
    cost_rearranged = solver.min_cost_with_rearrangement()
    cost_ordered = solver.min_cost_without_rearrangement()
    print(cost_ordered - cost_rearranged)

if __name__ == "__main__":
    main()
