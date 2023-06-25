import pygame
import math
import time

def distance(pos1, pos2):
	return math.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)

def get_angle_pos(angle):
	anglex = math.cos(math.radians(angle))
	angley = math.sin(math.radians(angle))

	return (anglex, angley)

def get_translated_position_from_angle(position, angle, scaling_factor=1):
	pos = get_angle_pos(angle)

	anglex = pos[0]
	angley = pos[1]

	anglex = position.x + scaling_factor * anglex
	angley = position.y + scaling_factor * -angley

	return (anglex, angley)

def draw_circle_angle(screen, point, final_angle):
	if final_angle <= 1:
		return

	pink_col = (255,0,255)
	circle_rad = 50

	for angle in range(1, final_angle):		
		apos = get_angle_pos(angle)

		anglex = apos[0]
		angley = apos[1]

		anglex = point[0] + circle_rad * anglex
		angley = point[1] + circle_rad * -angley

		screen.set_at((int(anglex), int(angley)), pink_col)


def main(winx, winy):
	pygame.display.init()

	black_col = (0,0,0)
	blue_col = (9,11,141)
	green_col = (61,192,62)
	pink_col = (255,0,255)
	grey_col = (170,170,170)

	screen = pygame.display.set_mode((winx, winy))

	done = False

	midpoint = pygame.math.Vector2(winx//2, winy//2)
	midpoint_distance = int(distance((winx//2, 0), midpoint))

	outline_offset = 25
	outline_rad = int(midpoint_distance - outline_offset)

	left_vec = pygame.math.Vector2((winx, winy//2)) - midpoint
	left_vec.normalize_ip()

	while not done:
		# Update
		mouse_pos = pygame.math.Vector2(pygame.mouse.get_pos())

		loc_vec = mouse_pos - midpoint
		loc_vec.normalize_ip()

		cangle = int(left_vec.angle_to(loc_vec))
		if cangle < 0:
			cangle = -cangle
		else:
			cangle = 360 - cangle

		#print("cangle", cangle)

		# Input
		for e in pygame.event.get():
			if e.type == pygame.KEYDOWN:
				if e.key == 27: # Esc
					print("Quitting..")
					done = True

		# Render
		screen.fill(black_col)

		# crosshairs
		pygame.draw.line(screen, pink_col, (0, winy//2), (winx, winy//2))
		pygame.draw.line(screen, pink_col, (winx//2, 0), (winx//2, winy))

		# outline
		pygame.draw.circle(
			screen,
			blue_col,
			(int(midpoint.x), int(midpoint.y)),
			outline_rad,
			2
		)

		# angle
		draw_circle_angle(screen, midpoint, cangle)
		
		# location vector
		#pygame.draw.line(
		#	screen,
		#	grey_col,
		#	(int(midpoint.x), int(midpoint.y)),
		#	(int(canglex), int(cangley)),
		#)
		pygame.display.flip()

	pygame.display.quit()


if __name__ == "__main__":
	winx = 600
	winy = winx

	main(winx, winy)
