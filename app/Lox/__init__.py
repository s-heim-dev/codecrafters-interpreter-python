import sys

from app.Lox.LoxError import LoxError
from app.Lox.Parser import Parser
from app.Lox.Scanner import Scanner
from app.Lox.Interpreter import Interpreter

class Lox():
    def runPrompt() -> None:
        while(True):
            print("> ")
            line = input()
            if not line:
                return

            Lox.evaluate(line)
            LoxError.hadSyntaxError = False
            LoxError.hadRuntimeError = False

    def runFile(path: str, command: str) -> None:
        with open(path, "r") as file:
            file_content = file.read()

        if command == "tokenize":
            Lox.tokenize(file_content)
        elif command == "parse":
            Lox.parse(file_content)
        elif command == "evaluate" or command == "run":
            Lox.evaluate(file_content, command="run")
        else:
            print(f"Unknown command: {command}", file=sys.stderr)
            exit(1)

        if LoxError.hadSyntaxError and not command == "evaluate":
            exit(65)
        elif LoxError.hadRuntimeError:
            exit(70)
            
    def tokenize(source: str) -> None:
        scanner = Scanner(source)
        for token in scanner.scanTokens():
            print(token)
    
    def parse(source: str) -> None:
        scanner = Scanner(source)
        tokens = scanner.scanTokens()
        parser = Parser(tokens)
        statements = parser.parse()
        if not LoxError.hadError():
            [print(statement) for statement in statements]
    
    def evaluate(source: str, command: str = "evaluate") -> None:
        scanner = Scanner(source)
        tokens = scanner.scanTokens()
        parser = Parser(tokens)
        statements = parser.parse(command == "evaluate")
        if not statements:
            return
        interpreter = Interpreter()
        interpreter.interpret(statements, command == "run")
