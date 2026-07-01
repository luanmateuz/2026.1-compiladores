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
from fucklang.symbol import SymbolTable
from fucklang.token import TokenType


@dataclass
class CodeGenerator:
    symbol_table: SymbolTable = field(default_factory=SymbolTable)
    sam_code: list[str] = field(default_factory=list)
    label_counter: int = 0

    def build(self, ast):
        if self.symbol_table.curr > 0:
            self.sam_code.append(f"ADDSP {self.symbol_table.curr}")

        for node in ast:
            self.visit(node)

        if self.symbol_table.curr > 0:
            self.sam_code.append(f"ADDSP -{self.symbol_table.curr}")

        self.sam_code.append("PUSHIMM 0")
        self.sam_code.append("STOP")

        return self.sam_code

    def visit(self, node):
        if isinstance(node, ConstStmt):
            self.const(node)
        elif isinstance(node, VarStmt):
            self.var(node)
        elif isinstance(node, Identifier):
            self.identifier(node)
        elif isinstance(node, AssignStmt):
            self.assign(node)
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
        elif isinstance(node, PutsStmt):
            self.puts(node)

    def new_label(self, name: str) -> str:
        label_name = f"LABEL_{name}_{self.label_counter}"
        self.label_counter += 1

        return label_name

    def const(self, node: ConstStmt):
        self.visit(node.value)
        symbol = self.symbol_table.resolve(node.name.lexeme)
        self.sam_code.append(f"STOREOFF {symbol.offset}")

    def var(self, node: VarStmt):
        self.visit(node.value)
        symbol = self.symbol_table.resolve(node.name.lexeme)
        self.sam_code.append(f"STOREOFF {symbol.offset}")

    def assign(self, node: AssignStmt):
        self.visit(node.right)
        symbol = self.symbol_table.resolve(node.left.lexeme)

        self.sam_code.append(f"STOREOFF {symbol.offset}")

    def identifier(self, node: Identifier):
        # self.sam_code.append(f"PUSHOFF {node.name}")
        self.sam_code.append(
            f"PUSHOFF {self.symbol_table.symbols[node.name].offset}"
        )

    def integer(self, node: Integer):
        self.sam_code.append(f"PUSHIMM {node.value} // integer")

    def float(self, node: Float):
        self.sam_code.append(f"PUSHIMMF {node.value} // float")

    def boolean(self, node: Boolean):
        v = 1 if node.value else 0
        self.sam_code.append(f"PUSHIMM {v} // boolean 1-true 0-false")

    def character(self, node: Character):
        self.sam_code.append(f"PUSHIMMCH {node.value} // character")

    def string(self, node: String):
        raise SystemError(f"Not implemented STRING! {node}")
        # self.sam_code.append(f"PUSHIMMSTR {node.value} # string")

    def unary_op(self, node: UnaryOp):
        self.visit(node.operand)
        if node.op.type == TokenType.MINUS:
            if isinstance(node.operand, Float):
                self.sam_code.append("PUSHIMMF -1.0")
                self.sam_code.append("TIMESF")
            else:
                self.sam_code.append("PUSHIMM -1")
                self.sam_code.append("TIMES")
        elif node.op.type == TokenType.NOT:
            # ISNIL: This is equivalent to the NOT instruction
            self.sam_code.append("ISNIL")

    def binary_op(self, node: BinaryOp):
        self.visit(node.left)
        self.visit(node.right)

        is_float = isinstance(node.left, Float)

        if node.op.type == TokenType.PLUS:
            if is_float:
                self.sam_code.append("ADDF")
            else:
                self.sam_code.append("ADD")
        elif node.op.type == TokenType.MINUS:
            if is_float:
                self.sam_code.append("SUBF")
            else:
                self.sam_code.append("SUB")
        elif node.op.type == TokenType.ASTERISK:
            if is_float:
                self.sam_code.append("TIMESF")
            else:
                self.sam_code.append("TIMES")
        elif node.op.type == TokenType.SLASH:
            if is_float:
                self.sam_code.append("DIVF")
            else:
                self.sam_code.append("DIV")
        elif node.op.type == TokenType.MOD:
            self.sam_code.append("MOD")
        elif node.op.type == TokenType.GT:
            self.sam_code.append("GREATER")
        elif node.op.type == TokenType.GE:
            self.sam_code.append("GREATER")
            self.visit(node.left)
            self.visit(node.right)
            self.sam_code.append("EQUAL")
            self.sam_code.append("OR")
        elif node.op.type == TokenType.LT:
            self.sam_code.append("LESS")
        elif node.op.type == TokenType.LE:
            self.sam_code.append("LESS")
            self.visit(node.left)
            self.visit(node.right)
            self.sam_code.append("EQUAL")
            self.sam_code.append("OR")
        elif node.op.type == TokenType.EQ:
            self.sam_code.append("EQUAL")
        elif node.op.type == TokenType.NE:
            self.sam_code.append("EQUAL")
            self.sam_code.append("ISNIL")

    def logical_or(self, node: LogicalOr):
        self.visit(node.left)
        self.visit(node.right)
        self.sam_code.append("OR")

    def logical_and(self, node: LogicalAnd):
        self.visit(node.left)
        self.visit(node.right)
        self.sam_code.append("AND")

    def paren_group(self, node: ParenGroup):
        self.visit(node.value)

    def stmts(self, node: Stmts):
        for s in node.stmts:
            self.visit(s)

    def if_stmt(self, node: IfStmt):
        label_else = self.new_label("ELSE")
        label_end = self.new_label("END")

        self.visit(node.boolean_expr)
        self.sam_code.append("ISNIL")

        self.sam_code.append(f"JUMPC {label_else}")

        if isinstance(node.if_stmts, list):
            for s in node.if_stmts:
                self.visit(s)
        else:
            self.visit(node.if_stmts)

        self.sam_code.append(f"JUMP {label_end}")

        self.sam_code.append(f"{label_else}:")
        if node.else_stmts:
            if isinstance(node.else_stmts, list):
                for s in node.else_stmts:
                    self.visit(s)
            else:
                self.visit(node.else_stmts)

        self.sam_code.append(f"{label_end}:")

    def for_stmt(self, node: ForStmt):
        label_for_start = self.new_label("FOR_START")
        label_for_end = self.new_label("FOR_END")

        if node.init:
            self.visit(node.init)

        self.sam_code.append(f"{label_for_start}:")
        self.visit(node.condition)
        self.sam_code.append("ISNIL")

        self.sam_code.append(f"JUMPC {label_for_end}")

        if isinstance(node.for_stmts, list):
            for s in node.for_stmts:
                self.visit(s)
        else:
            self.visit(node.for_stmts)

        if node.for_step:
            self.visit(node.for_step)

        self.sam_code.append(f"JUMP {label_for_start}")
        self.sam_code.append(f"{label_for_end}:")

    def puts(self, node: PutsStmt):
        if isinstance(node.expr, Identifier):
            name = node.expr.name
            offset = self.symbol_table.symbols[name].offset
            type = self.symbol_table.symbols[name].type

            self.sam_code.append(f"PUSHOFF {offset}")

            if type == TokenType.FLT_TYPE:
                self.sam_code.append("WRITEF")
            elif type == TokenType.CHR_TYPE:
                self.sam_code.append("WRITECH")
            elif type == TokenType.STR_TYPE:
                self.sam_code.append("WRITESTR")
            else:
                self.sam_code.append("WRITE")
        elif isinstance(node.expr, Character):
            self.visit(node.expr)
            self.sam_code.append("WRITECH")
        elif isinstance(node.expr, Integer):
            self.visit(node.expr)
            self.sam_code.append("WRITE")
        elif isinstance(node.expr, Float):
            self.visit(node.expr)
            self.sam_code.append("WRITEF")
        elif isinstance(node.expr, String):
            self.visit(node.expr)
            self.sam_code.append("WRITESTR")
        elif isinstance(node.expr, BinaryOp):
            # Work for BinaryOp INTEGERS
            # e.g: i = 1, then, i + 1 = 2
            # e.g: puts(i + 1);
            self.visit(node.expr)
            self.sam_code.append("WRITE")
        else:
            raise SyntaxError(f"Not implemented PutsStmt for {node.expr}")
