#
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.

#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.

#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
#     Copyright (C) 2019 Yavor Konstantinov
#

import mdownParser
import HtmlConverter
import argparse
import sys
import os.path


def main():
    parser = argparse.ArgumentParser(
        description='Convert the provided file from Markdown to HTML')
    parser.add_argument(
        'path', help="The path to the file to be converted")
    parser.add_argument(
        '-o', '--output', help="The path for the output file. If it is not provided, an HTML file will be created in the same folder with the same file name but ending with a .html file extension.")
    args = parser.parse_args()
   
   # Contains the file handle for the output file
    outputFile = None
    inputFile = None

    # Check if the provided path for the input file is valid
    if os.path.isfile(args.path) is True:
        if args.output is not None and os.path.isfile(args.output) is True:
            outputFile = open(args.output, "w+")
        # If the output file is not provided, one is created in the same folder
        # with the same name
        else:
            # Retrieve the path for the new file to be created
            inputHead, inputTail = os.path.split(args.path)
            inputTail = inputTail.split('.')[0]
            inputTail += ".html"
            print(inputTail)
            outputFile = open(os.path.join(inputHead, inputTail), "w+")
        
        # Open the input file
        inputFile = open(args.path)
    else:
        print("The provided path to the input file does not exist.")
        sys.exit(1)

if __name__ == '__main__':
    main()
