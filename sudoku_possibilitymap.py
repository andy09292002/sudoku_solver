# Sudoku puzzle (0 means empty)
board = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
]

# Function to print the board
def print_board(board):
    for row in board:
        print(" ".join(str(x) for x in row))

# Initialize the possibility map: True means the number is possible
def init_possibilities(board):
    poss = [[[True] * 9 for _ in range(9)] for _ in range(9)]  # 9x9x9 cube
    for i in range(9):
        for j in range(9):
            if board[i][j] != 0:
                num = board[i][j] - 1  # Convert to 0-based index
                # Set only this number as possible
                for k in range(9):
                    poss[i][j][k] = (k == num)
                # Remove this number from row, column, and 3x3 box
                update_possibilities(poss, i, j, num, False)
    return poss

# Update possibilities after placing a number
def update_possibilities(poss, row, col, num, value):
    # Update row
    for j in range(9):
        if j != col:
            poss[row][j][num] = value
    # Update column
    for i in range(9):
        if i != row:
            poss[i][col][num] = value
    # Update 3x3 box
    box_row, box_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(box_row, box_row + 3):
        for j in range(box_col, box_col + 3):
            if i != row or j != col:
                poss[i][j][num] = value

# Find cells with only one possible number
def find_single_possibilities(poss, board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                possible = [k + 1 for k in range(9) if poss[i][j][k]]
                if len(possible) == 1:
                    return i, j, possible[0]
    return None

# Find cell with fewest possibilities for guessing
def find_fewest_possibilities(poss, board):
    min_poss = 10
    best = None
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                possible = [k + 1 for k in range(9) if poss[i][j][k]]
                if 1 < len(possible) < min_poss:
                    min_poss = len(possible)
                    best = (i, j, possible)
    return best

# Check if puzzle is solved
def is_solved(board):
    return all(board[i][j] != 0 for i in range(9) for j in range(9))

# Check if puzzle is valid
def is_valid(poss):
    return all(
        any(poss[i][j][k] for k in range(9))
        for i in range(9) for j in range(9) if board[i][j] == 0
    )

# Main solving function
def solve(board, poss):
    while not is_solved(board):
        # Step 1: Fill cells with single possibilities
        single = find_single_possibilities(poss, board)
        if single:
            i, j, num = single
            board[i][j] = num
            update_possibilities(poss, i, j, num - 1, False)
            continue
        # Step 2: If no single possibilities, guess and backtrack
        if not is_valid(poss):
            return False
        guess = find_fewest_possibilities(poss, board)
        if not guess:
            return False
        i, j, possible = guess
        # Save state for backtracking
        board_copy = [row[:] for row in board]
        poss_copy = [[[p for p in row] for row in grid] for grid in poss]
        for num in possible:
            board[i][j] = num
            update_possibilities(poss, i, j, num - 1, False)
            if solve(board, poss):
                return True
            # Restore state and try next number
            board[:] = [row[:] for row in board_copy]
            poss[:] = [[[p for p in row] for row in grid] for grid in poss_copy]
        return False
    return True

# Run the solver
print("Original puzzle:")
print_board(board)
poss = init_possibilities(board)
if solve(board, poss):
    print("\nSolved puzzle:")
    print_board(board)
else:
    print("No solution found.")