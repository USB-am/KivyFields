# -*- coding: utf-8 -*-

from typing import Type, List, Dict, Union, Callable

from kivy.lang.builder import Builder
from kivy.properties import BooleanProperty, StringProperty, ListProperty
from kivy.uix.recycleview import RecycleView
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout


Builder.load_string('''
<_BaseRecycleSelect>:
	orientation: 'vertical'
	size_hint_y: None
	height: dp(400)

	MDBoxLayout:
		orientation: 'horizontal'
		size_hint_y: None
		height: dp(50)

		MDIcon:
			size_hint: (None, None)
			size: (dp(25), dp(50))
			icon: 'checkbox-marked-outline'

		MDLabel:
			text: root.title

		MDIconButton:
			id: add_btn
			size_hint: (None, None)
			size: (dp(50), dp(50))
			icon: 'plus'

	_SelectRecycleView:
		id: recycle_view


<_SelectRecycleView>:
	viewclass: 'SelectElement'

	SelectableRecycleBoxLayout:
		default_size: None, dp(50)
		default_size_hint: 1, None
		size_hint_y: None
		height: self.minimum_height
		orientation: 'vertical'


<SelectElement>:
	orientation: 'horizontal'
	size_hint_y: None
	height: dp(50)
	active: checkbox.active

	MDCheckbox:
		id: checkbox
		active: root.active
		group: root.group
		size_hint: (None, None)
		size: (dp(50), dp(50))
		on_release: root.store_checkbox_state()

	MDLabel:
		size_hint: (1, 1)
		text: root.text
''')


class SelectElement(RecycleDataViewBehavior, MDBoxLayout):
	''' List element '''

	index = None
	text = StringProperty()
	active = BooleanProperty()
	group = StringProperty(None)

	def refresh_view_attrs(self, rv, index, data):
		self.index = index
		return super().refresh_view_attrs(rv, index, data)

	def store_checkbox_state(self):
		rv = self.parent.parent
		rv.select_pressed_checkbox(index=self.index,
		                           state=self.active,
		                           group=self.group)


class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior, RecycleBoxLayout):
	''' Предстваление области отображения элементов списка '''


class _SelectRecycleView(RecycleView):
	''' Вьюха списка элементов '''

	def __init__(self, callbacks: List[Callable]=[], **options):
		super().__init__(**options)

		self.callbacks = callbacks

	def update_checkbox_state(self, index: int, state: bool, group: str) -> None:
		''' Обновить состояния чекбоксов '''

		if group:
			for elem in self.data:
				# if elem['active']:
				elem['active'] = False
		self.data[index]['active'] = state

	def run_callbacks(self) -> None:
		''' Запустить связанные методы '''
		for callback in self.callbacks:
			callback()

	def select_pressed_checkbox(self, index: int, state: bool, group: str) -> None:
		''' Изменить состояние выбранного чекбокса '''
		self.update_checkbox_state(index, state, group)
		self.run_callbacks()

	def select_by_entry(self, entry_id: int) -> None:
		''' Выбрать элемент '''

		if entry_id is None:
			return

		for element in self.data:
			if element['entry'].id == entry_id:
				break

		elem_index = self.data.index(element)
		self.data[elem_index]['active'] = True


class _BaseRecycleSelect(MDBoxLayout):
	'''
	Basic representation of a select field.

	~params:
	title: str - text on the top panel;
	data: List[Dict] - list of dictionaries containing information about the elements;
	group: str - name of the group of items.
	'''

	title = StringProperty()
	data = ListProperty()
	group = StringProperty(None)

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.update_data(new_data=kwargs['data'])

	def update_data(self, new_data: List[Dict]) -> None:
		self.ids.recycle_view.data = new_data

	def bind_btn(self, callback: Callable) -> None:
		''' Bind button on the top panel '''
		self.ids.add_btn.bind(on_release=lambda *_: callback())


class RecycleSelect(_BaseRecycleSelect):
	''' Single item selection field '''

	def get_value(self) -> Union[int, None]:
		''' Получить id выбранного элемента '''

		try:
			selected_elem = next(filter(lambda elem: elem['active'], self.data))
			if selected_elem:
				entry = selected_elem.get('entry')
				if entry:
					return entry.id
		except StopIteration:
			return None

	def set_value(self, entry_id: int) -> None:
		''' Выбрать элемент '''
		self.ids.recycle_view.select_by_entry(entry_id)


class RecycleMultiSelect(_BaseRecycleSelect):
	''' Поле выбора множества элементов '''

	def __init__(self, **kwargs):
		kwargs.update({'group': None})
		super().__init__(**kwargs)

	def get_value(self) -> List:
		''' Получить записи о выбранных элементах '''

		filtered_elems = filter(lambda elem: elem['active'], self.data)
		return list(map(lambda elem: elem['text'], filtered_elems))

	def set_value(self, entries: List) -> None:
		''' Выбрать элементы '''

		for entry in entries:
			self.ids.recycle_view.select_by_entry(entry.id)


class TestApp(MDApp):
	def build(self):
		return RecycleSelect(title='Test', data=[{
				'text': f'Element #{i+1}',
				'active': False,
				'group': 'test'} \
			for i in range(100)])


if __name__ == '__main__':
	TestApp().run()
