import sys

from app.Lox.LoxError import LoxError
from app.Lox.Parser import Parser
from app.Lox.Scanner import Scanner

class Lox():
    def runPrompt() -> None:
        while(True):
            print("> ")
            line = input()
            if not line:
                return

            Lox.parse(line)
            LoxError.hadError = False

    def runFile(path: str, command: str) -> None:
        with open(path, "r") as file:
            file_content = file.read()

        if command == "tokenize":
            Lox.tokenize(file_content)
        elif command == "parse":
            Lox.parse(file_content)
        else:
            print(f"Unknown command: {command}", file=sys.stderr)
            exit(1)

        if LoxError.hadError:
            exit(65)
            
    def tokenize(source: str) -> None:
        scanner = Scanner(source)
        for token in scanner.scanTokens():
            print(token)
    
    def parse(source: str) -> None:
        scanner = Scanner(source)
        tokens = scanner.scanTokens()
        parser = Parser(tokens)
        tree = parser.parse()
        if not LoxError.hadError:
            print(tree)
