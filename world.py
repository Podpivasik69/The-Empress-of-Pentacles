# кароче тут будет класс мира и ещё много разной фигни

class World:
    def __init__(self):
        self.substance_world = {} # список веществ, {(x, y): substance_object, ...}
        self.entity_world = {} # список сущностей, {(x, y): entity_object, ...}

    def remove_substance(self, x, y):
        if (x, y) in self.substance_world:
            del self.substance_world[(x, y)]

    def add_substance(self, substance):
        self.substance_world[(substance.x, substance.y)] = substance

    def remove_entity(self, x, y):
        if (x, y) in self.entity_world:
            del self.entity_world[(x, y)]

    def add_entity(self, entity):
        self.entity_world[(entity.x, entity.y)] = entity


world = World()