# -*- coding: utf-8 -*-

from typing import Any, List, Dict

from kivy.lang.builder import Builder
from kivymd.app import MDApp
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.boxlayout import MDBoxLayout


Builder.load_string('''
<_BaseChoiceField>:
    size_hint: 1, None
    height: dp(50)


<ChoiceSelectField>:
    MDTextField:
        id: txt_field
        hint_text: root.title
        on_text: root.open_menu()


<ChoiceFilterSelectField>:
    MDTextField:
        id: txt_field
        hint_text: root.title
        on_text: root.open_menu()
''')


class _BaseChoiceField(MDBoxLayout):
    def __init__(self, title: str, *args, **kwargs):
        self.title = title
        super().__init__(*args, **kwargs)
        self.menu_items = []
        self.menu = MDDropdownMenu(
            caller=self.ids.txt_field,
            items=self.menu_items,
            width_mult=4)
        self.menu.bind(on_dismiss=lambda *_: self.dismiss_menu())
        self.is_open = False

    def add_menu_items(self, items: List[Dict[str, Any]]) -> None:
        self.menu.items.extend(items)

    def update_menu_items(self, items: List[Dict[str, Any]]) -> None:
        self.menu.items = items

    def open_menu(self) -> None:
        if not hasattr(self, 'menu'):
            raise AttributeError('The MDDropdownMenu class was not pre-initialized. To resolve this, run the add_menu_items method before running the open_menu method.')
        if self.is_open:
            self.dismiss_menu()
        self.menu.open()
        self.is_open = True

    def dismiss_menu(self) -> None:
        if not hasattr(self, 'menu'):
            raise AttributeError('The MDDropdownMenu class was not pre-initialized. To resolve this, run the add_menu_items method before running the open_menu method.')
        self.menu.dismiss()
        self.is_open = False

    def menu_callback(self, text_item: str) -> None:
        self.ids.txt_field.text = text_item
        self.dismiss_menu()


class ChoiceSelectField(_BaseChoiceField):
    pass


class ChoiceFilterSelectField(_BaseChoiceField):
    def add_menu_items(self, items: List[Dict[str, Any]]) -> None:
        self.all_menu_items = items
        super().add_menu_items(items)

    def open_menu(self) -> None:
        txt = self.ids.txt_field.text.lower()
        items = list(filter(
            lambda item: txt in item['text'].lower(),
            self.all_menu_items))

        self.update_menu_items(items)
        super().open_menu()


class TestApp(MDApp):
    def build(self):
        all_items = ChoiceSelectField(title='Test ChoiceSelectField')
        menu_items = [{
                'text': f'Item #{i}',
                'viewclass': 'OneLineListItem',
                'on_release': lambda item=f'Item #{i}': all_items.menu_callback(item)
            } for i in range(10)]
        all_items.add_menu_items(menu_items)

        filtered_items = ChoiceFilterSelectField(title='Test ChoiceFilterSelectField')
        menu_items = [{
                'text': f'Item #{i}',
                'viewclass': 'OneLineListItem',
                'on_release': lambda item=f'Item #{i}': filtered_items.menu_callback(item)
            } for i in range(10)]
        filtered_items.add_menu_items(menu_items)

        boxl = MDBoxLayout(orientation='vertical')
        boxl.add_widget(all_items)
        boxl.add_widget(filtered_items)
        boxl.add_widget(MDBoxLayout())
        return boxl


if __name__ == '__main__':
    TestApp().run()
