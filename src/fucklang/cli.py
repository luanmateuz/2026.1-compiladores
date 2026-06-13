import argparse

from fucklang.lexer import Lexer


def flag_lexer(code: str) -> None:
    try:
        tokens = Lexer(code).tokenize()

        for t in tokens:
            print(t)
    except SyntaxError as err:
        print(err)


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="fucklang", description="fucklang cli"
    )
    parser.add_argument("filename", help="<filename.fk>")
    parser.add_argument("-l", "--lexer", action="store_true")

    args = parser.parse_args()

    if args.filename is None:
        raise SystemExit("Usage: fucklang <filename.fk>")

    if not args.filename.endswith("fk"):
        raise SystemExit(f"{args.filename} is not FUCK file!")

    with open(args.filename) as file:
        code = file.read()

        if args.lexer:
            flag_lexer(code)
            return


if __name__ == "__main__":
    main()
