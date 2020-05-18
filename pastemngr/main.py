import sys

from controller import EmptyPasteError
from argument_handler import Parser
from make_request import BadApiRequestError

def main():
    parser = Parser()

    parser.prepare()

    try:
        parser.run()
    except BadApiRequestError as e:
        sys.stderr.write(f'Bad API Request: {e}\n')
        return 1
    except FileNotFoundError as e:
        sys.stderr.write(f'File not found error: {e}\n')
        return 1
    except EmptyPasteError as e:
        sys.stderr.write(f'Couldn\'t create paste: {e}\n')

    return 0

if __name__ == '__main__':
    sys.exit(main())
