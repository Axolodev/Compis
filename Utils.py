from enum import Enum


class Tipo(Enum):
    Entero = 0
    Flotante = 1
    String = 2
    Vacio = 3
    Error = -1

    @staticmethod
    def getDefault(tipo):
        if tipo == Tipo.Entero:
            return 0
        elif tipo == Tipo.Flotante:
            return 0.0
        elif tipo == Tipo.String:
            return ""
        return None


class Operador:
    __operadores = {
        '+': 0,
        '-': 1,
        '*': 2,
        '/': 3,
        '%': 4,
        '<': 5,
        '>': 6,
        '<=': 7,
        '>=': 8,
        '!=': 9,
        '==': 10,
        '&&': 11,
        '||': 12,
        '=': 13,

        'negativo': 99,
        'a_flotante': 100,
        'a_string': 101,
        'a_entero': 102,
        'camina': 103,
        'gira': 104,
        'mira': 105,
        'reiniciar': 106,
        'salta_a': 107,
        'input': 150,
        'output': 151,

        'goto': 200,
        'gotoF': 201,
        'gotoT': 202,
        'gosub': 300,
        'return': 301,
        'ret': 302,
        'param': 303,
        'era': 304,
        'end': 999,
    }

    @staticmethod
    def getId(op):
        return Operador.__operadores[op]

DEBUGGING_MODE = True
