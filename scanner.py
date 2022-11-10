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
    reserved_words = [
        "HAI",
        "KTHXBYE",
    ]
    noise_words = [
        "OF",
    ]
    keyword = [
        "VISIBLE",
        "BTW",
        "OBTW",
        "I",
        "HAS",
        "A",
        "ITZ",

    ]
    operators = [
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
        "NOT",
        "ANY",
        "ALL",
        "BOTH SAEM",
        "DIFFRINT",
    ]
    concat = r'SMOOSH'
    typecast = [
        "MAEK",
        "IS NOW A",
        "A"
    ]
    input = r'GIMMEH'
    conditional = [
        "O RLY?",
        "YA_RLY",                                             # IF
        "MEBBE",                                              # ELSE IF
        "NO WAI",                                             # ELSE
        "OIC"
    ]
    switch = [
        # SWITCH CASE
        "WTF?",
        "OMG",
        "OMGWTF",
    ]
    loop = [
        "IM IN YR",
        "YR",
        "TIL",
        "WILE",
        "IM_OUTTA_YR",
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
        inline_comment = False
        multiline_comment = False

        for char in self.code:
            if not inline_comment and char == "\n":
                if not tmp_str:
                    continue
                word_list.append(''.join(tmp_str))
                tmp_str = []
            elif ''.join(tmp_str) in {"BTW", "OBTW"}:
                print("detected comment")
                if ''.join(tmp_str) == "BTW":
                    inline_comment = True
                else:
                    multiline_comment = True
                word_list.append(''.join(tmp_str))
                tmp_str = []
            elif inline_comment:
                tmp_str.append(char)
                if char == "\n":
                    word_list.append(''.join(tmp_str[:-1]))
                    inline_comment = False
                    tmp_str = []
            elif not tmp_id and char == '"':
                tmp_id = "yarn"
                tmp_str = [char]
                # tmp_str.append(char)
            elif tmp_id == 'yarn' and char == '"':
                tmp_str.append(char)
                word_list.append("".join(tmp_str))
                tmp_id = ''
                tmp_str = []
            elif tmp_id == 'yarn' and char == " ":
                # make sure that whitespaces inside strings are preserved
                tmp_str.append(char)
            elif char == " ":
                # for non-yarn words; whitespace delimits each lexeme
                # word_list.append("".join(tmp_str))
                # # reset after adding to wordlist
                if tmp_str:
                    word_list.append(''.join(tmp_str))
                tmp_str = []
            else:
                # build the yarn by char
                tmp_str.append(char)
                if ''.join(tmp_str) == "KTHXBYE":
                    word_list.append(''.join(tmp_str))
                # elif ''.join(tmp_str) == "BTW" or ''.join(tmp_str) == "OBTW":
                #     word_list.append(''.join(tmp_str))
                # print(tmp_str)
        print(word_list)
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
            if lex in self.reserved_words:
                tokens.append(Token("reserved_word", lex))
            elif lex in self.noise_words:
                tokens.append(Token("reserved_noise_word", lex))
            elif lex in self.keyword:
                tokens.append(Token("keyword", lex))
            elif lex in self.operators:
                tokens.append(Token("operator", lex))
            elif lex in self.separators:
                tokens.append(Token("separator", lex))
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
            elif re.match(self.comment_str, lex):
                tokens.append(Token("comment_string", lex))
            # word_ind += 1

        return tokens
        