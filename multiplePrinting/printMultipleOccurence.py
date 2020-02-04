import colorsys



for index in range(0, 1001):
    if index % 10 == 0:
        print("\033[1;31m{} : {}\033[1;m".format('multiple of 10', index))
    elif index % 3 == 0:
        print("foo : {}".format(index))
        if index % 5 == 0:
            print("     bar : {}".format(index))
    elif index % 5 == 0:
        print("bar : {}".format(index))
        if index % 3 == 0:
            print("     bar : {}".format(index))
    else:
        print("\033[2;34mothers : {}\033[2;m".format(index))
