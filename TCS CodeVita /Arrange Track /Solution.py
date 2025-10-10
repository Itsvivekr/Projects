from collections import deque
from copy import deepcopy

class Sheet:
    def __init__(self, grid, size):
        self.grid = grid  # 2D list of chars
        self.size = size
        self.rotation = 0  # 0, 90, 180, 270 degrees
    
    def rotate(self):
        # Rotate the sheet 90 degrees clockwise
        new_grid = [['']*self.size for _ in range(self.size)]
        for r in range(self.size):
            for c in range(self.size):
                new_grid[c][self.size-1-r] = self.grid[r][c]
        self.grid = new_grid
        self.rotation = (self.rotation + 90) % 360
        
    def get_cell(self, r, c):
        return self.grid[r][c]
    
    def __repr__(self):
        return "
".join("".join(row) for row in self.grid)

class Plan:
    def __init__(self, full_grid, N, M):
        self.full_grid = full_grid
        self.N = N
        self.M = M
        self.num_sheets = N // M
        self.sheets = []
        self.sheet_positions = [[None]*self.num_sheets for _ in range(self.num_sheets)]
        self.source_sheet_coords = None
        self.dest_sheet_coords = None
        self.source_global = None
        self.dest_global = None
        self.extract_sheets()
        
    def extract_sheets(self):
        # Extract sheets from the full grid
        for i in range(self.num_sheets):
            for j in range(self.num_sheets):
                grid = [self.full_grid[i*self.M + r][j*self.M: j*self.M + self.M] for r in range(self.M)]
                sheet = Sheet(grid, self.M)
                self.sheets.append(sheet)
                self.sheet_positions[i][j] = sheet
                # Check if S or D in this sheet; record their global position
                for r in range(self.M):
                    for c in range(self.M):
                        if grid[r][c] == 'S':
                            self.source_sheet_coords = (i, j)
                            self.source_global = (i*self.M + r, j*self.M + c)
                        elif grid[r][c] == 'D':
                            self.dest_sheet_coords = (i, j)
                            self.dest_global = (i*self.M + r, j*self.M + c)
    
    def set_arrangement(self, arrangement):
        # arrangement is a 2D list of (sheet_index, rotation) tuples describing sheets placement and orientation
        for i in range(self.num_sheets):
            for j in range(self.num_sheets):
                index, rot = arrangement[i][j]
                self.sheet_positions[i][j] = self.sheets[index]
                # Reset sheet rotation
                self.sheets[index].rotation = 0
                self.sheets[index].grid = deepcopy(self.sheets[index].grid)
                # Rotate sheet to required rotation
                for _ in range(rot // 90):
                    self.sheets[index].rotate()
    
    def construct_full_plan(self):
        # Combine arranged sheets into full plan grid
        full_plan = []
        for s_row in range(self.num_sheets):
            for r in range(self.M):
                row = []
                for s_col in range(self.num_sheets):
                    row.extend(self.sheet_positions[s_row][s_col].grid[r])
                full_plan.append(row)
        return full_plan
    
    def find_shortest_path(self):
        # BFS from S to D on constructed full plan
        plan = self.construct_full_plan()
        rows, cols = self.N, self.N
        start = None
        end = None
        for r in range(rows):
            for c in range(cols):
                if plan[r][c] == 'S':
                    start = (r, c)
                elif plan[r][c] == 'D':
                    end = (r, c)
        if not start or not end:
            return -1
        
        queue = deque()
        queue.append((start[0], start[1], 1))  # (r, c, dist)
        visited = [[False]*cols for _ in range(rows)]
        visited[start[0]][start[1]] = True
        
        directions = [(1,0),(-1,0),(0,1),(0,-1)]
        valid_cells = {'S', 'D', 'T'}
        
        while queue:
            r, c, dist = queue.popleft()
            if (r, c) == end:
                return dist
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols:
                    if not visited[nr][nc] and plan[nr][nc] in valid_cells:
                        visited[nr][nc] = True
                        queue.append((nr, nc, dist + 1))
        return -1  # No path found
    
    def validate_adjacency(self, sheet1, sheet2, direction):
        # Check if track cells of adjacent edges of two sheets align after rotation
        # direction: 'right' or 'down' - sheet2 is to the right or down of sheet1
        M = self.M
        if direction == 'right':
            for i in range(M):
                cell1 = sheet1.get_cell(i, M-1)
                cell2 = sheet2.get_cell(i, 0)
                # Valid track alignment required:
                # Both must be track cells (T, S, D) or both land (L)
                if (cell1 in 'STD') != (cell2 in 'STD'):
                    return False
            return True
        elif direction == 'down':
            for j in range(M):
                cell1 = sheet1.get_cell(M-1, j)
                cell2 = sheet2.get_cell(0, j)
                if (cell1 in 'STD') != (cell2 in 'STD'):
                    return False
            return True
        return False
    
    def all_sheets_arranged_valid(self, arrangement):
        # Check if arrangement is valid according to adjacency and source/dest placement
        # Source sheet is fixed at top-left = self.source_sheet_coords
        # Destination sheet fixed at bottom-right = self.dest_sheet_coords
        
        # Check source and dest placement fixed
        if arrangement[0][0][0] != self.source_sheet_coords[0]*self.num_sheets + self.source_sheet_coords[1]:
            return False
        if arrangement[self.num_sheets-1][self.num_sheets-1][0] != self.dest_sheet_coords[0]*self.num_sheets + self.dest_sheet_coords[1]:
            return False
        
        # Setup sheet objects with required rotations
        for i in range(self.num_sheets):
            for j in range(self.num_sheets):
                idx, rot = arrangement[i][j]
                self.sheets[idx].grid = deepcopy(self.sheets[idx].grid)
                self.sheets[idx].rotation = 0
                for _ in range(rot // 90):
                    self.sheets[idx].rotate()
        
        # Validate adjacency (right and down neighbors)
        for i in range(self.num_sheets):
            for j in range(self.num_sheets):
                current_idx, _ = arrangement[i][j]
                current_sheet = self.sheets[current_idx]
                # Right neighbor
                if j + 1 < self.num_sheets:
                    right_idx, _ = arrangement[i][j+1]
                    right_sheet = self.sheets[right_idx]
                    if not self.validate_adjacency(current_sheet, right_sheet, 'right'):
                        return False
                # Down neighbor
                if i + 1 < self.num_sheets:
                    down_idx, _ = arrangement[i+1][j]
                    down_sheet = self.sheets[down_idx]
                    if not self.validate_adjacency(current_sheet, down_sheet, 'down'):
                        return False
        return True

def solve(arrangement_problem):
    N, M, grid = arrangement_problem
    plan = Plan(grid, N, M)
    
    from itertools import permutations, product
    
    n = plan.num_sheets
    sheets_indices = list(range(len(plan.sheets)))
    # Fix source and dest sheet indices for positions
    source_idx = plan.source_sheet_coords[0]*n + plan.source_sheet_coords[1]
    dest_idx = plan.dest_sheet_coords[0]*n + plan.dest_sheet_coords[1]
    
    # We want to arrange the sheets in num_sheets x num_sheets grid,
    # with source sheet fixed at (0,0), dest at (n-1, n-1).
    # Build list of remaining sheets indices to permute.
    remaining_indices = sheets_indices[:]
    remaining_indices.remove(source_idx)
    if dest_idx != source_idx:
        remaining_indices.remove(dest_idx)
    
    min_dist = float('inf')
    
    # For each permutation of remaining sheets
    for perm in permutations(remaining_indices):
        # Construct arrangement grid indices
        arrangement_indices = [source_idx] + list(perm[:n*n - 2]) + [dest_idx]
        arrangement_grid = []
        idx = 0
        for i in range(n):
            row = []
            for j in range(n):
                row.append(arrangement_indices[idx])
                idx += 1
            arrangement_grid.append(row)
        
        # For all rotations combinations per sheet
        rotations = [0, 90, 180, 270]
        for rotation_combo in product(rotations, repeat=n*n):
            arrangement = []
            k = 0
            for i in range(n):
                row = []
                for j in range(n):
                    row.append((arrangement_grid[i][j], rotation_combo[k]))
                    k += 1
                arrangement.append(row)
            
            if plan.all_sheets_arranged_valid(arrangement):
                plan.set_arrangement(arrangement)
                dist = plan.find_shortest_path()
                if dist != -1 and dist < min_dist:
                    min_dist = dist
    return min_dist if min_dist != float('inf') else -1

# Example usage
if __name__ == "__main__":
    N, M = map(int, input().split())
    grid = [list(input().strip()) for _ in range(N)]
    result = solve((N, M, grid))
    print(result)
