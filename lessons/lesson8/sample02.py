import arcade
from arcade.gui import UIManager, UIFlatButton, UITextureButton, UILabel, UIInputText, UITextArea, UISlider, UIDropdown, \
    UIMessageBox  # Это разные виджеты
from arcade.gui.widgets.layout import UIAnchorLayout, UIBoxLayout  # А это менеджеры компоновки, как в pyQT


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

class MyGUIWindow(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Супер GUI Пример!")
        arcade.set_background_color(arcade.color.GRAY)
        
        # UIManager — сердце GUI
        self.manager = UIManager()
        self.manager.enable()  # Включить, чтоб виджеты работали
        
        # Layout для организации — как полки в шкафу
        self.anchor_layout = UIAnchorLayout()  # Центрирует виджеты
        self.box_layout = UIBoxLayout(vertical=True, space_between=10)  # Вертикальный стек
        
        # Добавим все виджеты в box, потом box в anchor
        self.setup_widgets()  # Функция ниже
        
        self.anchor_layout.add(self.box_layout)  # Box в anchor
        self.manager.add(self.anchor_layout)  # Всё в manager

    def on_button_click(self, button_text):
        message_box = UIMessageBox(
            width=300, height=200,
            message_text="Это UIMessageBox!\nХочешь продолжить?",
            buttons=("Да", "Нет")
        )
        message_box.on_action = self.on_message_button
        self.manager.add(message_box)

    def setup_widgets(self):
        # Здесь добавим ВСЕ виджеты — по порядку!
        label = UILabel(text="Привет, Мир! Это UILabel", 
                        font_size=20, 
                        text_color=arcade.color.WHITE, 
                        width=300, 
                        align="center")
        self.box_layout.add(label)

        text_area = UITextArea(text="Это UITextArea.\nМного строк!\nДля логов или чата.\nИли блога про своего котика", width=200, height=100, 
                               font_size=14, is_editable=True, scroll_speed=10)
        self.box_layout.add(text_area)

        flat_button = UIFlatButton(text="Плоская Кнопка", width=200, height=50, color=arcade.color.BLUE)
        flat_button.on_click = self.on_button_click
        self.box_layout.add(flat_button) 

        texture_normal = arcade.load_texture(":resources:/gui_basic_assets/button/red_normal.png")
        texture_hovered = arcade.load_texture(":resources:/gui_basic_assets/button/red_hover.png")
        texture_pressed = arcade.load_texture(":resources:/gui_basic_assets/button/red_press.png")
        texture_button = UITextureButton(texture=texture_normal, 
                                         texture_hovered=texture_hovered,
                                         texture_pressed=texture_pressed,
                                         scale=1.0)
        texture_button.on_click = lambda event: print("Текстурный клик!")
        self.box_layout.add(texture_button)

        input_text = UIInputText(x=0, y=0, width=200, height=30, text="Введи имя")
        input_text.on_change = lambda text: print(f"Текст изменился: {text}")
        self.box_layout.add(input_text)

        slider = UISlider(width=200, height=20, min_value=0, max_value=100, value=50)
        slider.on_change = lambda value: print(f"Слайдер: {value}")
        self.box_layout.add(slider)

        dropdown = UIDropdown(options=["Опция 1", "Опция 2", "Опция 3"], width=200)
        dropdown.on_change = lambda value: print(f"Выбрано: {value}")
        self.box_layout.add(dropdown)

    def on_message_button(self, event):
        print(f"Диалог: {event}")

    def on_draw(self):
        self.clear()
        self.manager.draw()  # Рисуй GUI поверх всего

    def on_mouse_press(self, x, y, button, modifiers):
        pass  # Для кликов, но manager сам обрабатывает

# Запуск
window = MyGUIWindow()
arcade.run()
