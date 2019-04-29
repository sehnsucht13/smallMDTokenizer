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
        
        inputFile = open(args.path)
    else:
        print("The provided path to the input file does not exist.")
        sys.exit(1)

if __name__ == '__main__':
    main()
