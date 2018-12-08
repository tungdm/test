import sys
import time


def test(i):
    print('Hello 1')
    return i*2


def main(name):
    j = 0
    for i in range(10):
        j += test(i)
    print('Hello 2')
    print('Hello, %s, %s' % (name, i))
    i = 0
    while i < 100:
        print('Hello, %s, %s' % (name, i))
        i += 5
        time.sleep(3)


if __name__ == '__main__':
    main(sys.argv[1])
