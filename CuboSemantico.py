import Tipo


class CuboSemantico:
    ENTERO = Tipo.Tipo.Entero
    FLOTANTE = Tipo.Tipo.Flotante
    STRING = Tipo.Tipo.String
    ERROR = Tipo.Tipo.Error

    __cubo = [
        # Entero
        [
            # Entero x Entero
            [
                ENTERO,  # +
                ENTERO,  # -
                ENTERO,  # *
                ENTERO,  # /
                ENTERO,  # %
                ENTERO,  # <
                ENTERO,  # >
                ENTERO,  # <=
                ENTERO,  # >=
                ENTERO,  # !=
                ENTERO,  # ==
                ENTERO,  # &&
                ENTERO  # ||
            ],
            # Entero x Flotante
            [
                FLOTANTE,  # +
                FLOTANTE,  # -
                FLOTANTE,  # *
                FLOTANTE,  # /
                ENTERO,  # %
                ENTERO,  # <
                ENTERO,  # >
                ENTERO,  # <=
                ENTERO,  # >=
                ENTERO,  # !=
                ENTERO,  # ==
                ENTERO,  # &&
                ENTERO  # ||
            ],
            # Entero x String
            [
                ERROR,  # +
                ERROR,  # -
                ERROR,  # *
                ERROR,  # /
                ERROR,  # %
                ERROR,  # <
                ERROR,  # >
                ERROR,  # <=
                ERROR,  # >=
                ERROR,  # !=
                ERROR,  # ==
                ERROR,  # &&
                ERROR  # ||
            ]
        ],

        # Flotante
        [
            # Flotante x Entero
            [
                FLOTANTE,  # +
                FLOTANTE,  # -
                FLOTANTE,  # *
                FLOTANTE,  # /
                ENTERO,  # %
                ENTERO,  # <
                ENTERO,  # >
                ENTERO,  # <=
                ENTERO,  # >=
                ENTERO,  # !=
                ENTERO,  # ==
                ENTERO,  # &&
                ENTERO  # ||
            ],
            # Flotante x Flotante
            [
                FLOTANTE,  # +
                FLOTANTE,  # -
                FLOTANTE,  # *
                FLOTANTE,  # /
                ENTERO,  # %
                ENTERO,  # <
                ENTERO,  # >
                ENTERO,  # <=
                ENTERO,  # >=
                ENTERO,  # !=
                ENTERO,  # ==
                ENTERO,  # &&
                ENTERO  # ||
            ],
            # Flotante x String
            [
                ERROR,  # +
                ERROR,  # -
                ERROR,  # *
                ERROR,  # /
                ERROR,  # %
                ERROR,  # <
                ERROR,  # >
                ERROR,  # <=
                ERROR,  # >=
                ERROR,  # !=
                ERROR,  # ==
                ERROR,  # &&
                ERROR  # ||
            ]
        ],

        # String
        [
            # String x Entero
            [
                ERROR,  # +
                ERROR,  # -
                ERROR,  # *
                ERROR,  # /
                ERROR,  # %
                ERROR,  # <
                ERROR,  # >
                ERROR,  # <=
                ERROR,  # >=
                ERROR,  # !=
                ERROR,  # ==
                ERROR,  # &&
                ERROR  # ||
            ],
            # String x Flotante
            [
                ERROR,  # +
                ERROR,  # -
                ERROR,  # *
                ERROR,  # /
                ERROR,  # %
                ERROR,  # <
                ERROR,  # >
                ERROR,  # <=
                ERROR,  # >=
                ERROR,  # !=
                ERROR,  # ==
                ERROR,  # &&
                ERROR  # ||
            ],
            # String x String
            [
                STRING,  # +
                ERROR,  # -
                ERROR,  # *
                ERROR,  # /
                ERROR,  # %
                ERROR,  # <
                ERROR,  # >
                ERROR,  # <=
                ERROR,  # >=
                ENTERO,  # !=
                ENTERO,  # ==
                ERROR,  # &&
                ERROR  # ||
            ]
        ],
    ]

    @staticmethod
    def getTipo(operador, tipo_operando1, tipo_operando2):
        retorno = CuboSemantico.__cubo[tipo_operando1][tipo_operando2][operador]
        if retorno is CuboSemantico.ERROR:
            raise ValueError("La variable no existe")
        return retorno
