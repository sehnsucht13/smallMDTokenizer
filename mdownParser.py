class mdParser(self, text):
    def tokenizeHeading(self, text):
        # Check if the first char in stream is #
        headingSize = 0
        headingText = ""
        currIndex = 0
        while(text[currIndex] == '#'):
            headingSize += 1
            currIndex += 1
        print(currIndex)
        # Skip over intial whitespace
        while(text[currIndex] == ' '):
            currIndex += 1

        print(currIndex)
        while(currIndex < len(text)):
            headingText += text[currIndex]
            currIndex += 1

        return {"size":headingSize, "text":headingText}


test = "#   Hello world"

output = tokenizeHeading(test)
print(output)
htmlOutput = "<h" + str(output['size']) + "> " + str(output['text']) + " </h" + str(output['size']) + ">"
print(htmlOutput)


        

