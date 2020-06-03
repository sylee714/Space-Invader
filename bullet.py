class Bullet():
    def __init__(self, img, x, y):
        self.img = img
        self.x = x
        self.y = y
        self.fired = False

    def set_x(self, x):
        self.x = x

    def set_y(self, y):
        self.y = y

    def set_fired(self, fired):
        self.fired = fired
