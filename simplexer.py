# _*_coding:utf-8_*_

import os
import argparse
import pickle
import ply.lex as lex

DATA_FILE = "data.dat"

tokens = [
    'NUMBER',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'EQUAL',
    'PERCENT',
    'ID',
    'LPAREN',
    'RPAREN',
    'LBRACK',
    'RBRACK',
    'LBRACE',
    'RBRACE',
    'COMMA',
    'DOT',
    'IN_EDGE',
    'IN_EDGE_SUB',
    'OUT_EDGE',
    'OUT_EDGE_SUB',
    'FARROW',
    'DQSTRING',
    'SQSTRING',
    'COLON',
    'DOCSTRING',
    "NEWLINE",
]

REPLACED_TOKEN = (
        'ID',
        'DQSTRING',
        'SQSTRING',
        'NEWLINE',
)

t_NUMBER       = r'\d'
t_PLUS         = r'\+'
t_MINUS        = r'-'
t_TIMES        = r'\*'
t_DIVIDE       = r'/'
t_EQUAL        = r'='
t_PERCENT      = r'%'
t_LPAREN       = r'\('
t_RPAREN       = r'\)'
t_LBRACK       = r'\['
t_RBRACK       = r'\]'
t_LBRACE       = r'{'
t_RBRACE       = r'}'
t_COMMA        = r','
t_DOT          = r'\.'
t_IN_EDGE      = r'->'
t_IN_EDGE_SUB  = r'~>'
t_OUT_EDGE     = r'<-'
t_OUT_EDGE_SUB = r'<~'
t_FARROW       = r'=>'
t_DQSTRING     = r'[ubr]*"[^"]+"'
t_SQSTRING     = r"[ubr]*'[^']+'"
t_COLON        = r":"



# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    t.type = "NEWLINE"
    t.value = "\n"
    return t

# A string containing ignored characters (spaces and tabs)
t_ignore = ' \t'


# Ignore Comment
def t_COMMENT(t):
    r'\#.*'
    pass

def t_DOCSTRING(t):
    r'"{3}\n?[.\n]+"{3}'
    pass

# Error handling rule
def t_error(t):
    # print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


reserved = {}

for kw in __import__("keyword").kwlist:
    reserved[kw] = kw.upper()

tokens = tokens + list(reserved.values())


# 識別子IDに対して、予約語をチェックする処理を追加
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')
    return t


def getArgs():
    parser = argparse.ArgumentParser(description="")

    # デバック用にファイル一つを指定できるものを用意
    parser.add_argument(
        "-f", "--input",
        dest="input_file",
        type=argparse.FileType("r"),
        help="input filename as train data"
    )

    # 複数のプログラムが用意されたフォルダを指定すると全てのファイルを読み込む
    parser.add_argument(
        "-s", "--source",
        default=None,
        type=str,
        dest="source"
    )

    return parser.parse_args()

def find_all_files(directory):
    for root, dirs, files in os.walk(directory):
        yield root
        for file in files:
            yield os.path.join(root, file)


if __name__ == "__main__":
    args = getArgs()

    lexer = lex.lex()

    if args.source is None:
        program_path_list = [args.input_file,]
        # デバック用なのでcodebooksも初期化
        codebooks = []
    else:
        program_path_list = find_all_files(args.source)
        program_path_list = filter(lambda p: os.path.splitext(p)[1] == ".py",
                                       program_path_list)
        try:
            with open(DATA_FILE, "rb") as d:
                codebooks = pickle.load(d)
        except EOFError:
            codebooks = []

    for program_path in program_path_list:
        codebook = []
        with open(program_path, "r") as f:
            for l in f.readlines():
                lexer.input(l)

                while True:
                    tok = lexer.token()
                    if not tok:
                        break
                    # print(tok.type + "\t" + tok.value)
                    if tok.type in REPLACED_TOKEN:
                        if tok.type == "NEWLINE":
                            if len(codebook) != 0 and codebook[-1] != "NEWLINE":
                                codebook.append(tok.type)
                            else:
                                pass # 連続改行は無視
                        else:
                            codebook.append(tok.type)
                    else:
                        codebook.append(tok.value)
        codebooks.append(codebook)
    if args.source is None:
        print codebooks
    else:
        with open(DATA_FILE, "wb") as d:
            pickle.dump(codebooks, d)
