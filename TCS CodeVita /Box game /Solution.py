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

def rotate_matrix(mat, direction):
    N = len(mat)
    new_mat = [[None]*N for _ in range(N)]
    if direction == 'left':
        for i in range(N):
            for j in range(N):
                new_mat[N-j-1][i] = mat[i][j]
    elif direction == 'right':
        for i in range(N):
            for j in range(N):
                new_mat[j][N-i-1] = mat[i][j]
    return new_mat

def deep_copy_cube(cube):
    return {face: [row[:] for row in cube[face]] for face in cube}

def apply_instruction(cube, instr, N):
    cube = deep_copy_cube(cube)
    parts = instr.split()
    if parts[0] == 'turn':
        if parts[1] == 'left':
            cube['front'], cube['left'], cube['back'], cube['right'] = cube['right'], cube['front'], cube['left'], cube['back']
            cube['top'] = rotate_matrix(cube['top'], 'right')
            cube['base'] = rotate_matrix(cube['base'], 'left')
        elif parts[1] == 'right':
            cube['front'], cube['right'], cube['back'], cube['left'] = cube['left'], cube['front'], cube['right'], cube['back']
            cube['top'] = rotate_matrix(cube['top'], 'left')
            cube['base'] = rotate_matrix(cube['base'], 'right')
    elif parts[0] == 'rotate':
        side = parts[1]
        if side == 'front':
            cube['front'], cube['base'], cube['back'], cube['top'] = cube['top'], cube['front'], cube['base'], cube['back']
            cube['left'] = rotate_matrix(cube['left'], 'right')
            cube['right'] = rotate_matrix(cube['right'], 'left')
        elif side == 'back':
            cube['front'], cube['top'], cube['back'], cube['base'] = cube['base'], cube['front'], cube['top'], cube['back']
            cube['left'] = rotate_matrix(cube['left'], 'left')
            cube['right'] = rotate_matrix(cube['right'], 'right')
        elif side == 'left':
            cube['top'], cube['left'], cube['base'], cube['right'] = cube['right'], cube['top'], cube['left'], cube['base']
            cube['front'] = rotate_matrix(cube['front'], 'left')
            cube['back'] = rotate_matrix(cube['back'], 'right')
        elif side == 'right':
            cube['top'], cube['right'], cube['base'], cube['left'] = cube['left'], cube['top'], cube['right'], cube['base']
            cube['front'] = rotate_matrix(cube['front'], 'right')
            cube['back'] = rotate_matrix(cube['back'], 'left')
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
            col = [face[i][idx] for i in range(N)]
            if direction == 'up':
                col = col[1:] + col[:1]
            else:
                col = col[-1:] + col[:-1]
            for i in range(N):
                face[i][idx] = col[i]
        cube[side] = face
    return cube

def solve():
    N, K, cube, instructions = read_input()
    for i in range(K):
        temp_cube = deep_copy_cube(cube)
        for j in range(K):
            if i == j:
                continue
            temp_cube = apply_instruction(temp_cube, instructions[j], N)
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
                        temp_cube = deep_copy_cube(cube)
                        for j2 in range(K):
                            if i2 == j2:
                                continue
                            temp_cube = apply_instruction(temp_cube, instructions[j2], N)
                        for face in temp_cube.values():
                            if is_solved(face):
                                print("Faulty")
                                print(instructions[i2])
                                return
                    cube[f1][i][j] = original
    print("Not Possible")

if __name__ == "__main__":
    solve()
