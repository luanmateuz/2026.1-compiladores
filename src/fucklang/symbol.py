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
            return self.const_stmt(node)

        elif isinstance(node, VarStmt):
            return self.var_stmt(node)

        elif isinstance(node, AssignStmt):
            return self.assign_stmt(node)

        elif isinstance(node, Identifier):
            return self.identifier(node)

        elif isinstance(node, Integer):
            return self.integer()

        elif isinstance(node, Float):
            return self.float()

        elif isinstance(node, Boolean):
            return self.boolean()

        elif isinstance(node, Character):
            return self.character()

        elif isinstance(node, String):
            return self.string()

        elif isinstance(node, PutsStmt):
            return self.puts_stmt(node)

        elif isinstance(node, UnaryOp):
            return self.unary_op(node)

        elif isinstance(node, BinaryOp):
            return self.binary_op(node)

        elif isinstance(node, LogicalOr):
            return self.logical_or(node)

        elif isinstance(node, LogicalAnd):
            return self.logical_and(node)

        elif isinstance(node, ParenGroup):
            return self.paren_group(node)

        elif isinstance(node, Stmts):
            return self.stmts(node)

        elif isinstance(node, IfStmt):
            return self.if_stmt(node)

        elif isinstance(node, ForStmt):
            return self.for_stmt(node)

        raise SyntaxError(f"Visit {node} not implemented.")

    def integer(self):
        return TokenType.INT_TYPE

    def float(self):
        return TokenType.FLT_TYPE

    def boolean(self):
        return TokenType.BOO_TYPE

    def character(self):
        return TokenType.CHR_TYPE

    def string(self):
        return TokenType.STR_TYPE

    def identifier(self, node: Identifier):
        symbol = self.symbol_table.resolve(node.name)
        return symbol.type

    def const_stmt(self, node: ConstStmt):
        expr_type = self.visit(node.value)

        if expr_type != node.type:
            raise SyntaxError(
                f"[Line {node.line}] Error: "
                f"expected {node.type}, got {expr_type}."
            )

        self.symbol_table.declare(
            node.name.lexeme,
            node.type,
            mutable=False,
        )

    def var_stmt(self, node: VarStmt):
        expr_type = self.visit(node.value)

        if expr_type != node.type:
            raise SyntaxError(
                f"[Line {node.line}] Error: "
                f"expected {node.type}, got {expr_type}."
            )

        self.symbol_table.declare(
            node.name.lexeme,
            node.type,
        )

    def assign_stmt(self, node: AssignStmt):
        expr_type = self.visit(node.right)

        symbol = self.symbol_table.resolve(node.left.lexeme)

        if not symbol.mutable:
            raise SyntaxError(
                f"[Line {node.line}] Error: "
                f"cannot assign to constant "
                f"'{node.left.lexeme}'."
            )

        if expr_type != symbol.type:
            raise SyntaxError(
                f"[Line {node.line}] Error: "
                f"expected {symbol.type}, got {expr_type}."
            )

    def puts_stmt(self, node: PutsStmt):
        return self.visit(node.expr)

    def unary_op(self, node: UnaryOp):
        operand_type = self.visit(node.operand)

        if node.op.type == TokenType.NOT:
            if operand_type != TokenType.BOO_TYPE:
                raise SyntaxError(
                    f"[Line {node.line}] Error: '!'requires boo operand."
                )

            return TokenType.BOO_TYPE

        return operand_type

    def binary_op(self, node: BinaryOp):
        left = self.visit(node.left)
        right = self.visit(node.right)

        if left != right:
            raise SyntaxError(f"[Line {node.line}] Error: {left} != {right}")

        arithmetic_ops = (
            TokenType.PLUS,
            TokenType.MINUS,
            TokenType.ASTERISK,
            TokenType.SLASH,
            TokenType.MOD,
        )

        relational_ops = (
            TokenType.LT,
            TokenType.LE,
            TokenType.GT,
            TokenType.GE,
            TokenType.EQ,
            TokenType.NE,
        )

        if node.op.type in arithmetic_ops:
            if left == TokenType.BOO_TYPE:
                raise SyntaxError(
                    f"[Line {node.line}] Error: "
                    f"invalid arithmetic operation on boos."
                )

            return left

        if node.op.type in relational_ops:
            return TokenType.BOO_TYPE

        return left

    def logical_or(self, node: LogicalOr):
        left = self.visit(node.left)
        right = self.visit(node.right)

        if left != TokenType.BOO_TYPE:
            raise SyntaxError(
                f"[Line {node.line}] Error: left operand must be bool."
            )

        if right != TokenType.BOO_TYPE:
            raise SyntaxError(
                f"[Line {node.line}] Error: right operand must be bool."
            )

        return TokenType.BOO_TYPE

    def logical_and(self, node: LogicalAnd):
        left = self.visit(node.left)
        right = self.visit(node.right)

        if left != TokenType.BOO_TYPE:
            raise SyntaxError(
                f"[Line {node.line}] Error: left operand must be bool."
            )

        if right != TokenType.BOO_TYPE:
            raise SyntaxError(
                f"[Line {node.line}] Error: right operand must be bool."
            )

        return TokenType.BOO_TYPE

    def paren_group(self, node: ParenGroup):
        return self.visit(node.value)

    def stmts(self, node: Stmts):
        for stmt in node.stmts:
            self.visit(stmt)

    def if_stmt(self, node: IfStmt):
        condition_type = self.visit(node.boolean_expr)

        if condition_type != TokenType.BOO_TYPE:
            raise SyntaxError(
                f"[Line {node.line}] Error: if condition must be boo."
            )

        if isinstance(node.if_stmts, list):
            for stmt in node.if_stmts:
                self.visit(stmt)
        else:
            self.visit(node.if_stmts)

        if node.else_stmts:
            if isinstance(node.else_stmts, list):
                for stmt in node.else_stmts:
                    self.visit(stmt)
            else:
                self.visit(node.else_stmts)

    def for_stmt(self, node: ForStmt):
        if node.init:
            self.visit(node.init)

        condition_type = self.visit(node.condition)

        if condition_type != TokenType.BOO_TYPE:
            raise SyntaxError(
                f"[Line {node.line}] Error: for condition must be boo."
            )

        if node.for_step:
            self.visit(node.for_step)

        if isinstance(node.for_stmts, list):
            for stmt in node.for_stmts:
                self.visit(stmt)
        else:
            self.visit(node.for_stmts)
