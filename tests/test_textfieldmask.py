import unittest

from tests import AppTest

from text_field_mask_test import MaskField


class TestTextFieldMask(unittest.TestCase):
	''' Тесты текстового поля с маской '''

	@classmethod
	def setUpClass(cls):
		cls.app = AppTest()
		cls.mask_field = MaskField(mask='+7 (___) ___-__-__')
		cls.app.screen.add_widget(cls.mask_field)

	@classmethod
	def tearDownClass(cls):
		cls.app.screen.remove_widget(cls.mask_field)

	def setUp(self):
		self.mask_field.clear()

	def test_oasdjaiosdj(self):
		self.assertEqual(True, 1==1)


if __name__ == '__main__':
	unittest.main()
