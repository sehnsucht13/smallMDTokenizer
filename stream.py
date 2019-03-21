import re


class streamSource:
    """ Class responsible for opening a file handle to the markdown file to be
        parsed and providing access to its components"""

    def __init__(self, streamPath):
        # hold the current line number in case of any errors
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
        """ Return the next line of text from the source file """
        self.lineNum += 1
        return self.fHandle.readline()

    def checkEOF(self):
        """ Check if the end of file is reached """
        return not (self.fHandle.tell() == self.eof)

    def lookAhead(self, regExp):
        """Checks if the beginning of the next line matches a regular expression"""
        pos = self.fHandle.tell()
        currLine = self.fHandle.readline()
        status = re.search(regExp, currLine)
        self.fHandle.seek(pos)
        return status
