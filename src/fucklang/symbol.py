from dataclasses import dataclass, field

from fucklang.node import (
    AssignStmt,
    BinaryOp,
    Boolean,
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
    Stmts,
    String,
    UnaryOp,
    VarStmt,
)
from fucklang.token import TokenType


@dataclass
class Symbol:
    idx: str
    type: TokenType
    offset: int
    mutable: bool


@dataclass
class SymbolTable:
    symbols: dict[str, Symbol] = field(default_factory=dict)
    curr: int = 0

    def declare(self, name, type, mutable=True):
        if name in self.symbols:
            raise SyntaxError(f"{name} is already declared.")

        symbol = Symbol(name, type, self.curr, mutable)
        self.symbols[name] = symbol
        self.curr += 1

        return symbol

    def resolve(self, name):
        if name not in self.symbols:
            raise SyntaxError(f"{name} is not declared.")

        return self.symbols[name]


@dataclass
class SemanticAnalyzer:
    symbol_table: SymbolTable = field(default_factory=SymbolTable)

    def analyze(self, ast):
        for node in ast:
            self.visit(node)

        return self.symbol_table

    def visit(self, node):
        if isinstance(node, ConstStmt):
            self.const_stmt(node)
        elif isinstance(node, VarStmt):
            self.var_stmt(node)
        elif isinstance(node, AssignStmt):
            self.assign_stmt(node)
        elif isinstance(node, Identifier):
            self.identifier(node)
        elif isinstance(node, Integer):
            self.integer(node)
        elif isinstance(node, Float):
            self.float(node)
        elif isinstance(node, Boolean):
            self.boolean(node)
        elif isinstance(node, Character):
            self.character(node)
        elif isinstance(node, String):
            self.string(node)
        elif isinstance(node, PutsStmt):
            self.puts_stmt(node)
        elif isinstance(node, UnaryOp):
            self.unary_op(node)
        elif isinstance(node, BinaryOp):
            self.binary_op(node)
        elif isinstance(node, LogicalOr):
            self.logical_or(node)
        elif isinstance(node, LogicalAnd):
            self.logical_and(node)
        elif isinstance(node, ParenGroup):
            self.paren_group(node)
        elif isinstance(node, Stmts):
            self.stmts(node)
        elif isinstance(node, IfStmt):
            self.if_stmt(node)
        elif isinstance(node, ForStmt):
            self.for_stmt(node)
        else:
            raise SyntaxError(f"Visit {node} not implemented.")

    def integer(self, node: Integer):
        pass

    def float(self, node: Float):
        pass

    def boolean(self, node: Boolean):
        pass

    def character(self, node: Character):
        pass

    def string(self, node: String):
        pass

    def identifier(self, node: Identifier):
        self.symbol_table.resolve(node.name)

    def const_stmt(self, node: ConstStmt):
        self.visit(node.value)
        self.symbol_table.declare(node.name.lexeme, node.type, mutable=False)

    def var_stmt(self, node: VarStmt):
        self.visit(node.value)

        self.symbol_table.declare(node.name.lexeme, node.type)

    def assign_stmt(self, node: AssignStmt):
        self.visit(node.right)
        symbol = self.symbol_table.resolve(node.left.lexeme)

        if not symbol.mutable:
            raise SyntaxError(
                f"[Line {node.line}] Error:"
                f"Cannot assign to const {node.left.lexeme}"
            )

    def puts_stmt(self, node: PutsStmt):
        self.visit(node.expr)

    def unary_op(self, node: UnaryOp):
        self.visit(node.operand)

    def binary_op(self, node: BinaryOp):
        self.visit(node.left)
        self.visit(node.right)

    def logical_or(self, node: LogicalOr):
        self.visit(node.left)
        self.visit(node.right)

    def logical_and(self, node: LogicalAnd):
        self.visit(node.left)
        self.visit(node.right)

    def paren_group(self, node: ParenGroup):
        self.visit(node.value)

    def stmts(self, node: Stmts):
        for s in node.stmts:
            self.visit(s)

    def if_stmt(self, node: IfStmt):
        self.visit(node.boolean_expr)

        if isinstance(node.if_stmts, list):
            for s in node.if_stmts:
                self.visit(s)
        else:
            self.visit(node.if_stmts)

        if node.else_stmts:
            if isinstance(node.else_stmts, list):
                for s in node.else_stmts:
                    self.visit(s)
            else:
                self.visit(node.else_stmts)

    def for_stmt(self, node: ForStmt):
        if node.init:
            self.visit(node.init)

        self.visit(node.condition)

        if node.for_step:
            self.visit(node.for_step)

        if isinstance(node.for_stmts, list):
            for s in node.for_stmts:
                self.visit(s)
        else:
            self.visit(node.for_stmts)
