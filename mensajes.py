from tkinter.messagebox import *


class Mensajes:
    def eliminadas(counter, lineas):
        respuesta = askyesno(
            "eliminar lineas?",
            "Borrar {} lineas por tener datos incompletos en campo documento?. Posicion de las lineas: {} ".format(
                counter, lineas
            ),
        )
        return respuesta

    def cancelado():
        showinfo("Cancelado", "Operacion cancelada")