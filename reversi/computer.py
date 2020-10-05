import math
import copy
from reversi import checked
import numpy as np

# Global variables because I'm lazy
transposition_table = {}
weights = [
	[ 512,-256, 256, -16, -16, 256,-256, 512],
	[-256,-256, -32, -32, -32, -32,-256,-256],
	[ 256, -32, 256,  16,  16, 256, -32, 256],
	[ -16, -32,  16,  16,  16,  16, -32, -16],
	[ -16, -32,  16,  16,  16,  16, -32, -16],
	[ 256, -32, 256,  16,  16, 256, -32, 256],
	[-256,-256, -32, -32, -32, -32,-256,-256],
	[ 512,-256, 256, -16, -16, 256,-256, 512]
]


# Actual AI algorithm (Computer Sciency stuff)
################################################################################
# Main code
def minimax(g, priority, alpha, beta, depth):

	if g.over() or depth == 0:
		return find_score(g, priority)

	valid_moves = heuristic_sort(g, g.find_valid(g.p))
	best_y, best_x = valid_moves[0]
	best_eval = -math.inf if g.p == priority else math.inf

	for y, x in valid_moves:
		new = copy.deepcopy(g)
		new.go(y, x)
		new_eval = minimax(new, priority, alpha, beta, depth - 1)
		new_eval = new_eval[0]
		if g.p == priority:
			if new_eval > best_eval:
				best_eval = new_eval
				best_y = y
				best_x = x
			alpha = max(alpha, best_eval)
		else:
			if new_eval < best_eval:
				best_eval = new_eval
				best_y = y
				best_x = x
			beta = min(beta, best_eval)
		if beta <= alpha:
			break
	return best_eval, best_y, best_x


# Sort moves according to which one seems better
def heuristic_sort(g, valid_moves):
	sorted_moves = []
	for move in valid_moves:
		y, x = move
		new = copy.deepcopy(g)
		new.go(y, x)
		rating = heuristic_score(new, g.p)
		sorted_moves.append({"move": move, "rating": rating})
	sorted_moves.sort(key = lambda x:x["rating"], reverse = True)
	return [move["move"] for move in sorted_moves]


# Finds the score of the baord
def find_score(g, priority):
	key = zobrist_key(g)
	if key[0] in transposition_table:
		if key[1] in transposition_table[key[0]]:
			score = transposition_table[key[0]][key[1]]
		else:
			score = heuristic_score(g, priority)
			transposition_table[key[0]][key[1]] = score
	else:
		score = heuristic_score(g, priority)
		transposition_table[key[0]] = {}
		transposition_table[key[0]][key[1]] = score
	return (score, -1, -1)


# Generates a zobrist key for the board
def zobrist_key(g):
	shift = 1
	key0 = 0
	key1 = 0
	for y in range(8):
		for x in range(8):
			if g.b[y][x] == 0:
				key0 += shift
			elif g.b[y][x] == 1:
				key1 += shift
			shift *= 2
	return (key0, key1)


# AI Heuristic (Mathyish stuff)
################################################################################
# Score the game using the heuristic
def heuristic_score(g, player):
	rating = 0
	oth_player = (player + 1) % 2

	mobility = mobility_score(g, player, oth_player)
	corner = corner_score(g, player, oth_player)
	frontier = frontier_score(g, player, oth_player)
	weight = weight_score(g, player, oth_player)
	stability = stability_score(g, player, oth_player)

	rating += corner * 6
	rating += (1 - g.turn / 60) * (frontier +  mobility + weight)
	rating += (1 + (3 * g.turn) / 60) * stability

	return rating


# Determine if the current player has better mobility
def mobility_score(g, player, oth_player):
	my_mobility = len(g.find_valid(player))
	oth_mobility = len(g.find_valid(oth_player))
	total_mobility = my_mobility + oth_mobility
	return (my_mobility - oth_mobility) / max(total_mobility, 1)


# Find how many corner a player owns
def corner_score(g, player, oth_player):
	corners = [0, 0]
	if g.b[0][0] != g.blank:
		corners[g.b[0][0]] += 1
	if g.b[7][0] != g.blank:
		corners[g.b[7][0]] += 1
	if g.b[0][7] != g.blank:
		corners[g.b[0][7]] += 1
	if g.b[7][7] != g.blank:
		corners[g.b[7][7]] += 1
	return (corners[player] - corners[oth_player]) / max(sum(corners), 1)


# Check number of the squares on the player's frontier
def frontier_score(g, player, oth_player):
	visited = [[[False for k in range(8)] for j in range(8)] for i in range(2)]
	frontier = [0, 0]
	for y in range(8):
		for x in range(8):
			if g.b[y][x] != g.blank:
				curr_player = g.b[y][x]
				for i in range(8):
					nY = y + g.dy[i]
					nX = x + g.dx[i]
					if (g.in_lim(nY, nX) and g.b[nY][nX] != curr_player
						and visited[curr_player][nY][nX] == False):
						visited[curr_player][nY][nX] = True
						frontier[curr_player] += 1
	return (frontier[player] - frontier[oth_player]) / max(sum(frontier), 1)


# Calculate the value of the board based on predetermined weights
def weight_score(g, player, oth_player):
	weights = [0, 0]
	for y in range(8):
		for x in range(8):
			if g.b[y][x] != g.blank:
				weights[g.b[y][x]] += square_weight(g, y, x)
	sum_weights = 1 if sum(weights) == 0 else sum(weights)
	return (weights[player] - weights[oth_player]) / sum_weights


# Calculate how hard it is for a player to change the configuration of the board
def stability_score(g, player, oth_player):
	stabils = [0, 0]
	for y in range(8):
		for x in range(8):
			if g.b[y][x] != g.blank:
				stabils[g.b[y][x]] += square_stabil(g, y, x)
	return (stabils[player] - stabils[oth_player]) / max(sum(stabils), 1)


# Find the stability of a square
def square_stabil(g, y, x):
	opposition = (g.b[y][x] + 1) % 2

	stability = 64
	oppositions = [False for _ in range(8)]
	blanks = [0 for _ in range(8)]
	for direction in range(8):
		for distance in range(1, 8):
			nY = y + g.dy[direction] * distance
			nX = x + g.dx[direction] * distance
			if g.in_lim(nY, nX):
				if g.b[nY][nX] == g.blank:
					blanks[direction] += 1
				if blanks[direction] == 0 and g.b[y][x] == opposition:
					oppositions[direction] == True
	
	# Double stability if square cannot be immediately flipped in a direction
	for direction in range(8):
		if oppositions[(direction + 4) % 8] and blanks[direction] > 0:
			stability //= 2
		else:
			stability *= 2
	
	# Consider future stability of square
	for direction in range(4):

		min_blank = min(blanks[direction], blanks[direction + 4])
		if min_blank % 2 == 0:
			stability *= 2
		else:
			stability //= 2
		stability //= 2 ** min_blank
	return stability


# Find the weight/ value of a square
def square_weight(g, y, x):
	# IMPLEMENT DYNAMIC SQUARE WEIGHTS
	weight = weights[y][x]
	# Scuffed method for testing
	if (((y == 1 and (x == 0 or x == 1)) or (y == 0 and x == 1) and (g.b[0][0] != g.blank))
		or ((y == 1 and (x == 6 or x == 7)) or (y == 0 and x == 7) and (g.b[0][7] != g.blank))
		or ((y == 6 and (x == 0 or x == 1)) or (y == 7 and x == 1) and (g.b[7][0] != g.blank))
		or ((y == 6 and (x == 6 or x == 7)) or (y == 7 and x == 6) and (g.b[7][7] != g.blank))):
		weight = 48
	return weight
