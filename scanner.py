"""
    Containts the Scanner/Lexical Analyzer Class for tokenizing a .lol file

    Classes:
        Scanner
        Token
"""
from dataclasses import dataclass
import re
from typing import Any


@dataclass
class Token:
    """
    A class for representing tokens
    ...
        Attributes:
            type: string
                - contains the type of the Token
            value: any
                - contains the value of the Token
    """

    type: str
    value: Any = None


@dataclass
class Scanner:
    """
    A class for representing a lexical analyzer/scanner
    ...
        Attributes:
            code: string
                - contains the contents of a lol program as a string
            tokens: list
                - stores the list of tokens from a given program
                - pass empty on init
        Immutable Attributes:
            keywords

    """

    code: str
    tokens: list
    HAI_keyword = r"^HAI$"
    KTHXBYE_keyword = r"^KTHXBYE$"
    # var declare
    IHASA_keyword = r"^I HAS A$"
    # fun_declaration
    HOWIZI_keyword = r"^HOW IZ I$"
    IFUSAYSO_keyword = r"^IF U SAY SO$"

    BTW_keyword = r"^BTW$"
    OBTW_keyword = r"^OBTW$"
    TLDR_keyword = r"^TLDR$"

    ITZ_keyword = r"^ITZ$"

    # ARITHMETIC ------------
    R_keyword = r"^R$"
    SUM_OF_keyword = r"^SUM OF$"
    DIFF_OF_keyword = r"^DIFF OF$"
    PRODUKT_OF_keyword = r"^PRODUKT OF$"
    QUOSHUNT_OF_keyword = r"^QUOSHUNT OF$"
    MOD_OF_keyword = r"^MOD OF$"
    BGGR_OF_keyword = r"^BIGGR OF$"
    SMALLR_OF_keyword = r"^SMALLR OF$"

    # LOGIC ----------
    BOTH_SAEM_keyword = r"^BOTH SAEM$"
    BOTH_OF = r"^BOTH OF$"
    EITHER_OF = r"^EITHER OF$"
    WON_OF = r"^WON OF$"
    ANY_OF = "^ANY OF$"
    ALL_OF = "^ALL OF$"

    DIFFRINT_operator = r"^DIFFRINT$"
    NOT_operator = r"^NOT$"
    SMOOSH_operator = r"^SMOOSH$"

    MAEK_keyword = r"^MAEK$"
    IS_NOW_A_keyword = r"^IS NOW A$"

    VISIBLE_keyword = r"VISIBLE$"
    GIMMEH_keyword = r"GIMMEH$"

    ORLY_keyword = r"^O RLY\?$"
    YA_RLY_keyword = r"^YA RLY$"
    MEBBE_keyword = r"^MEBBE$"
    NO_WAI_keyword = r"^NO WAI$"
    OIC_keyword = r"^OIC$"

    WTF_keyword = r"WTF\?"
    OMG_keyword = r"OMG"
    OMGWTF_keyword = r"OMGWTF"

    IM_IN_YR_keyword = r"IM IN YR"
    TIL_keyword = r"TIL"
    WILE_keyword = r"WILE"
    IM_OUTTA_YR_keyword = r"^IM OUTTA YR$"

    UPPIN_keyword = r"^UPPIN$"
    NERFIN_keyword = r"^NERFIN$"

    AN_keyword = r"^AN$"
    LINEBREAK = r"[\\]n$"
    identifiers = r"^[a-zA-Z][a-zA-Z0-9_]*$"
    # variable_ident = r'\b[a-zA-Z][a-zA-Z0-9_]*\b'
    # fxn_ident = r'\b[a-zA-Z][a-zA-Z0-9_]*\b'
    # loop_ident = r'\b[a-zA-Z][a-zA-Z0-9_]*\b'
    # recheck
    numbr_literal = r"^-?[0-9]+$"
    numbar_literal = r"^-?[0-9]*(\.)[0-9]+\b$"
    yarn_literal = r"^\"[a-zA-z\d\W]*\"$"
    troof_literal = r"\b(WIN)|(FAIL)\b"
    comment_str = r".*"
    # invalid_str =

    def create_word_list(self):
        """
        Creates a word list by iterating through the source code per character
        """
        word_list = []
        tmp_str = []
        tmp_id = ""
        multiline_comment = False
        eof = len(self.code) - 1

        for ind, char in enumerate(self.code):
            # scanning characters part of source code
            if tmp_id != "inline_comment" and char == "\n":
                if not tmp_str:
                    word_list.append(r"\n")
                    continue
                word_list.extend(("".join(tmp_str), r"\n"))
                tmp_str = []
            elif "".join(tmp_str) == "BTW":
                tmp_id = "inline_comment"  # = True
                word_list.append("".join(tmp_str))
                tmp_str = []
            elif "".join(tmp_str) == "OBTW":
                multiline_comment = True
                word_list.append("".join(tmp_str))
                tmp_str = []
            elif multiline_comment:
                tmp_str.append(char)
                if re.match(r"TLDR", "".join(tmp_str)):
                    word_list.append("".join(tmp_str))
                    multiline_comment = False
                    tmp_str = []
            # for inline_comment strings after BTW
            elif tmp_id == "inline_comment":
                tmp_str.append(char)
                if char == "\n":
                    word_list.extend(("".join(tmp_str[:-1]), r"\n"))
                    tmp_id = ""
                    tmp_str = []
                elif ind == eof:
                    word_list.append("".join(tmp_str))
                    tmp_id = ""
                    tmp_str = []
            # YARN LITERALS
            elif not tmp_id and char == '"':
                tmp_id = "yarn"
                tmp_str = [char]
            elif tmp_id == "yarn" and char == '"':
                # if 2nd double quote is detected add it to word list and clear yarn flag
                tmp_str.append(char)
                word_list.append("".join(tmp_str))
                tmp_id = ""
                tmp_str = []
            elif tmp_id == "yarn" and char == " ":
                # make sure that whitespaces inside strings are preserved
                tmp_str.append(char)
            elif char == " ":
                # for non-yarn words; whitespace delimits each lexeme
                # # reset after adding to wordlist
                if tmp_str:
                    word_list.append("".join(tmp_str))
                tmp_str = []
            # if char is at the last character
            elif ind == len(self.code) - 1:
                tmp_str.append(char)
                word_list.append("".join(tmp_str))
            else:
                # build the yarn by char
                tmp_str.append(char)
        return word_list

    def compound(self, word_list: list):
        """
        Clean word list before tokenizing
        """
        ind = 0
        cpy = word_list[:]
        size = len(cpy)

        ops = ["SUM", "DIFF", "PRODUKT", "QUOSHUNT", "MOD", "BIGGR", "SMALLR"]

        while ind < size:
            # I HAS A
            if re.match(r"^I$", cpy[ind]):
                cpy[ind] = f"{cpy[ind]} {cpy[ind+1]} {cpy[ind+2]}"
                del cpy[ind + 1]
                del cpy[ind + 1]
                size = len(cpy)
            elif cpy[ind] in ops:
                cpy[ind] = f"{cpy[ind]} {cpy[ind+1]}"
                del cpy[ind + 1]
                size = len(cpy)
            ind += 1
        # print(cpy)

        return cpy

    def tokenize(self):
        """
        Creates a token for every lexeme in the given source code
        """

        # Token list
        tokens = []

        # Word list
        word_list = self.compound(self.create_word_list())
        comment_flag = False

        # Word Index; keep track of the indices of the lexemes
        # word_ind = 0

        # Create Tokens from the word list
        for lex in word_list:
            if re.match(self.HAI_keyword, lex):
                tokens.append(Token("HAI_keyword", lex))
            elif re.match(self.KTHXBYE_keyword, lex):
                tokens.append(Token("KTHXBYE_keyword", lex))

            #  ------------------ loop -----------------------------
            elif re.match(self.IM_IN_YR_keyword, lex):
                tokens.append(Token("loop declaration", lex))
            elif re.match(self.TIL_keyword, lex):
                tokens.append(Token("loop keyword", lex))
            elif re.match(self.WILE_keyword, lex):
                tokens.append(Token("loop keyword", lex))
            elif re.match(self.IM_OUTTA_YR_keyword, lex):
                tokens.append(Token("end loop", lex))

            # elif lex in self.keyword:
            #     tokens.append(Token("keyword", lex))

            elif re.match(self.IHASA_keyword, lex):
                tokens.append(Token("variable declaration", lex))
            elif re.match(self.HOWIZI_keyword, lex):
                tokens.append(Token("function declaration", lex))
            elif re.match(self.IFUSAYSO_keyword, lex):
                tokens.append(Token("function end", lex))
            elif re.match(self.ITZ_keyword, lex):
                tokens.append(Token("ITZ keyword", lex))

            elif re.match(self.BTW_keyword, lex):
                tokens.append(Token("comment keyword", lex))
                comment_flag = True
            elif re.match(self.OBTW_keyword, lex):
                tokens.append(Token("multiline comment start", lex))
                comment_flag = True
            elif re.match(self.TLDR_keyword, lex):
                tokens.append(Token("multiline comment end", lex))
                comment_flag = False

            # TYPECASTING
            elif re.match(self.MAEK_keyword, lex):
                tokens.append(Token("MAEK keyword", lex))
            elif re.match(self.IS_NOW_A_keyword, lex):
                tokens.append(Token("IS NOW A keyword", lex))

            # ---------------- LOGIC --------------------------------
            elif re.match(self.BOTH_SAEM_keyword, lex):
                tokens.append(Token("BOTH_SAEM keyword", lex))
            elif re.match(self.BOTH_OF, lex):
                tokens.append(Token("BOTH_OF keyword", lex))
            elif re.match(self.EITHER_OF, lex):
                tokens.append(Token("EITHER_OF keyword", lex))
            elif re.match(self.WON_OF, lex):
                tokens.append(Token("WON_OF keyword", lex))
            elif re.match(self.ANY_OF, lex):
                tokens.append(Token("ANY_OF keyword", lex))
            elif re.match(self.ALL_OF, lex):
                tokens.append(Token("ALL_OF keyword", lex))
            elif re.match(self.DIFFRINT_operator, lex):
                tokens.append(Token("comparison_operator", lex))
            elif re.match(self.NOT_operator, lex):
                tokens.append(Token("comparison_operator", lex))
            # --------------- ARITHMETIC ----------------------------
            elif re.match(self.R_keyword, lex):
                tokens.append(Token("R keyword", lex))
            elif re.match(self.SUM_OF_keyword, lex):
                tokens.append(Token("SUM_OF keyword", lex))
            elif re.match(self.DIFF_OF_keyword, lex):
                tokens.append(Token("DIFF_OF keyword", lex))
            elif re.match(self.PRODUKT_OF_keyword, lex):
                tokens.append(Token("PRODUKT_OF keyword", lex))
            elif re.match(self.QUOSHUNT_OF_keyword, lex):
                tokens.append(Token("QUOSHUNT_OF keyword", lex))
            elif re.match(self.MOD_OF_keyword, lex):
                tokens.append(Token("MOD_OF keyword", lex))
            elif re.match(self.BGGR_OF_keyword, lex):
                tokens.append(Token("BGGR_OF keyword", lex))
            elif re.match(self.SMALLR_OF_keyword, lex):
                tokens.append(Token("SMALLR_OF keyword", lex))
            elif re.match(self.UPPIN_keyword, lex):
                tokens.append(Token("UPPIN keyword", lex))
            elif re.match(self.NERFIN_keyword, lex):
                tokens.append(Token("NERFIN keyword", lex))

            # --------------- SEPARATORS ----------------------------
            elif re.match(self.AN_keyword, lex):
                tokens.append(Token("AN keyword", lex))
            elif re.match(self.LINEBREAK, lex):
                tokens.append(Token("LINEBREAK", lex))
                if comment_flag:
                    comment_flag = False
            # -------------- STRING OPE -----------------------------
            elif re.match(self.SMOOSH_operator, lex):
                tokens.append(Token("concat_operator", lex))
            # -------------- INPUT/ OUTPUT --------------------------
            elif re.match(self.GIMMEH_keyword, lex):
                tokens.append(Token("input_keyword", lex))
            elif re.match(self.VISIBLE_keyword, lex):
                tokens.append(Token("VISIBLE_keyword", lex))
            # ---------------- FLOW CONTROL -------------------------
            elif re.match(self.ORLY_keyword, lex):
                tokens.append(Token("if_start", lex))
            elif re.match(self.YA_RLY_keyword, lex):
                tokens.append(Token("if_condition", lex))
            elif re.match(self.MEBBE_keyword, lex):
                tokens.append(Token("else_if_cond", lex))
            elif re.match(self.NO_WAI_keyword, lex):
                tokens.append(Token("else_cond", lex))
                # -------- SWITCH -------------------
            elif re.match(self.WTF_keyword, lex):
                tokens.append(Token("switch_start", lex))
            elif re.match(self.OMG_keyword, lex):
                tokens.append(Token("switch_case", lex))
            elif re.match(self.OMGWTF_keyword, lex):
                tokens.append(Token("default_case", lex))

            elif re.match(self.OIC_keyword, lex):
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
            elif not comment_flag and re.match(self.identifiers, lex):
                tokens.append(Token("identifiers", lex))
            # ----------------- COMMENT ----------------------------
            elif comment_flag and re.match(self.comment_str, lex):
                tokens.append(Token("comment_string", lex))
            else:
                raise SyntaxError(f"Invalid Character: {lex}")
            # word_ind += 1

        self.tokens = tokens
        return tokens


# test
# if __name__ == "__main__":
#     TEST_PATH = "inputs/test.lol"
#     code_contents = ""

#     with open(TEST_PATH, "r", encoding="utf-8") as lol_file:
#         code_contents = lol_file.read()

#     # Instantiate the Lexical Analyzer
#     lexi = Scanner(code_contents)
#     w_list = lexi.tokenize()

#     print(w_list)
