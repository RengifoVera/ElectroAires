from cmath import pi
import psycopg2
from tkinter import messagebox as mb
from ElectroAiresUI import Electro

tabla=Electro.Registro_Vehiculo

# CONEXION BASE DE DATOS HEROKU POSTGRESQL
def conexion_bd(query, datos):
    conn = psycopg2.connect(
        dbname="db2p0n0f7ofdjn",
        user="pflokzxrsqcyob",
        password="f08950e459414bb2097b3a979265e61461434169943a23b34d29dee6c74501c4",
        host="ec2-52-200-215-149.compute-1.amazonaws.com",
        port="5432"
    )
    cursor = conn.cursor()
    cursor.execute(query, datos)
    conn.commit()
    return cursor, conn
        
#REGISTRAR VEHICULO
def guardar(fecha,placa,valor,tipo,costos,arreglos):
    try:
        if fecha =='' or placa=='' or valor=='' or tipo=='INGRESE OPCION..' or costos =='' or arreglos =='':
            mb.showerror(
                "Cuidado", "Algun Campo Vacio O Algun Dato Mal Digitado")
        else:
            query = '''INSERT INTO electro VALUES (%s,%s,%s,%s,%s,%s)'''
            conexion_bd(query, (fecha,placa,valor,tipo,costos,arreglos))
            mb.showinfo("EXITO", "VEHICULO REGISTRADO")
    except:
        mb.showerror("CUIDADO", "DATOS NO GUARDADOS")
        



