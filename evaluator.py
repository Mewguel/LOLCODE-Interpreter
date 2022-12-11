"""
    Contains the Parser Class to analyze the syntax of the tokenized program

    Classes:
        Evaluator
"""
from typing import Dict
from dataclasses import dataclass, field


OPS = [
    "R keyword",
    "SUM_OF keyword",
    "DIFF_OF keyword",
    "PRODUKT_OF keyword",
    "QUOSHUNT_OF keyword",
    "MOD_OF keyword",
    # "BGGR_OF keyword",
    # "SMALLR_OF keyword",
    # "UPPIN keyword",
    # "NERFIN keyword",
]


@dataclass
class Evaluator:
    """
    A class for the semantic actions of the generated AST
    ...
        Attributes:
            ast: Dict
                - abstract syntax tree for the grammar checking
            var_table: Dict
    """

    ast: Dict
    var_table: Dict = field(default_factory=lambda: {})

    def evaluate(self):
        """
        Run through the AST
        """
        temp = self.ast
        while temp is not None:
            if temp["type"] == "VISIBLE_keyword":
                temp = self.visible(temp)
            elif temp["type"] == "variable declaration":
                temp = self.var_declare(temp)
            temp = temp["children"][0]

    def visible(self, node):
        """
        Print function
        """
        arguments = []
        # collect all arguments of Print
        while node is not None:
            if node["type"] == "yarn_literal":
                arguments.append(node["value"][1:-1])
            elif node["type"] in [
                "numbr_literal",
                "numbar_literal",
                "troof_literal",
            ]:
                arguments.append(node["value"])
            elif node["type"] in OPS:
                result = self.arithmetic(node)
                node = result[1]
                arguments.append(result[0])
                break
            elif node["type"] == "identifiers":
                for var_ident in self.var_table.keys():
                    if node["value"] == var_ident:
                        arguments.append(self.var_table[var_ident])
                        node = node["children"][0]
                        break

            node = node["children"][0]
            if node["type"] in ["LINEBREAK", "comment keyword"]:
                break

        for a in arguments:
            # print(f"{a}", end="")
            print(f"{a}")
        return node

    def arithmetic(self, node):
        """
        Perform math operations
        """
        # get base operation
        op = ""
        operand_1 = ""
        operand_2 = ""
        an_key = False

        if node["type"] in OPS:
            op = node["value"]
            node = node["children"][0]

        if node["type"] == "numbr_literal" and not operand_1:
            # get first operand
            operand_1 = int(node["value"])
            node = node["children"][0]
        elif node["type"] == "numbar_literal" and not operand_1:
            # get first operand
            operand_1 = float(node["value"])
            node = node["children"][0]
        # nested arithmetic expression
        elif node["type"] in OPS:
            res = self.arithmetic(node)
            node = res[1]
            operand_1 = res[0]
        elif node["type"] == "identifiers":
            operand_1 = self.var_table[node["value"]]
            node = node["children"][0]

        if node["type"] == "AN keyword":
            node = node["children"][0]
            an_key = True

        if an_key and node["type"] == "numbr_literal":
            # get 2nd
            operand_2 = int(node["value"])
            node = node["children"][0]
        elif an_key and node["type"] == "numbar_literal":
            # get 2nd
            operand_2 = float(node["value"])
            node = node["children"][0]
        elif node["type"] in OPS:
            res = self.arithmetic(node)
            node = res[1]
            operand_2 = res[0]
        elif node["type"] == "identifiers":
            operand_2 = self.var_table[node["value"]]
            node = node["children"][0]

        # base cases
        if operand_1 and operand_2:
            if op == "SUM OF":
                return (operand_1 + operand_2, node)
            elif op == "DIFF OF":
                return (operand_1 - operand_2, node)
            elif op == "PRODUKT OF":
                return (operand_1 * operand_2, node)
            elif op == "QUOSHUNT OF":
                if isinstance(operand_1, float) or isinstance(operand_2, float):
                    return (operand_1 / operand_2, node)
                return (operand_1 // operand_2, node)

    def var_declare(self, node):
        """
        I HAS A semantics
        """
        # get the variable name
        var_key = ""
        var_val = ""
        assign = False

        node = node["children"][0]
        if node["type"] == "identifiers":
            var_key = str(node["value"])
            node = node["children"][0]

        if node["type"] == "ITZ keyword":
            assign = True
            node = node["children"][0]

        if assign:
            if node["type"] == "yarn_literal":
                var_val = node["value"]
            elif node["type"] == "numbr_literal":
                var_val = int(node["value"])
            elif node["type"] == "numbar_literal":
                var_val = float(node["value"])
            elif node["type"] == "troof_literal":
                # Assign true of troof is WIN
                var_val = node["value"]
            # assign result of arithmetic operations
            elif node["type"] in [
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
            ]:
                res = self.arithmetic(node)
                # if res is not None:
                #     # print(res[0])
                #     self.var_table[var_key] = res[0]
                # print(self.var_table)
                # NEEDS FIXING

            node = node["children"][0]

        self.var_table[var_key] = var_val

        # if var key and no var val: var key is a noob
        # if var_key and not var_val:
        #     var_val = 0
        return node
