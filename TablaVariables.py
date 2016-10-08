import Variable


class TablaVariables:
    class __TablaVariables:
        def __init__(self):
            self.__scopeActual = 0
            self.__listaVariables = {}

        def nuevoScope(self):
            self.__scopeActual += 1

        def nuevaVariable(self, tipo, nombre):
            if (str(TablaFunciones.getScopeActual()) + "_" + str(nombre)) in self.__listaVariables or \
                            ("0_" + str(nombre)) in self.__listaVariables:
                raise ValueError("Ya existe una variable con este nombre")
            else:
                var = Variable.Variable(tipo, nombre, self.__scopeActual)
                self.__listaVariables.update({str(TablaFunciones.getScopeActual()) + "_" + str(nombre): var})

        def getValorVariable(self, nombre):
            if (str(TablaFunciones.getScopeActual()) + "_" + str(nombre)) in self.__listaVariables:
                return self.__listaVariables[str(TablaFunciones.getScopeActual()) + "_" + str(nombre)]
            elif ("0_" + str(nombre)) in self.__listaVariables:
                return self.__listaVariables["0_" + str(nombre)]
            raise ValueError("La variable no existe")

        def setValorAVariable(self, nombre, valor):
            if (str(TablaFunciones.getScopeActual()) + "_" + str(nombre)) in self.__listaVariables:
                var = self.__listaVariables.get(str(TablaFunciones.getScopeActual()) + "_" + str(nombre))
                var.setValor(valor)
                self.__listaVariables.update({str(TablaFunciones.getScopeActual()) + "_" + str(nombre): var})
            else:
                if ("0_" + str(nombre)) in self.__listaVariables:
                    var = self.__listaVariables.get("0_" + str(nombre))
                    var.setValor(valor)
                    self.__listaVariables.update({"0_" + str(nombre): var})
                else:
                    raise ValueError("La variable no existe")


    instancia = None

    def __new__(cls):
        if not TablaVariables.instancia:
            TablaVariables.instancia = TablaVariables.__TablaVariables()
        return TablaVariables.instancia

    def nuevoScope(self):
        self.instancia.nuevoScope()

    def creaVar(self, tipo, nombre, es_arreglo, es_matriz):
        self.instancia.nuevaVariable(tipo, nombre)

    def getVariable(self, nombre):
        return self.instancia.getValorVariable(nombre)

    def setValorAVariable(self, nombre, valor):
        self.instancia.setValorAVariable(nombre, valor)

    def __str__(self):
        for x in self.instancia.__listaVariables:
            print (x)
            for y in self.instancia.__listaVariables[x]:
                print (y, ':', self.instancia.__listaVariables[x][y])
