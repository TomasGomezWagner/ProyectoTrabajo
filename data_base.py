from peewee import *
import csv

try:
    sqilte_db = SqliteDatabase("agentes.db", pragmas={"journal_mode": "Wal"})

    class BaseModel(Model):
        """A base model thath wil use our Sqlite database"""

        class Meta:
            database = sqilte_db

    class Agentes(BaseModel):
        nombre = CharField()
        legajo = CharField()
        documento = CharField()

    sqilte_db.connect()
    sqilte_db.create_tables([Agentes])

except:
    pass


def llenar_tabla():
    try:
        with open(
            r"""C:\Users\Tom\Desktop\proyecto_trabajo_modificacion\csv\utiles\RN_AGENTES_INTERVINIENTES.csv""",
            "r",
        ) as file:
            reader = csv.reader(file, delimiter=";")
            for row in reader:
                persona = Agentes()
                persona.nombre = row[0]
                persona.legajo = row[1]
                persona.documento = row[2]
                persona.save()
    except:
        pass