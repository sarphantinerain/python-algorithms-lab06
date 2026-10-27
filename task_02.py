class Robot:
    population = 0

    def __init__(self, name):
        self.name = name
        Robot.population += 1
        print(f"Робот {self.name} был создан")

    def destroy(self):
        Robot.population -= 1
        print(f"Робот {self.name} был уничтожен")

    def say_hello(self):
        print(f"Робот {self.name} приветствует тебя, особь человеческого рода")

    @classmethod
    def how_many(cls):
        print(f"{cls.population}, вот сколько нас еще осталось")
