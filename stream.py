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

import re


class streamSource:
    """ Class responsible for controlling the file handle for the markdown file to be
        parsed and providing access to its components"""

    def __init__(self, fileHandle):
        # hold the current line number in case of any errors
        self.lineNum = 0
        try:
            self.fHandle = fileHandle
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

    def getLineNum(self):
        return self.lineNum

    def lookAheadLineTest(self, regExp):
        """Checks if the beginning of the next line matches a regular expression
            Used to checkfor any underlined headings """
        pos = self.fHandle.tell()
        currLine = self.fHandle.readline()
        status = re.search(regExp, currLine)
        self.fHandle.seek(pos)
        return status
