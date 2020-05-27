import sys

import pastemngr
from pastemngr.core.controller import ControlError
from pastemngr.core.argument_handler import Parser

def main():
    parser = Parser()

    parser.prepare()

    try:
        parser.run()
    except ControlError as e:
        print(f'Execution error -> {e}', file=sys.stderr)
        return 1

    return 0
