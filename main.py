import sys
import time


def test(i):
    for x in range(i):
        print('Hello 1')
    return i*2


def main(name):
    for i in range(10):
        print(i)


def my_implement():
    pass


if __name__ == '__main__':
    main(sys.argv[1])
