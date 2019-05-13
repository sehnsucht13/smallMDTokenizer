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

from stream import streamSource
import sys   # used to exit program when an undesirable state occurs
from tokenType import tokType


class mdTokenizer:
    """Class which tokenizes a markdown file by iterating through it line
    by line"""

    def __init__(self, source):
        # Holds a handle to the source class which restricts access to the

        # source file
        self.src = source
        # The current line of text
        self.text = ""
        # The current character
        self.currChar = ''
        # Current index along the line
        self.currIndex = 0
        # The list of tokens
        self.tokens = []

    def getNext(self):
        """ Return the next character in the current line"""
        self.currIndex += 1
        self.currChar = self.text[self.currIndex]
        return self.currChar

    def peekNext(self, n=1):
        """ Return the next character without incrementing the position"""
        return self.text[self.currIndex + n]

    def skipWhiteSpace(self):
        """Skips all whitespace until the next character is encountered"""
        while self.currChar == ' ':
            self.getNext()

    def skipWhiteSpaceNewLine(self):
        """Resets the current index and consumes whitespace until an any
        character which is not space is reached"""
        # Reset current index
        self.currIndex = 0
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
        if self.currChar == '\n' or self.currChar == '\r':
            return True
        return False

    def addEOL(self):
        """Adds an end of line token to the token list"""
        self.tokens.append({"type": tokType.EOL})

    def getNewLine(self):
        """ Get and set the next line from the source file """
        self.text = self.src.returnLine()
        self.currIndex = 0
        self.currChar = self.text[self.currIndex]

    def eatCharsPlain(self):
        """Consumes characters and returns them to the calling function in the form of
        a string. This function assumes that what is to be consumed is only
        plain characters without any markup. Used for headings"""
        itemText = ""
        while self.currChar != '\n':
            print(self.currChar)
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
        self.addEOL()

    def tokenizeUnmarkedHeading(self):
        """ Tokenize headings which are underlined """
        textContent = self.eatCharsMarkup()
        # skip over the next line since it is useless to parse
        src.returnLine()
        self.tokens.append({
            "type": tokType.UHEADING,
            "content": textContent
        })
        self.addEOL()

    def tokenizeText(self):
        """Tokenizes a line of marked up text"""
        # Case of an empty line
        if self.currChar == '\n':
            self.tokens.append({
                "type": tokType.BLANK
            })
        # Case of any other text
        else:
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

    def tokenizeBullet(self):
        """ Tokenize a markdown bullet """
        # skip over + or - or *
        self.getNext()
        self.currIndex += 1
        self.skipWhiteSpace()
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

    def returnTokenList(self):
        """ Return the list of tokens """
        return self.tokens

    def isHR(self, char):
        """ Count the occurence of a certain type of character on a line of 
            text. Used to detect line rules."""
        count = 1
        pos = 1
        while self.peekNext(pos) == char:
            count += 1
            pos += 1
            print("Yea")
        print(count)
        if self.peekNext(pos) == '\n' and count >= 3:
            return True
        else:
            return False

    def insertHR(self):
        """ Insert a horizontal rule token into the token stream """
        self.tokens.append({
            "type": tokType.HR
            })

    def tokenize(self):
        """ General driver of the entire tokenizer. 
            It applies the tokenizing rules based on the context detected
            by the first character of the stream which has not yet been consumed """
        while self.src.checkEOF():
            self.getNewLine()
            self.skipWhiteSpaceNewLine()
            # Standard heading starting with #
            if self.currChar == '#' and self.peekNext() == ' ':
                self.tokenizeMarkedHeading()
            # Underlined heading
            elif src.lookAheadLineTest("^(-{3,}|={3,})"):
                self.tokenizeUnmarkedHeading()
            elif self.currChar == '_':
                if self.isHR('_') == True:
                    self.insertHR()
            # Either a bullet or checklist item
            elif self.currChar == '-': 
                if self.isHR('-') == True:
                    self.insertHR()
                elif self.isCheckItemOrBullet() == 1:
                    print("bullet")
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
                print("Exit bullet case")
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
            elif str.isdigit(self.currChar) and self.peekNext(1) == '.' and self.peekNext(2) == ' ':
                self.tokenizeBullet()
            else:
                self.tokenizeText()

        # Add an EOF token
        self.tokens.append({"type": "EOF"})


# temp test
if __name__ == "__main__":
   src = streamSource("test.md")
   tok = mdTokenizer(src)
   tok.tokenize()
   print(tok.returnTokenList())
