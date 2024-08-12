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

    def evalBinary(self, expr: Expression.Binary) -> object:
        return expr
    
    def evalUnary(self, expr: Expression.Unary) -> object:
        right = self.evaluate(expr.right)

        if (expr.operator.tokenType == TokenType.MINUS):
            return -1 * right
        if (expr.operator.tokenType == TokenType.BANG):
            return not self.isTruthy(right)
        
        return None

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
            Lox.runtimeError(error)
    
    