class Vector:
    def __init__(self, *args):
        self.values = sorted(value for value in args if type(value) is int)

    def __str__(self):
        if not self.values:
            return "Пустой вектор"
        return "Вектор(" + ", ".join(map(str, self.values)) + ")"

    def __add__(self, other):
        if type(other) is int:
            return Vector(*(value + other for value in self.values))
        if isinstance(other, Vector):
            if len(self.values) != len(other.values):
                print("Сложение векторов разной длины недопустимо")
                return None
            return Vector(*(a + b for a, b in zip(self.values, other.values)))
        print(f"Вектор нельзя сложить с {other}")
        return None

    def __mul__(self, other):
        if type(other) is int:
            return Vector(*(value * other for value in self.values))
        if isinstance(other, Vector):
            if len(self.values) != len(other.values):
                print("Умножение векторов разной длины недопустимо")
                return None
            return Vector(*(a * b for a, b in zip(self.values, other.values)))
        print(f"Вектор нельзя умножать с {other}")
        return None
