import tkinter
import json
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter.ttk import Combobox
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

def eventoPrepararPrediccion():

    path_origen = Path(tb_ruta_set.get())
    path_img = None
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
    else:

        #Decodificar JSON a diccionario
        result_decoded = json.loads(result)
        #obtengo las claves
        keys = result_decoded.keys()

        iu_detalle_pred = tkinter.Toplevel(window)
        iu_detalle_pred.columnconfigure(0, weight=1)
        iu_detalle_pred.columnconfigure(1, weight=1)
        iu_detalle_pred.columnconfigure(2, weight=1)
        iu_detalle_pred.columnconfigure(3, weight=1)
        iu_detalle_pred.columnconfigure(4, weight=1)
        iu_detalle_pred.columnconfigure(5, weight=1)
        iu_detalle_pred.columnconfigure(6, weight=1)
        iu_detalle_pred.columnconfigure(7, weight=1)
        tamanio_fuente = 10

        i = 0
        for key in keys:

            Label(iu_detalle_pred, text=key, font=(fuente_default, tamanio_default)).grid(sticky=NSEW, padx=5,pady=5,row=i, column=2, columnspan=4)

            i = i+1

            values = result_decoded[key]

            #Cabecera de etiquetas de emociones
            Label(iu_detalle_pred, text="Enojo", font=(fuente_default, tamanio_fuente)).grid(sticky=NSEW, padx=1, pady=5,row=i, column=0, columnspan=1)
            Label(iu_detalle_pred, text="Desprecio", font=(fuente_default, tamanio_fuente)).grid(sticky=NSEW, padx=1, pady=5,row=i, column=1, columnspan=1)
            Label(iu_detalle_pred, text="Asco", font=(fuente_default, tamanio_fuente)).grid(sticky=NSEW, padx=1, pady=5,row=i, column=2, columnspan=1)
            Label(iu_detalle_pred, text="Miedo", font=(fuente_default, tamanio_fuente)).grid(sticky=NSEW, padx=1, pady=5,row=i, column=3, columnspan=1)
            Label(iu_detalle_pred, text="Felicidad", font=(fuente_default, tamanio_fuente)).grid(sticky=NSEW, padx=1, pady=5,row=i, column=4, columnspan=1)
            Label(iu_detalle_pred, text="Neutral", font=(fuente_default, tamanio_fuente)).grid(sticky=NSEW, padx=1, pady=5,row=i, column=5, columnspan=1)
            Label(iu_detalle_pred, text="Tristeza", font=(fuente_default, tamanio_fuente)).grid(sticky=NSEW, padx=1, pady=5,row=i, column=6, columnspan=1)
            Label(iu_detalle_pred, text="Sorpresa", font=(fuente_default, tamanio_fuente)).grid(sticky=NSEW, padx=1, pady=5,row=i, column=7, columnspan=1)

            i = i+1

            #Valores predichos

            Entry0=Entry(iu_detalle_pred, text=values['Enojo'], font=(fuente_default, tamanio_fuente))
            Entry1=Entry(iu_detalle_pred, text=values['Desprecio'], font=(fuente_default, tamanio_fuente))
            Entry2=Entry(iu_detalle_pred, text=values['Asco'], font=(fuente_default, tamanio_fuente))
            Entry3=Entry(iu_detalle_pred, text=values['Miedo'], font=(fuente_default, tamanio_fuente))
            Entry4=Entry(iu_detalle_pred, text=values['Felicidad'], font=(fuente_default, tamanio_fuente))
            Entry5=Entry(iu_detalle_pred, text=values['Neutral'], font=(fuente_default, tamanio_fuente))
            Entry6=Entry(iu_detalle_pred, text=values['Tristeza'], font=(fuente_default, tamanio_fuente))
            Entry7=Entry(iu_detalle_pred, text=values['Sorpresa'], font=(fuente_default, tamanio_fuente))

            Entry0.insert(0,values['Enojo'])
            Entry1.insert(0, values['Desprecio'])
            Entry2.insert(0, values['Asco'])
            Entry3.insert(0, values['Miedo'])
            Entry4.insert(0, values['Felicidad'])
            Entry5.insert(0, values['Neutral'])
            Entry6.insert(0, values['Tristeza'])
            Entry7.insert(0, values['Sorpresa'])

            Entry0.grid(sticky=W, padx=1, pady=5, row=i, column=0, columnspan=1)
            Entry1.grid(sticky=W, padx=1, pady=5, row=i, column=1, columnspan=1)
            Entry2.grid(sticky=W, padx=1, pady=5, row=i, column=2, columnspan=1)
            Entry3.grid(sticky=W, padx=1, pady=5, row=i, column=3, columnspan=1)
            Entry4.grid(sticky=W, padx=1, pady=5, row=i, column=4, columnspan=1)
            Entry5.grid(sticky=W, padx=1, pady=5, row=i, column=5, columnspan=1)
            Entry6.grid(sticky=W, padx=1, pady=5, row=i, column=6, columnspan=1)
            Entry7.grid(sticky=W, padx=1, pady=5, row=i, column=7, columnspan=1)



            #Entry1.insert(0,str(values['Desprecio']))
            #Entry2.insert(0,str(values['Asco']))
            #Entry3.insert(0,str(values['Miedo']))
            #Entry4.insert(0,str(values['Felicidad']))
            #Entry5.insert(0,str(values['Neutral']))
            #Entry6.insert(0,str(values['Tristeza']))
            #Entry7.insert(0,str(values['Sorpresa']))

            i = i+1






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

fuente_default="comic sans"
tamanio_default= 12
ck_redim_img = IntVar(value=1)
opc_selec_rb = IntVar()

window.title("R.L. Reconocimiento de emociones")

rb_single = Radiobutton(window, text="Single", variable=opc_selec_rb, value=1, command=habilitarPanelLateral,font=(fuente_default,tamanio_default))
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
rb_multiple.grid(sticky=W,padx=5,row = 0,column=2)
lbl_ruta_set.grid(sticky=W,padx=5,row=1,column=0,columnspan=2)
tb_ruta_set.grid(sticky=W+E,padx=5,row=2,column=0,columnspan=3)
btn_cargar_ruta.grid(sticky=W+E,padx=5,row=2,column=3)
lbl_mat_param.grid(sticky=W,padx=5,pady=10,row=3,columnspan=3)
combo_mat_param.grid(sticky=NSEW,padx=5,row=4,column=0,columnspan=3)
chkb_redim_img.grid(sticky=NSEW,row=4,column=3)
btn_gen_files.grid(sticky=NSEW,row=5,column=0,padx=5,pady=20,columnspan=4)

window.mainloop()