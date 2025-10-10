from collections import defaultdict

def min_cost_with_rearrangement(target, pieces, costs):
    target_freq = defaultdict(int)
    for ch in target:
        target_freq[ch] += 1

    piece_freqs = []
    for piece in pieces:
        freq = defaultdict(int)
        for ch in piece:
            freq[ch] += 1
        piece_freqs.append(freq)

    remaining = target_freq.copy()
    total_cost = 0

    while any(remaining.values()):
        best_piece = -1
        best_gain = 0
        for i, freq in enumerate(piece_freqs):
            gain = sum(min(freq[ch], remaining[ch]) for ch in remaining)
            if gain > best_gain:
                best_gain = gain
                best_piece = i
        if best_piece == -1:
            return float('inf')  # Cannot form target
        total_cost += costs[best_piece]
        for ch in piece_freqs[best_piece]:
            remaining[ch] = max(0, remaining[ch] - piece_freqs[best_piece][ch])
    return total_cost

def min_cost_without_rearrangement(target, pieces, costs):
    n = len(target)
    dp = [float('inf')] * (n + 1)
    dp[0] = 0

    for i in range(n + 1):
        if dp[i] == float('inf'):
            continue
        for j, piece in enumerate(pieces):
            k = i
            for ch in piece:
                if k < n and target[k] == ch:
                    k += 1
            if k > i:
                dp[k] = min(dp[k], dp[i] + costs[j])
    return dp[n] if dp[n] != float('inf') else -1

# 🔹 Main Program
def main():
    target = input().strip()
    n = int(input())
    pieces = input().strip().split()
    costs = list(map(int, input().strip().split()))

    cost_rearranged = min_cost_with_rearrangement(target, pieces, costs)
    cost_ordered = min_cost_without_rearrangement(target, pieces, costs)

    print(cost_ordered - cost_rearranged)

# Run the program
if __name__ == "__main__":
    main()
