import PySimpleGUI as psg
from Analiza import realizare_fotografie
from calibrare import array_to_data
import cv2
import numpy as np
from PIL import Image
from matplotlib import pyplot as afisare
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.animation as animation
import time
import datetime

def run_afisare_zona_utila_analiza(graph1,img_analiza,coloana1_in_functii, coloana2_in_functii, y_albastru_in_functii,y_rosu_in_functii,contor,ax,figure_canvas_agg,adaptare_zona_utila,incapsulare_analiza):
    height =1080
    if incapsulare_analiza==1:
        zona_de_interes = img_analiza[min(y_albastru_in_functii,y_rosu_in_functii)-adaptare_zona_utila:max(y_albastru_in_functii,y_rosu_in_functii)+adaptare_zona_utila,
                      coloana1_in_functii-10:coloana2_in_functii+150]
    if incapsulare_analiza==2:
        zona_de_interes = img_analiza[min(y_albastru_in_functii,y_rosu_in_functii)-adaptare_zona_utila:max(y_albastru_in_functii,y_rosu_in_functii)+adaptare_zona_utila,
                      coloana2_in_functii-40:coloana1_in_functii+150]
    #conversie la Pil
    color_coverted = cv2.cvtColor(zona_de_interes, cv2.COLOR_BGR2RGB)
    zona_de_interes_convertita = Image.fromarray(color_coverted)
    auxiliar_array = np.array(zona_de_interes_convertita, dtype=np.uint8)
    data = array_to_data(auxiliar_array)
    graph1.draw_image(data=data, location=(0, height))
    realizare_grafic(img_analiza, coloana1_in_functii, coloana2_in_functii, y_albastru_in_functii, y_rosu_in_functii,contor,ax,figure_canvas_agg,incapsulare_analiza)
    return 0


    # Save the plot to the file
def realizare_grafic(frame,coloana1_in_functii,coloana2_in_functii,linie_albastru, linie_rosu,contor,ax,figure_canvas_agg,incapsulare_analiza):
    imagine_gri = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    luminanta =[]
    x = []
    luminanta_vector =[]
    if linie_rosu==linie_albastru:
        for j in range(min(coloana1_in_functii,coloana2_in_functii),max(coloana1_in_functii,coloana2_in_functii)):
            luminanta.append(imagine_gri[linie_rosu][j])
    else:
        
        for j in range(min(coloana1_in_functii,coloana2_in_functii),max(coloana1_in_functii,coloana2_in_functii)+10):
            suma_col = 0
            for i in range(min(linie_albastru, linie_rosu), max(linie_albastru, linie_rosu)):
                suma_col += imagine_gri[i][j]
            luminanta.append(suma_col / (abs(linie_albastru - linie_rosu) + 1))
            
    lungime=len(luminanta)
    if incapsulare_analiza==1:
        x_values=np.linspace(400,700,lungime)
        x_extins=np.linspace(350,750,600)
        luminanta_interpolata=np.zeros_like(x_extins)
        indici=np.where((x_extins>=400)&(x_extins<=700))[0]
        luminanta_interpolata[indici]=np.interp(x_extins[indici],x_values,luminanta)
        if contor==1:
            ax.plot(x_extins, luminanta_interpolata)
            ax.set_title("Grafic_analiza")
            ax.set_xlabel('Pixeli')
            ax.set_ylabel('Intensitate')
            afisare.xlim(350,750)
            figure_canvas_agg.draw()
            figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
        if contor==0:
            ax.clear()
            ax.plot(x_extins, luminanta_interpolata)
            ax.set_title("Grafic analiza")
            ax.set_xlabel('Pixeli')
            ax.set_ylabel('Intensitate')
            afisare.xlim(350,750)
            figure_canvas_agg.draw()          
    if incapsulare_analiza==2:
        luminanta2=luminanta[::-1]
        x_values=np.linspace(400,700,lungime)
        x_extins=np.linspace(350,750,600)
        luminanta_interpolata=np.zeros_like(x_extins)
        indici=np.where((x_extins>=400)&(x_extins<=700))[0]
        luminanta_interpolata[indici]=np.interp(x_extins[indici],x_values,luminanta2)
        if contor==1:
            ax.plot(x_extins, luminanta_interpolata)
            ax.set_title("Analysis chart")
            ax.set_xlabel('Pixels')
            ax.set_ylabel('Intensity')
            afisare.xlim(750,350)
            figure_canvas_agg.draw()
            figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
        if contor==0:
            ax.clear()
            ax.plot(x_extins, luminanta_interpolata)
            ax.set_title("Analysis chart")
            ax.set_xlabel('Pixels')
            ax.set_ylabel('Intensity')
            afisare.xlim(750,350)
            figure_canvas_agg.draw()
    return 0
    
def run_spectometru_interfata_grafica(linie_rosu,col_rosu,linie_albastru,col_albastru,path,incapsulare_tip_output,incapsulare_analiza):
    #----2 graph uri, constructie de grafic + resprezentare live a zonei de interes------------------------------------------
    px=1/afisare.rcParams['figure.dpi']
    if incapsulare_tip_output==2:
        fig, ax = afisare.subplots(figsize=(480*px,180*px))
        x_ferestre=480
        y_graph=51
        y_canvas=150
        y_ferestre=320
        adaptare_zona_utila=25
        buton_x=10
        buton_y=1
    if incapsulare_tip_output==1:
        fig, ax = afisare.subplots(figsize=(600*px,400*px))
        x_ferestre=600
        y_graph=250
        y_canvas=220
        y_ferestre=800
        adaptare_zona_utila=50
        buton_x=14
        buton_y=2
    width, height = 1920, 1080
    flag_analiza=1
    contor=1
    container1 = psg.Graph(
        canvas_size=(x_ferestre, y_graph),
        graph_bottom_left=(0, 0),
        graph_top_right=(width, height),
        enable_events=True,
        drag_submits=True, key="graph1")
    layout_spectro = [
        [container1],
        [psg.Canvas(size=(x_ferestre, y_canvas), key='canvas')],
        [psg.Button('Start', key='start', size=(buton_x, buton_y)),psg.Button('stop', key='stop', size=(buton_x, buton_y)),psg.Button('save', key='save', size=(buton_x, buton_y)),psg.Push(),psg.Button('close', key='close', size=(buton_x, buton_y)),
        [psg.Text('', size=(15, 1), font=("Arial", 15), key='update')],]
                        ]
    f_spectro = psg.Window('Analyze', layout_spectro, finalize=True,size=(x_ferestre, y_ferestre))
    graph1 = f_spectro["graph1"]
    figure_canvas_agg = FigureCanvasTkAgg(afisare.gcf(),f_spectro['canvas'].TKCanvas)
    #----Loop ul pt eventuri cu timeout de 0.5 sec-------------------------------------------------------------------------------------
    #----Ulterior buton de salvare al graficului---------------------------------------------------------------------------------------
    while True:
            #aici in functie de flag apelam functia de foto si analiza pt spectru
            #realizare_fotografie()
        if flag_analiza ==1:
            f_spectro['update'].Update('')
            realizare_fotografie()
            img_analiza = cv2.imread(path)
            if contor==1:
                run_afisare_zona_utila_analiza(graph1,img_analiza,col_albastru,col_rosu,linie_albastru,linie_rosu,1,ax,figure_canvas_agg,adaptare_zona_utila,incapsulare_analiza)
                contor-=1
            else:
                run_afisare_zona_utila_analiza(graph1, img_analiza, col_albastru, col_rosu, linie_albastru, linie_rosu,
                                                0,ax,figure_canvas_agg,adaptare_zona_utila,incapsulare_analiza)
        event, values = f_spectro.Read(timeout=3000)
        if event == 'start':
            flag_analiza=1
            psg.popup("Analysis is running")
        if event =='stop':
            flag_analiza=0
            psg.popup("Analysis has been stopped")
        if event == 'save':
            if flag_analiza==0:
                data_ora = datetime.datetime.now()
                data_ora_string=data_ora.strftime('%m-%d-%y_%H:%M:%S')
                afisare.savefig('grafic_'+data_ora_string)
                psg.popup("The chart has been saved")
            else:
                psg.popup("The analysis has not been stopped")
        if event == 'close' or event == psg.WIN_CLOSED:
            f_spectro.close()
            break


#run_spectometru_interfata_grafica(319,494,322,50,"/home/calin/Desktop/Spectrometru/Cod/test.jpg",2)
