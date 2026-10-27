"""Примеры применения классов лабораторной работы № 6."""
from task_01 import Point
from task_02 import Robot
from task_03 import Stack
from task_04 import UserMail
from task_05 import Money
from task_06 import Vector as SimpleVector
from task_07 import Vector
from task_08 import ChessPlayer
from task_09 import Transport, Car, Boat, Plane
from task_10 import Vegetarian, MeatEater, SweetTooth
from task_11 import Wallet


def main():
    print("Лабораторная работа № 6. ООП в Python")
    first, second = Point(), Point()
    first.set_coordinates(0, 0)
    second.set_coordinates(3, 4)
    for metric in ("евклидово", "Чебышева", "городских кварталов"):
        print(f"Расстояние ({metric}): {first.get_distance(second, metric)}")

    robot = Robot("R2-D2")
    robot.say_hello()
    Robot.how_many()
    robot.destroy()

    stack = Stack()
    stack.push("первый")
    stack.push("второй")
    print("Стек:", stack.peek(), stack.pop(), stack.size())

    user = UserMail("student", "student@example.org")
    user.email = "new@example.org"
    print("Почта:", user.email)

    money = Money(10, 50)
    money.dollars = 20
    money.cents = 75
    print(money)
    print(SimpleVector(3, "строка", 1, -2))
    vector = Vector(3, -1, 2)
    print("Сложение векторов:", vector + Vector(1, 4, 5))
    print("Умножение вектора:", vector * -2)

    player = ChessPlayer("Иван", "Иванов", 2000)
    print("Рейтинг выше 1900:", player > 1900)
    print(Transport("Транспорт", 100))
    car = Car("Автомобиль", 180, 10000, 20)
    car.gasoline = 10
    print(car, car.gasoline, sep="; ")
    print(Boat("Яхта", 40, "Иван"))
    print(Plane("Самолет", 900, 180))

    vegetarian = Vegetarian(10, ["овощи"])
    meat = MeatEater(20, ["рыба"])
    sweet = SweetTooth(15, ["торт"])
    print(vegetarian)
    print(meat)
    print(sweet)
    print("Сладкоежек больше, чем вегетарианцев:", sweet > vegetarian)

    wallet = Wallet("RUB", 1000) + Wallet("RUB", 250)
    print("Баланс после сложения:", wallet.balance, wallet.currency)


if __name__ == "__main__":
    main()
