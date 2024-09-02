from typing import List

from app.Lox.LoxError import LoxError, LoxRuntimeError, ParseError
from app.Lox.Environment import Environment
from app.Lox.Expression import Expr
from app.Lox.Statement import Stmt
from app.Lox.Token import Token
from app.Lox.TokenType import TokenType

class Interpreter():
    def __init__(self):
        self.environment = Environment()

    def evaluate(self, expr: Expr) -> object:
        if expr == None:
            return None

        if (type(expr) == Expr.Literal):
            return self.evalLiteral(expr)
        if (type(expr) == Expr.Grouping):
            return self.evalGrouping(expr)
        if (type(expr) == Expr.Binary):
            return self.evalBinary(expr)
        if (type(expr) == Expr.Unary):
            return self.evalUnary(expr)
        if (type(expr) == Expr.Variable):
            return self.evalVariable(expr)
        if (type(expr) == Expr.Assign):
            return self.evalAssignment(expr)

        raise LoxRuntimeError(expr, "Unknown expression type")

    def evalAssignment(self, expr: Expr.Assign) -> object:
        value = self.evaluate(expr.value)
        self.environment.define(expr.name.lexeme, value)
        return value
    
    def evalVariable(self, expr: Expr.Variable) -> object:
        return self.environment.get(expr.name)

    def evalLiteral(self, expr: Expr.Literal) -> object:
        return expr.value

    def evalGrouping(self, expr: Expr.Grouping) -> object:
        return self.evaluate(expr.expression)
    
    def evalUnary(self, expr: Expr.Unary) -> object:
        right = self.evaluate(expr.right)

        if (expr.operator.tokenType == TokenType.MINUS):
            self.checkNumberOperand(expr.operator, right)
            return -1 * right
        if (expr.operator.tokenType == TokenType.BANG):
            return not self.isTruthy(right)
        
        return None
    
    def evalBinary(self, expr: Expr.Binary) -> object:
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)
    
        if (expr.operator.tokenType == TokenType.PLUS):
            self.checkNumberOrStringOperands(expr.operator, left, right)
            return left + right
        if (expr.operator.tokenType == TokenType.MINUS):
            self.checkNumberOperands(expr.operator, left, right)
            return left - right
        if (expr.operator.tokenType == TokenType.STAR):
            self.checkNumberOperands(expr.operator, left, right)
            return left * right
        if (expr.operator.tokenType == TokenType.SLASH):
            self.checkNumberOperands(expr.operator, left, right)
            return left / right
        if (expr.operator.tokenType == TokenType.GREATER):
            self.checkNumberOperands(expr.operator, left, right)
            return left > right
        if (expr.operator.tokenType == TokenType.GREATER_EQUAL):
            self.checkNumberOperands(expr.operator, left, right)
            return left >= right
        if (expr.operator.tokenType == TokenType.LESS):
            self.checkNumberOperands(expr.operator, left, right)
            return left < right
        if (expr.operator.tokenType == TokenType.LESS_EQUAL):
            self.checkNumberOperands(expr.operator, left, right)
            return left <= right
        if (expr.operator.tokenType == TokenType.EQUAL_EQUAL):
            return left == right
        if (expr.operator.tokenType == TokenType.BANG_EQUAL):
            return left != right
        
        return None

    def checkNumberOperand(self, operator: Token, operand: object) -> None:
        if (type(operand) == float):
            return
        raise LoxRuntimeError(operator, "Operand must be a number.")
        
    def checkNumberOperands(self, operator: Token, left: object, right: object) -> None:
        if (type(left) == float and type(right) == float):
            return
        raise LoxRuntimeError(operator, "Operands must be numbers.")
    
    def checkNumberOrStringOperands(self, operator: Token, left: object, right: object) -> None:
        if (type(left) == float and type(right) == float):
            return
        if (type(left) == str and type(right) == str):
            return
        raise LoxRuntimeError(operator, "Operands must be two numbers or two strings.")

    def isTruthy(self, obj: object) -> bool:
        if obj == None:
            return False
        if type(obj) == bool:
            return bool(obj)
        return True
    
    def stringify(self, obj: object) -> str:
        if (obj == None):
            return "nil"
        if (type(obj) == float):
            if (str(obj).endswith(".0")):
                return str(int(obj))
        if (type(obj) == bool):
            return str(obj).lower()
        
        return str(obj)
    
    def executeBlock(self, statements: List[Stmt], environment: Environment, ignoreExpressions: bool = False):
        previous = self.environment
        try:
            self.environment = environment
            for statement in statements:
                self.execute(statement, ignoreExpressions)
        finally:
            self.environment = previous
    
    def execute(self, statement: Stmt, ignoreExpressions: bool = False) -> None:
        if type(statement) == Stmt.Print or (type(statement) == Stmt.Expression and not ignoreExpressions):
            value = self.evaluate(statement.expression)
            print(self.stringify(value))
        elif type(statement) == Stmt.Var:
            self.environment.define(statement.name.lexeme, self.evaluate(statement.expression))
        elif type(statement) == Stmt.Block:
            self.executeBlock(statement.statements, Environment(), ignoreExpressions)
        else:
            self.evaluate(statement.expression)
    
    def interpret(self, statements: List[Stmt], ignoreExpressions: bool = False) -> None:
        try:
            for statement in statements:
                if statement:
                    self.execute(statement, ignoreExpressions)
        except LoxRuntimeError as error:
            LoxError.runtimeError(error)
    
    