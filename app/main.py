import sys

from app.Lox import Lox

def main():
    if len(sys.argv) == 1:
        Lox.runPrompt()
        exit(0)
    
    if len(sys.argv) < 3:
        print("Usage: ./your_program.sh tokenize <filename>", file=sys.stderr)
        exit(1)

    command = sys.argv[1]
    filename = sys.argv[2]

    Lox.runFile(filename, command)

if __name__ == "__main__":
    main()
