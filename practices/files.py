"""  """


with open('demo.txt', mode='w') as f:
    # f.write('Add this content!\n')
    # file_content = f.readlines()
    # f.close()

    # for line in file_content:
    #     print(line[:-1])    # exclude \n
    # line = f.readline()

    # while line:
    #     print(line)
    #     line = f.readline()
    f.write('Test if the flie is closed...')

user_input = input('Enter please: ')
print("Done!")