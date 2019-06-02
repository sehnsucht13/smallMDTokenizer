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
        print(self.currTok)

    def nextTok(self):
        """ Increments the position, sets the next token and returns it"""
        self.currTok = self.tokens[self.currIndex]
        self.currIndex += 1
        return self.currTok

    def peekTok(self, n=1):
        """ Returns the next token in stream without incrementing the
            position """
        return self.tokens[self.currIndex + n]

    def write(self, htmlString):
        """ Writes the provided HTML string to the output file 
            which is represented by the var called fileHandle """
        self.fileHandle.write(htmlString + "\n")

    def isMatch(self, text, token, singleLine,):
        """ Check if the provided token is matched in the current line or 
            the current block if no flag is provided """
        # Get the next token
        print("\n")
        print("Matching")
        print(text)
        textLen = len(text)
        index = 0
        if singleLine and index + 1 != textLen:
            currIndex = index + 1
            currTok = text[currIndex]
            while currIndex < len(text):
                if currTok["type"] == token:
                    return True
                else:
                    currIndex += 1
                    currTok = text[currIndex]
                    return False



    def tokToString(self, token):
        """ Convert any type of text markup token(bold, italics...) to its
            text representation if it cannot be matched with a closing pair """
        if token["type"] == tokType.BOLD:
            return "**"
        elif token["type"] == tokType.ICODE:
            return "`"
        elif token["type"] == tokType.CROSS:
            return "~~"
        elif token["type"] == tokType.ITALIC:
            return "*"

    def tokToHtml(self, token, close):
        """ Return the HTML representation of the token. This can be either the
            opening or closing tag depending on whether the argument \"close\"
            is true or not """
            if close is True:
                if token["type"] == tokType.BOLD:
                    return "</strong>"
                elif token["type"] == tokType.ITALIC:
                    return "</em>"
                elif token["type"] == tokType.CROSS:
                    return "</del>"
                elif token["type"] == tokType.ICODE:
                    return "</code>"
            else:
                if token["type"] == tokType.BOLD:
                    return "<strong>"
                elif token["type"] == tokType.ITALIC:
                    return "<em>"
                elif token["type"] == tokType.CROSS:
                    return "<del>"
                elif token["type"] == tokType.ICODE:
                    return "<code>"

    def convertText(self, text, singleLine):
        """ Converts text tokens to their HTML form. When a special token
            such as bold or italic, they are converted only if a matching 
            is found in the same block. Blocks are defined with spaces at 
            their end. If a matching token is not found inside the block 
            then the token is turned into its text representation """
                
        markUpText = ""
        textLen = len(text)

        if singleLine:
            index = 0
            while index < textLen:
                subTok = text[index]
                if subTok["type"] == tokType.PLAIN:
                    markUpText += subTok["content"]
                else:
                    # check if the current token matches on the line
                    if self.isMatch(text[index + 1:], subTok['type'], True):
                        # need function to retrieve the html representation of the token
                        print("Got a match")
                    else:
                        # Need a function to retrieve the literal text translation
                        print("No match :(")

                index += 1

            return markUpText 

    def convertHeading(self):
        """ Convert a heading to html and add it to output file """
        size = self.currTok['size']
        content = self.convertText(self.currTok['content'], True)
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

    def convertTokens(self):
        streamLen = len(self.tokens)
        while self.currIndex < streamLen:
            # Marked Heading
            if self.currTok['type'] == tokType.MHEADING:
                self.convertHeading()
            # Regular link
            elif self.currTok['type'] == tokType.LINK:
                self.convertLink()
            # Image link
            elif self.currTok['type'] == tokType.IMAGE:
                self.convertImage()
            # Blank line
            elif self.currTok['type'] == tokType.BLANK:
                self.write("")

            self.nextTok()

