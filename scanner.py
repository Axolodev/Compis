from __future__ import print_function

import logging
import ply.lex as lex
import ply.yacc as yacc
import Utils
import TablaVariables
import TablaFunciones
import CuboSemantico

var_table = TablaVariables.TablaVariables.getInstance()
func_table = TablaFunciones.TablaFunciones.getInstance()
listaParam = []

logging.basicConfig()

tokens = (
    'KW_INICIO', 'KW_FUNCION', 'KW_NORTE', 'KW_SUR',
    'KW_ESTE', 'KW_OESTE', 'KW_MIENTRAS', 'KW_SI',
    'KW_SI_NO', 'KW_FLOTANTE', 'KW_STRING', 'KW_VERDADERO',
    'KW_CAMINA', 'KW_GIRA', 'KW_MIRA', 'KW_A_STRING',
    'KW_REINICIAR', 'KW_INPUT', 'KW_OUTPUT', 'KW_A_ENTERO',
    'KW_ANCHO', 'KW_ALTO', 'KW_A_FLOTANTE', 'KW_SALTA_A',
    'KW_FALSO', 'KW_ENTERO', 'KW_RETORNA',

    'OP_COMPARADOR', 'OP_FACTOR', 'OP_TERMINO', 'OP_AND', 'OP_OR', 'OP_ASIGNACION',
    'OP_PARENTESIS_IZQ', 'OP_PARENTESIS_DER', 'OP_LLAVE_IZQ', 'OP_LLAVE_DER',
    'OP_CORCHETE_IZQ', 'OP_CORCHETE_DER', 'OP_PUNTO_COMA',
    'OP_COMA', 'OP_PUNTO',

    'ID', 'CTE_E', 'CTE_F', 'CTE_S',
)

reserved = {
    'retorna': 'KW_RETORNA',
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

t_OP_PUNTO_COMA = r';'
t_OP_PUNTO = r'[\.]'
t_OP_COMA = r'[\,]'

tipo_actual = None
variable_actual_es_arreglo = False
variable_actual_es_matriz = False


# Pilas auxiliares
pila_tipos = []
pila_operador = []
pila_operando = []

# Lista de cuadruplos
lista_cuadruplos = []


# cuadruplo inicial
cuadruplo_inicial = [None] * 4


def t_CTE_F(t):
    r'[0-9]+\.[0-9]+'
    t.value = float(t.value)
    return t


def t_CTE_E(t):
    r'\d+'
    # print(t.value, end="")
    t.value = int(t.value)
    return t


def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    if t.value in reserved:
        t.type = reserved[t.value]
    return t


t_CTE_S = r'\"[A-Za-z0-9_\(\)\{\}\[\]\<\>\! \t]*\"'

# Ignored characters
t_ignore = " \t"


def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


# Build the lexer

lexer = lex.lex()

start = 'inicio'


def p_empty(p):
    """empty :"""
    pass


def p_inicio(p):
    """inicio : crear_var crear_funciones KW_INICIO funcion"""
    print(var_table)
    print(func_table)
    print(lista_cuadruplos)
    print(pila_operador)
    print(pila_operando)
    print(pila_tipos)


def p_crear_funciones(p):
    """
    crear_funciones : funcion crear_funciones
                    | empty
    """
    pass


def p_funcion(p):
    """
    funcion : KW_FUNCION tipo_funcion ID OP_PARENTESIS_IZQ parametros OP_PARENTESIS_DER bloque_func
    """
    global listaParam
    func_table.nuevaFuncion(tipo_actual, p[3], listaParam)
    listaParam = []


def p_tipo_funcion(p):
    """
    tipo_funcion : tipo
                    | empty
    """
    func_table.nuevoScope()


def p_tipo(p):
    """
    tipo : KW_ENTERO
        | KW_FLOTANTE
        | KW_STRING
    """
    tipo = p[1]
    global tipo_actual
    if tipo == 'entero':
        tipo_actual = Utils.Tipo.Entero
    elif tipo == 'flotante':
        tipo_actual = Utils.Tipo.Flotante
    else:
        tipo_actual = Utils.Tipo.String


def p_parametos(p):
    """
    parametros : toma_parametro
                | empty
    """
    pass


def p_toma_parametro(p):
    """
    toma_parametro : tipo ID otro_parametro
    """
    var_table.nuevaVariable(p[1], p[2], None, None)
    listaParam.append(p[1])


def p_otro_parametro(p):
    """
    otro_parametro : OP_COMA toma_parametro
                    | empty
    """
    pass


def p_bloque_func(p):
    """
    bloque_func : OP_LLAVE_IZQ crear_var estatuto_rec OP_LLAVE_DER
    """
    pass


def p_crear_var(p):
    """
    crear_var : tipo def_var otra_var op_punto_coma crear_var
                | empty
    """
    pass


def p_op_punto_coma(p):
    """
    op_punto_coma : OP_PUNTO_COMA
    """
    # print(";")
    pass


def p_def_var(p):
    """
    def_var : ID arr_not arr_not
    """
    global variable_actual_es_arreglo, variable_actual_es_matriz
    var_table.nuevaVariable(tipo_actual, p[1], variable_actual_es_arreglo, variable_actual_es_matriz)
    variable_actual_es_arreglo = False
    variable_actual_es_matriz = False


def p_arr_not(p):
    """
    arr_not : OP_CORCHETE_IZQ CTE_E OP_CORCHETE_DER
            | empty
    """
    global variable_actual_es_matriz, variable_actual_es_arreglo
    if variable_actual_es_arreglo:
        variable_actual_es_matriz = True
    else:
        variable_actual_es_arreglo = True


def p_otra_var(p):
    """
    otra_var : OP_COMA def_var otra_var
            | empty
    """
    pass


def p_estatuto(p):
    """
    estatuto : asignacion
            | condicion
            | ciclo
            | ejec_funcion
            | funcion_predef
            | retorna
    """
    pass


def p_estatuto_rec(p):
    """
    estatuto_rec : estatuto OP_PUNTO_COMA estatuto_rec
                | empty
    """
    pass


def p_asignacion(p):
    """
    asignacion : ID arr_not arr_not OP_ASIGNACION expresion
    """


def p_ciclo(p):
    """
    ciclo : KW_MIENTRAS OP_PARENTESIS_IZQ expresion OP_PARENTESIS_DER bloque_est
    """
    pass


def p_ejec_funcion(p):
    """
    ejec_funcion : ID OP_PARENTESIS_IZQ ejec_funcion_medio OP_PARENTESIS_DER
    """
    pass


def p_ejec_funcion_medio(p):
    """
    ejec_funcion_medio : expresion ejec_funcion_cont
                        | empty
    """
    pass


def p_ejec_funcion_cont(p):
    """
    ejec_funcion_cont : OP_COMA expresion ejec_funcion_cont
                        | empty
    """
    pass


def p_funcion_predef(p):
    """
    funcion_predef : camina
                    | gira
                    | mira
                    | reiniciar
                    | input
                    | output
                    | salta_a
    """
    pass


def genera_cuadruplo(lista_op):
    global cuadruplo_inicial
    if len(pila_operador) > 0:

        operador = pila_operador.pop()
        if operador in lista_op:
            tipo_2 = pila_tipos.pop()
            tipo_1 = pila_tipos.pop()
            operando2 = pila_operando.pop()
            operando1 = pila_operando.pop()
            tipo_resultado = CuboSemantico.CuboSemantico.getTipo(operador, tipo_1, tipo_2)
            pila_tipos.append(tipo_resultado)

            cuadruplo_inicial[0] = operador
            cuadruplo_inicial[1] = operando1
            cuadruplo_inicial[2] = operando2
            cuadruplo_inicial[3] = -cuadruplo_inicial[1] # todo: Cambiar a resultado
            lista_cuadruplos.append(cuadruplo_inicial)
            pila_operando.append(cuadruplo_inicial[3])
        else:
            pila_operador.append(operador)


def p_expresion(p):
    """
    expresion : comp_or genera_cuadruplo_or otra_expresion_or
    """
    pass


def p_genera_cuadruplo_or(p):
    """
    genera_cuadruplo_or :
    """
    genera_cuadruplo(["||"])


def p_otra_expresion_or(p):
    """
    otra_expresion_or : consume_op_or expresion
                    | empty
    """
    pass


def p_consume_op_or(p):
    """
    consume_op_or : OP_OR
    """
    pila_operador.append(p[1])


def p_comp_or(p):
    """
    comp_or : comp_and genera_cuadruplo_and otra_expresion_and
    """
    pass


def p_genera_cuadruplo_and(p):
    """
    genera_cuadruplo_and :
    """
    genera_cuadruplo(["&&"])


def p_otra_expresion_and(p):
    """
    otra_expresion_and : consume_op_and expresion
                    | empty
    """
    pass


def p_consume_op_and(p):
    """
    consume_op_and : OP_AND
    """

    pila_operador.append(p[1])


def p_comp_and(p):
    """
    comp_and : exp genera_cuadruplo_comparador comp_and_end
    """
    pass


def p_genera_cuadruplo_comparador(p):
    """
    genera_cuadruplo_comparador :
    """
    genera_cuadruplo(["<", ">", "<=", ">=", "!=", "=="])


def p_comp_and_end(p):
    """
    comp_and_end : op_comparador comp_and
                | empty
    """
    pass


def p_op_comparador(p):
    """
    op_comparador : OP_COMPARADOR
    """
    pila_operador.append(p[1].value)


def p_exp(p):
    """
    exp : termino genera_cuadruplo_termino exp2
    """
    pass

def p_genera_cuadruplo(p):
    """
    genera_cuadruplo_termino :
    """
    genera_cuadruplo(["+", "-"])


def p_exp2(p):
    """
    exp2 : consume_op_termino exp
        | empty
    """
    pass


def p_consume_op_termino(p):
    """
    consume_op_termino : OP_TERMINO
    """
    pila_operador.append(p[1])


def p_termino(p):
    """
    termino : factor genera_cuadruplo_factor termino2
    """
    pass


def p_genera_cuadruplo_factor(p):
    """
    genera_cuadruplo_factor :
    """
    genera_cuadruplo(["*", "/", "%"])

def p_termino2(p):
    """
    termino2 : consume_op_factor termino
            | empty
    """
    pass


def p_consume_op_factor(p):
    """
    consume_op_factor : OP_FACTOR
    """
    pila_operando.append(p[1])


def p_factor(p):
    """
    factor : OP_PARENTESIS_IZQ expresion OP_PARENTESIS_DER
            | OP_TERMINO var_cte
            | var_cte
    """
    if len(p) == 3:
        tipo = pila_tipos.pop()
        if tipo != Utils.Tipo.String:
            pass  # todo: checar que no sea string
            if p[1].value == '-':
                global cuadruplo_inicial
                cuadruplo_inicial[0] = '-'
                cuadruplo_inicial[1] = pila_operando.pop()
                cuadruplo_inicial[2] = None
                cuadruplo_inicial[3] = -cuadruplo_inicial[1]
                lista_cuadruplos.append(cuadruplo_inicial)
                pila_operando.append(cuadruplo_inicial[3])
                pila_tipos.append(tipo)


def p_camina(p):
    """
    camina : KW_CAMINA OP_PARENTESIS_IZQ expresion OP_PARENTESIS_DER
    """
    pass


def p_gira(p):
    """
    gira : KW_GIRA OP_PARENTESIS_IZQ expresion OP_PARENTESIS_DER
    """
    pass


def p_mira(p):
    """
    mira : KW_MIRA OP_PARENTESIS_IZQ expresion OP_PARENTESIS_DER
    """
    pass


def p_a_string(p):
    """
    a_string : KW_A_STRING OP_PARENTESIS_IZQ a_string2 OP_PARENTESIS_DER
    """
    pass


def p_a_string2(p):
    """
    a_string2 : CTE_E
            | CTE_F
            | ID arr_not arr_not
    """
    pass


def p_a_entero(p):
    """
    a_entero : KW_A_ENTERO OP_PARENTESIS_IZQ a_entero2 OP_PARENTESIS_DER
    """
    pass


def p_a_entero2(p):
    """
    a_entero2 : CTE_F
            | concat_string
    """
    pass


def p_condicion(p):
    """
    condicion : KW_SI OP_PARENTESIS_IZQ expresion OP_PARENTESIS_DER bloque_est si_no
    """
    pass


def p_si_no(p):
    """
    si_no : KW_SI_NO bloque_est
            | empty
    """
    pass


def p_bloque_est(p):
    """
    bloque_est : OP_LLAVE_IZQ estatuto_rec OP_LLAVE_DER
    """
    pass


def p_retorna(p):
    """
    retorna : KW_RETORNA expresion
    """
    pass


def p_var_cte(p):
    """
    var_cte : var_consume_id_var_cte var_cte2
            | a_string
            | a_entero
            | a_flotante
            | p_cte_e_f
            | maneja_var_cte_defaults
    """
    pass


def p_maneja_var_cte_defaults(p):
    """
    maneja_var_cte_defaults : KW_VERDADERO
            | KW_FALSO
            | KW_NORTE
            | KW_SUR
            | KW_ESTE
            | KW_OESTE
            | KW_ANCHO
            | KW_ALTO
    """
    '''
    if p.type == 'KW_VERDADERO':
        p.value = 1
    elif p.type == 'KW_FALSO':
        p.value = 0
    elif p.type == 'KW_NORTE':
        p.value = 90
    elif p.type == 'KW_SUR':
        p.value = 270
    elif p.type == 'KW_ESTE':
        p.value = 0
    elif p.type == 'KW_OESTE':
        p.value = 180
    elif p.type == 'KW_ANCHO':
        p.value = 800
    elif p.type == 'KW_ALTO':
        p.value = 600
    p.type = 'CTE_E'
    construye_cuadruplo(p)
    '''


def p_cte_e_f(p):
    """
    p_cte_e_f : consume_cte_entero
            | consume_cte_flotante
    """
    print(p[1])


def p_consume_flotante(p):
    """
    consume_cte_flotante : CTE_F
    """
    genera_operando({"valor": p[1], "tipo": Utils.Tipo.Flotante})


def p_consume_entero(p):
    """
    consume_cte_entero : CTE_E
    """
    genera_operando({"valor": p[1], "tipo": Utils.Tipo.Entero})


def p_var_consume_id_var_cte(p):
    """
    var_consume_id_var_cte : ID
    """
    print(p[1])
    genera_operando(p[1])
    var_table.getVariable(p[1])


def p_var_cte2(p):
    """
    var_cte2 : arr_not arr_not
            | OP_PARENTESIS_IZQ var_cte3 OP_PARENTESIS_DER
    """
    pass


def p_var_cte3(p):
    """
    var_cte3 : expresion var_cte4
    """
    pass


def p_var_cte4(p):
    """
    var_cte4 : OP_COMA expresion var_cte4
            | empty
    """
    pass


def p_concat_string(p):
    """
    concat_string : CTE_S concat_string2
    """
    pass


def p_concat_string2(p):
    """
    concat_string2 : OP_PUNTO CTE_S
            | empty
    """
    pass


def p_a_flotante(p):
    """
    a_flotante : KW_A_FLOTANTE OP_PARENTESIS_IZQ a_flotante2 OP_PARENTESIS_DER
    """
    pass


def p_a_flotante2(p):
    """
    a_flotante2 : concat_string
                | CTE_F
    """
    pass


def p_reiniciar(p):
    """
    reiniciar : KW_REINICIAR OP_PARENTESIS_IZQ OP_PARENTESIS_DER
    """
    pass


def p_input(p):
    """
    input : KW_INPUT OP_PARENTESIS_IZQ ID input2 OP_PARENTESIS_DER
    """
    pass


def p_input2(p):
    """
    input2 : OP_COMA ID input2
            | empty
    """
    pass


def p_output(p):
    """
    output : KW_OUTPUT OP_PARENTESIS_IZQ concat_string OP_PARENTESIS_DER
    """
    pass


def p_salta_a(p):
    """
    salta_a : KW_SALTA_A OP_PARENTESIS_IZQ CTE_E OP_COMA CTE_E OP_PARENTESIS_DER
    """
    pass


def p_error(p):
    print("\nSyntax error with token of type " + p.type + " with value " + p.value + " in line " + str(p.lineno))
    pass


def genera_operando(operando_a_generar):
    global pila_operando
    global pila_tipos

    pila_tipos.append(operando_a_generar["tipo"])
    pila_operando.append(operando_a_generar["valor"])


parser = yacc.yacc()

data = '''
flotante global;
flotante globalDos[2];
string una_var[2][3], otra_var, another;
funcion prueba(entero x, flotante y){
    entero a;
    flotante b;
    a = 2 + 2;
}
funcion flotante cualquiera(entero dos){
    entero variable_meh;
}
inicio funcion entero ai(){
    string falla;
    entero x;
    output("");
    prueba1();
    gira(norte);

}'''
# checar que las funciones esten definidas
log = logging.getLogger("parserlog.log")
parser.parse(data, debug=0)
