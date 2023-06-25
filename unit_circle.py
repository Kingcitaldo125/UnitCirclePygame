import pygame
import math
import time

def distance(pos1, pos2):
	return math.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)

def draw_circle_angle(screen, midpoint, final_angle):
	if final_angle <= 1:
		return

	pink_col = (255,0,255)
	circle_rad = 50

	for angle in range(1, final_angle):
		anglex = midpoint[0]
		angley = midpoint[1]

		anglex = anglex + circle_rad * math.cos(math.radians(angle))
		angley = angley + circle_rad * -math.sin(math.radians(angle))

		screen.set_at((int(anglex), int(angley)), pink_col)


def main():
	pygame.display.init()

	black_col = (0,0,0)
	blue_col = (9,11,141)
	green_col = (61,192,62)
	pink_col = (255,0,255)

	winx = 600
	winy = winx

	screen = pygame.display.set_mode((winx, winy))

	done = False

	midpoint = (winx//2,winy//2)
	midpoint_distance = int(distance((winx//2,0), midpoint))
	outline_offset = 25
	outline_rad = midpoint_distance - outline_offset

	cangle = 2
	

	while not done:
		# Update
		mouse_pos = pygame.mouse.get_pos()

		# Input
		for e in pygame.event.get():
			if e.type == pygame.MOUSEBUTTONDOWN:
				if e.button == 4:
					cangle += 2
					cangle = cangle % 366
				elif e.button == 5:
					cangle -= 2
					if cangle <= 0:
						cangle = 365 - cangle

			if e.type == pygame.KEYDOWN:
				if e.key == 27: # Esc
					done = True

		# Render
		screen.fill(black_col)

		# crosshairs
		pygame.draw.line(screen, pink_col, (0, winy//2), (winx, winy//2))
		pygame.draw.line(screen, pink_col, (winx//2, 0), (winx//2, winy))

		# outline
		pygame.draw.circle(screen, blue_col, midpoint, outline_rad, 2)

		# angle
		draw_circle_angle(screen, midpoint, cangle)
		pygame.display.flip()

	pygame.display.quit()


if __name__ == "__main__":
	main()
