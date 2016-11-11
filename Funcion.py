import TablaVariables


class Funcion:

    def __init__(self, nombre, tipo, params, scope, cuadruplo):
        self.__nombre = nombre
        self.__tipo = tipo
        self.__scope = scope
        self.__params = params
        self.__cuadruplo_de_inicio = cuadruplo

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

    def getLenParams(self):
        return len(self.__params)

    def getNumVar(self):
        variables = TablaVariables.TablaVariables.getInstance().consigueVariablesPara(self.__scope)
        return len(variables) - len(self.__params)

    def getCuadruplo(self):
        return self.__cuadruplo_de_inicio

    def setCuadruplo(self, num_cuadruplo):
        self.__cuadruplo_de_inicio = num_cuadruplo

    def __str__(self):
        to_str = "Nombre: " + str(self.__nombre)
        to_str += "\n\tScope identificador: " + str(self.__scope)
        variables = TablaVariables.TablaVariables.getInstance().consigueVariablesPara(self.__scope)
        to_str += "\n\tVariables: "
        for i, j in variables.items():
            to_str += "\n\t\t" + i + ": " + str(j)
        to_str += "\n\tCuadruplo de inicio: " + str(self.__cuadruplo_de_inicio)
        return to_str
