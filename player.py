class Player():
    def __init__(self, img, x, y):
        self.img = img
        self.x = x
        self.y = y
        self.bullet_limit = 3
        self.bullet = []

    def load_bullet(self, bullet):
        self.bullet.append(bullet)

    def fire_bullet(self):
        return self.bullet.pop()

    def set_x(self, x):
        self.x = x

    def set_bullet_limit(self, limit):
        self.bullet_limit = limit
