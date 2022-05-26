import psycopg2
def creacion_db():
    # try:   
        conn = psycopg2.connect(
        dbname="db2p0n0f7ofdjn",
        user="pflokzxrsqcyob",
        password="f08950e459414bb2097b3a979265e61461434169943a23b34d29dee6c74501c4",
        host="ec2-52-200-215-149.compute-1.amazonaws.com",
        port="5432")
        cursor = conn.cursor()
        query = '''ALTER TABLE inventario ALTER COLUMN venta SET DATA TYPE int;'''
        cursor.execute(query)
        conn.commit()
        conn.close()
        print("Base de datos creada")
    # except:
    #     print("Base de datos no creada")
        
creacion_db()
