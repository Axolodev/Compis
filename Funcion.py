class Funcion:

    def __init__(self, nombre, tipo, params, scope):
        self.__nombre = nombre
        self.__tipo = tipo
        self.__scope = scope
        self.__params = params

    def getNombre(self):
        return self.__nombre

    def setNombre(self, nombre):
        self.__nombre = nombre

    def getTipo(self):
        return self.__tipo

    def setTipo(self, tipo):
        self.__tipo = tipo

    def getScope(self):
        return self.__scope

    def setScope(self, scope):
        self.__scope = scope

    def getParams(self):
        return self.__params

    def setParams(self, params):
        self.__params = params
