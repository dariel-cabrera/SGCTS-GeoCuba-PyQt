import sys
#Donde estan todas las fotos
from .nimgC import *
from PyQt6.QtWidgets import QApplication,QMainWindow,QHeaderView
from PyQt6.QtCore import QPropertyAnimation,QEasingCurve 
from PyQt6 import QtCore,QtWidgets
from PyQt6.uic import loadUi
from PyQt6 import uic
from PyQt6.QtWidgets import QMessageBox
from data.tla import TLAData
from model.ecuaciones import transporte_logitudinal_arena 
import re
class Principal(QMainWindow):
    def __init__(self):
        #Iniciando
        super(Principal,self).__init__()
        loadUi("gui/principal.ui",self)
        #Mostrando La Ventana a Maximizada
        self.showMaximized()
        #Llamando a la Funcion iniGUi()
        self.iniGUI()
        #Llamando a la funcion Mover Menu
        self.but_mover.clicked.connect(self.mover_menu)
        #Conexion de Botones 
        self.button_Inicio.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_inicio))
        self.button_Usuarios.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_usuarios))
        self.button_Calculo.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_calculo))
        self.button_Trazas.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_trazas))
        self.button_Ajustes.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_ajustes))

        #Control de Barra de Titulo
        self.button_MinimizarVentana.clicked.connect(self.control_bt_minimizar)
        self.Button_Minimizar.clicked.connect(self.control_bt_normal)
        self.Button_Maximizar.clicked.connect(self.control_bt_maximizar)
        self.Button_Cerrar.clicked.connect(lambda: self.close())

        #Eliminar barra de titulos
        #self.setWindowFlag(QtCore.Qt.WindowType.FramelessWindowHint)
        #self.setWindowOpacity(1)

        #SizeGrip
        self.gripSize=10
        self.grip=QtWidgets.QSizeGrip(self)
        self.grip.resize(self.gripSize,self.gripSize)

        #Ancho de columna adaptable
        #self.tableUsuarios.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        #self.table_Calculos.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        #Mover ventana
        #self.frame_superior.mouseMoveEvent= self.mover_ventana

 ######################  Principal ###########################   
    def iniGUI(self):
        #Conectando el Boton Nuevo Calculo con la ventana Nuevo Calculo
        self.button_NuevoCalculo.clicked.connect(self.nuevocalculo)
        self.nuevocalculo= uic.loadUi("gui/nuevoCalculo.ui")
        self.button_Calculo.clicked.connect(self.mostrar_datos_tablaCalculos)
    
    
   
    
    def control_bt_minimizar(self):
        self.showMinimized()
    
    
    def control_bt_normal(self):
        self.showNormal()
        self.Button_Minimizar.hide()
        self.Button_Maximizar.show()
    
    def control_bt_maximizar(self):
        self.showMaximized()
        self.Button_Maximizar.hide()
        self.Button_Minimizar.show()

    #def mover_ventana(self,event):
        #if self.isMaximized()==False:
            #if event.buttons()==QtCore.Qt.LeftButton:
                #self.move(self.pos()+ event.globalPos()-self.click_position)
                #self.click_position=event.globalPos()
                #event.accept()
            #if event.globalPos().y()<=10:
                #self.showMaximized()
                #self.Button_Maximizar.hide()
                #self.Button_Minimizar.show()
            #else:
                #self.showNormal()
                #self.Button_Minimizar.hide()
                #self.Button_Maximizar.show()
    
    # Mover Menu 
    def mover_menu(self):
        if True:
            width = self.frame_control.width()
            normal=0
            if width==0:
                extender=200
            else:
                extender=normal
            self.animacion= QPropertyAnimation(self.frame_control,b'minimumWidth')
            self.animacion.setDuration(300)
            self.animacion.setStartValue(width)
            self.animacion.setEndValue(extender)
            #self.animacion.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
            self.animacion.start()
    
    
    def mostrar_datos_tablaCalculos(self):
        self.mostrar= TLAData()
        datos=self.mostrar.mostrar_datos_tla()
        a=[]
        for x in datos:
            a.append([str(i) for i in x])
        print(a)
        
        i=len(a)
        self.table_Calculos.setRowCount(i)
        tablerow=0

        for row in a:
            self.table_Calculos.setItem(tablerow,0,QtWidgets.QTableWidgetItem(row[0]))
            self.table_Calculos.setItem(tablerow,1,QtWidgets.QTableWidgetItem(row[1]))
            self.table_Calculos.setItem(tablerow,2,QtWidgets.QTableWidgetItem(row[2]))
            self.table_Calculos.setItem(tablerow,3,QtWidgets.QTableWidgetItem(row[3]))
            self.table_Calculos.setItem(tablerow,4,QtWidgets.QTableWidgetItem(row[4]))
            self.table_Calculos.setItem(tablerow,5,QtWidgets.QTableWidgetItem(row[5]))
            self.table_Calculos.setItem(tablerow,6,QtWidgets.QTableWidgetItem(row[6]))
            self.table_Calculos.setItem(tablerow,7,QtWidgets.QTableWidgetItem(row[7]))
            self.table_Calculos.setItem(tablerow,8,QtWidgets.QTableWidgetItem(row[8]))
            tablerow += 1 
    
    def nuevocalculo(self):
        #Llamando a la ventana NuevoCalculo
        self.nuevocalculo.but_GuardarNuevoCalculo.clicked.connect(self.EntrarNuevoCalculo)
        self.nuevocalculo.butCancelarNuevoCalculo.clicked.connect(self.boton_Cancelar_NuevoCalculo)
        self.nuevocalculo.show()

########################## Nuevo Calculo #########################
    def validarCampos(self):
        DensidadArena=self.nuevocalculo.lineEdit_densidadArena.text()
        DensidadMar=self.nuevocalculo.lineEdit_DensidadMar.text()
        CoeficienteP=self.nuevocalculo.lineEdit_CoeficientePorocidad.text()
        altura=self.nuevocalculo.lineEdit_altura.text()
        angulo=self.nuevocalculo.lineEdit_AnguloRompiente.text()
        indice=self.nuevocalculo.lineEdit_IndiceRompiente.text()
        ubicacion=self.nuevocalculo.lineEdit_Ubicacion.text()

        validarDA=re.match('^[0-9\.]+$',DensidadArena,re.I)
        validarDM=re.match('^[0-9\.]+$',DensidadMar,re.I)
        validarC=re.match('^[0-9\.]+$',CoeficienteP,re.I)
        validarAl=re.match('^[0-9\.]+$',altura,re.I)
        validarAn=re.match('^[0-9\.]+$',angulo,re.I)
        validarindice= re.match('^[0-9\.]+$',indice,re.I)
        validarU=re.match('^[a-z A-Z\sÀÈÌÒÙáéíóúàèìòùäëïüö]+$',DensidadMar,re.I)
        ####### Validaciones Densidad Arena #############
        if DensidadArena=="":
            self.nuevocalculo.lineEdit_densidadArena.setStyleSheet("border: 1px solid red;")
            mBox= QMessageBox()
            mBox.setText("No se pueden entrar campos Vacios")
            mBox.exec()
            self.nuevocalculo.lineEdit_densidadArena.setFocus()
            self.nuevocalculo.lineEdit_densidadArena.setText("0")
            return False
        
        elif not validarDA:
            self.nuevocalculo.lineEdit_densidadArena.setStyleSheet("border: 1px solid red;")
            mBox= QMessageBox()
            mBox.setText("Solo Puede Entrar Numeros")
            mBox.exec()
            self.nuevocalculo.lineEdit_densidadArena.setFocus()
            self.nuevocalculo.lineEdit_densidadArena.setText("0")
            return False
        
        elif float(self.nuevocalculo.lineEdit_densidadArena.text())<=0:
            self.nuevocalculo.lineEdit_densidadArena.setStyleSheet("border: 1px solid red;")
            mBox= QMessageBox()
            mBox.setText("Debe entrar un Dato Mayor a 0")
            mBox.exec()
            self.nuevocalculo.lineEdit_densidadArena.setFocus()
            self.nuevocalculo.lineEdit_densidadArena.setText("0")
            return False
        ####### Validaciones Densidad Mar #############
        elif  DensidadMar=="":
            self.nuevocalculo.lineEdit_DensidadMar.setStyleSheet("border: 1px solid red;")
            mBox= QMessageBox()
            mBox.setText("No se pueden entrar campos Vacios")
            mBox.exec()
            self.nuevocalculo.lineEdit_DensidadMar.setFocus()
            self.nuevocalculo.lineEdit_DensidadMar.setText("0")
            return False
        
        elif not validarDM:
            self.nuevocalculo.lineEdit_DensidadMar.setStyleSheet("border: 1px solid red;")
            mBox= QMessageBox()
            mBox.setText("Solo Puede Entrar Numeros")
            mBox.exec()
            self.nuevocalculo.lineEdit_DensidadMar.setFocus()
            self.nuevocalculo.lineEdit_DensidadMar.setText("0")
            return False
        
        elif float(self.nuevocalculo.lineEdit_DensidadMar.text())<=0:
            self.nuevocalculo.lineEdit_DensidadMar.setStyleSheet("border: 1px solid red;")
            mBox= QMessageBox()
            mBox.setText("Debe entrar un Dato Mayor a 0")
            mBox.exec()
            self.nuevocalculo.lineEdit_DensidadMar.setFocus()
            self.nuevocalculo.lineEdit_DensidadMar.setText("0")
            return False
        ################ Validaciones Coeficiente ################
        elif  CoeficienteP=="":
            self.nuevocalculo.lineEdit_CoeficientePorocidad.setStyleSheet("border: 1px solid red;")
            mBox= QMessageBox()
            mBox.setText("No se pueden entrar campos Vacios")
            mBox.exec()
            self.nuevocalculo.lineEdit_CoeficientePorocidad.setFocus()
            self.nuevocalculo.lineEdit_CoeficientePorocidad.setText("0")
            return False
        
        elif not validarC:
            self.nuevocalculo.lineEdit_CoeficientePorocidad.setStyleSheet("border: 1px solid red;")
            mBox= QMessageBox()
            mBox.setText("Solo Puede Entrar Numeros")
            mBox.exec()
            self.nuevocalculo.lineEdit_CoeficientePorocidad.setFocus()
            self.nuevocalculo.lineEdit_CoeficientePorocidad.setText("0")
            return False
        
        elif float(self.nuevocalculo.lineEdit_CoeficientePorocidad.text())<=0:
            self.nuevocalculo.lineEdit_CoeficientePorocidad.setStyleSheet("border: 1px solid red;")
            mBox= QMessageBox()
            mBox.setText("Debe entrar un Dato Mayor a 0")
            mBox.exec()
            self.nuevocalculo.lineEdit_CoeficientePorocidad.setFocus()
            self.nuevocalculo.lineEdit_CoeficientePorocidad.setText("0")
            return False
        ####### Validaciones Altura #############
        elif  altura=="":
            self.nuevocalculo.lineEdit_altura.setStyleSheet("border: 1px solid red;")
            mBox= QMessageBox()
            mBox.setText("No se pueden entrar campos Vacios")
            mBox.exec()
            self.nuevocalculo.lineEdit_altura.setFocus()
            self.nuevocalculo.lineEdit_altura.setText("0")
            return False
        
        elif not validarAl:
            self.nuevocalculo.lineEdit_altura.setStyleSheet("border: 1px solid red;")
            mBox= QMessageBox()
            mBox.setText("Solo Puede Entrar Numeros")
            mBox.exec()
            self.nuevocalculo.lineEdit_altura.setFocus()
            self.nuevocalculo.lineEdit_altura.setText("0")
            return False
        
        elif float(self.nuevocalculo.lineEdit_altura.text())<=0:
            self.nuevocalculo.lineEdit_altura.setStyleSheet("border: 1px solid red;")
            mBox= QMessageBox()
            mBox.setText("Debe entrar un Dato Mayor a 0")
            mBox.exec()
            self.nuevocalculo.lineEdit_altura.setFocus()
            self.nuevocalculo.lineEdit_altura.setText("0")
            return False
        else:
            return True

    def EntrarNuevoCalculo(self):
        if self.validarCampos()== False:
            mBox= QMessageBox()
            mBox.setText("Datos Incorrecto Verifiquelos")
            mBox.exec()
        else:
            DensidadArena= float(self.nuevocalculo.lineEdit_densidadArena.text())
            DensidadMar=  float(self.nuevocalculo.lineEdit_DensidadMar.text())
            CoeficienteP=float(self.nuevocalculo.lineEdit_CoeficientePorocidad.text())
            altura=float(self.nuevocalculo.lineEdit_altura.text())
            angulo=float(self.nuevocalculo.lineEdit_AnguloRompiente.text())
            indice=float(self.nuevocalculo.lineEdit_IndiceRompiente.text())
            ubicacion=self.nuevocalculo.lineEdit_Ubicacion.text()
           

            resultado= transporte_logitudinal_arena(DensidadMar,indice,DensidadArena,CoeficienteP,altura,angulo)
            
            self.tla= TLAData()
            mBox= QMessageBox()
            if self.tla.insertar_datos_tla(ubicacion,DensidadMar,DensidadArena,CoeficienteP,altura,angulo,indice,resultado):
                mBox.setText("Datos Guardados con Exito Q="+ str(resultado))  
                self.mostrar_datos_tablaCalculos()
                self.nuevocalculo.hide()
                self.limpiarCamposNuevoCalculo()
                
            else:
                mBox.setText("Los Datos NO se Guardados")
            mBox.exec()
    

    def limpiarCamposNuevoCalculo(self):
        self.nuevocalculo.lineEdit_DensidadMar.setText("")
        self.nuevocalculo.lineEdit_densidadArena.setText("")
        self.nuevocalculo.lineEdit_DensidadMar.setText("")
        self.nuevocalculo.lineEdit_CoeficientePorocidad.setText("")
        self.nuevocalculo.lineEdit_altura.setText("")
        self.nuevocalculo.lineEdit_AnguloRompiente.setText("")
        self.nuevocalculo.lineEdit_IndiceRompiente.setText("")
        self.nuevocalculo.lineEdit_Ubicacion.setText("")
    
    def boton_Cancelar_NuevoCalculo(self):
        self.nuevocalculo.hide()
        self.limpiarCamposNuevoCalculo()
