from dataclasses import dataclass

from fucklang.token import Token, TokenType


class Node:
    pass


class Expr(Node):
    pass


class Stmt(Node):
    pass


@dataclass
class Integer(Expr):
    value: int
    line: int

    def __post_init__(self) -> None:
        assert isinstance(self.value, int), self.value

    def __repr__(self) -> str:
        return f"Integer[{self.value}]"


@dataclass
class Float(Expr):
    value: float
    line: int

    def __post_init__(self) -> None:
        assert isinstance(self.value, float), self.value

    def __repr__(self) -> str:
        return f"Float[{self.value}]"


@dataclass
class Character(Expr):
    value: str
    line: int

    def __post_init__(self) -> None:
        assert isinstance(self.value, str), self.value

    def __repr__(self) -> str:
        return f"Character[{self.value}]"


@dataclass
class String(Expr):
    value: str
    line: int

    def __post_init__(self) -> None:
        assert isinstance(self.value, str), self.value

    def __repr__(self) -> str:
        return f"String[{self.value}]"


@dataclass
class Boolean(Expr):
    value: bool
    line: int

    def __post_init__(self) -> None:
        assert isinstance(self.value, bool), self.value

    def __repr__(self) -> str:
        return f"Boolean[{self.value}]"


@dataclass
class UnaryOp(Expr):
    op: Token
    operand: Expr
    line: int

    def __post_init__(self) -> None:
        assert isinstance(self.op, Token), self.op
        assert isinstance(self.operand, Expr), self.operand

    def __repr__(self) -> str:
        return f"UnaryOp({self.op.lexeme!r}, {self.operand})"


@dataclass
class BinaryOp(Expr):
    op: Token
    left: Expr
    right: Expr
    line: int

    def __post_init__(self) -> None:
        assert isinstance(self.op, Token), self.op
        assert isinstance(self.left, Expr), self.left
        assert isinstance(self.right, Expr), self.right

    def __repr__(self) -> str:
        return f"BinaryOp({self.op.lexeme!r}, {self.left}, {self.right})"


@dataclass
class ParenGroup(Expr):
    """
    ( <expr> )
    """

    value: Expr
    line: int

    def __post_init__(self) -> None:
        assert isinstance(self.value, Expr), self.value

    def __repr__(self) -> str:
        return f"ParenGroup({self.value})"


@dataclass
class LogicalOr(Expr):
    op: Token
    left: Expr
    right: Expr
    line: int

    def __post_init__(self) -> None:
        assert isinstance(self.op, Token), self.op
        assert isinstance(self.left, Expr), self.left
        assert isinstance(self.right, Expr), self.right

    def __repr__(self) -> str:
        return f"LogicalOr({self.op.lexeme!r}, {self.left}, {self.right})"


@dataclass
class LogicalAnd(Expr):
    op: Token
    left: Expr
    right: Expr
    line: int

    def __post_init__(self) -> None:
        assert isinstance(self.op, Token), self.op
        assert isinstance(self.left, Expr), self.left
        assert isinstance(self.right, Expr), self.right

    def __repr__(self) -> str:
        return f"LogicalAnd({self.op.lexeme!r}, {self.left}, {self.right})"


@dataclass
class Identifier(Expr):
    name: str
    line: int

    def __post_init__(self) -> None:
        assert isinstance(self.name, str)

    def __repr__(self) -> str:
        return f"Identifier[{self.name}]"


@dataclass
class ConstStmt(Stmt):
    name: Token
    # type: Token
    type: TokenType
    value: Expr
    line: int

    def __post_init__(self) -> None:
        assert isinstance(self.name, Token)
        # assert isinstance(self.type, Token)
        assert isinstance(self.value, Expr)

    def __repr__(self) -> str:
        return (
            f"ConstStmt({self.name.lexeme!r}, "
            # f"{self.type.lexeme!r}, {self.value})"
            f"{self.type}, {self.value})"
        )


@dataclass
class VarStmt(Stmt):
    name: Token
    # type: Token
    type: TokenType
    value: Expr
    line: int

    def __post_init__(self) -> None:
        assert isinstance(self.name, Token)
        # assert isinstance(self.type, Token)
        assert isinstance(self.value, Expr)

    def __repr__(self) -> str:
        return (
            f"VarStmt({self.name.lexeme!r}, "
            # f"{self.type.lexeme!r}, {self.value})"
            f"{self.type}, {self.value})"
        )


@dataclass
class AssignStmt(Stmt):
    """left := right"""

    # left: Expr
    left: Token
    right: Expr
    line: int

    def __post_init__(self) -> None:
        # assert isinstance(self.left, Expr)
        assert isinstance(self.left, Token)
        assert isinstance(self.right, Expr)

    def __repr__(self) -> str:
        return f"AssignStmt(left={self.left}, right={self.right})"


@dataclass
class PutsStmt(Stmt):
    expr: Expr
    line: int

    def __post_init__(self) -> None:
        assert isinstance(self.expr, Expr)

    def __repr__(self) -> str:
        return f"PutsStmt({self.expr!r})"


@dataclass
class Stmts(Node):
    stmts: list
    line: int

    def __repr__(self) -> str:
        return f"Stmts({self.stmts})"


@dataclass
class IfStmt(Stmt):
    boolean_expr: Expr
    if_stmts: Stmts | list[Stmt]
    else_stmts: Stmts | list[Stmt] | None
    line: int

    def __repr__(self) -> str:
        return (
            f"IfStmt(boolean_expr={self.boolean_expr}, "
            f"if_stmts={self.if_stmts}, else_stmts={self.else_stmts})"
        )


@dataclass
class ForStmt(Stmt):
    init: VarStmt | None
    condition: Expr
    for_step: Stmt | None
    for_stmts: Stmts | list[Stmt]
    line: int

    def __repr__(self) -> str:
        return (
            f"ForStmt(init={self.init}, condition={self.condition}, "
            f"for_step={self.for_step}, for_stmts={self.for_stmts})"
        )


@dataclass
class FuncParam(Node):
    name: str
    param_type: TokenType


@dataclass
class FuncDecl(Stmt):
    name: str
    params: list[FuncParam]
    func_type: TokenType
    body: list[Stmt]
    line: int


@dataclass
class RetStmt(Stmt):
    value: Expr
    line: int


@dataclass
class FuncCall(Expr):
    name: str
    arguments: list[Expr]
    line: int
    type: TokenType | None = None
