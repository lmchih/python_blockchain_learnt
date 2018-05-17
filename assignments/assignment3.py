import copy


# 1) Create a list of “person” dictionaries with a name, age and list of hobbies for each person. Fill in any data you want.
persons = [
    {
        'name': 'Rick',
        'age': 38,
        'hobbies': ['swimming', 'reading', 'crypto mining']
    },
    {
        'name': 'Lynne',
        'age': 25,
        'hobbies': ['drama', 'music', 'sleeping']
    },
    {
        'name': 'Ben',
        'age': 35,
        'hobbies': ['video games', 'shopping']
    },
    {
        'name': 'Jack',
        'age': 27,
        'hobbies': ['movies', 'workout', 'eating']
    }
]

# print(persons)


# 2) Use a list comprehension to convert this list of persons into a list of names (of the persons).
names = [person['name'] for person in persons]
print(names)


# 3) Use a list comprehension to check whether all persons are older than 20.
is_all_older_than_20 = all([person['age'] > 20 for person in persons])
print(is_all_older_than_20)

# 4) Copy the person list such that you can safely edit the name of the first person (without changing the original list).
# shallow copy
# copied_persons = persons[:]

# deep copy
# copied_persons = copy.deepcopy(persons)
copied_persons = [person.copy() for person in persons]
print(copied_persons)
copied_persons[0]['name'] = 'Ming-Chih'
print(copied_persons[0]['name'])
print(persons[0]['name'])


# 5) Unpack the persons of the original list into different variables and output these variables.
# unpacked = [[(k, v) for k, v in person_dict.items()]
#             for person_dict in persons]  # list comprehension
# print(unpacked)
# p1, p2, p3, p4 = [person for person in unpacked]
p1, p2, p3, p4 = persons
print(p1)
print(p2)
print(p3)
print(p4)
