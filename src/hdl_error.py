from src.hdl import HDL

class HDLError:
    def error(line, message):
        HDLError.report(line, "", message)

    def report(line, where, message):
        print(f"[line {line}] Error {where}: {message}")
        HDL.had_error = True
