class Memoria:
    class __Memoria:
        def __init__(self):
            self.__bloque_global = []
            self.__bloque_temporal = []
            self.__bloque_local = []
            self.__bloque_constantes = {}

        def crear_o_buscar_constante(self, constante):
            if constante not in self.__bloque_constantes:
                self.__bloque_constantes.add(constante)
            return constante

    instancia = None

    @staticmethod
    def getInstance():
        if not Memoria.instancia:
            Memoria.instancia = Memoria.__Memoria()
        return Memoria.instancia
