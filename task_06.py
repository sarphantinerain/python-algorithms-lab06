class Vector:
    def __init__(self, *args):
        self.values = [value for value in args if type(value) is int]

    def __str__(self):
        if not self.values:
            return "Пустой вектор"
        return "Вектор(" + ", ".join(map(str, sorted(self.values))) + ")"
