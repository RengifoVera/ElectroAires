
import re
from tkinter import W, StringVar, Text, NW, Button, LabelFrame, Label, Frame, Entry, Text, Tk, Toplevel, CENTER, END, CENTER, font, messagebox as mb
from turtle import width
from tkcalendar import DateEntry
from tkinter import ttk


class Electro:
    def __init__(self, Inicio):

        self.ini = Inicio
        self.ini.title("Electro Aires App")
        self.ini.geometry(f"{600}x{(self.ini.winfo_screenheight())-200}")
        self.ini['bg'] = '#0059b3'
        self.ini.minsize(width=600, height=(self.ini.winfo_screenheight())-100)
        self.ini.resizable(False, False)

        # FRAME INCIO
        frame_inicio = Frame(self.ini)
        frame_inicio.config(bg='white', width=(self.ini.winfo_screenwidth(
        ))/3, height=(self.ini.winfo_screenheight())-100, bd=5)
        frame_inicio.pack(anchor=CENTER, pady=50)
        Label(frame_inicio, text="Bienvenido a Electro Aires App",
              font=('Britannic Bold', 25), bg="white").pack()
        # Buttons
        btn_registro = Button(frame_inicio, width=20, text="REGISTRAR VEHICULO", font=(
            'Andale Mono', 12), command=lambda: self.Registro_Vehiculo())
        btn_registro.pack(pady=15, padx=150)

        btn_reporte = Button(frame_inicio, width=20, text="GENERAR REPORTE", font=(
            "Andale Mono", 12), command=lambda: self.generar_reporte())
        btn_reporte.pack(pady=15, padx=150)

        # btn_generar = Button(frame_inicio, width=20,
        #                      text="GENERAR FACTURA", font=("Andale Mono", 12))
        # btn_generar.pack(pady=15, padx=150)

        btn_invertario = Button(frame_inicio, width=20,
                                text="INVENTARIO", font=("Andale Mono", 12),command=lambda:self.inventario())
        btn_invertario.pack(pady=15, padx=150)

        btn_salir = Button(frame_inicio, width=20, text="SALIR", font=(
            "Andale Mono", 12), command=lambda: salir())
        btn_salir.pack(pady=15, padx=150)

        def salir():
            self.ini.destroy()

    def Registro_Vehiculo(self):
        from backEnd import conexion_bd,guardar
        self.pant_reg = Toplevel()
        self.pant_reg.title("Registro Vehiculo")
        self.pant_reg.geometry(
            f'{self.pant_reg.winfo_screenwidth()}x{self.pant_reg.winfo_screenheight()}')
        self.pant_reg['bg'] = '#0059b3'
        Label(self.pant_reg, text=('REGISTRO VEHICULOS'), bg="#0059b3",
              font=('Britannic Bold', 25)).pack(side='top', pady=10)
        # FRAME DATOS VEHICULO
        frame_datos = LabelFrame(self.pant_reg)
        frame_datos.place(x=20, y=70, anchor=NW)
        Label(frame_datos, text=('DATOS VEHICULO'), font=(
            'Britannic Bold', 25)).grid(row=0, column=0, columnspan=3)

        Label(frame_datos, text="Fecha:", font=('Arial', 12)).grid(
            row=2, column=0, pady=30, ipadx=30)
        Label(frame_datos, text="Placa:", font=(
            'Arial', 12)).grid(row=3, column=0, ipadx=30)
        Label(frame_datos, text="Tipo Automovil", font=('Arial', 12)).grid(
            row=4, column=0, pady=30, ipadx=30)
        Label(frame_datos, text="Valor Total:", font=(
            'Arial', 12)).grid(row=5, column=0, ipadx=30)
        Label(frame_datos, text="Costo Materiales:", font=(
            'Arial', 12)).grid(row=6, column=0, pady=30, ipadx=30)
        Label(frame_datos, text="Descripcion Arreglos:", font=(
            'Arial', 12)).grid(row=7, column=0, ipadx=30)
        # #INPUTS

        entra_fecha = DateEntry(frame_datos, locale='es_ES', date_pattern='yyyy-MM-dd', font=('Arial', 12))
        entra_fecha.grid(row=2, column=1, pady=30, ipadx=30)

        entra_placa = Entry(frame_datos, width=17, font=('Arial', 12))
        entra_placa.grid(row=3, column=1, ipadx=30)

        entra_tipo = ttk.Combobox(frame_datos, font=(
            'Arial', 12), width=17, state='readonly')
        entra_tipo.set("Ingrese Opcion..")
        opciones = ["AUTOMOVIL", "CAMIONETA", "FURGON", "CAMION", "TRACTOMULA",
                    "VOLQUETA", "AMBULANCIA", "RETROESCABADORA", "TAXI", "OTRO"]
        entra_tipo['values'] = opciones
        entra_tipo.grid(row=4, column=1, ipadx=30, pady=30)

        entra_valor = Entry(frame_datos, width=17, font=('Arial', 12))
        entra_valor.grid(row=5, column=1, ipadx=30)

        entra_costos = Entry(frame_datos, width=17, font=('Arial', 12))
        entra_costos.grid(row=6, column=1, ipadx=30)

        entra_arreglos = Text(frame_datos, width=17, font=('Arial', 12))
        entra_arreglos.config(width=35, height=8, font='arial')
        entra_arreglos.grid(row=7, column=1, ipadx=30)

        # Button
        btn_salir = Button(self.pant_reg, text="Salir", width=25, font=(
            'Arial', 15), command=lambda: salir())
        btn_salir.pack(side='bottom', pady=50)

        btn_guardaDatos = Button(frame_datos, text="Guardar", width=20, font=('Arial', 12), command=lambda: guardar(
            entra_fecha.get().upper(),
            entra_placa.get().upper(),
            entra_valor.get().upper(),
            entra_tipo.get().upper(),
            entra_costos.get().upper(),
            entra_arreglos.get("1.0", "end-1c").upper()
        ))
        btn_guardaDatos.grid(row=8, column=1, pady=30)

        btn_limpiar = Button(frame_datos, text="Limpiar", width=20, font=(
            'Arial', 12), command=lambda: limpiar_campos())
        btn_limpiar.grid(row=8, column=0, pady=30)

        # FRAME BUSCAR

        frame_buscar = LabelFrame(self.pant_reg)
        frame_buscar.place(x=665, y=70)
        Label(frame_buscar, text=('BUSCAR VEHICULO'), font=(
            'Britannic Bold', 25)).grid(row=0, column=0, columnspan=3)

        Label(frame_buscar, text="Ingrese Placa: ", font=(
            'Arial', 12)).grid(row=2, column=0, pady=30)
        entra_placaBuscar = Entry(frame_buscar, font=('Arial', 12))
        entra_placaBuscar.grid(row=2, column=1)

        # Button

        btn_buscar = Button(frame_buscar, width=13, text='Buscar', font=(
            'Arial', 12), command=lambda: buscar_vehiculo(entra_placaBuscar.get().upper()))
        btn_buscar.grid(row=2, column=2)

        btn_mostrar = Button(frame_buscar, width=13,text='Mostar', font=('Arial', 12),command=lambda:limpiar_resultados())
        btn_mostrar.grid(row=2, column=3)
        
                
        # FRAME DETALLES
        frame_detalles=LabelFrame(self.pant_reg)
        frame_detalles.place(x=665,y=500)
        Label(frame_detalles,text='DETALLES',font=('Britannic Bold', 15)).pack()

        # TABLA DATOS VEHICULO

        style = ttk.Style(frame_buscar)
        style.configure('Treview', rowheight=50)

        Tabla_Datos = ttk.Treeview(frame_buscar, columns=[f"#{n}" for n in range(0, 6)])

        Tabla_Datos.grid(row=3, column=0, padx=80, pady=25, columnspan=5)

        Tabla_Datos.column("#0", width=1, minwidth=0, stretch=False)
        Tabla_Datos.column("#1", width=90, minwidth=40, stretch=False)
        Tabla_Datos.column("#2", width=80, minwidth=40, stretch=False)
        Tabla_Datos.column("#3", width=90, minwidth=60, stretch=False)
        Tabla_Datos.column("#4", width=80, minwidth=40, stretch=False)
        Tabla_Datos.column("#5", width=90, minwidth=40, stretch=False)
        Tabla_Datos.column("#6", width=80, minwidth=40, stretch=False)

        Tabla_Datos.heading('#1', text='Fecha', anchor=CENTER)
        Tabla_Datos.heading('#2', text='Placa', anchor=CENTER)
        Tabla_Datos.heading('#3', text='Tipo Vehiculo', anchor=CENTER)
        Tabla_Datos.heading('#4', text='Valor', anchor=CENTER)
        Tabla_Datos.heading('#5', text='Repuestos', anchor=CENTER)
        Tabla_Datos.heading('#6', text='Arreglos', anchor=CENTER)

        def limpiar_resultados():
            records = Tabla_Datos.get_children()
            for elementos in records:
                Tabla_Datos.delete(elementos)
            
        def buscar_vehiculo(placa):
            records = Tabla_Datos.get_children()
            for elementos in records:
                Tabla_Datos.delete(elementos)
            try:
                if placa == '':
                    mb.showerror(
                        "Cuidado", "Algun Campo Vacio O Algun Dato Mal Digitado")
                else:
                    query = '''Set lc_monetary TO 'es_CO.UTF-8'; SELECT fecha,placa,tipo,valor::money,costos::money,arreglos
                    FROM electro WHERE PLACA = '%s' ''' % placa
                    cursor, conn = conexion_bd(query, placa)
                    datos = cursor.fetchall()
                    conn.close()
                    if not datos:
                        mb.showwarning("ATENCION", "VEHICULO NO ENCONTRADO")
                    else:
                        for i in datos:
                            item = Tabla_Datos.insert("", 0, values=i)
                            Label(frame_detalles, text=f"Placa : {Tabla_Datos.set(item, '#2')} Costo Total: {Tabla_Datos.set(item, '#4')} Reparaciones: {Tabla_Datos.set(item, '#6')}").pack()

            except:
                mb.showerror("ERROR", "ALGO MALO PASO")


        def limpiar_campos():
            # entra_fecha.delete(0,END)
            entra_placa.delete(0, END)
            entra_valor.delete(0, END)
            entra_tipo.set("Ingrese Opcion..")
            entra_costos.delete(0, END)
            entra_arreglos.delete(1.0, END)

        def salir():
            self.pant_reg.destroy()
            self.ini.destroy()

        self.ini.withdraw()
        self.pant_reg.mainloop()

    def generar_reporte(self):
        from backEnd import conexion_bd
        self.pant_repo = Toplevel()
        self.pant_repo.title("Electro Aires App")
        self.pant_repo.geometry('1100x600')
        self.pant_repo['bg'] = '#0059b3'
        self.pant_repo.minsize(width=600, height=(self.pant_repo.winfo_screenheight())-100)
        self.pant_repo.resizable(False, False)
        
        Label(self.pant_repo,text="Estipular un rango de fechas para generar un informe de ingresos \nen dicho periodo de tiempo",font=('Britannic Bold', 15),bg='#0059b3').grid(row=1,column=1,columnspan=8,pady=50,padx=20)
        Label(self.pant_repo,text='Fechas' ,font=('Britannic Bold',12)).place()
        entra_fechaA = DateEntry(self.pant_repo, locale='es_ES', date_pattern='yyyy-MM-dd', font=('Arial', 12),width=15)
        entra_fechaA.place(x=100,y=150)
        
        entra_fechaB = DateEntry(self.pant_repo, locale='es_ES',width=15, date_pattern='yyyy-MM-dd', font=('Arial', 12))
        entra_fechaB.place(x=330,y=150)

        btn_generar=Button(self.pant_repo,text='GENERAR',width=17,font=('Arial',12),command=lambda:resultados_reporte(entra_fechaA.get(),entra_fechaB.get()))
        btn_generar.place(x=210,y=200)  
        
        Label(self.pant_repo,text="Resultados",font=('Britannic Bold',17),bg='#0059b3').place(x=70,y=280)

        # PANTALLA FECHAS 
        
        style = ttk.Style(self.pant_repo)
        style.configure('Treview', rowheight=50)

        Tabla_Fechas = ttk.Treeview(self.pant_repo, columns=[f"#{n}" for n in range(0,4)],height=30)

        Tabla_Fechas.place(x=650,y=20)

        Tabla_Fechas.column("#0", width=1, minwidth=0, stretch=False)
        Tabla_Fechas.column("#1", width=100, minwidth=100, stretch=False)
        Tabla_Fechas.column("#2", width=100, minwidth=100, stretch=False)
        Tabla_Fechas.column("#3", width=100, minwidth=100, stretch=False)
        Tabla_Fechas.column("#4", width=100, minwidth=100, stretch=False)

        Tabla_Fechas.heading('#1', text='Fecha', anchor=CENTER)
        Tabla_Fechas.heading('#2', text='Tipo Vehiculo', anchor=CENTER)
        Tabla_Fechas.heading('#3', text='Valor', anchor=CENTER)
        Tabla_Fechas.heading('#4', text='Repuestos', anchor=CENTER)
        #scrollbar
        verscrlbar = ttk.Scrollbar(self.pant_repo, orient="vertical", command=Tabla_Fechas.yview)
        verscrlbar.place(x=1053,y=21, height=404+221)
        Tabla_Fechas.configure(yscrollcommand=verscrlbar.set)

        # btn_salir = Button(self.pant_repo, text="Salir", width=25, font=(
        #     'Arial', 15), command=lambda: salir())
        
        def limpiar_resultados():
            records = Tabla_Fechas.get_children()
            for elementos in records:
                Tabla_Fechas.delete(elementos)


        

        def resultados_reporte(fechaA,fechaB):
            records = Tabla_Fechas.get_children()
            for elementos in records:
                Tabla_Fechas.delete(elementos)
            try:
                if fechaA == '' or fechaB == '':
                    mb.showwarning('ALERTA',"INGRESE LAS FECHAS")
                else:
                    query=''' SELECT fecha,tipo,valor::money,costos::money FROM electro WHERE fecha between %s and %s'''
                    cursor, conn =conexion_bd(query,(fechaA,fechaB))
                    datos = cursor.fetchall()
                    conn.close()
                    for i in datos:
                        Tabla_Fechas.insert("",0,values=i)
                    
            except:
                mb.showerror('ERROR','Algo salio MAL')

        def salir():
            self.pant_repo.destroy()
            self.ini.destroy()

        # btn_salir.grid(row=5,column=3,pady=50)
        # self.ini.withdraw()
        self.pant_repo.mainloop()

    def inventario(self):
        from backEnd import conexion_bd
        self.panta_inve=Toplevel()
        self.panta_inve.title("Inventario")
        self.panta_inve.geometry('1100x600')
        
        Label(self.panta_inve,text="INVENTARIO",font=('Britannic Bold',25)).pack(side='top')
        frame_inventario=Frame(self.panta_inve)
        frame_inventario.pack(side="top",pady=20)
        
        frame_Tablainventario=Frame(self.panta_inve)
        frame_Tablainventario.pack(side="top",pady=20)
        
        
        Label(frame_inventario,text="Nombre Producto: ",font=('Arial',12)).grid(row=1,column=1)
        entra_producto=Entry(frame_inventario,width=17)
        entra_producto.grid(row=1,column=2,pady=10,padx=20)
        
        Label(frame_inventario,text="Cantidad: ",font=('Arial',12)).grid(row=2,column=1)
        entra_Cantproducto=Entry(frame_inventario,width=17)
        entra_Cantproducto.grid(row=2,column=2,pady=10,padx=20)
        
        Label(frame_inventario,text="Precio Compra: ",font=('Arial',12)).grid(row=1,column=3)
        entra_productoCompra=Entry(frame_inventario,width=17)
        entra_productoCompra.grid(row=1,column=4,pady=10,padx=20)
        
        Label(frame_inventario,text="Precio Venta: ",font=('Arial',12)).grid(row=2,column=3)
        entra_productoVenta=Entry(frame_inventario,width=17)
        entra_productoVenta.grid(row=2,column=4,pady=10,padx=20)
        
        btn_agregar=Button(frame_inventario,text='AGREGAR',width=17,font=('Arial',10),command=lambda:guardar_productos(
            entra_producto.get().upper(),
            entra_Cantproducto.get().upper(),
            entra_productoCompra.get().upper(),
            entra_productoVenta.get().upper()
            ))
        btn_agregar.grid(row=3,column=2)
        
        btn_actualizar=Button(frame_inventario,text='ACTUALIZAR',width=17,font=('Arial',10))
        btn_actualizar.grid(row=3,column=3)
        
                
        btn_eliminar=Button(frame_inventario,text='MOSTRAR',width=17,font=('Arial',10),command=lambda:mostrar_productos())
        btn_eliminar.grid(row=3,column=4)
        
        style = ttk.Style(self.panta_inve)
        style.configure('Treview', rowheight=50)

        Tabla_inventario = ttk.Treeview(frame_Tablainventario, columns=[f"#{n}" for n in range(0,5)],height=15)

        Tabla_inventario.grid(row=0,column=0)

        Tabla_inventario.column("#0", width=1, minwidth=0, stretch=False)
        Tabla_inventario.column("#1", width=200, minwidth=100, stretch=False)
        Tabla_inventario.column("#2", width=200, minwidth=100, stretch=False)
        Tabla_inventario.column("#3", width=200, minwidth=100, stretch=False)
        Tabla_inventario.column("#4", width=200, minwidth=100, stretch=False)
        Tabla_inventario.column("#5", width=200, minwidth=100, stretch=False)
        
        Tabla_inventario.heading('#1', text='ID Producto', anchor=CENTER)
        Tabla_inventario.heading('#2', text='Nombre Producto', anchor=CENTER)
        Tabla_inventario.heading('#3', text='Cantidad', anchor=CENTER)
        Tabla_inventario.heading('#4', text='Precio Compra', anchor=CENTER)
        Tabla_inventario.heading('#5', text='Precio Venta', anchor=CENTER)
        #scrollbar
        verscrlbar = ttk.Scrollbar(self.panta_inve, orient="vertical", command=Tabla_inventario.yview)
        verscrlbar.place(x=1030,y=210, height=320)
        Tabla_inventario.configure(yscrollcommand=verscrlbar.set)
        
        
        # GUARDAR PRODUCTOS INVENTARIO
        def guardar_productos(nom_produc,cantidad,compra,venta):
            records=Tabla_inventario.get_children()
            for i in records:
                Tabla_inventario.delete(i)
            try:
                if nom_produc =='' or cantidad=='' or compra=='' or venta=='':
                    mb.showerror(
                        "Cuidado", "Algun Campo Vacio O Algun Dato Mal Digitado")
                else:
                    query='''INSERT INTO INVENTARIO VALUES (%s,%s,%s,%s)'''
                    conexion_bd(query,(nom_produc,cantidad,compra,venta))
                    
                    query2=''' SELECT ID_PRODUCT,PRODUCT_NAME,CANTIDAD,COMPRA::MONEY,VENTA::MONEY FROM INVENTARIO'''
                    cursor,conn=conexion_bd(query2,(nom_produc,cantidad,compra,venta))
                    datos=cursor.fetchall()
                    conn.close()
                    for i in datos:
                        Tabla_inventario.insert("",0,values=i)
                        
            except:
                mb.showerror("ERROR","ALGO SALIO MAL")
                        # GUARDAR PRODUCTOS INVENTARIO
        def mostrar_productos():
            records=Tabla_inventario.get_children()
            for i in records:
                Tabla_inventario.delete(i)            
            query2=''' SELECT ID_PRODUCT,PRODUCT_NAME,CANTIDAD,COMPRA::MONEY,VENTA::MONEY FROM INVENTARIO'''
            cursor,conn=conexion_bd(query2,())
            datos=cursor.fetchall()
            conn.close()
            for i in datos:
                Tabla_inventario.insert("",0,values=i)

        # self.ini.withdraw()
        self.panta_inve.mainloop()
    



if __name__ == '__main__':
    Inicio = Tk()
    Aplicacion = Electro(Inicio)
    Inicio.mainloop()
