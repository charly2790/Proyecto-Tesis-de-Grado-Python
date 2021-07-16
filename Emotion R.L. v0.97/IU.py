import tkinter
import json
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter.ttk import Combobox
from functools import partial
from tkinter.ttk import Separator
from Main import *
from tkinter.ttk import Progressbar
from pathlib import Path
import cv2
import dlib
from os import scandir
import os

def eventoCargarPath():
    tb_ruta_set.delete(0, END)
    path = None


    if opc_selec_rb.get() == 1:
        path = filedialog.askopenfilename()
    else:
        path = filedialog.askdirectory()

    try:
        path = path
    except:
        path = 'error_path'

    if path != 'error_path':
        tb_ruta_set.insert(0,path)
    else:
        messagebox.showerror('Error','Ocurrio un error al cargar la ruta indicada')

def EventoNext(claves,result,dic_index,dir,max,dic_iu_components):

    Lbl_cabecera = dic_iu_components['Lbl_head']
    Lbl_max = dic_iu_components['Lbl_max']
    Entry_anger = dic_iu_components['Entry_angry']
    Entry_contempt = dic_iu_components['Entry_contempt']
    Entry_disgust = dic_iu_components['Entry_disgust']
    Entry_fear = dic_iu_components['Entry_fear']
    Entry_happy = dic_iu_components['Entry_happy']
    Entry_neutral = dic_iu_components['Entry_neutral']
    Entry_sad = dic_iu_components['Entry_sad']
    Entry_surprise = dic_iu_components['Entry_surprise']

    Entry_anger.delete(0,END)
    Entry_contempt.delete(0,END)
    Entry_disgust.delete(0,END)
    Entry_fear.delete(0,END)
    Entry_happy.delete(0,END)
    Entry_neutral.delete(0,END)
    Entry_sad.delete(0,END)
    Entry_surprise.delete(0,END)

    pos = int(dic_index['pos'])

    if dir == 1:

        pos = pos + 1

        if pos == max:
            pos = 0
    else:

        pos = pos - 1

        if pos < 0:
            pos = max - 1


    valores = result[claves[pos]]

    Lbl_cabecera.config(text=claves[pos])
    Lbl_max.config(text="Valor predicho: "+traducir(valores['Maximo']))

    Entry_anger.insert(0, valores['Enojo'])
    Entry_contempt.insert(0, valores['Desprecio'])
    Entry_disgust.insert(0, valores['Asco'])
    Entry_fear.insert(0, valores['Miedo'])
    Entry_happy.insert(0, valores['Felicidad'])
    Entry_neutral.insert(0, valores['Neutral'])
    Entry_sad.insert(0, valores['Tristeza'])
    Entry_surprise.insert(0, valores['Sorpresa'])


    dic_index['pos'] = pos

def EventoBack(claves,dic_index,max,lbl_cabecera):

    pos = int(dic_index['pos'])

    if pos == 0:
        pos = max - 1
    else:
        pos = pos - 1

    messagebox.showinfo("Info","keys[0]:"+str(pos))

    lbl_cabecera.config(text = claves[pos])

    dic_index['pos'] = pos



def eventoPrepararPrediccion():

    #path_origen = Path(tb_ruta_set.get())

    #Opción una sola imágen
    opc_selec = opc_selec_rb.get()

    if opc_selec == 1:
        path_origen = None
        path_img = Path(tb_ruta_set.get())
    else:
        path_origen = Path(tb_ruta_set.get())
        path_img = None

    #path_img = None
    mat_param = combo_mat_param.get()
    ck_redim = ck_redim_img.get()
    result = ""

    #messagebox.showerror('dk_redim', str(ck_redim))

    try:
        result = darPrediccion(path_origen,path_img,mat_param,ck_redim)
    except:
        result = "UNKNOW_ERROR"

    if result == "UNKNOW_ERROR":
        messagebox.showerror("Ha ocurrido un error inesperado")
    elif result =="ERROR_NO_IMG_FOUND":
        messagebox.showerror("Error","No se ha encontrado ninguna imagen en el directorio indicado")
    elif result == "ERROR_LOADING_FILES":
        messagebox.showerror("Error", "Error al cargar archivos de configuraciones")
    else:

        #Decodificar JSON a diccionario
        result_decoded = json.loads(result)
        #obtengo las claves
        #keys = result_decoded.keys()
        keys = list(result_decoded)

        iu_detalle_pred = tkinter.Toplevel(window)
        iu_detalle_pred.columnconfigure(0, weight=1)
        iu_detalle_pred.columnconfigure(1, weight=1)
        iu_detalle_pred.columnconfigure(2, weight=1)
        iu_detalle_pred.columnconfigure(3, weight=1)

        tamanio_fuente = 10

        #messagebox.showinfo('Cant img', str(len(keys)) + "key[0]: "+ str(keys_2[0]))

        i = 0
        txt_label_head = keys[0]
        max = len(keys)
        dic_index = {'pos': 0}
        values = result_decoded[keys[dic_index['pos']]]
        predicted_value = traducir(values['Maximo'])

        lbl_head = Label(iu_detalle_pred, text=txt_label_head, font=(fuente_default, tamanio_default, estilo_titulo))

        lbl_max = Label(iu_detalle_pred, text="Valor predicho: " + predicted_value, font=(fuente_default, tamanio_default, estilo_titulo))

        lbl_angry = Label(iu_detalle_pred, text="Enojo", font=(fuente_default, tamanio_fuente, estilo_titulo))
        lbl_contempt = Label(iu_detalle_pred, text="Desprecio", font=(fuente_default, tamanio_fuente, estilo_titulo))
        lbl_disgust = Label(iu_detalle_pred, text="Asco", font=(fuente_default, tamanio_fuente, estilo_titulo))
        lbl_fear = Label(iu_detalle_pred, text="Miedo", font=(fuente_default, tamanio_fuente, estilo_titulo))

        lbl_happy = Label(iu_detalle_pred, text="Felicidad", font=(fuente_default, tamanio_fuente, estilo_titulo))
        lbl_neutral = Label(iu_detalle_pred, text="Neutral", font=(fuente_default, tamanio_fuente, estilo_titulo))
        lbl_sad = Label(iu_detalle_pred, text="Tristeza", font=(fuente_default, tamanio_fuente, estilo_titulo))
        lbl_surprise = Label(iu_detalle_pred, text="Sorpresa", font=(fuente_default, tamanio_fuente, estilo_titulo))

        entry_angry = Entry(iu_detalle_pred, font=(fuente_default, tamanio_fuente))
        entry_contempt = Entry(iu_detalle_pred, font=(fuente_default, tamanio_fuente))
        entry_disgust = Entry(iu_detalle_pred, font=(fuente_default, tamanio_fuente))
        entry_fear = Entry(iu_detalle_pred, font=(fuente_default, tamanio_fuente))

        entry_happy = Entry(iu_detalle_pred, font=(fuente_default, tamanio_fuente))
        entry_neutral = Entry(iu_detalle_pred, font=(fuente_default, tamanio_fuente))
        entry_sad = Entry(iu_detalle_pred, font=(fuente_default, tamanio_fuente))
        entry_surprise = Entry(iu_detalle_pred, font=(fuente_default, tamanio_fuente))

        entry_angry.insert(0, values['Enojo'])
        entry_contempt.insert(0, values['Desprecio'])
        entry_disgust.insert(0, values['Asco'])
        entry_fear.insert(0, values['Miedo'])

        entry_happy.insert(0, values['Felicidad'])
        entry_neutral.insert(0, values['Neutral'])
        entry_sad.insert(0, values['Tristeza'])
        entry_surprise.insert(0, values['Sorpresa'])

        dic_iu_components = {'Entry_angry':entry_angry,'Entry_contempt':entry_contempt,'Entry_disgust':entry_disgust,'Entry_fear':entry_fear,'Entry_happy':entry_happy
            ,'Entry_neutral':entry_neutral,'Entry_sad':entry_sad,'Entry_surprise':entry_surprise,'Lbl_head':lbl_head,'Lbl_max':lbl_max}

        btn_next = Button(iu_detalle_pred, text=">", font=(fuente_default, tamanio_default), command= lambda: EventoNext(keys,result_decoded,dic_index,1,max,dic_iu_components))
        btn_back = Button(iu_detalle_pred, text="<", font=(fuente_default, tamanio_default), command= lambda: EventoNext(keys,result_decoded,dic_index,0,max,dic_iu_components))

        #Cabecera nombre fotografía
        lbl_head.grid(sticky=NSEW, padx=5, pady=5, row=i, column=0, columnspan=4)

        i = i + 1

        # Cabecera nombre fotografía
        lbl_max.grid(sticky=NSEW, padx=5, pady=5, row=i, column=1, columnspan=2)

        i = i + 1


        #Cabecera rotulos de emociones 1)
        lbl_angry.grid(sticky=NSEW,padx=2, pady=5,row=i, column=0,columnspan=1)
        lbl_contempt.grid(sticky=NSEW, padx=2, pady=5, row=i, column=1, columnspan=1)
        lbl_disgust.grid(sticky=NSEW, padx=2, pady=5, row=i, column=2, columnspan=1)
        lbl_fear.grid(sticky=NSEW, padx=2, pady=5, row=i, column=3, columnspan=1)


        i = i + 1

        #Entrys valores emociones
        entry_angry.grid(sticky=W, padx=2, pady=5, row=i, column=0, columnspan=1)
        entry_contempt.grid(sticky=W, padx=2, pady=5, row=i, column=1, columnspan=1)
        entry_disgust.grid(sticky=W, padx=2, pady=5, row=i, column=2, columnspan=1)
        entry_fear.grid(sticky=W, padx=2, pady=5, row=i, column=3, columnspan=1)

        i = i + 1

        # Cabecera rotulos de emociones 2)
        lbl_happy.grid(sticky=NSEW, padx=2, pady=5, row=i, column=0, columnspan=1)
        lbl_neutral.grid(sticky=NSEW, padx=2, pady=5, row=i, column=1, columnspan=1)
        lbl_sad.grid(sticky=NSEW, padx=2, pady=5, row=i, column=2, columnspan=1)
        lbl_surprise.grid(sticky=NSEW, padx=2, pady=5, row=i, column=3, columnspan=1)

        i = i + 1

        entry_happy.grid(sticky=W, padx=2, pady=5, row=i, column=0, columnspan=1)
        entry_neutral.grid(sticky=W, padx=2, pady=5, row=i, column=1, columnspan=1)
        entry_sad.grid(sticky=W, padx=2, pady=5, row=i, column=2, columnspan=1)
        entry_surprise.grid(sticky=W, padx=2, pady=5, row=i, column=3, columnspan=1)

        i = i + 1

        btn_next.grid(sticky=NSEW, padx=5, pady=5, row=i+1, column=2, columnspan=2)
        btn_back.grid(sticky=NSEW, padx=5, pady=5, row=i+1, column=0, columnspan=2)










def habilitarPanelLateral():

    opc_selec = opc_selec_rb.get()

    tb_ruta_set.delete(0, END)

    messagebox.showerror('Error', str(opc_selec))



window = Tk()
window.columnconfigure(0,weight=1)
window.columnconfigure(1,weight=1)
window.columnconfigure(2,weight=1)
window.columnconfigure(3,weight=1)
window.resizable(0, 0)
window.geometry("400x300")

fuente_default="Cambria"
tamanio_default= 12
estilo_titulo = "bold"
ck_redim_img = IntVar(value=1)
opc_selec_rb = IntVar()


window.title("R.L. Reconocimiento de emociones")

rb_single = Radiobutton(window, text="Indiv.", variable=opc_selec_rb, value=1, command=habilitarPanelLateral,font=(fuente_default,tamanio_default))
rb_multiple = Radiobutton(window, text="Multiple", variable=opc_selec_rb, value=2, command=habilitarPanelLateral,font=(fuente_default,tamanio_default))
rb_multiple.select()
lbl_ruta_set = Label(window,text="Path imagen/es: ",font=(fuente_default,tamanio_default))
tb_ruta_set = Entry(window,font=(fuente_default,tamanio_default))
btn_cargar_ruta = Button(window,text="...",font=(fuente_default,tamanio_default),command=eventoCargarPath)
combo_mat_param = Combobox(window,font=(fuente_default,tamanio_default))
chkb_redim_img = Checkbutton(window, text='Redim.',font=(fuente_default,tamanio_default), variable = ck_redim_img,)

lbl_mat_param = Label(window,text="Matriz de parámetros: ",font=(fuente_default,tamanio_default))
combo_mat_param['values'] = ("RAFD_414","RAFD_1608","RAFD_1608_S_NORM","RAFD_1608_S_NORM_1200")
combo_mat_param.current(2)

btn_gen_files = Button(window, text = 'Predecir', font = (fuente_default,tamanio_default), command=eventoPrepararPrediccion)

v_col_span = 10

rb_single.grid(sticky=E,padx=5,pady=20,row = 0,column=1)
rb_single.config(state=DISABLED)
rb_multiple.grid(sticky=W,padx=5,row = 0,column=2)
lbl_ruta_set.grid(sticky=W,padx=5,row=1,column=0,columnspan=2)
tb_ruta_set.grid(sticky=W+E,padx=5,row=2,column=0,columnspan=3)
btn_cargar_ruta.grid(sticky=W+E,padx=5,row=2,column=3)
lbl_mat_param.grid(sticky=W,padx=5,pady=10,row=3,columnspan=3)
combo_mat_param.grid(sticky=NSEW,padx=5,row=4,column=0,columnspan=3)
chkb_redim_img.grid(sticky=NSEW,row=4,column=3)
btn_gen_files.grid(sticky=NSEW,row=5,column=0,padx=5,pady=20,columnspan=4)

window.mainloop()