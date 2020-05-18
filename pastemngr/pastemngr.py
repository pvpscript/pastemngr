import sys

from argument_handler import Parser
from make_request import BadApiRequest

def main():
    parser = Parser()

    parser.prepare()

    try:
        parser.run()
    except BadApiRequest as e:
        print(f'Bad API Request: {e}')
    except FileNotFoundError as e:
        print(f'File not found error: {e}')

    return 1

if __name__ == '__main__':
    sys.exit(main())
