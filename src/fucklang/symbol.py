from dataclasses import dataclass, field

from fucklang.node import (
    AssignStmt,
    BinaryOp,
    Boolean,
    Character,
    ConstStmt,
    Float,
    ForStmt,
    FuncCall,
    FuncDecl,
    Identifier,
    IfStmt,
    Integer,
    LogicalAnd,
    LogicalOr,
    ParenGroup,
    PutsStmt,
    RetStmt,
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
    is_func: bool = False
    params: list = field(default_factory=list)

    def __repr__(self) -> str:
        return (
            f"Symbol(idx={self.idx}, type={self.type}, "
            f"offset={self.offset}, mutable={self.mutable}, "
            f"is_func={self.is_func}, params={self.params})"
        )


@dataclass
class SymbolTable:
    parent: "SymbolTable" = None
    symbols: dict[str, Symbol] = field(default_factory=dict)
    curr: int = 0

    def declare(self, name, type, mutable=True, is_func=False, params=None):
        if name in self.symbols:
            raise SyntaxError(f"{name} is already declared in this scope.")

        symbol = Symbol(name, type, self.curr, mutable, is_func, params or [])
        self.symbols[name] = symbol
        self.curr += 1

        return symbol

    def resolve(self, name):
        if name in self.symbols:
            return self.symbols[name]

        if self.parent:
            return self.parent.resolve(name)

        raise SyntaxError(f"'{name}' is not declared.")


@dataclass
class SemanticAnalyzer:
    symbol_table: SymbolTable = field(default_factory=SymbolTable)
    cur_func_ret_type: TokenType | None = None

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

        elif isinstance(node, FuncDecl):
            return self.func_decl(node)

        elif isinstance(node, FuncCall):
            return self.func_call(node)

        elif isinstance(node, RetStmt):
            return self.ret_stmt(node)

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

    def func_decl(self, node: FuncDecl):
        func_ret_type = node.func_type

        self.symbol_table.declare(
            node.name,
            func_ret_type,
            mutable=False,
            is_func=True,
            params=node.params,
        )

        previous_scope = self.symbol_table
        self.symbol_table = SymbolTable(parent=previous_scope)

        old_ret_type = self.cur_func_ret_type
        self.cur_func_ret_type = func_ret_type

        for param in node.params:
            self.symbol_table.declare(
                param.name, param.param_type, mutable=True
            )

        for stmt in node.body:
            self.visit(stmt)

        self.cur_func_ret_type = old_ret_type
        self.symbol_table = previous_scope

    def func_call(self, node: FuncCall):
        symbol = self.symbol_table.resolve(node.name)

        if not symbol.is_func:
            raise SyntaxError(
                f"[Line {node.line}] Error: '{node.name}' is not a function."
            )

        if len(node.arguments) != len(symbol.params):
            raise SyntaxError(
                f"[Line {node.line}] Error: Function '{node.name}' expected "
                f"{len(symbol.params)} arguments, got {len(node.arguments)}."
            )

        for arg, param in zip(node.arguments, symbol.params):
            arg_type = self.visit(arg)
            expected_type = param.param_type

            if arg_type != expected_type:
                raise SyntaxError(
                    f"[Line {node.line}] Error: Invalid argument "
                    f"type for '{node.name}'. "
                    f"Expected {expected_type}, got {arg_type}."
                )

        node.type = symbol.type
        return symbol.type

    def ret_stmt(self, node: RetStmt):
        if self.cur_func_ret_type is None:
            raise SyntaxError(
                f"[Line {node.line}] Error: 'ret' statement outside function."
            )

        ret_value_type = (
            self.visit(node.value) if node.value else TokenType.VOID_TYPE
        )

        if ret_value_type != self.cur_func_ret_type:
            raise SyntaxError(
                f"[Line {node.line}] Error: Return type mismatch. "
                f"Expected {self.cur_func_ret_type}, got {ret_value_type}."
            )
