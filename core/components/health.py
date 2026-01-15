class Health:
    def __init__(self, max_health=100, current_health=100):
        self.max_health = max_health
        self.current_health = current_health
        self.is_alive = True

    def take_damage(self, amount):
        """ Метод для получения урона"""

        # ничего не делаем если урон меньше 0 или мы мертвы
        if amount <= 0 or not self.is_alive:
            return False  # умер
        if self.current_health > 0:
            self.current_health -= amount

        # если хп меньше 0
        if self.current_health <= 0:
            self.current_health = 0
            self.is_alive = False
            return True  # умер

        return False  # выжил

    def heal(self, amount):
        """ Метод для получения лечения """

        # ничего не делаем если отрицательное лечение или мы мертвы
        if amount <= 0 or not self.is_alive:
            return False

        # если возможное лечение больше чем макс хп то просто хп станет максимальным
        # при лечении сверх макс хп, хм будет равно макс
        self.current_health = min(self.max_health, (self.current_health + amount))
        # 50 + 20 = 70 мин (100, 70) = 70
        # 90 + 20 = 110 мин (100, 110) = 100
        return True

    def set_health(self, value):
        """ Метод, чтобы установить количество здоровья """
        if value > 0:
            self.current_health = min(value, self.max_health)
            self.is_alive = True
        elif value == 0:
            self.is_alive = False
            self.current_health = 0

    def set_max_health(self, value):
        """ Метод, чтобы установить максимальное количество здоровья """
        if value > 0:
            self.max_health = value
        elif value == 0:
            self.is_alive = False
        return False

    def get_procent(self):
        """ Метод для получения текущего процента здоровья (в виде от 0.0 до 1.0)"""
        return (self.current_health / self.max_health)
