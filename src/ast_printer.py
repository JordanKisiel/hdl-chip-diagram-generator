from src.grammar import * 

class AST_Printer(Vistor):
    strs = []

    def print(self, rule):
        return rule.accept(self)
    
    def visit_chip_spec(self, rule):
        self.strs.append(f"{rule.chip_token.lexeme} {rule.ident_token.lexeme} {rule.left_brace_token.lexeme}\n\n")
        rule.header.accept(self)
        rule.body.accept(self)
        self.strs.append(f"{rule.right_brace_token.lexeme}")
        return self.print_strs(self.strs)

    def visit_body(self, rule):
        self.strs.append(f"{rule.parts_token.lexeme}{rule.colon_token.lexeme}\n") 

        for part in rule.parts_list:
            part.accept(self)

    def visit_bus(self, rule):
        self.strs.append(f"{rule.ident_token.lexeme}") 
        self.strs.append(f"{rule.left_bracket_token.lexeme}") 
        self.strs.append(f"{rule.number_token.lexeme}")
        self.strs.append(f"{rule.right_bracket_token.lexeme}") 

    def visit_chip_io(self, rule):
        if isinstance(rule.ident_or_bus, Bus):
            rule.ident_or_bus.accept(self)
        else:
            self.strs.append(f"{rule.ident_or_bus.lexeme}")
        
        for io in rule.extra_io:
            io.accept(self) 

    def visit_extra_io(self, rule):
        self.strs.append(f"{rule.comma_token.lexeme} ")

        if isinstance(rule.ident_or_bus, Bus):
            self.ident_or_bus.accept(self)
        else:
            self.strs.append(f"{rule.ident_or_bus.lexeme}")

    def visit_connection(self, rule):
        if isinstance(rule.ident_or_sub_bus, Sub_Bus):
            self.ident_or_sub_bus.accept(self)
        else:
            self.strs.append(f"{rule.ident_or_sub_bus.lexeme}")

        self.strs.append(f"{rule.equal_token.lexeme}")
        self.strs.append(f"{rule.ident_or_binary_val.lexeme}")

    def visit_connections_list(self, rule):
        rule.connect_1.accept(self)
        self.strs.append(f"{rule.comma_token.lexeme} ")
        rule.connect_2.accept(self)

        for connection in rule.extra_connections:
            connection.accept(self)

    def visit_extra_connection(self, rule):
        self.strs.append(f"{rule.comma_token.lexeme} ")
        rule.connection.accept(self)

    def visit_header(self, rule):
        self.strs.append(f"{rule.in_token.lexeme} ")
        rule.chip_io_1.accept(self)
        self.strs.append(f"{rule.semi_token_1.lexeme}\n")
        self.strs.append(f"{rule.out_token.lexeme} ")
        rule.chip_io_2.accept(self)
        self.strs.append(f"{rule.semi_token_2.lexeme}\n")
        self.strs.append(f"\n")

    def visit_part(self, rule):
        self.strs.append(f"{rule.ident_token.lexeme}")
        self.strs.append(f"{rule.left_paren_token.lexeme}")
        
        rule.connections_list.accept(self)

        self.strs.append(f"{rule.right_paren_token.lexeme}")
        self.strs.append(f"{rule.semi_token.lexeme}\n")

    def visit_range(self, rule):
        self.strs.append(f"{rule.number_token_1.lexeme}") 
        self.strs.append(f"{rule.double_dot_token.lexeme}") 
        self.strs.append(f"{rule.number_token_2.lexeme}") 

    def visit_sub_bus(self, rule):
        self.strs.append(f"{rule.ident_token.lexeme}") 
        self.strs.append(f"{rule.left_bracket_token.lexeme}") 
        
        if isinstance(rule.number_or_range, Range):
            rule.number_or_range.accept(self)
        else:
            self.strs.append(f"{rule.number_or_range.lexeme}")

        self.strs.append(f"{rule.right_bracket_token.lexeme}") 

    def print_strs(self, strs):
        return ''.join(strs)