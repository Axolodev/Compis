import Funcion
import Variable


class TablaFunciones:
    class __TablaFunciones:
        def __init__(self):
            self.__scopeActual = 0
            self.__listaFunciones = {}

        def nuevoScope(self):
            self.__scopeActual += 1

        def nuevaFuncion(self, tipo, nombre, params):
            if str(nombre) in self.__listaFunciones:
                raise ValueError("Ya existe una funcion con este nombre")
            else:
                funcion = Funcion.Funcion(tipo, nombre, params, self.__scopeActual)
                self.__listaFunciones.update({str(nombre): funcion})

        def getScopeActual(self):
            return self.__scopeActual

        def checaParam(self, nombre, params):
            funcion = self.__listaFunciones.get(str(nombre))
            if len(funcion.getParams()) != len(params):
                raise ValueError('Longitud de parametros no coincide')
            else:
                listaParams = funcion.getParams()
                print listaParams
                print params
                for i in range(0, len(listaParams)-1):
                    if listaParams[i] != params[i]:
                        raise ValueError('Tipo de parametro no coincide')
                return True

        def __str__(self):
            for k in self.__listaFunciones:
                print str(k)
            return ""

    instancia = None

    @staticmethod
    def getInstance():
        if not TablaFunciones.instancia:
            TablaFunciones.instancia = TablaFunciones.__TablaFunciones()
        return TablaFunciones.instancia
