import numpy as np
import pandas as pd
import cv2
import dlib
import json
from os import scandir
import os


def traducir(pos):

    result = ""

    etiquetas = ["1 - Enojo","2 - Desprecio","3 - Asco","4 - Miedo","5 - Felicidad","6 - Neutral","7 - Tristeza","8 - Sorpresa"]

    result = etiquetas[pos]

    return result



def detectarCara(img,flag_gray,detector):

    #1) flag_gray = 1 indica que la imagen se encuentra en escala de grises
    #2) flag_gray = 0 indica lo contrario

    rostro = None
    gray = None

    if flag_gray != 1:
        # 1) Convierto la imagen a escala de grises
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        gray = img


    # 2) Detecto el rostro/s
    rostros = detector(gray)

    if len(rostros) > 0:
        rostro = rostros[0]

    #print(darLado(rostro))

    return rostro

def iniFaceDetector():

    detector = dlib.get_frontal_face_detector()

    return detector

def iniShapePredictor():

    sh_pred = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

    return sh_pred

def darLado(face):

    lado = 0
    x1 = face.left()
    x2 = face.right()

    # calculo ancho
    lado = x2 - x1

    return lado

def redimImg(img, ancho, dimRef):

    # calculo la proporción del cuadrado del rostro
    porc = (dimRef / ancho)

    n_ancho = int(img.shape[0] * porc)
    n_alto = int(img.shape[1] * porc)

    # nuevo tamaño de la imágen
    n_dim = (n_alto, n_ancho)

    # redimensiono la imágen
    n_img = cv2.resize(img, n_dim, interpolation=cv2.INTER_AREA)

    #convierto la imagen a escala de grises
    #n_img = cv2.cvtColor(n_img, cv2.COLOR_BGR2GRAY)

    return n_img

def hipotesisRL(mat_x,mat_param,mu,sigma):

    m = mat_x.shape[0]

    if mu is not None and sigma is not None:
        #normalizo la matriz de características
        mat_x_norm = (mat_x - mu) / sigma

    mat_param_transp = np.transpose(mat_param)

    #num_labels se corresponde con la cantidad de emociones
    num_labels = mat_param.shape[0]

    p = np.zeros((m,1),float)

    #en 'h' se guardará la salida de los clasificadores
    h = np.zeros((num_labels,m), dtype=np.float64)
    z = np.zeros((num_labels, m), dtype=np.float64)

    #se agrega una columna de 1s al comienzo de la matriz de características (mat_x)
    mat_x_norm = np.concatenate((np.ones((m,1)),mat_x),axis=1)

    #print("Shape mat_x: "+ str(mat_x.shape))
    #calculo del polinomio 'z'
    z = np.dot(mat_x_norm,mat_param_transp)

    #aplico la función sigmoide
    h = 1/(1+np.exp(-z))

    h = np.transpose(h)

    return h

def darPrediccion(path_origen, path_imagen, mat_param, ck_redim):
    shape_predictor = iniShapePredictor()
    face_detector = iniFaceDetector()
    Theta = None
    mu = None
    sigma = None
    file_theta = ""
    file_mu = ""
    file_sigma = ""
    df_Theta = None
    df_mu = None
    df_sigma = None
    img_leidas = []
    ind_unica_img = 0

    #Para predicciones individuales
    if path_imagen != None:
        ind_unica_img = 1

    # carga de matriz de parametros Theta y vectores p/normalización
    if mat_param == "RAFD_1608":

        file_theta = 'mat_param_1608.csv'
        file_mu = 'mu_1608.csv'
        file_sigma = 'sigma_1608.csv'

    elif mat_param == "RAFD_404":

        file_theta = 'mat_param_404.csv'
        file_mu = 'mu_404.csv'
        file_sigma = 'sigma_404.csv'

    elif mat_param == "RAFD_1608_S_NORM":

        file_theta = 'mat_parametros_1608_s_norm.csv'

    elif mat_param == "RAFD_1608_S_NORM_1200":

        file_theta = 'mat_parametros_1608_s_norm_1200.csv'


    try:
        df_Theta = pd.read_csv(file_theta, delimiter=';', header=None, dtype=np.float64, decimal=',',float_precision='high')
    except:
        dt_Theta = None

    if df_Theta is not None:
        Theta = np.asarray(df_Theta)

    try:
        df_mu = pd.read_csv(file_mu, delimiter=';', header=None, dtype=np.float64, decimal=',', float_precision='high')
    except:
        df_mu = None

    if df_mu is not None:
        mu = np.asarray(df_mu)

    try:
        df_sigma = pd.read_csv(file_sigma, delimiter=';', header=None, dtype=np.float64, decimal=',',float_precision='high')
    except:
        df_sigma = None

    if df_sigma is not None:
        sigma = np.asarray(df_mu)

    if Theta is None:
        return "ERROR_LOADING_FILES"

    result = ""
    img = None
    v_rostro = None
    v_lado = 0
    v_dim_ref = 371
    v_lim_inf = v_dim_ref - 5
    v_lim_sup = v_dim_ref + 5

    if ind_unica_img == 0:
        imagenes = [obj.name for obj in scandir(path_origen) if
                    obj.is_file() and (obj.name.endswith('.jpg') or obj.name.endswith('.png'))]
    else:
        imagenes = [path_imagen]

    cant_img = len(imagenes)

    if cant_img > 0:

        v_fila = 0

        for imagen in imagenes:

            if ind_unica_img == 0:
                # 1) Lectura de la imagen
                path_imagen = str(path_origen / imagen)


            img = cv2.imread(path_imagen)

            v_rostro = detectarCara(img, 0, face_detector)

            if v_rostro != None:

                v_lado = darLado(v_rostro)

                # Evaluo el check de redimensión de imágen
                if ck_redim == True:

                    if v_lado < v_lim_inf or v_lado > v_lim_sup:
                        # redimensiono la imágen
                        n_img = redimImg(img, v_lado, v_dim_ref)

                        v_rostro = detectarCara(n_img, 0, face_detector)

                        ancho = darLado(v_rostro)

                        print("nuevo ancho: " + str(ancho))

                        img = n_img

                img_esc_grises = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

                # localización de landmarks faciales
                landmarks = shape_predictor(img_esc_grises,v_rostro)

                linea = ""

                vec_landmarks = np.zeros((1, 136))

                j = 0
                for i in range(0, 68):
                    x = landmarks.part(i).x
                    y = landmarks.part(i).y

                    vec_landmarks[0, j] = int(x)
                    j = j + 1
                    vec_landmarks[0, j] = int(y)
                    j = j + 1

                if v_fila == 0:
                    mat_landmarks = vec_landmarks
                    v_fila = 1
                else:
                    mat_landmarks = np.concatenate((mat_landmarks,vec_landmarks))

                img_leidas.append(imagen)

        try:
            h_result = hipotesisRL(mat_landmarks, Theta,mu,sigma)
        except:
            h_result = None

        if h_result is not None:
            #result = json.dumps(h_result.tolist())

            # for img_leida in img_leidas:
            #    print(img_leida)

            # f = e[-1:,]

            # cantidad de predicciones realizadas
            cant_cols = h_result.shape[1]
            # Diccionario para predicciones individuales
            dic_col = {}
            # Diccionario para prediccion total
            dic_res = {}
            num_max = 0
            pos_num_max = 0

            for i in range(0, cant_cols):
                col_1 = h_result[:, i]

                #Calculo el máximo
                num_max = np.max(col_1)

                pos_num_max = int(np.where(col_1 == num_max)[0])

                dic_col = {'Enojo': col_1[0], 'Desprecio': col_1[1], 'Asco': col_1[2], 'Miedo': col_1[3],
                           'Felicidad': col_1[4], 'Neutral': col_1[5], 'Tristeza': col_1[6], 'Sorpresa': col_1[7], 'Maximo': pos_num_max}

                dic_res.setdefault(img_leidas[i], dic_col)

            result = json.dumps(dic_res)


        #print(h_result)

        #pos_max = np.where(h_result == max(h_result))

        #num_max = np.max(h_result)

        #pos_num_max = np.where(h_result == num_max)[0] + 1

        #print("num max: " + str(num_max) + " -pos: " + str(pos_num_max))

        #result = "Dim nueva imágen: " + str(darLado(v_rostro))
    else:
        result = "ERROR_NO_IMG_FOUND"

    return result