# core/components/grimoire.py
from core.components.grimoire_data import (
    GRIMOIRE_CONFIG,
    GRIMOIRE_CHAPTER_1,
    GRIMOIRE_CHAPTER_1_PAGES,
    GRIMOIRE_TEXT_MARGINS
)
import arcade


class Grimoire:
    def __init__(self, center_x, center_y, width, height, ):
        # конфиг
        self.data = GRIMOIRE_CONFIG

        self.chapters = [
            GRIMOIRE_CHAPTER_1,
        ]

        # размеры
        self.height = self.data.get('height', height)
        self.width = self.data.get('width', width)
        self.center_x = center_x
        self.center_y = center_y

        self.is_open = False
        self.current_chapter = 0  # текущая глава
        self.current_spread = 0  # текущий разворот книги (вмещает 2 страницы)

        self.pages = []  # список текстов для страниц
        self.pages = GRIMOIRE_CHAPTER_1_PAGES  # закачиваем сюда страницы из конфига

        self.spreads = []  # список разворотов страниц (кортежей, где страницы - индексы)
        # пример
        # (0, 1) левая страница = pages[0], правая страница = pages[1]
        # (2, None) левая страница = pages[2], правая страница = None
        # выглядит примерно так
        # spreads = [
        #     (0, 1),
        #     (2, None)
        # ]
        self.build_spreads()  # создаем развороты

        self.discovered_spells = set()  # открытые заклинания
        self.discovered_elements = set()  # открытые элементы
        self.background_texture = self.data.get('texture', None)
        # self.bookmarking_list = self.data.get()

        bookmark_path = self.data["bookmark_textures"]

        self.bookmark_textures = []
        for i in range(self.data["bookmark_count"]):
            path = bookmark_path.format(i)
            texture = arcade.load_texture(path)
            self.bookmark_textures.append(texture)

        texture_path = self.data.get('texture')  # загружаем текстуру книги
        if texture_path:
            self.background_texture = arcade.load_texture(texture_path)
        else:
            self.background_texture = None

    def build_spreads(self):
        """
        Метод создающий список разворотов страниц
        в зависимости от четности количества страниц
        разворот это пара страниц (левая, правая)
        если правой страницы нет, то она None
        """

        self.spreads = []  # очищаем список перед началом
        self.kolvo_pages = len(self.pages)
        for i in range(0, self.kolvo_pages, 2):
            # левая страница всегда есть
            left_index = i
            # если есть правая страница
            if i + 1 < self.kolvo_pages:
                right_index = i + 1
            # если нет
            else:
                right_index = None
            self.spreads.append((left_index, right_index))
        print(f'инфа по гримуару, сейчас {self.kolvo_pages} страниц, и {len(self.spreads)} разворотов')
        print(f'инфа по гримуару, развороты {self.spreads}')

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

    def next_spread(self):
        """ Метод для откртия следующего разворота страничек """
        if self.current_spread < len(self.spreads) - 1:
            self.current_spread += 1
            print(f'инфо по гримуару, перешли сейчас к развороту {self.current_spread}')
            return True
        else:
            print(f'инфо по гримуару, мы уже на последнем развороте {self.current_spread}')
            return False

    def prev_spread(self):
        """ Метод для откртия предыдующего разворота страничек """
        if self.current_spread > 0:
            self.current_spread -= 1
            print(f'инфо по гримуару, вернулись к развороту {self.current_spread}')
            return True
        else:
            print(f'инфо по гримуару, мы еще на первом развороте {self.current_spread}')
            return False

    def go_to_chapter(self, chapter_index):
        """ Метод для открытия нужной главы через закладку"""
        pass

    def unlock_spell(self, spell_name):
        """ Метод для разблокировкxи заклинания и добавления его в гримуар"""
        pass

    def unlock_element(self, element_name):
        """ Метод для разблокирвоки элемента/стихии"""
        pass

    def draw(self):
        # if not self.is_open:
        #     return

        if self.background_texture:  # есть текстура? - нарисуем!
            rect = arcade.rect.XYWH(self.center_x, self.center_y, self.width, self.height)
            arcade.draw_texture_rect(self.background_texture, rect)
            # TODO удалить потом
            # print("есть текстура книжки")

        left_idx, right_idx = self.spreads[self.current_spread]  # получили индексы страниц текущего разворота
        left_content = self.pages[left_idx]['content']  # получили контент для страницы из конфига

        # Координаты книги
        book_left = self.center_x - self.width / 2
        book_bottom = self.center_y - self.height / 2
        book_top = book_bottom + self.height

        # координаты для текста с отступом из конфига
        # левая страница
        left_text_x = book_left + GRIMOIRE_TEXT_MARGINS["left_page"]["x"]
        left_text_y = book_top - GRIMOIRE_TEXT_MARGINS["left_page"]["y"]

        arcade.draw_text(
            left_content,
            left_text_x, left_text_y,
            arcade.color.BLACK,
            self.data.get("font_size", 16),
            width=GRIMOIRE_TEXT_MARGINS["left_page"]["width"]
        )
        # если на развороте есть правая страница
        if right_idx is not None:
            right_content = self.pages[right_idx]['content']
            # координаты для правого текста
            right_text_x = book_left + GRIMOIRE_TEXT_MARGINS["right_page"]["x"]
            right_text_y = book_top - GRIMOIRE_TEXT_MARGINS["right_page"]["y"]

            arcade.draw_text(
                right_content,
                right_text_x, right_text_y,
                arcade.color.BLACK,
                self.data.get("font_size", 16),
                width=GRIMOIRE_TEXT_MARGINS["right_page"]["width"]
            )
        else:
            pass
