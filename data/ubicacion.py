from model.conexion import Conexion

class UbicacionData():
    
    
    def insertarUbicacion(self,nombre):
        self.db=Conexion().conectar()
        try:
            sql_insert= """INSERT INTO ubicaciones (NOMBRE) VALUES('{}') """.format(nombre)
            cur= self.db.cursor()
            cur.execute(sql_insert)
            self.db.commit()
        except Exception as ex:
            print ("Ya se Creo la Ubicacion",ex)
        if cur.rowcount == 1:
            cur.close()
            self.db.close()
            return True 
        else:
            cur.close()
            self.db.close()
            return  False


    def listaUbicaciones (self,id):
        self.db=Conexion().conectar()
        self.cursor=self.db.cursor()
        res=self.cursor.execute(""" SELECT * FROM ubicaciones WHERE IDMUNICIPIO ='{}' order by NOMBRE """ ) .format(id)
        ubicaciones= res.fetchall()
        self.cursor.close()
        self.db.close()
        return ubicaciones
    
    def editarUbicacion(self,nombre,nombreant):
        self.db=Conexion().conectar()
        self.cursor=self.db.cursor()
        actual= """ UPDATE  ubicaciones SET NOMBRE= '{}' WHERE NOMBRE= '{}' """  .format(nombre,nombreant) 
        self.cursor.execute(actual)
        a= self.cursor.rowcount
        self.db.commit()
        self.cursor.close()
        self.db.close()
        return a
    
    def eliminarUbicacion(self,id):
        self.db=Conexion().conectar()
        self.cursor=self.db.cursor()
        eliminar=""" DELETE FROM ubicaciones WHERE ID={} """ .format(id)
        self.cursor.execute(eliminar)
        self.db.commit()
        self.cursor.close()
        self.db.close()
 


