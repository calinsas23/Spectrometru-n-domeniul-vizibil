import numpy as np
import time
from PIL import Image
from matplotlib import pyplot as plt
from io import BytesIO
import cv2
from skimage import color
from numpy import asarray
import array as arr
import PIL
from PIL import Image
from picamera import PiCamera
import PySimpleGUI as psg

def realizare_fotografie():
	camera = PiCamera()
	camera.vflip = True
	camera.resolution = (1920, 1080)
	camera.capture("frame.jpg")
	camera.close()
	return 0
	
def Analiza_delimitare_coloana_calibrare(img_run_spect, incapsulare_tip_analiza,incapsulare_analiza):
    #albastru
    if incapsulare_analiza ==1:
        if incapsulare_tip_analiza == 1:
            height, width, _ = img_run_spect.shape
            for x in range(0,width):
                for y in range(150,350):
                    b, g, r = img_run_spect[y, x]
                    if b >= 130 and g < 50 and r < 50:
                        return x, y
    #rosu
        elif incapsulare_tip_analiza == 2:
            height, width, _ = img_run_spect.shape
            for x in range(width - 1220, 1, -1):
                for y in range(150,350):
                    b, g, r = img_run_spect[y, x]
                    if r >= 100 and g < 70 and b < 50:  
                        return x, y
    elif incapsulare_analiza ==2:
    #albastru
        if incapsulare_tip_analiza == 1:
            height, width, _ = img_run_spect.shape
            for x in range(width - 100, 1, -1):
                for y in range(300,550):
                    b, g, r = img_run_spect[y, x]
                    if b >= 130 and g < 50 and r < 50:
                        return x, y
    #rosu
        elif incapsulare_tip_analiza == 2:
            height, width, _ = img_run_spect.shape
            for x in range(1000,width):
                for y in range(300,550):
                    b, g, r = img_run_spect[y, x]
                    if r >= 100 and g < 70 and b < 50:  
                        return x, y
    return 0,0

def deseneaza_linie(img_run_spect, x, a):
    height, width, _ = img_run_spect.shape
    # deseneaza vertical
    if a == 1:
        for y in range(height):
            img_run_spect[y, x] = (255, 255, 255)
    # deseneaza orizontal
    elif a == 2:
        for y in range(width):
            img_run_spect[x, y] = (255, 255, 255)

# --------------------------------------------------------------------------------------------------------

def afisare_zona_utila_calibrare(img_copie, coloana_in_functii, y_in_functii, n, m, incapsulare_tip_analiza,
                                 deseneaza_orizontal, deseneaza_vertical,incapsulare_analiza):
    if incapsulare_tip_analiza == 1:
        linie_optima_calculata = linie_maxima(img_copie, n, m)
        deseneaza_linie(img_copie, coloana_in_functii, deseneaza_vertical)
        deseneaza_linie(img_copie, linie_optima_calculata, deseneaza_orizontal)
        if incapsulare_analiza==1:
            zona_de_interes = img_copie[y_in_functii - 100:y_in_functii + 100,
                          coloana_in_functii-20:coloana_in_functii + 700]
        elif incapsulare_analiza==2:
            zona_de_interes = img_copie[y_in_functii - 100:y_in_functii + 100,
                          coloana_in_functii -500:coloana_in_functii +150]
        return zona_de_interes
    elif incapsulare_tip_analiza == 2:
        linie_optima_calculata = linie_maxima(img_copie, n, m)
        deseneaza_linie(img_copie, coloana_in_functii, deseneaza_vertical)
        deseneaza_linie(img_copie, linie_optima_calculata, deseneaza_orizontal)
        if incapsulare_analiza==1:
            zona_de_interes = img_copie[y_in_functii-100:y_in_functii + 100,
                          coloana_in_functii - 400:coloana_in_functii + 100]
        elif incapsulare_analiza==2:
            zona_de_interes = img_copie[y_in_functii-100:y_in_functii + 100,
                          coloana_in_functii -150 :coloana_in_functii +500]
        return zona_de_interes


# nu avem exceptie, nu se poate ajunge aici daca calibrarea nu e facuta corespunzator
#sau daca sursa nu emite datorita tratarii acelor exceptii inainte de apelarea functiei.


def linie_maxima(img_gri, n, m):
    img_gray = color.rgb2gray(img_gri)
    img_de_calibrare = asarray(img_gray)
    linie_optima = 0
    suma_maxima=0
    for i in range(n):
        suma_curenta = 0
        for j in range(m):
            suma_curenta = suma_curenta + img_de_calibrare[i][j]
        if suma_curenta > suma_maxima:
            suma_maxima = suma_curenta
            linie_optima=i
    return linie_optima

def functie_analiza_imagine(incapsulare_tip_analiza,img_pt_rosu,img_pt_albastru,n, m,f_calib,incapsulare_analiza):
    #incapsulari locale
    deseneaza_vertical = 1
    deseneaza_orizontal = 2
    flag_lipsa_lumina=0
    if incapsulare_tip_analiza == 1:
        if incapsulare_analiza==1:
            coloana1_in_functii, y_albastru_in_functii = Analiza_delimitare_coloana_calibrare(img_pt_albastru,incapsulare_tip_analiza,incapsulare_analiza)
            if coloana1_in_functii==0 or y_albastru_in_functii==0:
                #tratare exceptie
                zona_de_interes_convertita=0
                flag_lipsa_lumina=1
                psg.popup("The blue source does not emit")
                f_calib.close()
            else:
            # print("Albastru: ", coloana1_in_functii)
                zona_de_interes = afisare_zona_utila_calibrare(img_pt_albastru, coloana1_in_functii, y_albastru_in_functii, n,m, incapsulare_tip_analiza, deseneaza_orizontal,deseneaza_vertical,incapsulare_analiza)
                color_coverted = cv2.cvtColor(zona_de_interes, cv2.COLOR_BGR2RGB)
                zona_de_interes_convertita = Image.fromarray(color_coverted)
            return coloana1_in_functii, y_albastru_in_functii, zona_de_interes_convertita,flag_lipsa_lumina
        elif incapsulare_analiza==2:
            coloana2_in_functii, y_albastru_in_functii = Analiza_delimitare_coloana_calibrare(img_pt_albastru,incapsulare_tip_analiza,incapsulare_analiza)
            if coloana2_in_functii==0 or y_albastru_in_functii==0:
                #tratare exceptie
                zona_de_interes_convertita=0
                flag_lipsa_lumina=1
                psg.popup("The blue source does not emit")
                f_calib.close()
            else:
            # print("Albastru: ", coloana1_in_functii)
                zona_de_interes = afisare_zona_utila_calibrare(img_pt_albastru, coloana2_in_functii, y_albastru_in_functii, n,m, incapsulare_tip_analiza, deseneaza_orizontal,deseneaza_vertical,incapsulare_analiza)
                color_coverted = cv2.cvtColor(zona_de_interes, cv2.COLOR_BGR2RGB)
                zona_de_interes_convertita = Image.fromarray(color_coverted)
            return coloana2_in_functii, y_albastru_in_functii, zona_de_interes_convertita,flag_lipsa_lumina
    elif incapsulare_tip_analiza == 2:
        if incapsulare_analiza==1:
            coloana2_in_functii, y_rosu_in_functii = Analiza_delimitare_coloana_calibrare(img_pt_rosu, incapsulare_tip_analiza,incapsulare_analiza)
            if coloana2_in_functii==0 or y_rosu_in_functii==0:
                zona_de_interes_convertita=0
                flag_lipsa_lumina=1
                psg.popup("The red source does not emit")
                f_calib.close()
            else:
                zona_de_interes = afisare_zona_utila_calibrare(img_pt_albastru, coloana2_in_functii, y_rosu_in_functii, n,
                                                       m, incapsulare_tip_analiza, deseneaza_orizontal,
                                                       deseneaza_vertical,incapsulare_analiza)
                color_coverted = cv2.cvtColor(zona_de_interes, cv2.COLOR_BGR2RGB)
                zona_de_interes_convertita = Image.fromarray(color_coverted)
            return coloana2_in_functii,y_rosu_in_functii, zona_de_interes_convertita,flag_lipsa_lumina
        elif incapsulare_analiza==2:
            coloana1_in_functii, y_rosu_in_functii = Analiza_delimitare_coloana_calibrare(img_pt_rosu, incapsulare_tip_analiza,incapsulare_analiza)
            if coloana1_in_functii==0 or y_rosu_in_functii==0:
                zona_de_interes_convertita=0
                flag_lipsa_lumina=1
                psg.popup("The red source does not emit")
                f_calib.close()
            else:
                zona_de_interes = afisare_zona_utila_calibrare(img_pt_albastru, coloana1_in_functii, y_rosu_in_functii, n,
                                                       m, incapsulare_tip_analiza, deseneaza_orizontal,
                                                       deseneaza_vertical,incapsulare_analiza)
                color_coverted = cv2.cvtColor(zona_de_interes, cv2.COLOR_BGR2RGB)
                zona_de_interes_convertita = Image.fromarray(color_coverted)
            # conversie la pill

            return coloana1_in_functii,y_rosu_in_functii, zona_de_interes_convertita,flag_lipsa_lumina
