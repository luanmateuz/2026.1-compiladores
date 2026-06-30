from fucklang.lexer import Lexer
from fucklang.node import (
    BinaryOp,
    Float,
    FuncCall,
    FuncDecl,
    FuncParam,
    Identifier,
    IfStmt,
    Integer,
    PutsStmt,
    RetStmt,
    String,
    VarStmt,
)
from fucklang.parser import Parser
from fucklang.token import Token, TokenType


def test_parser_primary_integer() -> None:
    tokens = Lexer("var x int := 10;").tokenize()
    ast = Parser(tokens).parse()[0]

    expected = VarStmt(
        Token(TokenType.IDENTIFIER, "x", line=1, column=5),
        TokenType.INT_TYPE,
        Integer(10, 1),
        1,
    )

    assert ast == expected


def test_parser_primary_float() -> None:
    tokens = Lexer("var x flt := 10.0;").tokenize()
    ast = Parser(tokens).parse()[0]

    expected = VarStmt(
        Token(TokenType.IDENTIFIER, "x", line=1, column=5),
        TokenType.FLT_TYPE,
        Float(10.0, 1),
        1,
    )

    assert ast == expected


def test_parser_vars_declarations() -> None:
    input = """var x int := 5;
var y int := 15;
var r int := x * y;"""

    tokens = Lexer(input).tokenize()
    ast = Parser(tokens).parse()

    expected = [
        VarStmt(
            Token(TokenType.IDENTIFIER, "x", line=1, column=5),
            TokenType.INT_TYPE,
            Integer(5, 1),
            line=1,
        ),
        VarStmt(
            Token(TokenType.IDENTIFIER, "y", line=2, column=5),
            TokenType.INT_TYPE,
            Integer(15, 2),
            line=2,
        ),
        VarStmt(
            Token(TokenType.IDENTIFIER, "r", line=3, column=5),
            TokenType.INT_TYPE,
            BinaryOp(
                Token(TokenType.ASTERISK, "*", line=3, column=16),
                Identifier("x", 3),
                Identifier("y", 3),
                line=3,
            ),
            line=3,
        ),
    ]

    assert ast == expected


def test_parser_var_declaration_if_stmts() -> None:
    input = """var z int := 11;
if (z > 5) {
    puts(z);
}"""
    expected = [
        VarStmt(
            Token(TokenType.IDENTIFIER, "z", line=1, column=5),
            TokenType.INT_TYPE,
            Integer(11, 1),
            line=1,
        ),
        IfStmt(
            BinaryOp(
                Token(TokenType.GT, lexeme=">", line=2, column=7),
                Identifier("z", 2),
                Integer(5, 2),
                line=2,
            ),
            if_stmts=[PutsStmt(Identifier("z", line=3), line=3)],
            else_stmts=None,
            line=4,
        ),
    ]

    tokens = Lexer(input).tokenize()
    ast = Parser(tokens).parse()

    assert ast == expected


def test_parser_fuck_declaration_without_params():
    input = """fuck this_shit() void {
    puts("x");            
}

this_shit();
"""
    tokens = Lexer(input).tokenize()
    ast = Parser(tokens).parse()

    expected = [
        FuncDecl(
            name="this_shit",
            params=[],
            func_type=TokenType.VOID_TYPE,
            body=[PutsStmt(expr=String('"x"', 2), line=2)],
            line=3,
        ),
        FuncCall(name="this_shit", arguments=[], line=5),
    ]

    assert ast == expected


def test_parser_fuck_declaration_with_params():
    input = """fuck sum(a int, b int) int {
    ret a + b;
}

var restult int := sum(1,2);
"""
    tokens = Lexer(input).tokenize()
    ast = Parser(tokens).parse()

    expected = [
        FuncDecl(
            name="sum",
            params=[
                FuncParam("a", TokenType.INT_TYPE),
                FuncParam("b", TokenType.INT_TYPE),
            ],
            func_type=TokenType.INT_TYPE,
            body=[
                RetStmt(
                    value=BinaryOp(
                        op=Token(TokenType.PLUS, "+", 2, 11),
                        left=Identifier("a", 2),
                        right=Identifier("b", 2),
                        line=2,
                    ),
                    line=2,
                )
            ],
            line=3,
        ),
        VarStmt(
            name=Token(TokenType.IDENTIFIER, "restult", 5, 5),
            type=TokenType.INT_TYPE,
            value=FuncCall(
                name="sum",
                arguments=[Integer(1, 5), Integer(2, 5)],
                line=5,
            ),
            line=5,
        ),
    ]

    assert ast == expected


def test_parser_fuck_declaration_with_params_ret_void():
    input = """fuck print_int(a int) void {
    puts(a);
}

print_int(9);
"""
    tokens = Lexer(input).tokenize()
    ast = Parser(tokens).parse()

    expected = [
        FuncDecl(
            name="print_int",
            params=[FuncParam("a", TokenType.INT_TYPE)],
            func_type=TokenType.VOID_TYPE,
            body=[PutsStmt(expr=Identifier("a", 2), line=2)],
            line=3,
        ),
        FuncCall(name="print_int", arguments=[Integer(9, 5)], line=5),
    ]

    assert ast == expected
