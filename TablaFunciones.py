import Funcion
import Variable
import Utils
import Memoria

class TablaFunciones:
    class __TablaFunciones:
        def __init__(self):
            self.__scopeActual = 0
            self.__listaFunciones = {}

        def nuevoScope(self):
            self.__scopeActual += 1
            Memoria.Memoria.getInstance().reseteaEspacios()

        def nuevaFuncion(self, tipo, nombre, params, cuadruplo):
            if str(nombre) in self.__listaFunciones:
                raise ValueError("Ya existe una funcion con este nombre")
            else:
                funcion = Funcion.Funcion(tipo, nombre, params, self.__scopeActual, cuadruplo=cuadruplo)
                self.__listaFunciones.update({str(nombre): funcion})

        def getScopeActual(self):
            return self.__scopeActual

        def checaParam(self, nombre, params):
            funcion = self.__listaFunciones.get(str(nombre))
            if Utils.DEBUGGING_MODE:
                print("En funcion " + nombre)
                print("Lista de parametros de entrada:")
                print(params)
                print("Lista de parametros de funcion:")
                print(funcion.getParams())
                print("")
            if len(funcion.getParams()) != len(params):
                raise ValueError('Longitud de parametros no coincide')
            else:
                listaParams = funcion.getParams()
                for i in range(0, len(listaParams)):
                    if listaParams[i] != params[i]:
                        raise ValueError('Tipo de parametro no coincide')
                return True

        def existeFuncion(self, nombre):
            return str(nombre) in self.__listaFunciones

        def getFuncion(self, nombre):
            if (str(nombre)) in self.__listaFunciones:
                return self.__listaFunciones[str(nombre)]
            raise KeyError("La funcion no existe")

        def __str__(self):
            for k in self.__listaFunciones:
                print(str(k))
            return ""

    instancia = None

    @staticmethod
    def getInstance():
        if not TablaFunciones.instancia:
            TablaFunciones.instancia = TablaFunciones.__TablaFunciones()
        return TablaFunciones.instancia
