from PyQt5.QtCore import (Qt, QTimer,QThread, QUrl,QRectF)
from PyQt5.QtWidgets import (QApplication, QMainWindow, QAction)
from PyQt5.QtGui import (QPainter ,QColor ,QFont ,QBrush ,QPen,QImage)
from PyQt5.QtMultimedia import (QMediaPlayer,QMediaPlaylist,QMediaContent)
import random
import time
import sys
import math
from math import pi

class MainWindow (QMainWindow) :
    def __init__(self):
        super (MainWindow, self).__init__()
        self.setWindowTitle("affichons ces satanés boules")
        self.setMinimumHeight(500)
        self.setMinimumWidth(self.height())

        self.tm = QTimer()
        self.tm.timeout.connect(self.animate)       #ça ne sert pas pour l'instant
        self.tm.start(1)

        self.setMouseTracking(False)

        self.eMercure = 0.205631  #toutes les valeurs de l'excentricités donnés dans le tableau
        self.eVenus = 0.006773
        self.eTerre = 0.016710
        self.eMars = 0.093412
        self.eJupiter =0.048393
        self.eSaturne = 0.054151
        self.eUranus = 0.047168
        self.eNeptune = 0.008586

        self.rMercure0 = 0.325296331   #toutes les valeurs du rayon donnés dans le tableau pour thêta = 0
        self.rVenus0 = 0.720362247
        self.rTerre0 =0.983313626
        self.rMars0 = 1.657730943
        self.rJupiter0 =5.415876318
        self.rSaturne0 =10.010717655
        self.rUranus0 =19.975221794
        self.rNeptune0 =29.959662109

        self.aMercure= self.rMercure0*(1+self.eMercure) / (1 - self.eMercure**2)  #calculs en fonction du rayon à thêta = 0 pour trouver a
        self.aVenus= self.rVenus0*(1+self.eVenus)   /   (1 - self.eVenus**2)
        self.aTerre= self.rTerre0*(1+self.eTerre)   /   (1 - self.eTerre**2)
        self.aMars= self.rMars0*(1+self.eMars)   /   (1 - self.eMars**2)
        self.aJupiter= self.rJupiter0*(1+self.eJupiter)   /   (1 - self.eJupiter**2)
        self.aSaturne= self.rSaturne0*(1+self.eSaturne)   /   (1 - self.eSaturne**2)
        self.aUranus= self.rUranus0*(1+self.eUranus)   /   (1 - self.eUranus**2)
        self.aNeptune= self.rNeptune0*(1+self.eNeptune)   /   (1 -self. eNeptune**2)

        self.cMercure = self.aMercure * self.eMercure    #calcul de c, distance entre le centre et le foyer
        self.cVenus = self.aVenus * self.eVenus
        self.cTerre = self.aTerre * self.eTerre
        self.cMars = self.aMars * self.eMars
        self.cJupiter = self.aJupiter * self.eJupiter
        self.cSaturne = self.aSaturne * self.eSaturne
        self.cUranus =  self.aUranus * self.eUranus
        self.cNeptune = self.aNeptune * self.eNeptune

        self.bMercure = ( self.aMercure**2 - self.cMercure**2 )**(1/2)    #calcul de b
        self.bVenus = ( self.aVenus**2 - self.cVenus**2 )**(1/2)
        self.bTerre = ( self.aTerre**2 - self.cTerre**2 )**(1/2)
        self.bMars = ( self.aMars**2 - self.cTerre**2 )**(1/2)
        self.bJupiter = ( self.aJupiter**2 - self.cJupiter**2 )**(1/2)
        self.bSaturne = ( self.aSaturne**2 - self.cSaturne**2 )**(1/2)
        self.bUranus = ( self.aUranus**2 - self.cUranus**2 )**(1/2)
        self.bNeptune = ( self.aNeptune**2 - self.cNeptune**2 )**(1/2)

        self.rMercure = self.aMercure*(1-self.eMercure**2) / (1 + self.eMercure*math.cos(0))
        self.rVenus = self.aVenus*(1-self.eVenus**2) / (1 +self.eVenus*math.cos(0))
        self.rTerre = self.aTerre*(1-self.eTerre**2) / (1 + self.eTerre*math.cos(0))
        self.rMars = self.aMars*(1-self.eMars**2) / (1 + self.eMars*math.cos(0))
        self.rJupiter = self.aJupiter*(1-self.eJupiter**2) / (1 + self.eJupiter*math.cos(0))
        self.rSaturne = self.aSaturne*(1-self.eSaturne**2) / (1 + self.eSaturne*math.cos(0))
        self.rUranus = self.aUranus*(1-self.eUranus**2) / (1 + self.eUranus*math.cos(0))
        self.rNeptune = self.aNeptune*(1-self.eNeptune**2) / (1 + self.eNeptune*math.cos(0))

        self.bd_p = 10
        self.bd_s = 0

        self.angle8 = -338 * pi / 180    #les angles pour placer les planètes aux bons endroits, convertis en radian afin de correspondre aux valeurs demandés par Math.cos()
        self.angle7 = -19 * pi / 180
        self.angle6 = -248 * pi / 180
        self.angle5 = -162 * pi / 180
        self.angle4 = -174 * pi / 180
        self.angle3 = -99 * pi / 180
        self.angle2 = -184 * pi / 180
        self.angle1 = -30 * pi / 180

        self.anny = 0  #une valeur de base pour que l'animation soit stoppé au démarrage

        self.zoom = 1 #une valeur de base pour que le zoom soit le plus reculé possible

        self.dateJour = 1 # les dates ne servent pas encore
        self.dateMois = 1
        self.dateAnnée = 2016

        self.vitesse = 0.001 #une vitesse posé de façon arbitraire à laquelle les planètes tournent

        self.pas = math.pi / 10  #valeur de l'avancer du pas de la terre en rotation pas à pas

        self.createActions()
        self.createMenus()



    def keyPressEvent(self ,e):  #j'ai ajouté des clefs afin de faciliter le processus de changement de vitesse et d'avance pas à pas
        code = e.key()

        if (code == Qt.Key_A):
            self.pasPlus()

        if (code == Qt.Key_Z):
            self.pasMoins()

        if (code == Qt.Key_R):
            self.plusvite()

        if (code == Qt.Key_T):
            self.moinsvite()



    def createActions(self): # les actions qui seront ensuite liés au createMenus afin d'affilier des taches aux boutons

        self.movement = QAction('&animer simulation', self, triggered = self.lanceAnny)
        self.nomovement = QAction('&stop simulation',self, triggered = self.arreteAnny)

        self.zozoin = QAction('&Zoom In', self, triggered = self.zoomin)
        self.zozoout = QAction('&Zoom Out', self, triggered = self.zoomout)

        self.gogo = QAction('&vitesse x 2  (R)', self, triggered = self.plusvite)
        self.nogo = QAction('&vitesse / 2  (T)', self, triggered = self.moinsvite)

        self.pasAv = QAction('&rota + 1/10  (A)', self, triggered = self.pasPlus)
        self.pasRec = QAction('&rota - 1/10  (Z)', self, triggered = self.pasMoins)

    def createMenus(self):  #le menu contenant tous les boutons et lançant les fonctions

        self.fmenu = self.menuBar().addMenu('&Animation')
        self.fmenu.addAction(self.movement)
        self.fmenu.addAction(self.nomovement)
        self.fmenu.addAction(self.gogo)
        self.fmenu.addAction(self.nogo)
        self.fmenu.addAction(self.pasAv)
        self.fmenu.addAction(self.pasRec)



        self.fmenu2 = self.menuBar().addMenu('Zoom')
        self.fmenu2.addAction(self.zozoin)
        self.fmenu2.addAction(self.zozoout)



    def plusvite(self):  #fonctions reliées aux boutons afin de faire avancer la simulation plus ou moins vite
        self.vitesse *= 2

    def moinsvite(self):
        self.vitesse /= 2


    def pasPlus(self):  #fonctions qui font avancer la rotation pas à pas d'1/20 de tour pour la terre, dans un sens ou dans l'autre. ( la rotation restant relative aux planètes ensuite )
            self.angle3 += self.pas
            self.angle8 += self.pas /164.78
            self.angle7 += self.pas /84.0180
            self.angle6 += self.pas /29.457
            self.angle5 += self.pas /11.8620
            self.angle4 += self.pas /1.8808
            self.angle2 += self.pas /0.6152
            self.angle1 += self.pas /0.2408

    def pasMoins(self):
            self.angle3 -= self.pas
            self.angle8 -= self.pas /164.78
            self.angle7 -= self.pas /84.0180
            self.angle6 -= self.pas /29.457
            self.angle5 -= self.pas /11.8620
            self.angle4 -= self.pas /1.8808
            self.angle2 -= self.pas /0.6152
            self.angle1 -= self.pas /0.2408



    def zoomin(self): #une valeur change, augment, afin que les conditions liés au zoom s'engagent, on lance ensuite la fonction calculZoom pour que tout reste à l'échelle
        self.zoom += 1
        if self.zoom >= 8 :
            self.zoom = 8
        self.calculZoom()

    def zoomout(self):   #une valeur change, diminue, afin que les conditions liés au zoom s'engagent, on lance ensuite la fonction calculZoom pour que tout reste à l'échelle
        self.zoom -= 1
        if self.zoom <= 1 :
            self.zoom = 1
        self.calculZoom()




    def calculZoom(self):  #une fonction copié collé du resize event afin de pouvoir l'executer quand bon me semble, dans ce cas présent lorsque l'utilisateur clique sur le bouton zoom

        if self.zoom == 1 :
            self.bd_p = 10
            self.bd_s = 0
            self.rayon8 = self.height() - 10   - 40
            self.rayon7 = self.rayon8 / 1.5
            self.rayon6 = self.rayon8 / 3
            self.rayon5 = self.rayon8 / 5.5
            self.rayon4 = self.rayon8 / 18.75
            self.rayon3 = self.rayon8 / 30
            self.rayon2 = self.rayon8 / 50
            self.rayon1 = self.rayon8 / 100

        if self.zoom == 2 :
            self.bd_p = 10
            self.bd_s = 0
            self.rayon8 = 0
            self.rayon7 = self.height() - 10   - 40
            self.rayon6 = self.rayon7 / 2
            self.rayon5 = self.rayon7 / 3.7
            self.rayon4 = self.rayon7 / 12
            self.rayon3 = self.rayon7 / 20
            self.rayon2 = self.rayon7 / 27.7
            self.rayon1 = self.rayon7 / 61.5

        if self.zoom == 3 :
            self.bd_p = 10
            self.bd_s = 5
            self.rayon8 = 0
            self.rayon7 = 0
            self.rayon6 = self.height() - 10   - 40
            self.rayon5 = self.rayon6 / 1.8
            self.rayon4 = self.rayon6 / 6
            self.rayon3 = self.rayon6 / 10
            self.rayon2 = self.rayon6 / 14
            self.rayon1 = self.rayon6 / 30.7

        if self.zoom == 4 :
            self.bd_p = 15
            self.bd_s = 10
            self.rayon8 = 0
            self.rayon7 = 0
            self.rayon6 = 0
            self.rayon5 = self.height() - 10   - 45
            self.rayon4 = self.rayon5 / 3.3
            self.rayon3 = self.rayon5 / 5.5
            self.rayon2 = self.rayon5 / 7.5
            self.rayon1 = self.rayon5 / 16.6

        if self.zoom == 5 :
            self.bd_p = 20
            self.bd_s = 30
            self.rayon8 = 0
            self.rayon7 = 0
            self.rayon6 = 0
            self.rayon5 = 0
            self.rayon4 = self.height() - 10   - 50
            self.rayon3 = self.rayon4 / 1.7
            self.rayon2 = self.rayon4 / 2.3
            self.rayon1 = self.rayon4 / 5

        if self.zoom == 6 :
            self.bd_p = 30
            self.bd_s = 50
            self.rayon8 = 0
            self.rayon7 = 0
            self.rayon6 = 0
            self.rayon5 = 0
            self.rayon4 = 0
            self.rayon3 = self.height() - 10   - 60
            self.rayon2 = self.rayon3 / 1.36
            self.rayon1 = self.rayon3 / 3

        if self.zoom == 7 :
            self.bd_p = 40
            self.bd_s = 100
            self.rayon8 = 0
            self.rayon7 = 0
            self.rayon6 = 0
            self.rayon5 = 0
            self.rayon4 = 0
            self.rayon3 = 0
            self.rayon2 = self.height() - 10   - 80
            self.rayon1 = self.rayon2 / 2.25

        if self.zoom == 8 :
            self.bd_p = 50
            self.bd_s = 300
            self.rayon8 = 0
            self.rayon7 = 0
            self.rayon6 = 0
            self.rayon5 = 0
            self.rayon4 = 0
            self.rayon3 = 0
            self.rayon2 = 0
            self.rayon1 = self.height() - 10   - 90

        self.pos8x = self.width() / 2 - self.rayon8 / 2
        self.pos8y = self.height() / 2 - self.rayon8 / 2 + 15


        self.pos7x = self.width() / 2 - self.rayon7 / 2
        self.pos7y = self.height() / 2 - self.rayon7 / 2 + 15


        self.pos6x = self.width() / 2 - self.rayon6 / 2
        self.pos6y = self.height() / 2 - self.rayon6 / 2 + 15


        self.pos5x = self.width() / 2 - self.rayon5 / 2
        self.pos5y = self.height() / 2 - self.rayon5 / 2 + 15


        self.pos4x = self.width() / 2 - self.rayon4 / 2
        self.pos4y = self.height() / 2 - self.rayon4 / 2 + 15


        self.pos3x = self.width() / 2 - self.rayon3 / 2
        self.pos3y = self.height() / 2 - self.rayon3 / 2 + 15


        self.pos2x = self.width() / 2 - self.rayon2 / 2
        self.pos2y = self.height() / 2 - self.rayon2 / 2 + 15


        self.pos1x = self.width() / 2 - self.rayon1 / 2
        self.pos1y = self.height() / 2 - self.rayon1 / 2 + 15

    def resizeEvent(self,e):  # la fonction resize event contenant les valeurs qui changent, en particulier pour permettre le zoom avec les rayons qui s'adaptent au zoom mais qui restent à l'échelle

        if self.zoom == 1 :
            self.bd_p = 10
            self.rayon8 = self.height() - 10   - 40
            self.rayon7 = self.rayon8 / 1.5
            self.rayon6 = self.rayon8 / 3
            self.rayon5 = self.rayon8 / 5.5
            self.rayon4 = self.rayon8 / 18.75
            self.rayon3 = self.rayon8 / 30
            self.rayon2 = self.rayon8 / 50
            self.rayon1 = self.rayon8 / 100

        if self.zoom == 2 :
            self.bd_p = 10
            self.rayon8 = 0
            self.rayon7 = self.height() - 10   - 40
            self.rayon6 = self.rayon7 / 2
            self.rayon5 = self.rayon7 / 3.7
            self.rayon4 = self.rayon7 / 12
            self.rayon3 = self.rayon7 / 20
            self.rayon2 = self.rayon7 / 27.7
            self.rayon1 = self.rayon7 / 61.5

        if self.zoom == 3 :
            self.bd_p = 10
            self.rayon8 = 0
            self.rayon7 = 0
            self.rayon6 = self.height() - 10   - 40
            self.rayon5 = self.rayon6 / 1.8
            self.rayon4 = self.rayon6 / 6
            self.rayon3 = self.rayon6 / 10
            self.rayon2 = self.rayon6 / 14
            self.rayon1 = self.rayon6 / 30.7

        if self.zoom == 4 :
            self.bd_p = 10
            self.rayon8 = 0
            self.rayon7 = 0
            self.rayon6 = 0
            self.rayon5 = self.height() - 10   - 40
            self.rayon4 = self.rayon5 / 3.3
            self.rayon3 = self.rayon5 / 5.5
            self.rayon2 = self.rayon5 / 7.5
            self.rayon1 = self.rayon5 / 16.6

        if self.zoom == 5 :
            self.bd_p = 10
            self.rayon8 = 0
            self.rayon7 = 0
            self.rayon6 = 0
            self.rayon5 = 0
            self.rayon4 = self.height() - 10   - 40
            self.rayon3 = self.rayon4 / 1.7
            self.rayon2 = self.rayon4 / 2.3
            self.rayon1 = self.rayon4 / 5

        if self.zoom == 6 :
            self.bd_p = 10
            self.rayon8 = 0
            self.rayon7 = 0
            self.rayon6 = 0
            self.rayon5 = 0
            self.rayon4 = 0
            self.rayon3 = self.height() - 10   - 40
            self.rayon2 = self.rayon3 / 1.36
            self.rayon1 = self.rayon3 / 3

        if self.zoom == 7 :
            self.bd_p = 10
            self.rayon8 = 0
            self.rayon7 = 0
            self.rayon6 = 0
            self.rayon5 = 0
            self.rayon4 = 0
            self.rayon3 = 0
            self.rayon2 = self.height() - 10   - 40
            self.rayon1 = self.rayon2 / 2.25

        if self.zoom == 8 :
            self.bd_p = 40
            self.rayon8 = 0
            self.rayon7 = 0
            self.rayon6 = 0
            self.rayon5 = 0
            self.rayon4 = 0
            self.rayon3 = 0
            self.rayon2 = 0
            self.rayon1 = self.height() - 10   - 40

        #les positions des anneaux et des planètes centrés

        self.pos8x = self.width() / 2 - self.rayon8 / 2
        self.pos8y = self.height() / 2 - self.rayon8 / 2 + 15


        self.pos7x = self.width() / 2 - self.rayon7 / 2
        self.pos7y = self.height() / 2 - self.rayon7 / 2 + 15


        self.pos6x = self.width() / 2 - self.rayon6 / 2
        self.pos6y = self.height() / 2 - self.rayon6 / 2 + 15


        self.pos5x = self.width() / 2 - self.rayon5 / 2
        self.pos5y = self.height() / 2 - self.rayon5 / 2 + 15


        self.pos4x = self.width() / 2 - self.rayon4 / 2
        self.pos4y = self.height() / 2 - self.rayon4 / 2 + 15


        self.pos3x = self.width() / 2 - self.rayon3 / 2
        self.pos3y = self.height() / 2 - self.rayon3 / 2 + 15


        self.pos2x = self.width() / 2 - self.rayon2 / 2
        self.pos2y = self.height() / 2 - self.rayon2 / 2 + 15


        self.pos1x = self.width() / 2 - self.rayon1 / 2
        self.pos1y = self.height() / 2 - self.rayon1 / 2 + 15




    def paintEvent(self,e):   #Fonction qui va "peindre" la fenetre, c'est l'affichage
        painter = QPainter(self)
        pen = QPen()

        #Un rectangle de la taille de la fenetre pour un fond noir
        couleurFond = QColor(0,0,0)
        painter.fillRect(0, 0, self.width(), self.height(), couleurFond)

        colorTour = QColor(0, 150, 255)
        pen = QPen()
        pen.setColor(colorTour)
        painter.setPen(pen)

        #conditions pour afficher le cercle décrivant la trajectoire des planètes
        if self.zoom <= 8 :
            painter.drawEllipse(self.pos1x,self.pos1y,self.rayon1,self.rayon1)
            if self.zoom <= 7 :
                painter.drawEllipse(self.pos2x,self.pos2y,self.rayon2,self.rayon2)
                if self.zoom <= 6 :
                    painter.drawEllipse(self.pos3x,self.pos3y,self.rayon3,self.rayon3)
                    if self.zoom <= 5 :
                        painter.drawEllipse(self.pos4x,self.pos4y,self.rayon4,self.rayon4)
                        if self.zoom <= 4 :
                            painter.drawEllipse(self.pos5x,self.pos5y,self.rayon5,self.rayon5)
                            if self.zoom <= 3 :
                                painter.drawEllipse(self.pos6x,self.pos6y,self.rayon6,self.rayon6)
                                if self.zoom <= 2 :
                                    painter.drawEllipse(self.pos7x,self.pos7y,self.rayon7,self.rayon7)
                                    if self.zoom <= 1 :
                                        painter.drawEllipse(self.pos8x,self.pos8y,self.rayon8,self.rayon8)

        #affichage du soleil au centre
        color = QColor(255,255,0)
        pen.setColor(color)
        painter.setPen(pen)
        brush = QBrush()
        brush.setColor(color)
        brush.setStyle(Qt.SolidPattern)
        painter.setBrush(brush)
        painter.drawEllipse(self.width() / 2 - self.bd_s / 2,self.height() / 2 - self.bd_s / 2 + 15,self.bd_s,self.bd_s)


        #un enchainement de conditions ( if ) afin de pouvoir maitriser le zoom en supprimant l'affichage des planètes qui ne sont plus à l'écran
        if self.zoom <= 8 :
            color = QColor(218, 65, 32)
            pen.setColor(color)
            painter.setPen(pen)
            brush = QBrush()
            brush.setColor(color)
            brush.setStyle(Qt.SolidPattern)
            painter.setBrush(brush)
            painter.drawEllipse(self.width() / 2 - (self.bd_p / 2) + (self.rayon1 / 2) * math.cos(self.angle1) , self.height() / 2 - (self.bd_p / 2) + 15 + (self.rayon1/2) * math.sin(self.angle1) , self.bd_p,self.bd_p)

            if self.zoom <= 7 :
                color = QColor(0,255,255)
                pen.setColor(color)
                painter.setPen(pen)
                brush = QBrush()
                brush.setColor(color)
                brush.setStyle(Qt.SolidPattern)
                painter.setBrush(brush)
                painter.drawEllipse(self.width() / 2 - (self.bd_p / 2) + (self.rayon2 / 2) * math.cos(self.angle2) , self.height() / 2 - (self.bd_p / 2) + 15 + (self.rayon2/2) * math.sin(self.angle2) , self.bd_p,self.bd_p)

                if self.zoom <= 6 :
                    color = QColor(255,228,181)
                    pen.setColor(color)
                    painter.setPen(pen)
                    brush = QBrush()
                    brush.setColor(color)
                    brush.setStyle(Qt.SolidPattern)
                    painter.setBrush(brush)
                    painter.drawEllipse(self.width() / 2 - (self.bd_p / 2) + (self.rayon3 / 2) * math.cos(self.angle3) , self.height() / 2 - (self.bd_p / 2) + 15 + (self.rayon3/2) * math.sin(self.angle3) , self.bd_p,self.bd_p)

                    if self.zoom <= 5 :
                        color = QColor(222,184,135)
                        pen.setColor(color)
                        painter.setPen(pen)
                        brush = QBrush()
                        brush.setColor(color)
                        brush.setStyle(Qt.SolidPattern)
                        painter.setBrush(brush)
                        painter.drawEllipse(self.width() / 2 - (self.bd_p / 2) + (self.rayon4 / 2) * math.cos(self.angle4) , self.height() / 2 - (self.bd_p / 2) + 15 + (self.rayon4/2) * math.sin(self.angle4) , self.bd_p,self.bd_p)

                        if self.zoom <= 4 :
                            color = QColor(178,34,34)
                            pen.setColor(color)
                            painter.setPen(pen)
                            brush = QBrush()
                            brush.setColor(color)
                            brush.setStyle(Qt.SolidPattern)
                            painter.setBrush(brush)
                            painter.drawEllipse(self.width() / 2 - (self.bd_p / 2) + (self.rayon5 / 2) * math.cos(self.angle5) , self.height() / 2 - (self.bd_p / 2) + 15 + (self.rayon5/2) * math.sin(self.angle5) , self.bd_p,self.bd_p)

                            if self.zoom <= 3 :
                                color = QColor(0,0,255)
                                pen.setColor(color)
                                painter.setPen(pen)
                                brush = QBrush()
                                brush.setColor(color)
                                brush.setStyle(Qt.SolidPattern)
                                painter.setBrush(brush)
                                painter.drawEllipse(self.width() / 2 - (self.bd_p / 2) + (self.rayon6 / 2) * math.cos(self.angle6) , self.height() / 2 - (self.bd_p / 2) + 15 + (self.rayon6/2) * math.sin(self.angle6) , self.bd_p,self.bd_p)

                                if self.zoom <= 2 :
                                    color = QColor(255,140,0)
                                    pen.setColor(color)
                                    painter.setPen(pen)
                                    brush = QBrush()
                                    brush.setColor(color)
                                    brush.setStyle(Qt.SolidPattern)
                                    painter.setBrush(brush)
                                    painter.drawEllipse(self.width() / 2 - (self.bd_p / 2) + (self.rayon7 / 2) * math.cos(self.angle7) , self.height() / 2 - (self.bd_p / 2) + 15 + (self.rayon7/2) * math.sin(self.angle7) , self.bd_p,self.bd_p)

                                    if self.zoom <= 1 :
                                        color = QColor(100,149,237)
                                        pen.setColor(color)
                                        painter.setPen(pen)
                                        brush = QBrush()
                                        brush.setColor(color)
                                        brush.setStyle(Qt.SolidPattern)
                                        painter.setBrush(brush)
                                        painter.drawEllipse(self.width() / 2 - (self.bd_p / 2) + (self.rayon8 / 2) * math.cos(self.angle8) , self.height() / 2 - (self.bd_p / 2) + 15 + (self.rayon8/2) * math.sin(self.angle8) , self.bd_p,self.bd_p)

        #histoire de dates, pas encore utile
        '''
        painter.setPen(pen)
        font = painter.font()
        font.setPointSize(self.width() / 50)
        painter.setFont(font)
        painter.drawText(self.width()/1.5, self.height() / 12, str(self.dateJour))
        painter.drawText(self.width()/1.3 + self.width()/50 * 8, self.height() / 12, str(self.dateAnnée))

        if self.dateMois == 10 :
            painter.drawText(self.width()/1.4 + self.width()/50*2, self.height() / 12, 'JANVIER')

        if self.dateMois == 2 :
            painter.drawText(self.width()/1.4 + self.width()/50*2, self.height() / 12, 'FEVRIER')

        if self.dateMois == 3 :
            painter.drawText(self.width()/1.4 + self.width()/50*2, self.height() / 12, 'MARS')

        if self.dateMois == 4 :
            painter.drawText(self.width()/1.4 + self.width()/50*2, self.height() / 12, 'AVRIL')

        if self.dateMois == 5 :
            painter.drawText(self.width()/1.4 + self.width()/50*2, self.height() / 12, 'MAI')

        if self.dateMois == 6 :
            painter.drawText(self.width()/1.4 + self.width()/50*2, self.height() / 12, 'JUIN')

        if self.dateMois == 7 :
            painter.drawText(self.width()/1.4 + self.width()/50*2, self.height() / 12, 'JUILLET')

        if self.dateMois == 8 :
            painter.drawText(self.width()/1.4 + self.width()/50*2, self.height() / 12, 'AOUT')

        if self.dateMois == 1 :
            painter.drawText(self.width()/1.4 + self.width()/50*2, self.height() / 12, 'SEPTEMBRE')

        if self.dateMois == 10 :
            painter.drawText(self.width()/1.4 + self.width()/50*2, self.height() / 12, 'OCTOBRE')

        if self.dateMois == 11 :
            painter.drawText(self.width()/1.4 + self.width()/50*2, self.height() / 12, 'NOVEMBRE')

        if self.dateMois == 12 :
            painter.drawText(self.width()/1.4 + self.width()/50*2, self.height() / 12, 'DECEMBRE')
        '''

        if -0.5 < self.angle3 / 2 * pi < 0.5 :
            self.dateAnnée += 1


    def arreteAnny(self): #fonction lié au bouton stop pour arreter l'animation
        self.anny = 0

    def lanceAnny(self): #fonction lié au bouton stop pour lancer ou relancer l'animation
        self.anny = 1




    def animate(self):

        #une condition est posé avec anny pour savoir si les planètes doivent tourner ou pas
        if self.anny == 0 :
            self.repaint()

        if self.anny == 1 :      #si elles tournent alors la terre prendra la valeur aribtraire de vitesse de rotation quand les autres planètes auront une vitesse à l'échelle, proportionnelle ( produit en croix )
            self.angle3 += self.vitesse
            self.angle8 += self.vitesse /164.78
            self.angle7 += self.vitesse /84.0180
            self.angle6 += self.vitesse /29.457
            self.angle5 += self.vitesse /11.8620
            self.angle4 += self.vitesse /1.8808
            self.angle2 += self.vitesse /0.6152
            self.angle1 += self.vitesse /0.2408

        self.repaint()


if __name__ == '__main__':

    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())