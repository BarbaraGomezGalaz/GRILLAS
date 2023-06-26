#!/usr/bin/env python
# coding: utf-8

# # IMPORTACIÓN DE LIBRERÍAS

# In[5]:


import numpy as np
import pandas as pd
from io import open
import math
import datetime


# # DEFINICIÓN DE FUNCIONES

# In[6]:


# INDETIFICACIÓN DEL PERFIL EN EL CUAL SE QUIERE TRABAJAR
def filtrador(info,nivel,orientacion,perfil):
    
    info=info[info['Nivel']==nivel]
    info=info[info['Orientación']==orientacion]
    info=info[info['Identificación']==perfil]
    info=pd.DataFrame(info) 
    
    return info

# INPUTS PARA CONFECCIÓN DE GRILLA
def inputs_grillas(centro_este,centro_norte,cota_piso,puntos_H,puntos_V,angulo,distancia):
    
    # DEFINICIÓN ORIENTACIÓN DE GRILLA
    angulo=angulo
    angulo_rad=math.radians(angulo)
    Var_cota=distancia #cada cuanto están separados los puntos en la grilla [m]
    Var_este=math.sin(angulo_rad)*Var_cota
    Var_norte=math.cos(angulo_rad)*Var_cota
    
    z=[]
    
    i=1
    while i<=puntos_V:
        if i==1:
            z_inicial=cota_piso-1
            z.append(z_inicial)
        else:
            z.append(z_inicial+Var_cota*(i-1))
        i=i+1
        
    e=[]
    n=[]
    
    j=1
    while j<=puntos_H:
        if j==1:
            e_inicial=centro_este-Var_este*(puntos_H-1)*0.5
            e.append(e_inicial)
            n_inicial=centro_norte-Var_norte*(puntos_H-1)*0.5
            n.append(n_inicial)
        else:
            e.append(e_inicial+Var_este*(j-1))
            n.append(n_inicial+Var_norte*(j-1))    
        j=j+1
        
    return [e,n,z]

# PUNTOS QUE DEFINEN LA GRILLA
def puntos_grilla(Este_filtrada, Norte_filtrada, Cota_filtrada):
    
    Puntos_Este=[]
    Puntos_Norte=[]
    Puntos_Cota=[]
    Puntos_Coordenada=[]
    
    for i in Cota_filtrada:
        j=0
        while j < len(Este_filtrada):

            Puntos_Este.append(Este_filtrada[j])
            Puntos_Norte.append(Norte_filtrada[j])
            Puntos_Cota.append(i)
            Puntos_Coordenada.append(",("+str(Este_filtrada[j])+","+str(Norte_filtrada[j])+","+str(i)+")")
                            
            j=j+1

    datos=[Puntos_Este,Puntos_Norte,Puntos_Cota,Puntos_Coordenada]
    datos={'Este':Puntos_Este,'Norte':Puntos_Norte,'Cota':Puntos_Cota,'Coordenadas':Puntos_Coordenada}
    df=pd.DataFrame(datos)
    
    return df


# # *** INFORMACIÓN A COMPLETAR ***

# In[17]:


### LECTURA DE ARCHIVOS ###

# INFORMACIÓN BASE PARA CREACIÓN DE GRILLAS

# ARCHIVO EXCEL QUE CONTENGA LAS SIGUIENTES COLUMNAS:
archivo_perfiles=pd.read_excel("BASE GRILLAS.xlsx",sheet_name='SELECCIONADOS')

# 'Nivel' : Texto o número entero que indique el nivel al cual pertenece la grilla a crear 
# 'Orientación' : Texto o número entero que indica la orientación de la galería a la cual corresponderá la grilla
# 'Ángulo' : Número entero que difine el rumbo que debe seguir la grilla desde una vista superior o planta
# 'Identificación' : Número entero que define el ID de la grilla a crear
# 'Este_centro' : Número flotante que indica la coordenada X del punto de referencia a partir del cual se creará la grilla
# 'Norte_centro' : Número flotante que indica la coordenada Y del punto de referencia a partir del cual se creará la grilla
# 'Cota_piso Abaqus' : Número flotante que indica la coordenada Z del punto de referencia a partir del cual se creará la grilla

# ARCHIVO EXCEL RESULTANTE, CONTENDRÁ TODOS LOS PUNTOS ASOCIADOS A LAS GRILLAS CREADAS
grilla_unica= pd.read_excel("PUNTOS_GRILLA_ÚNICA.xlsx",sheet_name='Hoja1')

### CONFECCIÓN DE GRILLAS ###

# INDICAR NIVEL Y ORIENTACIÓN DE LOS PERFILES A LOS CUALES SE LES CREARÁN LAS GRILLAS
NIVEL="NP"
ORIENTACION="CALLES"
base=archivo_perfiles[archivo_perfiles['Nivel']==NIVEL]
base=base[base['Orientación']==ORIENTACION]
base=base['Identificación']

# INDICAR CANTIDAD DE PUNTOS EN LA HORIZONTAL, VERTICAL Y ESPACIAMIENTO DE LA GRILLA
cantidad_puntos_h=96
cantidad_puntos_v=81
espaciamiento=0.15


# # INSTRUCCIONES - CONFECCIÓN DE GRILLAS

# In[18]:


# CREAR GRILLA PARA CADA UNO DE ELLOS
for i in base:
    grilla_unica= pd.read_excel("PUNTOS_GRILLA_ÚNICA.xlsx",sheet_name='Hoja1')
    info_filtrada=filtrador(archivo_perfiles,NIVEL,ORIENTACION,i)
    coordenada_x=list(info_filtrada['Este_centro'])[0]
    coordenada_y=list(info_filtrada['Norte_centro'])[0]
    coordenada_z=list(info_filtrada['Cota_piso Abaqus'])[0]
    info_grilla=inputs_grillas(coordenada_x,coordenada_y,coordenada_z,96,81,list(info_filtrada['Ángulo'])[0],espaciamiento)
    grilla_x=info_grilla[0]
    grilla_y=info_grilla[1]
    grilla_z=info_grilla[2]
    GRILLA=puntos_grilla(grilla_x,grilla_y,grilla_z)
    aux=pd.DataFrame({'Coordenadas':GRILLA['Coordenadas']})
    aux_actual=pd.concat([grilla_unica,aux], ignore_index=True)
    aux_actual.to_excel("PUNTOS_GRILLA_ÚNICA.xlsx",sheet_name='Hoja1',index=False)
    print("PERFIL "+str(i)+" - LISTO - - ",datetime.datetime.now().time())
    
print("CONFECCIÓN DE GRILLAS - - COMPLETADO")

