class Vehicle:
    def __init__(self, starting_max_speed=100):  # dunder
        # define instance attributes
        self.max_speed = starting_max_speed
        self.__warnings = []  # private variable!!!

    """ Called by Python whenever we're trying to output the class 
            :return: Some custom strings should be output
    """
    def __repr__(self):
        print('Printing....')
        return 'Max Speed: {}, Warning: {}'.format(self.max_speed, len(self.__warnings))

    def add_warning(self, warning_text):
        if len(warning_text) > 0:
            self.__warnings.append(warning_text)

    def get_warnings(self):
        return self.__warnings

    def drive(self):
        print('I am driving but certainly not faster than {}.'.format(self.max_speed))
