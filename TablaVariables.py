class TablaVariables:

    class __TablaVariables:
        def __init__(self):
            self.__scopeActual = 0

        def nuevoScope(self):
            self.__scopeActual+=1

    def __init__(self):
        if not TablaVariables.instancia:
            TablaVariables.instancia = TablaVariables.__TablaVariables()


    def nuevoScope(self):
        self.instancia.nuevoScope()