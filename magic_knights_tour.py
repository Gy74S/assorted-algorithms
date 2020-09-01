# Program to find magic square knights tour
# Doesn't consider diagonals, because I'm not sure if they exist for 8 x 8
# In fact it doesn't even work (idk how long it'll take to find a solution)
# Uses Warnsdorff's algo, but augmented to suit magic square conditions
# It also alternates/ backtracks bewteen quads using a stack every 4 moves

# If the square contains a Y, the algorithm works, an X, it does not work

# Y Y Y Y Y Y Y Y
# Y Y Y Y Y Y Y Y
# Y Y Y N N Y Y Y
# Y Y N Y Y N Y Y
# Y Y N Y Y N Y Y
# Y Y Y N N Y Y Y
# Y Y Y Y Y Y Y Y
# Y Y Y Y Y Y Y Y

dx = [2, 1, -1, -2, -2, -1, 1, 2]
dy = [1, 2, 2, 1, -1, -2, -2, -1]


# Driver code
def main():
	source = input("Starting position: ")
	src = [int(ord(source[0].lower()) - int(ord('a'))), int(source[1]) - 1]
	b = [[0 for j in range(8)] for i in range(8)]
	b[src[0]][src[1]] = 1
	printBoard(b)
	if solve(b, src, 1, [quadHash(src[0], src[1])], False):
		printBoard(b)
	else:
		print("Could not find solution")


# Backtracking solve
def solve(b, pos, t, qStack, backtrack):
	if t == 64:
		return True
	if backtrack and len(qStack) == 0: 
		backtrack = False
	if not backtrack and len(qStack) == 16: 
		backtrack = True
	quads = findQuad(qStack, backtrack)
	pq = heuristic(b, pos, t + 1, quads)
	for i in range(len(pq)):
		x = pos[1] + dx[pq[i]]
		y = pos[0] + dy[pq[i]]
		b[y][x] = t + 1
		newStack = qStack.copy()
		if not backtrack: 
			newStack.append(quadHash(y, x))
		if solve(b, [y, x], t + 1, newStack, backtrack):
			return True
		b[y][x] = 0
	return False


# Return priority queue of directions to go to
def heuristic(b, pos, t, quads):
	d = []
	for i in range(8):
		x = pos[1] + dx[i]
		y = pos[0] + dy[i]
		if isValid(b, y, x) and isMagic(b, y, x, t) and quadHash(y, x) in quads:
			degree = 0
			for j in range(8):
				nY = y + dy[j]
				nX = x + dx[j]
				if isValid(b, nY, nX) and isMagic(b, nY, nX, t + 1):
					degree += 1
			d.append([degree, i])
	d.sort(key = lambda i:i[0])
	return [d[i][1] for i in range(len(d))]


# Find which quad to prioritise
def findQuad(qStack, backtrack):
	if backtrack:
		return [qStack.pop()]
	if len(list(set(qStack))) == 0:
		return [0, 1, 2, 3]
	if qStack.count(qStack[-1]) < 4:
		return [qStack[-1]]
	return [i for i in range(4) if i not in qStack]


# Print out the chess board
def printBoard(b):
    for i in range(8):
        for j in range(8):
            print("%2d " % b[i][j], end="")
        print()
    print()


# Check which quad the square is in (currently only works for 8 x 8)
def quadHash(y, x):
	return 2 * (y > 3) + (x > 3)


# Check if the new move satisfies magic condition
def isMagic(b, y, x, t):
	tmpBoard = [row[:] for row in b]
	tmpBoard[y][x] = t
	halfRow = tmpBoard[y][4 * (x > 3) : 4 * (1 + (x > 3))]
	for i in halfRow:
		if i > 0 and i != t and (i - 1) // 4 == (t - 1) // 4:
			return False
	halfCol = [tmpBoard[i][x] for i in range(4 * (y > 3), 4 * (1 + (y > 3)))]
	for i in halfCol:
		if i > 0 and i != t and (i - 1) // 4 == (t - 1) // 4:
			return False
	r = tmpBoard[y]
	c = [tmpBoard[i][x] for i in range(8)]
	if (min(r) > 0 and sum(r) != 260) or (min(c) > 0 and sum(c) != 260):
		return False
	return True


# Check if square is valid
def isValid(b, y, x):
	return x >= 0 and x < 8 and y >= 0 and y < 8 and b[y][x] == 0


if __name__ == "__main__":
	main()