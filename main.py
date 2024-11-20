import sys
from src.lexer import Lexer
from src.hdl import HDL

def main():
    # incorrect number of args
    # must equal 3 because first arg is always the name of this script
    if len(sys.argv) != 3:
        print("Must provide source and destination files. Usage: python3 main.py <hdl source> <python dest>")
        sys.exit(64)
    else:
        compile_to_python(sys.argv[1], sys.argv[2])


def compile_to_python(source_path, dest_filename):
    with open(source_path, 'r') as source_file:
        source = source_file.read()
        generated_python = compile_file(source)
        print(generated_python)
    with open(f"compiled_files/{dest_filename}", "w") as dest_file:
        dest_file.write(generated_python)


def compile_file(source_text):
    lexer = Lexer(source_text)
    tokens = lexer.scan_tokens()

    # if there was an error, don't compile the file
    if HDL.had_error:
        sys.exit(65)

    # just printing the tokens for now
    token_text = ""

    for token in tokens:
        token_text += f"[{token}]\n"

    return token_text


if __name__ == "__main__":
    main()