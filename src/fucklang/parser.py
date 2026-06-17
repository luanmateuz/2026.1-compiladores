from fucklang.node import (
    AssignStmt,
    BinaryOp,
    Character,
    ConstStmt,
    Float,
    ForStmt,
    Identifier,
    IfStmt,
    Integer,
    LogicalAnd,
    LogicalOr,
    ParenGroup,
    PutsStmt,
    Stmt,
    String,
    UnaryOp,
    VarStmt,
)
from fucklang.token import Token, TokenType


class Parser:
    def __init__(self, tokens) -> None:
        self.tokens: list[Token] = tokens
        self.curr: int = 0  # current

    def peek(self) -> Token:
        return self.tokens[self.curr]

    def match(self, expected_token) -> bool:
        if self.curr >= len(self.tokens):
            return False
        if self.peek().type != expected_token:
            return False

        self.curr += 1
        return True

    def previous_token(self) -> Token:
        return self.tokens[self.curr - 1]

    def advance(self):
        token = self.tokens[self.curr]
        self.curr += 1

        return token

    def expected(self, expected_type):
        if self.curr >= len(self.tokens):
            raise SyntaxError(
                f"[Line {self.previous_token().line}] Error: "
                f"Found {self.previous_token().lexeme!r}, "
                f"expected {expected_type}"
            )
        elif self.peek().type != expected_type:
            raise SyntaxError(
                f"[Line {self.previous_token().line} "
                f"Column {self.previous_token().column}]"
                f" Error: Expected {expected_type}, "
                f"found {self.peek().lexeme!r}"
            )
        else:
            token = self.advance()
            return token

    def is_next(self, expected_type) -> bool:
        if self.curr >= len(self.tokens):
            return False
        return self.peek().type == expected_type

    def primary(self):
        """
        <primary> ::= <int> | <flt> | <chr> | <str>
                                            | <identifier>
                                            | '(' expr ')'
        """
        if self.match(TokenType.INT):
            return Integer(
                int(self.previous_token().lexeme), self.previous_token().line
            )
        elif self.match(TokenType.FLT):
            return Float(
                float(self.previous_token().lexeme), self.previous_token().line
            )
        elif self.match(TokenType.CHR):
            return Character(
                str(self.previous_token().lexeme), self.previous_token().line
            )
        elif self.match(TokenType.STR):
            return String(
                str(self.previous_token().lexeme), self.previous_token().line
            )
        elif self.match(TokenType.LPAREN):
            expr = self.expr()
            if not self.match(TokenType.RPAREN):
                raise SyntaxError(
                    f"Error [Line: {self.previous_token().line}]: "
                    f"')' expected."
                )

            return ParenGroup(expr, self.previous_token().line)
        else:
            identifier = self.expected(TokenType.IDENTIFIER)
            return Identifier(identifier.lexeme, self.previous_token().line)

    def unary(self):
        """
        <unary> ::= ( '!' | '+' | '-' ) <unary> | <primary>
        """
        if (
            self.match(TokenType.NOT)
            or self.match(TokenType.PLUS)
            or self.match(TokenType.MINUS)
        ):
            op = self.previous_token()
            operand = self.unary()
            return UnaryOp(op, operand, op.line)

        return self.primary()

    def modulo(self):
        """
        <modulo> ::= <unary> ( '%' <unary> )*
        """
        expr = self.unary()
        while self.match(TokenType.MOD):
            op = self.previous_token()
            right = self.unary()
            expr = BinaryOp(op, expr, right, op.line)

        return expr

    def multiplication(self):
        """
        <multiplication> ::= <modulo> ( ( '*' | '/' ) <modulo> )*
        """
        expr = self.modulo()
        while self.match(TokenType.ASTERISK) or self.match(TokenType.SLASH):
            op = self.previous_token()
            right = self.modulo()
            expr = BinaryOp(op, expr, right, op.line)

        return expr

    def addition(self):
        """
        <addition> ::= <multiplication> ( ( '+' | '-' ) <multiplication> )*
        """
        expr = self.multiplication()
        while self.match(TokenType.PLUS) or self.match(TokenType.MINUS):
            op = self.previous_token()
            right = self.multiplication()
            expr = BinaryOp(op, expr, right, op.line)

        return expr

    def comparison(self):
        """
        <comparison> ::= <addition> ( ('>' | '>=' | '<' | '<=' ) <addition>)*
        """
        expr = self.addition()
        while (
            self.match(TokenType.GT)
            or self.match(TokenType.GE)
            or self.match(TokenType.LT)
            or self.match(TokenType.LE)
        ):
            op = self.previous_token()
            right = self.addition()
            expr = BinaryOp(op, expr, right, op.line)

        return expr

    def equality(self):
        """
        <equality> ::= <comparison> ( ( '!=' | '==' ) <comparison> )*
        """
        expr = self.comparison()
        while self.match(TokenType.EQ) or self.match(TokenType.NE):
            op = self.previous_token()
            right = self.comparison()
            expr = BinaryOp(op, expr, right, op.line)

        return expr

    def logical_and(self):
        """
        <logical_and> ::= <equality> ( '&&' <equality> )*
        """
        expr = self.equality()
        while self.match(TokenType.AND):
            op = self.previous_token()
            right = self.equality()
            expr = LogicalAnd(op, expr, right, op.line)

        return expr

    def logical_or(self):
        """
        <logical_or> ::= <logical_and> ( '||' <logical_and> )*
        """
        expr = self.logical_and()
        while self.match(TokenType.OR):
            op = self.previous_token()
            right = self.logical_and()
            expr = LogicalOr(op, expr, right, op.line)

        return expr

    def expr(self):
        """
        Order:
            1. logical or
            2. logical and
            3. equality
            4. comparison
            5. addition, subtraction
            6. multiplication, division
            7. modulo
            8. unary, logical negation
            9. primary
        """
        return self.logical_or()

    def parse_type(self) -> Token:
        """
        <type> ::= int_type | flt_type | chr_type | str_type
        """
        if (
            self.match(TokenType.INT_TYPE)
            or self.match(TokenType.FLT_TYPE)
            or self.match(TokenType.CHR_TYPE)
            or self.match(TokenType.STR_TYPE)
        ):
            return self.previous_token()
        raise SyntaxError(f"Line {self.peek().line}: Expected a valid type.")

    def puts_stmt(self):
        """
        <puts_stmt> ::= "puts" "(" <expr> ")" ";"
        """
        if self.match(TokenType.PUTS):
            self.expected(TokenType.LPAREN)
            expr = self.expr()
            self.expected(TokenType.RPAREN)
            if not self.match(TokenType.SEMICOLON):
                raise SyntaxError(
                    f"Line {self.peek().line}: "
                    f"Expected ';' after variable declaration."
                )

            return PutsStmt(expr, self.previous_token().line)
        raise SyntaxError(f"Ops {self.peek().line}: Expected 'puts'.")

    def for_stmt(self):
        """
        <for_stmt> ::=
                        "for" "("
                            (<var_stmt> | ";")
                            <expr> ";"
                            <assign_expr>?
                        ")"
                        "{"
                            <stmts>
                        "}"
        """
        self.expected(TokenType.FOR)
        self.expected(TokenType.LPAREN)
        if self.is_next(TokenType.VAR):
            # ex:
            # var i int := 0;
            var = self.var_stmt()
            print(var)
        else:
            var = None
            self.expected(TokenType.SEMICOLON)
        # ex:
        # i < 10
        condition = self.expr()
        self.expected(TokenType.SEMICOLON)
        if self.is_next(TokenType.IDENTIFIER):
            # i := i + 1
            for_step = self.assign_expr()
        else:
            for_step = None
        self.expected(TokenType.RPAREN)
        self.expected(TokenType.LBRACE)
        for_stmts = self.stmts()

        return ForStmt(
            var, condition, for_step, for_stmts, self.previous_token().line
        )

    def if_stmt(self):
        """
        <if_stmt> ::=
                        "if" "(" <expr> ")" "{"
                            <stmts>
                        "}"
                        (
                        "else" <if_stmt> | "else" "{"
                            <stmts>
                        "}"
                        )?
        """
        self.expected(TokenType.IF)
        self.expected(TokenType.LPAREN)
        boolean_expr = self.expr()
        self.expected(TokenType.RPAREN)
        self.expected(TokenType.LBRACE)
        if_stmts = self.stmts()
        if self.is_next(TokenType.ELSE):
            self.expected(TokenType.ELSE)
            if self.is_next(TokenType.IF):
                else_stmts = self.if_stmt()
            else:
                self.expected(TokenType.LBRACE)
                else_stmts = self.stmts()
        else:
            else_stmts = None

        return IfStmt(
            boolean_expr, if_stmts, else_stmts, self.previous_token().line
        )

    def const_stmt(self):
        """
        <const_stmt> ::= "const" IDENTIFIER <type> ":=" <expr> ";"
        """
        self.expected(TokenType.CONST)
        line = self.previous_token().line
        if not self.match(TokenType.IDENTIFIER):
            raise SyntaxError("Error: expected const name.")
        name = self.previous_token()
        const_type = self.parse_type()

        if not self.match(TokenType.ASSIGN):
            raise SyntaxError(
                f"Line {self.peek().line}: "
                f"Constants must be initialized with ':='."
            )
        expr = self.expr()

        if not self.match(TokenType.SEMICOLON):
            raise SyntaxError(
                f"Line {self.peek().line}: "
                f"Expected ';' after constant declaration."
            )

        return ConstStmt(name, const_type, expr, line)

    def var_stmt(self):
        """
        <var_stmt> ::= "var" IDENTIFIER <type> ":=" <expr> ";"
        """
        self.expected(TokenType.VAR)
        line = self.previous_token().line
        if not self.match(TokenType.IDENTIFIER):
            raise SyntaxError("Error: expected var name.")

        name = self.previous_token()
        # var_type = self.parse_type()
        var_type = self.parse_type().type

        if not self.match(TokenType.ASSIGN):
            raise SyntaxError(
                f"Line {self.peek().line}: "
                f"Variables must be initialized with ':='."
            )
        expr = self.expr()

        if not self.match(TokenType.SEMICOLON):
            raise SyntaxError(
                f"Line {self.peek().line}: "
                f"Expected ';' after variable declaration."
            )

        return VarStmt(name, var_type, expr, line)

    def assign_expr(self):
        """
        <assign_expr> ::= IDENTIFIER ":=" <expr>
        """
        line = self.previous_token().line
        if not self.match(TokenType.IDENTIFIER):
            raise SyntaxError("Error: expected var name.")

        name = self.previous_token()
        if not self.match(TokenType.ASSIGN):
            raise SyntaxError(
                f"Line {self.peek().line}: "
                f"Variables must be initialized with ':='."
            )
        expr = self.expr()

        return AssignStmt(name, expr, line)

    def assign_stmt(self):
        """
        <assign_stmt> ::= IDENTIFIER ":=" <expr> ";"
        """
        stmt = self.assign_expr()
        self.expected(TokenType.SEMICOLON)
        return stmt

    def stmt(
        self,
    ) -> IfStmt | ForStmt | PutsStmt | VarStmt | ConstStmt | AssignStmt:
        if self.peek().type == TokenType.IF:
            return self.if_stmt()
        elif self.peek().type == TokenType.FOR:
            return self.for_stmt()
        elif self.peek().type == TokenType.PUTS:
            return self.puts_stmt()

        else:
            if self.peek().type == TokenType.VAR:
                return self.var_stmt()
            elif self.peek().type == TokenType.CONST:
                return self.const_stmt()
            elif self.peek().type == TokenType.IDENTIFIER:
                return self.assign_stmt()
            else:
                raise SyntaxError("Oh shit, :/")

    def stmts(self):
        statements: list[Stmt] = []
        while not self.match(TokenType.EOF) and not self.match(
            TokenType.RBRACE
        ):
            statements.append(self.stmt())

        return statements

    def program(self):
        return self.stmts()

    def parse(self):
        return self.program()
