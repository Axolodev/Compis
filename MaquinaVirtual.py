from __future__ import print_function
import Utils
import TablaVariables
import TablaFunciones
import Memoria


class MaquinaVirtual:
    def __init__(self, lista_cuadruplos):
        self.__lista_cuadruplos = lista_cuadruplos
        self.__pila_ejecucion = []
        self.__cantidades_variables_actuales = []

    def ejecutar(self):
        if Utils.DEBUGGING_MODE:
            print("----------------------------")
            print("Ejecucion:")
        id_goto = Utils.Operador.getId('goto')
        id_sum = Utils.Operador.getId('+')
        id_assign = Utils.Operador.getId('=')
        id_ret = Utils.Operador.getId('ret')
        id_era = Utils.Operador.getId('era')
        id_gosub = Utils.Operador.getId('gosub')

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

        lista_variables_main = [v.getTipo().value for v in
                                TablaFunciones.TablaFunciones.getInstance().getListaVariablesDeMain().values()]
        lista_variables_main = [[x == 0, x == 1, x == 2] for x in lista_variables_main]
        lista_variables_main = [sum(x) for x in zip(*lista_variables_main)]
        Memoria.Memoria.getInstance().darDeAltaLocales(lista_variables_main)
        self.__cantidades_variables_actuales = lista_variables_main

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
                pass

            elif operator == id_assign:
                dir1 = self.__lista_cuadruplos[i][1]
                dir2 = self.__lista_cuadruplos[i][3]
                valor = Memoria.Memoria.getInstance().getValorParaEspacio(dir1)
                Memoria.Memoria.getInstance().setValorParaEspacio(dir2, valor)

            elif operator == id_ret:
                Memoria.Memoria.getInstance().liberarLocales(self.__cantidades_variables_actuales)
                if len(self.__pila_ejecucion) > 0:
                    funcion_padre = self.__pila_ejecucion.pop()
                    i = funcion_padre[0]
                    self.__cantidades_variables_actuales = funcion_padre[1]


            elif operator == id_era:
                scope = TablaFunciones.TablaFunciones.getInstance().getFuncion(self.__lista_cuadruplos[i][1]).getScope()
                variables = TablaVariables.TablaVariables.getInstance().consigueVariablesPara(scope)
                print("variables locales de funciones: ")
                print(variables)
                lista_variables_funcion = [v.getTipo().value for v in
                                       variables.values()]
                lista_variables_funcion = [[x == 0, x == 1, x == 2] for x in lista_variables_funcion]
                lista_variables_funcion = [sum(x) for x in zip(*lista_variables_funcion)]
                Memoria.Memoria.getInstance().darDeAltaLocales(lista_variables_funcion)
                self.__cantidades_variables_actuales = lista_variables_funcion

            elif operator == id_gosub:
                self.__pila_ejecucion.append([i, self.__cantidades_variables_actuales, []])
                i = TablaFunciones.TablaFunciones.getInstance().getFuncion(self.__lista_cuadruplos[i][1]).getCuadruplo()-1




            i += 1

        if Utils.DEBUGGING_MODE:
            Memoria.Memoria.getInstance().printVariablesActuales()
