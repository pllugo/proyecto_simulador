#!/usr/bin/env python
'''
Archivos [Python]
Ejercicios de profundización
---------------------------
Autor: Pedro Luis Lugo Garcia
Version: 1.2

Descripcion:
Proyecto: Simulador Ambiental-Química Atmosférica
'''

__author__ = "Pedro Luis Lugo Garcia"
__email__ = "pllugo@gmail.com"
__version__ = "1.0"

import csv

import numpy as np

import math

import matplotlib.pyplot as plt

#Librerias importadas para poder realizar cálculos
#y graficas del programa

def tiempo_total(tiempo_segundos, tecnica_medicion, tiempo_fotolisis):#función que toma la lista en segundos
    primeros_tiempos = []                                              #y la divide en dos restando según metodologia
    tiempos_restantes = []
    for i in range(len(tiempo_segundos)):
        if tecnica_medicion == "FTIR":
            if i <= tiempo_fotolisis -1:
                primeros_tiempos.append(tiempo_segundos[i] - tiempo_segundos[0])
            else:
                tiempos_restantes.append(tiempo_segundos[i] - tiempo_segundos[tiempo_fotolisis])
        else:
            if tecnica_medicion == "GC-FID":#Aqui no se restan los tiempos debido
                if i <= tiempo_fotolisis -1:#a que se obtienen directamente por el usuario
                    primeros_tiempos.append(float(tiempo_segundos[i]))
                else:
                    tiempos_restantes.append(float(tiempo_segundos[i]))
            else:
                print("Error no introdujo la tecnica de medición")  
    return primeros_tiempos, tiempos_restantes
            

def lista_segundos(lista_tiempo):#Función para pasar una lista de h a segundos
    dato_tiempo =[]
    for j in range(len(lista_tiempo)):
        tiempo = lista_tiempo[j]
        hora = int(tiempo[:2])     
        minutos = int(tiempo[3:5])
        segundos = int(tiempo[6:8])
        tiempo_total = hora*3600 + minutos*60 + segundos
        dato_tiempo.append(tiempo_total)
    return dato_tiempo


def variable_tiempo(elemento):#funcion para pasar una variable de horas a segundos
    hora = int(elemento[:2])     
    minutos = int(elemento[3:5])
    segundos = int(elemento[6:8])
    tiempo_exacto = hora*3600 + minutos*60 + segundos
    return tiempo_exacto


def informacion_diccionario(datos, primer_dato, segundo_dato):#Función para generar listas del diccionario
    with open(datos) as csvfile: #Leo el archivo tipo diccionario
        datos_diccionario = list(csv.DictReader(csvfile))
    columna_y = primer_dato
    columna_x = segundo_dato
    cantidad_filas = len(datos_diccionario)
    lista_y =[]
    lista_x = []
    for i in range(cantidad_filas):
        if datos_diccionario[i][columna_y] != 0:
            lista_y.append(datos_diccionario[i][columna_y])       
            lista_x.append(datos_diccionario[i][columna_x])
        else:
            print("El diccionario esta vacio")
            break
    csvfile.close()
    return lista_y, lista_x


def lista_grafica(lista_compuesto, lista_referencia, condicion):#función para separar la lista del compuesto
    primera_lista = []                                          #en una primera lista del COV y la de la referencia
    segunda_lista = []
    for i in range(condicion, len(lista_compuesto)):
        primera_lista.append(float(lista_compuesto[i]))
        segunda_lista.append(float(lista_referencia[i]))
    return primera_lista, segunda_lista


def tabla_cinetica(archivo, valor_kwall, generar_archivo, medicion, numero_fotolisis):#Función para generar el archivo para gráficar
    with open(archivo) as csvfile: #Leo el archivo tipo diccionario
        datos_diccionario = list(csv.DictReader(csvfile))
    if medicion == "FTIR":
        columna_fc = "factor compuesto"
        columna_fr = "factor referencia"
        columna_tiempo = "tiempo (h)"
        cinetica = {}
        csvfile = open(generar_archivo, 'w', newline='')
        if valor_kwall != 0:
            header = ["tiempo (h)", "tiempo (s)", "factor compuesto", "factor referencia", "Ln(Co/Ct)", "Ln(Refo/Reft)", "kwall-loss"]
        else:
            header = ["tiempo (h)", "tiempo (s)", "factor compuesto", "factor referencia", "Ln(Co/Ct)", "Ln(Refo/Reft)"]
        writer = csv.DictWriter(csvfile, fieldnames=header)
        writer.writeheader()
        datos = len(datos_diccionario)
        for i in range(datos):
            if i >= numero_fotolisis:    
                compuesto_cero = float(datos_diccionario[numero_fotolisis][columna_fc]) #Aqui son los calculos para el compuesto
                compuesto_tiempo = float(datos_diccionario[i][columna_fc])
                logaritmo_compuesto = math.log(compuesto_cero / compuesto_tiempo)
                tiempo_hora = variable_tiempo(datos_diccionario[i][columna_tiempo])
                tiempo_total = tiempo_hora - variable_tiempo(datos_diccionario[numero_fotolisis][columna_tiempo])
                compuesto_kwall = logaritmo_compuesto - valor_kwall * tiempo_total
                referencia_cero = float(datos_diccionario[numero_fotolisis][columna_fr]) #Aqui son los calculos para la referencia
                referencia_tiempo = float(datos_diccionario[i][columna_fr])
                logaritmo_referencia = math.log(referencia_cero / referencia_tiempo)
                if valor_kwall != 0:
                    cinetica = {"tiempo (h)": datos_diccionario[i][columna_tiempo], "tiempo (s)": tiempo_total, "factor compuesto": datos_diccionario[i][columna_fc], "factor referencia": datos_diccionario[i][columna_fr], "Ln(Co/Ct)": round(logaritmo_compuesto, 4), "Ln(Refo/Reft)": round(logaritmo_referencia, 4), "kwall-loss": compuesto_kwall}
                    writer.writerow(cinetica)
                else:
                    cinetica = {"tiempo (h)": datos_diccionario[i][columna_tiempo], "tiempo (s)": tiempo_total, "factor compuesto": datos_diccionario[i][columna_fc], "factor referencia": datos_diccionario[i][columna_fr], "Ln(Co/Ct)": round(logaritmo_compuesto, 3), "Ln(Refo/Reft)": round(logaritmo_referencia, 3)}
                    writer.writerow(cinetica)
            else:
                compuesto_cero = float(datos_diccionario[0][columna_fc]) #Aqui son los calculos para el compuesto
                compuesto_tiempo = float(datos_diccionario[i][columna_fc])
                logaritmo_compuesto = math.log(compuesto_cero / compuesto_tiempo)
                tiempo_hora = variable_tiempo(datos_diccionario[i][columna_tiempo])
                tiempo_total = tiempo_hora - variable_tiempo(datos_diccionario[0][columna_tiempo])
                compuesto_kwall = logaritmo_compuesto - valor_kwall * tiempo_total
                referencia_cero = float(datos_diccionario[0][columna_fr]) #Aqui son los calculos para la referencia
                referencia_tiempo = float(datos_diccionario[i][columna_fr])
                logaritmo_referencia = math.log(referencia_cero / referencia_tiempo)
                if valor_kwall != 0:
                    cinetica = {"tiempo (h)": datos_diccionario[i][columna_tiempo], "tiempo (s)": tiempo_total, "factor compuesto": datos_diccionario[i][columna_fc], "factor referencia": datos_diccionario[i][columna_fr], "Ln(Co/Ct)": round(logaritmo_compuesto, 4), "Ln(Refo/Reft)": round(logaritmo_referencia, 4), "kwall-loss": compuesto_kwall}
                    writer.writerow(cinetica)
                else:
                    cinetica = {"tiempo (h)": datos_diccionario[i][columna_tiempo], "tiempo (s)": tiempo_total, "factor compuesto": datos_diccionario[i][columna_fc], "factor referencia": datos_diccionario[i][columna_fr], "Ln(Co/Ct)": round(logaritmo_compuesto, 3), "Ln(Refo/Reft)": round(logaritmo_referencia, 3)}
                    writer.writerow(cinetica)
    else:
        if medicion == "GC-FID":#En ésta parte el archivo cambia
            columna_fc = "area R" #porque cambia la técnica de medición
            columna_fr = "area C"
            columna_tiempo = "tiempo (s)"
            cinetica = {}
            csvfile = open(generar_archivo, 'w', newline='')
            if valor_kwall != 0:
                header = ["tiempo (s)", "area R", "area C", "Ln(Co/Ct)", "Ln(Refo/Reft)", "kwall-loss"]
            else:
                header = ["tiempo (s)", "area R", "area C", "Ln(Co/Ct)", "Ln(Refo/Reft)"]
            writer = csv.DictWriter(csvfile, fieldnames=header)
            writer.writeheader()
            datos = len(datos_diccionario)
            for i in range(datos):
                if i >= numero_fotolisis:    #El número 3 porque en ésta técnica siempre son 3 ptos de fotólisis
                    compuesto_cero = float(datos_diccionario[numero_fotolisis][columna_fc]) #Aqui son los calculos para el compuesto
                    compuesto_tiempo = float(datos_diccionario[i][columna_fc])
                    logaritmo_compuesto = math.log(compuesto_cero / compuesto_tiempo)
                    #tiempo_hora = variable_tiempo(datos_diccionario[i][columna_tiempo])
                    #tiempo_total = tiempo_hora - variable_tiempo(datos_diccionario[3][columna_tiempo])
                    compuesto_kwall = logaritmo_compuesto - valor_kwall * float(datos_diccionario[i][columna_tiempo])
                    referencia_cero = float(datos_diccionario[numero_fotolisis][columna_fr]) #Aqui son los calculos para la referencia
                    referencia_tiempo = float(datos_diccionario[i][columna_fr])
                    logaritmo_referencia = math.log(referencia_cero / referencia_tiempo)
                    if valor_kwall != 0:
                        cinetica = {"tiempo (s)": datos_diccionario[i][columna_tiempo], "area C": datos_diccionario[i][columna_fc], "area R": datos_diccionario[i][columna_fr], "Ln(Co/Ct)": round(logaritmo_compuesto, 4), "Ln(Refo/Reft)": round(logaritmo_referencia, 4), "kwall-loss": compuesto_kwall}
                        writer.writerow(cinetica)
                    else:
                        cinetica = {"tiempo (s)": datos_diccionario[i][columna_tiempo], "area C": datos_diccionario[i][columna_fc], "area R": datos_diccionario[i][columna_fr], "Ln(Co/Ct)": round(logaritmo_compuesto, 3), "Ln(Refo/Reft)": round(logaritmo_referencia, 3)}
                        writer.writerow(cinetica)
                else:
                    compuesto_cero = float(datos_diccionario[0][columna_fc]) #Aqui son los calculos para el compuesto
                    compuesto_tiempo = float(datos_diccionario[i][columna_fc])
                    logaritmo_compuesto = math.log(compuesto_cero / compuesto_tiempo)
                    #tiempo_hora = variable_tiempo(datos_diccionario[i][columna_tiempo])
                    #tiempo_total = tiempo_hora - variable_tiempo(datos_diccionario[0][columna_tiempo])
                    compuesto_kwall = logaritmo_compuesto - valor_kwall * float(datos_diccionario[i][columna_tiempo])
                    referencia_cero = float(datos_diccionario[0][columna_fr]) #Aqui son los calculos para la referencia
                    referencia_tiempo = float(datos_diccionario[i][columna_fr])
                    logaritmo_referencia = math.log(referencia_cero / referencia_tiempo)
                    if valor_kwall != 0:
                        cinetica = {"tiempo (s)": datos_diccionario[i][columna_tiempo], "area C": datos_diccionario[i][columna_fc], "area R": datos_diccionario[i][columna_fr], "Ln(Co/Ct)": round(logaritmo_compuesto, 4), "Ln(Refo/Reft)": round(logaritmo_referencia, 4), "kwall-loss": compuesto_kwall}
                        writer.writerow(cinetica)
                    else:
                        cinetica = {"tiempo (s)": datos_diccionario[i][columna_tiempo], "area C": datos_diccionario[i][columna_fc], "area R": datos_diccionario[i][columna_fr], "Ln(Co/Ct)": round(logaritmo_compuesto, 3), "Ln(Refo/Reft)": round(logaritmo_referencia, 3)}
                        writer.writerow(cinetica)
        else:
            print("Error, coloco una técnica de medición la cual no esta contemplada")
    csvfile.close()


def genera(lista, dato_fotolisis):#Función para generar dos listas
    primeros_datos = []            #Una lista con los primeros datos de linea base
    datos_secundarios = []         #Otra lista con el resto de datos para las gráficas
    if lista:
        for i in range(len(lista)):
            if i >= dato_fotolisis:
                primer_numero = float((lista[dato_fotolisis]))
                segundo_numero = float((lista[i]))
                resultado = math.log(primer_numero / segundo_numero)
                datos_secundarios.append(resultado)
            else:
                primer_numero = float((lista[0]))
                segundo_numero = float((lista[i]))
                resultado = math.log(primer_numero / segundo_numero)
                primeros_datos.append(resultado)
    else:
        print("Lista vacia")
    return primeros_datos, datos_secundarios


def calculo_cinetica(lista_abscisa, lista_coordenada): #Función para calcular la constante cinética del COV
    abscisa_x = np.array(lista_coordenada)
    ordenada_y =np.array(lista_abscisa)
    suma_x = sum(lista_coordenada)
    suma_y = sum(lista_abscisa)
    suma_x2 = sum(abscisa_x*abscisa_x)
    suma_y2 = sum(ordenada_y*ordenada_y)
    sum_xy = sum(abscisa_x * ordenada_y)
    prom_x = suma_x / len(lista_abscisa)
    prom_y = suma_y / len(lista_abscisa)
    pendiente = (suma_x * suma_y - len(lista_abscisa)*sum_xy) / (suma_x**2 - len(lista_abscisa)*suma_x2)
    intercepto = prom_y - pendiente * prom_x
    sigmax = np.sqrt(suma_x2 / len(abscisa_x) - prom_x**2)
    sigmay = np.sqrt(suma_y2 / len(abscisa_x) - prom_y**2)
    sigmaxy = sum_xy / len(abscisa_x) - prom_x * prom_y
    r2 = round((sigmaxy / (sigmax * sigmay))**2, 4)
    print("R2 =", r2)
    plt.plot(abscisa_x, ordenada_y, "o", label="Datos")
    plt.plot(abscisa_x, pendiente*abscisa_x + intercepto, label="Ajuste")
    plt.xlabel("Ln(Refo/Reft)")
    plt.ylabel("Ln(Co/Ct)")
    plt.title("kComp/kRef = {0:.3E} (cm3.molécula-1.s-1)".format(pendiente))
    plt.grid()
    plt.legend(loc=4)
    plt.show()
    return pendiente


def calculo_kwall(lista_abscisa, lista_coordenada): #Función para calcular k_wall_loss
    abscisa_kwall = np.array(lista_abscisa)
    ordenada_kwall =np.array(lista_coordenada)
    suma_abscisa = sum(lista_abscisa)
    suma_ordenadas = sum(lista_coordenada)
    suma_x2 = sum(abscisa_kwall*abscisa_kwall)
    suma_y2 = sum(ordenada_kwall*ordenada_kwall)
    sum_xy = sum(abscisa_kwall * ordenada_kwall)
    prom_x = suma_abscisa / len(lista_abscisa)
    prom_y = suma_ordenadas / len(lista_abscisa)
    pendiente = (suma_abscisa * suma_ordenadas - len(lista_abscisa)*sum_xy) / (suma_abscisa**2 - len(lista_abscisa)*suma_x2)
    intercepto = prom_y - pendiente * prom_x
    sigmax = np.sqrt(suma_x2 / len(abscisa_kwall) - prom_x**2)
    sigmay = np.sqrt(suma_y2 / len(abscisa_kwall) - prom_y**2)
    sigmaxy = sum_xy / len(abscisa_kwall) - prom_x * prom_y
    r2 = round((sigmaxy / (sigmax * sigmay))**2, 4)
    print("R2 =", r2)
    plt.plot(abscisa_kwall, ordenada_kwall, "o" , label="Datos")
    plt.plot(abscisa_kwall, pendiente*abscisa_kwall + intercepto, label="Ajuste")
    if intercepto > 0:
        plt.text(200, 0.02, "y = {}x + {}".format(pendiente, intercepto))
    else:
        plt.text(200, 0.02, "y = {}x {}".format(pendiente, intercepto))
    plt.text(250, 0.015, "R2 = {}".format(r2))
    plt.xlabel("tiempo (s)")
    plt.ylabel("Ln(Co/Ct)")
    plt.title("k Wall Loss (kwall_loss = {0:.3E} s-1)".format(pendiente))
    plt.grid()
    plt.legend(loc=4)
    plt.show()
    return pendiente


def diccionario_compuestos(nombre, dato_radical): #lista de datos estandarizada para buscar propiedades
    archivo_nombres = "base_datos.csv"
    with open(archivo_nombres) as csvfile: #Leo el archivo tipo diccionario
        datos_diccionario = list(csv.DictReader(csvfile))
    columna_español = "NOMBRE"
    columna_ingles = "NAME"
    columna_radical = dato_radical
    columna_densidad = "DENSIDAD g/mL"
    columna_peso = "PESO MOLECULAR g/mol"
    cantidad_filas = len(datos_diccionario)
    for i in range(cantidad_filas):
        if datos_diccionario[i][columna_español] == nombre:
            constante = float(datos_diccionario[i][columna_radical])
            resultado_peso = float(datos_diccionario[i][columna_peso])
            resultado_densidad = float(datos_diccionario[i][columna_densidad])
            print("La constante cinética de {} es {} con radicales {}".format(nombre, constante, dato_radical))
            break
        else:
            if datos_diccionario[i][columna_ingles] == nombre:
                constante = float(datos_diccionario[i][columna_radical])
                resultado_peso = float(datos_diccionario[i][columna_peso])
                resultado_densidad = float(datos_diccionario[i][columna_densidad])
                print("La constante cinética de {} es {} con radicales {}".format(nombre, constante, dato_radical))
                break
            else:
                continue
    csvfile.close()
    return constante, resultado_peso, resultado_densidad


def indice_acidificacion(valor):#Función para calcular el AP
    archivo_potenciales = "datos_acidificacion.csv"
    with open(archivo_potenciales) as csvfile: #Leo el archivo tipo diccionario
        diccionario_potenciales = list(csv.DictReader(csvfile))
    columna_compuesto = "compuestos"
    columna_ap = "Acidification Potencial"
    lista_potenciales = []
    lista_compuestos = []
    cantidad_datos = len(diccionario_potenciales)
    for i in range(cantidad_datos):
        lista_compuestos.append(diccionario_potenciales[i][columna_compuesto])
        lista_potenciales.append(float(diccionario_potenciales[i][columna_ap]))
    potencial = min(lista_potenciales, key=lambda x:abs(x-valor))
    for j in range(len(lista_compuestos)):
        if potencial == lista_potenciales[j]:
            print("El potencial de acidificación del compuesto {} es parecido al {} cuyo valor es {}".format(valor, lista_compuestos[j], potencial))
    csvfile.close()


def tiempo_residencia(constante_cinetica, tipo_radical):#Función para calcular el tiempo de residencia
    if tipo_radical == "OH":                           #atmosferico de un COV
        tiempo = 1 / (constante_cinetica * 2E6)
    else:
        if tipo_radical == "Cl":
            tiempo = 1 / (constante_cinetica * 1E4)
        else:
            if tipo_radical == "NO3":
                tiempo = 1 / (constante_cinetica * 5E8)
            else:
                print("O3")
                tiempo = 1 / (constante_cinetica * 7E11)
    return tiempo


def funcion_ozono(parametro, tipo_compuesto, region):#funcion para buscar en el archivo
    archivo_ozono = "datos_POCP.csv"                 #de datos de POCP
    with open(archivo_ozono) as csvfile: #Leo el archivo tipo diccionario
        diccionario_ozono = list(csv.DictReader(csvfile))
    columna_parametro = "Parametro"
    columna_cov = "COV"
    columna_europa = "Condiciones del noroeste de Europa"
    columna_usa = "Condiciones urbanas de USA"
    for i in range(len(diccionario_ozono)):
        if region == 1:#europa
            if diccionario_ozono[i][columna_parametro] == parametro:
                if diccionario_ozono[i][columna_cov] == tipo_compuesto:
                    valor_retorno = float(diccionario_ozono[i][columna_europa])
        else:#USA
            if diccionario_ozono[i][columna_parametro] == parametro:
                if diccionario_ozono[i][columna_cov] == tipo_compuesto:
                    valor_retorno = float(diccionario_ozono[i][columna_usa])
    csvfile.close()
    return valor_retorno


def potencial_ozono(peso_molecular, numero_enlaces, numero_carbonos, koh_compuesto):#Función para calcular POCP
    condiones_region = int(input("""Ingrese la region que desea usar para realizar los calculos
                                    1 Condiciones del noroeste de Europa
                                    2 Condiciones urbanas de USA\n"""))
    compuesto_organico = int(input("""Ingrese que tipo de compuesto organico desea estudiar:
                                1 Alifático
                                2 Aromático\n"""))
    if compuesto_organico == 1:
        valor_a = funcion_ozono("A", "alifaticos", condiones_region)
        valor_d = funcion_ozono("D", "alifaticos", condiones_region)
        valor_epsilon = funcion_ozono("epsilon", "alifaticos", condiones_region)
        informacion_producto = int(input("""Conoce ud la kOH del producto mayoritario que se genera?
                                    1 Si
                                    2 No\n"""))
        if informacion_producto == 1:
            koh_producto = float(input("Ingrese la kOH del producto mayoritario segun rendimiento molar:\n"))
            if koh_producto < 2E-12:
                valor_fi = float(input("Ingrese el rendimiento molar del producto:\n"))
                valor_delta = valor_d * (1 - (1E12 * koh_producto / 2)) * 1E12 * koh_producto ** valor_epsilon
                valor_f = ((numero_enlaces - ( valor_fi * numero_enlaces))/ numero_enlaces) ** valor_delta
            else:
                valor_f = 1
        else:
            valor_f = 1
    else:
        sustituyentes_aromaticos = int(input("Ingrese la cantidad de sustituyentes alquilos (0 a 3), si es mayor, colocar 3:\n"))
        if sustituyentes_aromaticos == 0:
            valor_a = funcion_ozono("A","aromaticos con 0 sustituyentes alquilos", condiones_region)
        else:
            if sustituyentes_aromaticos == 1:
                valor_a = funcion_ozono("A","aromaticos con 1 sustituyentes alquilos", condiones_region)
            else:
                if sustituyentes_aromaticos == 2:
                    valor_a = funcion_ozono("A","aromaticos con 2 sustituyentes alquilos", condiones_region)
                else:
                    valor_a = funcion_ozono("A","aromaticos con 3 sustituyentes alquilos", condiones_region)
    condicion_p = int(input("""Ingrese que grupo funcional posee el compuesto:
                            1 aldehido o cétona
                            2 alfa-dicarbonilos
                            3 ciclocetonas
                            4 ninguna de las anteriores\n"""))
    if condicion_p == 1:
        valor_p = funcion_ozono("P","aldehidos y cetonas", condiones_region)
    else:
        if condicion_p == 2:
            valor_p = funcion_ozono("P","alfa-dicarbonilos", condiones_region)
        else:
            if condicion_p == 3:
                valor_p = funcion_ozono("P","ciclocetonas", condiones_region)
            else:
                valor_p = 0
    condicion_ro3 = int(input("""Ingrese si su compuesto es:
                            1 Alqueno ó Oxigenado insaturado
                            2 Ninguna de las anteriores\n"""))
    if condicion_ro3 == 1:
        valor_e = funcion_ozono("E","alquenos y oxigenados insaturados", condiones_region)
        valor_lambda = funcion_ozono("lambda","alquenos y oxigenados insaturados", condiones_region)
        constante_ozono = float(input("Ingrese la constante con radical ozono del compuesto (cm3.molécula-1.s-1):\n"))
        valor_mu = ((constante_ozono / 1.55E-18) * (koh_compuesto / 7.80E-12)) ** valor_lambda
        valor_ro3 = valor_e ** valor_mu
    else:
        valor_ro3 = 0
    condicion_q = int(input("""Ingrese si su compuesto es:
                            1 Benzaldehido ó Estirenos
                            2 Hidroxiarenos
                            3 Ninguna de las anteriores\n"""))
    if condicion_q == 1:
        valor_q = funcion_ozono("Q","benzaldehidos y estirenos", condiones_region)
    else:
        if condicion_q == 2:
            valor_q = funcion_ozono("Q","hidroxiarenos", condiones_region)
        else:
            valor_q = 0
    #Luego de tener todos los valores según usuario
    #Se calcula el valor de POCP (valor_pocp)
    valor_b = funcion_ozono("B", "todos", condiones_region)
    valor_alfa = funcion_ozono("alfa", "todos", condiones_region)
    valor_c = funcion_ozono("C", "todos", condiones_region)
    valor_beta = funcion_ozono("beta", "todos", condiones_region)
    valor_gamma = (numero_enlaces / 6) * (28.05 / peso_molecular)
    gamma_r = (koh_compuesto / 7.80E-12) * (6 / numero_enlaces)
    valor_r = 1 - (1 / (valor_b * gamma_r + 1))
    valor_s = (1 - valor_alfa) * math.e ** (-valor_c * numero_carbonos ** valor_beta) + valor_alfa
    valor_pocp = round((valor_a * valor_gamma * valor_r * valor_s * valor_f) + valor_p + valor_ro3 - valor_q, 2)
    return valor_pocp


def informacion_compuestos(dato_nombre):#función para encontrar las propiedades del compuesto
    archivo_compuestos = "datos_covs.csv"
    with open(archivo_compuestos) as csvfile: #Leo el archivo tipo diccionario
        datos_diccionario = list(csv.DictReader(csvfile))
        columna_nombres = "Nombre"
        columna_densidad = "Densidad (g/mL)"
        columna_molecular = "Peso Molecular (g/mol)"
        for i in range(len(datos_diccionario)):
            if datos_diccionario[i][columna_nombres] == dato_nombre:
                dato_densidad = float(datos_diccionario[i][columna_densidad])
                dato_molecular = float(datos_diccionario[i][columna_molecular])
                break
            else:
                continue
    csvfile.close()
    return dato_densidad, dato_molecular


def concentracion(cantidad, dato_peso, dato_densidad):#función para conocer la cantidad de compuesto a inyectar
    factor_conversion = 1000                           # en el reactor
    factor_concentracion = 2.46E13
    numero_avogadro = 6.02E23
    tipo_reactor = int(input("""Ingrese el Volumen del reactor:
                                1 Reactor 405 L UNC
                                2 Reactor 480 L Universidad de Wuppertal
                                3 Reactor 1080 L Universidad de Wuppertal\n"""))
    if tipo_reactor == 1:#UNC
        volumen_reactor = 405000
        resultado_concentracion = (((dato_densidad * cantidad * numero_avogadro)/(factor_conversion * dato_peso * volumen_reactor))/ factor_concentracion)
    else:
        if tipo_reactor == 2:#UW
            volumen_reactor = 480000
            resultado_concentracion = (((dato_densidad * cantidad * numero_avogadro)/(factor_conversion * dato_peso * volumen_reactor))/ factor_concentracion)
        else:
            if tipo_reactor == 3:#UW
                volumen_reactor = 1080000
                resultado_concentracion = (((dato_densidad * cantidad * numero_avogadro)/(factor_conversion * dato_peso * volumen_reactor))/ factor_concentracion)
            else:
                print("Disculpe, solo los reactores antes mencionados, son los usados")
                resultado_concentracion = 0
    return resultado_concentracion
        
    
def cinetica_quimica(dato_archivo, radical):#Función para calcular la constante cinética de un COV
    nombre_compuesto = str(input("Ingrese el nombre del compuesto:\n"))#El compuesto también llamado COV
    cantidad_compuesto = float(input("Ingrese la cantidad de compuesto inyectado (uL):\n"))
    densidad_comp, peso_comp = informacion_compuestos(nombre_compuesto)#Aqui busco la información sobre el COV
    concentracion_cov = concentracion(cantidad_compuesto, peso_comp, densidad_comp)
    print("La concentración en del {} en [ppm] = {}".format(nombre_compuesto, concentracion_cov))
    nombre_referencia = str(input("Ingrese el nombre de la referencia:\n"))
    cantidad_referencia = float(input("Ingrese la cantidad de referencia inyectada (uL):\n"))
    constante_referencia, peso_ref, densidad_ref = diccionario_compuestos(nombre_referencia, radical)#Aqui busco la constante de referencia ingresada
    concentracion_referencia = concentracion(cantidad_referencia, peso_ref, densidad_ref)
    print("La concentración en del {} en [ppm] = {}".format(nombre_referencia, concentracion_referencia))
    metodo = int(input("""Introduzca el método a utilizar:
                            1. Método FTIR
                            2. Método GC-FID:\n"""))
    fotolisis = int(input("Ingrese hasta que punto hizo el tiempo base:\n"))
    temperatura = int(input("Ingrese la temperatura (K):\n"))
    cinetica = str(input("Por favor, indicar el nombre del archivo donde se guardará la cinética:\n"))
    if metodo == 1:#FTIR
        print("Se procede a calcular la k del compuesto {} a {} K por FTIR, usando {} como referencia \n".format(nombre_compuesto, temperatura, nombre_referencia))
        lista_compuesto, tiempo = informacion_diccionario(dato_archivo, "factor compuesto", "tiempo (h)")
        datos_kwall, datos_grafica = genera(lista_compuesto, fotolisis)# datos_grafica = valores a restar el k_wall
        lista_temporal = lista_segundos(tiempo)
        tiempo_wall_loss, tiempo_grafica = tiempo_total(lista_temporal, "FTIR", fotolisis)
        k_wall = calculo_kwall(tiempo_wall_loss, datos_kwall)
        if k_wall <= 1E-4:#se desprecia
            k_wall = 0
            tabla_cinetica(dato_archivo, k_wall, cinetica, "FTIR", fotolisis)
            compuesto, referencia = informacion_diccionario(cinetica, "Ln(Co/Ct)", "Ln(Refo/Reft)")
            vector_compuesto, vector_referencia = lista_grafica(compuesto, referencia, fotolisis)
            pendiente = calculo_cinetica(vector_compuesto, vector_referencia)
            print("kcomp/kref = {}".format(pendiente))
            k_cinetica = pendiente * constante_referencia
        else:#aqui se resta el valor de k_wall
            tabla_cinetica(dato_archivo, k_wall, cinetica, "FTIR", fotolisis)
            wall_loss, referencia = informacion_diccionario(cinetica, "kwall-loss", "Ln(Refo/Reft)")
            vector_kwall, vector_referencia = lista_grafica(wall_loss, referencia, fotolisis)
            pendiente = calculo_cinetica(vector_kwall, vector_referencia)
            k_cinetica = pendiente * constante_referencia
    else:#GC-FID
        print("Se procede a calcular la k del compuesto {} a {} K por GC-FID, usando {} como referencia \n".format(nombre_compuesto, temperatura, nombre_referencia))
        lista_compuesto, tiempo = informacion_diccionario(dato_archivo, "area C", "tiempo (s)")
        datos_kwall, datos_grafica = genera(lista_compuesto, fotolisis)# datos_grafica = valores a restar el k_wall
        tiempo_wall_loss, tiempo_grafica = tiempo_total(tiempo, "GC-FID", fotolisis)
        k_wall = calculo_kwall(tiempo_wall_loss, datos_kwall)
        if k_wall <= 1E-4:#se desprecia
            k_wall = 0
            tabla_cinetica(dato_archivo, k_wall, cinetica, "GC-FID", fotolisis)
            compuesto, referencia = informacion_diccionario(cinetica, "Ln(Co/Ct)", "Ln(Refo/Reft)")
            vector_compuesto, vector_referencia = lista_grafica(compuesto, referencia, fotolisis)
            pendiente = calculo_cinetica(vector_compuesto, vector_referencia)
            print("kcomp/kref = {}".format(pendiente))
            k_cinetica = pendiente * constante_referencia
        else:#aqui se resta el valor de k_wall
            tabla_cinetica(dato_archivo, k_wall, cinetica, "GC-FID", fotolisis)
            wall_loss, referencia = informacion_diccionario(cinetica, "kwall-loss", "Ln(Refo/Reft)")
            vector_kwall, vector_referencia = lista_grafica(wall_loss, referencia, fotolisis)
            pendiente = calculo_cinetica(vector_kwall, vector_referencia)
            k_cinetica = pendiente * constante_referencia
    return k_cinetica, nombre_compuesto

    
def simulador():#Aqui es donde se va a desarrollar el programa
    """ Aqui se encuentra lo que va a realizar el programa
        Simulador Ambiental: Química Atmosférica """
    estudio = int(input("""Ingrese: 
                            1 Cinética Química
                            2 Impactos Ambientales\n"""))
    if estudio == 1:
        opciones_cinetica = int(input("""Ingrese:
                                        1 Cinética con Radicales Atmosféricos
                                        2 Productos\n"""))
        if opciones_cinetica == 1:#Aqui se realizan todos los cálculos cinéticos
            archivo = str(input("Ingrese el nombre del archivo donde posee la cinética:\n"))
            radical_cinetica = str(input("Por favor, introducir el radical con que desea estudiar el compuesto:\n"))
            resultado_constante, compuesto_interes = cinetica_quimica(archivo, radical_cinetica)
            print("La constante cinética de {}".format(compuesto_interes),"es {0:.3E} (cm3.molécula-1.s-1)".format(resultado_constante))
        else:
            print("Lo sentimos, por ahora no procesamos productos")#Aqui los cálculos de productos seran para
    else:#Aqui van los calculos de Impactos Ambientales            #los proximos modulos del curso
        opciones_impacto = int(input("""Ingrese:
                                        1 Tiempo de residencia atmosféricos (t[x] x = OH, Cl, NO3 y O3)
                                        2 Potencial de Acidificación (AP)
                                        3 Potencial Fotoquímico de creación de ozono (POCP)\n"""))
        if opciones_impacto == 1:#Aqui van todos los cálculos de tiempo de residencia
            condicion_tiempo = int(input("""Posee ud la constante cinética del compuesto?
                                            1 Si
                                            2 No\n"""))
            if condicion_tiempo == 1:
                compuesto_interes = str(input("Ingrese el nombre del compuesto:\n"))
                resultado_constante = float(input("Por favor introducir la constante cinética:\n"))
                radical_cinetica = str(input("Por favor, introducir el radical con que desea estudiar el compuesto: \n"))
                impacto_tiempo = tiempo_residencia(resultado_constante, radical_cinetica)
                print("t[{}] para {}".format(radical_cinetica, compuesto_interes), " = ", round(impacto_tiempo, 2), "s", ",", round(impacto_tiempo / 3600, 2), "h", ",", round(impacto_tiempo / (3600 * 24), 2), "días", ",", round(impacto_tiempo / (3600 * 24 *365), 2), "años")
            else:
                archivo = str(input("Ingrese el nombre del archivo donde posee la cinética:\n"))
                radical_cinetica = str(input("Por favor, introducir el radical con que desea estudiar el compuesto:\n"))
                resultado_constante, compuesto_interes = cinetica_quimica(archivo, radical_cinetica)
                print("La constante cinética de {}".format(compuesto_interes),"es {0:.3E} (cm3.molécula-1.s-1)".format(resultado_constante))
                impacto_tiempo = tiempo_residencia(resultado_constante, radical_cinetica)
                print("t[{}] para {}".format(radical_cinetica, compuesto_interes), " = ", round(impacto_tiempo, 2), "s", ",", round(impacto_tiempo / 3600, 2), "h", ",", round(impacto_tiempo / (3600 * 24), 2), "días", ",", round(impacto_tiempo / (3600 * 24 *365), 2), "años")
        else:
            if opciones_impacto == 2:#Aqui va todos los cálculos de AP
                peso_compuesto = float(input("Ingrese el Peso molecular del compuesto (g/mol):\n"))
                numero_cloro = int(input("Ingrese la cantidad de átomos de Cloro que posee el compuesto:\n"))
                numero_fluor = int(input("Ingrese la cantidad de átomos de Flúor que posee el compuesto:\n"))
                numero_nitrogeno = int(input("Ingrese la cantidad de átomos de Nitrogeno que posee el compuesto:\n"))
                numero_azufre = int(input("Ingrese la cantidad de átomos de Azufre que posee el compuesto:\n"))
                potencial_ap = round((64.066 / peso_compuesto) * (numero_cloro + numero_fluor + numero_nitrogeno + 2 * numero_azufre) / 2, 2)
                if potencial_ap >= 0.5 and potencial_ap <= 1:
                    print("Posee un AP moderado, tiene tendencia a producir lluvia ácida")
                    indice_acidificacion(potencial_ap)
                else:
                    if potencial_ap >= 0.5 and potencial_ap >= 1:
                        print("Posee un AP moderado, tiene tendencia a producir lluvia ácida")
                        indice_acidificacion(potencial_ap)
                    else:
                        print("El potencial AP = {} del compuesto es < 0,5, se le considera que tiene poca probabilidad de producir lluvia ácida".format(potencial_ap))
            else:#Aqui va todos los cálculos de POCP
                peso_compuesto = float(input("Ingrese el Peso molecular del compuesto (g/mol):\n"))
                enlaces_compuesto = int(input("Ingrese el número de enlaces del compuesto:\n"))
                carbonos_compuesto = int(input("Ingrese los números de carbono del compuesto:\n"))
                condicion_pocp = int(input("""Posee ud la constante cinética del compuesto?
                                            1 Si
                                            2 No\n"""))
                if condicion_pocp == 1:
                    nombre_compuesto = str(input("Ingrese el nombre del compuesto:\n"))
                    resultado_constante = float(input("Por favor introducir la constante cinética:\n"))
                    pocp = potencial_ozono(peso_compuesto, enlaces_compuesto, carbonos_compuesto, resultado_constante)
                    print("El valor de POCP es = {} para el {} y el del Etileno el POCP = 100".format(pocp, nombre_compuesto))
                else:
                    archivo = str(input("Ingrese el nombre del archivo donde posee la cinética:\n"))
                    radical_cinetica = str(input("Por favor, introducir el radical con que desea estudiar el compuesto:\n"))
                    resultado_constante, compuesto_interes = cinetica_quimica(archivo, radical_cinetica)
                    print("La constante cinética de {}".format(compuesto_interes),"es {0:.3E} (cm3.molécula-1.s-1)".format(resultado_constante))
                    pocp = potencial_ozono(peso_compuesto, enlaces_compuesto, carbonos_compuesto, resultado_constante)
                    print("El valor de POCP es = {} para el {} y el del Etileno el POCP = 100".format(pocp, compuesto_interes))
    

if __name__ == '__main__':
    print("Proyecto: Simulador Ambiental: Química Atmosférica")
    simulador()