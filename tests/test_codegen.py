from fucklang.codegen import CodeGenerator
from fucklang.lexer import Lexer
from fucklang.node import Boolean, Integer
from fucklang.parser import Parser
from fucklang.symbol import SemanticAnalyzer


def test_codegen_integer():
    codegen = CodeGenerator()

    codegen.visit(Integer(value=10, line=1))

    assert codegen.sam_code == ["PUSHIMM 10 // integer"]


def test_codegen_boolean_true():
    codegen = CodeGenerator()

    codegen.visit(Boolean(value=True, line=1))

    assert codegen.sam_code == ["PUSHIMM 1 // boolean 1-true 0-false"]


def test_codegen_primary_integer() -> None:
    tokens = Lexer("var x int := 10;").tokenize()
    ast = Parser(tokens).parse()
    symbol = SemanticAnalyzer().analyze(ast)
    code = CodeGenerator(symbol).build(ast)

    expected = [
        "ADDSP 1",
        "PUSHIMM 10 // integer",
        "STOREOFF 0",
        "ADDSP -1",
        "PUSHIMM 0",
        "STOP",
    ]

    assert code == expected
    assert len(code) == len(expected)
