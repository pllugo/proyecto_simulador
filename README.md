# Simulador de Química Ambiental 🧑‍🏭
  Este es un proyecto para conocer el impacto ambiental del estudios de compuestos que pueden contaminar el aire, agua y suelo.
  El simulador se centra, por los momentos, en conocer la cinética por el cual un compuesto puede interactuar con radicales atmosfericos (elementos capaces de degradar     contaminantes).

1. Obtener la constante cinética de un compuesto con radicales atmosféricos y comparar el resultado con una base de datos de otras cinéticas de compuestos similares.

2. Monitoreo de productos formados durante la reacción del compuesto con un radical atmosférico (%Porcentaje de formación de cada producto) (Queda para el segundo modulo del proyecto)

3. Determinar los Impactos ambientales con los siguientes indices: Potencial de Acidificación (AP), Potencial fotoquimico de creación de ozono (POCP) y tiempo de residencia atmosférico (t) y comparar con una base de datos de otros compuestos.

### Metodología experimental

  Para el funcionamiento del simulador de quimica ambiental, se estudió la química atmosferica, en donde un compuesto de interes (Compuesto Orgánico Volátil COV) reacciona con un radical atmosferico, a su vez  tambien se coloca a reaccionar un compuesto de referencia (que se conoce su cinética) con ese mismo radical. Haciendo reordenamientos matemáticos correspondientes, éste estudio se resume como: 
   
  - Ln(Comp0/Compt) = (kComp/kRef).Ln(Ref0/Reft)   (I)
  - y = m.x
  - Donde:
    - Comp0: Compuesto de interes al tiempo 0
    - Compt: Compuesto de interes al tiempo t
    - Ref0: Compuesto de Referencia al tiempo 0
    - Reft: Compuesto de Referencia al tiempo t
    - kComp: Constante cinética del compuesto de interes
    - kRef: Constante cinética del compuesto de Referencia
    
  La ecuación (I) representa una línea recta (y=mx) el cual se puede calcular la pendiente (m) y con la constante cinética del compuesto de referencia se puede conocer la cinética del compuesto a estudiar con el radical correspondiente. Por lo que se le suministrará al simulador unos datos experimentales de cinética de una Dicetona Fluorada y un Fluoroéster con radicales OH (radical con mayor concentración en la atmosfera).
  
### Técnias de medición

1. FTIR: Espectroscopía Infrarroja con Transformada de Fourier
2. GC-FID: Cromatografía Gaseosa con Detector de Llama

### Estructura del Simulador de Química Ambiental ⌨

- _simulador_ : La función simulador es donde se desarrolla la parte central del programa y llama a las demás funciones
- _cinetica_quimica_ : La función cinetica_quimica se envian los datos de: archivos donde se posee la cinética y el radical por el cual va a trabajar dicha cinética
- _concentración_ : Esta función se encarga de conocer la cantidad de compuesto a inyectar en los reactores de 405, 480 y 1080 L para el estudio cinético
- _información compuestos_ : Esta función recibe el nombre del compuesto y busca en la base de datos sus propiedades como peso molecular y densidad
- _potencial ozono_ : La función para calcular el POCP (Potencial fotoquimico de creación de ozono), aqui el usuario debe especificar que tipo de compuesto posee (aldehidos, cetonas, esteres, alifatico, arometico, etc).
- _funcion ozono_ : En ésta función busca en una base de datos, si el criterio es Europa o USA para el cálculo del POCP.
- _tiempo residencia_ : La función realiza el calculo para el tiempo de residencia atmosferico, dependiendo del radical que introduce el usuario
- _indice acidificacion_ : La función se ingresa un potencial de acidificación y busca en una base de datos el valor mas proximo a éste potencial de acidificación.
- _diccionario compuestos_ : En ésta función se suministra el nombre de la referencia y el dato del radical y la función busca en un archivo csv la constante cinética, peso molecular y densidad de la referencia a utilizar.
- _calculo kwall_ : Esta función arroja el valor de la constante cinética del compuesto de interés si sufre perdidas de pared en el reactor utilizado, llamado kwall loss, además de presentar al usuario la grafica de los datos experimentales suministrados. Si la kwall es menor al valor programado, éste valor se despreciará, en caso contrario se restará al valor de la constante cinética a calcular.
- _calculo cinetica_ : En esta función arroja el valor de la constante cinética del COV de interés, además de presentar la gráfica de los datos experimentales, a traves, de minimos cuadrados.
- _genera_ : La función genera dos listas de los primeros datos (experimentos a oscuras) y la segunda lista de datos (experimentos con UV encendido), según el dato de fotólisis ingresado por el usuario
- _tabla cinetica_ : La función genera un archivo csv, donde coloca los calculos de los datos experimentales suministrados, ésto sirve como evidencia de como se construyó la grafica.
- _lista grafica_ : Función que separa las listas generadas en la primera para el COV y la segunda para el compuesto de referencia, éstas listas sirven para realizar las graficas que se presentan al usuario.
- _informacion diccionario_ : Función para generar listas a partir de un archivo CSV
- _variable tiempo_ : La función se encarga de transformar un dato de tiempo en formato hh:mm:ss a s
- _lista segundos_ : La función pasa los datos de una lista en hh:mm:ss a s
- _tiempo total_ : La función divide la lista de tiempos en segundos en dos partes, si la técnica de medición es FTIR, tanto la primera lista como la segunda, los tiempos se restan según la metodologia del programa. Si la técnica de medición es GC-FID, solo divide la lista en dos no es necesario realizar restas de elementos.


### Datos de entrada del simulador

Para el funcionamiento del simulador, se contará solo con los siguientes datos de entrada:

1. Etil Fluoroacetato: Compuesto que cuenta con datos experimentales cinéticos solo en FTIR y con la referencia Butano con radicales OH
2. 1,1,1-Trifluoro-2,4-pentanodiona: Compuesto que cuenta con datos experimentales cinéticos con referencia Isobutano y Dietil eter para FTIR y GC-FID respectivamente con radicales OH.
3. Temperatura: 298 K
4. Los experimentos en GC-FID casi siempre poseen hasta 3 puntos de tiempo base y para FTIR se poseen 5 puntos de tiempo base.


### Pruebas del Simulador de Química Ambiental

 ![kwall loss](\images\kwall_loss.jpeg)
 
La impresión de los resultados se hace por consola, por ejemplo:

```
Proyecto: Simulador Ambiental: Química Atmosférica
Ingrese: 
                            1 Cinética Química    
                            2 Impactos Ambientales
1
Ingrese:
                                        1 Cinética con Radicales Atmosféricos
                                        2 Productos
1
Ingrese el nombre del archivo donde posee la cinética:
cinetica_EFA_OH.csv
Por favor, introducir el radical con que desea estudiar el compuesto:
OH
Ingrese el nombre del compuesto:
Etil Fluoroacetato
Ingrese la cantidad de compuesto inyectado (uL):
10
Ingrese el Volumen del reactor:
                                1 Reactor 405 L UNC
                                2 Reactor 480 L Universidad de Wuppertal
                                3 Reactor 1080 L Universidad de Wuppertal
2
La concentración en del Etil Fluoroacetato en [ppm] = 5.276028137284201
Ingrese el nombre de la referencia:
Butano
Ingrese la cantidad de referencia inyectada (uL):
70
La constante cinética de Butano es 2.38e-12 con radicales OH
Ingrese el Volumen del reactor:
                                1 Reactor 405 L UNC
                                2 Reactor 480 L Universidad de Wuppertal
                                3 Reactor 1080 L Universidad de Wuppertal
2
La concentración en del Butano en [ppm] = 35.184161309094165
Introduzca el método a utilizar:
                            1. Método FTIR
                            2. Método GC-FID:
1
Ingrese hasta que punto hizo el tiempo base:
5
Ingrese la temperatura (K):
298
Por favor, indicar el nombre del archivo donde se guardará la cinética:
cinetica_nueva.csv
Se procede a calcular la k del compuesto Etil Fluoroacetato a 298 K por FTIR, usando Butano como referencia

R2 = 0.9519
R2 = 0.9966
La constante cinética de Etil Fluoroacetato es 1.120E-12 (cm3.molécula-1.s-1)
```

### Construido con 🛠
Librerias:
- numpy
- matplotlib.pyplot (herramienta para graficar)
- math

### Versión 📌

  Versión 1.00

### Autores ✒
- Datos de cinéticas con COVs **MSc. Pedro Lugo**
- Programación del simulador **MSc. Pedro Lugo**
- Base de datos de COVs **Lic. Vianni Straccia**
