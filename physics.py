import random

world_w = 200
world_h = 150
empty = (0, 0, 0)
White = (255, 255, 255)
steam = (255, 255, 253)
snow = (255, 255, 254)
water = (0, 0, 255)
acid = (0, 255, 0)
plasm = (255, 0, 255)
fire = (255, 0, 0)
petrol = (73, 77, 43)
boom = (254, 0, 0)
lava = (139, 0, 0)
sand = (255, 255, 0)
wood = (150, 111, 51)
stone = (80, 80, 80)
iron = (80, 80, 59)
powder = (70, 70, 70)
smoke = (128, 128, 128)
phantom = [water, empty, smoke, fire, plasm, boom, lava, petrol, acid]
gorach = [fire, plasm, lava, boom]
rastvor = [wood, sand, iron, stone]
spc = [wood]
dynamic = [steam, snow, water, acid, plasm, fire, petrol, boom, lava, sand, powder, smoke]

# Цветовые варианты для каждого вещества
sand_colors = [(255, 255, 0), (255, 230, 0), (240, 220, 70), (210, 180, 40)]
water_colors = [(0, 0, 255), (30, 144, 255), (0, 105, 148), (70, 130, 180)]
stone_colors = [(80, 80, 80), (105, 105, 105), (169, 169, 169), (120, 120, 120)]
wood_colors = [(150, 111, 51), (139, 69, 19), (160, 120, 80), (101, 67, 33)]
fire_colors = [(255, 0, 0), (255, 69, 0), (255, 140, 0), (255, 215, 0)]
lava_colors = [(139, 0, 0), (178, 34, 34), (205, 92, 92), (255, 99, 71)]
snow_colors = [(255, 255, 254), (240, 248, 255), (245, 245, 245), (255, 250, 250)]
steam_colors = [(255, 255, 253), (230, 230, 230), (240, 240, 240), (220, 220, 220)]
smoke_colors = [(128, 128, 128), (140, 140, 140), (160, 160, 160), (180, 180, 180)]
plasm_colors = [(255, 0, 255), (200, 0, 200), (255, 100, 255), (180, 0, 180)]
petrol_colors = [(73, 77, 43), (85, 90, 50), (65, 70, 40), (95, 100, 55)]
acid_colors = [(0, 255, 0), (50, 255, 50), (0, 200, 0), (100, 255, 100)]
powder_colors = [(70, 70, 70), (80, 80, 80), (90, 90, 90), (100, 100, 100)]
iron_colors = [(80, 80, 59), (90, 90, 65), (70, 70, 55), (100, 100, 75)]
boom_colors = [(254, 0, 0), (255, 50, 50), (240, 0, 0), (255, 100, 100)]

world = {}  # (x, y): Substance object


class Substance:  # все вещества
    def __init__(self, x, y, color):
        self.t = 0
        self.r = 10
        self.x = x
        self.y = y
        self.color = color
        self.fake_color = color

    def action(self):
        if self.r <= 0:
            remove_substance(self.x, self.y)

    def get_color(self):
        return self.color

    def move_to(self, new_x, new_y):
        if (self.x, self.y) in world and world[(self.x, self.y)] is self:
            del world[(self.x, self.y)]

        self.x = new_x
        self.y = new_y
        world[(new_x, new_y)] = self


class Dust(Substance):  # песок, зола
    def __init__(self, x, y, color):
        super().__init__(x, y, color)

    def action(self):
        super().action()
        x, y = self.x, self.y

        down = world.get((x, y + 1))
        down_left = world.get((x - 1, y + 1))
        down_right = world.get((x + 1, y + 1))

        down_color = down.get_color() if down else empty
        down_left_color = down_left.get_color() if down_left else empty
        down_right_color = down_right.get_color() if down_right else empty

        if down_color in phantom:
            if down:
                down.move_to(x, y)
            self.move_to(x, y - 1)
        elif down_left_color in phantom and down_right_color in phantom:
            r = random.randint(1, 2)
            if r == 1:
                if down_left:
                    down_left.move_to(x, y)
                self.move_to(x - 1, y - 1)
            else:
                if down_right:
                    down_right.move_to(x, y)
                self.move_to(x + 1, y - 1)
        elif down_left_color in phantom:
            if down_left:
                down_left.move_to(x, y)
            self.move_to(x - 1, y - 1)
        elif down_right_color in phantom:
            if down_right:
                down_right.move_to(x, y)
            self.move_to(x + 1, y - 1)


class Solid(Substance):  # камень, кирпич, дерево, железо и тд
    def __init__(self, x, y, color):
        super().__init__(x, y, color)

    def action(self):
        super().action()


class Liquid(Substance):  # вода, бензин
    def __init__(self, x, y, color):
        super().__init__(x, y, color)
        self.timer = 3

    def action(self):
        super().action()
        x, y = self.x, self.y

        down = world.get((x, y - 1))
        down_color = down.get_color() if down else empty

        if down_color != self.color and down_color in phantom[1:]:
            self.move_to(x, y - 1)
            if down:
                down.move_to(x, y)
            return

        directions = [-1, 1]
        random.shuffle(directions)
        for dx in directions:
            side = world.get((x + dx, y))
            side_color = side.get_color() if side else empty

            if side_color in phantom[1:]:
                if side:
                    side.move_to(x, y)
                self.move_to(x + dx, y)
                return
        self.timer -= 1


class Gas(Substance):  # дым, пар, огонь, плазма
    def __init__(self, x, y, color):
        super().__init__(x, y, color)

    def action(self):
        super().action()
        x, y = self.x, self.y
        up = world.get((x, y + 1))
        up_color = up.get_color() if up else empty

        directions = [-1, 1]
        random.shuffle(directions)

        for dx in directions:
            side = world.get((x + dx, y + 1))
            side_color = side.get_color() if side else empty

            if side_color in phantom:
                self.move_to(x + dx, y + 1)
                if side:
                    side.move_to(x, y)
                return

        if up_color in phantom:
            self.move_to(x, y + 1)
            if up:
                up.move_to(x, y)
            return

        for dx in directions:
            side = world.get((x + dx, y))
            side_color = side.get_color() if side else empty

            if side_color in phantom:
                self.move_to(x + dx, y)
                if side:
                    side.move_to(x, y)
                return


class Sand(Dust):
    def __init__(self, x, y):
        super().__init__(x, y, color=sand)
        self.fake_color = random.choice(sand_colors)

    def action(self):
        if self.t >= 3000000:
            remove_substance(self.x, self.y)
            add_substance(Lava(self.x, self.y, sand))
            return
        super().action()


class Water(Liquid):
    def __init__(self, x, y):
        super().__init__(x, y, color=water)
        self.fake_color = random.choice(water_colors)

    def action(self):
        if self.t >= 30:
            remove_substance(self.x, self.y)
            add_substance(Steam(self.x, self.y))
            return
        if self.timer <= 0:
            self.timer = 3
            self.fake_color = random.choice(water_colors)
        super().action()


class Stone(Solid):
    def __init__(self, x, y):
        super().__init__(x, y, color=stone)
        self.fake_color = random.choice(stone_colors)

    def action(self):
        super().action()
        if self.t >= 3000000:
            remove_substance(self.x, self.y)
            add_substance(Lava(self.x, self.y, stone))


class Smoke(Gas):
    def __init__(self, x, y):
        super().__init__(x, y, color=smoke)
        self.fake_color = random.choice(smoke_colors)
        self.life = random.randint(50, 150)

    def action(self):
        self.life -= 1
        if self.life <= 0:
            remove_substance(self.x, self.y)
            return
        super().action()


class Wood(Solid):
    def __init__(self, x, y):
        super().__init__(x, y, color=wood)
        self.fake_color = random.choice(wood_colors)

    def action(self):
        super().action()
        if self.t > 30:
            x, y = self.x, self.y
            remove_substance(x, y)
            r = random.randint(1, 10)
            if r == 1:
                add_substance(Smoke(x, y))
            else:
                add_substance(Fire(x, y))


class Fire(Gas):
    def __init__(self, x, y):
        super().__init__(x, y, color=fire)
        self.fake_color = random.choice(fire_colors)
        self.life = random.randint(10, 30)
        self.t = 3

    def action(self):
        x, y = self.x, self.y
        self.life -= 1
        if self.life <= 0:
            remove_substance(x, y)
            return
        if self.t <= 0:
            remove_substance(x, y)
            return

        directions = [(0, -1), (1, 0), (-1, 0), (0, 1), (1, 1), (-1, 1), (1, -1), (-1, -1)]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if (nx, ny) in world:
                if world[(nx, ny)].color not in gorach:
                    world[(nx, ny)].t += self.t
                    if world[(nx, ny)].color == water:
                        remove_substance(x, y)
                        return
        down = world.get((x, y - 1))
        down_color = down.get_color() if down else empty
        if down_color not in spc:
            super().action()


class Steam(Gas):
    def __init__(self, x, y, parent=steam):
        super().__init__(x, y, color=parent)
        self.fake_color = random.choice(steam_colors)
        self.life = random.randint(150, 300)

    def action(self):
        self.life -= 1
        if self.life <= 0:
            remove_substance(self.x, self.y)
            if self.color == steam:
                add_substance(Water(self.x, self.y))
            else:
                add_substance(Acid(self.x, self.y))
            return
        super().action()


class Plasm(Gas):
    def __init__(self, x, y):
        super().__init__(x, y, color=plasm)
        self.fake_color = random.choice(plasm_colors)
        self.life = random.randint(20, 40)
        self.t = 1000000

    def action(self):
        x, y = self.x, self.y
        self.life -= 1
        if self.life <= 0:
            remove_substance(x, y)
            return
        super().action()

        directions = [(0, -1), (1, 0), (-1, 0), (0, 1), (1, 1), (-1, 1), (1, -1), (-1, -1)]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if (nx, ny) in world:
                if world[(nx, ny)].color not in gorach:
                    world[(nx, ny)].t += self.t


class Lava(Liquid):
    def __init__(self, x, y, parent_color):
        super().__init__(x, y, color=lava)
        self.fake_color = random.choice(lava_colors)
        self.t = random.randint(200, 350)
        self.parent_color = parent_color

    def action(self):
        x, y = self.x, self.y
        self.t -= 1
        if self.t <= 0:
            remove_substance(self.x, self.y)
            if self.parent_color == iron:
                add_substance(Iron(self.x, self.y))
                return
            add_substance(Stone(self.x, self.y))
            return
        super().action()

        directions = [(0, -1), (1, 0), (-1, 0), (0, 1), (1, 1), (-1, 1), (1, -1), (-1, -1)]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if (nx, ny) in world:
                if world[(nx, ny)].color not in gorach:
                    world[(nx, ny)].t += self.t
        if self.timer <= 0:
            self.timer = 7
            self.fake_color = random.choice(lava_colors)


class Powder(Dust):
    def __init__(self, x, y):
        super().__init__(x, y, color=powder)
        self.fake_color = random.choice(powder_colors)

    def action(self):
        x, y = self.x, self.y
        if self.t >= 3:
            remove_substance(x, y)
            add_substance(Boom(x, y))
            directions = [(0, -1), (1, 0), (-1, 0), (0, 1), (1, 1), (-1, 1), (1, -1), (-1, -1)]
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if (nx, ny) in world:
                    if world[(nx, ny)].color == powder:
                        x, y = nx, ny
                        remove_substance(x, y)
                        add_substance(Boom(x, y))
                        add_substance(Boom(x, y))
            return
        super().action()


class Boom(Gas):
    def __init__(self, x, y):
        super().__init__(x, y, color=boom)
        self.fake_color = random.choice(boom_colors)
        self.dir = [random.randint(-1, 1), random.randint(-1, 1)]
        self.t = random.randint(30, 50)

    def action(self):
        x, y = self.x, self.y
        self.t -= 1
        if self.t <= 0:
            remove_substance(x, y)
            return

        new_x = x + self.dir[0]
        new_y = y + self.dir[1]

        if new_x <= 0 or new_x >= world_w - 1 or new_y <= 0 or new_y >= world_h - 1:
            remove_substance(x, y)
            return
        side = world.get((x + self.dir[0], y + self.dir[1]))
        side_color = side.get_color() if side else empty
        if side_color not in [empty]:
            remove_substance(x + self.dir[0], y + self.dir[1])
            self.t -= 5
        self.move_to(x + self.dir[0], y + self.dir[1])
        directions = [(0, -1), (1, 0), (-1, 0), (0, 1), (1, 1), (-1, 1), (1, -1), (-1, -1)]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if (nx, ny) in world:
                if world[(nx, ny)].color not in gorach:
                    world[(nx, ny)].t += self.t
        directions = [(0, -1), (1, 0), (-1, 0), (0, 1)]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if (nx, ny) in world:
                if world[(nx, ny)].color != White:
                    remove_substance(nx, ny)
                    add_substance(Fire(nx, ny))


class Petrol(Liquid):
    def __init__(self, x, y):
        super().__init__(x, y, color=petrol)
        self.fake_color = random.choice(petrol_colors)

    def action(self):
        x, y = self.x, self.y
        if self.t >= 3:
            remove_substance(x, y)
            add_substance(Boom(x, y))
            directions = [(0, -1), (1, 0), (-1, 0), (0, 1), (1, 1), (-1, 1), (1, -1), (-1, -1)]
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if (nx, ny) in world:
                    if world[(nx, ny)].color == powder:
                        x, y = nx, ny
                        remove_substance(x, y)
                        add_substance(Boom(x, y))
                        add_substance(Boom(x, y))
            return
        super().action()
        if self.timer <= 0:
            self.timer = 5
            self.fake_color = random.choice(petrol_colors)


class Acid(Liquid):
    def __init__(self, x, y):
        super().__init__(x, y, color=acid)
        self.fake_color = random.choice(acid_colors)
        self.life = 1

    def action(self):
        x, y = self.x, self.y
        if self.life <= 0:
            remove_substance(x, y)
            return
        if self.t >= 10:
            remove_substance(x, y)
            add_substance(Steam(x, y, acid))
            return

        down = world.get((x, y - 1))
        if down and down.get_color() in rastvor:
            down.r -= 1
            return

        directions = [-1, 1]
        random.shuffle(directions)
        for dx in directions:
            side = world.get((x + dx, y))
            if side and side.get_color() in rastvor:
                side.r -= 1
                self.life -= 1
                return
        if self.timer <= 0:
            self.timer = 2
            self.fake_color = random.choice(acid_colors)
        super().action()


class Iron(Solid):
    def __init__(self, x, y):
        super().__init__(x, y, color=iron)
        self.fake_color = random.choice(iron_colors)

    def action(self):

        x, y = self.x, self.y
        if self.t > 1000000:
            remove_substance(self.x, self.y)
            add_substance(Lava(self.x, self.y, iron))
            return
        if self.t >= 3:
            directions = [(0, 1)]
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if (nx, ny) in world:
                    if world[(nx, ny)].color not in gorach:
                        world[(nx, ny)].t += self.t
        self.t -= 3
        super().action()


class Snow(Dust):
    def __init__(self, x, y):
        super().__init__(x, y, color=snow)
        self.fake_color = random.choice(snow_colors)
        self.t = -random.randint(150, 250)

    def action(self):
        x, y = self.x, self.y
        self.t += 1
        if self.t >= 0:
            remove_substance(x, y)
            add_substance(Water(x, y))
            return
        directions = [(0, -1), (1, 0), (-1, 0), (0, 1), (1, 1), (-1, 1), (1, -1), (-1, -1)]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if (nx, ny) in world:
                if world[(nx, ny)].color not in [empty, snow, White, water]:
                    if world[(nx, ny)].t >= 0:
                        world[(nx, ny)].t += self.t
                        self.t += 30
        super().action()


def add_substance(substance):
    world[(substance.x, substance.y)] = substance


def remove_substance(x, y):
    if (x, y) in world:
        del world[(x, y)]

