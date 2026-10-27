from math import hypot


class ArgumentError(TypeError):
    """Ошибка типа аргумента, указанная в условии задания."""


class Point:
    def set_coordinates(self, x, y):
        self.x = x
        self.y = y

    def get_distance(self, other, dist="euclidean"):
        if not isinstance(other, Point):
            print("Передана не точка")
            raise ArgumentError("Передана не точка")

        dx = abs(self.x - other.x)
        dy = abs(self.y - other.y)
        if dist in ("euclidean", "евклидово"):
            return hypot(dx, dy)
        if dist in ("chebyshev", "Чебышева", "чебышева"):
            return max(dx, dy)
        if dist in ("manhattan", "городских кварталов"):
            return dx + dy
        raise ValueError("Неизвестный вид расстояния")
