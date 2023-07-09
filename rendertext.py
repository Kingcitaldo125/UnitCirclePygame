from pygame import font
from fontcontroller import FontController

class RenderText():
	def __init__(
		self,
		font_controller: FontController,
		foreground_col: tuple,
		background_col: tuple,
		x=0,
		y=0,
		text="",
	):
		self.font = font_controller.get_instance()
		self.text = text
		self.x = x
		self.y = y
		self.foreground_col = foreground_col
		self.background_col = background_col

	def update_x(self, newx):
		self.x = newx

	def update_y(self, newy):
		self.y = newy

	def update_text(self, newtext):
		self.text = newtext

	def draw(self, screen):
		xtext = self.font.render(self.text, False, self.foreground_col, self.background_col)
		xtext_rect = xtext.get_rect()
		xtext_rect.center = (self.x, self.y)
		screen.blit(xtext, xtext_rect)
