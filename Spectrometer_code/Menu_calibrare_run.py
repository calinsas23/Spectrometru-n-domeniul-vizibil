import cv2
import numpy as np
import matplotlib.pyplot as afisare
import PySimpleGUI as psg
import time
from calibrare import calibrare
from run_spectrometru import run_spectometru_interfata_grafica

#from picamera import PiCamera
#----Creare fereastra principala---------------------------------------------------------------------------------------------------------------------------------
def functie_principala_menu(incapsulare_tip_output,x_ferestre,y_ferestre,incapsulare_analiza):
	interfata_menu = [
            [psg.Button('Calibrate_red', key='calib_rosu', size=(15, 2)),
             psg.Button('Calibrate_blue', key='calib_albastru', size=(15, 2)),
             psg.Button('Run', key='start', size=(15, 2))]
            ]
	fereastra_menu = psg.Window('Menu', interfata_menu, finalize=True, size=(400, 100))
    #----Initializari globale---------------------------------------------------------------------------------------------------------------------------------------
	rosu_setat= False
	albastru_setat=False
	albastru=1
	rosu=2
	path = "/home/pi/Desktop/Spectrometru/Cod/frame.jpg"
    #----Loop de eventuri--------------------------------------------------------------------------------------------------------------------------------------------
	while True:
		event_meniu, valoare_menu = fereastra_menu.read()
		if event_meniu == psg.WIN_CLOSED:
			break
    #----Calibrare rosu----------------------------------------------------------------------------------------------------------------------------------------------
		if event_meniu == 'calib_rosu':
			linie_rosu,col_rosu,confirmare_set=calibrare(rosu,path,x_ferestre,y_ferestre,incapsulare_analiza)
			print(linie_rosu,col_rosu)
			if confirmare_set==True:
				rosu_setat=True
			if rosu_setat == False:
				psg.popup("Red color calibration was not done")
    #----Calibrare albastru------------------------------------------------------------------------------------------------------------------------------------------
		if event_meniu == 'calib_albastru':
			linie_albastru,col_albastru,confirmare_set=calibrare(albastru,path,x_ferestre,y_ferestre,incapsulare_analiza)
			print(linie_albastru,col_albastru)
			if confirmare_set == True:
				albastru_setat=True
			if albastru_setat == False:
				psg.popup("Blue color calibration was not done")
    #----Verificare conditii pentru a trece la analiza propriu zisa---------------------------------------------------------------------------------------------------
		if event_meniu == 'start' and rosu_setat==False:
			psg.popup("Red color calibration was not done")
		if event_meniu == 'start' and albastru_setat==False:
			psg.popup("Blue color calibration was not done")
    #----Daca conditiile de calibrare sunt indeplinite se porneste analiza propriu zisa-------------------------------------------------------------------------------
		if event_meniu == 'start' and albastru_setat == True and rosu_setat==True:
			run_spectometru_interfata_grafica(linie_rosu,col_rosu,linie_albastru,col_albastru,path,incapsulare_tip_output,incapsulare_analiza)
	fereastra_menu.close()


