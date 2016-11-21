from __future__ import print_function
import Memoria
import Utils
import TablaVariables


class Variable:
    def __init__(self, tipo, nombre, scope, lista_dimensiones):
        if Utils.DEBUGGING_MODE:
            print("Nombre:", nombre)
            print("\tTipo:", tipo)
            print("\tDimensiones:", lista_dimensiones)
        self.__nombre = nombre
        self.__tipo = tipo
        self.__scope = scope
        self.__valor = None
        self.__espacio_memoria = 0
        self.__constantes_acceso = []
        self.__lista_dimensiones = lista_dimensiones
        if lista_dimensiones is not None and len(lista_dimensiones) > 0:
            acum_dimensiones = 1
            for dimension in lista_dimensiones:
                acum_dimensiones *= dimension
            k = acum_dimensiones
            lista_constantes_acceso = []
            for dimension in lista_dimensiones:
                acum_dimensiones /= dimension
                lista_constantes_acceso.append(acum_dimensiones)
            lista_constantes_acceso[-1] = k
            self.__constantes_acceso = lista_constantes_acceso
        if tipo != Utils.Tipo.Vacio:
            self.__espacio_memoria = Memoria.Memoria.getInstance().generaEspacioVariable(scope, tipo, lista_dimensiones)
        if Utils.DEBUGGING_MODE:
            print("Constantes de acceso:", self.__constantes_acceso)
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

    def getLimSuperior(self, indice):
        try:
            return self.__lista_dimensiones[indice]
        except IndexError:
            raise IndexError(
                "Se intento acceder a una variable con " + str(indice) + ", teniendo un total de " + str(len(
                    self.__lista_dimensiones)) + " dimensiones.")

    def getDimension(self, num_dimension):
        try:
            return self.__constantes_acceso[num_dimension]
        except IndexError:
            raise IndexError(
                "Se intento acceder a una variable con " + str(num_dimension) + ", teniendo un total de " + str(len(
                    self.__constantes_acceso)) + " dimensiones.")

    def getCantidadDimensiones(self):
        return len(self.__constantes_acceso)

    def getDimensiones(self):
        return self.__constantes_acceso

    def __str__(self):
        to_str = self.__nombre
        to_str += " " + str(self.__tipo)
        return to_str
