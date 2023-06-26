import pygame
import math
from random import randrange
import time


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
	red_col = (255,0,0)
	blue_col = (9,11,141)
	green_col = (61,192,62)
	pink_col = (255,0,255)
	grey_col = (170,170,170)
	rand_col = tuple([randrange(0,255) for i in range(3)])

	screen = pygame.display.set_mode((winx, winy))

	done = False

	midpoint = pygame.math.Vector2(winx//2, winy//2)
	toppoint = pygame.math.Vector2((winx//2, 0))
	midpoint_distance = midpoint.distance_to(toppoint)

	outline_offset = 25
	outline_rad = int(midpoint_distance - outline_offset)

	left_vec = pygame.math.Vector2((winx, winy//2)) - midpoint
	left_vec.normalize_ip()

	while not done:
		# Update
		mouse_pos = pygame.math.Vector2(pygame.mouse.get_pos())

		angle_vec = mouse_pos - midpoint
		cangle = 0

		try:
			angle_vec.normalize_ip()
			cangle = int(left_vec.angle_to(angle_vec))
		except ValueError:
			pass

		if cangle < 0:
			cangle = -cangle
		else:
			cangle = 360 - cangle\

		# Extract position details from the angle
		# Should automatically translate to the midpoint
		# and scale to the outline circle's radius
		canglex, cangley = get_translated_position_from_angle(
			midpoint,
			cangle,
			outline_rad,
		)

		rad_vec = pygame.math.Vector2((canglex, cangley))

		mp_dist = midpoint.distance_to(mouse_pos)
		rv_dist = rad_vec.distance_to(midpoint)
		ratio = mp_dist / rv_dist

		if ratio > 1.0:
			ratio = 1.0

		lerped_pos = rad_vec.lerp(pygame.math.Vector2(midpoint), 1-ratio)

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
		if cangle != 90:
			draw_circle_angle(screen, midpoint, cangle)
		else:
			pygame.draw.rect(screen, pink_col, (midpoint.x, midpoint.y - 50, 50, 51), 1)

		# location vector
		pygame.draw.line(
			screen,
			grey_col,
			(int(midpoint.x), int(midpoint.y)),
			(int(canglex), int(cangley)),
		)

		# Circle at point where angle vector and outer circle intersect
		pygame.draw.circle(screen, red_col, (int(rad_vec.x), int(rad_vec.y)), 3)

		# Circle at point along the angle vector where it and mouse point intersect
		pygame.draw.circle(screen, rand_col, (int(lerped_pos.x), int(lerped_pos.y)), 5)

		# x angle vector
		pygame.draw.line(
			screen,
			blue_col,
			(int(midpoint.x), int(midpoint.y)),
			(int(mouse_pos.x), int(midpoint.y)),
		)

		# y angle vector
		pygame.draw.line(
			screen,
			green_col,
			(int(mouse_pos.x), int(midpoint.y)),
			(int(mouse_pos.x), int(mouse_pos.y)),
		)

		pygame.display.flip()

	pygame.display.quit()


if __name__ == "__main__":
	winx = 600
	winy = winx

	main(winx, winy)
