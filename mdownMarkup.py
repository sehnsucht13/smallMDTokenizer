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

def tokenizeImage(self):
    """ Tokenizes an image link """
    imgDesc = ""
    imgURL = ""
    imgTitle = ""

    if self.currChar == "!":
        self.getNext()

    # Skip over the opening [ bracket
    self.getNext()

    # retrieve the description
    while self.currChar != "]":
        imgDesc += self.currChar
        self.getNext()

    # Skip over the closing ] bracket
    self.getNext()
    # Skip over the (
    self.getNext()

    # Retrieve the url
    while self.currChar not in ['"', ")"]:
        imgURL += self.currChar
        self.getNext()

    # Retrieve the link title
    if self.currChar == '"':
        self.getNext()
        while self.currChar != '"':
            imgTitle += self.currChar
            self.getNext()

    # skip over the )
    self.getNext()
    self.getNext()

    self.tokens.append(
        {"type": tokType.IMAGE, "desc": imgDesc, "url": imgURL, "title": imgTitle}
    )

def tokenizeLink(self):
    """Tokenizes a standard markdown link"""
    linkTitle = ""
    linkPath = ""
    self.skipWhiteSpace()
    self.getNext()
    self.skipWhiteSpace()
    while self.getNext() != "]":
        linkTitle += self.currChar

    # Skip over the ] character
    self.getNext()
    self.skipWhiteSpace()
    # Skip over (
    self.getNext()
    self.skipWhiteSpace()
    while self.getNext() != ")":
        linkPath += self.currChar

    self.tokens.append({"type": tokType.LINK, "title": linkTitle, "path": linkPath})

def eatCharsMarkup(self):
    """Consume characters which are using some type of markup such as * or **"""
    textArr = []
    while self.currChar != "\n":
        # Case of bold text like **WORD**
        if (
            self.currChar == "*"
            and self.peekNext(1) == "*"
            and self.peekNext(2) != " "
        ) or (
            self.currChar == "_"
            and self.peekNext(1) == "_"
            and self.peekNext(2) != " "
        ):

            # Skip over * and *
            self.getNext()
            self.getNext()
            # Add token for the left run bolded
            textArr.append({"type": tokType.LBOLD})

        elif (
            self.peekPrev() != " "
            and self.currChar == "*"
            and self.peekNext(1) == "*"
        ) or (
            self.peekPrev() != " "
            and self.currChar == "_"
            and self.peekNext(1) == "_"
        ):
            # Skip over * and *
            self.getNext()
            self.getNext()
            textArr.append({"type": tokType.RBOLD})
            print("got rbold")

        # Case of italic text like *WORD*
        elif (self.currChar == "*" and self.peekNext(1) != " ") or (
            self.currChar == "_" and self.peekNext(1) != " "
        ):
            # Skip over * to next character
            self.getNext()
            # Add token for italic text
            textArr.append({"type": tokType.LITALIC})

        elif (self.currChar == "*" and self.peekPrev() != " ") or (
            self.currChar == "_" and self.peekPrev() != " "
        ):
            # Skip over * to next character
            self.getNext()
            # Add token for italic text
            textArr.append({"type": tokType.RITALIC})
        # Inline code
        elif self.currChar == "`":
            # skip over the `
            self.getNext()
            # Add token
            textArr.append({"type": tokType.ICODE})

        # Small addition to regular markdown markup which supports crossed out text
        # Uses ~~Crossed out text~~
        elif self.currChar == "~" and self.peekNext() == "~":
            self.getNext()
            self.getNext()
            textArr.append({"type": tokType.CROSS})

        # Default case for plain text
        else:
            textContent = ""
            while self.currChar not in ["\n", "*", "_", "[", "`", "("]:
                # Check for escape characters
                if self.currChar == "\\" and self.peekNext() in [
                    "(",
                    ")",
                    "[",
                    "]",
                    "\\",
                    "_",
                    "*",
                    "_",
                    ".",
                    "!",
                    "-",
                    "`",
                ]:
                    # Skip over the /
                    self.getNext()
                    # Add the escaped character as a normal one
                    textContent += self.currChar
                else:
                    textContent += self.currChar

                self.getNext()

            # Add token for plain text with its content
            textArr.append({"type": tokType.PLAIN, "content": textContent})

    return textArr

