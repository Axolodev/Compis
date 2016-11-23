from __future__ import print_function

import logging
import warnings

import CuboSemantico
import Memoria
import TablaFunciones
import TablaVariables
import Utils
import ply.lex as lex
import ply.yacc as yacc

var_table = TablaVariables.TablaVariables.getInstance()
func_table = TablaFunciones.TablaFunciones.getInstance()
lista_param = []
variable_nombre_funcion = ""
indiceParametro = 0

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
    'OP_COMA',

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
t_OP_COMPARADOR = r'>=|<=|[<]|[>]|[=][=]|![=]'
t_OP_AND = r'[&][&]'
t_OP_OR = r'[|][|]'
t_OP_ASIGNACION = r'='
t_OP_PARENTESIS_IZQ = r'\('
t_OP_PARENTESIS_DER = r'\)'
t_OP_LLAVE_IZQ = r'\{'
t_OP_LLAVE_DER = r'\}'
t_OP_CORCHETE_IZQ = r'\['
t_OP_CORCHETE_DER = r'\]'

t_OP_PUNTO_COMA = r';'
t_OP_COMA = r'[\,]'

tipo_actual = Utils.Tipo.Vacio
lista_dimensiones = []
tipo_funcion_actual = Utils.Tipo.Vacio
nombre_funcion_actual = None
contador_variable_dimensionada = 0
var_actual = None

# Pilas auxiliares
pila_tipos = []
pila_operadores = []
pila_operandos = []
pila_saltos = []
pila_dimensiones = []

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


t_CTE_S = r'"[A-Za-z0-9_\(\)\{\}\[\]\<\>\! \t]*"'

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
    """inicio : crear_cuadruplo_inicio crear_var crear_funciones encontrar_posicion_cuadruplo_de_inicio funcion"""
    cuadruplo_inicial[0] = Utils.Operador.getId('end')
    lista_cuadruplos.append(cuadruplo_inicial)

    if Utils.DEBUGGING_MODE:
        print("Tabla de variables:")
        print(var_table)
        print("Tabla de funciones:")
        print(func_table)
        print("Lista de cuadruplos:")
        i = 0
        for item in lista_cuadruplos:
            print(str(i) + ':' + str(item))
            i += 1

        print()
        print("Pila de operadores:")
        print(pila_operadores)
        print("Pila de operandos:")
        print(pila_operandos)
        print("Pila de tipos:")
        print(pila_tipos)


def p_encontrar_posicion_cuadruplo_de_inicio(p):
    """
    encontrar_posicion_cuadruplo_de_inicio : KW_INICIO
    """
    global cuadruplo_inicial
    cuadruplo_inicial = lista_cuadruplos[0]
    cuadruplo_inicial[3] = len(lista_cuadruplos)
    lista_cuadruplos[0] = cuadruplo_inicial
    cuadruplo_inicial = [None] * 4


def p_crear_cuadruplo_inicio(p):
    """
    crear_cuadruplo_inicio :
    """
    global cuadruplo_inicial
    cuadruplo_inicial[0] = Utils.Operador.getId('goto')
    lista_cuadruplos.append(cuadruplo_inicial)
    cuadruplo_inicial = [None] * 4


def p_crear_funciones(p):
    """
    crear_funciones : funcion crear_funciones
                    | empty
    """
    pass


def p_consumir_nombre_funcion(p):
    """
    consumir_nombre_funcion : ID
    """
    global nombre_funcion_actual
    global tipo_funcion_actual
    nombre_funcion_actual = p[1]
    var_table.nuevaVariable(tipo_funcion_actual, p[1], None, scope="0")


def p_funcion(p):
    """
    funcion : KW_FUNCION tipo_funcion consumir_nombre_funcion OP_PARENTESIS_IZQ parametros OP_PARENTESIS_DER dar_de_alta_funcion bloque_func
    """
    global tipo_funcion_actual
    global cuadruplo_inicial
    global nombre_funcion_actual
    tipo_funcion_actual = Utils.Tipo.Vacio
    if Utils.DEBUGGING_MODE:
        print("Nombre actual:", variable_nombre_funcion)
    cuadruplo_inicial[0] = Utils.Operador.getId('ret')
    lista_cuadruplos.append(cuadruplo_inicial)
    cuadruplo_inicial = [None] * 4


def p_dar_de_alta_funcion(p):
    """
    dar_de_alta_funcion :
    """
    global lista_param
    global tipo_actual
    global nombre_funcion_actual
    func_table.nuevaFuncion(tipo_actual, nombre_funcion_actual, lista_param, len(lista_cuadruplos))
    # Borrar valores de variables que ya no se necesitan.
    nombre_funcion_actual = None
    lista_param = []


def p_tipo_funcion(p):
    """
    tipo_funcion : tipo
                    | empty
    """
    func_table.nuevoScope()
    global tipo_funcion_actual
    tipo_funcion_actual = tipo_actual


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


def p_consume_parametro_de_funcion(p):
    """
    consume_parametro_de_funcion : tipo ID
    """
    global tipo_actual
    global lista_param
    var_table.nuevaVariable(tipo_actual, p[2], None)
    lista_param.append(tipo_actual)


def p_toma_parametro(p):
    """
    toma_parametro : consume_parametro_de_funcion otro_parametro
    """
    pass


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
    global pila_tipos
    global pila_operandos
    pila_tipos = []
    pila_operandos = []


def p_def_var(p):
    """
    def_var : ID def_dimensiones
    """
    global lista_dimensiones
    var_table.nuevaVariable(tipo_actual, p[1], lista_dimensiones=lista_dimensiones)
    lista_dimensiones = []


def p_def_dimensiones(p):
    """
    def_dimensiones : declaracion_dimensiones def_dimensiones
                | empty
    """


def p_declaracion_dimensiones(p):
    """
    declaracion_dimensiones : OP_CORCHETE_IZQ CTE_E OP_CORCHETE_DER
    """
    global lista_dimensiones
    lista_dimensiones.append(p[2])
    Memoria.Memoria.getInstance().generaEspacioConstantes(Utils.Tipo.Entero, p[2])


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
    estatuto_rec : estatuto op_punto_coma estatuto_rec
                | empty
    """
    pass


def p_asignacion(p):
    """
    asignacion : var_consume_id_var_cte acceso_variable_dimensionada OP_ASIGNACION expresion
    """
    global cuadruplo_inicial
    tipo_operando = pila_tipos.pop()
    tipo_resultado = pila_tipos.pop()
    CuboSemantico.CuboSemantico.getTipo("=", tipo_operando, tipo_resultado)
    cuadruplo_inicial[0] = Utils.Operador.getId('=')
    cuadruplo_inicial[1] = pila_operandos.pop()
    cuadruplo_inicial[3] = pila_operandos.pop()
    lista_cuadruplos.append(cuadruplo_inicial)
    cuadruplo_inicial = [None] * 4


def p_ciclo(p):
    """
    ciclo : KW_MIENTRAS consume_par_izq_ciclo expresion consume_par_der bloque_est
    """
    falso = pila_saltos.pop()
    retorno = pila_saltos.pop()
    global cuadruplo_inicial
    cuadruplo_inicial[0] = Utils.Operador.getId('goto')
    cuadruplo_inicial[3] = retorno
    lista_cuadruplos.append(cuadruplo_inicial)
    cuadruplo_inicial = [None] * 4
    cuadruplo_inicial = lista_cuadruplos[falso]
    cuadruplo_inicial[3] = len(lista_cuadruplos)
    cuadruplo_inicial = [None] * 4


def p_consume_par_izq_ciclo(p):
    """
    consume_par_izq_ciclo : OP_PARENTESIS_IZQ
    """
    pila_saltos.append(len(lista_cuadruplos))


def p_ejec_funcion(p):
    """
    ejec_funcion : consume_id_funcion consume_par_izq genera_era ejec_funcion_medio OP_PARENTESIS_DER
    """
    global lista_param
    global cuadruplo_inicial
    global pila_operadores
    i = 0
    pila_operadores.pop()
    func_table.checaParam(variable_nombre_funcion, lista_param)
    lista_param = []
    var = var_table.getVariable(variable_nombre_funcion)
    pila_tipos.append(var.getTipo())
    if Utils.DEBUGGING_MODE:
        print("Tipo de retorno de funcion:", var.getTipo(), "\n")
        print("Cuadruplos:")
        print("Pila de tipos despues de funcion:\n", pila_tipos)
        print("------------------------")

    espacio = Memoria.Memoria.getInstance().generaEspacioTemporal(var.getTipo())
    pila_operandos.append(espacio)
    cuadruplo_inicial[0] = Utils.Operador.getId('=')
    cuadruplo_inicial[1] = var.getEspacioMemoria()
    cuadruplo_inicial[3] = espacio
    lista_cuadruplos.append(cuadruplo_inicial)
    cuadruplo_inicial = [None] * 4


def p_genera_era(p):
    """
    genera_era :
    """
    global cuadruplo_inicial

    cuadruplo_inicial[0] = Utils.Operador.getId('era')
    cuadruplo_inicial[1] = variable_nombre_funcion
    lista_cuadruplos.append(cuadruplo_inicial)
    if Utils.DEBUGGING_MODE:
        print("Cuadruplo ERA:", cuadruplo_inicial)
    cuadruplo_inicial = [None] * 4


def p_consume_id_funcion(p):
    """
    consume_id_funcion : ID
    """
    global variable_nombre_funcion
    if not func_table.existeFuncion(p[1]):
        raise NameError("La funcion no existe")
    variable_nombre_funcion = p[1]


def p_ejec_funcion_medio(p):
    """
    ejec_funcion_medio : expresion_parametro ejec_funcion_cont
                        | empty
    """
    global indiceParametro
    global cuadruplo_inicial
    indiceParametro = 0
    cuadruplo_inicial[0] = Utils.Operador.getId('gosub')
    cuadruplo_inicial[1] = variable_nombre_funcion
    lista_cuadruplos.append(cuadruplo_inicial)
    cuadruplo_inicial = [None] * 4


def p_expresion_parametro(p):
    """
    expresion_parametro : expresion
    """
    global lista_param
    global pila_tipos
    global cuadruplo_inicial
    global indiceParametro

    lista_param.insert(0, pila_tipos.pop())
    funcion = func_table.getFuncion(variable_nombre_funcion)
    lista_variables = var_table.consigueVariablesPara(funcion.getScope())
    lista = list(zip(lista_variables.values()))
    lista_memoria = [list(x)[0].getEspacioMemoria() for x in lista]
    variables_ordenadas = sorted(lista_memoria)

    cuadruplo_inicial[0] = Utils.Operador.getId('param')
    cuadruplo_inicial[1] = pila_operandos.pop()
    cuadruplo_inicial[3] = variables_ordenadas[indiceParametro]
    indiceParametro += 1
    lista_cuadruplos.append(cuadruplo_inicial)
    cuadruplo_inicial = [None] * 4


def p_ejec_funcion_cont(p):
    """
    ejec_funcion_cont : OP_COMA expresion_parametro ejec_funcion_cont
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
    if len(pila_operadores) > 0:
        operador = pila_operadores.pop()
        if operador in lista_op:
            tipo_2 = pila_tipos.pop()
            tipo_1 = pila_tipos.pop()
            operando2 = pila_operandos.pop()
            operando1 = pila_operandos.pop()
            tipo_resultado = CuboSemantico.CuboSemantico.getTipo(operador, tipo_1, tipo_2)
            pila_tipos.append(tipo_resultado)
            espacio = Memoria.Memoria.getInstance().generaEspacioTemporal(tipo_resultado)
            cuadruplo_inicial[0] = Utils.Operador.getId(operador)
            cuadruplo_inicial[1] = operando1
            cuadruplo_inicial[2] = operando2
            cuadruplo_inicial[3] = espacio
            lista_cuadruplos.append(cuadruplo_inicial)
            pila_operandos.append(espacio)
            cuadruplo_inicial = [None] * 4
        else:
            pila_operadores.append(operador)


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
    pila_operadores.append(p[1])


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

    pila_operadores.append(p[1])


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
    pila_operadores.append(p[1])


def p_exp(p):
    """
    exp : termino genera_cuadruplo_termino exp2
    """
    pass


def p_genera_cuadruplo_termino(p):
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
    pila_operadores.append(p[1])


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
    pila_operadores.append(p[1])


def p_factor(p):
    """
    factor : consume_par_izq expresion OP_PARENTESIS_DER
            | OP_TERMINO var_cte
            | var_cte
    """

    if len(p) == 4:
        if len(pila_operadores) > 0:
            top = pila_operadores.pop()
            if top != "(":
                pila_operadores.append(top)
    elif len(p) == 3:
        tipo = pila_tipos.pop()
        if tipo == Utils.Tipo.String:
            raise ArithmeticError('Tipo string no puede ser negativo')
        elif p[1] == '-':
            global cuadruplo_inicial
            cuadruplo_inicial[0] = Utils.Operador.getId('-')
            cuadruplo_inicial[1] = pila_operandos.pop()
            cuadruplo_inicial[2] = None
            cuadruplo_inicial[3] = Memoria.Memoria.getInstance().generaEspacioTemporal(tipo)
            lista_cuadruplos.append(cuadruplo_inicial)
            pila_operandos.append(cuadruplo_inicial[3])
            cuadruplo_inicial = [None] * 4
            pila_tipos.append(tipo)


def p_consume_par_izq(p):
    """
    consume_par_izq : OP_PARENTESIS_IZQ
    """
    pila_operadores.append("(")


def p_camina(p):
    """
    camina : KW_CAMINA OP_PARENTESIS_IZQ expresion OP_PARENTESIS_DER
    """
    metros = pila_operandos.pop()
    tipo = pila_tipos.pop()
    if Utils.DEBUGGING_MODE:
        print(tipo)
    if tipo != Utils.Tipo.Entero:
        raise TypeError('Solo puedes caminar usando unidades enteras')
    global cuadruplo_inicial
    cuadruplo_inicial[0] = Utils.Operador.getId('camina')
    cuadruplo_inicial[3] = metros
    lista_cuadruplos.append(cuadruplo_inicial)
    cuadruplo_inicial = [None] * 4


def p_gira(p):
    """
    gira : KW_GIRA OP_PARENTESIS_IZQ expresion OP_PARENTESIS_DER
    """
    metros = pila_operandos.pop()
    tipo = pila_tipos.pop()
    if tipo == Utils.Tipo.String:
        raise TypeError('No puedes girar con palabras')
    global cuadruplo_inicial
    cuadruplo_inicial[0] = Utils.Operador.getId('gira')
    cuadruplo_inicial[3] = metros
    lista_cuadruplos.append(cuadruplo_inicial)
    cuadruplo_inicial = [None] * 4


def p_mira(p):
    """
    mira : KW_MIRA OP_PARENTESIS_IZQ expresion OP_PARENTESIS_DER
    """
    metros = pila_operandos.pop()
    tipo = pila_tipos.pop()
    if tipo == Utils.Tipo.String:
        raise TypeError('No puedes mirar en dirar en direccion a palabras')
    global cuadruplo_inicial
    cuadruplo_inicial[0] = Utils.Operador.getId('mira')
    cuadruplo_inicial[3] = metros
    lista_cuadruplos.append(cuadruplo_inicial)
    cuadruplo_inicial = [None] * 4


def p_a_string(p):
    """
    a_string : KW_A_STRING OP_PARENTESIS_IZQ a_string2 OP_PARENTESIS_DER
    """
    pass


def p_a_string2(p):
    """
    a_string2 : expresion
    """
    global pila_tipos
    global cuadruplo_inicial
    tipo = pila_tipos.pop()
    if tipo == Utils.Tipo.Entero or tipo == Utils.Tipo.Flotante:
        pila_tipos.append(Utils.Tipo.String)
        resultado = pila_operandos.pop()
        cuadruplo_inicial[0] = Utils.Operador.getId('a_string')
        cuadruplo_inicial[1] = resultado
        cuadruplo_inicial[3] = Memoria.Memoria.getInstance().generaEspacioTemporal(Utils.Tipo.String)
        lista_cuadruplos.append(cuadruplo_inicial)
        pila_operandos.append(cuadruplo_inicial[3])
        cuadruplo_inicial = [None] * 4
    else:
        warnings.warn("La expresion ya tiene como tipo de resultado un string. Seguro que quieres convertirlo?")


def p_a_entero(p):
    """
    a_entero : KW_A_ENTERO OP_PARENTESIS_IZQ a_entero2 OP_PARENTESIS_DER
    """
    pass


def p_a_entero2(p):
    """
    a_entero2 : expresion
    """
    global pila_tipos
    global cuadruplo_inicial
    tipo = pila_tipos.pop()
    if tipo == Utils.Tipo.Flotante or tipo == Utils.Tipo.String:
        pila_tipos.append(Utils.Tipo.Entero)
        resultado = pila_operandos.pop()
        cuadruplo_inicial[0] = Utils.Operador.getId('a_entero')
        cuadruplo_inicial[1] = resultado
        cuadruplo_inicial[3] = Memoria.Memoria.getInstance().generaEspacioTemporal(Utils.Tipo.Entero)
        lista_cuadruplos.append(cuadruplo_inicial)
        pila_operandos.append(cuadruplo_inicial[3])
        cuadruplo_inicial = [None] * 4
    else:
        warnings.warn("La expresion ya tiene como tipo de resultado un entero. Seguro que quieres convertirlo?")


def p_condicion(p):
    """
    condicion : KW_SI OP_PARENTESIS_IZQ expresion consume_par_der bloque_est si_no
    """
    pass


def p_consume_par_der(p):
    """
    consume_par_der : OP_PARENTESIS_DER
    """
    tipo = pila_tipos.pop()
    if tipo == Utils.Tipo.String:
        raise TypeError('Tipo string no puede ser usado como condicion')
    resultado = pila_operandos.pop()
    global cuadruplo_inicial
    cuadruplo_inicial[0] = Utils.Operador.getId('gotoF')
    cuadruplo_inicial[1] = resultado
    lista_cuadruplos.append(cuadruplo_inicial)
    pila_saltos.append(len(lista_cuadruplos) - 1)
    cuadruplo_inicial = [None] * 4


def p_si_no(p):
    """
    si_no : consume_si_no bloque_est
            | empty
    """
    posicion_falso = pila_saltos.pop()
    cuadruplo_goto_f = lista_cuadruplos[posicion_falso]
    cuadruplo_goto_f[3] = len(lista_cuadruplos)
    lista_cuadruplos[posicion_falso] = cuadruplo_goto_f


def p_consume_si_no(p):
    """
    consume_si_no : KW_SI_NO
    """
    global cuadruplo_inicial
    posicion_falso = pila_saltos.pop()
    cuadruplo_inicial[0] = Utils.Operador.getId('goto')
    lista_cuadruplos.append(cuadruplo_inicial)
    pila_saltos.append(len(lista_cuadruplos) - 1)
    cuadruplo_inicial = [None] * 4
    cuadruplo_goto_f = lista_cuadruplos[posicion_falso]
    cuadruplo_goto_f[3] = len(lista_cuadruplos)
    lista_cuadruplos[posicion_falso] = cuadruplo_goto_f


def p_bloque_est(p):
    """
    bloque_est : OP_LLAVE_IZQ estatuto_rec OP_LLAVE_DER
    """
    pass


def p_retorna(p):
    """
    retorna : KW_RETORNA expresion
    """
    global cuadruplo_inicial
    global tipo_funcion_actual
    tipo_expresion = pila_tipos.pop()
    if tipo_expresion != tipo_funcion_actual:
        raise TypeError(
            "Funcion de tipo " + tipo_funcion_actual + " no puede retornar un valor de tipo " + tipo_expresion)
    cuadruplo_inicial[0] = Utils.Operador.getId('return')
    cuadruplo_inicial[3] = pila_operandos.pop()
    lista_cuadruplos.append(cuadruplo_inicial)
    cuadruplo_inicial = [None] * 4


def p_var_cte(p):
    """
    var_cte : var_o_llamada_funcion
            | a_string
            | a_entero
            | a_flotante
            | cte_e_f_s
            | maneja_var_cte_defaults
    """


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
    valor_kw = None
    if p[1] == 'verdadero':
        valor_kw = 1
    elif p[1] == 'falso':
        valor_kw = 0
    elif p[1] == 'norte':
        valor_kw = 90
    elif p[1] == 'sur':
        valor_kw = 270
    elif p[1] == 'este':
        valor_kw = 0
    elif p[1] == 'oeste':
        valor_kw = 180
    elif p[1] == 'ancho':
        valor_kw = 800
    elif p[1] == 'alto':
        valor_kw = 600
    tipo = Utils.Tipo.Entero
    espacio_memoria = Memoria.Memoria.getInstance().generaEspacioConstantes(Utils.Tipo.Entero, valor_kw)
    genera_operando({"tipo": tipo, "valor": espacio_memoria})


def p_cte_e_f_s(p):
    """
    cte_e_f_s : consume_cte_entero
            | consume_cte_flotante
            | consume_cte_string
    """
    pass


def p_consume_flotante(p):
    """
    consume_cte_flotante : CTE_F
    """
    valor = Memoria.Memoria.getInstance().generaEspacioConstantes(Utils.Tipo.Flotante, p[1])
    genera_operando({"valor": valor, "tipo": Utils.Tipo.Flotante})


def p_consume_entero(p):
    """
    consume_cte_entero : CTE_E
    """
    valor = Memoria.Memoria.getInstance().generaEspacioConstantes(Utils.Tipo.Entero, p[1])
    genera_operando({"valor": valor, "tipo": Utils.Tipo.Entero})


def p_consume_string(p):
    """
    consume_cte_string : CTE_S
    """
    valor = Memoria.Memoria.getInstance().generaEspacioConstantes(Utils.Tipo.String, p[1])
    genera_operando({"valor": valor, "tipo": Utils.Tipo.String})


def p_var_o_llamada_funcion(p):
    """
    var_o_llamada_funcion : var_consume_id_var_cte acceso_variable_dimensionada
                        | ejec_funcion
    """
    pass


def p_var_consume_id_var_cte(p):
    """
    var_consume_id_var_cte : ID
    """
    global var_actual
    global contador_variable_dimensionada
    var = var_table.getVariable(p[1])
    var_actual = var
    genera_operando({"tipo": var.getTipo(), "valor": var.getEspacioMemoria()})


def p_acceso_variable_dimensionada(p):
    """
    acceso_variable_dimensionada : fondo_falso_dimension acceso_arreglo acceso_variable_dimensionada_rec
                | empty
    """
    global var_actual, contador_variable_dimensionada, pila_operandos
    # Generar cuadruplos de acceso
    if len(p) > 2:
        if Utils.DEBUGGING_MODE:
            print("Sacar fondo falso de pila_dimensiones")
        cuadruplo_acceso = [None] * 4
        # Generar cuadruplo final de acceso al arreglo
        cuadruplo_acceso[0] = Utils.Operador.getId('+')
        # Resultado de operaciones previas
        cuadruplo_acceso[1] = pila_operandos.pop()
        # La K es constante ya que nuestra indexacion siempre es de 0 a N
        cuadruplo_acceso[2] = Memoria.Memoria.getInstance().generaEspacioConstantes(Utils.Tipo.Entero, 0)
        # Limite superior del arreglo
        cuadruplo_acceso[3] = Memoria.Memoria.getInstance().generaEspacioTemporal(Utils.Tipo.Entero)
        pila_operandos.append(cuadruplo_acceso[3])

        cuadruplo_apuntador = [None] * 4
        dir_base = pila_dimensiones[-1][0].getEspacioMemoria()
        cuadruplo_apuntador[0] = Utils.Operador.getId('+')
        cuadruplo_apuntador[1] = pila_operandos.pop()
        # Cuadruplo con direccion base de la lista
        cuadruplo_apuntador[2] = Memoria.Memoria.getInstance().generaEspacioConstantes(Utils.Tipo.Entero, dir_base)
        cuadruplo_apuntador[3] = Memoria.Memoria.getInstance().generaEspacioTemporal(Utils.Tipo.Entero)
        pila_operandos.append([cuadruplo_apuntador[3]])
        pila_operadores.pop()
        lista_cuadruplos.append(cuadruplo_acceso)
        lista_cuadruplos.append(cuadruplo_apuntador)

        # Obtener variable dimensionada anterior, en caso de que la haya
        if len(pila_dimensiones) > 0:
            fondo = pila_dimensiones.pop()
            contador_variable_dimensionada = fondo[1]


def p_acceso_variable_dimensionada_rec(p):
    """
    acceso_variable_dimensionada_rec : acceso_arreglo acceso_variable_dimensionada_rec
                | empty
    """
    pass


def p_fondo_falso_dimension(p):
    """
    fondo_falso_dimension : empty
    """
    global pila_dimensiones
    global var_actual, contador_variable_dimensionada
    if Utils.DEBUGGING_MODE:
        print("Meter fondo falso a pila_dimensiones")
    pila_dimensiones.append([var_actual, contador_variable_dimensionada])
    contador_variable_dimensionada = 0
    pila_operadores.append("(")


def p_acceso_arreglo(p):
    """
    acceso_arreglo :  OP_CORCHETE_IZQ expresion OP_CORCHETE_DER
    """
    global pila_operandos
    global contador_variable_dimensionada
    global var_actual
    global pila_tipos
    lim_superior = pila_dimensiones[-1][0].getLimSuperior(contador_variable_dimensionada)
    if Utils.DEBUGGING_MODE:
        print(Utils.bcolors.buildInfoMessage("Chequeo de limites"))
        print(Utils.bcolors.buildInfoMessage(pila_dimensiones[-1][0].getNombre()))
        print(Utils.bcolors.buildInfoMessage(str(contador_variable_dimensionada)))
        print(Utils.bcolors.buildInfoMessage(str(lim_superior)))
        print(Utils.bcolors.buildInfoMessage("Cuadruplo:" + str(len(lista_cuadruplos))))
    dimension = pila_dimensiones[-1][0].getDimension(contador_variable_dimensionada)
    cuadruplo_verificacion = [None] * 4
    cuadruplo_verificacion[0] = Utils.Operador.getId('ver')
    cuadruplo_verificacion[1] = Memoria.Memoria.getInstance().generaEspacioConstantes(Utils.Tipo.Entero, 0)
    cuadruplo_verificacion[2] = Memoria.Memoria.getInstance().generaEspacioConstantes(Utils.Tipo.Entero, lim_superior)
    cuadruplo_verificacion[3] = pila_operandos[-1]
    lista_cuadruplos.append(cuadruplo_verificacion)
    if pila_dimensiones[-1][0].getCantidadDimensiones() - 1 != contador_variable_dimensionada:
        aux = pila_operandos.pop()
        temporal = Memoria.Memoria.getInstance().generaEspacioTemporal(Utils.Tipo.Entero)
        cuadruplo_dimension = [None] * 4
        cuadruplo_dimension[0] = Utils.Operador.getId('*')
        cuadruplo_dimension[1] = aux
        cuadruplo_dimension[2] = Memoria.Memoria.getInstance().generaEspacioConstantes(Utils.Tipo.Entero, dimension)
        cuadruplo_dimension[3] = temporal
        lista_cuadruplos.append(cuadruplo_dimension)
        pila_operandos.append(temporal)
    if contador_variable_dimensionada > 0:
        aux2 = pila_operandos.pop()
        aux1 = pila_operandos.pop()
        temporal = Memoria.Memoria.getInstance().generaEspacioTemporal(Utils.Tipo.Entero)
        cuadruplo_dimension = [None] * 4
        cuadruplo_dimension[0] = Utils.Operador.getId('+')
        cuadruplo_dimension[1] = aux1
        cuadruplo_dimension[2] = aux2
        cuadruplo_dimension[3] = temporal
        lista_cuadruplos.append(cuadruplo_dimension)
        pila_operandos.append(temporal)
    contador_variable_dimensionada += 1


def p_a_flotante(p):
    """
    a_flotante : KW_A_FLOTANTE OP_PARENTESIS_IZQ a_flotante2 OP_PARENTESIS_DER
    """
    pass


def p_a_flotante2(p):
    """
    a_flotante2 : expresion
    """
    global pila_tipos
    global cuadruplo_inicial
    tipo = pila_tipos.pop()
    if tipo == Utils.Tipo.Entero or tipo == Utils.Tipo.String:
        pila_tipos.append(Utils.Tipo.Flotante)
        resultado = pila_operandos.pop()
        cuadruplo_inicial[0] = Utils.Operador.getId('a_flotante')
        cuadruplo_inicial[1] = resultado
        cuadruplo_inicial[3] = Memoria.Memoria.getInstance().generaEspacioTemporal(Utils.Tipo.Flotante)
        lista_cuadruplos.append(cuadruplo_inicial)
        pila_operandos.append(cuadruplo_inicial[3])
        cuadruplo_inicial = [None] * 4
    else:
        warnings.warn("La expresion ya tiene como tipo de resultado un flotante. Seguro que quieres convertirlo?")


def p_reiniciar(p):
    """
    reiniciar : KW_REINICIAR OP_PARENTESIS_IZQ OP_PARENTESIS_DER
    """
    global cuadruplo_inicial
    cuadruplo_inicial[0] = Utils.Operador.getId('reiniciar')
    lista_cuadruplos.append(cuadruplo_inicial)
    cuadruplo_inicial = [None] * 4


def p_input(p):
    """
    input : KW_INPUT OP_PARENTESIS_IZQ consume_id_input input2 OP_PARENTESIS_DER
    """
    pass


def p_input2(p):
    """
    input2 : OP_COMA consume_id_input input2
            | empty
    """
    pass


def p_consume_id_input(p):
    """
    consume_id_input : ID
    """
    var = var_table.getVariable(p[1])
    global cuadruplo_inicial
    cuadruplo_inicial[0] = Utils.Operador.getId('input')
    cuadruplo_inicial[1] = var.getTipo().value
    cuadruplo_inicial[3] = var.getEspacioMemoria()
    lista_cuadruplos.append(cuadruplo_inicial)
    cuadruplo_inicial = [None] * 4


def p_output(p):
    """
    output : KW_OUTPUT OP_PARENTESIS_IZQ valores_a_imprimir OP_PARENTESIS_DER
    """
    pass


def p_valores_a_imprimir(p):
    """
    valores_a_imprimir : expresion

    """
    pila_tipos.pop()
    resultado = pila_operandos.pop()
    global cuadruplo_inicial
    cuadruplo_inicial[0] = Utils.Operador.getId('output')
    cuadruplo_inicial[3] = resultado
    lista_cuadruplos.append(cuadruplo_inicial)
    cuadruplo_inicial = [None] * 4


def p_salta_a(p):
    """
    salta_a : KW_SALTA_A OP_PARENTESIS_IZQ expresion OP_COMA expresion OP_PARENTESIS_DER
    """
    tipo2 = pila_tipos.pop()
    tipo1 = pila_tipos.pop()
    if tipo1 == Utils.Tipo.String or tipo2 == Utils.Tipo.String:
        raise TypeError('Solo puedes caminar unidades enteras')
    operando2 = pila_operandos.pop()
    operando1 = pila_operandos.pop()
    global cuadruplo_inicial
    cuadruplo_inicial[0] = Utils.Operador.getId('salta_a')
    cuadruplo_inicial[1] = operando1
    cuadruplo_inicial[2] = operando2
    lista_cuadruplos.append(cuadruplo_inicial)
    cuadruplo_inicial = [None] * 4


def p_error(p):
    print("\nSyntax error with token of type " + p.type + " with value " + p.value + " in line " + str(p.lineno))


def genera_operando(operando_a_generar):
    global pila_operandos
    global pila_tipos

    pila_tipos.append(operando_a_generar["tipo"])
    pila_operandos.append(operando_a_generar["valor"])


def parse(source):
    with open('../Compis/source.txt', 'r') as content_file:
        content = content_file.read()
    parser = yacc.yacc()
    data = '''
        entero matriz_global[3][4];
        inicio funcion entero main(){
            entero i;
            entero aa[3];
            entero j;
            i = 0;
            mientras(i < 3){
                aa[i] = (i + 1) * 5;
                j = 0;
                mientras(j < 4){
                    matriz_global[i][j] = (j + 1) + (i * 4);
                    output(j);
                    j = j + 1;
                };
                i = i + 1;
            };
        }
    '''
    matrix_test = '''
        entero matriz_global[3][4][3];

        funcion entero fibonacci_rec(entero num){
            si(num == 1 || num == 2){
                retorna 1;
            };
            retorna fibonacci_rec(num - 1) + fibonacci_rec(num - 2);
        }

        funcion entero factorial_rec(entero num){
            output(num);
            output(num == 1);
            si(num == 1){
                retorna 1;
            };
            retorna num * factorial_rec(num - 1);
        }

        funcion entero factorial_iter(entero num){
            entero x;
            x = 1;
            mientras(num > 0){
                x = x * num;
                num = num - 1;
            };
            retorna x;
        }

        funcion entero fibonacci_iter(){
            entero num_uno, num_dos, num_tres;
            entero arreglo_flotante[2][5];
            entero contador;
            arreglo_flotante[1][3] = arreglo_flotante[1][1];
            num_uno = 1;
            num_dos = 1;
            mientras(contador < 7){
                num_uno = num_dos;
                num_dos = num_tres;
                num_tres = num_uno + num_dos;
                contador = contador + 1;
            };
            retorna num_tres;
        }

        inicio funcion entero main(){
            entero i;
            entero arreglo[3];
            entero j;
            entero k;
            entero contador;
            contador = 0;
            i = 0;
            mientras(i < 3){
                j = 0;
                mientras(j < 4){
                    k = 0;
                    mientras(k < 3){
                        contador = contador + 1;
                        matriz_global[i][j][k] = contador;
                        k = k + 1;
                    };
                    j = j + 1;
                };
                i = i + 1;
            };


            output(factorial_rec(5));
            output(0);
            output(factorial_iter(5));
            output(fibonacci_iter());
        }
    '''

    recursive_test = """
        funcion entero factorial_rec(entero num){
            entero temp;
            si(num == 1){
                retorna 1;
            };
            temp = num * factorial_rec(num - 1);
            retorna temp;
        }
        inicio funcion entero main(){
            output(factorial_rec(4));
        }
    """

    recursive_fact = """
        entero arreglo_find[5];

        funcion entero factorial_recursivo(entero num){
            entero temp;
            si(num == 1){
                retorna 1;
            };
            temp = num*factorial_recursivo(num-1);
            retorna temp;
        }
        funcion entero fibonacci_rec(entero num){
            si(num == 1 || num == 2){
                retorna 1;
            };
            retorna fibonacci_rec(num - 1) + fibonacci_rec(num - 2);
        }

        funcion entero camina_cuadrados_rec(entero x){
            entero y;
            si (x == 1){
                retorna 1;
            };
            y = camina_cuadrados_rec(x - 1) * 2;
            camina(y);
            gira(-90);
            retorna y;
        }

        funcion entero factorial_iter(entero num){
            entero x;
            x = 1;
            mientras(num > 0){
                x = x * num;
                num = num - 1;
            };
            retorna x;
        }

        funcion entero fibonacci_iter(){
            entero num_uno, num_dos, num_tres;
            entero contador;
            num_uno = 1;
            num_dos = 1;
            mientras(contador < 6){
                camina(contador * 5);
                num_uno = num_dos;
                num_dos = num_tres;
                num_tres = num_uno + num_dos;
                contador = contador + 1;
            };
            retorna num_tres;
        }

        funcion camina_cuadrados_it(entero x){
            entero contador;
            contador = 0;
            mientras(contador < x){
                camina(-contador * 2);
                gira(90);
                contador = contador + 1;
            };
        }

        inicio funcion entero main(){
            entero x;
            entero y;
            x = 6;
            y = 4;
            output(fibonacci_iter());
            output(fibonacci_rec(y));

            output(factorial_recursivo(x));
            output(factorial_iter(x));

            camina_cuadrados_rec(10);
            camina_cuadrados_it(50);
        }
    """
    parser.parse(recursive_fact, debug=0)
    return lista_cuadruplos


# checar que las funciones esten definidas
log = logging.getLogger("parserlog.log")
