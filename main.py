import sys


def test(i):
    return i*2


def main(name):
    j = 0
    for i in range(10):
        j += test(i)

    print('Hello, %s, %s' % (name, i))


if __name__ == '__main__':
    main(sys.argv[1])
