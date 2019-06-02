from enum import Enum, auto


class tokType(Enum):
    # Heading starting with a #
    MHEADING = auto()
    # Underlined heading
    UHEADING = auto()
    # Checkmark
    CHECKMARK = auto()
    # Regular link(anything but an image link)
    LINK = auto()
    # Plain text in a heading. No markup is recognized
    PLAIN = auto()
    # Marked up text
    MARKUPTEXT = auto()
    # Bullet mark
    BULLET = auto()
    # End of line
    EOL = auto()
    # End of file
    EOF = auto()
    # Code block
    CBLOCK = auto()
    # Blank line
    BLANK = auto()
    # left run Italic
    LITALIC = auto()
    # Right run italic
    RITALIC = auto()
    # Left run bold
    LBOLD = auto()
    # Right run bold
    RBOLD = auto()
    # Indent
    INDENT = auto()
    # Block Quotes
    BLOCKQUOTE = auto()
    # Image
    IMAGE = auto()
    # Inline Code
    ICODE = auto()
    # Horizontal Rule
    HR = auto()
    # Numbered bullet
    NUMBULLET = auto()
    # Crossed out text
    CROSS = auto()
