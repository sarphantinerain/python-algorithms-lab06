class Initialization:
    def __init__(self, capacity, food):
        if type(capacity) is not int:
            print("Количество людей должно быть целым числом")
            return
        self.capacity = capacity
        self.food = food


class Vegetarian(Initialization):
    def __init__(self, capacity, food):
        super().__init__(capacity, food)

    def __str__(self):
        return (f"{self.capacity} людей предпочитают не есть мясо! "
                f"Они предпочитают {self.food}")


class MeatEater(Initialization):
    def __init__(self, capacity, food):
        super().__init__(capacity, food)

    def __str__(self):
        return f"{self.capacity} мясоедов! Помимо мяса они едят еще и {self.food}"


class SweetTooth(Initialization):
    def __init__(self, capacity, food):
        super().__init__(capacity, food)

    def __str__(self):
        return f"Сладкоежек {self.capacity}. Их любимая еда: {self.food}"

    def __eq__(self, other):
        if type(other) is int:
            return self.capacity == other
        if isinstance(other, (Vegetarian, MeatEater)):
            return self.capacity == other.capacity
        return f"Невозможно сравнить количество сладкоежек с {other}"

    def __lt__(self, other):
        if type(other) is int:
            return self.capacity < other
        if isinstance(other, (Vegetarian, MeatEater)):
            return self.capacity < other.capacity
        return f"Невозможно сравнить количество сладкоежек с {other}"

    def __gt__(self, other):
        if type(other) is int:
            return self.capacity > other
        if isinstance(other, (Vegetarian, MeatEater)):
            return self.capacity > other.capacity
        return f"Невозможно сравнить количество сладкоежек с {other}"
