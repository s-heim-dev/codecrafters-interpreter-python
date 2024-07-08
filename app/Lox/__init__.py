from app.Lox.LoxError import LoxError
from app.Lox.Scanner import Scanner
from app.Lox.Token import Token
from app.Lox.TokenType import TokenType

class Lox():
    def runPrompt():
        while(True):
            print("> ")
            line = input()
            if not line:
                return
            
            Lox.run(line)
            LoxError.hadError = False

    def runFile(path: str):
        with open(path, "r") as file:
            file_content = file.read()

        Lox.run(file_content)
        if LoxError.hadError:
            exit(65)
            
    def run(source: str):
        scanner = Scanner(source)

        for token in scanner.scanTokens():
            print(token)