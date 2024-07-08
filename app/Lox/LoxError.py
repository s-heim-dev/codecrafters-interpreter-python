import sys

class LoxError():
    hadError = False

    def error(line: int, message: str):
        LoxError.report(line, "", message)
    
    def report(line: int, where: str, message: str):
        print(f"[line {line}] Error{where}: {message}", file=sys.stderr)
        LoxError.hadError = True