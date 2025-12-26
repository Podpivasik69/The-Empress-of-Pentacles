import arcade


class UltimateBar:
    def __init__(self, max_value, current_value, center_x, center_y,
                 width, height, color_left, color_mid, color_right, frame_texture_path, is_gradient=False):
        self.max_value = max_value  # максимум хп в хп баре
        self.current_value = current_value  # текущее значение хп в баре, изначально полное = максимальному
        self.center_x = center_x
        self.center_y = center_y
        self.width = width
        self.height = height
        # 3 основых цвета бара
        self.color_left = color_left
        self.color_mid = color_mid
        self.color_right = color_right
        # текстурка рамки
        self.frame_texture_path = frame_texture_path
        self.is_gradient = is_gradient  # определяем рисовать с градиентом или нет
        # TODO сделать градиент

    def setup(self):
        # вычисляем координаты для rect.LBWH
        self.left = self.center_x - self.width / 2
        self.bottom = self.center_y - self.height / 2
        self.frame_texture = arcade.load_texture(self.frame_texture_path)

    def set_value(self, new_value):
        """ Метод сеттер - установщик значения для прогресс бара"""
        # если новое значение меньше 0 то будет 0
        if new_value < 0:
            new_value = 0
        # тоже самое но с максимумом
        if new_value > self.max_value:
            new_value = self.max_value
        # обновление текущего значения бара
        self.current_value = new_value

    def draw_default(self):
        """ Отрисовка стандартного прогресс бара без градиента """
        if self.max_value <= 0:
            return

        # процент заполения
        procent = self.current_value / self.max_value
        if procent <= 0:
            arcade.draw_texture_rect(self.frame_texture, arcade.rect.XYWH \
                (self.center_x, self.center_y, self.width, self.height))
            return
        if procent < 0.33:
            color = self.color_left
        elif procent < 0.66:
            color = self.color_mid
        else:
            color = self.color_right

        # ширина заполения
        fill_widht = self.width * procent

        arcade.draw_rect_filled(arcade.rect.LBWH(self.left, self.bottom, fill_widht, self.height), color)
        arcade.draw_texture_rect(self.frame_texture, arcade.rect.XYWH \
            (self.center_x, self.center_y, self.width, self.height))

    def draw_gradient(self):
        """ Отрисовка прогресс бара с градинтными цветами """
        if self.max_value <= 0:
            return
        # процент заполения
        procent = self.current_value / self.max_value
        if procent <= 0.5:
            color1 = self.color_left
            color2 = self.color_mid
            ratio = procent / 0.5
        else:
            color1 = self.color_mid
            color2 = self.color_right
            ratio = (procent - 0.5) / 0.5
        # смешивание цветов по r g b каналам
        result_r = color1[0] * (1 - ratio) + color2[0] * ratio
        result_g = color1[1] * (1 - ratio) + color2[1] * ratio
        result_b = color1[2] * (1 - ratio) + color2[2] * ratio

        color = (int(result_r), int(result_g), int(result_b))

        # ширина заполения
        fill_widht = self.width * procent

        arcade.draw_rect_filled(arcade.rect.LBWH(self.left, self.bottom, fill_widht, self.height), color)
        arcade.draw_texture_rect(self.frame_texture, arcade.rect.XYWH \
            (self.center_x, self.center_y, self.width, self.height))

    def draw(self):
        if self.is_gradient:
            self.draw_gradient()
        else:
            self.draw_default()
