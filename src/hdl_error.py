class HDLError:
    had_error = False

    def error(line, message):
        HDLError.report(line, "", message)

    def report(line, where, message):
        print(f"[line {line}] Error {where}: {message}")
        HDLError.had_error = True
