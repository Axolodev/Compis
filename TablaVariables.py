import Variable
import TablaFunciones


class TablaVariables:

    class __TablaVariables:
        def __init__(self):
            self.__scopeActual = 0
            self.__listaVariables = {}
            self.tablaFunciones = TablaFunciones.TablaFunciones.getInstance()

        def nuevoScope(self):
            self.__scopeActual += 1

        def nuevaVariable(self, tipo, nombre, es_arreglo, es_matriz):
            if (str(self.tablaFunciones.getScopeActual()) + "_" + str(nombre)) in self.__listaVariables or \
                            ("0_" + str(nombre)) in self.__listaVariables:
                raise ValueError("Ya existe una variable con este nombre")
            else:
                var = Variable.Variable(tipo, nombre, self.__scopeActual)
                self.__listaVariables.update({str(self.tablaFunciones.getScopeActual()) + "_" + str(nombre): var})

        def getValorVariable(self, nombre):
            if (str(self.tablaFunciones.getScopeActual()) + "_" + str(nombre)) in self.__listaVariables:
                return self.__listaVariables[str(self.tablaFunciones.getScopeActual()) + "_" + str(nombre)]
            elif ("0_" + str(nombre)) in self.__listaVariables:
                return self.__listaVariables["0_" + str(nombre)]
            raise ValueError("La variable no existe")

        def setValorAVariable(self, nombre, valor):
            if (str(self.tablaFunciones.getScopeActual()) + "_" + str(nombre)) in self.__listaVariables:
                var = self.__listaVariables.get(str(self.tablaFunciones.getScopeActual()) + "_" + str(nombre))
                var.setValor(valor)
                self.__listaVariables.update({str(self.tablaFunciones.getScopeActual()) + "_" + str(nombre): var})
            else:
                if ("0_" + str(nombre)) in self.__listaVariables:
                    var = self.__listaVariables.get("0_" + str(nombre))
                    var.setValor(valor)
                    self.__listaVariables.update({"0_" + str(nombre): var})
                else:
                    raise ValueError("La variable no existe")


    instancia = None

    @staticmethod
    def getInstance():
        if not TablaVariables.instancia:
            TablaVariables.instancia = TablaVariables.__TablaVariables()
        return TablaVariables.instancia

    def __str__(self):
        for x in self.instancia.__listaVariables:
            print (x)
            for y in self.instancia.__listaVariables[x]:
                print (y, ':', self.instancia.__listaVariables[x][y])
