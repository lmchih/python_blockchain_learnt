from vehicle import Vehicle

class Car(Vehicle):

    def brag(self):
        print('How cool this is!')

car1 = Car()
car1.drive()    # method
# Car.max_speed = 200
# print (car1.max_speed)  # attribute
car1.add_warning('New Warning')
# car1.__warnings.append([])
# print(car1.__dict__)    # just a snapshot. not actually connect to the instance!
print(car1)
print(car1.get_warnings())


car2 = Car(200)
car2.drive()
print(car2.get_warnings())


car3 = Car(300)
car3.drive()
print(car3.get_warnings())
