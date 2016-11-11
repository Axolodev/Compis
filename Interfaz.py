from __future__ import print_function
import Memoria
import random
import logging
import ply.lex as lex
import ply.yacc as yacc
import Utils
import TablaVariables
import TablaFunciones
import CuboSemantico
import warnings
import Tortuga
import scanner as scanner
import io

import Tkinter
from Tkinter import *
import turtle


class Application(Frame):
    def run(self):
        input = self.TEXT.get("1.0", "end-1c")
        with io.FileIO("source.txt", "w") as file:
            file.write(input)
        print(input)
        scanner.run(input)

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

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()


root = Tk()
root.title("Draw with Jr. Lang!")
cv = Tkinter.Canvas(root, width=600, height=600)
cv.pack(side=Tkinter.BOTTOM)
t = turtle.RawTurtle(cv)
t.shape("turtle")
t.color("green")
screen = t.getscreen()
app = Application(master=root)
app.mainloop()
root.destroy()
