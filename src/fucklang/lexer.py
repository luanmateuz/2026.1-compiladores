from fucklang.token import KEYWORDS, Token, TokenType


class Lexer:
    def __init__(self, source) -> None:
        self.source = source
        self.start = 0
        self.curr = 0
        self.line = 1
        self.line_start = 0
        self.tokens = []

    def advance(self):
        ch = self.source[self.curr]
        self.curr = self.curr + 1

        return ch

    def peek(self):
        if self.curr >= len(self.source):
            return "\0"
        return self.source[self.curr]

    def lookahead(self, n=1):
        if self.curr >= len(self.source):
            return "\0"
        return self.source[self.curr + n]

    def match(self, expected):
        if self.curr >= len(self.source):
            return False
        if self.source[self.curr] != expected:
            return False
        self.curr = self.curr + 1
        return True

    def handle_number(self):
        while self.peek().isdigit():
            self.advance()
        if self.peek() == "." and self.lookahead().isdigit():
            self.advance()  # consume the '.'
            while self.peek().isdigit():
                self.advance()
            self.add_token(TokenType.FLT)
        else:
            self.add_token(TokenType.INT)
        if self.peek().isalpha() or self.peek() == "_":
            bad_char = self.peek()
            raise SyntaxError(
                f"[Line {self.line}, Column {self.curr - self.line_start + 1}]"
                f" Error at '{bad_char}': Invalid number format."
            )

    def handle_character(self, start_quote):
        if self.peek() != start_quote and not (self.curr >= len(self.source)):
            self.advance()
        if self.curr >= len(self.source):
            raise SyntaxError(
                f"[Line {self.line}, Column {
                    self.start - self.line_start + 1
                }] Unterminated character."
            )
        if self.peek() != start_quote and not (self.curr >= len(self.source)):
            raise SyntaxError(
                f"[Line {self.line}, Column {
                    self.start - self.line_start + 1
                }] Unterminated character."
            )

        self.advance()  # consume the ending quote
        self.add_token(TokenType.CHR)

    def handle_string(self, start_quote):
        while self.peek() != start_quote and not (
            self.curr >= len(self.source)
        ):
            self.advance()
        if self.curr >= len(self.source):
            raise SyntaxError(
                f"[Line {self.line}, Column {
                    self.start - self.line_start + 1
                }] Unterminated string."
            )
        self.advance()  # consume the ending quote
        self.add_token(TokenType.STR)

    def handle_identifier(self):
        while self.peek().isalnum() or self.peek() == "_":
            self.advance()
        # check if the identifier matches a key in the keywords dict
        text = self.source[self.start : self.curr]
        keywork_type = KEYWORDS.get(text)
        if keywork_type is None:
            self.add_token(TokenType.IDENTIFIER)
        else:
            self.add_token(keywork_type)

    def add_token(self, token_type):
        column = self.start - self.line_start + 1
        self.tokens.append(
            Token(
                token_type,
                self.source[self.start : self.curr],
                self.line,
                column,
            )
        )

    def tokenize(self):
        while self.curr < len(self.source):
            self.start = self.curr
            ch = self.advance()
            if ch == "\n":
                self.line = self.line + 1
                self.line_start = self.curr
            elif ch == "\t":
                pass
            elif ch == "\r":
                pass
            elif ch == " ":
                pass
            elif ch == "#":
                while self.peek() != "\n" and not (
                    self.curr >= len(self.source)
                ):
                    self.advance()
            elif ch == "(":
                self.add_token(TokenType.LPAREN)
            elif ch == ")":
                self.add_token(TokenType.RPAREN)
            elif ch == "{":
                self.add_token(TokenType.LBRACE)
            elif ch == "}":
                self.add_token(TokenType.RBRACE)
            elif ch == "+":
                self.add_token(TokenType.PLUS)
            elif ch == "-":
                self.add_token(TokenType.MINUS)
            elif ch == "*":
                self.add_token(TokenType.ASTERISK)
            elif ch == "/":
                self.add_token(TokenType.SLASH)
            elif ch == "%":
                self.add_token(TokenType.MOD)
            elif ch == ",":
                self.add_token(TokenType.COMMA)
            elif ch == ";":
                self.add_token(TokenType.SEMICOLON)
            elif ch == ":":
                if self.match("="):
                    self.add_token(TokenType.ASSIGN)
                else:
                    raise SyntaxError(
                        f"[Line {self.line}, Column {
                            self.start - self.line_start + 1
                        }] Error at '{ch}': Unexpected character."
                    )
            elif ch == "=":
                if self.match("="):
                    self.add_token(TokenType.EQ)
                else:
                    raise SyntaxError(
                        f"[Line {self.line}, Column {
                            self.start - self.line_start + 1
                        }] Error at '{ch}': Unexpected character."
                    )
            elif ch == "!":
                if self.match("="):
                    self.add_token(TokenType.NE)
                else:
                    self.add_token(TokenType.NOT)
            elif ch == ">":
                if self.match("="):
                    self.add_token(TokenType.GE)
                else:
                    self.add_token(TokenType.GT)
            elif ch == "<":
                if self.match("="):
                    self.add_token(TokenType.LE)
                else:
                    self.add_token(TokenType.LT)
            elif ch == "&":
                if self.match("&"):
                    self.add_token(TokenType.AND)
                else:
                    raise SyntaxError(
                        f"[Line {self.line}, Column {
                            self.start - self.line_start + 1
                        }] Error at '{ch}': Unexpected character."
                    )
            elif ch == "|":
                if self.match("|"):
                    self.add_token(TokenType.OR)
                else:
                    raise SyntaxError(
                        f"[Line {self.line}, Column {
                            self.start - self.line_start + 1
                        }] Error at '{ch}': Unexpected character."
                    )
            elif ch == "'":
                self.handle_character(ch)
            elif ch == '"':
                self.handle_string(ch)
            elif ch.isdigit():
                self.handle_number()
            elif ch.isalpha() or ch == "_":
                self.handle_identifier()
            else:
                raise SyntaxError(
                    f"[Line {self.line}, Column {
                        self.start - self.line_start + 1
                    }] Error at '{ch}': Unexpected character."
                )

        self.start = self.curr
        self.add_token(TokenType.EOF)

        return self.tokens
