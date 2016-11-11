from __future__ import print_function
import Variable
import TablaFunciones
import Utils


class TablaVariables:
    class __TablaVariables:
        def __init__(self):
            self.__scopeActual = 0
            self.__listaVariables = {}
            self.tablaFunciones = TablaFunciones.TablaFunciones.getInstance()

        def nuevoScope(self):
            self.__scopeActual += 1

        def nuevaVariable(self, tipo, nombre, es_arreglo, es_matriz, scope=None):
            if scope is None:
                scope = str(self.tablaFunciones.getScopeActual())
            if (scope + "_" + str(nombre)) in self.__listaVariables or ("0_" + str(nombre)) in self.__listaVariables:
                raise KeyError("Ya existe una variable con este nombre")
            else:
                var = Variable.Variable(tipo, nombre, scope)
                var.setValor(Utils.Tipo.getDefault(var.getTipo()))
                self.__listaVariables.update({scope + "_" + str(nombre): var})
                return var

        def getVariable(self, nombre):
            if (str(self.tablaFunciones.getScopeActual()) + "_" + str(nombre)) in self.__listaVariables:
                return self.__listaVariables[str(self.tablaFunciones.getScopeActual()) + "_" + str(nombre)]
            elif ("0_" + str(nombre)) in self.__listaVariables:
                return self.__listaVariables["0_" + str(nombre)]
            raise KeyError("La variable no existe")

        def setValorAVariable(self, nombre, valor):
            var = self.__listaVariables.get(str(self.tablaFunciones.getScopeActual()) + "_" + str(nombre))
            if var is not None:
                var.setValor(valor)
                self.__listaVariables.update({str(self.tablaFunciones.getScopeActual()) + "_" + str(nombre): var})
            else:
                var = self.__listaVariables.get("0_" + str(nombre))
                if var is not None:
                    var.setValor(valor)
                    self.__listaVariables.update({"0_" + str(nombre): var})
                else:
                    raise KeyError("La variable no existe")

        def __str__(self):
            for k in self.__listaVariables:
                print(str(k))
            return ""

        def consigueVariablesPara(self, scope):
            return dict((key, value) for key, value in self.__listaVariables.items() if key.startswith(str(scope) + "_"))

    instancia = None

    @staticmethod
    def getInstance():
        if not TablaVariables.instancia:
            TablaVariables.instancia = TablaVariables.__TablaVariables()
        return TablaVariables.instancia


