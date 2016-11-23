from __future__ import print_function

import Tkinter
import tkSimpleDialog
import turtle
import MaquinaVirtual
import math
from Tkinter import *


class Interfaz():
    class __Interfaz(Frame):
        def __init__(self):
            self.root = Tkinter.Tk()
            self.root.title("Draw with Jr. Lang!")
            self.root.geometry("1920x1080")
            cv = Tkinter.Canvas(self.root, width=2000, height=400)
            cv.pack(side=BOTTOM)
            self.__turtle = turtle.RawTurtle(cv)
            self.__turtle.speed(5)

            self.__turtle.shape("turtle")
            self.__turtle.color("green")
            self.parse_texto = ""
            self.boton_presionado = False
            Frame.__init__(self, self.root)
            self.pack()
            self.createWidgets()

        def run(self):
            _input = self.CODE.get("1.0", "end-1c")
            mv = MaquinaVirtual.MaquinaVirtual(_input)
            mv.ejecutar()

        def createWidgets(self):
            self.QUIT = Button(self)
            self.QUIT["text"] = "QUIT"
            self.QUIT["fg"] = "red"
            self.QUIT["command"] = self.quit

            self.RUN = Button(self)
            self.RUN["text"] = "RUN",
            self.RUN["fg"] = "green"
            self.RUN["command"] = self.run

            label_code = Label(self.root, text="CODIGO")
            label_output = Label(self.root, text="OUTPUT")

            self.CODE = Text(self.root)
            label_code.pack(side=LEFT)

            self.CODE.pack(side=LEFT)
            self.OUTPUT = Text(self.root)
            self.OUTPUT.configure(state="disabled")
            self.OUTPUT.pack(side=RIGHT)
            label_output.pack(side=RIGHT)
            self.RUN.pack()
            self.QUIT.pack()

        def camina(self, metros):
            self.__turtle.forward(metros)

        def mira(self, angulo):
            self.__turtle.setheading(angulo)

        def gira(self, angulo):
            self.__turtle.left(angulo)

        def salta(self, x, y):
            self.__turtle.penup()
            self.__turtle.goto(x, y)
            self.__turtle.pendown()

        def reinicia(self):
            self.__turtle.home()
            self.__turtle.clear()

        def asigna(self, tipo):
            if tipo == 0:
                var = "entero"
                resultado = tkSimpleDialog.askinteger('Address', 'Ingresa variable tipo: ' + var)
            elif tipo == 1:
                var = "flotante"
                resultado = tkSimpleDialog.askfloat('Address', 'Ingresa variable tipo: ' + var)
            else:
                var = "string"
                resultado = tkSimpleDialog.askstring('Address', 'Ingresa variable tipo: ' + var)

            return resultado

        def muestra(self, valor):
            self.OUTPUT.configure(state="normal")
            self.OUTPUT.insert(END, "Este es el valor que imprimiste: " + str(valor) + "\n")
            self.OUTPUT.configure(state="disabled")

        def destroy(self):
            self.root.destroy()

    instancia = None

    @staticmethod
    def getInstance():
        if not Interfaz.instancia:
            Interfaz.instancia = Interfaz.__Interfaz()
        return Interfaz.instancia



