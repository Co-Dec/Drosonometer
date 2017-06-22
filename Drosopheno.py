#!/usr/bin/python3
# -*- coding: Utf-8 -*-
import sys
import os
import time
import matplotlib
matplotlib.use("Qt4Agg")
import matplotlib.pyplot as plt

import numpy as numpy
from pylab import *
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas

try :
	from PyQt4 import QtGui, QtCore
	print ("Pyqt Loaded successfully !")
	Pyqt = True
except ImportError as err:
	print ("Package PyQt4 not found, you can install it by running : apt-get install python3-pyqt4")
	print ("Sorry : "+str(err))


class My_Chronometer(QtGui.QMainWindow):
	def __init__(self):
		"""
		Lancer le programme et apelle UI
		"""
		super(QtGui.QMainWindow, self).__init__()
		self.init_toolbar = False
		self.init_readylabel = False
		self.initUI()
	
	
	def initUI(self):
		"""
		Organisation de l'UI
		"""
		self.countM = 0
		self.countF = 0
		
		self.countN = 0
		
		self.time_F = []
		self.time_M = []
		
		# New window :
		#self.newwinbut = QtGui.QPushButton(self)
		#self.newwinbut.clicked.connect(self.drawtimes)
		
		
		# Projet crée ? non
		self.created = False
		self.started=False
		
		# Pas de projet crée ni d'utilisateur sélectionné.
		self.Strain = "No project started"
		self.worker=""
		
		#Appel des constructeur 
		self.Build_Labels()
		self.Build_Buttons()
		self.Build_Timer()
		self.Build_LCD_Screen()
		self.Build_BottomWindow()
		self.Build_TopWindow()
		self.Build_Count_Frame()
		self.Build_Window()
		self.Build_Status_Bar()
		self.Caroline_ExitAction()
		self.Build_Toolbar()
		
		self.setGeometry(400, 200, 500, 750)        
		self.setWindowTitle('Drosonometre')    
		self.setWindowIcon(QtGui.QIcon('suzu.jpg'))
		
		self.show()
		
	def Build_Labels(self) : 
		# Etiquettes qui affichent le manipulateur et la souche travaillée
		self.Loaded_project = QtGui.QLabel(self.Strain,self)
		self.loaded_worker = QtGui.QLabel(self.worker,self)
		self.Males_awake = QtGui.QLabel("Males awake : " + str(self.countM),self)
		self.Fem_awake = QtGui.QLabel("Females awake : " +str(self.countF),self)
		
	def Build_Buttons(self) : 
		
		# BOuton de nouveau projet
		self.np = QtGui.QPushButton("New project",self)
		self.np.clicked.connect(self.open_project)
		
		# Bouton de lancement du chronomètre :
		self.startbuttonr = QtGui.QPushButton("Start experiment",self)
		self.startbuttonr.clicked.connect(self.startbutton)
		
		#Bouton pour montrer les plot 
		self.Plot_Button = QtGui.QPushButton("Show Plot",self)
		self.Plot_Button.clicked.connect(self.Show_Plot)
		
		#Bouton pour arrêter l'expérience
		self.Stop_Button = QtGui.QPushButton("Stop Experiment",self)
		self.Stop_Button.clicked.connect(self.stop_project)
		
		
	def Build_Timer(self) :
		# Tout les combiens update le chronomètre ?
		self.timerS = QtCore.QTimer()
		self.timerS.timeout.connect(self.timer)
		self.timerS.start(100)
	
	def Build_LCD_Screen (self) : 
		# Ecran LCD
		self.lcd = QtGui.QLCDNumber(self)
		
		
	def Build_BottomWindow(self) : 
			
		# Definir le layout des boutons males et femelle :
		VLAY = QtGui.QHBoxLayout() #Je dis que c'est un layout
				
		# Ajouter les 2 boutons :
		
		male = QtGui.QPushButton("Male",self)
		male.setIcon(QtGui.QIcon('male.jpeg'))
		male.clicked.connect(self.printimemal)
		
		VLAY.addWidget(male)
		
		fem = QtGui.QPushButton("Femelle",self)
		fem.setIcon(QtGui.QIcon('fem.png'))
		fem.clicked.connect(self.printimefem)
		
		VLAY.addWidget(fem)		
		
		dele=  QtGui.QPushButton("Delete last",self)
		dele.setIcon(QtGui.QIcon('close-file-icon.png'))
		dele.clicked.connect(self.delete_last)
		
		VLAY.addWidget(dele)
	
		# Applique le layout au bas de la fenetre :
		self.WidBas = QtGui.QFrame() #Je définis mon Widget du bas comme gros widget qui en contien d'autres
		self.WidBas.setLayout(VLAY)	# je dis que son layout c'est celui que je viens de créer
	
	def Build_TopWindow (self) : 
		# LAyout des étiquettes d'état :
		setuplayout = QtGui.QHBoxLayout()
		setuplayout.addWidget(self.Loaded_project)
		setuplayout.addWidget(self.loaded_worker)
		
		self.topwid=QtGui.QFrame()
		self.topwid.setLayout(setuplayout)
	
	def Build_Count_Frame (self) : 
		self.countawake = QtGui.QFrame()
		layoutcount = QtGui.QVBoxLayout()
		layoutcount.addWidget(self.Males_awake)
		layoutcount.addWidget(self.Fem_awake)
		layoutcount.addWidget(self.topwid)
		self.countawake.setLayout(layoutcount)
		
	def Build_Window (self) : 
		# Définit le layout total de l'apply
		self.Tot=QtGui.QVBoxLayout()
		
		self.Tot.addWidget(self.countawake)
		self.Tot.addWidget(self.lcd)
		self.Tot.addWidget(self.np)
		#self.Tot.addWidget(self.newwinbut)
		self.Tot.addWidget(self.startbuttonr)
		self.Tot.addWidget(self.Plot_Button)
		self.Tot.addWidget(self.Stop_Button)
		self.Tot.addWidget(self.WidBas)
	
		WidGen = QtGui.QFrame()
		WidGen.setLayout(self.Tot)
		self.setCentralWidget(WidGen)
	
	def Build_Status_Bar (self): 
		# La status bar :
		self.readyLabel = QtGui.QLabel("Ready")
		self.statusBar().addWidget(self.readyLabel)
		self.init_readylabel = True 
			
	def Caroline_ExitAction (self) : #Désolé, j'ai pas pu m'en empêcher :3 
		# Exit
		self.exitAction = QtGui.QAction(QtGui.QIcon('close-file-icon.png'), '&Exit', self)
		self.exitAction.setShortcut('Ctrl+Q')
		self.exitAction.setStatusTip('Exit program')
		self.exitAction.triggered.connect(self.close)
	
	def Build_Toolbar (self) : 
		# Toolbar
		self.toolbar = self.addToolBar('Exit')
		self.toolbar.addAction(self.exitAction)
		self.init_toolbar = True 
		
	def initUI_2(self): #Permet de réinitialiser la fenêtre pour faire une nouvelle expérience sans avoir à fermer/relancer. 
		"""
		Organisation de l'UI
		"""
		self.countM = 0
		self.countF = 0
		
		self.countN = 0
		
		# New window :
		#self.newwinbut = QtGui.QPushButton(self)
		#self.newwinbut.clicked.connect(self.drawtimes)
		
		
		# Projet crée ? non
		self.created = False
		self.started=False
		
		# Pas de projet crée ni d'utilisateur sélectionné.
		self.Strain = "No project started"
		self.worker=""
		
		#Appel des constructeur 
		self.Build_Labels()
		self.Build_Buttons()
		self.Build_Timer()
		self.Build_LCD_Screen()
		self.Build_BottomWindow()
		self.Build_TopWindow()
		self.Build_Count_Frame()
		self.Build_Window()
		self.Caroline_ExitAction()
		
		self.setGeometry(400, 200, 500, 750)        
		self.setWindowTitle('Drosonometre')    
		self.setWindowIcon(QtGui.QIcon('suzu.jpg'))
		
		self.show()
		
	
	
	def delete_last(self) :
		if self.started and self.countN >=1 :
			reply = QtGui.QMessageBox.question(self, 'Message',"Are you sure to delete last time?", QtGui.QMessageBox.Yes|QtGui.QMessageBox.No, QtGui.QMessageBox.No)
			if reply == QtGui.QMessageBox.Yes :
				f = open(self.ATM,"r")
				e = open("tmp","w")
				act=""
				for i in f :
					if act != "" :
						e.write(act)
					act = i
				f.close()
				e.close()
				f= open("tmp","r")
				e=open(self.ATM,"w")
				for i in f :
					e.write(i)
				e.close()
				f.close()
				Sex = self.child.Table.item(self.countN,0).text()
				self.child.Table.removeRow(self.countN)
				self.countN-=1
				
				if Sex == "F" :
					self.countF -=1
				elif Sex =="M" :
					self.countM -=1
				os.remove('tmp')
	
	def open_project(self):
		"""
		Permet de créer une nouvelle session et de lancer par la suite le chronomètre.
		"""
		if not self.created :
			File=QtGui.QFileDialog.getSaveFileName(self, 'Create your project CSV')
			
			
			Strain, ok2 = QtGui.QInputDialog.getText(self, 'Input Dialog', 'Strain :')
			if ok2 :
				
				Worker, ok3 = QtGui.QInputDialog.getText(self,'Input Dialog', 'Worker :')
				if ok3 :
					Newproj = open(File,"w")
					Newproj.write(Strain+"_"+Worker+"\t"+"WakeUpTime"+"\n")
					Newproj.close()
					self.ATM=File
					self.Strain=Strain
					self.created = True
					self.Loaded_project.setText("Strain : " + self.Strain)
					self.loaded_worker.setText("Worker : "+ Worker)
					self.Tot.removeWidget(self.np)
					self.np.deleteLater()
					self.np = None

					self.child = Aff_Timers(self)
					
					
	def printimefem(self):
		"""
		Appelé quand on clique sur le bouton femelle
		"""
		if self.started :
			Wakeup = open(self.ATM,"a")
			Wakeup.write("F" + "\t" + str(time.time()-self.Deb)+"\n")
			Wakeup.close()
			
			self.child.add_value("F",str(time.time()-self.Deb),self.countN)
			self.countN+=1
			self.countF+=1
			self.Males_awake.setText("Males awake : " + str(self.countM))
			self.Fem_awake.setText("Females awake : " +str(self.countF))
			
			self.child.Table.verticalScrollBar().setValue(self.countN-10)
			
			self.time_F.append(time.time()-self.Deb)
			#self.Plot.Print_Plot(self.time_F, self.time_M)
			
			
	def printimemal(self):
		"""
		Appelé quand on clique sur le bouton male
		"""
		if self.started :
			Wakeup = open(self.ATM,"a")
			Wakeup.write("M" + "\t" + str(time.time()-self.Deb)+"\n")
			Wakeup.close()
			
			self.child.add_value("M",str(time.time()-self.Deb),self.countN)	
			self.countN+=1
			self.countM+=1
			self.Males_awake.setText("Males awake : " + str(self.countM))
			self.Fem_awake.setText("Females awake : " +str(self.countF))
			self.child.Table.verticalScrollBar().setValue(self.countN-10)
			
			self.time_M.append(time.time()-self.Deb)
			#self.Plot.Print_Plot(self.time_F, self.time_M)
			

	def Show_Plot (self) : 
		if self.started : 
			
			#D'abord, on regarde combien de bloc de 10 sec on a dans le chiffre maximum des liste males et femelles
			if self.time_F != [] and self.time_M != [] : 
			
				if max(self.time_F) > max(self.time_M) : 
					maximum = max(self.time_F)
				else : 
					maximum = max(self.time_M)
			elif self.time_F != [] and self.time_M == [] : 
				maximum = max(self.time_F)
			elif self.time_F == [] and self.time_M != [] : 
				maximum = max(self.time_M)	
					
			indice = 0
			while maximum > 0 : 
				maximum -= 10 
				indice += 1
			maximum = 10*indice
			
			#Ensuite, pour chaque tranche de 10 secondes, je regarde combien d'individus se sont réveillé dans la tranche. 
			self.Nb_Indiv = [0]
			self.Tranche = [0]
			for bloc in range(0, maximum, 10) : 
				self.Tranche.append(bloc+10)
				Indiv_Bloc = 0
				for time in self.time_M : 
					if time > bloc and time < bloc +10 : 
						Indiv_Bloc +=1 
				for time in self.time_F : 
					if time > bloc and time < bloc + 10 : 
						Indiv_Bloc += 1 
				self.Nb_Indiv.append(Indiv_Bloc)
			
			plot(self.Tranche, self.Nb_Indiv)
			show()

		
			
		
	def timer(self):
		"""
		Afficher le temps voulu sur le timer
		"""
		if self.started :
			self.lcd.display(round(float(time.time()-self.Deb)))
			
			
		else :
			self.lcd.display(0)
	
	def startbutton(self):
		"""
		Départ du chronomètre
		"""
		if not self.started and self.created:
			self.Deb=time.time()
			self.started=True
			self.startbuttonr.text().replace("Start", "Stop")
			self.Tot.removeWidget(self.startbuttonr)
			self.startbuttonr.deleteLater()
			self.startbuttonr = None

			#self.Plot = Print_Plot(self)
			
			
	def keyPressEvent(self, e):
		if self.started :
			if e.key() == QtCore.Qt.Key_M:
				self.printimemal()
				
					
			if e.key() == QtCore.Qt.Key_F:
				self.printimefem()
		
				
	def stop_project(self) : 
		if self.started : 
			reply = QtGui.QMessageBox.question(self, 'Message',"Are you sure you want to stop experiment ? ", QtGui.QMessageBox.Yes|QtGui.QMessageBox.No, QtGui.QMessageBox.No)
			if reply == QtGui.QMessageBox.Yes :
				self.initUI_2()
				self.time_F = []
				self.time_M = [] 
			
	
	
	
	def closeEvent(self, event):
		"""
		redefinit la fermeture du programme pour avoir une confirmation
		"""
		reply = QtGui.QMessageBox.question(self, 'Message',"Are you sure to quit?", QtGui.QMessageBox.Yes|QtGui.QMessageBox.No, QtGui.QMessageBox.No)
		if reply == QtGui.QMessageBox.Yes:
			event.accept()
		else:
			event.ignore() 
	
class Aff_Timers(QtGui.QMainWindow):
	def __init__(self,parent=None):
		"""
		Lancer le programme et apelle UI
		"""
		super(Aff_Timers, self).__init__(parent)
		self.parent = parent
		self.setWindowTitle("Drosonotable")
		self.initUI()
	
	def add_value(self,S,T,n):
				
		self.Table.setItem(int(n)+1,0,QtGui.QTableWidgetItem(S))
		self.Table.setItem(int(n)+1,1,QtGui.QTableWidgetItem(T))

		
	def initUI(self):
		self.Table=QtGui.QTableWidget()
		self.Table.setRowCount(150)
		self.Table.setColumnCount(2)
		self.Table.setItem(0,0,QtGui.QTableWidgetItem("Sexe"))
		self.Table.setItem(0,1,QtGui.QTableWidgetItem("WakeUpTime"))	
		
		self.setCentralWidget(self.Table)
		self.setGeometry(1000, 200, 250, 750)        

		self.show()


#Tentative, infructueuse, c'est useless pour l'instant mais je garde au cas où je finis par trouver 

#~ class Print_Plot(QtGui.QMainWindow):
	
	#~ def __init__(self, parent=None) : 
		#~ super(Print_Plot, self).__init__(parent)
		#~ self.parent = parent
		#~ self.initUI()
		
	#~ def Print_Plot(self, liste_F, liste_M) : 
		
		#~ #D'abord, on regarde combien de bloc de 10 sec on a dans le chiffre maximum des liste males et femelles
		#~ if liste_F != [] and liste_M != [] : 
		
			#~ if max(liste_F) > max(liste_M) : 
				#~ maximum = max(liste_F)
			#~ else : 
				#~ maximum = max(liste_M)
		#~ elif liste_F != [] and liste_M == [] : 
			#~ maximum = max(liste_F)
		#~ elif liste_F == [] and liste_M != [] : 
			#~ maximum = max(liste_M)	
				
		#~ indice = 0
		#~ while maximum > 0 : 
			#~ maximum -= 10 
			#~ indice += 1
		#~ maximum = 10*indice
		
		#~ #Ensuite, pour chaque tranche de 10 secondes, je regarde combien d'individus se sont réveillé dans la tranche. 
		#~ self.Nb_Indiv = [0]
		#~ self.Tranche = [0]
		#~ for bloc in range(0, maximum, 10) : 
			#~ self.Tranche.append(bloc+10)
			#~ Indiv_Bloc = 0
			#~ for time in liste_M : 
				#~ if time > bloc and time < bloc +10 : 
					#~ Indiv_Bloc +=1 
			#~ for time in liste_F : 
				#~ if time > bloc and time < bloc + 10 : 
					#~ Indiv_Bloc += 1 
			#~ self.Nb_Indiv.append(Indiv_Bloc)
		
		#~ plot(self.Tranche, self.Nb_Indiv) 
		#~ show()
		
	#~ def initUI(self):
		#~ self.setWindowTitle("Drosonoplot")
		#~ self.fig = Figure()
		#~ self.canvas = FigureCanvas(self.fig)
		#~ self.setCentralWidget(self.canvas)
		#~ self.setGeometry(0, 0, 0, 0)        

		#~ self.show()
		
		
def main():
    
    app = QtGui.QApplication(sys.argv)
    
    ex = My_Chronometer()
    sys.exit(app.exec_())

if __name__ == '__main__':
	
	main()	
