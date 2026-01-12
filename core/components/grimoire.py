# core/components/grimoire.py
from constants import GRIMOIRE
import arcade


class Grimoire:
    def __init__(self, center_x, center_y, wight, height, ):
        self.data = GRIMOIRE

        self.height = self.data.get('height', height)
        self.wight = self.data.get('weight', wight)
        self.bottom_x = center_x
        self.bottom_y = center_y

        self.is_open = False
        self.current_chapter = 0
        self.current_page = 0

        self.discovered_spells = set()  # открытые заклинания
        self.discovered_elements = set()  # открытые элементы

        self.background_texture = self.data.get('texture', None)
        self.bookmarking_list = self.data.get()

        bookmark_path = self.data["bookmark_textures"]

        self.bookmark_textures = []
        for i in range(self.data["bookmark_count"]):
            path = bookmark_path.format(i)
            texture = arcade.load_texture(path)
            self.bookmark_textures.append(texture)

    def open(self):
        """ Метод открытия гримуара"""
        if self.is_open:
            return

        self.is_open = True

    def close(self):
        """ Метод закрытия гримуара"""
        if not self.is_open:
            return
        self.is_open = False

    def toggle(self):
        """ Метод переключения состояния гримуара"""
        if self.is_open:
            self.close()
        else:
            self.open()

    def next_page(self):
        """ Метод для откртия следующей страницы"""
        pass

    def prev_page(self):
        """ Метод для открытия предыдущей страницы"""
        pass

    def go_to_chapter(self, chapter_index):
        """ Метод для открытия нужной главы через закладку"""
        pass

    def unlock_spell(self, spell_name):
        """ Метод для разблокировки заклинания и добавления его в гримуар"""
        pass

    def unlock_element(self, element_name):
        """ Метод для разблокирвоки элемента/стихии"""
        pass

    def draw(self):
        if not self.is_open:
            return
        if self.background_texture:
            arcade.draw_texture_rect(self.background_texture, arcade.a(self.bottom_x, self.bottom_y, self.wight, self.height))
