from enum import Enum


class Tipo(Enum):
    Vacio = 0
    Entero = 1
    Flotante = 2
    String = 3

    @staticmethod
    def getDefault(tipo):
        if tipo == Tipo.Entero:
            return 0
        elif tipo == Tipo.Flotante:
            return 0.0
        elif tipo == Tipo.String:
            return ""
        return None
