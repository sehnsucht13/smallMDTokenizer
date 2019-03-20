class mdTokenizer:
    """Class which tokenizes a markdown line"""
    def __init__(self, templateText):
        self.text = templateText
        self.currIndex = 0
        self.lookAhead = 0
        self.lineNum = 0
        self.tokens = []

    def skipWhiteSpace(self):
        """Skips all whitespace until the next character is encountered"""
        while(self.text[self.currIndex] == ' '):
            self.currIndex += 1

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
        self.tokens.append({"type":"Heading", "size":headingSize, "text":headingText})

    def tokenizeText(self):
        """Tokenizes a line of (for now) plain text"""
        textContent = ""
        self.skipWhiteSpace()
        while(self.text[self.currIndex] != '\n'):
            textContent += self.text[self.currIndex]
            self.currIndex += 1

        self.tokens.append({"type": "Text", "text": textContent})

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
        self.tokens.append({"type": "Link", "title": linkTitle, "path": linkPath})

    def tokenizeImage(self):
        """ Tokenizes an image link """
        # skip over the ! char which indicates that it is an image
        self.currIndex += 1
        # The image link in standard markdown is just like the standard link
        self.tokenizeLink() 

    def returnTokenList(self):
        return self.tokens

# some small tests below
test = "  [   here is my link]     (here is my path)"

output = mdTokenizer(test)
output.tokenizeLink()
print(output.returnTokenList())
