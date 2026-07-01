import argparse
from importlib import metadata
from pathlib import Path

from fucklang.codegen import CodeGenerator
from fucklang.lexer import Lexer
from fucklang.parser import Parser
from fucklang.symbol import SemanticAnalyzer

PKG_VERSION = metadata.version("fucklang")


def write_output(
    sam: list[str], filename: str, output: str | None = None
) -> None:
    if output is None:
        output = str(Path(filename).with_suffix(".sam"))

    with open(output, "w", encoding="utf-8") as file:
        file.write("\n".join(sam))

    print(f"It's done '{output}'")


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="fucklang",
        description="fucklang compiler",
        add_help=False,
    )

    parser.add_argument(
        "filename",
        metavar="FILE",
        help="Source file (.fk)",
    )
    parser.add_argument(
        "-h",
        "--help",
        action="help",
        help="Show this help message and exit",
    )

    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"%(prog)s {PKG_VERSION}",
        help="Print fucklang version",
    )

    parser.add_argument(
        "-l",
        "--lexer",
        action="store_true",
        help="Print lexer tokens",
    )

    parser.add_argument(
        "-p",
        "--parser",
        action="store_true",
        help="Print parser AST",
    )

    parser.add_argument(
        "-s",
        "--symbol",
        action="store_true",
        help="Print symbol table",
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print generated SaM without writing a file",
    )

    parser.add_argument(
        "-o",
        "--output",
        help="Output SaM file",
    )

    args = parser.parse_args()

    if not args.filename.endswith(".fk"):
        raise SystemExit(f"error: '{args.filename}' is not a .fk file")

    try:
        with open(args.filename, encoding="utf-8") as file:
            source = file.read()

        tokens = Lexer(source).tokenize()

        if args.lexer:
            for token in tokens:
                print(token)

        ast = Parser(tokens).parse()

        if args.parser:
            print(ast)

        symbol_table = SemanticAnalyzer().analyze(ast)

        if args.symbol:
            for name, symbol in symbol_table.symbols.items():
                print(f"{name}: {symbol}")

        sam = CodeGenerator(symbol_table).build(ast)

        if args.dry_run:
            print("\n".join(sam))
        else:
            write_output(
                sam,
                filename=args.filename,
                output=args.output,
            )

    except FileNotFoundError:
        raise SystemExit(f"error: file '{args.filename}' not found")

    except PermissionError:
        raise SystemExit(f"error: permission denied: '{args.filename}'")

    except SyntaxError as err:
        raise SystemExit(err)


if __name__ == "__main__":
    main()
