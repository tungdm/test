import sys
import time


def main(name):
    i = 0
    while i < 100:
        print('Hello, %s, %s' % (name, i))
        i += 5
        time.sleep(3)


if __name__ == '__main__':
    main(sys.argv[1])
