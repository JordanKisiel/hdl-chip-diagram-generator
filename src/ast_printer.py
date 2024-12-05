from src.grammar import Vistor

class AST_Printer(Vistor):
    def print(self, rule):
        return rule.accept(self)
    
    def visit_chip_spec(self, rule):
        lines = []
        lines.append(f"{rule.chip_token.lexeme} {rule.ident_token.lexeme} {rule.left_brace_token.lexeme}")
        return self.print_lines(lines)

    def visit_body(self, grammar_rule):
        pass

    def visit_bus(self, grammar_rule):
        pass

    def visit_chip_io(self, grammar_rule):
        pass

    def visit_connection(self, grammar_rule):
        pass

    def visit_connections_list(self, grammar_rule):
        pass

    def visit_header(self, grammar_rule):
        pass

    def visit_part(self, grammar_rule):
        pass

    def visit_range(self, grammar_rule):
        pass

    def visit_sub_bus(self, grammar_rule):
        pass

    def print_lines(self, lines):
        return '\n'.join(lines)