import Utils


class CuboSemantico:
    ENTERO = Utils.Tipo.Entero
    FLOTANTE = Utils.Tipo.Flotante
    STRING = Utils.Tipo.String
    ERROR = Utils.Tipo.Error

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
                ENTERO,  # ||
                ENTERO,  # =
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
                ENTERO,  # ||
                ENTERO,  # =
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
                ERROR,  # ||
                ERROR,  # =
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
                ENTERO,  # ||
                FLOTANTE,  # =
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
                ENTERO,  # ||
                FLOTANTE,  # =
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
                ERROR,  # ||
                ERROR,  # =
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
                ERROR,  # ||
                ERROR,  # =
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
                ERROR,  # ||
                ERROR,  # =
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
                ERROR,  # ||
                STRING,  # =
            ]
        ],
    ]

    @staticmethod
    def getTipo(operador, tipo_operando1, tipo_operando2):
        operador_value = Utils.Operador.getId(operador)
        print(operador, tipo_operando1, tipo_operando2)
        retorno = CuboSemantico.__cubo[tipo_operando1.value][tipo_operando2.value][operador_value]
        if retorno is CuboSemantico.ERROR:
            raise ValueError("Error de semantica. " + tipo_operando1 + " y " + tipo_operando2 + " no pueden trabajar con " + operador)
        return retorno
