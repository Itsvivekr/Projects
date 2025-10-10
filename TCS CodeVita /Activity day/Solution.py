def get_ascii_value(s):
    return sum(ord(c) for c in s)

def parse_input():
    n, m = map(int, input().split())
    l = int(input())
    partitions = []
    for _ in range(l):
        partitions.append(tuple(map(int, input().split())))
    r = int(input())
    strings = input().split()
    return n, m, partitions, r, strings

def build_boxes(n, m, partitions):
    grid = [[0 for _ in range(m)] for _ in range(n)]
    visited = [[False for _ in range(m)] for _ in range(n)]
    box_id = 1

    vertical_lines = set()
    horizontal_lines = set()
    for x1, y1, x2, y2 in partitions:
        if x1 == x2:
            for y in range(min(y1, y2), max(y1, y2)):
                vertical_lines.add((x1, y))
        elif y1 == y2:
            for x in range(min(x1, x2), max(x1, x2)):
                horizontal_lines.add((x, y1))

    def is_valid(x, y):
        return 0 <= x < n and 0 <= y < m

    def dfs(x, y, box_id):
        stack = [(x, y)]
        cells = []
        min_x, min_y = x, y
        while stack:
            cx, cy = stack.pop()
            if visited[cx][cy]:
                continue
            visited[cx][cy] = True
            grid[cx][cy] = box_id
            cells.append((cx, cy))
            min_x = min(min_x, cx)
            min_y = min(min_y, cy)
            for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
                nx, ny = cx + dx, cy + dy
                if is_valid(nx, ny) and not visited[nx][ny]:
                    if dx == 1 and (cx+1, cy) in vertical_lines:
                        continue
                    if dx == -1 and (cx, cy) in vertical_lines:
                        continue
                    if dy == 1 and (cx, cy+1) in horizontal_lines:
                        continue
                    if dy == -1 and (cx, cy) in horizontal_lines:
                        continue
                    stack.append((nx, ny))
        return cells, (min_x, min_y)

    boxes = []
    for i in range(n):
        for j in range(m):
            if not visited[i][j]:
                cells, bottom_left = dfs(i, j, box_id)
                area = len(cells)
                boxes.append({
                    'id': box_id,
                    'area': area,
                    'bottom_left': bottom_left,
                    'cells': cells
                })
                box_id += 1
    return boxes

def assign_strings(boxes, strings):
    boxes.sort(key=lambda b: (b['bottom_left'][1], b['bottom_left'][0]))
    for i in range(len(boxes)):
        boxes[i]['string'] = strings[i]
    return boxes

def rank_boxes(boxes):
    boxes.sort(key=lambda b: (-b['area'], b['bottom_left'][0], b['bottom_left'][1]))
    return boxes

# Main
n, m, partitions, r, strings = parse_input()
boxes = build_boxes(n, m, partitions)
boxes = assign_strings(boxes, strings)
ranked = rank_boxes(boxes)
print(get_ascii_value(ranked[r - 1]['string']))
