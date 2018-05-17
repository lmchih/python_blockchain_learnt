''' 1) Craete a list of names '''
names = ['Vincent', 'Nicolas', 'Marilyne',
         'Westbrook', 'Stephen', 'Jackson', 'Lee']


def print_names():
    for i in range(len(names)):
        """ 1) use a for loop to output the length of each name ( len() ). """
        print("{} has length {}".format(names[i], len(names[i])))
        """ 2) Add an if check inside the loop to only output names longer than 5 characters. """
        if len(names[i]) > 5:
            print("{}'s longer than 5 characters.".format(names[i]))
        """ 3) Add another if check to see whether a name includes a "n" or "N" character. """
        if 'n' in names[i] or 'N' in names[i]:
            print("{} contains 'n' or 'N' character.".format(names[i]))


''' 4) Use a while loop to empty the list of names (via pop() ) '''
def empty_list(the_list):
    while len(the_list) > 0:
        the_list.pop()


print_names()
empty_list(names)
print("After calling empty_list() the names become: {}".format(names))
