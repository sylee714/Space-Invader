class Enemy():
    def __init__(self, img, x, y, x_change_value, y_change_value):
        self.img = img
        self.x = x
        self.y = y
        self.x_change_value = x_change_value
        self.y_change_value = y_change_value

    def set_x(self, x):
        self.x = x

    def set_y(self, y):
        self.y = y

    def set_x_change_value(self, x_change_value):
        self.x_change_value = x_change_value

    def set_y_change_value(self, y_change_value):
        self.y_change_value = y_change_value
