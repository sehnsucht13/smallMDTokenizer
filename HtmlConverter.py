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

from tokenType import tokType

class HTMLConverter():
    """ Convert a stream of tokens passed by \"tokenStream\" into a 
        valid HTML file which is saved in the file represented by 
        \"outputFileHandle\" """
    def __init__(self, tokenStream, outputFileHandle):
        # File handle to the output file
        self.fileHandle = outputFileHandle
        # Holds the stream of tokens
        self.tokens = tokenStream
        # The index along the stream
        self.currIndex = 0
        # Holds the current token
        self.currTok = self.tokens[self.currIndex]

    def nextTok(self):
        """ Increments the position, sets the next token and returns it"""
        self.currTok = self.tokens[self.currIndex]
        self.currIndex += 1
        return self.currTok

    def peekTok(self):
        """ Returns the next token in stream without incrementing the
            position """
        return self.tokens[self.currIndex + 1]

    def write(self, htmlString):
        """ Writes the provided HTML string to the output file 
            which is represented by the var called fileHandle """
            self.fileHandle.write(htmlString + "\n")

    def convertHeading(self):
        """ Convert a heading to html and add it to output file """
        size = self.currTok['size']
        content = self.currTok['content']
        outputString = "<h{0}>{1}</h{0}>".format(size, content)
        self.write(outputString)

    def convertLink(self):
        """ Converts a link to HTML and adds it to the output file """
        linkTitle = self.currTok['title']
        linkPath = self.currTok['path']
        outputString = "<a href=\"{0}\">{1}</a>"
        self.write(outputString)

    def convertImage(self):
        """ Converts an image link to HTML and adds it to the output file """
        imgAltText = self.currtok['title']
        imgPath = self.currTok['path']
        outputString = "<img src=\"{0}\" alt=\"{1}\" width=\"200\" height=\"200\">"

    def convertTokens():
        while True:
            # Marked Heading
            if self.currTok['type'] == tokType.MHEADING:
                self.convertHeading()
                self.nextTok()
            # Regular link
            elif self.currTok['type'] == tokType.LINK:
                self.convertLink()
                self.nextTok()
            # Image link
            elif self.currTok['type'] == tokType.IMAGE:
                self.convertImage()
                self.nextTok()
            # Blank line
            elif self.currTok['type'] == tokType.Blank:
                self.write("")
                self.nextTok()
            # Exit the loop
            elif self.currTok['type'] == tokType.EOF:
                break



