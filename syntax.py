import ply.yacc as yacc
from runner import symbol_table
from lexical import tokens
import runner


# Definir precedência dos operadores
precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('nonassoc', 'LESS_THAN', 'GREATER_THAN', 'LESS_THAN_EQUALS', 'GREATER_THAN_EQUALS', 'EQUALS_EQUALS', 'NOT_EQUALS'),
)


# Definir as regras sintáticas
def p_programa_minipar(p):
    '''programa_minipar : bloco_stmt'''
    p[0] = p[1]

def p_bloco_stmt(p):
    '''bloco_stmt : bloco_SEQ
                  | bloco_PAR
                  | bloco_stmt bloco_SEQ
                  | bloco_stmt bloco_PAR'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = (p[1], p[2])

def p_bloco_SEQ(p):
    '''bloco_SEQ : SEQ stmts'''
    p[0] = ('SEQ', p[2])

def p_bloco_PAR(p):
    '''bloco_PAR : PAR stmts'''
    p[0] = ('PAR', p[2])

def p_bloco_IF(p):
    '''bloco_IF : IF LPAREN bool RPAREN LBRACE stmts RBRACE'''
    p[0] = ('IF', p[3], p[6])

def p_bloco_WHILE(p):
    '''bloco_WHILE : WHILE LPAREN bool RPAREN LBRACE stmts RBRACE'''
    p[0] = ('WHILE', p[3], p[6])

def p_bloco_INPUT(p):
    '''bloco_INPUT : INPUT LPAREN RPAREN'''
    p[0] = ('INPUT')

def p_bloco_OUTPUT(p):
    '''bloco_OUTPUT : OUTPUT LPAREN output_args RPAREN'''
    p[0] = ('OUTPUT', p[3])

def p_output_args(p):
    '''output_args : expr
                   | output_args COMMA expr'''
    if len(p) == 2:
        p[0] = (p[1],)
    else:
        p[0] = p[1] + (p[3],)

def p_stmts(p):
    '''stmts : stmt
             | stmts stmt'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_stmt(p):
    '''stmt : atribuicao
            | bloco_IF
            | bloco_WHILE
            | bloco_INPUT
            | bloco_OUTPUT
            | c_channel
            | c_channel_stmt'''
    p[0] = p[1]

def p_atribuicao(p):
    '''atribuicao : ID EQUALS expr
                  | ID EQUALS STRING
                  | ID EQUALS bloco_INPUT
                  | ID EQUALS receive_stmt'''
                  
    p[0] = ('=', p[1], p[3])
    if p[1] not in symbol_table: 
        symbol_table[p[1]] = p[3]

def p_expr(p):
    '''expr : INT
            | STRING
            | expr PLUS expr
            | expr MINUS expr
            | expr TIMES expr
            | expr DIVIDE expr
            | expr LESS_THAN expr
            | expr GREATER_THAN expr
            | expr LESS_THAN_EQUALS expr
            | expr GREATER_THAN_EQUALS expr
            | expr EQUALS_EQUALS expr
            | expr NOT_EQUALS expr
            '''
 
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = (p[2], p[1], p[3])

def p_expr_id(p):
    '''expr : ID'''
    if p[1] not in symbol_table:
        print(f"Erro semântico: identificador '{p[1]}' não declarado")
        runner.has_error = True
    p[0] = p[1]

def p_bool(p):
    '''bool : expr'''
    p[0] = p[1]

def p_comment(p):
    '''comment : COMMENT'''
    pass  # Comentários são ignorados, então não fazemos nada

def p_c_channel(p):
    '''c_channel : C_CHANNEL ID LPAREN STRING COMMA STRING RPAREN'''
    p[0] = ('C_CHANNEL', p[2], p[4], p[6])

    runner.channels[p[2]] = (p[4],p[6])

def p_c_channel_stmt(p):
    '''c_channel_stmt : send_stmt
                      | receive_stmt''' 
    p[0] = p[1]

def p_send_stmt(p):
    '''send_stmt : ID DOT SEND LPAREN ID COMMA expr COMMA expr COMMA expr RPAREN
                 | ID DOT SEND LPAREN ID RPAREN'''
    if len(p) == 7:
            p[0] = (p[1], 'SEND', p[5])
    elif len(p) == 13:
        p[0] = (p[1], 'SEND', p[5], p[7], p[9], p[11])
    
    if p[1] not in runner.channels:
        print(f"Erro semântico: identificador '{p[1]}' em '{p[1]}.{p[3]}()' não declarado")
        runner.has_error = True

def p_receive_stmt(p):
    '''receive_stmt : ID DOT RECEIVE LPAREN ID COMMA expr COMMA expr COMMA expr RPAREN
                    | ID DOT RECEIVE LPAREN ID RPAREN'''
    if len(p) == 7:
            p[0] = (p[1], 'RECEIVE', p[5])
    elif len(p) == 13:
        p[0] = (p[1], 'RECEIVE', p[5], p[7], p[9], p[11])
    
    if p[1] not in runner.channels:
        print(f"Erro semântico: identificador '{p[1]}' em '{p[1]}.{p[3]}()' não declarado")
        runner.has_error = True

def p_error(p):
    runner.has_error = True
    if p:
        print(f"Erro sintático: token inesperado '{p.value}' na linha {p.lineno}.")
        print(f"Contexto: próximo aos tokens {p.lexer.lexdata[max(0, p.lexpos-20):p.lexpos+20]}") # teste
        # Trata o erro e recupera a análise
    else:
        print("Erro sintático: fim de arquivo inesperado.")
    parser.errok()
    
# Criar o analisador sintático
parser = yacc.yacc()