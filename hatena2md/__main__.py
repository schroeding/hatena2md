"""
hatena2md

A Hatena Notation to Markdown Converter
"""

import argparse
import sys
from hatena2md import Hatena2MD

def main():  
    parser = argparse.ArgumentParser('hatena2md')
    parser.add_argument('-i', dest='input', help='input file (otherwise stdin)', default=None, required=False)
    parser.add_argument('-o', dest='output', help='output file (otherwise stdout)', default=None, required=False)
    args = parser.parse_args(sys.argv[1:])

    if (args.input is None):
        try:
            hatena = sys.stdin.buffer.read()
        except (KeyboardInterrupt):
            return
    else: 
        try:
            file = open(args.input, 'rb')
        except (Exception):
            print('Could not open the specified input file!')
            return
        hatena = file.read()
        file.close()

    markdown = Hatena2MD(str(hatena, encoding='utf-8')).toMarkdown()

    if (args.output is None):
        print(markdown)
    else: 
        try:
            file = open(args.output, 'wb')
        except (Exception):
            print('Could not open the specified output file!')
            return
        file.write(bytes(markdown, encoding='utf-8'))
        file.close()

if (__name__ == '__main__'):
    main()