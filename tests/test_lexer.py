import pytest

from fucklang.lexer import Lexer
from fucklang.token import KEYWORDS, Token, TokenType


@pytest.mark.parametrize("keyword_str, expected_type", KEYWORDS.items())
def test_lexer_all_keywords(
    keyword_str: str, expected_type: TokenType
) -> None:
    tokens = Lexer(keyword_str).tokenize()

    assert len(tokens) == 2
    assert tokens[0].type == expected_type
    assert tokens[0].lexeme == keyword_str


def test_lexer_char_string() -> None:
    input = "'a' \"abcdefg\""
    expected = [
        (TokenType.CHR, "'a'"),
        (TokenType.STR, '"abcdefg"'),
        (TokenType.EOF, ""),
    ]

    tokens = Lexer(input).tokenize()
    types = [(t.type, t.lexeme) for t in tokens]

    assert types == expected


def test_lexer_integer_float() -> None:
    input = "7 3.141596"
    expected = [
        (TokenType.INT, "7"),
        (TokenType.FLT, "3.141596"),
        (TokenType.EOF, ""),
    ]

    tokens = Lexer(input).tokenize()
    types = [(t.type, t.lexeme) for t in tokens]

    assert types == expected


def test_lexer_math_operators() -> None:
    input = "* / + - %"
    expected = [
        (TokenType.ASTERISK, "*"),
        (TokenType.SLASH, "/"),
        (TokenType.PLUS, "+"),
        (TokenType.MINUS, "-"),
        (TokenType.MOD, "%"),
        (TokenType.EOF, ""),
    ]

    tokens = Lexer(input).tokenize()
    types = [(t.type, t.lexeme) for t in tokens]

    assert types == expected


def test_lexer_logical_operators() -> None:
    input = "&& || !"  # and or not
    expected = [
        (TokenType.AND, "&&"),
        (TokenType.OR, "||"),
        (TokenType.NOT, "!"),
        (TokenType.EOF, ""),
    ]

    tokens = Lexer(input).tokenize()
    types = [(t.type, t.lexeme) for t in tokens]

    assert types == expected


def test_lexer_relational_operators() -> None:
    input = "> >= < <= == != :="
    expected = [
        (TokenType.GT, ">"),
        (TokenType.GE, ">="),
        (TokenType.LT, "<"),
        (TokenType.LE, "<="),
        (TokenType.EQ, "=="),
        (TokenType.NE, "!="),
        (TokenType.ASSIGN, ":="),
        (TokenType.EOF, ""),
    ]

    tokens = Lexer(input).tokenize()
    types = [(t.type, t.lexeme) for t in tokens]

    assert types == expected


def test_lexer_delimiters() -> None:
    input = "() {} ;"
    expected = [
        (TokenType.LPAREN, "("),
        (TokenType.RPAREN, ")"),
        (TokenType.LBRACE, "{"),
        (TokenType.RBRACE, "}"),
        (TokenType.SEMICOLON, ";"),
        (TokenType.EOF, ""),
    ]

    tokens = Lexer(input).tokenize()
    types = [(t.type, t.lexeme) for t in tokens]

    assert types == expected


def test_lexer_line_column_track() -> None:
    input = """var x int := 1;
puts(x);
"""
    expected = [
        Token(TokenType.VAR, "var", 1, 1),
        Token(TokenType.IDENTIFIER, "x", 1, 5),
        Token(TokenType.INT_TYPE, "int", 1, 7),
        Token(TokenType.ASSIGN, ":=", 1, 11),
        Token(TokenType.INT, "1", 1, 14),
        Token(TokenType.SEMICOLON, ";", 1, 15),
        Token(TokenType.PUTS, "puts", 2, 1),
        Token(TokenType.LPAREN, "(", 2, 5),
        Token(TokenType.IDENTIFIER, "x", 2, 6),
        Token(TokenType.RPAREN, ")", 2, 7),
        Token(TokenType.SEMICOLON, ";", 2, 8),
        Token(TokenType.EOF, "", 3, 1),
    ]

    tokens = Lexer(input).tokenize()
    for id, token in enumerate(tokens):
        assert token == expected[id]


def test_lexer_line_column_track_err() -> None:
    input = """var x int = 1;
puts(x);
"""
    expected = r"\[Line 1, Column 11\] Error at '=': Unexpected character."

    with pytest.raises(SyntaxError, match=expected):
        _ = Lexer(input).tokenize()


def test_lexer_const_declaration() -> None:
    input = "const pi flt := 3.14"
    expected = [
        (TokenType.CONST, "const"),
        (TokenType.IDENTIFIER, "pi"),
        (TokenType.FLT_TYPE, "flt"),
        (TokenType.ASSIGN, ":="),
        (TokenType.FLT, "3.14"),
        (TokenType.EOF, ""),
    ]

    tokens = Lexer(input).tokenize()
    types = [(t.type, t.lexeme) for t in tokens]

    assert types == expected


def test_lexer_var_declaration_chr() -> None:
    input = "var c chr := 'a';"

    expected = [
        (TokenType.VAR, "var"),
        (TokenType.IDENTIFIER, "c"),
        (TokenType.CHR_TYPE, "chr"),
        (TokenType.ASSIGN, ":="),
        (TokenType.CHR, "'a'"),
        (TokenType.SEMICOLON, ";"),
        (TokenType.EOF, ""),
    ]

    tokens = Lexer(input).tokenize()
    types = [(t.type, t.lexeme) for t in tokens]
    for id, t in enumerate(types):
        assert t == expected[id]


def test_lexer_var_declaration_chr_invalid() -> None:
    input = "var simple_chr chr := 'abc';"
    expected = "Unterminated character."

    with pytest.raises(SyntaxError, match=expected):
        _ = Lexer(input).tokenize()


def test_lexer_var_declaration_chr_without_begin_single_quote() -> None:
    input = "var simple_chr chr := a';"
    expected = "Unterminated character."

    with pytest.raises(SyntaxError, match=expected):
        _ = Lexer(input).tokenize()


def test_lexer_var_declaration_chr_without_end_single_quote() -> None:
    input = "var simple_chr chr := 'a;"
    expected = "Unterminated character."

    with pytest.raises(SyntaxError, match=expected):
        _ = Lexer(input).tokenize()


def test_lexer_var_declaration_str() -> None:
    input = 'var my_f_string str := "fuuuuuuuuuck";'
    expected = [
        (TokenType.VAR, "var"),
        (TokenType.IDENTIFIER, "my_f_string"),
        (TokenType.STR_TYPE, "str"),
        (TokenType.ASSIGN, ":="),
        (TokenType.STR, '"fuuuuuuuuuck"'),
        (TokenType.SEMICOLON, ";"),
        (TokenType.EOF, ""),
    ]

    tokens = Lexer(input).tokenize()
    types = [(t.type, t.lexeme) for t in tokens]
    for id, t in enumerate(types):
        assert t == expected[id]


def test_lexer_var_declaration_str_without_begin_double_quote() -> None:
    input = 'var my_f_string str := fuuuuuuuuuck";'
    expected = "Unterminated string."

    with pytest.raises(SyntaxError, match=expected):
        _ = Lexer(input).tokenize()


def test_lexer_var_declaration_str_without_end_double_quote() -> None:
    input = 'var my_f_string str := "fuuuuuuuuuck;'
    expected = "Unterminated string."

    with pytest.raises(SyntaxError, match=expected):
        _ = Lexer(input).tokenize()


def test_lexer_var_declaration_int() -> None:
    input = "var num int := 10;"

    expected = [
        (TokenType.VAR, "var"),
        (TokenType.IDENTIFIER, "num"),
        (TokenType.INT_TYPE, "int"),
        (TokenType.ASSIGN, ":="),
        (TokenType.INT, "10"),
        (TokenType.SEMICOLON, ";"),
        (TokenType.EOF, ""),
    ]

    tokens = Lexer(input).tokenize()
    types = [(t.type, t.lexeme) for t in tokens]
    for id, t in enumerate(types):
        assert t == expected[id]


def test_lexer_var_declaration_int_invalid() -> None:
    input = "var num int := 1_0;"
    # input = "var num int := 1a;"
    expected = "Invalid number format."

    with pytest.raises(SyntaxError, match=expected):
        _ = Lexer(input).tokenize()


def test_lexer_var_declaration_flt() -> None:
    input = "var num flt := 1.0;"

    expected = [
        (TokenType.VAR, "var"),
        (TokenType.IDENTIFIER, "num"),
        (TokenType.FLT_TYPE, "flt"),
        (TokenType.ASSIGN, ":="),
        (TokenType.FLT, "1.0"),
        (TokenType.SEMICOLON, ";"),
        (TokenType.EOF, ""),
    ]

    tokens = Lexer(input).tokenize()
    types = [(t.type, t.lexeme) for t in tokens]
    for id, t in enumerate(types):
        assert t == expected[id]


def test_lexer_var_declaration_flt_invalid() -> None:
    input = "var num flt := .0;"
    # input = "var num flt := 1.;"
    expected = "Unexpected character."

    with pytest.raises(SyntaxError, match=expected):
        _ = Lexer(input).tokenize()


def test_lexer_fucklang_code_simple() -> None:
    input = """
    # sum x and y
    var x int := 10;
    var y int := 20;
    var sum int := x + y;
    """

    expected = [
        (TokenType.VAR, "var"),
        (TokenType.IDENTIFIER, "x"),
        (TokenType.INT_TYPE, "int"),
        (TokenType.ASSIGN, ":="),
        (TokenType.INT, "10"),
        (TokenType.SEMICOLON, ";"),
        (TokenType.VAR, "var"),
        (TokenType.IDENTIFIER, "y"),
        (TokenType.INT_TYPE, "int"),
        (TokenType.ASSIGN, ":="),
        (TokenType.INT, "20"),
        (TokenType.SEMICOLON, ";"),
        (TokenType.VAR, "var"),
        (TokenType.IDENTIFIER, "sum"),
        (TokenType.INT_TYPE, "int"),
        (TokenType.ASSIGN, ":="),
        (TokenType.IDENTIFIER, "x"),
        (TokenType.PLUS, "+"),
        (TokenType.IDENTIFIER, "y"),
        (TokenType.SEMICOLON, ";"),
        (TokenType.EOF, ""),
    ]

    tokens = Lexer(input).tokenize()
    types = [(t.type, t.lexeme) for t in tokens]
    for id, t in enumerate(types):
        assert t == expected[id]


def test_lexer_fucklang_code_with_if_else() -> None:
    input = """
    var x int := 10;
    var y int := 20;

    fuck main() int {
        if (x >= y) {
            puts(x);
        } else {
            puts(y);
        }

        ret 0;
    }
    """
    expected = [
        (TokenType.VAR, "var"),
        (TokenType.IDENTIFIER, "x"),
        (TokenType.INT_TYPE, "int"),
        (TokenType.ASSIGN, ":="),
        (TokenType.INT, "10"),
        (TokenType.SEMICOLON, ";"),
        (TokenType.VAR, "var"),
        (TokenType.IDENTIFIER, "y"),
        (TokenType.INT_TYPE, "int"),
        (TokenType.ASSIGN, ":="),
        (TokenType.INT, "20"),
        (TokenType.SEMICOLON, ";"),
        (TokenType.FUCK, "fuck"),
        (TokenType.IDENTIFIER, "main"),
        (TokenType.LPAREN, "("),
        (TokenType.RPAREN, ")"),
        (TokenType.INT_TYPE, "int"),
        (TokenType.LBRACE, "{"),
        (TokenType.IF, "if"),
        (TokenType.LPAREN, "("),
        (TokenType.IDENTIFIER, "x"),
        (TokenType.GE, ">="),
        (TokenType.IDENTIFIER, "y"),
        (TokenType.RPAREN, ")"),
        (TokenType.LBRACE, "{"),
        (TokenType.PUTS, "puts"),
        (TokenType.LPAREN, "("),
        (TokenType.IDENTIFIER, "x"),
        (TokenType.RPAREN, ")"),
        (TokenType.SEMICOLON, ";"),
        (TokenType.RBRACE, "}"),
        (TokenType.ELSE, "else"),
        (TokenType.LBRACE, "{"),
        (TokenType.PUTS, "puts"),
        (TokenType.LPAREN, "("),
        (TokenType.IDENTIFIER, "y"),
        (TokenType.RPAREN, ")"),
        (TokenType.SEMICOLON, ";"),
        (TokenType.RBRACE, "}"),
        (TokenType.RET, "ret"),
        (TokenType.INT, "0"),
        (TokenType.SEMICOLON, ";"),
        (TokenType.RBRACE, "}"),
        (TokenType.EOF, ""),
    ]

    tokens = Lexer(input).tokenize()
    types = [(t.type, t.lexeme) for t in tokens]
    for id, t in enumerate(types):
        assert t == expected[id]


def test_lexer_fucklang_code_with_function() -> None:
    input = """
    # multiply x and y
    fuck mul(a int, b int) int {
        ret a * b;
    }

    fuck main() int {
        var r int := mul(10, 2);
        puts(r);

        ret 0;
    }
    """
    expected = [
        (TokenType.FUCK, "fuck"),
        (TokenType.IDENTIFIER, "mul"),
        (TokenType.LPAREN, "("),
        (TokenType.IDENTIFIER, "a"),
        (TokenType.INT_TYPE, "int"),
        (TokenType.COMMA, ","),
        (TokenType.IDENTIFIER, "b"),
        (TokenType.INT_TYPE, "int"),
        (TokenType.RPAREN, ")"),
        (TokenType.INT_TYPE, "int"),
        (TokenType.LBRACE, "{"),
        (TokenType.RET, "ret"),
        (TokenType.IDENTIFIER, "a"),
        (TokenType.ASTERISK, "*"),
        (TokenType.IDENTIFIER, "b"),
        (TokenType.SEMICOLON, ";"),
        (TokenType.RBRACE, "}"),
        (TokenType.FUCK, "fuck"),
        (TokenType.IDENTIFIER, "main"),
        (TokenType.LPAREN, "("),
        (TokenType.RPAREN, ")"),
        (TokenType.INT_TYPE, "int"),
        (TokenType.LBRACE, "{"),
        (TokenType.VAR, "var"),
        (TokenType.IDENTIFIER, "r"),
        (TokenType.INT_TYPE, "int"),
        (TokenType.ASSIGN, ":="),
        (TokenType.IDENTIFIER, "mul"),
        (TokenType.LPAREN, "("),
        (TokenType.INT, "10"),
        (TokenType.COMMA, ","),
        (TokenType.INT, "2"),
        (TokenType.RPAREN, ")"),
        (TokenType.SEMICOLON, ";"),
        (TokenType.PUTS, "puts"),
        (TokenType.LPAREN, "("),
        (TokenType.IDENTIFIER, "r"),
        (TokenType.RPAREN, ")"),
        (TokenType.SEMICOLON, ";"),
        (TokenType.RET, "ret"),
        (TokenType.INT, "0"),
        (TokenType.SEMICOLON, ";"),
        (TokenType.RBRACE, "}"),
        (TokenType.EOF, ""),
    ]

    tokens = Lexer(input).tokenize()
    types = [(t.type, t.lexeme) for t in tokens]
    for id, t in enumerate(types):
        assert t == expected[id]
