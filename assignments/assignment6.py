import json
import pickle


# 1) Write a short Python script which queries the user for input (infinite loop with exit possibility) and writes the input to a file.
# 2) Add another option to your user interface: The user should be able to output the data stored in the file in the terminal.
# waiting_for_input = True

# while waiting_for_input:
#     print('\'q\' to quit.')
#     print('\'r\' to see data stored.')
#     print('\'w\' to write to a file: ')
#     user_input = input('Please choose your action: ')
#     if user_input == 'q':
#         waiting_for_input = False
#     elif user_input == 'r':
#         # read file
#         with open('assignment.txt', mode='r') as f:
#             file_content = f.readlines()
#             for el in file_content:
#                 print(el[:-1])
#     elif user_input == 'w':
#         with open('assignment.txt', mode='a') as f:
#             write_content = input('Enter any strings: ')
#             f.write(str(write_content))
#             f.write('\n')
#             print('You enter: {}'.format(write_content))
#     else:
#         pass


# print('Bye~')


# 3) Store user input in a list (instead of directly adding it to the file) and write that list to the file – both with pickle and json.
# 4) Adjust the logic to load the file content to work with pickled/ json data.
def json_write(string):
    with open('write.txt', mode='a') as f:
        f.write(json.dumps(string))
        f.write('\n')


def json_read():
    with open('write.txt', mode='r') as f:
        content = f.readlines()
        for line in content:
            print(json.loads(line))


def pickle_write(string):
    with open('write.p', mode='ab') as f:
        f.write(pickle.dumps(string))


def pickle_read():
    with open('write.p', mode='rb') as f:
        print(pickle.loads(f.read()))


running = True
user_input_list = []

while running:
    print('\'q\' to quit.')
    print('\'1\' to write into JSON data.')
    print('\'2\' to read JSOn file: ')
    print('\'3\' to write into Pickle data.')
    print('\'4\' to read Pickle file.')
    user_input = input('Please choose your action: ')
    if user_input == 'q':
        running = False

    elif user_input == '1':
        text = input('Enter text: ')
        user_input_list.append(text)
        with open('write.txt', mode='w') as f:
            f.write(json.dumps(user_input_list))
    elif user_input == '2':
        with open('write.txt', mode='r') as f:
            file_content = json.loads(f.read())
            for line in file_content:
                print(line)
    elif user_input == '3':
        text = input('Enter text: ')
        user_input_list.append(text)
        with open('write.p', mode='wb') as f:
            f.write(pickle.dumps(user_input_list))
    elif user_input == '4':
        with open('write.p', mode='rb') as f:
            file_content = pickle.loads(f.read())
            for line in file_content:
                print(line)

print('Bye~')
