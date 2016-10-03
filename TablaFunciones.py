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
            if self.__listaFunciones.has_key(str(self.__scopeActual) + "_" + str(nombre)):
                raise ValueError('Otra funcion existe con el mismo nombre')
            else:
                var = Funcion.Funcion(tipo, nombre, params)
                self.__listaFunciones.update({str(self.__scopeActual) + "_" + str(nombre): var})

        def checaParam(self, nombre, params):
            funcion = self.__listaFunciones.getValue(str(self.__scopeActual) + "_" + str(nombre), default=None)
            if len(funcion.getParams()) != len(params):
                raise ValueError('Longitud de parametros no coincide')
            else:
                listaParams = funcion.getParams()
                for i in listaParams:
                    if listaParams[i].tipo != params.tipo:
                        raise ValueError('Tipo de parametro no coincide')
                return True





    instancia = None

    def __new__(cls):
        if not TablaFunciones.instancia:
            TablaFunciones.instancia = TablaFunciones.__TablaFunciones()
        return TablaFunciones.instancia

    def nuevoScope(self):
        self.instancia.nuevoScope()

    def creaFuncion(self, tipo, nombre):
        self.instancia.nuevaFuncion(tipo, nombre)

    def verificaParam(self, nombre, params):
        return self.instancia.checaParam(nombre, params)




