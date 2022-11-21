"""
    Contains the Parser Class to analyze the syntax of the tokenized program

    Classes:
        Parser
"""
import sys
from typing import List, Dict
from dataclasses import dataclass

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

    def check(self, token_type: str):
        """
        Check the type of the given token
        """
        valid_op_types = [
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
        next_token = self.next_t

        if next_token is None:
            raise SyntaxError(
                f"Unexpected end of program at Line: {self.line}, expected {token_type}"
            )
        if token_type == "expression" and next_token.type not in valid_op_types:
            print(f"next_token---type: {next_token.type}")
            raise SyntaxError(
                f"Invalid Operator: {next_token.value} at Line: {self.line}, expected expression operator"
            )
        elif token_type != "expression" and next_token.type != token_type:
            raise SyntaxError(
                f"Unexpected token: {next_token.value} at Line: {self.line}, expected {token_type}"
            )
            # print(f"Unexpected token: {next_token.value}, expected {token_type}")

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
        return self.ast_index > len(self.tokens) - 1

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

        <program>: HAI <statement>
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

        raise SyntaxError(f"Unexpected program start {c_tok}, expected HAI")

    # def separator(self):
    #     """
    #     Linebreaks etc.
    #     """

    #     if self.tokens[self.ast_index].type == "LINEBREAK":
    #         curr_token = self.check("LINEBREAK")
    #         self.line += 1
    #         return {
    #             "type": curr_token.type,
    #             "value": curr_token.value,
    #             "line": self.line - 1,
    #             "parent": self.ast_index - 1,
    #             "children": [self.statement()],
    #         }

    #     raise SyntaxError(f"Unexpected token {curr_token.value}")

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
        # TODO: SEPARATE TO SEPARATOR fn
        elif self.tokens[self.ast_index].type == "LINEBREAK":
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
            self.line += 1
            return {
                "type": curr_token.type,
                "value": curr_token.value,
                "line": self.line - 1,
                "parent": self.ast_index - 1,
                "children": [self.literal()],
            }
        elif self.tokens[self.ast_index].value == "BTW":
            curr_token = self.check("comment keyword")
            self.line += 1
            return {
                "type": curr_token.type,
                "value": curr_token.value,
                "line": self.line - 1,
                "parent": self.ast_index - 1,
                "children": [self.inline_comment()],
            }
        elif self.tokens[self.ast_index].value == "KTHXBYE":
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
            f"Unexpected token {c_tok} at Line: {self.line}, expected something else"
        )

    def inline_comment(self):
        """
        for strings after BTW
        """
        if self.tokens[self.ast_index].value:
            curr_token = self.check("comment_string")
            self.line += 1
            return {
                "type": curr_token.type,
                "value": curr_token.value,
                "line": self.line - 1,
                "parent": self.ast_index - 1,
                # TODO: replace with LINEBREAK separator
                "children": [self.statement()],
            }
        c_tok = self.tokens[self.ast_index].value
        raise SyntaxError(
            f"Unexpected token {c_tok} at Line: {self.line}, expected something else"
        )

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
                "children": [self.literal()],
            }
        c_tok = self.tokens[self.ast_index].value
        raise SyntaxError(
            f"Unexpected token {c_tok} at Line: {self.line}, expected something else"
        )

    def identifiers(self):
        """
        print operand
        """
        if self.tokens[self.ast_index].type == "identifiers":
            curr_token = self.check("identifiers")
            return {
                "type": curr_token.type,
                "value": curr_token.value,
                "line": self.line,
                "parent": self.ast_index - 1,
                "children": [self.statement()],
            }
        c_tok = self.tokens[self.ast_index].value
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
        else:
            c_tok = self.tokens[self.ast_index].value
            raise SyntaxError(
                f"Unexpected token {c_tok} at Line: {self.line}, expected something else"
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
        if self.tokens[self.ast_index].type == "variable_declaration":
            curr_token = self.check("variable_declaration")
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
        if self.tokens[self.ast_index].type == "identifier":
            curr_token = self.check("identifier")
            return {
                "type": "variable identifier",
                "value": curr_token.value,
                "parent": self.ast_index - 1,
                "children": [self.assignment()],
            }
        raise SyntaxError(f"Unexpected token {c_tok}, expected variable declaration.")

    def assignment(self):
        """
        ITZ ::= literal
        """
        c_tok = self.tokens[self.ast_index].value
        if self.tokens[self.ast_index].type == "ITZ keyword":
            curr_token = self.check("ITZ keyword")
            return {
                "type": curr_token.type,
                "value": curr_token.value,
                "parent": self.ast_index - 1,
                "children": [self.literal()],
            }

        raise SyntaxError(f"Unexpected token {c_tok}, expected variable declaration.")
