# This is the puzzle grid. 0 means empty. You can change this to any Sudoku puzzle.
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

# Function to print the board nicely
def print_board(board):
    for row in board:
        print(" ".join(map(str, row)))

# Function to find the next empty spot (0)
def find_empty(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return (i, j)  # row, column
    return None  # No empty spots left

# Function to check if a number is okay to place here
def valid(board, num, pos):
    # Check the row
    for i in range(9):
        if board[pos[0]][i] == num and pos[1] != i:
            return False
    # Check the column
    for i in range(9):
        if board[i][pos[1]] == num and pos[0] != i:
            return False
    # Check the 3x3 box
    box_x = pos[1] // 3
    box_y = pos[0] // 3
    for i in range(box_y * 3, box_y * 3 + 3):
        for j in range(box_x * 3, box_x * 3 + 3):
            if board[i][j] == num and (i, j) != pos:
                return False
    return True

# The main solving function using backtracking
def solve(board):
    empty = find_empty(board)
    if not empty:
        return True  # Puzzle is solved!
    row, col = empty
    for num in range(1, 10):  # Try numbers 1 to 9
        if valid(board, num, (row, col)):
            board[row][col] = num  # Place the number
            if solve(board):  # Try to solve the rest
                return True
            board[row][col] = 0  # Backtrack: erase and try next
    return False  # No solution from here

# Show the puzzle before solving
print("Original puzzle:")
print_board(board)

# Solve it
if solve(board):
    print("\nSolved puzzle:")
    print_board(board)
else:
    print("No solution found.")