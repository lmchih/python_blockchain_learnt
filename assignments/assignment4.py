# 1) Write a normal function that accepts another function as an argument. Output the result of that other function in your “normal” function.
# def another_func():
#     print("another function")
def normal_func(anotherfunc):
    print(anotherfunc(1))


# 2) Call your “normal” function by passing a lambda function – which performs any operation of your choice – as an argument.
normal_func(lambda x: x * 2)

# 3) Tweak your normal function by allowing an infinite amount of arguments on which your lambda function will be executed.
def infinite_normal_func(anotherfunc, *args):
    for arg in args:
        print("Result: {}".format(anotherfunc(arg)))


infinite_normal_func(lambda x: x*2, 1, 2, 3, 4)


# 4) Format the output of your “normal” function such that numbers look nice and are centered in a 20 character column.
def infinite_normal_func_neat(anotherfunc, *args):
    for arg in args:
        print("Result: {:^20.2f}".format(anotherfunc(arg)))


infinite_normal_func_neat(lambda x: x*2, 1, 2, 3, 4)