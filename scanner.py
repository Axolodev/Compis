# -----------------------------------------------------------------------------
# calc.py
#
# A simple calculator with variables.
# -----------------------------------------------------------------------------
from __future__ import print_function
tokens = (
    'KW_INICIO', 'KW_FUNCION', 'KW_NORTE', 'KW_SUR',
    'KW_ESTE', 'KW_OESTE', 'KW_MIENTRAS', 'KW_SI',
    'KW_SI_NO', 'KW_FLOTANTE', 'KW_STRING', 'KW_VERDADERO',
    'KW_CAMINA', 'KW_GIRA', 'KW_MIRA', 'KW_A_STRING',
    'KW_REINICIAR', 'KW_INPUT', 'KW_OUTPUT', 'KW_A_ENTERO',
    'KW_ANCHO', 'KW_ALTO', 'KW_A_FLOTANTE', 'KW_SALTA_A',
    'KW_FALSO', 'KW_ENTERO',

    'OP_SUMA', 'OP_RESTA', 'OP_MULTIPLICACION', 'OP_DIVISION', 'OP_RESIDUO',
    'OP_MENOR_QUE', 'OP_MAYOR_QUE', 'OP_MENOR_IGUAL', 'OP_MAYOR_IGUAL',
    'OP_DIFERENTE_DE', 'OP_IGUAL_A', 'OP_AND', 'OP_OR', 'OP_ASIGNACION',
    'OP_PARENTESIS_IZQ', 'OP_PARENTESIS_DER', 'OP_LLAVE_IZQ', 'OP_LLAVE_DER',
    'OP_CORCHETE_IZQ', 'OP_CORCHETE_DER', 'OP_PUNTO_COMA',
    'OP_COMA', 'OP_PUNTO',

    'ID', 'CTE_E', 'CTE_F', 'CTE_S',
)

reserved = {
    'inicio': 'KW_INICIO',
    'funcion': 'KW_FUNCION',
    'norte': 'KW_NORTE',
    'sur': 'KW_SUR',
    'este': 'KW_ESTE',
    'oeste': 'KW_OESTE',
    'mientras': 'KW_MIENTRAS',
    'si': 'KW_SI',
    'si_no': 'KW_SI_NO',
    'flotante': 'KW_FLOTANTE',
    'string': 'KW_STRING',

    'verdadero': 'KW_VERDADERO',
    'falso': 'KW_FALSO',

    'camina': 'KW_CAMINA',
    'gira': 'KW_GIRA',
    'mira': 'KW_MIRA',
    'a_string': 'KW_A_STRING',
    'reiniciar': 'KW_REINICIAR',
    'input': 'KW_INPUT',
    'output': 'KW_OUTPUT',
    'a_entero': 'KW_A_ENTERO',
    'ancho': 'KW_ANCHO',
    'alto': 'KW_ALTO',
    'a_flotante': 'KW_A_FLOTANTE',
    'salta_a': 'KW_SALTA_A',
    'entero': 'KW_ENTERO',
}

# Tokens
t_OP_TERMINO = r'\+|\-'
t_OP_FACTOR = r'\*|\/|\%'
t_OP_COMPARADOR = r'[<]|[>]|[>][=]|[<][=]|[=][=]|![=]'
t_OP_AND = r'[&][&]'
t_OP_OR = r'[|][|]'
t_OP_ASIGNACION = r'[=]'
t_OP_PARENTESIS_IZQ = r'\('
t_OP_PARENTESIS_DER = r'\)'
t_OP_LLAVE_IZQ = r'\{'
t_OP_LLAVE_DER = r'\}'
t_OP_CORCHETE_IZQ = r'\['
t_OP_CORCHETE_DER = r'\]'

t_OP_PUNTO_COMA = r'\;'
t_OP_PUNTO = r'[\.]'
t_OP_COMA = r'[\,]'


def t_CTE_F(t):
    r'[0-9]+\.[0-9]+'
    t.value = float(t.value)
    return t

def t_CTE_E(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    if t.value in reserved:
        t.type = reserved[t.value]
    return t


t_CTE_S = r'\"[A-Za-z0-9_\(\)\{\}\[\]\<\>\!]*\"'

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

start = 'inicio'

def p_empty(p):
    'empty :'
    pass

def p_inicio(p):
    'inicio : crear_var_glob crear_funciones KW_INICIO funcion'
    pass

def p_crear_funciones(p):
    '''
    crear_funciones : funcion crear_funciones
                    | empty
    '''
    pass

def p_crear_var_glob(p):
    '''
    crear_var_glob : crear_var crear_var_glob
                    | empty
    '''
    pass

def p_funcion(p):
    '''
    funcion : KW_FUNCION tipo_funcion print_id OP_PARENTESIS_IZQ parametros OP_PARENTESIS_DER bloque_func
    '''
    pass

def p_print_id(p):
    'print_id : ID'
    print (p[1])

def p_tipo_funcion(p):
    '''
    tipo_funcion : tipo
                    | empty
    '''
    pass

def p_tipo(p):
    '''
    tipo : KW_ENTERO
        | KW_FLOTANTE
        | KW_STRING
    '''
    print(p[1] + " ", end="")

def p_parametos(p):
    '''
    parametros : toma_parametro
                | empty
    '''
    pass

def p_toma_parametro(p):
    '''
    toma_parametro : tipo ID otro_parametro
    '''
    pass



def p_otro_parametro(p):
    '''
    otro_parametro : print_coma toma_parametro
                    | empty
    '''
    pass

def p_print_coma(p):
    '''
    print_coma : OP_COMA
    '''
    print(", ", end="")

def p_bloque_func(p):
    '''
    bloque_func : OP_LLAVE_IZQ crear_var estatuto OP_LLAVE_DERECHA
    '''
    pass

def p_crear_var(p):
    '''
    crear_var : tipo def_var otra_var OP_PUNTO_COMA crear_var
                | empty
    '''
    pass


def p_def_var(p):
    '''
    def_var : print_id arr_not arr_not
    '''
    pass

def p_arr_not(p):
    '''
    arr_not : OP_CORCHETE_IZQ CTE_E OP_CORCHETE_DER
    '''
    print ("[" + p[2] + "]", end="")

def p_otra_var(p):
    '''
    otra_var : print_coma def_var p_otra_var
            | empty
    '''
    pass

def p_estatuto(p):
    '''
    estatuto : asignacion
            | condicion
            | ciclo
            | ejec_funcion
            | funcion_predef
    '''

def p_un_estatuto(p):
    '''
    un_estatuto : estatuto un_estatuto
                | empty
    '''

def p_ciclo(p):
    '''
    ciclo : KW_MIENTRAS OP_PARENTESIS_IZQ expresion OP_PARENTESIS_DER bloque_est
    '''

def p_ejec_funcion(p):
    '''
    ejec_funcion : ID OP_PARENTESIS_IZQ ejec_funcion_medio OP_PARENTESIS_DER OP_PUNTO_COMA
    '''

def p_ejec_funcion_medio(p):
    '''
    ejec_funcion_medio : expresion ejec_funcion_cont
                        | empty
    '''

def p_ejec_funcion_cont(p):
    '''
    ejec_funcion_cont : OP_COMA expresion ejec_funcion_cont
                        | empty
    '''

def p_funcion_predef(p):
    '''
    funcion_predef : camina
                    | gira
                    | mira
                    | a_string
                    | a_entero
                    | a_flotante
                    | reiniciar
                    | input
                    | output
    '''

def p_expresion(p):
    '''
    expresion(p): comp_or otra_expresion_or
    '''

def p_otra_expresion_or(p):
    '''
    otra_expresion_or : OP_OR comp_or
                    | empty
    '''

def p_comp_or(p):
    '''
    comp_or : comp_and otra_expresion_and
    '''

def p_otra_expresion_and(p):
    '''
    otra_expresion_and : OP_AND comp_and
                    | empty
    '''

def p_comp_and(p):
    '''
    comp_and : exp comp_and_end
    '''

def p_comp_and_end(p):
    '''
    comp_and_end : op_comparador exp
                | empty
    '''

def p_op_comparador(p):
    '''
    op_comparador : OP_COMPARADOR
    '''
    print(' ' + p.value + ' ', end="")

def p_exp(p):
    '''
    exp : termino exp2
    '''

def p_exp2(p):
    '''
    exp2 : OP_TERMINO exp
        | empty
    '''

def p_termino(p):
    '''
    termino : factor termino2
    '''

def p_termino2(p):
    '''
    termino2 : OP_FACTOR termino
            | empty
    '''

def p_factor(p):
    '''
    factor : OP_PARENTISIS_IZQ expresion OP_PARENTESIS_DER
            | OP_TERMINO var_cte
            | var_cte
    '''

def p_var_cte(p):
    '''
    factor2 : var_cte
    '''

def p_camina(p):
    '''
    camina : KW_CAMINA OP_PARENTESIS_IZQ expresion OP_PARENTESIS_DER OP_PUNTO_COMA
    '''

def p_gira(p):
    '''
    gira : KW_GIRA OP_PARENTESIS_IZQ expresion OP_PARENTESIS_DER OP_PUNTO_COMA
    '''

def p_mira(p):
    '''
    mira: KW_MIRA OP_PARENTESIS_IZQ expresion OP_PARENTESIS_DER OP_PUNTO_COMA
    '''

def p_a_string(p):
    '''
    a_string: KW_A_STRING OP_PARENTESIS_IZQ a_string2 OP_PARENTESIS_DER OP_PUNTO_COMA
    '''

def p_a_string2(p):
    '''
    a_string2 : CTE_E
            | CTE_F
            | ID arr_not arr_not
    '''

def p_a_entero(p):
    '''
    a_entero : KW_ENTERO OP_PARENTESIS_IZQ a_entero2 OP_PARENTESIS_DER OP_PUNTO_COMA
    '''


def p_a_entero2(p):
    '''
    a_entero2 : CTE_F
            | concat_string
    '''

def p_condicion(p):
    '''
    condicion : KW_SI OP_PARENTESIS_IZQ expresion OP_PARENTESIS_DER bloque_est si_no
    '''

def p_si_no(p):
    '''
    si_no : KW_SI_NO bloque_est
            | empty
    '''

def p_bloque_est(p):
    '''
    bloque_est : OP_LLAVE_IZQ estatuto OP_LLAVE_DER
    '''
'''
-------------------------
'''

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
