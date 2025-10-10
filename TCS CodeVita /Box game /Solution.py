import sys
import copy

def read_input():
    N, K = map(int, sys.stdin.readline().split())
    cube = {}
    faces = ['base', 'back', 'top', 'front', 'left', 'right']
    for face in faces:
        cube[face] = [sys.stdin.readline().strip().split() for _ in range(N)]
    instructions = [sys.stdin.readline().strip() for _ in range(K)]
    return N, K, cube, instructions

def is_solved(face):
    color = face[0][0]
    return all(cell == color for row in face for cell in row)

def rotate_face(face, direction):
    N = len(face)
    new_face = [[None]*N for _ in range(N)]
    if direction == 'left':
        for i in range(N):
            for j in range(N):
                new_face[N-j-1][i] = face[i][j]
    elif direction == 'right':
        for i in range(N):
            for j in range(N):
                new_face[j][N-i-1] = face[i][j]
    return new_face

def apply_instruction(cube, instr):
    cube = copy.deepcopy(cube)
    parts = instr.split()
    if parts[0] == 'turn':
        if parts[1] == 'left':
            cube['front'], cube['left'], cube['back'], cube['right'] = cube['right'], cube['front'], cube['left'], cube['back']
            cube['top'] = rotate_face(cube['top'], 'right')
            cube['base'] = rotate_face(cube['base'], 'left')
        elif parts[1] == 'right':
            cube['front'], cube['right'], cube['back'], cube['left'] = cube['left'], cube['front'], cube['right'], cube['back']
            cube['top'] = rotate_face(cube['top'], 'left')
            cube['base'] = rotate_face(cube['base'], 'right')
    elif parts[0] == 'rotate':
        # Simplified: no-op for now
        pass
    else:
        side, idx, direction = parts
        idx = int(idx) - 1
        face = cube[side]
        if direction in ['left', 'right']:
            row = face[idx]
            if direction == 'left':
                row = row[1:] + row[:1]
            else:
                row = row[-1:] + row[:-1]
            face[idx] = row
        elif direction in ['up', 'down']:
            col = [face[i][idx] for i in range(len(face))]
            if direction == 'up':
                col = col[1:] + col[:1]
            else:
                col = col[-1:] + col[:-1]
            for i in range(len(face)):
                face[i][idx] = col[i]
        cube[side] = face
    return cube

def solve():
    N, K, cube, instructions = read_input()
    for i in range(K):
        temp_cube = copy.deepcopy(cube)
        for j in range(K):
            if i == j:
                continue
            temp_cube = apply_instruction(temp_cube, instructions[j])
        for face in temp_cube.values():
            if is_solved(face):
                print(instructions[i])
                return
    # Try fault correction
    colors = [cell for face in cube.values() for row in face for cell in row]
    for f1 in cube:
        for i in range(N):
            for j in range(N):
                original = cube[f1][i][j]
                for c in set(colors):
                    if c == original:
                        continue
                    cube[f1][i][j] = c
                    for i2 in range(K):
                        temp_cube = copy.deepcopy(cube)
                        for j2 in range(K):
                            if i2 == j2:
                                continue
                            temp_cube = apply_instruction(temp_cube, instructions[j2])
                        for face in temp_cube.values():
                            if is_solved(face):
                                print("Faulty")
                                print(instructions[i2])
                                return
                    cube[f1][i][j] = original
    print("Not Possible")

if __name__ == "__main__":
    solve()
