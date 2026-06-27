import pytest

from fucklang.lexer import Lexer
from fucklang.parser import Parser
from fucklang.symbol import SemanticAnalyzer, SymbolTable
from fucklang.token import TokenType


def test_symbol_declare():
    table = SymbolTable()

    symbol = table.declare("x", TokenType.INT_TYPE)

    assert symbol.idx == "x"
    assert symbol.type == TokenType.INT_TYPE
    assert symbol.offset == 0


def test_symbol_resolve():
    table = SymbolTable()

    table.declare("x", TokenType.INT_TYPE)

    symbol = table.resolve("x")

    assert symbol.idx == "x"


def test_symbol_redeclare():
    table = SymbolTable()

    table.declare("x", TokenType.INT_TYPE)

    with pytest.raises(SyntaxError):
        table.declare("x", TokenType.INT_TYPE)


def test_symbol_resolve_undeclared():
    table = SymbolTable()

    with pytest.raises(SyntaxError):
        table.resolve("x")


def test_symbol_const():
    table = SymbolTable()

    symbol = table.declare("pi", TokenType.FLT_TYPE, mutable=False)

    assert symbol.mutable is False


def test_symbol_const_decl() -> None:
    tokens = Lexer("const PI flt := 3.141596;").tokenize()
    ast = Parser(tokens).parse()
    symbol = SemanticAnalyzer().analyze(ast)

    expected = SymbolTable()
    expected.declare("PI", TokenType.FLT_TYPE, False)
    expected.curr = 1

    assert symbol == expected


def test_symbol_var_decl_integer() -> None:
    tokens = Lexer("var x int := 10;").tokenize()
    ast = Parser(tokens).parse()
    symbol = SemanticAnalyzer().analyze(ast)

    expected = SymbolTable()
    expected.declare("x", TokenType.INT_TYPE, True)
    expected.curr = 1

    assert symbol == expected


def test_symbol_const_decl_and_assign_err() -> None:
    tokens = Lexer("const PI flt := 3.14; PI := 3.0;").tokenize()
    ast = Parser(tokens).parse()

    with pytest.raises(SyntaxError):
        _ = SemanticAnalyzer().analyze(ast)


def test_symbol_var_decl_integer_assing_float_err() -> None:
    tokens = Lexer("var x int := 10.0;").tokenize()
    ast = Parser(tokens).parse()

    with pytest.raises(SyntaxError):
        _ = SemanticAnalyzer().analyze(ast)


def test_symbol_var_decl_float_assing_boolean_err() -> None:
    tokens = Lexer("var x flt := true;").tokenize()
    ast = Parser(tokens).parse()

    with pytest.raises(SyntaxError):
        _ = SemanticAnalyzer().analyze(ast)


def test_symbol_assing_binary_op_sum_booleans_err() -> None:
    tokens = Lexer("var x boo := true; x := true + false;").tokenize()
    ast = Parser(tokens).parse()

    with pytest.raises(SyntaxError):
        _ = SemanticAnalyzer().analyze(ast)


def test_symbol_assing_binary_op_booleans() -> None:
    tokens = Lexer("var x boo := true; x := !true;").tokenize()
    ast = Parser(tokens).parse()
    symbol = SemanticAnalyzer().analyze(ast)
    print(symbol)

    expected = SymbolTable()
    expected.declare("x", TokenType.BOO_TYPE, True)
    expected.curr = 1

    assert symbol == expected
