import Interfaz


def main():
    app = Interfaz.Interfaz.getInstance()
    app.mainloop()
    app.getInstance().destroy()

main()
