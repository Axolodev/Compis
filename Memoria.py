from __future__ import print_function
import Utils


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
            self.__bloque_global = []
            self.__bloque_temporal = []
            self.__bloque_local = []
            self.__bloque_constantes = {}
            self.__contadores_globales = [0, 0, 0]
            self.__contadores_temporales = [0, 0, 0]
            self.__contadores_locales = [0, 0, 0]
            self.__contadores_constantes = [0, 0, 0]

        def crear_o_buscar_constante(self, constante):
            if constante not in self.__bloque_constantes:
                self.__bloque_constantes.add(constante)
            return constante

        def generaEspacioConstantes(self, tipo, valor):
            llave_de_constante = str(tipo.value) + "_" + str(valor)
            if llave_de_constante not in self.__bloque_constantes:
                espacio_de_memoria = Memoria.OFFSET_ENTEROS_CONSTANTES + tipo.value * Memoria.ESPACIO_CONSTANTES + \
                                     self.__contadores_constantes[tipo.value]
                self.__bloque_constantes.update({llave_de_constante: espacio_de_memoria})
                self.__contadores_constantes[tipo.value] += 1
            return self.__bloque_constantes[llave_de_constante]

        def generaEspacioVaraiablesLocales(self, tipo):
            if Utils.DEBUGGING_MODE:
                print(tipo)
                print("Contadores locales", self.__contadores_locales)
            espacio = Memoria.OFFSET_ENTEROS_LOCALES + self.__contadores_locales[
                tipo.value] + Memoria.ESPACIO_LOCALES * tipo.value
            self.__contadores_locales[tipo.value] += 1
            print("Espacio:", espacio, "\n____________________________")
            return espacio

        def generaEspacioVaraiablesGlobales(self, tipo):
            espacio = Memoria.OFFSET_ENTEROS_GLOBALES + self.__contadores_globales[
                tipo.value] + Memoria.ESPACIO_GLOBALES * tipo.value
            self.__contadores_globales[tipo.value] += 1
            print("Espacio:", espacio, "\n____________________________")
            return espacio

        def generaEspacioTemporal(self, tipo):
            if Utils.DEBUGGING_MODE:
                print(tipo)
                print("Contadores locales", self.__contadores_locales)
            espacio = Memoria.OFFSET_ENTEROS_TEMPORALES + self.__contadores_temporales[
                tipo.value] + Memoria.ESPACIO_TEMPORALES * tipo.value
            self.__contadores_temporales[tipo.value] += 1
            print("Espacio:", espacio, "\n____________________________")
            return espacio

        def generaEspacioVariable(self, scope, tipo):
            if int(scope) != 0:
                return self.generaEspacioVaraiablesLocales(tipo)
            return self.generaEspacioVaraiablesGlobales(tipo)

        def reseteaEspacios(self):
            self.__contadores_locales = [0, 0, 0]
            self.__contadores_temporales = [0, 0, 0]

    instancia = None

    @staticmethod
    def getInstance():
        if not Memoria.instancia:
            Memoria.instancia = Memoria.__Memoria()
        return Memoria.instancia
