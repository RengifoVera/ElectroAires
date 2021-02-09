from tkinter import Button,LabelFrame,Label,Frame,Entry,Text,Tk,PhotoImage,Toplevel,CENTER,END,StringVar
from tkinter import ttk
import psycopg2
from tkcalendar import DateEntry
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from tkinter import messagebox as mb
import os 
from datetime import date
class Electro:
    def __init__(self,inicio):
        self.ini=inicio
        self.ini.title("Electro Aires & Aires")
        self.ini.geometry('500x600')
        self.ini.resizable(0,0)
        #Crear Frame Inicio
        img=PhotoImage(file="./Imagenes/inicio.png")
        lbl_imagen=Label(self.ini,image=img)
        lbl_imagen.pack()
        lbl_imagen.img=img
        frame_inicio=Frame(self.ini)
        frame_inicio.pack()
        Label(self.ini,text="Desarrollado Por ©JhonJRVera™",font=("Impact",9)).pack(side="bottom")
    
        btn_registro=Button(frame_inicio,text='Registar Automovil',font=("Arial",12),width=20,command = self.Registrar_auto)
        btn_registro.grid(row=2,column=3,pady=10)

        btn_generar=Button(frame_inicio,text='Generar Reporte',font=("Arial",12),width=20,command=self.Generar_Reporte)
        btn_generar.grid(row=2,column=4,padx=10,pady=10)

        btn_factura=Button(frame_inicio,text='Generar Factura',font=("Arial",12),width=20,command=self.Generar_factura)
        btn_factura.grid(row=4,column=3,pady=10,columnspan=2)

        btn_salir=Button(frame_inicio,text='Salir',font=("Arial",12),width=10,command=lambda:Salir())
        btn_salir.grid(row=5,column=3,pady=10,columnspan=2)
        def Salir():
            self.ini.destroy()
        
        self.ini.mainloop()
    def Generar_Reporte(self):
        self.pantalla_reporte=Toplevel()
        self.pantalla_reporte.geometry('1100x600')
        self.pantalla_reporte.title("Reporte De Ingresos")
        self.pantalla_reporte.resizable(0,0)
        
        img_1=PhotoImage(file="./Imagenes/banner.png")
        Label(self.pantalla_reporte,image=img_1).pack()


        frame_reporte=Frame(self.pantalla_reporte)
        frame_reporte.place(x=50,y=120)


        Label(frame_reporte,text="Estipular dos(2) fechas \n para generar el reporte \nde ingresos en las fechas dadas",font=("Arial",12)).grid(row=0,column=0,pady=15,columnspan=3)
        #EJECUTA BUSQUEDA EN LA BASE DE DATOS
        def generar_Reporte(fecha_a,fecha_b):
            records=Tabla_Reporte.get_children()
            for elementos in records:
                Tabla_Reporte.delete(elementos)
            try:
                if entra_fechaA.get() == '' or entra_fechaB.get()=='':
                    mb.showerror("Cuidado","Ingrese Fechas")
                
                else:
                        conn=psycopg2.connect(
                            dbname="ElectroAires",
                            user="postgres",
                            password="vera",
                            host="localhost",
                            port="5432")
                        cursor=conn.cursor()
                        #MUESTRA VALOR TOTAL DE ARREGLOS IN UN RANGO DE FECHAS
                        query = ''' Set lc_monetary TO 'es_CO.UTF-8';
                                    SELECT sum(valor)::money
                                    from electro
                                    where fecha BETWEEN %s and %s
                                    '''                        
                        cursor.execute(query, (fecha_a,fecha_b))
                        row=cursor.fetchall()
                        def convertTuple(tup): 
                            str =  ''.join(tup) 
                            return str 
                        for x in row:
                            str=convertTuple(x)
                            Valor_total['text']=str
                       #MUESTRA VALOR TOTAL DE LOS REPUESTOS USADO 
                        query2 = ''' Set lc_monetary TO 'es_CO.UTF-8';
                                    SELECT sum(valor_materiales)::money
                                    from electro
                                    where fecha BETWEEN %s and %s
                                    '''                        
                        cursor.execute(query2, (fecha_a,fecha_b))
                        row=cursor.fetchall()
                        for z in row:
                            str=convertTuple(z)
                            Valor_total_repuestos['text']=str
                       #MUESTRA VALOR TERMIANDO CON LOS DESCUENTOS 
                        query2 = ''' Set lc_monetary TO 'es_CO.UTF-8';
                                    SELECT (sum(valor) - sum(valor_materiales))::money
                                    from electro
                                    where fecha BETWEEN %s and %s
                                    '''                        
                        cursor.execute(query2, (fecha_a,fecha_b))
                        row=cursor.fetchall()
                        for g in row:
                            str=convertTuple(g)
                            Valor_total_total['text']=str
                       #DISPLAY DATOS IN THE TABLA
                        query4='''Set lc_monetary TO 'es_CO.UTF-8'; 
                        SELECT fecha,marca,valor::money,valor_materiales::money from electro '''
                        cursor.execute(query4)
                        datos=cursor.fetchall()
                        for y in datos:
                            Tabla_Reporte.insert("",0,values=y)
                        conn.commit()
                        conn.close()
            except:
                mb.showerror("Cuidado","Algo sucedio con las fechas, mira bien")
        #Fecha A
        Label(frame_reporte,text="Fecha Desde: ",font=("Arial",12)).grid(row=2,column=0,pady=15)
        entra_fechaA=DateEntry(frame_reporte,locale='es_ES',date_pattern='yyyy-MM-dd',width=25)
        entra_fechaA.grid(row=3,column=0,pady=5)
        #Fecha B
        Label(frame_reporte,text="Fecha Hasta: ",font=("Arial",12)).grid(row=4,column=0,pady=15)
        entra_fechaB=DateEntry(frame_reporte,locale='es_ES',date_pattern='yyyy-MM-dd',width=25)
        entra_fechaB.grid(row=5,column=0,pady=5)
        #MUESTRA VALOR TOTAL MENSUAL

        Label(self.pantalla_reporte,text="VALOR TOTAL\nMES ELEGIDO").place(x=947,y=142)
        Valor_total=Label(self.pantalla_reporte,text="", width=15,borderwidth=2, relief="sunken",font=("calibri",12))
        Valor_total.place(x=930,y=180)

        Label(self.pantalla_reporte,text="VALOR TOTAL\nREPUESTOS\nMES ELEGIDO").place(x=947,y=210)
        Valor_total_repuestos=Label(self.pantalla_reporte,text="", width=15,borderwidth=2, relief="sunken",font=("calibri",12))
        Valor_total_repuestos.place(x=930,y=270)

        Label(self.pantalla_reporte,text="VALOR TOTAL\n DESCONTANDO\nREPUESTOS",fg='blue').place(x=947,y=310)
        Valor_total_total=Label(self.pantalla_reporte,text="", width=15,borderwidth=2, relief="sunken",font=("calibri",12))
        Valor_total_total.place(x=930,y=370)

        #Botones 
        btn_Reporte=Button(frame_reporte,text="Generar",font=("Arial",12),width=17,command=lambda:generar_Reporte(entra_fechaA.get(),entra_fechaB.get()))
        btn_Reporte.grid(row=9,column=0,pady=25)

        def salir_Reporte():
            self.ini.state(newstate="normal")
            self.pantalla_reporte.destroy()
            self.ini.deiconify()
        btn_SalirR=Button(frame_reporte,text="Salir",font=("Arial",12),width=15,command=lambda:salir_Reporte())
        btn_SalirR.grid(row=10,column=0,pady=5)

        Tabla_Reporte=ttk.Treeview(self.pantalla_reporte,columns=[f"#{n}" for n in range(0,4)],height=20)
        Tabla_Reporte.place(x=300,y=140)
        Tabla_Reporte.column("#0",width=0,minwidth=1)
        Tabla_Reporte.column("#1",width=150,minwidth=100,anchor=CENTER )
        Tabla_Reporte.column("#2",width=150,minwidth=100,anchor=CENTER )
        Tabla_Reporte.column("#3",width=150,minwidth=100,anchor=CENTER )
        Tabla_Reporte.column("#4",width=150,minwidth=100,anchor=CENTER )


        Tabla_Reporte.heading('#0', text = '')
        Tabla_Reporte.heading('#1', text = 'Fecha', anchor = CENTER)
        Tabla_Reporte.heading('#2', text = 'Marca', anchor = CENTER)
        Tabla_Reporte.heading('#3', text = 'Precio', anchor = CENTER)
        Tabla_Reporte.heading('#4', text = 'Valor Materiales', anchor = CENTER)
        
        #scrollbar
        verscrlbar = ttk.Scrollbar(self.pantalla_reporte, orient="vertical", command=Tabla_Reporte.yview)
        verscrlbar.place(x=905,y=142, height=200+223)
        Tabla_Reporte.configure(yscrollcommand=verscrlbar.set)




        self.ini.withdraw()
        self.pantalla_reporte.deiconify()
        self.pantalla_reporte.mainloop()
    def Registrar_auto(self):
        self.pantalla_registro=Toplevel()
        self.pantalla_registro.geometry('1080x768')
        self.pantalla_registro.title("Registro De Automoviles")
        self.pantalla_registro.resizable(0,0)
        #Funciones
        def salir():
            self.pantalla_registro.destroy()
            self.ini.destroy()
        #Imagen
        frame_imagen=Frame(self.pantalla_registro,width=1000,height=162)
        frame_imagen.pack()
        img_registro=PhotoImage(file='./Imagenes/banner.png')
        Label(frame_imagen,image=img_registro).place(x=0)


        #Creacion Frame Buscar Vehiculo
        frame_buscar=LabelFrame(self.pantalla_registro,width=500,height=500)
        frame_buscar.place(x=600,y=130)

        #Creacion Frame botones
        img_save=PhotoImage(file='./Imagenes/guardar.png')
        img_new=PhotoImage(file='./Imagenes/nuevo.png')
        img_undo=PhotoImage(file='./Imagenes/volver.png')
        img_quit=PhotoImage(file='./Imagenes/salir.png')
        frame_btn=Frame(self.pantalla_registro,width=500,height=500)
        frame_btn.place(x=470,y=130)
        #FUNCIONES PARA GUARDAR EN LA BASE DE DATOS
        def Guarda_DatosCarro(a,b,c,d,e,f,g):
            try:
                if entra_fecha.get()== '' or entra_marca.get()=='' or entra_tipo.get()=='Ingrese Opcion..' or entra_placa.get()=='' or entra_valor.get()==' ' or entra_arreglo.get("1.0","end")==' ' or entra_costoRepuesto.get()=="":
                        mb.showerror("Cuidado","Algun Campo Vacio O Algun Dato Mal Digitado")
                else:
                        conn=psycopg2.connect(
                            dbname="ElectroAires",
                            user="postgres",
                            password="vera",
                            host="localhost",
                            port="5432")
                        cursor=conn.cursor()
                        query=''' INSERT INTO electro VALUES(%s,%s,%s,%s,%s,%s,%s)'''
                        cursor.execute(query,(a,b,c,d,e,f,g))
                        
                        mb.showinfo("EXITO","Datos Guardados")
                        conn.commit()
                        conn.close()
                        limpiar_campos()
            except:
                    mb.showerror("Cuidado","Datos No Guardados")

        btn_save=Button(frame_btn,image=img_save,font=("Arial",12),command=lambda:Guarda_DatosCarro(
            entra_fecha.get().upper(),
            entra_marca.get().upper(),
            entra_tipo.get().upper(),
            entra_placa.get().upper(),
            entra_valor.get(),
            entra_arreglo.get("1.0","end").upper(),
            entra_costoRepuesto.get()))
        btn_save.grid(row=0,column=0)
        Label(frame_btn,text="Guardar",font=("Arial",12)).grid(row=1,column=0)
        def limpiar_campos():
            entra_marca.delete(0, END)
            entra_tipo.set("Ingrese Opcion..")
            entra_placa.delete(0, END)
            entra_valor.delete(0, END)
            entra_costoRepuesto.delete(0,END)
            entra_arreglo.delete("1.0",END)
           
        btn_new=Button(frame_btn,image=img_new,font=("Arial",12),command=lambda:limpiar_campos())
        btn_new.grid(row=2,column=0)
        Label(frame_btn,text="Nuevo",font=("Arial",12)).grid(row=3,column=0)
        def regresar():
            self.ini.state(newstate="normal")
            self.pantalla_registro.withdraw()
            self.ini.deiconify()
        btn_volver=Button(frame_btn,image=img_undo,font=("Arial",12),command=lambda:regresar())
        btn_volver.grid(row=4,column=0)
        Label(frame_btn,text="Volver",font=("Arial",12)).grid(row=5,column=0)

        btn_quit=Button(frame_btn,image=img_quit,font=("Arial",12),command=lambda:salir())
        btn_quit.grid(row=6,column=0)
        Label(frame_btn,text="Salir",font=("Arial",12)).grid(row=7,column=0)

        #Creacion Frame Registro
        frame_registro=LabelFrame(self.pantalla_registro,text='Registro Vehiculo   ',font=("Arial",12),width=500,height=500)
        frame_registro.place(x=120,y=130)

        Label(frame_buscar,text="BUSQUEDA DEL VEHICULO:  \n\n - Busca a todos los vehiculos arreglados, o uno en \nespecial digitando la placa del vehiculo a buscar \n\n - Eliminar datos de una vehiculo dada su placa  \n\n - Editar los datos de un vehiculo en especial ",font=("Arial",12)).grid(row=2,column=4,columnspan=5)
        btn_buscar=Button(frame_buscar,text="BUSQUEDA",font=("Arial",12),width=15,command=self.Buscar_auto)
        btn_buscar.grid(row=3,column=6,pady=30)

        Label(frame_buscar,text=" GARANTIA:\n\n En esta seccion se podra registrar un nuevo arreglo\n a un vehiculo dada su placa y si esta en la fecha adecuada\n que se estipulo para reclamar una garantia  ",font=("Arial",12)).grid(row=9,column=6)
     
        btn_garantia=Button(frame_buscar,text="GARANTIA",font=("Arial",12),command=self.Garantia)
        btn_garantia.grid(row=11,column=6,pady=15)
        #Espacio de registro carro
        Label(frame_registro,text="Fecha:",font=("Arial",12)).grid(row=0,column=0,pady=10)
        Label(frame_registro,text="Marca:",font=("Arial",12)).grid(row=1,column=0,pady=10)
        Label(frame_registro,text="Tipo Vehiculo:",font=("Arial",12)).grid(row=2,column=0,pady=10)
        Label(frame_registro,text="Placa:",font=("Arial",12)).grid(row=3,column=0,pady=10)
        Label(frame_registro,text="Valor:",font=("Arial",12)).grid(row=4,column=0,pady=10)
        Label(frame_registro,text="Costo Repuestos:",font=("Arial",12)).grid(row=5,column=0,pady=10)
        Label(frame_registro,text="Descripcion Arreglo:",font=("Arial",12)).grid(row=6,column=0,pady=10)
        entra_fecha=DateEntry(frame_registro,locale='es_ES',date_pattern='yyyy-MM-dd',width=25)
        entra_fecha.grid(row=0,column=1,pady=10)

        entra_marca=Entry(frame_registro,width=25)
        entra_marca.focus()
        entra_marca.grid(row=1,column=1,pady=10)

        entra_tipo=ttk.Combobox(frame_registro,width=25,state='readonly')
        entra_tipo.set("Ingrese Opcion..")
        opciones=["AUTOMOVIL","CAMIONETA","FURGON","CAMION","TRACTOMULA","VOLQUETA","AMBULANCIA","RETROESCABADORA","TAXI","OTRO"]
        entra_tipo['values']=opciones
        entra_tipo.grid(row=2,column=1,pady=10)

        entra_placa=Entry(frame_registro,width=25) 
        entra_placa.grid(row=3,column=1,pady=10)

        entra_valor=Entry(frame_registro,width=25) 
        entra_valor.grid(row=4,column=1,pady=10)

        entra_costoRepuesto=Entry(frame_registro,width=25)
        entra_costoRepuesto.grid(row=5,column=1,pady=10)

        entra_arreglo=Text(frame_registro)
        entra_arreglo.config(width=35, height=8,font='arial')
        entra_arreglo.grid(row=7,column=0,pady=10,columnspan=5)

        self.ini.withdraw()
        self.pantalla_registro.state(newstate="normal")
        self.pantalla_registro.deiconify()
        self.pantalla_registro.mainloop()
    def Buscar_auto(self):

        self.pantalla_buscar=Toplevel()
        self.pantalla_buscar.geometry('1300x600')
        self.pantalla_buscar.title("Busqueda De Automoviles")
        #self.pantalla_buscar.resizable(0,0)
        
        img_1=PhotoImage(file="./Imagenes/banner.png")
        Label(self.pantalla_buscar,image=img_1).pack()

        #Creacion Frame Buscar
        frame_buscar=LabelFrame(self.pantalla_buscar,text=" Buscar  ")
        frame_buscar.place(x=50,y=120)

        Label(frame_buscar,text="Buscar Vehiculo",font=("Arial",12)).grid(row=0,column=0,pady=20,columnspan=2)


        entra_buscarPlaca=Entry(frame_buscar,font=("Arial",12),width=17)
        entra_buscarPlaca.grid(row=2,column=2,columnspan=2)
        #limpia entrada de texto de busqueda
        def limpiar(event):
           event.widget.delete(0,END)
        entra_buscarPlaca.insert(0,"Ingrese Placa...")
        entra_buscarPlaca.bind("<Button-1>",limpiar)
        def buscar_placa(placa):
            records=Tabla_Datos.get_children()
            for elementos in records:
                Tabla_Datos.delete(elementos)
            try:
                if entra_buscarPlaca.get()=='Ingrese Placa...' or  entra_buscarPlaca.get()==" " :
                    mb.showerror("Cuidado","Ingrese Placa a BUSCAR")
                else:
                    conn=psycopg2.connect(
                        dbname="ElectroAires",
                        user="postgres",
                        password="vera",
                        host="localhost",
                        port="5432")
                    cursor=conn.cursor()
                    query= '''Set lc_monetary TO 'es_CO.UTF-8';
                    select fecha,marca,tipo_carro,placa,valor::money,arreglo,fecha_ingreso,arreglo_nuevo 
                    from electro WHERE PLACA = '%s' ''' %  entra_buscarPlaca.get().upper()
                    cursor.execute(query,(placa))
                    row=cursor.fetchall()
 
                    for x in row:
                        Tabla_Datos.insert("",0,values=x)
                    conn.commit()
                    conn.close()
                    entra_buscarPlaca.delete(0, END)
                    
            except:	
                    mb.showerror("Cuidado","Vehiculo No ENCONTRADO")

        btn_buscarPlaca=Button(frame_buscar,text="Buscar ",font=("Arial",12),width=20,command=lambda:buscar_placa(entra_buscarPlaca.get()))
        btn_buscarPlaca.grid(row=2,column=3,columnspan=5,padx=10)
        

        #Tabla



        style = ttk.Style(frame_buscar)
        style.configure('Treeview', rowheight=30)

        Tabla_Datos=ttk.Treeview(frame_buscar,columns=[f"#{n}" for n in range(0,8)])
        Tabla_Datos.grid(row=4,column=0,columnspan=10,pady=25)
        Tabla_Datos.column("#0",width=1,minwidth=0,stretch = False )
        Tabla_Datos.column("#1",width=100,minwidth=100,stretch = False )
        Tabla_Datos.column("#2",width=100,minwidth=100,stretch = False )
        Tabla_Datos.column("#3",width=150,minwidth=100,stretch = False )
        Tabla_Datos.column("#4",width=100,minwidth=100,stretch = False )
        Tabla_Datos.column("#5",width=100,minwidth=100,stretch = False ) 
        Tabla_Datos.column("#6",width=300,minwidth=100 )
        Tabla_Datos.column("#7",width=150,minwidth=150,stretch = False )
        
        Tabla_Datos.heading('#1', text = 'Fecha', anchor = CENTER)
        Tabla_Datos.heading('#2', text = 'Marca', anchor = CENTER)
        Tabla_Datos.heading('#3', text = 'Tipo Vehiculo', anchor = CENTER)
        Tabla_Datos.heading('#4', text = 'Placa', anchor = CENTER)
        Tabla_Datos.heading('#5', text = 'Valor', anchor = CENTER)
        Tabla_Datos.heading('#6', text = 'Arreglos')
        Tabla_Datos.heading('#7', text = 'Fecha Garantia', anchor = CENTER)
        Tabla_Datos.heading('#8', text = 'Trabajo Garantia', anchor = CENTER)
        #scrollbar
        verscrlbar = ttk.Scrollbar(frame_buscar, orient="vertical", command=Tabla_Datos.yview)
        verscrlbar.place(x=1187,y=122, height=200+127)
        Tabla_Datos.configure(yscrollcommand=verscrlbar.set)
        
      
        #Botones Pantalla Buscar
        def salir_buscar():
            self.pantalla_registro.state(newstate="normal")
            self.pantalla_buscar.destroy()
            self.pantalla_registro.deiconify()
        btn_eliminar=Button(frame_buscar,text="Eliminar",width=15,font=("Arial",12),command=lambda:eliminar_auto(entra_buscarPlaca.get()))
        btn_eliminar.grid(row=5,column=4,padx=5)
        btn_salir=Button(frame_buscar,text="Salir",font=("Arial",12),width=15,command=lambda:salir_buscar())
        btn_salir.grid(row=5,column=3,padx=5)
        btn_mostrar=Button(frame_buscar,text="Mostrar Todo",font=("Arial",12),width=15,command=lambda:all_data())
        btn_mostrar.grid(row=5,column=2,padx=5)

        btn_editar=Button(frame_buscar,text="Editar",font=("Arial",12),width=15,command=lambda:Editar_auto())
        btn_editar.grid(row=5,column=1)
        #FUNCION DE ELIMINACION DE DATOS DEL VEHICULO
        def eliminar_auto(placa):
            records=Tabla_Datos.get_children()
            for elementos in records:
                Tabla_Datos.delete(elementos)
            try:
                if entra_buscarPlaca.get()=="Ingrese Placa..." or entra_buscarPlaca.get()=='':
                    mb.showerror("Cuidado","Ingrese Placa")
                else:
                    conn=psycopg2.connect(
                                dbname="ElectroAires",
                                user="postgres",
                                password="vera",
                                host="localhost",
                                port="5432")
                    cursor=conn.cursor()
                    query= '''delete from electro WHERE PLACA = '%s' ''' %  entra_buscarPlaca.get().upper()
                    cursor.execute(query,(placa))
                    mb.showinfo("Electro Aires","Vehiculo ELIMINADO")
                    conn.commit()
                    conn.close()
            except:
                mb.showinfo("Cuidado","Vehiculo NO Eliminado")
        #FUNCION QUE EDITA LOS DATOS DE UN VEHICULO DADA SU PLACA
        def Editar_auto():
            if Tabla_Datos.item(Tabla_Datos.selection())['values']=='':
                mb.showerror("Cuidado","Seleccion datos a Editar")
            else:
                #PANTALLA EDITAR DATOS
                pantalla_editar=Toplevel()
                pantalla_editar.title("Editar Datos Vehiculo")
                #pantalla_editar.resizable(0,0)
                img_1=PhotoImage(file="./Imagenes/b_buscar.png")
                Label(pantalla_editar,image=img_1).pack()
                frame_editar=LabelFrame(pantalla_editar,text="Editar datos Vehiculo",font=("Arial",10))
                frame_editar.pack()
                #CAPTURA LOS DATOS DE LA TABLA 
                fecha=Tabla_Datos.item(Tabla_Datos.selection())['values'][0]
                marca= Tabla_Datos.item(Tabla_Datos.selection())['values'][1]
                tipo=Tabla_Datos.item(Tabla_Datos.selection())['values'][2]
                placa=Tabla_Datos.item(Tabla_Datos.selection())['values'][3]
                valor=Tabla_Datos.item(Tabla_Datos.selection())['values'][4]
                arreglos=Tabla_Datos.item(Tabla_Datos.selection())['values'][5]

                Label(frame_editar, text = 'Fecha:',font=("Arial",12)).grid(row = 0, column = 1)
                Entry(frame_editar, textvariable = StringVar(frame_editar, value = fecha), state = 'readonly',width=25).grid(row = 0, column = 2,pady=15,padx=15)

                Label(frame_editar, text = 'Marca:',font=("Arial",12)).grid(row = 2, column = 1)
                Entry(frame_editar, textvariable = StringVar(frame_editar, value = marca), state = 'readonly',width=25).grid(row = 2, column = 2,pady=15,padx=15)

                Label(frame_editar, text = 'Tipo Carro:',font=("Arial",12)).grid(row = 3, column = 1)
                Entry(frame_editar, textvariable = StringVar(frame_editar, value = tipo), state = 'readonly',width=25).grid(row = 3, column = 2,pady=1,padx=15)

                Label(frame_editar, text = 'Placa:',font=("Arial",12)).grid(row = 0, column = 4,padx=15)
                old_placa=Entry(frame_editar, textvariable = StringVar(frame_editar, value = placa), state = 'readonly',width=25)
                old_placa.grid(row = 0, column = 5,pady=15,padx=15)

                Label(frame_editar, text = 'Valor:',font=("Arial",12)).grid(row = 2, column = 4,padx=15)
                Entry(frame_editar, textvariable = StringVar(frame_editar, value = valor), state = 'readonly',width=25).grid(row = 2, column = 5,pady=15,padx=15)

                Label(frame_editar, text = 'Arreglos:',font=("Arial",12)).grid(row = 3, column = 4,padx=15 )
                Entry(frame_editar, textvariable = StringVar(frame_editar, value = arreglos),state='readonly',width=25).grid(row = 3, column = 5,pady=15,padx=15)

                #SEPARACION DE DATOS VIEJOS CON LOS NUEVOS
                Label(frame_editar,text="Ingreso de nuevos datos",font=("Arial",12),fg="blue").grid(row=6,column=1,columnspan=2)

                Label(frame_editar, text = 'Nueva Marca:',font=("Arial",12)).grid(row = 7, column = 1)
                N_marca=Entry(frame_editar, width=25)
                N_marca.grid(row = 7, column = 2,pady=15,padx=15)

                Label(frame_editar, text = 'Nuevo Tipo Carro:',font=("Arial",12)).grid(row = 8, column = 1)
                N_Tc=ttk.Combobox(frame_editar,width=25,state='readonly')
                N_Tc.set("Ingrese Opcion..")
                opciones=["AUTOMOVIL","CAMIONETA","FURGON","CAMION","TRACTOMULA","VOLQUETA","AMBULANCIA","RETROESCABADORA","TAXI","OTRO"]
                N_Tc['values']=opciones
                N_Tc.grid(row = 8, column = 2,pady=1,padx=15)
                
                # Label(frame_editar, text = 'Nuevo Arreglo:',font=("Arial",12)).grid(row = 9, column = 1)
                # n_arreglo=Text(frame_editar)
                # n_arreglo.config(width=35, height=8,font='arial')
                # n_arreglo.grid(row=9,column=2,pady=10,columnspan=2)

                Label(frame_editar, text = 'Nueva Placa:',font=("Arial",12)).grid(row = 7, column = 4,padx=15)
                N_placa=Entry(frame_editar,width=25)
                N_placa.grid(row = 7, column = 5,pady=15,padx=15)

                Label(frame_editar, text = 'Nuevo Valor:',font=("Arial",12)).grid(row = 8, column =4,padx=15)
                N_Valor=Entry(frame_editar, width=25)
                N_Valor.grid(row = 8, column = 5,pady=15,padx=15)


                btn_Actualizar=Button(frame_editar,text="Actualizar",font=("Arial",12),width=17,command=lambda:guardar_edicion(
                    N_marca.get().upper(),
                    N_placa.get().upper(),
                    N_Tc.get().upper(),
                    N_Valor.get(),
                    old_placa.get().upper()
                    #,n_arreglo.get("1.0",END).upper()
                   ))
                btn_Actualizar.grid(row=11,column=1,pady=15,columnspan=5)


                btn_salir=Button(frame_editar,text="Salir",font=("Arial",12),width=15,command=lambda:salir())
                btn_salir.grid(row=12,column=1,pady=15,columnspan=5)


                def salir():
                    pantalla_editar.destroy()
                #GUARDA DATOS EDITADOS
                def guardar_edicion(A,B,C,D,E):
                    try:
                        if N_Tc.get()=='Ingrese Opcion..' or N_Valor.get()=='':
                            mb.showerror("Cuidado","Ingrese NUEVO VALOR O NUEVO TIPO CARRO")
                        else:    
                            conn=psycopg2.connect(
                                        dbname="ElectroAires",
                                        user="postgres",
                                        password="vera",
                                        host="localhost",
                                        port="5432")
                            cursor=conn.cursor()
                            query='''update electro set marca=%s , placa=%s, tipo_carro=%s,valor=%s where placa=%s '''
                            cursor.execute(query,(A,B,C,D,E))
                            conn.commit()
                            conn.close()
                            mb.showinfo("Electro Aires","Datos actualizados CORRECTAMENTE")

                    except:
                        mb.showerror("Error","Datos No Guardados")

                pantalla_editar.mainloop()
        #MUESTRA TODOS LOS DATOS DE LA BASE DE DATOS
        def all_data():
            records=Tabla_Datos.get_children()
            for elementos in records:
                Tabla_Datos.delete(elementos)
            conn=psycopg2.connect(
                        dbname="ElectroAires",
                        user="postgres",
                        password="vera",
                        host="localhost",
                        port="5432")
            cursor=conn.cursor()
            query= '''Set lc_monetary TO 'es_CO.UTF-8';
                    select fecha,marca,tipo_carro,placa,valor::money,arreglo,fecha_ingreso,arreglo_nuevo 
                    from electro '''
            cursor.execute(query)
            row=cursor.fetchall()
 
            for x in row:
                Tabla_Datos.insert("",0,values=x)
            conn.commit()
            conn.close()
        self.pantalla_buscar.state(newstate="zoomed")
        self.pantalla_buscar.mainloop()     
    def Generar_factura(self):

        self.pantalla_factura=Toplevel()
        self.pantalla_factura.title("Generar Factura")
        self.pantalla_factura.geometry('700x550')
        self.pantalla_factura.resizable(0,0)
        #Imagen
        img_1=PhotoImage(file="./Imagenes/b_buscar.png")
        Label(self.pantalla_factura,image=img_1).pack()
        #Frame factura
        frame_factura=Frame(self.pantalla_factura)
        frame_factura.place(x=120,y=120)
        #Fecha
        Label(frame_factura,text="Fecha: ",font=("Arial",12)).grid(row=2,column=0,pady=15)
        entra_fechaF=DateEntry(frame_factura,locale='es_ES',date_pattern='yyyy-MM-dd',width=20)
        entra_fechaF.grid(row=2,column=2,pady=5)

        Label(frame_factura,text="Factura N°",font=("Arial",12)).grid(row=3,column=0,columnspan=2,pady=10)
        entra_venta=Entry(frame_factura,width=20)
        entra_venta.focus()
        entra_venta.grid(row=3,column=2,padx=15)


        Label(frame_factura,text="Cliente",font=("Arial",12)).grid(row=4,column=0,pady=10)
        entra_cliente=Entry(frame_factura,width=20)
        entra_cliente.grid(row=4,column=2)

        
        Label(frame_factura,text="CC-NIT",font=("Arial",12)).grid(row=5,column=0,pady=10)
        entra_id=Entry(frame_factura,width=20)
        entra_id.grid(row=5,column=2)

        Label(frame_factura,text="Tipo Carro",font=("Arial",12)).grid(row=6,column=0,pady=10)
        entra_carro=ttk.Combobox(frame_factura,width=20,state='readonly')
        entra_carro.set("Ingrese Opcion..")
        opciones=["AUTOMOVIL","CAMIONETA","FURGON","CAMION","TRACTOCAMION","VOLQUETA","AMBULANCIA","RETROESCABADORA","TAXI","OTRO"]
        entra_carro['values']=opciones
        entra_carro.grid(row=6,column=2)

        Label(frame_factura,text="Placa",font=("Arial",12)).grid(row=7,column=0,pady=10)
        entra_placa=Entry(frame_factura,width=20)
        entra_placa.grid(row=7,column=2)

        Label(frame_factura,text="Descripcion",font=("Arial",12)).grid(row=2,column=4,pady=10)
        entra_desc=Text(frame_factura,width=20)
        entra_desc.config(width=35, height=8,font='arial')
        entra_desc.grid(row=3,column=4,rowspan=4,columnspan=4)


        Label(frame_factura,text="Valor Total",font=("Arial",12)).grid(row=8,column=0,pady=10)
        entra_valorF=Entry(frame_factura,width=20)
        entra_valorF.grid(row=8,column=2)

        def salir():
            self.pantalla_factura.destroy()
            self.ini.state(newstate="normal")
            self.ini.deiconify()
        
        btn_salir_fac=Button(frame_factura,text="Salir",font=("Arial",12),width=10,command=lambda:salir())
        btn_salir_fac.grid(row=15,column=6,columnspan=2)
        
        def gen_factura():
            if entra_venta.get()=='' or entra_cliente.get()=='' or entra_id.get()=='' or entra_carro.get()=='' or entra_placa.get()==''  or entra_valorF.get()=='' :
                mb.showerror("Cuidado","No puede dejar cuadros de entrada de vacíos")
            elif  entra_desc.get("1.0","end")==" ":
                mb.showerror("Cuidado","No puede dejar cuadros de entrada de vacíos")
            else:
                
                c = canvas.Canvas("Factura-ElectroAires-"+ str(date.today())+".pdf",pagesize=letter)
                # Para titulos asignamos una fuente y el tamaño = 14
                c.setFont('Helvetica', 14)
                # Dibujamos una imagen (IMAGEN, X,Y, WIDTH, HEIGH)
                c.drawImage('./Imagenes/factu.png', 0, 0,612,792)
                #entradad de texto
                fecha=entra_fechaF.get()
                nufact=entra_venta.get()
                cliente=entra_cliente.get().upper()
                iden=entra_id.get()
                carro=entra_carro.get().upper()
                placa=entra_placa.get().upper()
                desc=entra_desc.get("1.0","end")
                valor=entra_valorF.get()

                # Dibujamos texto: (X,Y,Texto)
                c.drawString(70,600,"Fecha:")
                c.drawString(125,600,fecha)

                c.drawString(400,600,"N° Factura")
                c.drawString(480,600,nufact)

                c.drawString(70,575,"Cliente:")
                c.drawString(125,575,cliente)

                c.drawString(400,575,"Nit:")
                c.drawString(425,575,iden)

                c.drawString(70,550,"Carro:")
                c.drawString(125,550,carro)

                c.drawString(400,550,"Placa:")
                c.drawString(445,550,placa)

                c.drawString(80,520,"DETALLE")
                c.drawString(70,35,"VALOR TOTAL")

                c.drawString(400,35,"$")
                c.drawString(420,35,valor)
                #parrafo
                textobject=c.beginText(90,480)

                for line in desc.splitlines(False):
                    line=line.replace("\n","")
                    textobject.textLine(line.strip())
                c.drawText(textobject)
                c.save()
                mb.showinfo("Información", "Factura Generada")
                
        btn_generar_fact=Button(frame_factura,text="Generar",font=("Arial",12),width=17,command=lambda:gen_factura())
        btn_generar_fact.grid(row=15,column=4,columnspan=2,pady=40)
        self.pantalla_factura.deiconify()
        self.ini.withdraw()
        self.pantalla_factura.mainloop()
    def Garantia(self):
        pantalla_garantia=Toplevel()
        pantalla_garantia.title("Garantias")
        pantalla_garantia.resizable
        
        img_1=PhotoImage(file="./Imagenes/b_buscar.png")
        Label(pantalla_garantia,image=img_1).pack()
        frame_garantia=Frame(pantalla_garantia)
        frame_garantia.pack()

        Label(frame_garantia,text="Fecha Garantia",font=('Arial',12)).grid(row=0,column=1)
        Label(frame_garantia,text="Placa Vehiculo",font=('Arial',12)).grid(row=0,column=4)
        Label(frame_garantia,text="Descripcion Arreglo",font=('Arial',12)).grid(row=5,column=1)

        entra_fechaG=DateEntry(frame_garantia,locale='es_ES',date_pattern='yyyy-MM-dd',width=25)
        entra_fechaG.grid(row=2,column=1)

        entra_placaG=Entry(frame_garantia)
        entra_placaG.grid(row=2,column=4,pady=17)

        entra_arregloG=Text(frame_garantia)
        entra_arregloG.config(width=35, height=8,font='arial')
        entra_arregloG.grid(row=7,column=1,pady=10,columnspan=10)

        btn_guardar=Button(frame_garantia,text="GUARDAR",font=('Arial',12),width=17,command=lambda:guarda_garantia(entra_fechaG.get().upper(),entra_arregloG.get("1.0","end").upper(),entra_placaG.get().upper()))
        btn_guardar.grid(row=10,column=1,pady=20,columnspan=2)
        
        btn_salir=Button(frame_garantia,text="SALIR",font=('Arial',12),width=15,command=lambda:salir())
        btn_salir.grid(row=10,column=3,pady=20,columnspan=2)

        def salir():
            pantalla_garantia.destroy()
        
        def guarda_garantia(fecha,descri,placa):
            try:
                if entra_fechaG.get()=="" or entra_placaG.get()=="" or entra_arregloG.get("1.0","end")=="":
                    mb.showerror("Cuidado","Faltan Ingresar Datos")
                else:
                        conn=psycopg2.connect(
                            dbname="ElectroAires",
                            user="postgres",
                            password="vera",
                            host="localhost",
                            port="5432")
                        cursor=conn.cursor()
                        query=''' UPDATE electro SET fecha_ingreso = %s, arreglo_nuevo = %s WHERE placa=%s '''
                        cursor.execute(query,(fecha,descri,placa))
                        
                        mb.showinfo("EXITO","Datos Guardados")
                        conn.commit()
                        conn.close()
            except:
                mb.showerror("Error","Datos No Guardados")
        pantalla_garantia.mainloop()
if __name__=='__main__':
    inicio= Tk()
    Aplicacion= Electro(inicio)
    inicio.mainloop()
