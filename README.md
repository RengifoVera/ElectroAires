# App-ElectroAires
Con este aplicativo podemos llevar y gestionar en ingreso de vehiculos a un taller de aire Acondicionado Automotriz 
con el que podemos ver los datos,arreglos y fechas en las que se le hizo alguna modificacion u arreglo a un 
vehiculo en especial, las funciones son las CRUD, y tambien permite conocer el ingreso total de un mes  
estipulado descontando el valor de los materiales usados en la reparacion del vehiculo, tambien permite 
crear una factura (no electronica) si no un PDF con los datos del cliente y el establecimiento en el que  
se realizo en trabajo, para tener un formato digital de una factura 
# Requisitos

Tener instalado PYTHON 3.8 o superior   
Tener instalado POSTGRESQL 12 o superior


# Dependencias
En el gestor debemos crear una base de datos llamada ElectroAires asi tal cual con las mayusculas                    
Para usar esta app debemos usar este codigo SQL en POSTGRESQL para crear las tablas necesarias en la base de datos  
        
CREATE TABLE ELECTRO
(   
        FECHA DATE,  
        MARCA TEXT,  
        TIPO_CARRO TEXT,        
        PLACA VARCHAR(10),    
        VALOR NUMERIC,    
        ARREGLO TEXT, 
        VALOR_MATERIALES NUMERIC, 
        FECHA_INGRESO DATE,  
        ARREGLO_NUEVO TEXT,      
        PRIMARY KEY(PLACA)    
    )   
