"""
    Contains the Parser Class to analyze the syntax of the tokenized program

    Classes:
        Parser
"""
# import sys
from typing import List, Dict
from dataclasses import dataclass, field

from scanner import Token

INVALID_PROGRAM_START = "Error: Program start not detected"
# sys.tracebacklimit = 0


@dataclass
class Parser:
    """
    A class for representing a syntax analyzer/parser
    ...
        Attributes:
            tokens: List <Token>
                - stores the list of tokens from a given program
                - pass empty on init
            ast: Dict
                - abstract syntax tree for the grammar checking
            next_t: Token
                - the next token used for checking
            ast_index: int
                - current index in the token list while building the ast
            line: int
                - keeps track of the current line number
    """

    tokens: List[Token]
    ast: Dict
    next_t: Token = None
    ast_index: int = 0
    line: int = 1
    valid_op_types: List = field(
        default_factory=lambda: [
            "R keyword",
            "SUM_OF keyword",
            "DIFF_OF keyword",
            "PRODUKT_OF keyword",
            "QUOSHUNT_OF keyword",
            "MOD_OF keyword",
            "BGGR_OF keyword",
            "SMALLR_OF keyword",
            "UPPIN keyword",
            "NERFIN keyword",
        ]
    )

    def check(self, token_type: str):
        """
        Check the type of the given token
        """

        next_token = self.next_t

        # print(f">>>>>{self.tokens[self.ast_index].value}")

        # print(f">>>>>{next_token}")
        # print(f">>>>>{token_type}")

        if next_token is None:
            raise SyntaxError(
                f"Unexpected end of program {next_token} at Line: {self.line}, expected KTHXBYE"
            )
        if token_type == "expression" and next_token.type not in self.valid_op_types:
            raise SyntaxError(
                f"Invalid Operator: {next_token.value} at Line: {self.line}, expected expression operator"
            )
        elif token_type != "expression" and next_token.type != token_type:
            raise SyntaxError(
                f"Unexpected token: {next_token.value} at Line: {self.line}, expected {token_type}"
            )

        # Update the next_token to the next token ,:)
        self.ast_index += 1
        self.next_t = self.get_next_token()

        return next_token

    def token_limit_reached(self):
        """
        check if ast index exceeds the len of token list
        return True if no more tokens
        return False if has more tokens
        """
        return self.ast_index > (len(self.tokens) - 1)

    def get_next_token(self):
        """
        returns the next token if has more token
        """
        return None if self.token_limit_reached() else self.tokens[self.ast_index]

    def build_ast(self):
        """
        Parse the token list and produces an ast bnf
        """
        # get the root node-> program start -> should always be HAI
        self.next_t = self.get_next_token()
        self.ast = self.program()
        return self.ast

    def program(self):
        """
        Starting: HAI

        <program>: HAI <linebreak> <statement> <linebreak> KTHXBYE

        <program>: BTW <statement>
        """
        c_tok = self.tokens[self.ast_index].value

        if self.tokens[self.ast_index].value == "HAI":
            curr_token = self.check("HAI_keyword")
            return {
                "type": curr_token.type,
                "value": curr_token.value,
                "line": self.line,
                "parent": None,
                "children": [self.statement()],
                # "children": [self.separator()],
            }
        elif self.tokens[self.ast_index].value == "BTW":
            return self.comment_statement()

        raise SyntaxError(f"Unexpected program start {c_tok}, expected HAI")

    def program_end(self):
        """
        <statement> : KTHXBYE <inline comment> | <multiline comment>
        """
        if self.tokens[self.ast_index].value == "KTHXBYE":
            print(self.next_t)
            curr_token = self.check("KTHXBYE_keyword")
            return {
                "type": curr_token.type,
                "value": curr_token.value,
                "line": self.line,
                "parent": self.ast_index - 1,
                "children": [None],
            }
        c_tok = self.tokens[self.ast_index].value
        raise SyntaxError(
            f"Unexpected token {c_tok} at Line: {self.line}, expected end of program"
        )

    def separator(self):
        """
        Linebreaks etc.
        """

        if self.tokens[self.ast_index].type == "LINEBREAK":
            curr_token = self.check("LINEBREAK")
            self.line += 1
            return {
                "type": curr_token.type,
                "value": curr_token.value,
                "line": self.line - 1,
                "parent": self.ast_index - 1,
                "children": [self.statement()],
            }
        elif self.tokens[self.ast_index].value == "AN":
            curr_token = self.check("AN keyword")
            return {
                "type": curr_token.type,
                "value": curr_token.value,
                "line": self.line,
                "parent": self.ast_index - 1,
                "children": [self.literal()],
            }

        raise SyntaxError(f"Unexpected token {curr_token.value}")

    def statement(self):
        """
        <statement> :
                        <print><statement>|
                        <gimmeh><statement>|
                        <variable declaration><statement>|
                        <assignment statement><statement>|
                        <expr><statement>|
                        <comparison operation><statement>|
                        <if statement><statement>|
                        <switch case statement><statement>|
                        <comment><statement>|
                        <long comment><statement>|
                        <linebreak><statement>|
                        KTHXBYE
        """
        # for error detection
        if self.tokens[self.ast_index].value == "VISIBLE":
            curr_token = self.check("VISIBLE_keyword")
            return {
                "type": curr_token.type,
                "value": curr_token.value,
                "line": self.line,
                "parent": self.ast_index - 1,
                "children": [self.expression()],
            }
        # separators
        elif self.tokens[self.ast_index].type == "LINEBREAK":
            return self.separator()
        elif self.tokens[self.ast_index].value == "AN":
            return self.separator()

        # program start
        elif self.tokens[self.ast_index].value == "HAI":
            return self.program()
        elif self.tokens[self.ast_index].value == "KTHXBYE":
            return self.program_end()

        elif self.tokens[self.ast_index].value == "BTW":
            return self.comment_statement()

        elif self.tokens[self.ast_index].type == "variable declaration":
            return self.variable_declaration()

        c_tok = self.tokens[self.ast_index].value
        raise SyntaxError(
            f"Unexpected token {c_tok} at Line: {self.line}, error token: {self.tokens[self.ast_index].value}"
        )

    def comment_statement(self):
        """
        For statements starting with BTW
        """
        curr_token = self.check("comment keyword")
        return {
            "type": curr_token.type,
            "value": curr_token.value,
            "line": self.line - 1,
            "parent": self.ast_index - 1,
            "children": [self.inline_comment()],
        }

    def inline_comment(self):
        """
        for strings after BTW
        """
        if self.tokens[self.ast_index].value:
            curr_token = self.check("comment_string")
            return {
                "type": curr_token.type,
                "value": curr_token.value,
                "line": self.line - 1,
                "parent": self.ast_index - 1,
                # "children": [self.statement()],
                "children": [self.separator()],
            }
        c_tok = self.tokens[self.ast_index].value
        raise SyntaxError(f"Unexpected token {c_tok} at Line: {self.line}, Linebreak")

    def expression(self):
        """
        Operator + operands + AN + operands
        -> actually this evaluates the operator
        """
        if "literal" in self.tokens[self.ast_index].type:
            return self.literal()
        elif self.tokens[self.ast_index].type == "identifiers":
            return self.identifiers()
        elif self.tokens[self.ast_index].value:
            curr_token = self.check("expression")
            return {
                "type": curr_token.type,
                "value": curr_token.value,
                "line": self.line,
                "parent": self.ast_index - 1,
                "children": [self.assignment_operand()],
            }
        c_tok = self.tokens[self.ast_index].value
        raise SyntaxError(
            f"Unexpected token {c_tok} at Line: {self.line}, expected {self.ast_index}"
        )

    def identifiers(self):
        """
        print operand
        """
        c_tok = self.tokens[self.ast_index].value
        if self.tokens[self.ast_index].type == "identifiers":
            curr_token = self.check("identifiers")
            return {
                "type": curr_token.type,
                "value": curr_token.value,
                "line": self.line,
                "parent": self.ast_index - 1,
                "children": [self.statement()],
            }
        raise SyntaxError(
            f"Unexpected token {c_tok} at Line: {self.line}, expected something else"
        )

    def literal(self):
        """
        <literal> :
                    yarn | numbr | numbar | troof
        """

        if self.tokens[self.ast_index].type == "yarn_literal":
            curr_token = self.check("yarn_literal")
            return {
                "type": curr_token.type,
                "value": curr_token.value,
                "line": self.line,
                "parent": self.ast_index - 1,
                "children": [self.statement()],
            }
        elif self.tokens[self.ast_index].type == "numbr_literal":
            curr_token = self.check("numbr_literal")
            return {
                "type": curr_token.type,
                "value": curr_token.value,
                "line": self.line,
                "parent": self.ast_index - 1,
                "children": [self.statement()],
            }
        elif self.tokens[self.ast_index].type == "numbar_literal":
            curr_token = self.check("numbar_literal")
            return {
                "type": curr_token.type,
                "value": curr_token.value,
                "line": self.line,
                "parent": self.ast_index - 1,
                "children": [self.statement()],
            }
        elif self.tokens[self.ast_index].type == "troof_literal":
            curr_token = self.check("troof_literal")
            return {
                "type": curr_token.type,
                "value": curr_token.value,
                "line": self.line,
                "parent": self.ast_index - 1,
                "children": [self.statement()],
            }
        c_tok = self.tokens[self.ast_index].value
        raise SyntaxError(
            f"Unexpected token {c_tok} at Line: {self.line}, expected another tok"
        )

    def variable_declaration(self):
        """
        <variable declaration> ::= I HAS A varident <linebreak>|
            I HAS A varident <comment> <linebreak>|
            I HAS A varident ITZ <value> <linebreak>|
            I HAS A varident ITZ <value> <comment> <linebreak>|
            I HAS A IT <linebreak>
        """
        c_tok = self.tokens[self.ast_index].value
        if self.tokens[self.ast_index].type == "variable declaration":
            curr_token = self.check("variable declaration")
            return {
                "type": curr_token.type,
                "value": curr_token.value,
                "line": self.line,
                "parent": self.ast_index - 1,
                "children": [self.varident()],
            }
        raise SyntaxError(
            f"Unexpected token {c_tok} at Line: {self.line}, expected variable declaration."
        )

    def varident(self):
        """
        Variable identifier
        """
        c_tok = self.tokens[self.ast_index].value
        # print(self.tokens[self.ast_index - 1].value)
        # print(self.tokens[self.ast_index].type)
        # print(self.tokens[self.ast_index + 1].value)
        if self.tokens[self.ast_index].type == "identifiers":
            curr_token = self.check("identifiers")
            return {
                "type": "variable identifier",
                "value": curr_token.value,
                "parent": self.ast_index - 1,
                "line": self.line,
                "children": [self.assignment()],
            }
        raise SyntaxError(f"Unexpected token {c_tok}, expected variable identifier.")

    def assignment(self):
        """
        ITZ ::= <assignment_operand>
        """
        c_tok = self.tokens[self.ast_index].value
        if self.tokens[self.ast_index].type == "ITZ keyword":
            curr_token = self.check("ITZ keyword")
            return {
                "type": curr_token.type,
                "value": curr_token.value,
                "parent": self.ast_index - 1,
                "line": self.line,
                "children": [self.assignment_operand()],
            }
        # if no ITZ is detected
        # automatically make the last varident as a NOOB
        # init its value to zero
        elif self.tokens[self.ast_index].type in ["LINEBREAK", "AN keyword"]:
            # self.ast[self.ast_index - 1]["assigned"] = 0
            return self.separator()

        raise SyntaxError(f"Unexpected token {c_tok}, expected variable declaration.")

    def assignment_operand(self):
        """
        assignment_operands ::= literal | expression | varident
        """
        c_tok = self.tokens[self.ast_index].value
        if "literal" in self.tokens[self.ast_index].type:
            return self.literal()
        elif self.tokens[self.ast_index].type in self.valid_op_types:
            return self.expression()
        elif self.tokens[self.ast_index].type == "identifiers":
            return self.varident()
        raise SyntaxError(f"Unexpected token {c_tok}, expected variable declaration.")
