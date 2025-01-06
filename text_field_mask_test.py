# -*- coding: utf-8 -*-

from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.textfield import MDTextField


Builder.load_string('''
<MaskField>:
	hint_text: 'Test'
	mask: '+7 (___) ___-__-__'
	symbol: '_'
	only_digits: True
	text: self.mask
''')


class MaskField(MDTextField):
	'''
	Text widget with input mask.

	~params:
	mask: str - the mask by which the field will be filled;
	symbol: str - the character that will be replaced by the entered value;
	only_digits: bool - allow input of numbers only.
	'''

	def __init__(self, mask: str='', symbol: str='_', only_digits: bool=True, **kwargs):
		self.mask = mask
		self.symbol = symbol
		self.only_digits = only_digits

		super().__init__(**kwargs)

		self.memory = ''

	def insert_text(self, substring: str, from_undo: bool=False) -> None:
		''' Input processing '''
		if self.only_digits and not substring.isdigit():
			return

		ind = self.text.find(self.symbol)

		if ind >= 0:
			self.memory += substring
			self.update_text()
			try:
				self.cursor = (self.text.index(self.symbol), 0)
			except ValueError:
				self.cursor = (len(self.mask), 0)

	def do_backspace(self, from_undo: bool=False, mode: str='bkspc') -> None:
		''' Handling backspace pressing '''
		ind = abs(self.cursor_index()-1)
		memory_ind = self.mask.count(self.symbol, 0, ind)
		self.memory = self.memory[:memory_ind] + self.memory[memory_ind+1:]

		self.update_text()
		self.cursor = (ind, 0)

	def update_text(self) -> None:
		''' Update text to match values ​​in memory '''

		result = self.mask
		for char in self.memory:
			result = result.replace(self.symbol, char, 1)

		self.text = result

	def clear(self) -> None:
		self.text = self.mask
		self.memory = ''


class TestApp(MDApp):
	def build(self):
		return MaskField()


if __name__ == '__main__':
	TestApp().run()
