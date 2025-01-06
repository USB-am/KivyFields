from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen


class AppTest(MDApp):
	def __init__(self, *a, **kw):
		super().__init__(*a, **kw)

		self.screen = Screen()

	def build(self):
		return self.screen
