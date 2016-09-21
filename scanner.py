# -----------------------------------------------------------------------------
# calc.py
#
# A simple calculator with variables.
# -----------------------------------------------------------------------------

tokens = (
    'INICIO', 'FUNCION', 'NORTE', 'SUR', 'ESTE', 'OESTE',
    'MIENTRAS', 'SI', 'SI_NO', 'FLOTANTE',
    'STRING', 'VERDADERO', 'CAMINA', 'GIRA',
    'MIRA', 'A_STRING', 'REINICIAR', 'INPUT',
    'OUTPUT', 'A_ENTERO', 'ANCHO', 'ALTO',
    'A_FLOTANTE', 'SALTA_A', 'FALSO', 'ENTERO', 'MAS', 'MENOS', 'POR',
    'ENTRE', 'RESIDUO', 'MENOR_QUE', 'MAYOR_QUE',
    'MENOR_IGUAL', 'MAYOR_IGUAL', 'DIFERENTE_DE', 'IGUAL_A',
    'AND', 'OR', 'IGUAL', 'PARENTESIS_IZQ',
    'PARENTESIS_DER', 'LLAVE_IZQ', 'LLAVE_DER', 'CORCHETE_IZQ',
    'CORCHETE_DER','PUNTO_COMA', 'COMILLA', 'COMA', 'ID', 'CTE_I', 'PUNTO',
    'CTE_S',
)

reserved = {
    'inicio' : 'INICIO',
    'funcion' : 'FUNCION',
    'norte' : 'NORTE',
    'sur' : 'SUR',
    'este' : 'ESTE',
    'oeste' : 'OESTE',
    'mientras' : 'MIENTRAS',
    'si' : 'SI',
    'si_no' : 'SI_NO',
    'flotante' : 'FLOTANTE',
    'string' : 'STRING',
    'verdadero' : 'VERDADERO',
    'falso' : 'FALSO',
    'camina' : 'CAMINA',
    'gira' : 'GIRA',
    'mira' : 'MIRA',
    'a_string' : 'A_STRING',
    'reiniciar' : 'REINICIAR',
    'input' : 'INPUT',
    'output' : 'OUTPUT',
    'a_entero' : 'A_ENTERO',
    'ancho' : 'ANCHO',
    'alto' : 'ALTO',
    'a_flotante' : 'A_FLOTANTE',
    'salta_a' : 'SALTA_A',
    'entero' : 'ENTERO',
}

# Tokens
t_SEMICOLON = r'\;'
t_PERIOD = r'[\.]'
t_COMMA = r'[\,]'
t_COLON = r'\:'
t_LEFT_BRACKET = r'\{'
t_RIGHT_BRACKET = r'\}'
t_LEFT_PARENTHESIS = r'\('
t_RIGHT_PARENTHESIS = r'\)'
t_EQUAL_OPERATOR  = r'\='
t_COMPARISON_OPERATOR = r'[<][>]|[>]|[<]'
t_EXP_OPERATOR = r'\+|\-'
t_TERM_OPERATOR = r'\*|\/'
def t_CONST_NUMBER_FLOAT(t):
    r'[0-9]+\.[0-9]+'
    t.value = float(t.value)
    return t
def t_CONST_NUMBER_INT(t):
    r'\d+'
    t.value = int(t.value)
    return t
def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    if t.value in reserved:
        t.type = reserved[t.value]
    return t
t_CONST_STRING = r'\"[A-Za-z0-9_\(\)\{\}\[\]\<\>\!]*\"'

# Ignored characters
t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
import ply.lex as lex
lexer = lex.lex()

start = 'program'

def p_empty(p):
    'empty :'
    pass

def p_program(p):
    '''
    program : KEYWORD_PROGRAM IDENTIFIER COLON program_vars block_start
    '''
    print("Program start\n\tIdentifier:" + p[2] + "\n")

def p_program_vars(p):
    '''
    program_vars : vars
                | empty
    '''
    pass

def p_vars(p):
    '''
    vars : KEYWORD_VAR var_declaration_start
    '''
    print("VARIABLES:\n")

def p_var_declaration_start(p):
    '''
    var_declaration_start : IDENTIFIER var_declaration_end
    '''
    print("\t- Identifier: " + p[1] + "\n")

def p_var_declaration_end(p):
    '''
    var_declaration_end : COMMA var_declaration_start
                | var_type_start
    '''
    pass



def p_var_type_start(p):
    '''
    var_type_start : COLON var_type_def SEMICOLON var_type_end
    '''
    pass

def p_var_type_end(p):
    '''
    var_type_end : var_declaration_start
                | empty
    '''
    pass


def p_var_type_def(p):
    '''
    var_type_def : KEYWORD_TYPE_INT
                | KEYWORD_TYPE_FLOAT
    '''
    print("type definition: " + p[1] + "\n")

def p_block_start(p):
    '''
    block_start : LEFT_BRACKET block_end
    '''
    print("block start\n")

def p_block_end(p):
    '''
    block_end : statement block_end
                | RIGHT_BRACKET block_end_output
    '''
    pass

def p_block_end_output(p):
    '''
    block_end_output : empty
    '''
    print("block end\n")

def p_statement(p):
    '''
    statement : assign
                | condition
                | output
    '''
    pass

def p_assign(p):
    '''
    assign : IDENTIFIER EQUAL_OPERATOR expression SEMICOLON
    '''
    print(p[1] + " = ")

def p_expression(p):
    '''
    expression : exp_start exp_comparison
    '''
    pass

def p_exp_comparison(p):
    '''
    exp_comparison : exp_comparison_output exp_start
                | empty
    '''
    pass

def p_exp_comparison_output(p):
    '''
    exp_comparison_output : COMPARISON_OPERATOR
    '''
    print(" " + p[1])

def p_exp_start(p):
    '''
    exp_start : term_start exp_end
    '''
    pass

def p_exp_end(p):
    '''
    exp_end : exp_end_f
            | empty
    '''
    pass

def p_exp_end_f(p):
    '''
    exp_end_f : EXP_OPERATOR exp_start
    '''
    print(' ' + p[1] + ' ')

def p_error(t):
    print("Syntax error at '%s'" % t.value)

def p_term_start(p):
    '''
    term_start : factor term_end
    '''
    pass

def p_term_end(p):
    '''
    term_end : term_end_output
            | empty
    '''
    pass

def p_term_end_output(p):
    '''
    term_end_output : TERM_OPERATOR term_start
    '''
    print(p[1] + ' ')

def p_output(p):
    '''
    output : output_output write_start
    '''
    pass


def p_output_output(p):
    '''
    output_output : KEYWORD_PRINT LEFT_PARENTHESIS
    '''
    print("print (")

def p_write_start(p):
    '''
    write_start : write_start_output write_end
                | expression write_end
    '''
    pass

def p_write_start_output(p):
    '''
    write_start_output : CONST_STRING
    '''
    print(p[1] + ' ')

def p_write_end(p):
    '''
    write_end : PERIOD write_start
                | RIGHT_PARENTHESIS SEMICOLON
    '''
    print("\n")

def p_condition(p):
    '''
    condition : KEYWORD_IF LEFT_PARENTHESIS expression RIGHT_PARENTHESIS block_start condition_else
    '''
    pass

def p_condition_else(p):
    '''
    condition_else : KEYWORD_ELSE block_start
                    | empty
    '''
    pass

def p_factor(p):
    '''
    factor : LEFT_PARENTHESIS expression RIGHT_PARENTHESIS
                | EXP_OPERATOR constant_val
                | constant_val
    '''
    pass


def p_constant_val(p):
    '''
    constant_val : IDENTIFIER
        | CONST_NUMBER_INT
        | CONST_NUMBER_FLOAT
    '''
    print(str(p[1]) + ' ')

import ply.yacc as yacc
parser = yacc.yacc()

data = '''
program programa_patito :
var i_one, i_two, i_three : int ;
f_one, f_two, f_three : float ; {
    if(one + 2 < three) {
        one = 1 + 2;
        print ("Hello!1234567890");
    } else {
        lex = 30;
        false = one <> two;
    }
    one = 1;
    f_three = 2 * 3 + 5 * 2 + 6 + 6 + 7 + 8;
    f_two = 2.000;
    one = 1 + 2;
    two = one + three + 1.0;
}
'''


parser.parse(data)
