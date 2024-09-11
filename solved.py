import queue
from maze_creator import main_maze

def path(maze):
    def valid(maze, moves):
        for x, pos in enumerate(maze[0]):
            if pos == "O":
                start = x

        i = start
        j = 0
        for move in moves:
            if move == "L":
                i -= 1
            elif move == "R":
                i += 1
            elif move == "U":
                j -= 1
            elif move == "D":
                j += 1

            if not(0 <= i < len(maze[0]) and 0 <= j < len(maze)):
                return False
            elif (maze[j][i] == "#"):
                return False
        return True

    def findEnd(maze, moves):
        for x, pos in enumerate(maze[0]):
            if pos == "O":
                start = x

        i = start
        j = 0
        for move in moves:
            if move == "L":
                i -= 1

            elif move == "R":
                i += 1

            elif move == "U":
                j -= 1

            elif move == "D":
                j += 1

        if maze[j][i] == "X":
            return True
        return False

    nums = queue.Queue()
    nums.put("")
    add = ""

    # change our languge of code to make this code, work!
    # change 'w' -> "#" and 'c' -> ''

    for i in range(1, len(maze)-1):
        for j in range(0, len(maze[0])):
            if maze[i][j] == 'w':
                maze[i][j] = '#'
            else:
                maze[i][j] = " "

    #find the start position
    for i in range(0, len(maze[0])):
        if maze[0][i] == 'c':
            maze[0][i] = 'O'
        else:
            maze[0][i] = '#'

    #find the exit block
    for i in range(0, len(maze[0])):
        if maze[-1][i] == 'c':
            maze[-1][i] = 'X'
        else:
            maze[-1][i] = '#'

    while not findEnd(maze, add): 
        add = nums.get()
        for j in ["L", "R", "U", "D"]:
            put = add + j
            if valid(maze, put):
                if len(put) < 3:
                    nums.put(put)
                else:
                    if put[-1] == "L" and put[-2] !="R" or put[-1] == "R" and put[-2] != "L" or put[-1] == "U" and put[-2] != "D" or put[-1] == "D" and put[-2] !="U":
                        nums.put(put)
    return add

