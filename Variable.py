from __future__ import print_function
import Memoria
import Utils


class Variable:

    def __init__(self, tipo, nombre, scope):
        if Utils.DEBUGGING_MODE:
            print("Nombre:", nombre)
            print("\tTipo:", tipo)
        self.__nombre = nombre
        self.__tipo = tipo
        self.__scope = scope
        self.__valor = None
        self.__espacio_memoria = 0
        if tipo != Utils.Tipo.Vacio:
            self.__espacio_memoria = Memoria.Memoria.getInstance().generaEspacioVariable(scope, tipo)
        print("Espacio nuevo de variable:", self.__espacio_memoria)

    def getNombre(self):
        return self.__nombre

    def getEspacioMemoria(self):
        return self.__espacio_memoria

    def getValor(self):
        return self.__valor

    def setValor(self, valor):
        self.__valor = valor

    def setScope(self, scope):
        self.__scope = scope

    def getTipo(self):
        return self.__tipo

    def getScope(self):
        return self.__scope
