from app.Lox.Scanner import Scanner

class Lox():
    def runPrompt():
        while(True):
            print("> ")
            line = input()
            if not line:
                return
            
            Lox.run(line)
            Scanner.hadError = false

    def runFile(path: str):
        with open(path, "r") as file:
            file_content = file.read()

        Lox.run(file_content)
        if Scanner.hadError:
            exit(65)
            
    def run(source: str):
        scanner = Scanner(source)

        for token in scanner.scanTokens():
            print(token)