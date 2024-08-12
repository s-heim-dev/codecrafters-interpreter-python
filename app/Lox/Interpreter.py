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
        if (type(expr.value) == float and int(expr.value) == expr.value):
            return int(expr.value)

        return expr.value

    def evalGrouping(self, expr: Expression.Grouping) -> object:
        return self.evaluate(expr.expression)

    def evalBinary(self, expr: Expression.Binary) -> object:
        return expr
    
    def evalUnary(self, expr: Expression.Unary) -> object:
        right = self.evaluate(expr.right)

        if (expr.operator.tokenType == TokenType.MINUS):
            return -1 * right
        
        return None
    
    def interpret(self, expr: Expression) -> None:
        try:
            value = self.evaluate(expr)
            print(value)
        except LoxRuntimeError as error:
            Lox.runtimeError(error)
    
    