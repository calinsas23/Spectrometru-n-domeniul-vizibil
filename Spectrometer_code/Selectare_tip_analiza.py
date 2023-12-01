import PySimpleGUI as psg
from Menu_calibrare_run import functie_principala_menu
def selectare_analiza(incapsulare_tip_output,x_ferestre,y_ferestre):
    incapsulare_analiza=0
    interfata_mod_analiza = [
        [psg.Button('Individual  spectrometer', key='singur', size=(15, 3)),psg.Push(), psg.Button('Spectrometer with selector', key='cu_selector', size=(15, 3))]
                ]
    fereastra_mod_analiza = psg.Window('Select analysis type', interfata_mod_analiza, finalize=True,size=(400, 100))
    while True:
        event_select_analiza, valoare_select_analiza = fereastra_mod_analiza.read()
        if event_select_analiza == 'singur':
            incapsulare_analiza=1
            break
        if event_select_analiza == 'cu_selector':
            incapsulare_analiza=2
            break
        if event_select_analiza == psg.WIN_CLOSED:
            fereastra_display.close()
            break
    if incapsulare_analiza!=0:
        fereastra_mod_analiza.close()
        functie_principala_menu(incapsulare_tip_output,x_ferestre,y_ferestre,incapsulare_analiza)
    else:
        fereastra_mod_analiza.close()
    
