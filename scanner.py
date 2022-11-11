'''
    Containts the Scanner/Lexical Analyzer Class for tokenizing a .lol file

    Classes:
        Scanner
        Token
'''
from dataclasses import dataclass
import re
from typing import Any

@dataclass
class Token:
    '''
    A class for representing tokens
    ...
        Attributes:
            type: string
                - contains the type of the Token
            value: any
                - contains the value of the Token
    '''
    type: str
    value: Any = None


@dataclass
class Scanner:
    '''
    A class for representing a lexical analyzer/scanner
    ...
        Attributes:
            code: string
                - contains the contents of a lol program as a string
        Immutable Attributes:
            reserved_words: list
                - list of reserved words
            noise_words: list
                - list of noise words
            keyword: list
                - list of keyword
            operators: list
                - list of operators

    '''
    code: str
    start_prog = r'HAI'
    end_prog = r'KTHXBYE'
    of_keyword = r'^OF$'
    keyword = [
        "BTW",
        "OBTW",
        "TLDR",
        "I",
        "HAS",
        "A",
        "ITZ",
        "SAEM",
        "O",
        "HOW",
        "IZ",
        "I",
        "YR",
    ]
    arith_operators = [
        "R",
        "SUM",
        "DIFF",
        "PRODUKT",
        "QUOSHUNT",
        "MOD",
        "BIGGR",
        "SMALLR",
    ]
    logical = [
        "BOTH",
        "EITHER",
        "WON",
        "ANY",
        "ALL",
        "BOTH",
    ]
    diffrnt_op = r'DIFFRINT'
    not_operator = r'NOT'
    concat = r'SMOOSH'
    typecast = [
        "MAEK",
        "IS NOW A",
    ]
    output = r'VISIBLE'
    input = r'GIMMEH'
    start_cond = r"O RLY\?"
    if_cond = r"YA RLY"
    elif_cond = r"MEBBE"
    else_cond = r"NO WAI"
    end_cond = r"OIC"

    switch = [
        # SWITCH CASE
        r"WTF\?",
        r"OMG",
        r"OMGWTF",
    ]
    loop = [
        "IM IN YR",
        "TIL",
        "WILE",
        "IM OUTTA YR",
    ]
    increment = "UPPIN"
    decrement = "NERFIN"

    separators = [
        "AN",
    ]
    identifiers = r'^[a-zA-Z][a-zA-Z0-9_]*$'
    # variable_ident = r'\b[a-zA-Z][a-zA-Z0-9_]*\b'
    # fxn_ident = r'\b[a-zA-Z][a-zA-Z0-9_]*\b'
    # loop_ident = r'\b[a-zA-Z][a-zA-Z0-9_]*\b'
    numbr_literal = r'\b-?[0-9]+\b'
    numbar_literal = r'\b-?[0-9]*(\.)[0-9]+\b'
    yarn_literal = r'^\"[a-zA-z\d\W]*\"$'
    troof_literal = r'\b(WIN)|(FAIL)\b'
    comment_str = r'.*'

    def create_word_list(self):
        '''
            Creates a word list by iterating through the source code per character
        '''
        word_list = []
        tmp_str = []
        tmp_id = ''
        multiline_comment = False
        # combine these lists
        # compounds = [w for w in self.logical]
        # compounds.extend(self.arith_operators)
        eof = len(self.code) - 1

        for ind, char in enumerate(self.code):
            # scanning characters part of source code
            if tmp_id != "inline_comment" and char == "\n":
                if not tmp_str:
                    continue
                word_list.append(''.join(tmp_str))
                tmp_str = []
            elif ''.join(tmp_str) == "BTW":
                tmp_id = "inline_comment"           # = True
                word_list.append(''.join(tmp_str))
                tmp_str = []
            elif ''.join(tmp_str) == "OBTW":
                multiline_comment = True
                word_list.append(''.join(tmp_str))
                tmp_str = []
            elif multiline_comment:
                tmp_str.append(char)
                if re.match(r'TLDR', ''.join(tmp_str)):
                    word_list.append(''.join(tmp_str))
                    multiline_comment = False
                    tmp_str = []
            # for inline_comment strings after BTW
            elif tmp_id == "inline_comment":
                tmp_str.append(char)
                if char == "\n":
                    word_list.append(''.join(tmp_str[:-1]))
                    tmp_id = ''
                    tmp_str = []
                elif ind == eof:
                    word_list.append(''.join(tmp_str))
                    tmp_id = ''
                    tmp_str = []
            elif not tmp_id and char == '"':
                tmp_id = "yarn"
                tmp_str = [char]
                # tmp_str.append(char)
            elif tmp_id == 'yarn' and char == '"':
                # if 2nd double quote is detected add it to word list and clear yarn flag
                tmp_str.append(char)
                word_list.append("".join(tmp_str))
                tmp_id = ''
                tmp_str = []
            elif tmp_id == 'yarn' and char == " ":
                # make sure that whitespaces inside strings are preserved
                tmp_str.append(char)
            elif char == " ":
                # for non-yarn words; whitespace delimits each lexeme
                # # reset after adding to wordlist
                if tmp_str:
                    word_list.append(''.join(tmp_str))
                tmp_str = []
            # if char is at the last character
            elif ind == len(self.code)-1:
                tmp_str.append(char)
                word_list.append(''.join(tmp_str))
            else:
                # build the yarn by char
                tmp_str.append(char)
        return word_list


    def tokenize(self):
        '''
            Creates a token for every lexeme in the given source code
        '''

        # Token list
        tokens = []

        # Word list
        word_list = self.create_word_list()

        # Word Index; keep track of the indices of the lexemes
        # word_ind = 0

        # Create Tokens from the word list
        for lex in word_list:
            if re.match(self.start_prog, lex):
                tokens.append(Token("program_start", lex))
            elif re.match(self.end_prog, lex):
                tokens.append(Token("program_end", lex))
            elif re.match(self.of_keyword, lex):
                tokens.append(Token("of", lex))
            elif lex in self.loop:
                tokens.append(Token("loop_keyword", lex))
            elif lex in self.keyword:
                tokens.append(Token("keyword", lex))
            # ---------------- LOGIC --------------------------------
            elif lex in self.logical:
                tokens.append(Token("logical_operator", lex))
            elif re.match(self.diffrnt_op, lex):
                tokens.append(Token("comparison_operator", lex))
            elif re.match(self.not_operator, lex):
                tokens.append(Token("comparison_operator", lex))
            # --------------- ARITHMETIC ----------------------------
            elif lex in self.arith_operators:
                tokens.append(Token("arith_operator", lex))
            # --------------- SEPARATORS ----------------------------
            elif lex in self.separators:
                tokens.append(Token("separator", lex))
            # -------------- STRING OPE -----------------------------
            elif re.match(self.concat, lex):
                tokens.append(Token("concat_operator", lex))
            # -------------- INPUT/ OUTPUT --------------------------
            elif re.match(self.input, lex):
                tokens.append(Token("input_keyword", lex))
            elif re.match(self.output, lex):
                tokens.append(Token("output_keyword", lex))
            # ---------------- FLOW CONTROL -------------------------
            elif re.match(self.start_cond, lex):
                tokens.append(Token("if_start", lex))
            elif re.match(self.if_cond, lex):
                tokens.append(Token("if_condition", lex))
            elif re.match(self.elif_cond, lex):
                tokens.append(Token("else_if_cond", lex))
            elif re.match(self.else_cond, lex):
                tokens.append(Token("else_cond", lex))
            elif re.match(self.switch[0], lex):
                tokens.append(Token("switch_start", lex))
            elif re.match(self.switch[1], lex):
                tokens.append(Token("switch_case", lex))
            elif re.match(self.switch[2], lex):
                tokens.append(Token("default_case", lex))
            elif re.match(self.end_cond, lex):
                tokens.append(Token("end_condition", lex))
            # ----------------- LITERALS ----------------------------
            elif re.match(self.numbr_literal, lex):
                tokens.append(Token("numbr_literal", lex))
            elif re.match(self.numbar_literal, lex):
                tokens.append(Token("numbar_literal", lex))
            elif re.match(self.yarn_literal, lex):
                tokens.append(Token("yarn_literal", lex))
            elif re.match(self.troof_literal, lex):
                tokens.append(Token("troof_literal", lex))
            elif re.match(self.identifiers, lex):
                tokens.append(Token("identifiers", lex))
            # ----------------- COMMENT ----------------------------
            elif re.match(self.comment_str, lex):
                tokens.append(Token("comment_string", lex))
            # word_ind += 1

        return tokens
        