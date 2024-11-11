import ply.lex as lex
import runner

# Lista de tokens
tokens = [
    'SEQ', 'PAR', 'IF', 'ELSE', 'WHILE',
    'INPUT', 'OUTPUT',
    'SEND', 'RECEIVE',
    'ID', 'INT', 'STRING',
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE',
    'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE',
    'COMMA', 'EQUALS', 'LESS_THAN', 'GREATER_THAN', 
    'LESS_THAN_EQUALS', 'GREATER_THAN_EQUALS', 
    'EQUALS_EQUALS', 'NOT_EQUALS', 'COMMENT', 'C_CHANNEL', 'DOT'
]

# Expressões Regulares para os tokens
t_SEQ = r'SEQ'
t_PAR = r'PAR'
t_IF = r'if'
t_ELSE = r'else'
t_WHILE = r'while'
t_INPUT = r'Input'
t_OUTPUT = r'Output'
t_SEND = r'send'
t_RECEIVE = r'receive'
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_COMMA = r','
t_EQUALS = r'='
t_LESS_THAN = r'<'
t_GREATER_THAN = r'>'
t_LESS_THAN_EQUALS = r'<='
t_GREATER_THAN_EQUALS = r'>='
t_EQUALS_EQUALS = r'=='
t_NOT_EQUALS = r'!='
t_C_CHANNEL = r'c_channel'
t_DOT = r'\.'


# Ignorar espaços em branco e tabulações
t_ignore = ' \t\n\r'

# Definir regras para tokens complexos
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    reserved = {
        'SEQ', 'PAR', 'if', 'else', 'while', 
        'Input', 'Output',
        'send', 'receive', 'c_channel'
    }
 #   print("t-value: ", t.value)
    if t.value in reserved:
        t.type = t.value.upper()
    return t

def t_INT(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_STRING(t):
    #r'"[^"\n]*"' 
    r'"[^"\n]*"|\'[^\'\n]*\''
    t.value = t.value[1:-1]  # Remove as aspas
    return t

# Tratar caracteres ilegais
def t_error(t):
    runner.has_error = True
    print(f"Caractere ilegal '{t.value[0]}' na linha {t.lineno}")
    t.lexer.skip(1)

def t_COMMENT(t):
    r'\#.*\n?'
    pass  # Comentários são ignorados, então não fazemos nada


# Criar o analisador léxico
lexer = lex.lex()