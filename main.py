'''
    Main Program that reads a lol file and runs the lexer[WIP], syntax analyzer[ON QUEUE]

    Functions:
        display_tok
'''

# Imports
import scanner

# Constants
TEST_PATH = "inputs/power.lol"

def display_tok(tok_list: list):
    '''
        Takes a list of Tokens
        Displays the symbol table with token type and the value of the lexeme
    '''
    print("------- Symbol Table --------")
    for token in tok_list:
        print(f'{token.type}: {token.value}')


if __name__ == "__main__":
    # lol program source code will be stored here
    code_contents = ""

    with open(TEST_PATH, 'r', encoding="utf-8") as lol_file:
        code_contents = lol_file.read()

    # Instantiate the Lexical Analyzer
    lexi = scanner.Scanner(code_contents)
    # Store tokens obtained from scanner
    tok = lexi.tokenize()
    display_tok(tok)
