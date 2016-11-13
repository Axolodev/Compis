from __future__ import print_function

import Tkinter
import turtle
import MaquinaVirtual
from Tkinter import *


class Interfaz():
    class __Interfaz(Frame):
        def __init__(self):
            self.root = Tkinter.Tk()
            self.root.title("Draw with Jr. Lang!")
            cv = Tkinter.Canvas(self.root, width=600, height=600)
            cv.pack(side=Tkinter.BOTTOM)
            self.__turtle = turtle.RawTurtle(cv)
            self.__turtle.shape("turtle")
            self.__turtle.color("green")
            Frame.__init__(self, self.root)
            self.pack()
            self.createWidgets()

        def run(self):
            _input = self.TEXT.get("1.0", "end-1c")
            mv = MaquinaVirtual.MaquinaVirtual(_input)
            mv.ejecutar()

        def createWidgets(self):
            self.QUIT = Button(self)
            self.QUIT["text"] = "QUIT"
            self.QUIT["fg"] = "red"
            self.QUIT["command"] = self.quit

            self.QUIT.pack({"side": "bottom"})

            self.RUN = Button(self)
            self.RUN["text"] = "RUN",
            self.RUN["fg"] = "green"
            self.RUN["command"] = self.run
            self.RUN.pack({"side": "top"})

            self.TEXT = Text(self, width=70, height=70)
            self.TEXT.pack()

        def camina(self, metros):
            self.__turtle.forward(metros * 5)

        def destroy(self):
            self.root.destroy()

    instancia = None

    @staticmethod
    def getInstance():
        if not Interfaz.instancia:
            Interfaz.instancia = Interfaz.__Interfaz()
        return Interfaz.instancia



