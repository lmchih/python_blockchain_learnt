from vehicle import Vehicle


class Bus(Vehicle):
    def __init__(self, starting_max_speed=100):  # dunder
        # define instance attributes
        super().__init__(starting_max_speed)  # calls the parent Constructor
        self.passengers = []

    def add_group(self, passengers):
        self.passengers.extend(passengers)


bus1 = Bus(350)
passengers = ['Rick', 'Dino', 'An']
bus1.add_warning('Warning! Engine is hot!')
bus1.add_group(passengers)
print(bus1.passengers)
print(bus1.get_warnings())
