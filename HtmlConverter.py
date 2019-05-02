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
import tokenType

class HTMLConverter():
    def __init__(self, tokenStream, outputFileHandle):
        self.fileHandle = outputFileHandle
        # Holds the stream of tokens
        self.tokens = tokenStream
        # Holds the current token
        self.currTok = None
        # The index along the stream
        self.currIndex = 0

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
        imgAltText = self.currtok['title']
        imgPath = self.currTok['path']
        outputString = "<img src=\"{0}\" alt=\"{1}\" width=\"200\" height=\"200\">"

    def convertTokens():

