import pygame
import random
import copy

# GLOBALS VARS
s_width = 800
s_height = 700
play_width = 300  
play_height = 600 
block_size = 30

top_left_x = (s_width - play_width) // 2
top_left_y = s_height - play_height

m_play_width = 150  
m_play_height = 300 
m_block_size = 15

m_top_left_x = 50
m_top_left_y = 350


S = [['.....',
      '......',
      '..00..',
      '.00...',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

N = [['.....',
      '.....',
      '.....',
      '.....',
      '.....'],
     ['.....',
      '.....',
      '.....',
      '.....',
      '.....']]

shapes = [S, Z, I, O, J, L, T, N]
shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128), (0, 0, 0)]


class Piece(object):
	def __init__(self, x, y, shape):
		self.x = x
		self.y = y
		self.shape = shape
		self.color = shape_colors[shapes.index(shape)]
		self.rotation = 0


def create_grid(locked_pos={}):
	grid = [[(0, 0, 0) for x in range(10)] for x in range(20)]
	
	for i in range(len(grid)):
		for j in range(len(grid[i])):
			if (j, i) in locked_pos:
				c = locked_pos[(j, i)]
				grid[i][j] = c
	return grid




def convert_shape_format(shape):
	positions = []
	form = shape.shape[shape.rotation % len(shape.shape)]

	for i, line in enumerate(form):
		row = list(line)
		for j, column in enumerate(row):
			if column == '0':
				positions.append((shape.x + j, shape.y + i))
	for i, pos in enumerate(positions):
		positions[i] = (pos[0] - 2, pos[1] - 4)
	return positions


def valid_space(shape, grid):
	accepted_pos = [[(j, i) for j in range(10) if grid[i][j] == (0, 0, 0)] for i in range(20)]
	accepted_pos = [j for sub in accepted_pos for j in sub]
	formated = convert_shape_format(shape)

	for pos in formated:
		if pos not in accepted_pos:
			if pos[1] > -1:
				return False
	return True


def garbage_format(valuey):
	positions = []
	j = 0
	while j < 9:
		positions.append((j, valuey))
		j = j+1
	return positions


def	garbage(grid, locked, inc):
	i = 20 - inc
	for key in sorted(list(locked)):
		x, y = key
		newKey = (x, y - inc)
		locked[newKey] = locked.pop(key)
	while i < 20:
		garbo = garbage_format(i)
		for pos in garbo:
			p = (pos[0], pos[1])
			locked[p] = (115, 115, 115)
		i += 1

def check_lost(positions):
	for pos in positions:
		x, y = pos
		if y < 1:
			return True
	return False



def get_shape(bag):
	arr = [S, Z, I, O, J, L, T]
	var = random.choice(arr)
	i = 0
	while var in bag and i < 5:
		var = random.choice(arr)
		i += 1
	return Piece(5, 0, var)




def draw_text_middle(text, size, color, win):
	sx = top_left_x + play_width + 50
	sy = top_left_y + 50
	
	font = pygame.font.SysFont('Arial', size, bold=True)
	label = font.render(text, 1, color)
 
	win.blit(label, (top_left_x + play_width/2 - (label.get_width() / 2), top_left_y + play_height/2 - label.get_height()/2))


def draw_grid(surface, grid):
	sx = top_left_x
	sy = top_left_y

	for i in range(len(grid)):
		pygame.draw.line(surface, (128, 128, 128), (sx, sy + i * block_size), (sx + play_width, sy + i * block_size)) 
		for j in range(len(grid[i])):
			pygame.draw.line(surface, (128, 128, 128), (sx + j * block_size, sy), (sx + j * block_size, sy + play_height)) 


def	update_score(nscore):
	with open('scores', 'r') as f:
		lines = f.readline()
		score = lines[0].strip()

	with open('scores', 'w') as f:
		if (nscore > (int)(score)):
			f.write(str(nscore))
		else:
			f.write(str(score))
		
def clear_rows(grid, locked):
	inc = 0

	for i in range(len(grid) - 1, -1, -1):
		row = grid[i]
		if (0, 0, 0) not in row:
			inc += 1
			ind = i
			for j in range(len(row)):
				try:
					del locked[(j, i)]
				except:
					continue
	if inc > 0:
		for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
			x, y = key
			if y < ind:
				newKey = (x, y + inc)
				locked[newKey] = locked.pop(key)
	return inc



def draw_next_shape(shape, win, cleared_line, level):
	font = pygame.font.SysFont('Arial', 30)
	label = font.render('Next Shape', 1, (255, 255, 255))

	sx = top_left_x + play_width + 50
	sy = top_left_y + 50
	format = shape.shape[shape.rotation % len(shape.shape)]

	for i, line in enumerate(format):
		row = list(line)
		for j, column in enumerate(row):
			if column == '0':
				pygame.draw.rect(win, shape.color, (sx + j * block_size, sy + i * block_size, block_size, block_size), 0)

	pygame.draw.rect(win, (255, 0, 0), (sx + 10, sy, 120, 120), 2)
	win.blit(label, (sx + 10, sy - 30))
	font = pygame.font.SysFont('Arial', 30)

	label = font.render('Cleared :' + str(cleared_line), 1, (255, 255, 255))
	win.blit(label, (sx + 15, sy + 180))
	label = font.render('Level :' + str(level), 1, (255, 255, 255))
	win.blit(label, (sx + 15, sy + 200))

def draw_hold(win, shape):
	font = pygame.font.SysFont('Arial', 30)
	label = font.render('Hold', 1, (255, 255, 255))

	sx = 25
	sy = top_left_y + 50
	format = shape.shape[shape.rotation % len(shape.shape)]

	for i, line in enumerate(format):
		row = list(line)
		for j, column in enumerate(row):
			if column == '0':
				pygame.draw.rect(win, shape.color, (sx + j * block_size, sy + i * block_size, block_size, block_size), 0)

	pygame.draw.rect(win, (255, 0, 0), (sx + 10, sy, 120, 120), 2)
	win.blit(label, (sx + 10, sy - 30))


def draw_window(surface, grid, score=0, combo=1):
	surface.fill((0, 0, 0))

	pygame.font.init
	font = pygame.font.SysFont('Arial', 60)
	label = font.render('Tetris', 1 ,(255, 255, 255))
	
	surface.blit(label, (top_left_x + play_width / 2 - (label.get_width() / 2), 30))
	
	font = pygame.font.SysFont('Arial', 30)
	label = font.render('Score: ' + str(score), 1, (255, 255, 255))

	sx = top_left_x + play_width + 50
	sy = top_left_y + 50
	surface.blit(label, (sx + 15 , sy + 140))

	font = pygame.font.SysFont('Arial', 30)
	label = font.render('Combo: ' + str(combo), 1, (255, 255, 255))

	sx = top_left_x + play_width + 50
	sy = top_left_y + 50
	surface.blit(label, (sx + 15 , sy + 160))

	for i in range(len(grid)):
		for j in range(len(grid[i])):
			pygame.draw.rect(surface, grid[i][j], (top_left_x + j * block_size, top_left_y + i * block_size, block_size, block_size), 0)
	pygame.draw.rect(surface, (255, 0, 0), (top_left_x, top_left_y, play_width, play_height), 5)
	
	
	for i in range(len(grid)):
		for j in range(len(grid[i])):
			pygame.draw.rect(surface, grid[i][j], (m_top_left_x + j * m_block_size, m_top_left_y + i * m_block_size, m_block_size, m_block_size), 0)
	pygame.draw.rect(surface, (255, 0, 0), (m_top_left_x, m_top_left_y, m_play_width, m_play_height), 5)
	draw_grid(surface, grid)

def get_score(pts, score, combo, level):
	i = ((level * pts) / 4) + 1
	i = i * pts
	i = i * combo
	score += i
	score = round(score)
	return score

def update_bag(bag, current_piece):
	bag.shift()
	newbag = bag
	newbag.append(current_piece.shape)
	return newbag

def main(win):
	locked_pos = {}
	grid = create_grid(locked_pos)
	change_piece = False
	run = True
	bag = [S, Z, S, Z]
	current_piece = get_shape(bag)
	next_piece = get_shape(bag)
	clock = pygame.time.Clock()
	fall_time = 0
	fall_speed = 0.17
	level = 1
	lock = round(fall_speed * 140)
	pts = 0
	held = 0
	cleared_line = 0
	score = 0
	combo = 1
	hold_piece = Piece(5, 0, O)

	while run:
		bag.pop(0)
		bag.append(current_piece.shape)
		grid = create_grid(locked_pos)
		fall_time += clock.get_rawtime()
		clock.tick()
		i = level
		level = round((cleared_line / 10)) + 1
		if level > i:
			fall_speed -= 0.05
		if fall_time / 1000 > fall_speed:
			fall_time = 0
			current_piece.y += 1
			if not(valid_space(current_piece, grid)) and current_piece.y > 0:
				while not(valid_space(current_piece, grid)) and current_piece.y > 0:
						current_piece.y -= 1
			else:
				lock = round(fall_speed * 140)
		current_piece.y += 1
		if not(valid_space(current_piece, grid)) and current_piece.y > 0:
			lock -= 1
			if lock == 0:
				change_piece = True
		current_piece.y -= 1
		for event in pygame.event.get():
			if event.type== pygame.QUIT:
				run = False
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					current_piece.x -= 1
					if not (valid_space(current_piece, grid)):
						current_piece.x +=1
				if event.key == pygame.K_RIGHT:
					current_piece.x += 1
					if not (valid_space(current_piece, grid)):
						current_piece.x -=1
				if event.key == pygame.K_DOWN:
					current_piece.y +=1
					if not (valid_space(current_piece, grid)):
						current_piece.y -=1
				if event.key == pygame.K_UP:
						while valid_space(current_piece, grid) and current_piece.y < 21:
							current_piece.y += 1
						while not valid_space(current_piece, grid):
							current_piece.y -= 1
				if event.key == pygame.K_s:
					current_piece.rotation += 1
					if not (valid_space(current_piece, grid)):
						current_piece.x += 1
						if not (valid_space(current_piece, grid)):
							current_piece.x -= 2
							if not (valid_space(current_piece, grid)):
								current_piece.x += 1
								current_piece.rotation -=1
				if event.key == pygame.K_d:
					current_piece.rotation -= 1
					if not (valid_space(current_piece, grid)):
						current_piece.x += 1
						if not (valid_space(current_piece, grid)):
							current_piece.x -= 2
							if not (valid_space(current_piece, grid)):
								current_piece.x += 1
								current_piece.rotation +=1
				if event.key == pygame.K_SPACE and held == 0:
					held = 1
					tmp = copy.deepcopy(current_piece)
					current_piece = copy.deepcopy(hold_piece)
					hold_piece = tmp
				if event.key == pygame.K_f:
					garbage(grid, locked_pos, 3)
					grid = create_grid(locked_pos)
					draw_window(win, grid, score, combo)
					pygame.display.update()

		shape_pos = convert_shape_format(current_piece)
		ghost = copy.deepcopy(current_piece)
		ghost.y = -25
		while valid_space(ghost, grid) and ghost.y < 22:
			ghost.y += 1
		while not valid_space(ghost, grid):
			ghost.y -= 1
		ghost_pos = convert_shape_format(ghost)
		
		for i in range(len(ghost_pos)):
			x, y = ghost_pos[i]
			if y > - 1:
				grid[y][x] = (255, 255, 255)
		for i in range(len(shape_pos)):
			x, y = shape_pos[i]
			if y > - 1:
				grid[y][x] = current_piece.color
		
		if change_piece:
			for pos in shape_pos:
				p = (pos[0], pos[1])
				locked_pos[p] = current_piece.color
			current_piece = next_piece
			next_piece = get_shape(bag)
			change_piece = False
			pts = clear_rows(grid, locked_pos)
			if pts > 0:
				combo = combo + (2 * pts) - 2
			else:
				combo = 1
			cleared_line += pts
			while pts:
				clear_rows(grid, locked_pos)
				pts -= pts
			lock = round(fall_speed * 140)
			held = 0
		
		score = get_score(pts, score, combo, level)
		draw_window(win, grid, score, combo)
		draw_hold(win, hold_piece)
		draw_next_shape(next_piece, win, cleared_line, level)
		pygame.display.update()
		if check_lost(locked_pos):
			run = False
			update_score(score)

def main_menu(win):
	run = True
	while run:
		win.fill((0,0,0))
		draw_text_middle("Press Any Key To Play", 60, (255, 255, 255), win)
		pygame.display.update()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
			if event.type == pygame.KEYDOWN:
				main(win)
	pygame.display.quit()

if __name__ == "__main__":
    pygame.font.init()
win = pygame.display.set_mode((s_width, s_height))
pygame.display.set_caption('Tetris')
main_menu(win)