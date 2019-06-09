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
import re


class mdTokenizer:
    """Class which tokenizes a markdown file by iterating through it line
    by line"""

    def __init__(self, source):

        # Handle to the source file
        self.src = source

        # The contents of the source file
        self.text = self.src.read()

        # Index of the last character in the source file
        self.EOF = len(self.text)

        # Current index along the source
        self.currIndex = 0

        # A list holding the structure of the document
        self.document = []

        # The current block. Used for plaintext while headers and all others
        # reside in their own block
        self.currBlock = []

        # The current character
        self.currChar = self.text[self.currIndex]

        # Indicates if the previous line was a blank.
        # used to recognize horizontal ruling vs plain - or =
        self.blankFlag = False

    def getNext(self):
        """ Return the next character in the current line """
        self.currIndex += 1
        if self.currIndex >= self.EOF:
            self.currChar = "\n"
        else:
            self.currChar = self.text[self.currIndex]

        return self.currChar

    def peekNext(self, n=1):
        """ Return the next character without incrementing the position """
        if n + self.currIndex == self.EOF:
            return "\n"
        else:
            return self.text[self.currIndex + n]

    def peekPrev(self):
        """ Return the previous character in the stream without decrementing
            the position """
        # Case of being at the beginning of file
        if self.currIndex == 0:
            return None
        else:
            return self.text[self.currIndex - 1]

    def skipWhiteSpace(self):
        """Skips all whitespace until the next character is encountered"""
        while self.currChar == " ":
            self.getNext()

    def closeBlock(self):
        """ Adds the current block the the document structure. Used when another blocktype
            such as a bullet follows plain text."""
        if len(self.currBlock) is not 0:
            # Add the block to the document structure
            self.document.append(self.currBlock)
            # Create a new block
            self.currBlock = []

    def skipWhiteSpaceNewLine(self):
        """Resets the current index and consumes whitespace until an any
        character which is not space is reached"""
        # Used to measure indentation levels for lists within lists
        spaceNumberCount = 0
        # Iterate and count until we reach anything which is not a space
        while self.currChar == " ":
            spaceNumberCount += 1
            self.getNext()

        # If the number of spaces is more than 0 then we have indented text
        if spaceNumberCount != 0:
            self.currBlock.append({"type": tokType.INDENT, "count": spaceNumberCount})

    def checkEmptyLine(self):
        """Check if the current line is an empty line"""
        if self.currChar == "\n":
            return True
        return False

    def addEOL(self):
        """Adds an end of line token to the token list"""
        self.currBlock.append({"type": tokType.EOL})

    def isRFlank(self):
        prevChar = self.peekPrev()
        if prevChar == " ":
            return False
        # Case of a newline, considered a right flank
        elif prevChar is False:
            return True

    def eatChars(self):
        """Consumes characters and returns them to the calling function in the form of
        a string. This function assumes that what is to be consumed is only
        plain characters without any markup. Used for headings"""
        itemText = ""
        while self.currChar != "\n":
            itemText += self.currChar
            self.getNext()
        return itemText

    def tokenizeMarkedHeading(self):
        """Tokenizes a standard markdown heading"""
        headingSize = 1
        headingText = ""

        while self.getNext() == "#":
            if headingSize != 6:
                headingSize += 1

        # Skip over intial whitespace
        self.skipWhiteSpace()

        # Add contents of heading
        headingText = self.eatChars()

        # Close off the block
        self.closeBlock()

        # Append to token list
        self.document.append(
            {"type": tokType.MHEADING, "size": headingSize, "content": headingText}
        )

    def tokenizeUnmarkedHeading(self):
        """ Tokenize headings which are underlined """
        textContent = self.eatChars()
        # skip over the next line since it is useless to parse
        while self.getNext() != "\n":
            pass

        # Close off the block
        self.closeBlock()
        self.document.append({"type": tokType.UHEADING, "content": textContent})

    def tokenizeText(self):
        """Tokenizes a line of marked up text"""
        # Case of an empty line
        if self.currChar == "\n":
            self.blankFlag = True
            self.currBlock.append({"type": tokType.BLANK})

        # Case of any other text
        else:
            self.blankFlag = False
            textContent = self.eatChars()
            self.currBlock.append({"type": tokType.PLAIN, "content": textContent})


    def tokenizeCheckItem(self):
        """ Tokenize a checklist item of the form:
            - [ ] ITEM """
        status = None
        self.skipWhiteSpace()
        # Skip over the -
        self.getNext()
        self.skipWhiteSpace()
        # Skip over the beginning [
        self.getNext()

        if self.currChar == "x":
            status = True

        # Skip over the closing ]
        self.getNext()
        self.getNext()
        self.skipWhiteSpace()

        checkItemContent = self.eatChars()

        # Close off the block
        self.closeBlock()
        self.document.append(
            {"type": tokType.CHECKMARK, "status": status, "content": checkItemContent}
        )


    def isCheckItemOrBullet(self):
        """Check if the current line is a simple list bullet or is a checkmark"""
        if self.peekNext(1) == ' ' and self.peekNext(2) == '[':
            return tokType.CHECKMARK
        elif self.peekNext(1) == ' ':
            return tokType.BULLET
        else:
            return tokType.PLAIN

    def isNumBullet(self):
        """ Check if the current line starting with a number is a 
            numbered bullet or a regular line of markdown text"""
        pos = 0
        # Skip numbers on the line
        while str.isdigit(self.peekNext(pos)):
            pos += 1
        # Check if the bullet is the required format
        if self.peekNext(pos) == "." and self.peekNext(pos + 1) == " ":
            return True
        else:
            return False

    def tokenizeBullet(self):
        """ Tokenize a markdown bullet """
        # Case of a numbered list item
        if str.isdigit(self.currChar) == True:
            # Iterate over all digits. This parses does not care about the
            # number associate with the bullet. The numbers are assigned
            # automatically when converting into an HTML numbered list
            while str.isdigit(self.currChar):
                self.getNext()
            # At this point, we are the . character
            self.getNext()
            self.skipWhiteSpace()
            # Consume the chars
            text = self.eatChars()

            self.closeBlock()
            self.document.append({"type": tokType.NUMBULLET, "content": text})

        # Case of a regular bullet
        else:
            # Skip over the *, - or +
            self.getNext()
            # Skip over the whitespace
            self.skipWhiteSpace()

            # Consume the characters
            text = self.eatChars()

            self.closeBlock()
            self.document.append({"type": tokType.BULLET, "content": text})

    def isHR(self, char):
        """ Count the occurence of a certain type of character on a line of 
            text. Used to detect horizontal line rules."""
        count = 1
        pos = 1
        while self.peekNext(pos) == char:
            count += 1
            pos += 1
        if self.peekNext(pos) == "\n" and count >= 3 and self.blankFlag == True:
            return True
        else:
            return False

    def insertHR(self):
        """ Insert a horizontal rule token into the token stream """
        print("Insert hr")
        while self.currChar != "\n":
            self.getNext()

        self.getNext()

        self.closeBlock()
        self.document.append({"type": tokType.HR})

    def getNextLine(self):
        """ Returns the start and end positions of the next line """
        # starting position of next line
        startPos = 1
        # End position of next line. Represents \n
        endPos = 0
        # Find the beginning of next string
        while self.peekNext(startPos) != "\n":
            startPos += 1

        # At this point, startPos points to the index of \n
        startPos += 1

        endPos = startPos
        startPos += self.currIndex

        # Find the end of next string
        while self.peekNext(endPos) != "\n":
            endPos += 1

        endPos += self.currIndex
        # Skip over the \n
        endPos += 1
        return (startPos, endPos)

    def isUnderlinedHeading(self):
        """ Check if the next line is an underlined heading """
        start, end = self.getNextLine()
        string = self.text[start:end]
        searchExp = re.compile("^(-{3,}|={3,})\n")
        output = searchExp.fullmatch(string)

        return output

    def tokenize(self):
        """ General driver of the entire tokenizer. 
            It applies the tokenizing rules based on the context detected
            by the first character of the stream which has not yet been consumed """
        while self.currIndex + 1 < self.EOF:
            if self.currChar == "\n":
                self.getNext()
            self.skipWhiteSpaceNewLine()
            # Standard heading starting with #
            if self.currChar == "#":
                self.tokenizeMarkedHeading()
            # Underlined heading
            elif self.isUnderlinedHeading():
                self.tokenizeUnmarkedHeading()
            elif self.currChar == "_":
                if self.isHR("_") == True:
                    self.insertHR()
            # Either a bullet or checklist item
            elif self.currChar == '-' and self.isHR('-') == True:
                self.insertHR()
                self.blankFlag = False
            elif self.currChar == '-' and self.peekNext(1) == ' ':
                # Check the type of the current line
                # If it is not a checkmark or a bullet, it is treated as
                # plaintext
                tokenType = self.isCheckItemOrBullet()
                if tokenType == tokType.CHECKMARK:
                    self.tokenizeCheckItem()
                elif tokenType == tokType.BULLET:
                    self.tokenizeBullet()
            # Bullet starting with a +
            elif self.currChar == "+" and self.peekNext() == " ":
                self.tokenizeBullet()
            # Bullet starting with a *
            elif self.currChar == "*":
                if self.isHR("*") == True:
                    self.insertHR()
                elif self.peekNext() == " ":
                    self.tokenizeBullet()
            # Numbered Bullets
            elif str.isdigit(self.currChar) and self.isNumBullet() == True:
                self.tokenizeBullet()
            # Case of plain text
            else:
                self.tokenizeText()

    
        self.closeBlock()
        # Add an EOF token to signify end of file
        self.document.append({"type": "EOF"})

    def returnTokenList(self):
        """ Return the list of tokens which outlines the entire structure of the document"""
        return self.document


# temp test
if __name__ == "__main__":
 src = open("test.md", "r")
 tok = mdTokenizer(src)
 tok.tokenize()
 print(tok.returnTokenList())
