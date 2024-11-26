from colors import Colors

def print_lines():
    with open("./tools/grammar/hdl-grammar.txt", 'r') as grammar_file:
        grammar_lines = grammar_file.readlines()
        lines_to_print = []
        # split out each line into non_term and expansion
        # add to lines list for further processing
        for line in grammar_lines:
            lines_to_print.append(line.split(" => "))
        
        # find the longest non_term
        longest_non_term = 0
        for line in lines_to_print:
            non_term = line[0]
            if len(non_term) > longest_non_term:
                longest_non_term = len(non_term)

        # use length of longest non_term to prefix
        # each non_term with spaces (this will line
        # up each line on =>)
        for line in lines_to_print:
            prefix_len = longest_non_term - len(line[0])
            prefix = " " * prefix_len
            line[0] = f"{prefix}{line[0]}"
        
        # print each line
        for line in lines_to_print:
            non_term = line[0]
            expansion = line[1]
            print(f"{Colors.OKCYAN}{non_term}{Colors.ENDC} => {expansion}")



print_lines()