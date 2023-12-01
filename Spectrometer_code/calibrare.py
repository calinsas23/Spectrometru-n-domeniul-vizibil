import PySimpleGUI as psg
from io import BytesIO
from PIL import Image
import numpy as np
import time
import cv2
import sys
from matplotlib import pyplot as plt
from Analiza import functie_analiza_imagine
from Analiza import realizare_fotografie


# ----conversie imagine pt afisare in graph-----------------------------------------------------------------------------------
def array_to_data(array):
    im = Image.fromarray(array)
    with BytesIO() as output:
        im.save(output, format="PNG")
        data = output.getvalue()
    return data


# ----functia de afisare in graph-------- """camera - al 3 lea param--------------------------------------------------------------------------------------
def afisare_img_in_graph(graph,incapsulare_tip_calibrare,f_calib,n,m,img_pt_rosu,img_pt_albastru,incapsulare_analiza):
    height = 1080
    # albastru
    if incapsulare_tip_calibrare == 1:
        if incapsulare_analiza==1:
            coloana1, y_albastru, zona_utila_albastru,flag_lipsa_lumina= functie_analiza_imagine(incapsulare_tip_calibrare,img_pt_rosu,img_pt_albastru,n, m,f_calib,incapsulare_analiza)
            auxiliar_array = np.array(zona_utila_albastru, dtype=np.uint8)
        elif incapsulare_analiza==2:
            coloana2, y_albastru, zona_utila_albastru,flag_lipsa_lumina= functie_analiza_imagine(incapsulare_tip_calibrare,img_pt_rosu,img_pt_albastru,n, m,f_calib,incapsulare_analiza)
            auxiliar_array = np.array(zona_utila_albastru, dtype=np.uint8)
    # rosu
    elif incapsulare_tip_calibrare == 2:
        if incapsulare_analiza==1:
            coloana2, y_rosu, zona_utila_rosu,flag_lipsa_lumina= functie_analiza_imagine(incapsulare_tip_calibrare,img_pt_rosu,img_pt_albastru,n, m,f_calib,incapsulare_analiza)
            auxiliar_array = np.array(zona_utila_rosu, dtype=np.uint8)
        elif incapsulare_analiza==2:
            coloana1, y_rosu, zona_utila_rosu,flag_lipsa_lumina= functie_analiza_imagine(incapsulare_tip_calibrare,img_pt_rosu,img_pt_albastru,n, m,f_calib,incapsulare_analiza)
            auxiliar_array = np.array(zona_utila_rosu, dtype=np.uint8)
    # functie de analiza img
    if flag_lipsa_lumina==0:
        data = array_to_data(auxiliar_array)
        graph.draw_image(data=data, location=(0, height))
        if incapsulare_tip_calibrare == 1:
            if incapsulare_analiza==1:
                f_calib['coloana'].Update('Column: ' + str(coloana1))
                f_calib['linie'].Update('Line: ' + str(y_albastru))
                return coloana1, y_albastru
            elif incapsulare_analiza==2:
                f_calib['coloana'].Update('Column: ' + str(coloana2))
                f_calib['linie'].Update('Line: ' + str(y_albastru))
                return coloana2, y_albastru
        elif incapsulare_tip_calibrare == 2:
            if incapsulare_analiza==1:
                f_calib['coloana'].Update('Column: ' + str(coloana2))
                f_calib['linie'].Update('Line: ' + str(y_rosu))
                return coloana2, y_rosu
            elif incapsulare_analiza==2:
                f_calib['coloana'].Update('Column: ' + str(coloana1))
                f_calib['linie'].Update('Line: ' + str(y_rosu))
                return coloana1, y_rosu
    if incapsulare_tip_calibrare == 1:
        if incapsulare_analiza==1:
            return coloana1, y_albastru
        elif incapsulare_analiza==2:
            return coloana2, y_albastru
    elif incapsulare_tip_calibrare == 2:
        if incapsulare_analiza==1: 
            return coloana2, y_rosu
        elif incapsulare_analiza==2:
            return coloana1, y_rosu

# ----functia propriu zisa de calibrare------------------------------------------------------------------------------------------
def calibrare(incapsulare_tip_calibrare,path,x_ferestre,y_ferestre,incapsulare_analiza):
    # ----declaratii variabile globale pt Calibrare(incluzand alea din Analiza-----------------------------------------------------------------------------------------------
    width, height = 1920, 1080
    confirmare_set = False
    linie_set = 0
    coloana_set = 0
    # ----creare graph plus layout----------------------------------------------------------------------------------------------------
    container = psg.Graph(
        canvas_size=(x_ferestre, y_ferestre-150),
        graph_bottom_left=(0, 0),
        graph_top_right=(width, height),
        enable_events=True,
        drag_submits=True, key="Graph")
    layout_calib = [
        [container],
        [psg.Text('', size=(10, 1), font=("Arial", 15), key='linie')],
        [psg.Text('', size=(15, 1), font=("Arial", 15), key='coloana')],
        [psg.Button('Set', key='set', size=(15, 2)), psg.Push(), psg.Button('Close', key='close', size=(15, 2))]
    ]
    f_calib = psg.Window('Calibration', layout_calib, finalize=True,size=(x_ferestre, y_ferestre))
    graph = f_calib["Graph"]
    # ----Loop ul pt eventuri cu timeout de 0.5 sec-------------------------------------------------------------------------------------
    #    Daca in 0.5 sec nu se apasa un buton => se repeta loopul=> se face si se incarca alta fotografie------------------------------
    while True:
        if confirmare_set==False:
            realizare_fotografie()
            img_pt_rosu = cv2.imread(path)
            img_pt_albastru = img_pt_rosu.copy()
            n, m, c = img_pt_rosu.shape
        # ----Apel functie de captura si afisare img plus cod de test img cu un plot--------------------------------------------------------
            coloana_calibrata, linie_calibrata = afisare_img_in_graph(graph,incapsulare_tip_calibrare,f_calib,n,m,img_pt_rosu,img_pt_albastru,incapsulare_analiza)
        # ----evaluare events---------------------------------------------------------------------------------------------------------------
        event, values = f_calib.Read(timeout=7000)
        if event == 'close' or event == psg.WIN_CLOSED:
            f_calib.close()
            break
        if event == 'set':
            confirmare_set = True
            linie_set = linie_calibrata
            coloana_set = coloana_calibrata
            f_calib.close()
    return linie_set, coloana_set, confirmare_set


