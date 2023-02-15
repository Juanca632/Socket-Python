import pymysql
import socket

HOST = "127.0.0.1"   # Direccion loopback
PORT = 65123         # > 1023 (Puerto escucha)

empleado = []



class DataBase:
    def __init__(self):
        self.connection = pymysql.connect(
                user='root', 
                password='root',
                host='localhost',
                database='datos'
            )
        self.cursor = self.connection.cursor()
        print('Exito')

    def select(self, id):
        sql = 'SELECT empl_ID, empl_primer_nombre, empl_segundo_nombre, empl_email, empl_fecha_nac, empl_sueldo, empl_comision, empl_cargo_ID, empl_Gerente_ID, empl_dpto_ID FROM datos.empleados WHERE empl_ID = {}'.format(id)
        self.cursor.execute(sql)
        empl = self.cursor.fetchone()
        
        try:
            print("Id:", empl[0])
            print("Pr Nombre", empl[1])
            print("Sg Nombre", empl[2])
        except Exception as e:
            print("ID Eliminado")
    
    def update(self, id, PrNm, SgNm, Em, FeNa, Su, Co, Car, Ger, Dpt, Flag):
        sql = 'UPDATE empleados SET empl_primer_nombre, empl_segundo_nombre, empl_email, empl_fecha_nac, empl_sueldo, empl_comision, empl_cargo_ID, empl_Gerente_ID, empl_dpto_ID FROM datos.empleados WHERE empl_ID = {}'.format(id, PrNm, SgNm, Em, FeNa, Su, Co, Car, Ger, Dpt)
    
    def delete(self, id):
        sql = 'DELETE FROM datos.empleados WHERE empl_ID = {}'.format(id)
        self.cursor.execute(sql)
        self.connection.commit()
        print('Eliminada')
        
    def insert(self, PrNm, SgNm, Em, FeNa, Su, Co, Car, Dpt):
        sql = 'INSERT INTO `empleados` (`empl_primer_nombre`,`empl_segundo_nombre`,`empl_email`,`empl_fecha_nac`,`empl_sueldo`,`empl_comision`, `empl_cargo_ID`,`empl_Gerente_ID`,`empl_dpto_ID`) VALUES({},{},{},{},{},{},{},NULL,{})'.format("'"+PrNm+"'","'"+SgNm+"'","'"+Em+"'","'"+FeNa+"'","'"+Su+"'","'"+Co+"'","'"+Car+"'","'"+Dpt+"'")
        self.cursor.execute(sql)
        self.connection.commit()
        empl = self.cursor.fetchone()
        print(empl)
        
        
databases = DataBase()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST,PORT))
    s.listen()
    conn, addr = s.accept()

    with conn:
        print(f"Conectado a {addr}:")
        while True:
            data = conn.recv(1024).decode("utf-8")
            if not data:
                break
            empleado.append(data)
            if(empleado[0] == "1" and len(empleado) == 8):
                print("\nSe desea agregar un nuevo empleado")
                databases.insert(empleado[1],empleado[2],"example@hotmail.com","2029-01-10 00:00:00",empleado[5],empleado[6],empleado[7],empleado[8])
                print(empleado)
                message = "Recibido".encode("utf-8")
                conn.sendall(message)
            elif(empleado[0] == "2" and len(empleado) == 9):
                print("\nSe desea actualizar un empleado")
                print(empleado)
                message = "Recibido".encode("utf-8")
                conn.sendall(message)
            elif(empleado[0] == "3" and len(empleado) == 2):
                print("\nSe desea consultar un empleado")
                databases.select(empleado[1])
                print(empleado)
                message = "Recibido".encode("utf-8")
                conn.sendall(message)
            elif(empleado[0] == "4" and len(empleado) == 2):
                print("\nSe desea eliminar un empleado")
                databases.delete[empleado[1]]
                print(empleado)
                message = "Recibido".encode("utf-8")
                conn.sendall(message)
            else:
                print("Oops, hubo un error")




