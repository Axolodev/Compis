from __future__ import print_function

import sys
from types import IntType, FloatType, StringType

import Memoria
import TablaFunciones
import TablaVariables
import Utils
import scanner as scanner


class MaquinaVirtual:
    def __init__(self, _input):
        lista_cuadruplos = scanner.parse(_input)
        self.__lista_cuadruplos = lista_cuadruplos
        self.__pila_ejecucion = []
        self.__cantidades_variables_locales_actuales = []

    def ejecutar(self):
        import Interfaz
        if Utils.DEBUGGING_MODE:
            print("----------------------------")
            print("Ejecucion:")
        id_goto = Utils.Operador.getId('goto')
        id_sum = Utils.Operador.getId('+')
        id_assign = Utils.Operador.getId('=')
        id_ret = Utils.Operador.getId('ret')
        id_era = Utils.Operador.getId('era')
        id_gosub = Utils.Operador.getId('gosub')
        id_return = Utils.Operador.getId('return')
        id_camina = Utils.Operador.getId('camina')
        id_gira = Utils.Operador.getId('gira')
        id_mira = Utils.Operador.getId('mira')
        id_salta_a = Utils.Operador.getId('salta_a')
        id_reiniciar = Utils.Operador.getId('reiniciar')
        id_input = Utils.Operador.getId('input')
        id_output = Utils.Operador.getId('output')
        id_product = Utils.Operador.getId('*')
        id_substract = Utils.Operador.getId('-')
        id_division = Utils.Operador.getId('/')
        id_mod = Utils.Operador.getId('%')
        id_and = Utils.Operador.getId('&&')
        id_or = Utils.Operador.getId('||')
        id_lt = Utils.Operador.getId('<')
        id_gt = Utils.Operador.getId('>')
        id_loet = Utils.Operador.getId('<=')
        id_goet = Utils.Operador.getId('>=')
        id_equals = Utils.Operador.getId('==')
        id_different = Utils.Operador.getId('!=')
        id_goto_f = Utils.Operador.getId('gotoF')
        id_goto_t = Utils.Operador.getId('gotoT')
        id_a_entero = Utils.Operador.getId('a_entero')
        id_a_flotante = Utils.Operador.getId('a_flotante')
        id_a_string = Utils.Operador.getId('a_string')

        offset_locales = [0, 0, 0]

        lista_globales = TablaVariables.TablaVariables.getInstance().consigueVariablesPara(0)

        Memoria.Memoria.getInstance().generaEspaciosParaGlobales(lista_globales)
        # Suponer que las constantes ya estan cargadas en el diccionario de constantes.
        Memoria.Memoria.getInstance().generaEspaciosParaConstantes()

        if Utils.DEBUGGING_MODE:
            print("Globales:")
            for k, v in lista_globales.items():
                print(v)

        if Utils.DEBUGGING_MODE:
            Memoria.Memoria.getInstance().printVariablesActuales()
        lista_variables_funcion = []
        lista_variables_main = [v.getTipo().value for v in
                                TablaFunciones.TablaFunciones.getInstance().getListaVariablesDeMain().values()]
        lista_variables_main = [[x == 0, x == 1, x == 2] for x in lista_variables_main]
        lista_variables_main = [sum(x) for x in zip(*lista_variables_main)]
        Memoria.Memoria.getInstance().darDeAltaLocales(lista_variables_main)
        self.__cantidades_variables_locales_actuales = lista_variables_main

        i = 0
        while i < len(self.__lista_cuadruplos):
            operator = self.__lista_cuadruplos[i][0]
            if Utils.DEBUGGING_MODE:
                print(i, self.__lista_cuadruplos[i])

            if operator == id_goto:
                if Utils.DEBUGGING_MODE:
                    print("Goto", self.__lista_cuadruplos[i][3])
                i = self.__lista_cuadruplos[i][3] - 1

            elif operator == id_sum:
                dir1 = self.__lista_cuadruplos[i][1]
                dir2 = self.__lista_cuadruplos[i][2]
                valor1 = Memoria.Memoria.getInstance().getValorParaEspacio(dir1, offset_locales)
                valor2 = Memoria.Memoria.getInstance().getValorParaEspacio(dir2, offset_locales)
                dir_resultado = self.__lista_cuadruplos[i][3]
                Memoria.Memoria.getInstance().setValorParaEspacio(dir_resultado, valor1 + valor2, offset_locales)

            elif operator == id_assign:
                dir1 = self.__lista_cuadruplos[i][1]
                dir2 = self.__lista_cuadruplos[i][3]
                valor = Memoria.Memoria.getInstance().getValorParaEspacio(dir1,
                                                                          offset_locales)
                if Utils.DEBUGGING_MODE:
                    print(self.__lista_cuadruplos[i])
                Memoria.Memoria.getInstance().setValorParaEspacio(dir2, valor, offset_locales)

            elif operator == id_ret:
                Memoria.Memoria.getInstance().liberarLocales(self.__cantidades_variables_locales_actuales)
                offset_locales = [x - y for x, y in zip(offset_locales, self.__cantidades_variables_locales_actuales)]
                if len(self.__pila_ejecucion) > 0:
                    funcion_padre = self.__pila_ejecucion.pop()
                    i = funcion_padre[0]
                    self.__cantidades_variables_locales_actuales = funcion_padre[1]

            elif operator == id_era:
                scope = TablaFunciones.TablaFunciones.getInstance().getFuncion(self.__lista_cuadruplos[i][1]).getScope()
                variables = TablaVariables.TablaVariables.getInstance().consigueVariablesPara(scope)
                if Utils.DEBUGGING_MODE:
                    print("Variables de scope:", scope)
                    print(variables)
                    print("variables locales de funciones: ")
                    print(variables)
                lista_variables_funcion = [v.getTipo().value for v in
                                           variables.values()]
                lista_variables_funcion = [[x == 0, x == 1, x == 2] for x in lista_variables_funcion]
                lista_variables_funcion = [sum(x) for x in zip(*lista_variables_funcion)]
                Memoria.Memoria.getInstance().darDeAltaLocales(lista_variables_funcion)

            elif operator == id_return:
                # Obtener el nombre de la funcion actual, este se encuentra en la pila de ejecucion. Se inserta en gosub
                nombre_funcion = self.__pila_ejecucion[len(self.__pila_ejecucion) - 1][3]
                # Obtener el espacio de memoria de la funcion utilizando su nombre. El espacio es una variable global
                espacio_de_funcion = TablaVariables.TablaVariables.getInstance().getVariable(
                    nombre_funcion).getEspacioMemoria()
                # Obtener el valor resultante de la expresion evaluada en el return
                valor = Memoria.Memoria.getInstance().getValorParaEspacio(self.__lista_cuadruplos[i][3],
                                                                          offset_locales)
                if Utils.DEBUGGING_MODE:
                    print("Valor a retornar:", valor)
                # Asignar el valor obtenido en la instruccion anterior a el espacio de la variable de la funcion.
                Memoria.Memoria.getInstance().setValorParaEspacio(espacio_de_funcion, valor, offset_locales)
                # Encontrar el ret correspondiente de la funcion
                while self.__lista_cuadruplos[i + 1][0] != id_ret:
                    i += 1

            elif operator == id_gosub:
                # Obtener el nombre de la funcion que se ejecutara
                nombre_funcion = self.__lista_cuadruplos[i][1]
                # Congelar el espacio actual de ejecucion
                self.__pila_ejecucion.append([i, self.__cantidades_variables_locales_actuales, [], nombre_funcion])
                # Obtener el primer cuadruplo de la funcion que se debe ejecutar
                i = TablaFunciones.TablaFunciones.getInstance().getFuncion(nombre_funcion).getCuadruplo() - 1
                # Obtener nuevo offset de locales
                offset_locales = [x + y for x, y in zip(offset_locales, self.__cantidades_variables_locales_actuales)]
                self.__cantidades_variables_locales_actuales = lista_variables_funcion
                Memoria.Memoria.getInstance().congelarTemporalesParaNuevaFuncion()

            elif operator == id_camina:
                Interfaz.Interfaz.getInstance().camina(
                    Memoria.Memoria.getInstance().getValorParaEspacio(self.__lista_cuadruplos[i][3], offset_locales))

            elif operator == id_mira:
                Interfaz.Interfaz.getInstance().mira(
                    Memoria.Memoria.getInstance().getValorParaEspacio(self.__lista_cuadruplos[i][3]))

            elif operator == id_gira:
                Interfaz.Interfaz.getInstance().gira(
                    Memoria.Memoria.getInstance().getValorParaEspacio(self.__lista_cuadruplos[i][3]))

            elif operator == id_salta_a:
                Interfaz.Interfaz.getInstance().salta(
                    Memoria.Memoria.getInstance().getValorParaEspacio(self.__lista_cuadruplos[i][1]),
                    Memoria.Memoria.getInstance().getValorParaEspacio(self.__lista_cuadruplos[i][2]))

            elif operator == id_reiniciar:
                Interfaz.Interfaz.getInstance().reinicia()

            elif operator == id_product:
                dir1 = self.__lista_cuadruplos[i][1]
                dir2 = self.__lista_cuadruplos[i][2]
                dir_r = self.__lista_cuadruplos[i][3]
                valor1 = Memoria.Memoria.getInstance().getValorParaEspacio(dir1)
                valor2 = Memoria.Memoria.getInstance().getValorParaEspacio(dir2)
                valor_r = valor1 * valor2
                Memoria.Memoria.getInstance().setValorParaEspacio(dir_r, valor_r, offset_locales)

            elif operator == id_mod:
                dir1 = self.__lista_cuadruplos[i][1]
                dir2 = self.__lista_cuadruplos[i][2]
                dir_r = self.__lista_cuadruplos[i][3]
                valor1 = Memoria.Memoria.getInstance().getValorParaEspacio(dir1)
                valor2 = Memoria.Memoria.getInstance().getValorParaEspacio(dir2)
                if valor2 == 0 or valor2 == 0.0:
                    raise ZeroDivisionException('Intentaste hacer residuo con 0!')
                valor_r = valor1 % valor2
                Memoria.Memoria.getInstance().setValorParaEspacio(dir_r, valor_r, offset_locales)

            elif operator == id_division:
                dir1 = self.__lista_cuadruplos[i][1]
                dir2 = self.__lista_cuadruplos[i][2]
                dir_r = self.__lista_cuadruplos[i][3]
                valor1 = Memoria.Memoria.getInstance().getValorParaEspacio(dir1)
                valor2 = Memoria.Memoria.getInstance().getValorParaEspacio(dir2)
                if valor2 == 0 or valor2 == 0.0:
                    raise ZeroDivisionException('Intentaste dividir entre 0!')
                valor_r = valor1 / valor2
                Memoria.Memoria.getInstance().setValorParaEspacio(dir_r, valor_r, offset_locales)

            elif operator == id_substract:
                dir1 = self.__lista_cuadruplos[i][1]
                dir_r = self.__lista_cuadruplos[i][3]
                valor1 = Memoria.Memoria.getInstance().getValorParaEspacio(dir1)
                if self.__lista_cuadruplos[i][2] is None:
                    valor_r = - valor1
                else:
                    dir2 = self.__lista_cuadruplos[i][2]
                    valor2 = Memoria.Memoria.getInstance().getValorParaEspacio(dir2)
                    valor_r = valor1 - valor2
                Memoria.Memoria.getInstance().setValorParaEspacio(dir_r, valor_r, offset_locales)

            elif operator == id_lt:
                dir1 = self.__lista_cuadruplos[i][1]
                dir2 = self.__lista_cuadruplos[i][2]
                dir_r = self.__lista_cuadruplos[i][3]
                valor1 = Memoria.Memoria.getInstance().getValorParaEspacio(dir1)
                valor2 = Memoria.Memoria.getInstance().getValorParaEspacio(dir2)
                if valor1 < valor2:
                    valor_r = 1
                else:
                    valor_r = 0
                Memoria.Memoria.getInstance().setValorParaEspacio(dir_r, valor_r, offset_locales)

            elif operator == id_gt:
                dir1 = self.__lista_cuadruplos[i][1]
                dir2 = self.__lista_cuadruplos[i][2]
                dir_r = self.__lista_cuadruplos[i][3]
                valor1 = Memoria.Memoria.getInstance().getValorParaEspacio(dir1)
                valor2 = Memoria.Memoria.getInstance().getValorParaEspacio(dir2)
                if valor1 > valor2:
                    valor_r = 1
                else:
                    valor_r = 0
                Memoria.Memoria.getInstance().setValorParaEspacio(dir_r, valor_r, offset_locales)

            elif operator == id_loet:
                dir1 = self.__lista_cuadruplos[i][1]
                dir2 = self.__lista_cuadruplos[i][2]
                dir_r = self.__lista_cuadruplos[i][3]
                valor1 = Memoria.Memoria.getInstance().getValorParaEspacio(dir1)
                valor2 = Memoria.Memoria.getInstance().getValorParaEspacio(dir2)
                if valor1 <= valor2:
                    valor_r = 1
                else:
                    valor_r = 0
                Memoria.Memoria.getInstance().setValorParaEspacio(dir_r, valor_r, offset_locales)

            elif operator == id_goet:
                dir1 = self.__lista_cuadruplos[i][1]
                dir2 = self.__lista_cuadruplos[i][2]
                dir_r = self.__lista_cuadruplos[i][3]
                valor1 = Memoria.Memoria.getInstance().getValorParaEspacio(dir1)
                valor2 = Memoria.Memoria.getInstance().getValorParaEspacio(dir2)
                if valor1 >= valor2:
                    valor_r = 1
                else:
                    valor_r = 0
                Memoria.Memoria.getInstance().setValorParaEspacio(dir_r, valor_r, offset_locales)

            elif operator == id_equals:
                dir1 = self.__lista_cuadruplos[i][1]
                dir2 = self.__lista_cuadruplos[i][2]
                dir_r = self.__lista_cuadruplos[i][3]
                valor1 = Memoria.Memoria.getInstance().getValorParaEspacio(dir1)
                valor2 = Memoria.Memoria.getInstance().getValorParaEspacio(dir2)
                if valor1 == valor2:
                    valor_r = 1
                else:
                    valor_r = 0
                Memoria.Memoria.getInstance().setValorParaEspacio(dir_r, valor_r, offset_locales)

            elif operator == id_and:
                dir1 = self.__lista_cuadruplos[i][1]
                dir2 = self.__lista_cuadruplos[i][2]
                dir_r = self.__lista_cuadruplos[i][3]
                valor1 = Memoria.Memoria.getInstance().getValorParaEspacio(dir1)
                valor2 = Memoria.Memoria.getInstance().getValorParaEspacio(dir2)
                if valor1 != 0 and valor2 != 0:
                    valor_r = 1
                else:
                    valor_r = 0
                Memoria.Memoria.getInstance().setValorParaEspacio(dir_r, valor_r, offset_locales)

            elif operator == id_or:
                dir1 = self.__lista_cuadruplos[i][1]
                dir2 = self.__lista_cuadruplos[i][2]
                dir_r = self.__lista_cuadruplos[i][3]
                valor1 = Memoria.Memoria.getInstance().getValorParaEspacio(dir1)
                valor2 = Memoria.Memoria.getInstance().getValorParaEspacio(dir2)
                if valor1 != 0 or valor2 != 0:
                    valor_r = 1
                else:
                    valor_r = 0
                Memoria.Memoria.getInstance().setValorParaEspacio(dir_r, valor_r, offset_locales)

            elif operator == id_different:
                dir1 = self.__lista_cuadruplos[i][1]
                dir2 = self.__lista_cuadruplos[i][2]
                dir_r = self.__lista_cuadruplos[i][3]
                valor1 = Memoria.Memoria.getInstance().getValorParaEspacio(dir1)
                valor2 = Memoria.Memoria.getInstance().getValorParaEspacio(dir2)
                if valor1 != valor2:
                    valor_r = 1
                else:
                    valor_r = 0
                Memoria.Memoria.getInstance().setValorParaEspacio(dir_r, valor_r, offset_locales)

            elif operator == id_goto_f:
                dir1 = self.__lista_cuadruplos[i][1]
                valor1 = Memoria.Memoria.getInstance().getValorParaEspacio(dir1)
                if valor1 == 0:
                    i = self.__lista_cuadruplos[i][3] - 1

            elif operator == id_goto_t:
                dir1 = self.__lista_cuadruplos[i][1]
                valor1 = Memoria.Memoria.getInstance().getValorParaEspacio(dir1)
                if valor1 != 0:
                    i = self.__lista_cuadruplos[i][3] - 1

            elif operator == id_input:

                data = Interfaz.Interfaz.getInstance().asigna(self.__lista_cuadruplos[i][1])
                if data is not None:
                    Memoria.Memoria.getInstance().setValorParaEspacio(self.__lista_cuadruplos[i][3], data,
                                                                      offset_locales)
                '''
                data = input("Escribe valor de variable : " + str(self.__lista_cuadruplos[i][1]) + "\n")
                print("------------------------------------------------------------------")
                if type(data) is IntType and self.__lista_cuadruplos[i][1].value == 0:
                    Memoria.Memoria.getInstance().setValorParaEspacio(self.__lista_cuadruplos[i][3], data,
                                                                      offset_locales)
                elif type(data) is FloatType and self.__lista_cuadruplos[i][1].value == 1:
                    Memoria.Memoria.getInstance().setValorParaEspacio(self.__lista_cuadruplos[i][3], data,
                                                                      offset_locales)
                elif type(data) is StringType and self.__lista_cuadruplos[i][1].value == 2:
                    Memoria.Memoria.getInstance().setValorParaEspacio(self.__lista_cuadruplos[i][3], data,
                                                                      offset_locales)
                else:
                    raise TypeError('Tipo ingresado no corresponde a tipo declarado')

                '''

            elif operator == id_output:
                Interfaz.Interfaz.getInstance().muestra(Memoria.Memoria.getInstance().
                                                        getValorParaEspacio(self.__lista_cuadruplos[i][3]))

            elif operator == id_a_entero:
                var = Memoria.Memoria.getInstance().getValorParaEspacio(self.__lista_cuadruplos[i][1], offset_locales)
                Memoria.Memoria.getInstance().setValorParaEspacio(self.__lista_cuadruplos[i][3], int(var),
                                                                  offset_locales)

            elif operator == id_a_flotante:
                var = Memoria.Memoria.getInstance().getValorParaEspacio(self.__lista_cuadruplos[i][1], offset_locales)
                Memoria.Memoria.getInstance().setValorParaEspacio(self.__lista_cuadruplos[i][3], float(var),
                                                                  offset_locales)
            elif operator == id_a_string:
                var = Memoria.Memoria.getInstance().getValorParaEspacio(self.__lista_cuadruplos[i][1], offset_locales)
                Memoria.Memoria.getInstance().setValorParaEspacio(self.__lista_cuadruplos[i][3], str(var),
                                                                  offset_locales)

            i += 1

        if Utils.DEBUGGING_MODE:
            Memoria.Memoria.getInstance().printVariablesActuales()
