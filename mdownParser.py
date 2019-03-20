class mdTokenizer:
    def __init__(self, templateText):
        self.text = templateText
        self.currIndex = 0
        self.lookAhead = 0
        self.lineNum = 0
        self.tokens = []

    def skipWhiteSpace(self):
        while(self.text[self.currIndex] == ' '):
            self.currIndex += 1

    def tokenizeHeading(self):
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
        textContent = ""
        self.skipWhiteSpace()
        while(self.text[self.currIndex] != '\n'):
            textContent += self.text[self.currIndex]
            self.currIndex += 1

        self.tokens.append({"type": "Text", "text": textContent})

    def tokenizeLink(self):
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
            

    def returnTokenList(self):
        return self.tokens

test = "[here is my link](here is my path)"

output = mdTokenizer(test)
output.tokenizeLink()
print(output.returnTokenList())
