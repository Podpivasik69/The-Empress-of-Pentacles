class Mana:
    def __init__(self, current_mana=100, max_mana=100, regen_rate=10.0):
        self.max_mana = max_mana
        self.current_mana = current_mana
        self.regen_rate = regen_rate

    def spend_mana(self, amount):
        """  Метод для расходау маны """
        # если отрицательно ничего не делаем
        if amount <= 0:
            return False
        # если возможная трата маны (хватает маны)
        if self.current_mana >= amount:
            self.current_mana -= amount
            return True

    def regen_mana(self, delta_time):
        """ Метод для востановления маны"""
        # если маны не максимум
        if self.current_mana < self.max_mana:
            self.current_mana = min(self.current_mana + self.regen_rate * delta_time, self.max_mana)

    def set_mana(self, value):
        """ установление количества маны"""
        value = max(0, min(value, self.max_mana))
        self.current_mana = value

    def set_max_mana(self, value):
        if value > 0:
            self.max_mana = value
