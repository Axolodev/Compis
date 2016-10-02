import Variable

class TablaVariables:

    class __TablaVariables:
        def __init__(self):
            self.__scopeActual = 0
            self.__listaVariables = {}

        def nuevoScope(self):
            self.__scopeActual += 1

        def nuevaVariable(self, tipo, nombre):
            if (str(self.__scopeActual) + "_" + str(nombre)) in self.__listaVariables:
                raise ValueError("Ya existe una variable con este nombre")
            else:
                var = Variable.Variable(tipo, nombre, self.__scopeActual)
                self.__listaVariables.update({str(self.__scopeActual) + "_" + str(nombre): var})

        def getVariable(self, nombre, scope):
            if not (str(scope) + "_" + str(nombre)) in self.__listaVariables:
                raise ValueError("La variable no existe")
            else:
                return self.__listaVariables[str(scope) + "_" + str(nombre)]

        def setValorAVariable(self, nombre, scope, valor):
            if not (str(scope) + "_" + str(nombre)) in self.__listaVariables:
                raise ValueError("La variable no existe")
            else:
                var = self.__listaVariables.get(str(self.__scopeActual) + "_" + str(nombre))
                var.setValor(valor)
                self.__listaVariables.update({str(self.__scopeActual) + "_" + str(nombre): var})

    instancia = None

    def __new__(cls):
        if not TablaVariables.instancia:
            TablaVariables.instancia = TablaVariables.__TablaVariables()
        return TablaVariables.instancia

    def nuevoScope(self):
        self.instancia.nuevoScope()

    def creaVar(self, tipo, nombre):
        self.instancia.nuevaVariable(tipo, nombre)

    def getVariable(self, nombre, scope):
        return self.instancia.getVariable(nombre, scope)

    def setValorAVariable(self, nombre, scope, valor):
        self.instancia.setValorAVariable(nombre, scope, valor)




