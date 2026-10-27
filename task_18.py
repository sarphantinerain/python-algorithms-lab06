class Transport:
    def __init__(self, brand, max_speed, kind=None):
        self.brand = brand
        self.max_speed = max_speed
        self.kind = kind

    def __str__(self):
        return (f"Тип транспорта {self.kind} марки {self.brand} "
                f"может развить скорость {self.max_speed} км/ч")


class Car(Transport):
    def __init__(self, brand, max_speed, mileage, gasoline_residue):
        super().__init__(brand, max_speed, "Car")
        self.mileage = mileage
        self.__gasoline_residue = gasoline_residue

    @property
    def gasoline(self):
        return f"Осталось бензина на {self.__gasoline_residue} км"

    @gasoline.setter
    def gasoline(self, value):
        if type(value) is int:
            self.__gasoline_residue += value
            print(f"Объем топлива увеличен на {value} л "
                  f"и составляет {self.__gasoline_residue} л")
        else:
            print("Ошибка заправки автомобиля")


class Boat(Transport):
    def __init__(self, brand, max_speed, kind="Boat", owners_name=None):
        # Поддерживаются Boat(brand, speed, owner) и явный аргумент kind.
        if owners_name is None:
            owners_name = kind
        super().__init__(brand, max_speed, "Boat")
        self.owners_name = owners_name

    def __str__(self):
        return f"Этой лодкой марки {self.brand} владеет {self.owners_name}"


class Plane(Transport):
    def __init__(self, brand, max_speed, capacity):
        super().__init__(brand, max_speed, "Plane")
        self.capacity = capacity

    def __str__(self):
        return f"Самолет марки {self.brand} вмещает в себя {self.capacity} людей"
