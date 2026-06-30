from dataclasses import dataclass
from enum import Enum, auto


class TokenType(Enum):
    # keywords
    VAR = auto()
    CONST = auto()
    IF = auto()
    ELSE = auto()
    FOR = auto()
    FUCK = auto()
    RET = auto()
    PUTS = auto()
    TRUE = auto()
    FALSE = auto()
    INT_TYPE = auto()
    FLT_TYPE = auto()
    CHR_TYPE = auto()
    STR_TYPE = auto()
    BOO_TYPE = auto()
    VOID_TYPE = auto()

    # identifier and literals
    IDENTIFIER = auto()
    INT = auto()
    FLT = auto()
    CHR = auto()
    STR = auto()
    BOO = auto()

    # operators
    ASSIGN = auto()
    PLUS = auto()
    MINUS = auto()
    ASTERISK = auto()
    SLASH = auto()
    MOD = auto()

    # relational operators
    LT = auto()
    GT = auto()
    LE = auto()
    GE = auto()
    EQ = auto()
    NE = auto()

    # logical operators
    AND = auto()
    OR = auto()
    NOT = auto()

    # delimiters
    LPAREN = auto()
    RPAREN = auto()
    LBRACE = auto()
    RBRACE = auto()
    COMMA = auto()
    SEMICOLON = auto()

    # special
    EOF = auto()


KEYWORDS: dict[str, TokenType] = {
    "var": TokenType.VAR,
    "const": TokenType.CONST,
    "if": TokenType.IF,
    "else": TokenType.ELSE,
    "for": TokenType.FOR,
    "fuck": TokenType.FUCK,
    "ret": TokenType.RET,
    "puts": TokenType.PUTS,
    "true": TokenType.TRUE,
    "false": TokenType.FALSE,
    "void": TokenType.VOID_TYPE,
    "int": TokenType.INT_TYPE,
    "flt": TokenType.FLT_TYPE,
    "chr": TokenType.CHR_TYPE,
    "str": TokenType.STR_TYPE,
    "boo": TokenType.BOO_TYPE,
}


@dataclass
class Token:
    type: TokenType
    lexeme: str
    line: int
    column: int

    def __repr__(self) -> str:
        return (
            f"{self.type}, lexeme: {self.lexeme!r}, "
            f"line: {self.line}, column: {self.column}"
        )
