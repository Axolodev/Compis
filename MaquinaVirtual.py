from __future__ import print_function
import Utils
import TablaVariables
import Memoria

class MaquinaVirtual:
    def __init__(self, lista_cuadruplos):
        self.__lista_cuadruplos = lista_cuadruplos

    def ejecutar(self):
        if Utils.DEBUGGING_MODE:
            print("----------------------------")
            print("Ejecucion:")
        goto_it = Utils.Operador.getId('goto')
        sum_id = Utils.Operador.getId('+')
        assign_id = Utils.Operador.getId('=')

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

        i = 0
        while i < len(self.__lista_cuadruplos):
            operator = self.__lista_cuadruplos[i][0]
            if Utils.DEBUGGING_MODE:
                print(i, self.__lista_cuadruplos[i])

            if operator == goto_it:
                if Utils.DEBUGGING_MODE:
                    print("Goto", self.__lista_cuadruplos[i][3])
                i = self.__lista_cuadruplos[i][3] - 1

            if operator == sum_id:
                pass

            if operator == assign_id:
                dir1 = self.__lista_cuadruplos[i][1]
                dir2 = self.__lista_cuadruplos[i][3]
                valor = Memoria.Memoria.getInstance().getValorParaEspacio(dir1)
                Memoria.Memoria.getInstance().setValorParaEspacio(dir2, valor)

            i += 1

        if Utils.DEBUGGING_MODE:
            Memoria.Memoria.getInstance().printVariablesActuales()
