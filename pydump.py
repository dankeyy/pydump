#!/usr/bin/env python3

import re
import sys
import os
import pathlib


def main():
    filepath = sys.argv[1]

    source_lines = pathlib.Path(filepath).read_text().splitlines()
    if not source_lines:
        raise ValueError("WHERE'S THE CODE")

    bytecode_lines = iter(os.popen("python -m dis " + filepath))

    lineno_pattern = re.compile(r"^\s{1,4}(\d+).*$")

    buffer = next(bytecode_lines)
    lineno = int(re.match(lineno_pattern, buffer).groups()[0])

    while True:
        print(filepath + ':', lineno)
        print(source_lines[lineno - 1], end='\n\n')

        while True:
            bytecode_line = next(bytecode_lines, None)
            if bytecode_line is None:
                return

            print(buffer, end='')
            buffer = bytecode_line

            new_block = re.match(lineno_pattern, bytecode_line)
            if new_block:
                lineno = int(new_block.groups()[0])
                break


if __name__ == '__main__':
    main()
