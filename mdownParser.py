from stream import streamSource


class mdTokenizer:
    """Class which tokenizes a markdown line"""

    def __init__(self, source):
        self.src = source
        self.text = ""
        self.currChar = ''
        self.currIndex = 0
        self.tokens = []

    def skipWhiteSpace(self):
        """Skips all whitespace until the next character is encountered"""
        while(self.text[self.currIndex] == ' '):
            self.currIndex += 1

    def skipWhiteSpaceNewLine(self):
        """Resets the current index and consumes whitespace until a character is reached"""
        # Reset current index
        self.currIndex = 0
        self.skipWhiteSpace()

    def getNextChar(self):
        """ Return the next character """
        self.currChar = self.text[self.currIndex]
        self.currIndex += 1
        return self.currChar

    def peekNextChar(self):
        """ Return the next character """
        return self.text[self.currIndex]

    def getNewLine(self):
        """ Get and set the next line from the source file """
        self.text = self.src.returnLine()
        self.currIndex = 0
        self.currChar = self.text[self.currIndex]

    def eatCharsPlain(self):
        """Consumes characters and returns them to the calling function in the form of
        a string. This function assumes that what is to be consumed is only plain 
        characters without any markup. Used for headings"""
        itemText = ""
        while(self.getNextChar() != '\n'):
            itemText += self.currChar
        return itemText

    def eatCharsMarkup(self):
        textArr = []
        while(self.currChar != '\n'):
            # Case of bold text like **WORD**
            if(self.currChar == "*" and self.peekNextChar() == "*"):
                print("Detected double bold")
                boldText = ""
                # Skip over the following *
                self.getNextChar()
                self.getNextChar()
                while(self.currChar != "*"):
                    boldText += self.currChar
                    self.getNextChar()

                # at this point, currChar is on the first closing *
                # Move to second *
                self.getNextChar()
                # Now skipped over ** completely
                self.getNextChar()
                # Add token for bolded text
                textArr.append({
                    "type" : "Text",
                    "markup" : "B",
                    "text" : boldText
                    })

            # Case of italic text like *WORD*
            elif(self.currChar == "*"):
                print("Detected single italic")
                italicText = ""
                # Skip over to next character
                self.getNextChar()
                while(self.currChar != "*"):
                    italicText += self.currChar
                    self.getNextChar()
                # At this point, currChar is on a *
                self.getNextChar()
                print("Here is the char " + self.currChar)
                textArr.append({
                    "type" : "Text",
                    "markup" : "I",
                    "text" : italicText
                    })
            # Default case for plain text
            else:
                plainText = ""
                while self.currChar != '\n' and self.currChar != '*':
                    plainText += self.currChar
                    self.getNextChar()
                textArr.append({
                    "type" : "Text",
                    "markup" : "P",
                    "text" : plainText
                    })

        return textArr
        

    def addEOL(self):
        """Adds an end of line token to the token list"""
        self.tokens.append({"type": "EOL"})

    def tokenizeMarkedHeading(self):
        """Tokenizes a standard markdown heading"""
        # Check if the first char in stream is #
        headingSize = 0
        headingText = ""
        while(self.getNextChar() == '#'):
            headingSize += 1

        # Skip over intial whitespace
        self.skipWhiteSpace()
        # Add contents of heading
        headingText = self.eatCharsPlain()
        # Append to token list
        self.tokens.append(
            {"type": "Heading", "size": headingSize, "text": headingText})
        self.addEOL()

    def tokenizeText(self):
        """Tokenizes a line of (for now) plain text"""
        textContent = self.eatCharsMarkup()
        self.tokens.append({"type": "Text", "text": textContent})
        self.addEOL()

    def tokenizeUnmarkedHeading(self):
        """ Tokenize headings which are underlined """
        textContent = ""
        while(self.getNextChar() != '\n'):
            textContent += self.currChar
        src.returnLine()
        self.tokens.append({
            "type": "Heading",
            "text": textContent
        })
        self.addEOL()

    def tokenizeLink(self):
        """Tokenizes a standard markdown link"""
        linkTitle = ""
        linkPath = ""
        self.skipWhiteSpace()
        self.currIndex += 1
        self.skipWhiteSpace()
        while(self.getNextChar() != ']'):
            linkTitle += self.currChar

        # Skip over the ] character
        self.currIndex += 1
        self.skipWhiteSpace()
        # Skip over (
        self.currIndex += 1
        self.skipWhiteSpace()
        while(self.getNextChar() != ')'):
            linkPath += self.currChar

        self.tokens.append(
            {"type": "Link", "title": linkTitle, "path": linkPath})

    def tokenizeImage(self):
        """ Tokenizes an image link """
        # skip over the ! char which indicates that it is an image
        self.currIndex += 1
        # The image link in standard markdown is just like the standard link
        self.tokenizeLink()

    def tokenizeCheckItem(self):
        """ Tokenize a checklist item of the form:
            - [ ] ITEM """
        status = None
        checkItemContent = ""
        self.skipWhiteSpace()
        # Skip over the -
        self.currIndex += 1
        self.skipWhiteSpace()
        # Skip over [
        self.currIndex += 1

        if(self.text[self.currIndex] == 'x'):
            status = True

        # Skip over ]
        self.currIndex += 1
        self.currIndex += 1
        self.skipWhiteSpace()
        while(self.text[self.currIndex] != '\n'):
            checkItemContent += self.text[self.currIndex]
            self.currIndex += 1

        self.tokens.append(
            {"type": "Check", "status": status, "text": checkItemContent})
        self.addEOL()

    def isCheckItemOrBullet(self):
        """Check if the current line is a simple list bullet or is a checkmark"""
        # Used to look ahead in the string
        lookAheadIndex = self.currIndex + 1
        while(lookAheadIndex != len(self.text)):
            if(self.text[lookAheadIndex] == '['):
                return 1
            lookAheadIndex += 1

    def tokenizeBullet(self):
        """ Tokenize a markdown bullet """
        # skip over + or - or *
        self.currIndex += 1
        self.skipWhiteSpace()
        text = self.eatChars()
        self.tokens.append(
            {"type": "Bullet", "text": text}
        )

    def tokenizeCodeBlock(self):
        """ Tokenize a code block """
        tickCount = 0
        while(self.text[self.currIndex] == '`'):
            tickCount += 1
            self.currIndex += 1
        if(tickCount == 3):
            # get next line
            pass
        else:
            print("Malformed code block\n")

    def returnTokenList(self):
        """ Return the list of tokens """
        return self.tokens

    def tokenize(self):
        """ General function which applies the tokenizing rules based on the context"""
        while(src.checkEOF()):
            self.getNewLine()
            self.skipWhiteSpaceNewLine()
            # Standard heading starting with #
            if(self.text[self.currIndex] == '#'):
                print("Tripped test 1")
                self.tokenizeMarkedHeading()
            # Underlined heading
            elif(src.lookAheadLineTest("^(-{2,}|={2,})")):
                print("Tripped test 2")
                self.tokenizeUnmarkedHeading()
            # Either a bullet or checklist item
            elif(self.text[self.currIndex] == '-'):
                print("Tripped test 3")
                if(self.isCheckItemOrBullet() == 1):
                    self.tokenizeCheckItem()
                else:
                    self.tokenizeBullet()
            # Image link 
            elif(self.text[self.currIndex] == '!'):
                print("Tripped test 4")
                self.tokenizeImage()
            # Normal link
            elif(self.text[self.currIndex] == '['):
                print("Tripped test 5")
                self.tokenizeLink()
            # Bullet
            elif(self.text[self.currIndex] == '+'):
                print("Tripped test 6")
                self.tokenizeBullet()
            # Bullet
            elif(self.text[self.currIndex] == '*' and self.peekNextChar() == " "):
                print("Tripped test 7")
                self.tokenizeBullet()
            # Plain sentence
            elif(str.isalnum(self.currChar)):
                print("Tripped test 8")
                self.tokenizeText()
            # Blank line
            elif(len(self.text) == 0):
                print("Tripped test BLANK")
                self.tokens.append({"type": "BLANK"})
            # Unhandled case
            else:
                pass
        # Add an EOF token
        self.tokens.append({"type": "EOF"})


if __name__ == "__main__":
    src = streamSource("test.md")
    tok = mdTokenizer(src)
    tok.tokenize()
    print(tok.returnTokenList())
