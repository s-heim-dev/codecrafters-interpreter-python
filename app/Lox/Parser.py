from typing import List

from app.Lox.LoxError import ParseError
from app.Lox.Expression import Expression
from app.Lox.Token import Token
from app.Lox.TokenType import TokenType

class Parser():
    def __init__(self, tokens: List[TokenType]):
        self.tokens = tokens
        self.current = 0
    
    def parse(self) -> Expression:
        try:
            return self.expression()
        except ParseError:
            return None

    def peek(self) -> Token:
        return self.tokens[self.current]
    
    def previous(self) -> Token:
        return self.tokens[self.current - 1]
    
    def isAtEnd(self) -> bool:
        return self.peek().tokenType == TokenType.EOF

    def advance(self) -> Token:
        if not self.isAtEnd():
            self.current += 1
        return self.previous()
    
    def check(self, tokenType: TokenType) -> bool:
        if self.isAtEnd():
            return False
        return self.peek().tokenType == tokenType
    
    def match(self, *types) -> bool:
        for tokenType in types:
            if (self.check(tokenType)):
                self.advance()
                return True
        return False
    
    def expression(self) -> Expression:
        return self.equality()
    
    def equality(self) -> Expression:
        expr = self.comparison()
        while (self.match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL)):
            operator = self.previous()
            right = self.comparison()
            expr = Expression.Binary(expr, operator, right)
        return expr
    
    def comparison(self) -> Expression:
        expr = self.term()
        while(self.match(TokenType.GREATER, TokenType.GREATER_EQUAL, TokenType.LESS, TokenType.LESS_EQUAL)):
            operator = self.previous()
            right = self.term()
            expr = Expression.Binary(expr, operator, right)
        return expr
    
    def term(self) -> Expression:
        expr = self.factor()
        while(self.match(TokenType.MINUS, TokenType.PLUS)):
            operator = self.previous()
            right = self.factor()
            expr = Expression.Binary(expr, operator, right)
        return expr
    
    def factor(self) -> Expression:
        expr = self.unary()
        while(self.match(TokenType.SLASH, TokenType.STAR)):
            operator = self.previous()
            right = self.unary()
            expr = Expression.Binary(expr, operator, right)
        return expr
    
    def unary(self) -> Expression:
        if (self.match(TokenType.BANG, TokenType.MINUS)):
            operator = self.previous()
            right = self.unary()
            return Expression.Unary(operator, right)
        return self.primary()
    
    def primary(self) -> Expression:
        if (self.match(TokenType.FALSE)):
            return Expression.Literal("false")
        if (self.match(TokenType.TRUE)):
            return Expression.Literal("true")
        if (self.match(TokenType.NIL)):
            return Expression.Literal("nil")
        
        if (self.match(TokenType.NUMBER, TokenType.STRING)):
            return Expression.Literal(self.previous().literal)
        
        if (self.match(TokenType.LEFT_PAREN)):
            expr = self.expression()
            self.consume(TokenType.RIGHT_PAREN, "Expect ')' after expression.")
            return Expression.Grouping(expr)
    
    def consume(self, tokenType: TokenType, message: str):
        if (self.check(tokenType)):
            return self.advance()
        
        LoxError.parseError(self.peek(), message)

    