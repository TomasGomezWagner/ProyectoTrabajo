import os
from pathlib import Path
import csv
from tkinter import filedialog
from mensajes import Mensajes
from data_base import *


class Model:
    def __init__(self):
        pass

    def new_frame(self, old, new):
        old.pack_forget()
        return new.pack()

    # FUNCION PRINCIPAL
    def mod_edicion(ruta, nombre, cp, localidad, check, opcion, mensaje):

        save_path = Path(ruta.get()).resolve().parent
        filas = []
        lista_filtrada = []

        if opcion.get() == "seleccionar proceso":
            mensaje["text"] = "no selecciono proceso"

        elif opcion.get() == "salida de edicion":
            Model.edicion(ruta, cp, filas, check)
            Model.generar_csv(save_path, nombre, filas, mensaje)

        elif opcion.get() == "empsat":
            Model.empsat(ruta, lista_filtrada, localidad, check, filas, mensaje)
            if not filas == []:
                Model.generar_csv(save_path, nombre, filas, mensaje)

    # modificar el archivo de salida de edicion
    def edicion(ruta, cp, filas, check):
        with open(str(ruta.get()), "r") as file:
            reader = csv.reader(file, delimiter=";")
            for row in reader:
                row[9] = ""  # quito patente
                if check.get() == True:
                    pass
                else:
                    row[16] = Model.agregar_agentes(row[15])
                row[27] = str(cp.get())  # codigo postal
                row[
                    33
                ] = 'Ley Anexo I "E" Decreto 718/18 reg. Ley Provincial 5263 y mod.'  # agrego ley
                filas.append(row)
            return filas

    # modificar el archivo de empsat
    def empsat(ruta, lista_filtrada, localidad, check, filas, mensaje):
        with open(str(ruta.get()), "r") as file:
            reader = csv.reader(file, delimiter=";")
            filtrado = Model.filtro_documento(reader, lista_filtrada)
            if filtrado:
                for row in filtrado:
                    row[28] = str(localidad.get())  # localidad
                    row[52] = Model.filtro_infractor(row[52])  # acorto el infractor
                    row[64] = Model.filtro_modelo(row[64])  # modifico el modelo
                    if check.get() == True:
                        row[78] = "Agencia provincial de seguridad vial"  # constatador
                        row[79] = "Alonso Alexis Mauro"  # firma
                    else:
                        pass
                    row[83] = row[85]  # numero de lote
                    row[86] = ""  # quita numero de pieza
                    filas.append(row)
                return filas
            else:
                mensaje["text"] = "cancelado"
                print("Operacion cancelada")

    # Genero el csv
    def generar_csv(save_path, nombre, filas, mensaje):
        with open(
            (os.path.join(save_path, f"{nombre.get()}.csv")),
            "w",
            newline="",
        ) as file:
            writer = csv.writer(file, delimiter=";")
            for row in filas:
                writer.writerow(row)
            mensaje["text"] = "listo"
            file.close()
            print("listo")

    def get_ruta(ruta):
        name = filedialog.askopenfilename()
        return ruta.set(name)

    def filtro_infractor(celda):
        separacion = celda.split("-")

        if len(separacion[0]) > 99:
            arreglo = separacion[0][0:97]
            rta = arreglo + " - " + arreglo
            return rta
        else:
            return celda

    def filtro_modelo(celda):
        sep = celda.split("-")

        primer_termino = sep[0]
        del sep[0]
        modelo = primer_termino + "-" + " ".join(sep)
        return modelo

    def filtro_documento(lector, lista):
        i = 0
        counter = 0
        lineas = []
        for line in lector:
            i += 1
            if line[54] == "0":
                if not line[56] == "0":
                    if line[53] == "0":
                        line[54] = line[56]

                    elif line[56][2] == "0":
                        line[54] = line[56][3:10]

                    else:
                        line[54] = line[56][2:10]

            if (line[54] == "0" and line[56] == "0") or line[56] == "0":
                counter += 1
                lineas.append(i)
                print(str(i) + ": linea con datos incorrectos en campo documento")
            elif (
                len(line[54]) < 7
                or len(line[56]) < 11
                or len(line[56]) > 11
                or len(line[54]) > 11
            ):
                counter += 1
                lineas.append(i)
                print(
                    str(i)
                    + ": linea con errores de cantidad caracteres en documento o cuil/cuit"
                )
            elif line[53] == "1" and len(line[54]) > 8:
                counter += 1
                lineas.append(i)
                print(str(i) + ": linea con mas caracteres en documento")
            else:
                lista.append(line)
        if counter > 0:
            if Mensajes.eliminadas(counter, lineas):
                return lista
            else:
                Mensajes.cancelado()
        else:
            return lista

    def agregar_agentes(dato):
        numero = dato
        agente = Agentes.get(Agentes.legajo == numero).nombre
        dato = f"{agente} ({numero})"
        return dato