from __future__ import print_function

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
                    Memoria.Memoria.getInstance().getValorParaEspacio(self.__lista_cuadruplos[i][3]))

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

            elif operator == id_salta_a:
                Interfaz.Interfaz.getInstance().salta(
                    Memoria.Memoria.getInstance().getValorParaEspacio(self.__lista_cuadruplos[i][1]),
                    Memoria.Memoria.getInstance().getValorParaEspacio(self.__lista_cuadruplos[i][2]))

            elif operator == id_reiniciar:
                Interfaz.Interfaz.getInstance().reinicia()
            i += 1

        if Utils.DEBUGGING_MODE:
            Memoria.Memoria.getInstance().printVariablesActuales()
