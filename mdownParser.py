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


class mdTokenizer:
    """Class which tokenizes a markdown line"""

    def __init__(self, source):
        self.src = source
        self.text = ""
        self.currIndex = 0
        self.EOLToken = {"type": "EOL"}
        self.tokens = []

    def skipWhiteSpace(self):
        """Skips all whitespace until the next character is encountered"""
        while(self.text[self.currIndex] == ' '):
            self.currIndex += 1

    def skipWhiteSpaceNewLine(self):
        # Reset current index
        self.currIndex = 0
        self.skipWhiteSpace()

    def tokenizeHeading(self):
        """Tokenizes a standard markdown heading"""
        # Check if the first char in stream is #
        headingSize = 0
        headingText = ""
        while(self.text[self.currIndex] == '#'):
            headingSize += 1
            self.currIndex += 1
        # Skip over intial whitespace
        self.skipWhiteSpace()
        # Add contents of heading
        while(self.text[self.currIndex] != '\n'):
            headingText += self.text[self.currIndex]
            self.currIndex += 1

        # Append to token list
        self.tokens.append(
            {"type": "Heading", "size": headingSize, "text": headingText})
        self.tokens.append(self.EOLToken)

    def tokenizeText(self):
        """Tokenizes a line of (for now) plain text"""
        textContent = ""
        self.skipWhiteSpace()
        while(self.text[self.currIndex] != '\n'):
            textContent += self.text[self.currIndex]
            self.currIndex += 1

        self.tokens.append({"type": "Text", "text": textContent})
        self.tokens.append(self.EOLToken)

    def tokenizeLink(self):
        """Tokenizes a standard markdown link"""
        linkTitle = ""
        linkPath = ""
        self.skipWhiteSpace()
        self.currIndex += 1
        self.skipWhiteSpace()
        while(self.text[self.currIndex] != ']'):
            linkTitle += self.text[self.currIndex]
            self.currIndex += 1

        # Skip over the ] character
        self.currIndex += 1
        self.skipWhiteSpace()
        # Skip over (
        self.currIndex += 1
        self.skipWhiteSpace()
        while(self.text[self.currIndex] != ')'):
            linkPath += self.text[self.currIndex]
            self.currIndex += 1

        self.currIndex += 1
        self.tokens.append(
            {"type": "Link", "title": linkTitle, "path": linkPath})

    def tokenizeImage(self):
        """ Tokenizes an image link """
        # skip over the ! char which indicates that it is an image
        self.currIndex += 1
        # The image link in standard markdown is just like the standard link
        self.tokenizeLink()

    def tokenizeCheckItem(self):
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
        self.tokens.append(self.EOLToken)

    def tokenizeCodeBlock(self):
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
        return self.tokens

    def tokenize(self):
        while(src.checkEOF()):
            self.text = self.src.returnLine()
            self.skipWhiteSpaceNewLine()
            if(self.text[self.currIndex] == '#'):
                self.tokenizeHeading()
            elif(self.text[self.currIndex] == '-'):
                self.tokenizeCheckItem()
            elif(self.text[self.currIndex] == '!'):
                self.tokenizeImage()
            elif(self.text[self.currIndex] == '['):
                self.tokenizeLink()
            elif(str.isalnum(self.text[self.currIndex])):
                self.tokenizeText()
            else:
                print("Cannot parse this string")
                break

            # some small tests below
            #test = " -           [ ]            Here is some content for my check list item\n"


if __name__ == "__main__":
    src = streamSource("test.md")
    tok = mdTokenizer(src)
    tok.tokenize()
    print(tok.returnTokenList())
