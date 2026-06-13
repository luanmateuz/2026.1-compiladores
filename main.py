import sys

from fucklang.lexer import Lexer

if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit("Usage: python3 main.py <filename>")

    if not sys.argv[1].endswith("fk"):
        raise SystemExit(f"{sys.argv[1]} is not FUCK file!")

    with open(sys.argv[1]) as file:
        code = file.read()

        try:
            tokens = Lexer(code).tokenize()
            print(tokens)
        except SyntaxError as err:
            print(err)
