import argparse

from fucklang.codegen import CodeGenerator
from fucklang.lexer import Lexer
from fucklang.parser import Parser
from fucklang.symbol import SemanticAnalyzer


def flag_lexer(code: str) -> None:
    try:
        tokens = Lexer(code).tokenize()

        for t in tokens:
            print(t)
    except SyntaxError as err:
        print(err)


def flag_parser(code: str) -> None:
    try:
        tokens = Lexer(code).tokenize()
        ast = Parser(tokens).parse()
        print(ast)
    except SyntaxError as err:
        print(err)


def flag_symbol_table(code: str) -> None:
    try:
        tokens = Lexer(code).tokenize()
        ast = Parser(tokens).parse()
        symbol = SemanticAnalyzer().analyze(ast)
        for idx in symbol.symbols:
            print(f"{idx}: {symbol.symbols[idx]}")
    except SyntaxError as err:
        print(err)


def flag_dry_run(code: str) -> None:
    try:
        tokens = Lexer(code).tokenize()
        ast = Parser(tokens).parse()
        symbol = SemanticAnalyzer().analyze(ast)
        code = CodeGenerator(symbol).build(ast)
        print("\n".join(code))
    except SyntaxError as err:
        print(err)


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="fucklang", description="fucklang cli"
    )
    parser.add_argument("filename", help="<filename.fk>")
    parser.add_argument("-l", "--lexer", action="store_true")
    parser.add_argument("-p", "--parser", action="store_true")
    parser.add_argument("-s", "--symbol", action="store_true")
    parser.add_argument("--dry-run", action="store_true")

    args = parser.parse_args()

    if args.filename is None:
        raise SystemExit("Usage: fucklang <filename.fk>")

    if not args.filename.endswith("fk"):
        raise SystemExit(f"{args.filename} is not FUCK file!")

    with open(args.filename) as file:
        code = file.read()

        if args.lexer:
            flag_lexer(code)

        if args.parser:
            flag_parser(code)

        if args.symbol:
            flag_symbol_table(code)

        if args.dry_run:
            flag_dry_run(code)


if __name__ == "__main__":
    main()
