# 1 Create two variables – one with your name and one with your age
name = input('Please enter your name: ')
age = input('Please enter your age: ')

# 2 Create a function which prints your data as one string
def print_my_info():
    """ Print the user name and age. """
    print('My name is {}. I am {} years old.'.format(name, age))
    print('I have lived for ' + str(live_decades(age)) + ' decades.')

# 3 Create a function which prints ANY data (two arguments) as one string
def print_any_info(arg1, arg2):
    """  Print two concatenated strings. """
    print(str(arg1) + ', ' + str(arg2))


print_any_info(6.28, 987)

# 4 Create a function which calculates and returns the number of decades you already lived (e.g. 23 = 2 decades)
def live_decades(age):
    """  Calcualte the integer part of the age received. """
    return int(age)//10


print_my_info()
