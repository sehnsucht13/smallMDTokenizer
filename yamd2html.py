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

from mdownParser import mdTokenizer
from HtmlConverter import HTMLConverter
from sys import exit
import argparse
import os

def checkArgPath(args):
    """ Checks whether or not the provided file paths exists. If needed, 
        files and folders are created to accomodate the output path
        provided. Also opens file handles to the respective files and returns them"""
    # Check if the provided path for the input and output files is valid
    if os.path.isfile(args.path) is True:
        if args.output is not None:
            # Case of providing a valid output file
            if os.path.isfile(args.output) is True:
                outputFileHandle = open(args.output, "w")
            # Case of outptut file not existing. Create any new directories 
            # along the way
            else:
                outputPath, outputFile = os.path.split(args.output)
                os.makedirs(outputPath)
                outputFileHandle = open(args.output, "w")

        # If the output file is not provided, one is created in the same folder
        # with the same name
        else:
            # Retrieve the path for the new file to be created
            inputHead, inputTail = os.path.split(args.path)
            inputTail = inputTail.split('.')[0]
            inputTail += ".html"
            outputFileHandle = open(os.path.join(inputHead, inputTail), "w+")
        
        # Open the input file
        inputFileHandle = open(args.path)

        return (inputFileHandle, outputFileHandle)
    else:
        print("""The provided path to the input file does not exist. Please
                double check that you provided it correctly!""")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(
        description='Convert the provided file from Markdown to HTML')
    parser.add_argument(
        'path', help="The path to the file to be converted")
    parser.add_argument(
        '-o', '--output', help="The path for the output file. If it is not provided, an HTML file will be created in the same folder with the same file name but ending with a .html file extension.")
    args = parser.parse_args()
   
   # File handles for input and output file 
    inputFile, outputFile = checkArgPath(args)

    tokenizer = mdTokenizer(inputFile)
    tokenizer.tokenize()
    # List of tokens extracted from the markdown input file provided
    tokens = tokenizer.returnTokenList()
    print(tokens)

    converter = HTMLConverter(tokens, outputFile)
    # Convert the tokens and output to an HTML file
    converter.convertTokens()

if __name__ == '__main__':
    main()
