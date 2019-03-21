import re

mdRegExp = {
    'mdUndelineHeading': "^(==+|---+|***+|___+)"
}


class streamSource:
    """ Class responsible for opening a file handle to the markdown file to be
        parsed and providing access to its components"""

    def __init__(self, streamPath):
        self.lineNum = 0
        try:
            self.fHandle = open(streamPath, 'r')
            # find end of file
            self.fHandle.seek(0, 2)
            # save end of file location
            self.eof = self.fHandle.tell()
            # go back to beginning
            self.fHandle.seek(0)
        except PermissionError:
            print("The file cannot be opened for reading due to a lack of permission!")
        except FileNotFoundError:
            print("The file requested could not be found.")
            print(
                "Make sure that the path is specified properly and that the file exists")

    def returnLine(self):
        self.lineNum += 1
        return self.fHandle.readline()

    def checkEOF(self):
        return not (self.fHandle.tell() == self.eof)

    def lookAhead(self, regExp):
        """Checks if the beginning of the next line matches a regular expression"""
        currLine = self.fHandle.readline()
        status = re.search(regExp, currLine)
        return status
