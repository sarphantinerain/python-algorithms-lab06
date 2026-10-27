"""Проверки всех задач лабораторной: python -m unittest -v."""
import contextlib
import importlib.util
import io
from pathlib import Path
import unittest


def capture(action):
    stream = io.StringIO()
    with contextlib.redirect_stdout(stream):
        result = action()
    return result, stream.getvalue()


def expect_error(error_type, message, action):
    try:
        capture(action)
    except error_type as error:
        assert str(error) == message, (str(error), message)
    else:
        raise AssertionError(f"Ожидалось исключение {error_type.__name__}")


class Lab06Tests(unittest.TestCase):
    """Каждая задача загружается отдельно, без конфликта имен классов."""

    def test_task_01(self):
        from task_01 import Point, ArgumentError
        a, b = Point(), Point()
        a.set_coordinates(0, 0)
        b.set_coordinates(3, 4)
        assert (b.x, b.y) == (3, 4)
        assert a.get_distance(b) == 5
        assert a.get_distance(b, "Чебышева") == 4
        assert a.get_distance(b, "городских кварталов") == 7
        assert a.get_distance(a) == 0
        assert b.get_distance(a) == a.get_distance(b)
        expect_error(ArgumentError, "Передана не точка", lambda: a.get_distance(3))
        expect_error(ValueError, "Неизвестный вид расстояния", lambda: a.get_distance(b, "unknown"))

    def test_task_02(self):
        from task_02 import Robot
        Robot.population = 0
        assert Robot.population == 0
        first, output = capture(lambda: Robot("R2-D2"))
        assert output == "Робот R2-D2 был создан\n"
        second, _ = capture(lambda: Robot("C-3PO"))
        assert first.name == "R2-D2" and Robot.population == 2
        assert capture(first.say_hello)[1] == "Робот R2-D2 приветствует тебя, особь человеческого рода\n"
        assert capture(Robot.how_many)[1] == "2, вот сколько нас еще осталось\n"
        assert capture(first.destroy)[1] == "Робот R2-D2 был уничтожен\n"
        assert Robot.population == 1
        capture(second.destroy)
        assert Robot.population == 0

    def test_task_03(self):
        from task_03 import Stack
        stack = Stack()
        assert stack.values == [] and stack.is_empty() and stack.size() == 0
        assert capture(stack.pop) == (None, "Empty Stack\n")
        assert capture(stack.peek) == (None, "Empty Stack\n")
        assert stack.push("first") is None
        stack.push("second")
        assert stack.peek() == "second" and stack.size() == 2
        assert stack.pop() == "second" and stack.pop() == "first"
        assert stack.is_empty()
        assert Stack().values is not stack.values

    def test_task_04(self):
        from task_04 import UserMail
        user = UserMail("student", "old@example.org")
        assert user.login == "student" and user.email == "old@example.org"
        user.email = "new@example.ru"
        assert user.get_email() == "new@example.ru"
        for invalid in ["no-at.ru", "two@@example.ru", "a.b@example", None]:
            assert capture(lambda: setattr(user, "email", invalid))[1] == "Ошибочная почта\n"
            assert user.email == "new@example.ru"
        assert user._UserMail__email == "new@example.ru"

    def test_task_05(self):
        from task_05 import Money
        money = Money(12, 35)
        assert money.total_cents == 1235 and money.dollars == 12 and money.cents == 35
        money.dollars = 7
        assert money.total_cents == 735 and money.cents == 35
        money.cents = 99
        assert money.total_cents == 799 and money.dollars == 7
        assert str(money) == "Ваше состояние составляет 7 долларов 99 центов"
        for name, values in [("dollars", [-1, 1.5, "2", True]), ("cents", [-1, 100, 1.5, True])]:
            for value in values:
                assert capture(lambda: setattr(money, name, value))[1] == f"Error {name}\n"
                assert money.total_cents == 799
        money.dollars = 0
        money.cents = 0
        assert vars(money) == {"total_cents": 0}

    def test_task_06(self):
        from task_06 import Vector
        vector = Vector(3, "4", 1, 2.5, -2, True, 1)
        assert vector.values == [3, 1, -2, 1]
        assert str(vector) == "Вектор(-2, 1, 1, 3)"
        assert vector.values == [3, 1, -2, 1]
        assert str(Vector()) == "Пустой вектор"
        assert str(Vector(False, None, 1.0)) == "Пустой вектор"

    def test_task_07(self):
        from task_07 import Vector
        vector = Vector(3, -1, 2, "x", True, 1.5)
        assert vector.values == [-1, 2, 3]
        assert str(vector) == "Вектор(-1, 2, 3)"
        assert str(Vector()) == "Пустой вектор"
        assert (vector + 2).values == [1, 4, 5]
        assert (vector * -2).values == [-6, -4, 2]
        assert (vector + Vector(1, 4, 5)).values == [0, 6, 8]
        assert (vector * Vector(-3, 0, 2)).values == [0, 3, 6]
        assert (Vector() + Vector()).values == []
        assert capture(lambda: vector + Vector(1)) == (None, "Сложение векторов разной длины недопустимо\n")
        assert capture(lambda: vector * Vector(1)) == (None, "Умножение векторов разной длины недопустимо\n")
        assert capture(lambda: vector + "x") == (None, "Вектор нельзя сложить с x\n")
        assert capture(lambda: vector * "x") == (None, "Вектор нельзя умножать с x\n")
        assert vector.values == [-1, 2, 3]

    def test_task_08(self):
        from task_08 import ChessPlayer
        player = ChessPlayer("Иван", "Иванов", 2000)
        assert (player.name, player.surname, player.rating) == ("Иван", "Иванов", 2000)
        assert (player == 2000) is True and (player == 1999) is False
        assert (player > 1999) is True and (player > 2000) is False
        assert (player < 2001) is True and (player < 2000) is False
        assert (player == ChessPlayer("А", "Б", 2000)) is True
        assert (player > ChessPlayer("А", "Б", 1999)) is True
        assert (player < ChessPlayer("А", "Б", 2001)) is True
        for method in [player.__eq__, player.__lt__, player.__gt__]:
            assert method("2000") == "Невозможно выполнить сравнение"

    def test_task_09(self):
        from task_09 import Transport, Car, Boat, Plane
        transport = Transport("A", 100)
        assert transport.kind is None
        assert str(transport) == "Тип транспорта None марки A может развить скорость 100 км/ч"
        car = Car("B", 180, 10000, 20)
        assert isinstance(car, Transport) and car.kind == "Car" and car.mileage == 10000
        assert car.gasoline == "Осталось бензина на 20 км"
        assert capture(lambda: setattr(car, "gasoline", 5))[1] == "Объем топлива увеличен на 5 л и составляет 25 л\n"
        for invalid in [2.5, "5", True]:
            assert capture(lambda: setattr(car, "gasoline", invalid))[1] == "Ошибка заправки автомобиля\n"
            assert car.gasoline == "Осталось бензина на 25 км"
        assert car._Car__gasoline_residue == 25
        for boat in [Boat("C", 40, "Иван"), Boat("C", 40, "Boat", "Иван"), Boat("C", 40, owners_name="Иван")]:
            assert boat.kind == "Boat" and boat.owners_name == "Иван"
            assert str(boat) == "Этой лодкой марки C владеет Иван"
        plane = Plane("D", 900, 180)
        assert plane.kind == "Plane" and plane.capacity == 180
        assert str(plane) == "Самолет марки D вмещает в себя 180 людей"

    def test_task_10(self):
        from task_10 import Initialization, Vegetarian, MeatEater, SweetTooth
        vegetarian = Vegetarian(10, ["овощи"])
        meat = MeatEater(20, ["рыба"])
        sweet = SweetTooth(15, ["торт"])
        assert str(vegetarian) == "10 людей предпочитают не есть мясо! Они предпочитают ['овощи']"
        assert str(meat) == "20 мясоедов! Помимо мяса они едят еще и ['рыба']"
        assert str(sweet) == "Сладкоежек 15. Их любимая еда: ['торт']"
        assert isinstance(sweet, Initialization)
        assert (sweet == 15) is True and (sweet == 10) is False
        assert (sweet < 16) is True and (sweet < 15) is False
        assert (sweet > 14) is True and (sweet > 15) is False
        assert (sweet > vegetarian) is True and (sweet < meat) is True
        assert (sweet == Vegetarian(15, [])) is True
        assert (sweet == MeatEater(15, [])) is True
        for method in [sweet.__eq__, sweet.__lt__, sweet.__gt__]:
            assert method("x") == "Невозможно сравнить количество сладкоежек с x"
        for cls in [Initialization, Vegetarian, MeatEater, SweetTooth]:
            invalid, output = capture(lambda: cls([23], []))
            assert output == "Количество людей должно быть целым числом\n"
            assert not hasattr(invalid, "capacity") and not hasattr(invalid, "food")

    def test_task_11(self):
        from task_11 import Wallet
        for currency, error, message in [
            (123, TypeError, "Неверный тип валюты"),
            ("US", NameError, "Неверная длина названия валюты"),
            ("usd", ValueError, "Название должно состоять только из заглавных букв"),
            ("U1D", ValueError, "Название должно состоять только из заглавных букв"),
        ]:
            expect_error(error, message, lambda: Wallet(currency, 0))
        first, second = Wallet("USD", 100), Wallet("USD", 30)
        assert (first == Wallet("USD", 100)) is True
        assert (first == second) is False
        total, difference = first + second, first - second
        assert isinstance(total, Wallet) and total.currency == "USD" and total.balance == 130
        assert difference.currency == "USD" and difference.balance == 70
        assert first.balance == 100 and second.balance == 30 and total is not first
        expect_error(TypeError, "Wallet не поддерживает сравнение с 3", lambda: first == 3)
        expect_error(ValueError, "Нельзя сравнить разные валюты", lambda: first == Wallet("EUR", 100))
        for other in [3, Wallet("EUR", 30)]:
            expect_error(ValueError, "Данная операция запрещена", lambda: first + other)
            expect_error(ValueError, "Данная операция запрещена", lambda: first - other)

    def test_task_12(self):
        from task_12 import Vector
        vector = Vector(3, "4", 1, 2.5, -2, True, 1)
        assert vector.values == [3, 1, -2, 1]
        assert str(vector) == "Вектор(-2, 1, 1, 3)"
        assert vector.values == [3, 1, -2, 1]
        assert str(Vector()) == "Пустой вектор"
        assert str(Vector(False, None, 1.0)) == "Пустой вектор"

    def test_task_13(self):
        from task_13 import Vector
        vector = Vector(3, -1, 2, "x", True, 1.5)
        assert vector.values == [-1, 2, 3]
        assert str(vector) == "Вектор(-1, 2, 3)"
        assert str(Vector()) == "Пустой вектор"
        assert (vector + 2).values == [1, 4, 5]
        assert (vector * -2).values == [-6, -4, 2]
        assert (vector + Vector(1, 4, 5)).values == [0, 6, 8]
        assert (vector * Vector(-3, 0, 2)).values == [0, 3, 6]
        assert (Vector() + Vector()).values == []
        assert capture(lambda: vector + Vector(1)) == (None, "Сложение векторов разной длины недопустимо\n")
        assert capture(lambda: vector * Vector(1)) == (None, "Умножение векторов разной длины недопустимо\n")
        assert capture(lambda: vector + "x") == (None, "Вектор нельзя сложить с x\n")
        assert capture(lambda: vector * "x") == (None, "Вектор нельзя умножать с x\n")
        assert vector.values == [-1, 2, 3]

    def test_task_14(self):
        from task_14 import ChessPlayer
        player = ChessPlayer("Иван", "Иванов", 2000)
        assert (player.name, player.surname, player.rating) == ("Иван", "Иванов", 2000)
        assert (player == 2000) is True and (player == 1999) is False
        assert (player > 1999) is True and (player > 2000) is False
        assert (player < 2001) is True and (player < 2000) is False
        assert (player == ChessPlayer("А", "Б", 2000)) is True
        assert (player > ChessPlayer("А", "Б", 1999)) is True
        assert (player < ChessPlayer("А", "Б", 2001)) is True
        for method in [player.__eq__, player.__lt__, player.__gt__]:
            assert method("2000") == "Невозможно выполнить сравнение"

    def test_task_15(self):
        from task_15 import Transport, Car, Boat, Plane
        transport = Transport("A", 100)
        assert transport.kind is None
        assert str(transport) == "Тип транспорта None марки A может развить скорость 100 км/ч"
        car = Car("B", 180, 10000, 20)
        assert isinstance(car, Transport) and car.kind == "Car" and car.mileage == 10000
        assert car.gasoline == "Осталось бензина на 20 км"
        assert capture(lambda: setattr(car, "gasoline", 5))[1] == "Объем топлива увеличен на 5 л и составляет 25 л\n"
        for invalid in [2.5, "5", True]:
            assert capture(lambda: setattr(car, "gasoline", invalid))[1] == "Ошибка заправки автомобиля\n"
            assert car.gasoline == "Осталось бензина на 25 км"
        assert car._Car__gasoline_residue == 25
        for boat in [Boat("C", 40, "Иван"), Boat("C", 40, "Boat", "Иван"), Boat("C", 40, owners_name="Иван")]:
            assert boat.kind == "Boat" and boat.owners_name == "Иван"
            assert str(boat) == "Этой лодкой марки C владеет Иван"
        plane = Plane("D", 900, 180)
        assert plane.kind == "Plane" and plane.capacity == 180
        assert str(plane) == "Самолет марки D вмещает в себя 180 людей"

    def test_task_16(self):
        from task_16 import Initialization, Vegetarian, MeatEater, SweetTooth
        vegetarian = Vegetarian(10, ["овощи"])
        meat = MeatEater(20, ["рыба"])
        sweet = SweetTooth(15, ["торт"])
        assert str(vegetarian) == "10 людей предпочитают не есть мясо! Они предпочитают ['овощи']"
        assert str(meat) == "20 мясоедов! Помимо мяса они едят еще и ['рыба']"
        assert str(sweet) == "Сладкоежек 15. Их любимая еда: ['торт']"
        assert isinstance(sweet, Initialization)
        assert (sweet == 15) is True and (sweet == 10) is False
        assert (sweet < 16) is True and (sweet < 15) is False
        assert (sweet > 14) is True and (sweet > 15) is False
        assert (sweet > vegetarian) is True and (sweet < meat) is True
        assert (sweet == Vegetarian(15, [])) is True
        assert (sweet == MeatEater(15, [])) is True
        for method in [sweet.__eq__, sweet.__lt__, sweet.__gt__]:
            assert method("x") == "Невозможно сравнить количество сладкоежек с x"
        for cls in [Initialization, Vegetarian, MeatEater, SweetTooth]:
            invalid, output = capture(lambda: cls([23], []))
            assert output == "Количество людей должно быть целым числом\n"
            assert not hasattr(invalid, "capacity") and not hasattr(invalid, "food")

    def test_task_17(self):
        from task_17 import Wallet
        for currency, error, message in [
            (123, TypeError, "Неверный тип валюты"),
            ("US", NameError, "Неверная длина названия валюты"),
            ("usd", ValueError, "Название должно состоять только из заглавных букв"),
            ("U1D", ValueError, "Название должно состоять только из заглавных букв"),
        ]:
            expect_error(error, message, lambda: Wallet(currency, 0))
        first, second = Wallet("USD", 100), Wallet("USD", 30)
        assert (first == Wallet("USD", 100)) is True
        assert (first == second) is False
        total, difference = first + second, first - second
        assert isinstance(total, Wallet) and total.currency == "USD" and total.balance == 130
        assert difference.currency == "USD" and difference.balance == 70
        assert first.balance == 100 and second.balance == 30 and total is not first
        expect_error(TypeError, "Wallet не поддерживает сравнение с 3", lambda: first == 3)
        expect_error(ValueError, "Нельзя сравнить разные валюты", lambda: first == Wallet("EUR", 100))
        for other in [3, Wallet("EUR", 30)]:
            expect_error(ValueError, "Данная операция запрещена", lambda: first + other)
            expect_error(ValueError, "Данная операция запрещена", lambda: first - other)

    def test_task_18(self):
        from task_18 import Transport, Car, Boat, Plane
        transport = Transport("A", 100)
        assert transport.kind is None
        assert str(transport) == "Тип транспорта None марки A может развить скорость 100 км/ч"
        car = Car("B", 180, 10000, 20)
        assert isinstance(car, Transport) and car.kind == "Car" and car.mileage == 10000
        assert car.gasoline == "Осталось бензина на 20 км"
        assert capture(lambda: setattr(car, "gasoline", 5))[1] == "Объем топлива увеличен на 5 л и составляет 25 л\n"
        for invalid in [2.5, "5", True]:
            assert capture(lambda: setattr(car, "gasoline", invalid))[1] == "Ошибка заправки автомобиля\n"
            assert car.gasoline == "Осталось бензина на 25 км"
        assert car._Car__gasoline_residue == 25
        for boat in [Boat("C", 40, "Иван"), Boat("C", 40, "Boat", "Иван"), Boat("C", 40, owners_name="Иван")]:
            assert boat.kind == "Boat" and boat.owners_name == "Иван"
            assert str(boat) == "Этой лодкой марки C владеет Иван"
        plane = Plane("D", 900, 180)
        assert plane.kind == "Plane" and plane.capacity == 180
        assert str(plane) == "Самолет марки D вмещает в себя 180 людей"

    def test_all_notebooks(self):
        import json
        root = Path(__file__).resolve().parent
        notebooks = sorted(root.glob("task-*.ipynb"))
        self.assertEqual(len(notebooks), 19)
        for path in notebooks:
            with self.subTest(notebook=path.name):
                notebook = json.loads(path.read_text(encoding="utf-8"))
                namespace = {}
                for cell in notebook["cells"]:
                    if cell["cell_type"] == "code":
                        source = "".join(cell["source"])
                        self.assertTrue(source.strip())
                        exec(compile(source, path.name, "exec"), namespace)


if __name__ == "__main__":
    unittest.main()
