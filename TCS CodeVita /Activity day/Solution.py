def ascii_value(s):
    return sum(ord(c) for c in s)

def solve():
    import sys
    input = sys.stdin.readline

    # Read grid dimensions N (width) x M (height)
    N, M = map(int, input().split())
    L = int(input())  # Number of partition lines

    # Collect vertical and horizontal partition lines (including grid boundary)
    vertical_lines = {0, N}
    horizontal_lines = {0, M}

    for _ in range(L):
        x1, y1, x2, y2 = map(int, input().split())
        if x1 == x2:
            # Vertical line
            vertical_lines.add(x1)
        elif y1 == y2:
            # Horizontal line
            horizontal_lines.add(y1)

    # Sorted coordinate lists
    vertical_lines = sorted(vertical_lines)
    horizontal_lines = sorted(horizontal_lines)

    # Generate all boxes formed by consecutive vertical and horizontal lines
    # Each box identified by bottom-left corner and area
    boxes = []
    for i in range(len(vertical_lines) - 1):
        for j in range(len(horizontal_lines) - 1):
            x1, x2 = vertical_lines[i], vertical_lines[i+1]
            y1, y2 = horizontal_lines[j], horizontal_lines[j+1]
            area = (x2 - x1) * (y2 - y1)
            boxes.append((area, x1, y1, i, j))

    # Read Raghu's rank R
    R = int(input())

    # Read strings for boxes in left-to-right, bottom-to-top order
    strings = input().split()

    # Sort boxes by left-to-right (i), bottom-to-top (j) order for string assignment
    boxes.sort(key=lambda b: (b[3], b[4]))  # sort by vertical then horizontal index
    box_to_string = {box: strings[idx] for idx, box in enumerate(boxes)}

    # Rank boxes by area descending, then by x ascending, then by y ascending
    ranked = sorted(boxes, key=lambda b: (-b[0], b[1], b[2]))

    # Select the box that matches the assigned rank R
    target_box = ranked[R-1]

    # Find the string corresponding to the target box
    selected_string = box_to_string[target_box]

    # Calculate sum of ASCII values of characters in the string
    result = ascii_value(selected_string)

    print(result)

if __name__ == "__main__":
    solve()
