import mdownParser
import HtmlConverter
import argparse


def main():
    parser = argparse.ArgumentParser(
        description='Convert the provided file from Markdown to HTML')
    parser.add_argument('PATH', help="The path to the file to be converted")
    args = parser.parse_args()
    print(args)


if __name__ == '__main__':
    main()
