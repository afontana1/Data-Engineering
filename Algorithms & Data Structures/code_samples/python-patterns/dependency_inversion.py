class Animal:
    def __init__(self, speaking_behavior):
        self.speaking_behavior = speaking_behavior

    def speak(self):
        return self.speaking_behavior.speak()


class Cat:
    def speak(self):
        return "Meow"


class Dog:
    def speak(self):
        return "Woof"


class Bird:
    def speak(self):
        return "Cawwww!"


cat = Animal(Cat())
