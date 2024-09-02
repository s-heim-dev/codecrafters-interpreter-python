from typing import List

import sys

from app.Lox.LoxError import LoxError, ParseError
from app.Lox.Expression import Expr
from app.Lox.Statement import Stmt
from app.Lox.Token import Token
from app.Lox.TokenType import TokenType

class Parser():
    def __init__(self, tokens: List[TokenType]):
        self.tokens = tokens
        self.current = 0
    
    def parse(self, ignoreSemicolons: bool = False) -> List[Stmt]:
        try:
            statements = []
            while (not self.isAtEnd()):
                statements.append(self.statement(ignoreSemicolons))
            return statements
        except ParseError as error:
            LoxError.runtimeError(error)
            return None

    
    def statement(self, ignoreSemicolons: bool = False) -> Stmt:
        if self.match(TokenType.PRINT):
            return self.printStatement()
        return self.expressionStatement(ignoreSemicolons)
    
    def printStatement(self) -> Stmt:
        expr = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after value.")
        return Stmt.Print(expr)
    
    def expressionStatement(self, ignoreSemicolons: bool = False) -> Stmt:
        expr = self.expression()
        if (not ignoreSemicolons):
            self.consume(TokenType.SEMICOLON, "Expect ';' after value.")
        return Stmt.Expression(expr)

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
    
    def expression(self) -> Expr:
        return self.equality()
    
    def equality(self) -> Expr:
        expr = self.comparison()
        while (self.match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL)):
            operator = self.previous()
            right = self.comparison()
            expr = Expr.Binary(expr, operator, right)
        return expr
    
    def comparison(self) -> Expr:
        expr = self.term()
        while(self.match(TokenType.GREATER, TokenType.GREATER_EQUAL, TokenType.LESS, TokenType.LESS_EQUAL)):
            operator = self.previous()
            right = self.term()
            expr = Expr.Binary(expr, operator, right)
        return expr
    
    def term(self) -> Expr:
        expr = self.factor()
        while(self.match(TokenType.MINUS, TokenType.PLUS)):
            operator = self.previous()
            right = self.factor()
            expr = Expr.Binary(expr, operator, right)
        return expr
    
    def factor(self) -> Expr:
        expr = self.unary()
        while(self.match(TokenType.SLASH, TokenType.STAR)):
            operator = self.previous()
            right = self.unary()
            expr = Expr.Binary(expr, operator, right)
        return expr
    
    def unary(self) -> Expr:
        if (self.match(TokenType.BANG, TokenType.MINUS)):
            operator = self.previous()
            right = self.unary()
            return Expr.Unary(operator, right)
        return self.primary()
    
    def primary(self) -> Expr:
        if (self.match(TokenType.FALSE)):
            return Expr.Literal(False)
        if (self.match(TokenType.TRUE)):
            return Expr.Literal(True)
        if (self.match(TokenType.NIL)):
            return Expr.Literal(None)
        
        if (self.match(TokenType.NUMBER, TokenType.STRING)):
            return Expr.Literal(self.previous().literal)
        
        if (self.match(TokenType.LEFT_PAREN)):
            expr = self.expression()
            self.consume(TokenType.RIGHT_PAREN, "Expect ')' after expression.")
            return Expr.Grouping(expr)
            
        LoxError.parseError(self.peek(), "Expect expression.")
    
    def consume(self, tokenType: TokenType, message: str):
        if (self.check(tokenType)):
            return self.advance()
        
        LoxError.parseError(self.peek(), message)

    