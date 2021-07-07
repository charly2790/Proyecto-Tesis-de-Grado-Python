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

    #messagebox.showerror('dk_redim', str(ck_redim))

    result = darPrediccion(path_origen,path_img,mat_param,ck_redim)

    messagebox.showerror('Error',result)


window = Tk()
fuente_default="comic sans"
tamanio_default= 12
ck_redim_img = IntVar()

window.title("R.L. Reconocimiento de emociones")

lbl_ruta_set = Label(window,text="Path origen: ",font=(fuente_default,tamanio_default))
tb_ruta_set = Entry(window,font=(fuente_default,tamanio_default),width=40)
btn_cargar_ruta = Button(window,text="...",font=(fuente_default,tamanio_default),command=eventoCargarPath)
combo_mat_param = Combobox(window)
chkb_redim_img = Checkbutton(window, text='Redimensionar',font=(fuente_default,tamanio_default), variable = ck_redim_img)

lbl_mat_param = Label(window,text="Matriz de parámetros: ",font=(fuente_default,tamanio_default))
combo_mat_param['values'] = ("RAFD_414","RAFD_1608","RAFD_1608_S_NORM","RAFD_1608_S_NORM_1200")
combo_mat_param.current(1)

btn_gen_files = Button(window, text = 'Predecir', font = (fuente_default,tamanio_default), command=eventoPrepararPrediccion)

v_col_span = 10

lbl_ruta_set.grid(sticky=W,columnspan=3,padx=10,pady=5)
tb_ruta_set.grid(row=1,columnspan=v_col_span,padx=10,sticky="ew")
btn_cargar_ruta.grid(row=1,column=v_col_span + 1,columnspan=1,padx=2)
lbl_mat_param.grid(sticky=W,columnspan=3,padx=10,pady=5)
combo_mat_param.grid(sticky=W,columnspan=3,padx=10,pady=5)
chkb_redim_img.grid(sticky=W,row=5,padx=10)

btn_gen_files.grid(row=6,padx=10,pady=10,columnspan=v_col_span+2,sticky="ew")

window.mainloop()