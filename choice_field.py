# -*- coding: utf-8 -*-

from typing import List, Dict

from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.textfield import MDTextField


Builder.load_string('''
<ChoiceSelectField>:
    id: container
''')


class ChoiceSelectField(MDBoxLayout):
    def __init__(self, content: Widget, items: List[Dict], **options):
        '''
        Поле выбора одного варианта из множества items в открываемом по клику выпадающему меню.

        :param content: отображаемая часть.
        :param items: список словарей для отображения.
            items = [{
                'text': '...',
                'viewclass': 'OneLineListItem',
                'on_release': <Callable>
            }, ...]
        :param **options: аргументы MDBoxLayout для родительского класса.
        '''
        self.content = content
        self.items = items
        self.is_open = False

        super().__init__(**options)

        self.add_widget(content)

    def bind_caller(self, caller: Widget, position: str='bottom', width_mult: int=4) -> None:
        '''
        Привязать событие открытия выпадающего меню.

        :param caller: виждет открывающий выпадающее меню.
        :param position: позиция всплывающего меню (auto, center, bottom).
        :param width_mult: ширина меню выбора.
        '''
        self.menu = MDDropdownMenu(
            caller=caller,
            items=self.items,
            width_mult=width_mult
        )
        self.menu.bind(on_dismiss=self.close_menu)

    def open_menu(self, *_) -> None:
        ''' Открыть меню '''
        if not hasattr(self, 'menu'):
            return

        if self.is_open:
            self.menu.dismiss()

        self.menu.open()
        self.is_open = True

    def close_menu(self, *_) -> None:
        if self.is_open:
            self.menu.dismiss()
        self.is_open = False


class TestApp(MDApp):
    def build(self):

        def set_text(instance: MDTextField, text: str) -> None:
            instance.text = text

        txt_field = MDTextField(hint_text='Enter text')

        choice = ChoiceSelectField(
            content=txt_field,
            items=[
                {
                    'text': f'Item #{i}',
                    'viewclass': 'OneLineListItem',
                    'on_release': lambda choice=f"Item #{i}": set_text(txt_field, choice)
                }
                for i in range(50)
            ])
        choice.bind_caller(caller=txt_field)
        txt_field.bind(text=choice.open_menu)
        return choice


if __name__ == '__main__':
    TestApp().run()
