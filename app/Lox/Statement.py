from app.Lox.Expression import Expr

class Stmt():
    pass

class Stmt(Stmt):
    class Expression(Stmt):
        def __init__(self, expression: Expr):
            self.expression = expression
        
        def __str__(self) -> str:
            return str(self.expression)
        
        def __repr__(self) -> str:
            return self.__str__()

    class Print(Stmt):
        def __init__(self, expression: Expr):
            self.expression = expression
        
        def __str__(self) -> str:
            return f"PRINT {self.expression}"
        
        def __repr__(self) -> str:
            return self.__str__()

