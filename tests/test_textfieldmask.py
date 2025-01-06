import unittest

from tests import AppTest

from mask_textfield import MaskField


class TestTextFieldMask(unittest.TestCase):
	''' Тесты текстового поля с маской '''

	@classmethod
	def setUpClass(cls):
		cls.app = AppTest()

		cls.mask = '+7 (___) ___-__-__'
		cls.mask_field = MaskField(
			mask=cls.mask,
			symbol='_',
			only_digits=True
		)
		cls.app.screen.add_widget(cls.mask_field)

	@classmethod
	def tearDownClass(cls):
		cls.app.screen.remove_widget(cls.mask_field)

	def setUp(self):
		self.mask_field.clear()

	def test_update_text(self):
		self.mask_field.memory = '8005553535'
		self.mask_field.update_text()
		self.assertEqual(self.mask_field.text, '+7 (800) 555-35-35')

		self.mask_field.memory = '800555'
		self.mask_field.update_text()
		self.assertEqual(self.mask_field.text, '+7 (800) 555-__-__')

	def test_insert_text(self):
		self.mask_field.insert_text('q')
		self.assertEqual(self.mask_field.text, '+7 (___) ___-__-__')

		self.mask_field.insert_text('8')
		self.assertEqual(self.mask_field.text, '+7 (8__) ___-__-__')

	def test_do_backspace(self):
		self.mask_field.memory = '8005553535'
		self.mask_field.do_backspace()
		self.assertEqual(self.mask_field.text, '+7 (800) 555-35-3_')


if __name__ == '__main__':
	unittest.main()
