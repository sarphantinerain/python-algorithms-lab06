class UserMail:
    def __init__(self, login, email):
        self.login = login
        self.__email = email

    def get_email(self):
        return self.__email

    def set_email(self, email):
        if (isinstance(email, str) and email.count("@") == 1
                and "." in email.split("@")[1]):
            self.__email = email
        else:
            print("Ошибочная почта")

    email = property(get_email, set_email)
