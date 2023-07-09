import pygame

class FontController(object):
	font_instance = None

	def __init__(self):
		print("Call 'get_instance'")

	@classmethod
	def quit(cls):
		if cls.font_instance:
			pygame.font.quit()

	@classmethod
	def get_instance(cls):
		if not cls.font_instance:
			pygame.font.init()
			cls.font_instance = pygame.font.Font('freesansbold.ttf', 16)
		return cls.font_instance
