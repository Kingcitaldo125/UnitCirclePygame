import pygame
import math
from random import randrange

from fontcontroller import FontController
from rendertext import RenderText


def lerp(v0, v1, t):
	return v0 + t * (v1 - v0)

def get_angle_pos(angle):
	"""
	Given an angle, in degrees, return the resulting normalized x,y polar coordinate.
	"""
	anglex = math.cos(math.radians(angle))
	angley = math.sin(math.radians(angle))

	return (anglex, angley)


def get_translated_position_from_angle(position, angle, scaling_factor=1):
	"""
	Given an angle, in degrees, and a position, as a PyGame Vector2,
	return the resulting normalized x,y polar coordinate translated to
	a world space position that's indicated by the position vector.
	scaling_factor will scale the resulting positions by a factor of
	itself and the associated angle position.
	"""
	pos = get_angle_pos(angle)

	anglex = pos[0]
	angley = pos[1]

	anglex = position.x + scaling_factor * anglex
	angley = position.y + scaling_factor * -angley

	return (anglex, angley)


def draw_circle_angle(screen, point, final_angle):
	"""
	Draw a 'partial' circle around the 'point' position vector, up to the 'final_angle'.
	Calculates the position of the pixels that should be 'filled in' given a partial angle,
	then fills in the resulting pixels at said position.
	Moves in a counter-clockwise direction, starting at angle/theta of '1' degrees.
	"""
	pink_col = (255,0,255)
	circle_rad = 50

	for angle in range(final_angle):
		apos = get_angle_pos(angle)

		anglex = apos[0]
		angley = apos[1]

		anglex = point[0] + circle_rad * anglex
		angley = point[1] + circle_rad * -angley

		screen.set_at((int(anglex), int(angley)), pink_col)

def draw_angle_vectors(screen, blue_col, green_col, midpoint, finalpoint):
	"""
	Draw lines representing the x and y angle vectors to the 'screen'.
	The x vector represents the 'adjacent' side of the angle in the unit circle (blue).
	The y vector represents the 'opposite' side of the angle in the unit circle (green).
	"""
	# x angle vector
	pygame.draw.line(
		screen,
		blue_col,
		(int(midpoint.x), int(midpoint.y)),
		(int(finalpoint.x), int(midpoint.y)),
		2,
	)

	# y angle vector
	pygame.draw.line(
		screen,
		green_col,
		(int(finalpoint.x), int(midpoint.y)),
		(int(finalpoint.x), int(finalpoint.y)),
		2,
	)

def draw_cos_text(screen, rendertext, theta):
	"""
	Draw 'cos(theta) = X to the screen. Where 'X' is the cosine of the 'theta'.
	"""
	cos_text_val = str(round(math.cos(math.radians(theta)),3))
	rendertext.update_x(150)
	rendertext.update_y(30)
	rendertext.update_text("cos("+str(theta)+"°) = "+cos_text_val)
	rendertext.draw(screen)

def draw_sin_text(screen, rendertext, theta):
	"""
	Draw 'sin(theta) = X to the screen. Where 'X' is the sine of the 'theta'.
	"""
	sin_text_val = str(round(math.sin(math.radians(theta)),3))
	rendertext.update_x(150)
	rendertext.update_y(65)
	rendertext.update_text("sin("+str(theta)+"°) = "+sin_text_val)
	rendertext.draw(screen)

def draw_tan_text(screen, rendertext, theta):
	"""
	Draw 'tan(theta) = X to the screen. Where 'X' is the tangent of the 'theta'.
	"""
	tan_val = math.tan(math.radians(theta))
	tan_text_val = str(round(tan_val,3))
	rendertext.update_x(150)
	rendertext.update_y(100)
	rendertext.update_text("sin("+str(theta)+"°) = "+tan_text_val)
	rendertext.draw(screen)

def main(winx, winy):
	"""
	Driver code. Houses all of the main application logic.
	"""
	pygame.display.init()

	black_col = (18,22,28)
	red_col = (255,0,0)
	blue_col = (0,0,255)
	green_col = (0,255,0)
	pink_col = (255,0,255)
	grey_col = (170,170,170)
	rand_col = tuple([randrange(0,255) for i in range(3)])

	screen = pygame.display.set_mode((winx, winy))

	clock = pygame.time.Clock()

	font_controller = FontController()

	done = False

	midpoint = pygame.math.Vector2(winx//2, winy//2)
	toppoint = pygame.math.Vector2((winx//2, 0))
	midpoint_distance = midpoint.distance_to(toppoint) - 100

	outline_offset = 25
	outline_rad = int(midpoint_distance - outline_offset)

	left_vec = pygame.math.Vector2((winx, winy//2)) - midpoint
	left_vec.normalize_ip()

	cosine_rendertext = RenderText(font_controller, blue_col, black_col)
	sine_rendertext = RenderText(font_controller, green_col, black_col)
	tangent_rendertext = RenderText(font_controller, grey_col, black_col)

	print("Press 'Esc' to quit")

	while not done:
		# Update
		mouse_pos = pygame.math.Vector2(pygame.mouse.get_pos())

		angle_vec = mouse_pos - midpoint
		theta = 0

		try:
			angle_vec.normalize_ip()
			theta = int(left_vec.angle_to(angle_vec))
		except ValueError:
			pass

		if theta < 0:
			theta = -theta
		else:
			theta = 360 - theta

		if theta == 360:
			theta = 0

		# Extract position details from the angle
		# Should automatically translate to the midpoint
		# and scale to the outline circle's radius
		thetax, thetay = get_translated_position_from_angle(
			midpoint,
			theta,
			outline_rad,
		)

		rad_vec = pygame.math.Vector2((thetax, thetay))

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
		if theta != 90:
			draw_circle_angle(screen, midpoint, theta)
		else:
			pygame.draw.rect(screen, pink_col, (midpoint.x, midpoint.y - 50, 50, 51), 1)

		# location vector
		# represents the 'hypotenuse' side of the angle in the unit circle (grey).
		pygame.draw.line(
			screen,
			grey_col,
			(int(midpoint.x), int(midpoint.y)),
			(int(thetax), int(thetay)),
			2,
		)

		# Circle at point where angle vector and outer circle intersect
		pygame.draw.circle(screen, red_col, (int(rad_vec.x), int(rad_vec.y)), 3)

		# Circle at point along the angle vector where it and mouse point intersect
		pygame.draw.circle(screen, rand_col, (int(lerped_pos.x), int(lerped_pos.y)), 5)

		draw_angle_vectors(screen, blue_col, green_col, midpoint, rad_vec)

		# Text
		draw_cos_text(screen, cosine_rendertext, theta)
		draw_sin_text(screen, sine_rendertext, theta)
		draw_tan_text(screen, tangent_rendertext, theta)
		
		#"""
		# Draw text value cosine along angle vector
		cos_text_val = str(round(math.cos(math.radians(theta)),3))

		cosine_rendertext.update_x(lerp(int(midpoint.x), int(rad_vec.x), 0.5))
		cosine_rendertext.update_y(winy//2)
		cosine_rendertext.update_text(cos_text_val)
		cosine_rendertext.draw(screen)

		# Draw text value sine along angle vector
		sin_text_val = str(round(math.sin(math.radians(theta)),3))

		sine_rendertext.update_x(int(rad_vec.x))
		sine_rendertext.update_y(lerp(int(midpoint.y), int(rad_vec.y), 0.5))
		sine_rendertext.update_text(sin_text_val)
		sine_rendertext.draw(screen)
		#"""

		pygame.display.flip()

		clock.tick(60)

	font_controller.quit()
	pygame.display.quit()


if __name__ == "__main__":
	winx = 600
	winy = winx

	main(winx, winy)
