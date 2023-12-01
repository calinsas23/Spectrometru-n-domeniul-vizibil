import PySimpleGUI as psg
from Selectare_tip_analiza import selectare_analiza
incapsulare_tip_output=0
x_ferestre=0
y_ferestre=0
interfata_display = [
    [psg.Button('HDMI', key='monitor', size=(15, 2)),psg.Push(), psg.Button('Display', key='display', size=(15, 2))]
                ]
fereastra_display = psg.Window('Output adapt', interfata_display, finalize=True,size=(400, 100))
while True:
    event_display, valoare_display = fereastra_display.read()
    if event_display == 'monitor':
        incapsulare_tip_output=1
        x_ferestre=600
        y_ferestre=800
        break
    if event_display == 'display':
        incapsulare_tip_output=2
        x_ferestre=480
        y_ferestre=320
        break
    if event_display == psg.WIN_CLOSED:
        fereastra_display.close()
        break
#------se verifica selectarea unei optiuni-------------------------------------------
if incapsulare_tip_output!=0:
    fereastra_display.close()
    selectare_analiza(incapsulare_tip_output,x_ferestre,y_ferestre)
else:
    fereastra_display.close()
    
    

    
        
