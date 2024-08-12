from app.Lox.LoxError import LoxError, LoxRuntimeError, ParseError
from app.Lox.Expression import Expression
from app.Lox.Token import Token
from app.Lox.TokenType import TokenType

class Interpreter():
    def evaluate(self, expr: Expression) -> object:
        if (type(expr) == Expression.Literal):
            return self.evalLiteral(expr)
        if (type(expr) == Expression.Grouping):
            return self.evalGrouping(expr)
        if (type(expr) == Expression.Binary):
            return self.evalBinary(expr)
        if (type(expr) == Expression.Unary):
            return self.evalUnary(expr)

        raise LoxRuntimeError(expr)

    def evalLiteral(self, expr: Expression.Literal) -> object:
        return expr.value

    def evalGrouping(self, expr: Expression.Grouping) -> object:
        return self.evaluate(expr.expression)
    
    def evalUnary(self, expr: Expression.Unary) -> object:
        right = self.evaluate(expr.right)

        if (expr.operator.tokenType == TokenType.MINUS):
            self.checkNumberOperand(expr.operator, right)
            return -1 * right
        if (expr.operator.tokenType == TokenType.BANG):
            return not self.isTruthy(right)
        
        return None
    
    def evalBinary(self, expr: Expression.Binary) -> object:
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
        raise LoxRuntimeError(operator, "Operand must be a number")
        
    def checkNumberOperands(self, operator: Token, left: object, right: object) -> None:
        if (type(left) == float and type(right) == float):
            return
        raise LoxRuntimeError(operator, "Operands must be numbers")
    
    def checkNumberOrStringOperands(self, operator: Token, left: object, right: object) -> None:
        if (type(left) == float and type(right) == float):
            return
        if (type(left) == str and type(right) == str):
            return
        raise LoxRuntimeError(operator, "Operands must be numbers or strings")

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
    
    def interpret(self, expr: Expression) -> None:
        try:
            value = self.evaluate(expr)
            print(self.stringify(value))
        except LoxRuntimeError as error:
            LoxError.runtimeError(error)
    
    