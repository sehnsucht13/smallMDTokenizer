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

import sys   # used to exit program when an undesirable state occurs
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
        # The current character
        self.currChar = ''
        # Current index along the source
        self.currIndex = 0
        # The list of tokens created
        self.tokens = []
        self.blankFlag = False

    def getNext(self):
        """ Return the next character in the current line"""
        self.currIndex += 1
        self.currChar = self.text[self.currIndex]
        return self.currChar

    def peekNext(self, n=1):
        """ Return the next character without incrementing the position"""
        if(n + self.currIndex == self.EOF):
            print("True")
            return '\n'
        else:
            return self.text[self.currIndex + n]

    def skipWhiteSpace(self):
        """Skips all whitespace until the next character is encountered"""
        while self.currChar == ' ':
            self.getNext()

    def skipWhiteSpaceNewLine(self):
        """Resets the current index and consumes whitespace until an any
        character which is not space is reached"""
        # Used to measure indentation levels for lists within lists
        spaceNumberCount = 0
        # Iterate and count until we reach anything which is not a space
        while self.currChar == ' ':
            spaceNumberCount += 1
            self.getNext()

        # If the number of spaces is more than 0 then we have indented text
        if spaceNumberCount != 0:
            self.tokens.append({
                    "type": tokType.INDENT,
                    "count": spaceNumberCount
                })


    def checkEmptyLine(self):
        """Check if the current line is an empty line"""
        if self.currChar == '\n': 
            return True
        return False

    def addEOL(self):
        """Adds an end of line token to the token list"""
        self.tokens.append({"type": tokType.EOL})

    def eatCharsPlain(self):
        """Consumes characters and returns them to the calling function in the form of
        a string. This function assumes that what is to be consumed is only
        plain characters without any markup. Used for headings"""
        itemText = ""
        while self.currChar != '\n':
            itemText += self.currChar
            self.getNext()
        return itemText

    def eatCharsMarkup(self):
        """Consume characters which are using some type of markup such as * or **"""
        textArr = []
        while self.currChar != '\n':
            # Case of bold text like **WORD**
            if (self.currChar == '*' and self.peekNext() == '*') or (self.currChar == '_' and self.peekNext() == '_'):
                # Skip over the following *
                self.getNext()
                self.getNext()
                # Add token for bolded text
                textArr.append({
                    "type": tokType.BOLD,
                })

            # Case of italic text like *WORD*
            elif self.currChar == "*" or self.currChar == '_':
                # Skip over * to next character
                self.getNext()

                # Add token for italic text
                textArr.append({
                    "type" : tokType.ITALIC
                })

            # Inline code
            elif self.currChar == '`':
                # skip over the `
                self.getNext()
                # Add token
                textArr.append({
                    "type": tokType.ICODE     
                })

            # Small addition to regular grammar which supports crossed out text
            elif self.currChar == '~' and self.peekNext() == '~':
                self.getNext()
                self.getNext()
                textArr.append({
                    "type": tokType.CROSS
                })

            # Default case for plain text
            else:
                textContent = ""
                while self.currChar not in ['\n', '*', '_', '[', '`']:
                    textContent += self.currChar
                    self.getNext()

                # Add token for plain text with its content
                textArr.append({
                    "type": tokType.PLAIN,
                    "content": textContent
                })

        return textArr

    def tokenizeMarkedHeading(self):
        """Tokenizes a standard markdown heading"""
        headingSize = 1
        headingText = ""

        while self.getNext() == '#':
            if headingSize != 6:
                headingSize += 1

        # Skip over intial whitespace
        self.skipWhiteSpace()
        
        # Add contents of heading
        headingText = self.eatCharsMarkup()

        # Append to token list
        self.tokens.append({
            "type": tokType.MHEADING,
            "size": headingSize,
            "content": headingText
        })

    def tokenizeUnmarkedHeading(self):
        """ Tokenize headings which are underlined """
        textContent = self.eatCharsMarkup()
        # skip over the next line since it is useless to parse
        while self.currChar != '\n':
            self.getNext()

        self.tokens.append({
            "type": tokType.UHEADING,
            "content": textContent
        })

    def tokenizeText(self):
        """Tokenizes a line of marked up text"""
        # Case of an empty line
        if self.currChar == '\n':
            self.blankFlag = True
            self.tokens.append({
                "type": tokType.BLANK
            })

        # Case of any other text
        else:
            self.blankFlag = False
            textContent = self.eatCharsMarkup()
            self.tokens.append({
                "type": tokType.MARKUPTEXT,
                "content": textContent
                })


    def tokenizeLink(self):
        """Tokenizes a standard markdown link"""
        linkTitle = ""
        linkPath = ""
        self.skipWhiteSpace()
        self.getNext()
        self.skipWhiteSpace()
        while self.getNext() != ']':
            linkTitle += self.currChar

        # Skip over the ] character
        self.getNext()
        self.skipWhiteSpace()
        # Skip over (
        self.getNext()
        self.skipWhiteSpace()
        while self.getNext() != ')':
            linkPath += self.currChar

        self.tokens.append({
            "type": tokType.LINK, 
            "title": linkTitle, 
            "path": linkPath
            })

    def tokenizeImage(self):
        """ Tokenizes an image link """
        imgDesc = ""
        imgURL = ""
        imgTitle = ""

        if(self.currChar == '!'):
            self.getNext()

        # Skip over the opening [ bracket
        self.getNext()
        
        # retrieve the description
        while self.currChar != ']':
            imgDesc += self.currChar
            self.getNext()
        
        print(imgDesc)
        # Skip over the closing ] bracket
        self.getNext()
        # Skip over the (
        self.getNext()

        # Retrieve the url
        while self.currChar not in ['"', ')']:
            imgURL += self.currChar
            self.getNext()

        print(imgURL)

        # Retrieve the link title
        if self.currChar == '"':
            self.getNext()
            while self.currChar != '"':
                imgTitle += self.currChar
                self.getNext()


        # skip over the )
        self.getNext()
        self.getNext()

        self.tokens.append({
                "type": tokType.IMAGE,
                "desc": imgDesc,
                "url": imgURL,
                "title": imgTitle
            })


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

        if self.currChar == 'x':
            status = True

        # Skip over the closing ]
        self.getNext()
        self.getNext()
        self.skipWhiteSpace()
        
        checkItemContent = self.eatCharsMarkup()
        self.tokens.append({
            "type": tokType.CHECKMARK,
            "status": status,
            "content": checkItemContent
        })
        self.addEOL()

    def isCheckItemOrBullet(self):
        """Check if the current line is a simple list bullet or is a checkmark"""
        # Used to look ahead in the string
        lookAheadIndex = self.currIndex + 1
        while lookAheadIndex != len(self.text):
            if self.text[lookAheadIndex] == '[':
                return 1
            lookAheadIndex += 1

    def isNumBullet(self):
        """ Check if the current line starting with a number is a 
            numbered bullet or a regular line of markdown text"""
        pos = 0
        # Skip numbers on the line
        while str.isdigit(self.peekNext(pos)):
            pos += 1
        # Check if the bullet is the required format
        if self.peekNext(pos) == '.' and self.peekNext(pos + 1) == ' ':
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
            text = self.eatCharsMarkup()
            self.tokens.append({
                "type": tokType.NUMBULLET,
                "content": text
            })

        # Case of a regular bullet
        else:
            print("Here is the bullet")
            print(self.currChar)
            # Skip over the *, - or +
            self.getNext()
            # Skip over the whitespace
            self.skipWhiteSpace()
            
            # Consume the characters
            text = self.eatCharsMarkup()
            self.tokens.append({
                "type": tokType.BULLET,
                "content": text
            })

    def tokenizeCodeBlock(self):
        """ Tokenize a code block. """
        tickCount = 0
        lang = ""
        codeBlockContent = []
        while(self.currChar == '`'):
            tickCount += 1
            self.getNext()
        if(tickCount == 3):
            # Consume characters
            lang = self.eatCharsPlain()
            # get next line
            self.getNewLine()
            while self.currChar != '`':
                if self.checkEmptyLine():
                    print("Detected blank line")
                    codeBlockContent.append({
                        "type": "BLANK"
                    })
                    print("Got to here")
                    self.getNewLine()
                else:
                    # Consume entire line
                    lineContent = self.eatCharsPlain()
                    codeBlockContent.append({
                        "line": lineContent
                    })
                    print("Got to else")
                    self.getNewLine()

            tickCount = 0
            while self.currChar == '`':
                tickCount += 1
                self.getNext()

            # Case of malformed block
            if tickCount != 3:
                errString = """Malformed code block ending at line: {}\nMissing {} tickmark""".format(
                    src.getLineNum(), (3 - tickCount))
                sys.exit(errString)

            # At this point, we have a line with the form of ```
            self.tokens.append({
                "type": tokType.CBLOCK,
                "lang": lang,
                "content": codeBlockContent
            })

        else:
            errString = "Error recognizing markdown syntax at line number: {} ".format(
                src.getLineNum)
            sys.exit(errString)


    def isHR(self, char):
        """ Count the occurence of a certain type of character on a line of 
            text. Used to detect line rules."""
        count = 1
        pos = 1
        while self.peekNext(pos) == char:
            count += 1
            pos += 1
        if self.peekNext(pos) == '\n' and count >= 3 and self.blankFlag == True:
            return True
        else:
            return False

    def insertHR(self):
        """ Insert a horizontal rule token into the token stream """
        while self.currChar != '\n':
            self.getNext()

        self.getNext()
        self.tokens.append({
            "type": tokType.HR
            })

    def isUnderlinedHeading(self):
        # starting position of next line
        startPos = 1
        # End position of next line. Represents \n
        endPos = 0
        # Find the beginning of next string
        while self.peekNext(startPos) != '\n':
            startPos += 1

        # At this point, startPos points to the index of \n
        startPos += 1

        endPos = startPos
        startPos += self.currIndex

        # Find the end of next string
        while self.peekNext(endPos) != '\n':
            endPos += 1

        endPos += self.currIndex
        endPos += 1 

        string = self.text[startPos:endPos]
        print(string)
        searchExp = re.compile("^(-{3,}|={3,})\n")
        print(len(string))
        output = searchExp.fullmatch(string)

        return output

    def tokenize(self):
        """ General driver of the entire tokenizer. 
            It applies the tokenizing rules based on the context detected
            by the first character of the stream which has not yet been consumed """
        while self.currIndex + 1 != self.EOF:
            if self.currChar == '\n':
                self.getNext()
            self.skipWhiteSpaceNewLine()
            # Standard heading starting with #
            if self.currChar == '#': 
                self.tokenizeMarkedHeading()
            # Underlined heading
            elif self.isUnderlinedHeading():
                self.tokenizeUnmarkedHeading()
            elif self.currChar == '_':
                if self.isHR('_') == True:
                    self.insertHR()
            # Either a bullet or checklist item
            elif self.currChar == '-': 
                if self.isHR('-') == True:
                    self.insertHR()
                    self.blankFlag = False
                elif self.isCheckItemOrBullet() == 1:
                    self.tokenizeCheckItem()
                else:
                    self.tokenizeBullet()
            # Bullet starting with a +
            elif self.currChar == '+' and self.peekNext() == ' ':
                self.tokenizeBullet()
            # Bullet starting with a *
            elif self.currChar == '*':
                if self.isHR('*') == True:
                    self.insertHR()
                elif self.peekNext() == ' ':
                    self.tokenizeBullet()
            # Image link
            elif self.currChar == '!' and self.peekNext() == '[':
                self.tokenizeImage()
            # Normal link
            elif self.currChar == '[':
                self.tokenizeLink()
            # Code blocks
            elif self.currChar == '`' and self.peekNext() == '`' and self.peekNext(2) == '`':
                self.tokenizeCodeBlock()
            # Numbered Bullets
            elif str.isdigit(self.currChar) and self.isNumBullet() == True:
                self.tokenizeBullet()
            else:
                self.tokenizeText()

        # Add an EOF token
        self.tokens.append({"type": "EOF"})

    def returnTokenList(self):
        """ Return the list of tokens """
        return self.tokens

# temp test
if __name__ == "__main__":
   src = open("test.md", "r")
   tok = mdTokenizer(src)
   tok.tokenize()
   print(tok.returnTokenList())
