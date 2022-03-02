from tkinter import *
from tkinter import ttk
from model import Model


class Views:
    def __init__(self, root):
        self.principal = root
        self.principal.geometry("400x350")
        self.principal.title("Modificaciones")

        self.frame_principal = Frame(self.principal)
        self.frame_principal.pack()
        Button(
            self.frame_principal,
            text="Rio Negro",
            command=lambda: Model.new_frame(
                self, self.frame_principal, self.rio_negro()
            ),
        ).pack()
        Button(self.frame_principal, text="Segundo envio").pack()
        Button(self.frame_principal, text="otros proyectos", state="disable").pack()

    def rio_negro(self):
        options = ["salida de edicion", "empsat"]
        self.ruta = StringVar()
        self.name = StringVar()
        self.cp = StringVar()
        self.localidad = StringVar()
        self.check = BooleanVar()

        self.principal.title("Modificar Rio Negro")
        self.frame_rio = Frame(self.principal)
        Label(self.frame_rio, text="MODIFICACIONES RIO NEGRO").pack()

        self.list_options = ttk.Combobox(
            self.frame_rio, values=options, state="readonly", foreground="grey"
        )
        self.list_options.pack()
        self.list_options.set("seleccionar proceso")
        Label(self.frame_rio, text="seleccionar archivo").pack()
        self.ruta_visible = Entry(self.frame_rio, textvariable=self.ruta).pack()
        Button(
            self.frame_rio,
            text="seleccionar",
            command=lambda: Model.get_ruta(self.ruta),
        ).pack()
        self.chekbox = Checkbutton(
            self.frame_rio, text="Equipo fijo", variable=self.check
        ).pack()
        Label(self.frame_rio, text="nuevo codigo postal(Solo salida de edicion)").pack()
        self.new_cp = Entry(self.frame_rio, textvariable=self.cp)
        self.new_cp.pack()
        Label(self.frame_rio, text="nueva localidad(Solo empsat)").pack()
        self.new_localidad = Entry(self.frame_rio, textvariable=self.localidad)
        self.new_localidad.pack()
        Label(self.frame_rio, text="nombre del nuevo archivo").pack()
        self.new_name = Entry(self.frame_rio, textvariable=self.name).pack()
        Button(
            self.frame_rio,
            text="modificar",
            command=lambda: Model.mod_edicion(
                self.ruta,
                self.name,
                self.new_cp,
                self.new_localidad,
                self.check,
                self.list_options,
                self.mensaje,
            ),
        ).pack()
        self.mensaje = Label(self.frame_rio)
        self.mensaje.pack()
        self.volver = Button(
            self.frame_rio,
            text="volver",
            command=lambda: Model.new_frame(self, self.frame_rio, self.frame_principal),
        ).pack()
        return self.frame_rio