class Variable:

    def __init__(self, tipo, nombre, scope):
        self.__nombre = nombre
        self.__tipo = tipo
        self.__scope = scope
        self.__valor = None

    def getNombre(self):
        return self.__nombre

    def getValor(self):
        return self.__valor

    def setValor(self, valor):
        self.__valor = valor

    def getTipo(self):
        return self.__tipo

    def getScope(self):
        return self.__scope
