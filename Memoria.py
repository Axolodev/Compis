from __future__ import print_function
import Utils
import operator


class Memoria:
    OFFSET_INICIO_GLOBALES = 1000

    ESPACIO_GLOBALES = 1000
    OFFSET_ENTEROS_GLOBALES = OFFSET_INICIO_GLOBALES
    OFFSET_FLOTANTES_GLOBALES = OFFSET_ENTEROS_GLOBALES + ESPACIO_GLOBALES
    OFFSET_STRINGS_GLOBALES = OFFSET_FLOTANTES_GLOBALES + ESPACIO_GLOBALES

    ESPACIO_TEMPORALES = 1000
    OFFSET_ENTEROS_TEMPORALES = OFFSET_STRINGS_GLOBALES + ESPACIO_GLOBALES
    OFFSET_FLOTANTES_TEMPORALES = OFFSET_ENTEROS_TEMPORALES + ESPACIO_TEMPORALES
    OFFSET_STRINGS_TEMPORALES = OFFSET_FLOTANTES_TEMPORALES + ESPACIO_TEMPORALES

    ESPACIO_LOCALES = 1000
    OFFSET_ENTEROS_LOCALES = OFFSET_STRINGS_TEMPORALES + ESPACIO_TEMPORALES
    OFFSET_FLOTANTES_LOCALES = OFFSET_ENTEROS_LOCALES + ESPACIO_LOCALES
    OFFSET_STRINGS_LOCALES = OFFSET_FLOTANTES_LOCALES + ESPACIO_LOCALES

    ESPACIO_CONSTANTES = 1000
    OFFSET_ENTEROS_CONSTANTES = OFFSET_STRINGS_LOCALES + ESPACIO_LOCALES
    OFFSET_FLOTANTES_CONSTANTES = OFFSET_ENTEROS_CONSTANTES + ESPACIO_CONSTANTES
    OFFSET_STRINGS_CONSTANTES = OFFSET_FLOTANTES_CONSTANTES + ESPACIO_CONSTANTES

    class __Memoria:
        def __init__(self):
            self.__bloque_global = [[], [], []]
            self.__bloque_temporal = [[], [], []]
            self.__bloque_local = [[], [], []]
            self.__bloque_constantes_ejecucion = [[], [], []]
            self.__bloque_constantes_compilacion = {}
            self.__contadores_globales = [0, 0, 0]
            self.__contadores_temporales = [0, 0, 0]
            self.__contadores_locales = [0, 0, 0]
            self.__contadores_constantes = [0, 0, 0]
            self.__pila_offsets_temporales = []
            self.__offsets_temporales = [0, 0, 0]

        def crear_o_buscar_constante(self, constante):
            if constante not in self.__bloque_constantes_compilacion:
                self.__bloque_constantes_compilacion.add(constante)
            return constante

        def generaEspacioConstantes(self, tipo, valor):
            llave_de_constante = str(tipo.value) + "_" + str(valor)
            if llave_de_constante not in self.__bloque_constantes_compilacion:
                espacio_de_memoria = Memoria.OFFSET_ENTEROS_CONSTANTES + tipo.value * Memoria.ESPACIO_CONSTANTES + \
                                     self.__contadores_constantes[tipo.value]
                self.__bloque_constantes_compilacion.update({llave_de_constante: espacio_de_memoria})
                self.__contadores_constantes[tipo.value] += 1
            return self.__bloque_constantes_compilacion[llave_de_constante]

        def generaEspacioVaraiablesLocales(self, tipo):
            if Utils.DEBUGGING_MODE:
                print(tipo)
                print("Contadores locales", self.__contadores_locales)
            espacio = Memoria.OFFSET_ENTEROS_LOCALES + self.__contadores_locales[
                tipo.value] + Memoria.ESPACIO_LOCALES * tipo.value
            self.__contadores_locales[tipo.value] += 1
            if Utils.DEBUGGING_MODE:
                print("Espacio:", espacio, "\n____________________________")
            return espacio

        def generaEspacioVaraiablesGlobales(self, tipo):
            espacio = Memoria.OFFSET_ENTEROS_GLOBALES + self.__contadores_globales[
                tipo.value] + Memoria.ESPACIO_GLOBALES * tipo.value
            self.__contadores_globales[tipo.value] += 1
            if Utils.DEBUGGING_MODE:
                print("Espacio:", espacio, "\n____________________________")
            return espacio

        def generaEspacioTemporal(self, tipo):
            if Utils.DEBUGGING_MODE:
                print(tipo)
                print("Contadores locales", self.__contadores_locales)
            espacio = Memoria.OFFSET_ENTEROS_TEMPORALES + self.__contadores_temporales[
                tipo.value] + Memoria.ESPACIO_TEMPORALES * tipo.value
            self.__contadores_temporales[tipo.value] += 1
            if Utils.DEBUGGING_MODE:
                print("Espacio:", espacio, "\n____________________________")
            return espacio

        def generaEspacioVariable(self, scope, tipo):
            if int(scope) != 0:
                return self.generaEspacioVaraiablesLocales(tipo)
            return self.generaEspacioVaraiablesGlobales(tipo)

        def reseteaEspacios(self):
            self.__contadores_locales = [0, 0, 0]
            self.__contadores_temporales = [0, 0, 0]

        def generaEspaciosParaGlobales(self, lista_globales):
            for k, gl in lista_globales.items():
                self.__bloque_global[gl.getTipo().value].insert(0, Utils.Tipo.getDefault(gl.getTipo()))

        def printVariablesActuales(self):
            print("Globales:")
            print("Enteros:")
            for i in self.__bloque_global[0]:
                print(i)
            print("Flotantes:")
            for i in self.__bloque_global[1]:
                print(i)
            print("Strings:")
            for i in self.__bloque_global[2]:
                print(i)
            print("Constantes compilacion:")
            print(self.__bloque_constantes_compilacion)
            print("Constantes ejecucion:")
            print(self.__bloque_constantes_ejecucion)

            print("Locales:")
            print("Enteros:", len(self.__bloque_local[0]))
            for i in self.__bloque_local[0]:
                print(i)
            print("Flotantes:", len(self.__bloque_local[1]))
            for i in self.__bloque_local[1]:
                print(i)
            print("Strings:", len(self.__bloque_local[2]))
            for i in self.__bloque_local[2]:
                print(i)

        def generaEspaciosParaConstantes(self):
            constantes_ordenadas = sorted(self.__bloque_constantes_compilacion.items(), key=operator.itemgetter(1))
            for k, _ in constantes_ordenadas:
                tipo = int(k[0])
                valor = k[2:]
                if tipo == Utils.Tipo.Entero.value:
                    valor = int(valor)
                if tipo == Utils.Tipo.Flotante.value:
                    valor = float(valor)
                if tipo == Utils.Tipo.String.value:
                    valor = valor[1:-1]
                self.__bloque_constantes_ejecucion[tipo].append(valor)

        def getValorParaEspacio(self, espacio, offset_actual_locales=None):
            if espacio < Memoria.OFFSET_ENTEROS_TEMPORALES:
                # Es global
                valor_tipo = (espacio - Memoria.OFFSET_ENTEROS_GLOBALES) / Memoria.ESPACIO_GLOBALES
                indice = (espacio - Memoria.OFFSET_ENTEROS_GLOBALES) % Memoria.ESPACIO_GLOBALES
                return self.__bloque_global[valor_tipo][indice]

            if espacio >= Memoria.OFFSET_ENTEROS_CONSTANTES:
                # Es constante
                valor_tipo = (espacio - Memoria.OFFSET_ENTEROS_CONSTANTES) / Memoria.ESPACIO_CONSTANTES
                indice = (espacio - Memoria.OFFSET_ENTEROS_CONSTANTES) % Memoria.ESPACIO_CONSTANTES
                if Utils.DEBUGGING_MODE:
                    print("Get de constante:")
                    print("\tValor:", self.__bloque_constantes_ejecucion[valor_tipo][indice])
                    print("\tEspacio:", espacio)
                return self.__bloque_constantes_ejecucion[valor_tipo][indice]

            if Memoria.OFFSET_ENTEROS_LOCALES <= espacio <= Memoria.OFFSET_STRINGS_LOCALES + Memoria.ESPACIO_LOCALES:
                # Es local
                valor_tipo = (espacio - Memoria.OFFSET_ENTEROS_LOCALES) / Memoria.ESPACIO_LOCALES
                indice = (espacio - Memoria.OFFSET_ENTEROS_LOCALES) % Memoria.ESPACIO_LOCALES
                return self.__bloque_local[valor_tipo][indice + offset_actual_locales[valor_tipo]]

            # Es temporal
            if Memoria.OFFSET_ENTEROS_TEMPORALES <= espacio <= Memoria.OFFSET_STRINGS_TEMPORALES + \
                    Memoria.ESPACIO_TEMPORALES:
                valor_tipo = (espacio - Memoria.OFFSET_ENTEROS_TEMPORALES) / Memoria.ESPACIO_TEMPORALES
                indice = (espacio - Memoria.OFFSET_ENTEROS_TEMPORALES) % Memoria.ESPACIO_TEMPORALES
                print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
                print("Valor tipo:", valor_tipo)
                print("Indice:", indice)
                print(self.__bloque_temporal)
                print("Offsets: ", self.__offsets_temporales)
                print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
                if len(self.__pila_offsets_temporales) > 0:
                    return self.__bloque_temporal[valor_tipo][
                        indice + self.__pila_offsets_temporales[-1][valor_tipo]]
                return self.__bloque_temporal[valor_tipo][indice]

        def setValorParaEspacio(self, espacio, valor, offset_actual_locales=None):
            """
            Funcion que se encarga de asignar valores a los espacios de memoria.
            :param espacio: El espacio de memoria al que se le quiere asignar un valor
            :param valor: Valor a asignar en el espacio de memoria
            :param offset_actual_locales: Offsets utilizados para manejar las variables locales
            :return: Nada.
            """
            if Memoria.OFFSET_ENTEROS_GLOBALES <= espacio < Memoria.OFFSET_STRINGS_GLOBALES + Memoria.ESPACIO_GLOBALES:
                # Es global
                valor_tipo = (espacio - Memoria.OFFSET_ENTEROS_GLOBALES) / Memoria.ESPACIO_GLOBALES
                indice = (espacio - Memoria.OFFSET_ENTEROS_GLOBALES) % Memoria.ESPACIO_GLOBALES
                if Utils.DEBUGGING_MODE:
                    print("Set de global:")
                    print("\tValor:", valor)
                    print("\tEspacio:", espacio)
                    print(espacio, indice, valor_tipo)
                self.__bloque_global[valor_tipo][indice] = valor

            # Manejo de locales
            if Memoria.OFFSET_ENTEROS_LOCALES <= espacio < Memoria.OFFSET_STRINGS_LOCALES + Memoria.ESPACIO_LOCALES:
                if Utils.DEBUGGING_MODE:
                    print("_______________________________________________")
                    print(offset_actual_locales)
                    print(self.__bloque_local)
                    print("_______________________________________________")
                valor_tipo = (espacio - Memoria.OFFSET_ENTEROS_LOCALES) / Memoria.ESPACIO_LOCALES
                indice = (espacio - Memoria.OFFSET_ENTEROS_LOCALES) % Memoria.ESPACIO_LOCALES
                self.__bloque_local[valor_tipo][indice + offset_actual_locales[valor_tipo]] = valor

            # Aqui se manejan los temporales
            if Memoria.OFFSET_ENTEROS_TEMPORALES <= espacio <= Memoria.OFFSET_STRINGS_TEMPORALES + \
                    Memoria.ESPACIO_TEMPORALES:
                valor_tipo = (espacio - Memoria.OFFSET_ENTEROS_TEMPORALES) / Memoria.ESPACIO_TEMPORALES
                self.__bloque_temporal[valor_tipo].append(valor)
                if Utils.DEBUGGING_MODE:
                    print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
                    print(self.__offsets_temporales)
                    print(self.__bloque_temporal)
                    print("Pila de offsets", self.__pila_offsets_temporales)
                    print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
                self.__offsets_temporales[valor_tipo] += 1
                if Utils.DEBUGGING_MODE:
                    print("__________________TEMPORALES___________________")
                    print(self.__offsets_temporales)
                    print(self.__bloque_temporal)
                    print("Pila de offsets", self.__pila_offsets_temporales)
                    print("_______________________________________________")

        def darDeAltaLocales(self, lista):
            counter = 0
            if len(lista) > 0:
                while counter < 3:
                    tipo = Utils.Tipo.Entero
                    if counter == 1:
                        tipo = Utils.Tipo.Flotante
                    if counter == 2:
                        tipo = Utils.Tipo.String
                    print(lista)
                    for i in range(0, lista[counter]):
                        self.__bloque_local[counter].append(Utils.Tipo.getDefault(tipo))
                    counter += 1

        def liberarLocales(self, cantidades):
            counter = 0
            if len(self.__pila_offsets_temporales) > 0:
                print("_________________________________")
                print("Liberacion de offsets temporales")
                print("Pila de offsets", self.__pila_offsets_temporales)
                offsets_de_padre = self.__pila_offsets_temporales.pop()

                diferencias_de_offsets = [x - y for x, y in zip(self.__offsets_temporales, offsets_de_padre)]
                print("Diferencias de offsets", diferencias_de_offsets)
                while counter < 3:
                    for i in range(0, diferencias_de_offsets[counter]):
                        self.__bloque_temporal[counter].pop()
                    counter += 1
                self.__offsets_temporales = offsets_de_padre
            counter = 0
            if len(cantidades) > 0:
                while counter < 3:
                    for i in range(0, cantidades[counter]):
                        self.__bloque_local[counter].pop()
                    counter += 1

            if Utils.DEBUGGING_MODE:
                print("Bloque local:", self.__bloque_local)
                print("Bloque temporal:", self.__bloque_temporal)
                print("Offsets temporales:", self.__offsets_temporales)

        def congelarTemporalesParaNuevaFuncion(self):
            self.__pila_offsets_temporales.append(self.__offsets_temporales[:])

    instancia = None

    @staticmethod
    def getInstance():
        if not Memoria.instancia:
            Memoria.instancia = Memoria.__Memoria()
        return Memoria.instancia
