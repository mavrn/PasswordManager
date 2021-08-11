import random
import string

SPECIAL_CHARACTERS = "!!___$%&/()=?"


class PasswordGenerator:
    def __init__(self, length=8, letters=True, numbers=True, special_chars=True, custom_chars=None):
        self.length = length
        self.letters = letters
        self.special_chars = special_chars
        self.numbers = numbers
        self.custom_chars = custom_chars

    def __repr__(self):
        info = """Generator info:
Password length: {}
Includes letters: {}
Includes numbers: {}
Includes special characters: {}\n""".format(self.length, self.letters, self.numbers, self.special_chars)

        custom = "Yes, " + str(self.custom_chars) if self.custom_chars is not None else "False"
        info += "Has a custom character pool: " + custom
        return info

    def set_length(self, length):
        self.length = length

    def set_characters(self, letters, numbers, special_chars):
        self.letters = letters
        self.numbers = numbers
        self.special_chars = special_chars

    def set_custom_chars(self, custom_chars):
        if custom_chars == "":
            self.custom_chars = None
        else:
            self.custom_chars = custom_chars

    def generate(self, amount=1, re=False):
        try:
            amount = int(amount)
        except ValueError:
            print("Invalid amount: ", amount)
            return

        passwords = []

        if self.custom_chars is not None:
            chars = self.custom_chars
        else:
            chars = ""
            chars += string.ascii_letters if self.letters else ""
            chars += string.digits if self.numbers else ""
            chars += SPECIAL_CHARACTERS if self.special_chars else ""

        for _ in range(amount):
            passwords.append(''.join((random.choice(chars)) for x in range(self.length)))

        if re:
            return passwords
        else:
            for password in passwords:
                print(password)


if __name__ == "__main__":
    pg = PasswordGenerator(20)
    pg.generate("5")
