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


class HTMLConverter():
    def __init__(self, tokenStream):
        self.tokens = tokenStream
        self.currIndex = 0

    def peek(self):
        return self.tokens.pop(self.currIndex)

    def next(self):
        return self.tokens[self.currIndex + 1]

    def convertText(self):
        pass

    def convertHeading(self):
        """ Convert a heading to html"""
        tok = self.peek()
        size = tok['size']
        content = tok['content']
