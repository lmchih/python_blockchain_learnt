def unlimited_arguments(*args, **dict_args):
    # print(args) # python creats a tuple for you
    print(dict_args)
    for k, v in dict_args.items():
        print(k, v)


unlimited_arguments(1,2,3,4, name='Rick', age=38)