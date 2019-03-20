class mdTokenizer:
    def __init__(self, templateText):
        self.text = templateText
        self.currIndex = 0
        self.lookAhead = 0
        self.lineNum = 0
        self.tokens = []

    def tokenizeHeading(self, text):
        # Check if the first char in stream is #
        headingSize = 0
        headingText = ""
        while(text[self.currIndex] == '#'):
            headingSize += 1
            self.currIndex += 1
        # Skip over intial whitespace
        while(text[self.currIndex] == ' '):
            self.currIndex += 1
        print(self.currIndex)
        while(text[self.currIndex] != '\n'):
            headingText += text[self.currIndex]
            self.currIndex += 1

        # Append to token list
        self.tokens.append({"size":headingSize, "text":headingText})

    def returnTokenList(self):
        return self.tokens

test = "### Hello world\n"

output = mdTokenizer(test)
output.tokenizeHeading(test)
print(output.returnTokenList())
