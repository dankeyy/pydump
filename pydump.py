#!/usr/bin/env python3

import re
import sys
import os
import pathlib


def pydump():
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

            # if this matches,
            # it means the disassembly line starts with a leading integer,
            # denoting source line number and the beginning of
            # a new dis code block that describes it
            starts_codeblock = re.match(lineno_pattern, bytecode_line)
            if starts_codeblock:
                lineno = int(starts_codeblock.groups()[0])
                break


if __name__ == '__main__':
    pydump()
