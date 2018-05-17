# 1) Create a Food class with a “name” and a “kind” attribute as well as a “describe() ” method (which prints “name” and “kind” in a sentence).
class Food:
    name = 'X'
    kind = 'Y'

    def __init__(self, name=name, kind=kind):
        self.name = name
        self.kind = kind

    def describe(self):
        print('{} is a kind of {}'.format(self.name, self.kind))

# 2) Try turning describe()  from an instance method into a class and a static method. Change it back to an instance method thereafter.
    @classmethod
    def cls_describe(cls):
        print('{} is a kind of {}'.format(cls.name, cls.kind))

    @staticmethod
    def static_descirbe(name, kind):
        print('{} is a kind of {}'.format(name, kind))

# 4) Overwrite a “dunder” method to be able to print your “Food” class.
    def __repr__(self):
        return str(self.__dict__)


# 3) Create a  “Meat” and a “Fruit” class – both should inherit from “Food”. Add a “cook() ” method to “Meat” and “clean() ” to “Fruit”.
class Meat(Food):
    # Optional
    def __init__(self, name):
        super().__init__(name, 'Meat')

    def cook(self):
        print('{} is getting cooked.'.format(self.name))


class Fruit(Food):
    def clean(self):
        print('{} is getting cleaning'.format(self.name))


# instance method
food1 = Food('Banana', 'Fruit')
food2 = Food('Steak', 'Meat')
food1.describe()
food2.describe()

# inheritance
food3 = Fruit('Apple', 'Fruit')
food3.describe()
food3.clean()
print(food3)

food4 = Meat('Pork')
food4.describe()
food4.cook()
print(food4)

# class method
Food.name = 'Broccoli'
Food.kind = 'Vegetable'
Food.cls_describe()


# static method
Food.static_descirbe('Coffee', 'Drink')
