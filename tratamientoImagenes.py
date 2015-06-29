import random
import shutil
import os
import difflib

#REALIZADO POR:
#ABRAHAM REQUENA MESA
#MANUEL JESÚS BARRERA POZO
#HEMOS CONSIDERADO LA POBLACION INICIAL COMO UN CONJUNTO DE CROMOSOMAS FORMADOS POR K CUADRADOS CADA UNO, UTILIZANDO LA FUNCION CREARCROMOSOMA()
#POSTERIORMENTE, UNA VEZ CREADA LA POBLACIÓN INICIAL Y PARA REALIZAR LOS CRUCES LO HACEMOS DE LA SIGUIENTE 3 MANERA:
#NOS QUEDAMOS CON LOS 2 MEJORES CROMOSOMAS DE LA POBLACION, Y ELIMINAMOS LOS DOS PEORES. LUEGO, COMBINAMOS LOS 2 CROMOSOMAS MEJORES TENIENDO DE NUEVO
#EL MISMO NUMERO DE INDIVIDUOS.
#EN LA FUNCION MEJORIMAGEN(), COMENZAMOS LLAMANDO A LA FUNCION CREARCROMOSOMA() PARA CREAR LA POBLACION INICIAL, Y EJECUTAMOS LA FUNCION DEFINITIVA
#TANTAS VECES COMO ITERACIONES MARQUEMOS.
#CUANDO REALIZAMOS TODAS LAS ITERACIONES, NOS QUEDAMOS CON EL MEJOR INDIVIDUO Y LO LLAMAMOS RESULTADOFINAL


def crearGenAleatorioBueno(nombre):
    tam = 30
    gris = random.randint(0,255)
    tamanoCuadrado = random.randint(0, tam)
    tamanoActual = tamanoCuadrado
    aleatorio = random.randint(0,(tam-tamanoCuadrado))
    loBlancoQuenoEsCuadrado = random.randint(0,tam - tamanoCuadrado)
    blanco = 255
    archi = open(nombre + '.pgm' , 'w')
    archivo = open(nombre + '.pgm' , 'a')
    archi.write('P2\n')
    archi.write(str(tam) + ' ' + str(tam) +'\n')
    archi.write('255\n')
    for i in range (tam*aleatorio):
      archi.write(str(blanco) + '\n')
    while (tamanoActual > 0):
        for i in range (loBlancoQuenoEsCuadrado):
            archi.write(str(blanco) + '\n')
        for i in range (tamanoCuadrado):
            archi.write(str(gris) + '\n')
        for i in range (tam - loBlancoQuenoEsCuadrado - tamanoCuadrado):
            archi.write(str(blanco) + '\n')
        tamanoActual = tamanoActual - 1
    for i in range ((tam*tam)-(tam*aleatorio)-(tam*tamanoCuadrado)):
       archi.write(str(blanco) + '\n')
    archi.close()


def crearCromosoma(numeroCromosomas, numeroCuadrados):
    for a in range(numeroCromosomas):
        lista = []
        for j in range(numeroCuadrados):
            cuadrado = crearGenAleatorioBueno(str(a)+'-'+str(j))
            lista.append(str(a)+'-'+str(j) + '.pgm')
        #lista = ['0.pgm', '1.pgm', '2.pgm', '3.pgm', '4.pgm']
        #lista = ['q1.pgm' , 'q2.pgm' , 'q3.pgm']
        cuadroFinal = open('resultado'+str(a)+'.pgm' ,'w')
        cuadroFinal.write('P2\n')
        primero = open(lista[0])
        primeralinea = primero.readline()
        byte1 = int(primero.read(2))
        total = byte1 * byte1
        cuadroFinal.write(str(byte1) + ' ' + str(byte1) + '\n')
        for j in range (total+1):
            l = []
            for i in range (numeroCuadrados):
                a = open (lista[i])
                a.readline()
                a.readline()
                lineas = a.readlines()
                lineaActual = lineas[j]
                cantidadDeGris = 255 - int(lineaActual)
                l.append(cantidadDeGris)
            suma =0
            for j in l:
                suma = suma + int(j)
                grisFinal = 255 - int(suma)
                if(suma>255):
                    grisFinal = 0
            cuadroFinal.write(str(grisFinal)+'\n')

def funcionDeValoracion(a, b):
    imagenCandidata = open(a) #miimagen
    imagenSerie = open(b) #carritogolf
    imagenSerie.readline() #primera linea
    imagenCandidata.readline() #primera linea
    tam = imagenSerie.read(2) #lee tamaño
    imagenSerie.readline() #segunda linea
    imagenCandidata.readline() #segunda linea
    nLineas = int(tam) * int(tam)
    vTotal = 0
    for i in range(nLineas):
        s = int(imagenSerie.readline()) #carrito
        c = int(imagenCandidata.readline()) #miimagen
        v = abs(s - c)
        vTotal = vTotal + v
    return vTotal

def definitiva(iteracion,imagen,numeroCromosomas,numeroCuadrados,porc):
    mejores = [] #resultados que vamos a cruzar
    peores = [] #resultados que vamos a eliminar y el nuevo resultado sera cuando crucemos.
    listaOrdenada = [] #lista donde vayamos metiendo los cuadrados para realizar el cromosoma
    for i in range(numeroCromosomas):
        i = funcionDeValoracion('resultado' + str(i)+'.pgm', imagen)
        listaOrdenada.append(i)
    listaOrdenada.sort() #ordenamos la lista
    print(listaOrdenada)
    x = 2
    mejorValoracion = listaOrdenada[0]
    segundaMejorValoracion = listaOrdenada[1]
    while(mejorValoracion==segundaMejorValoracion and x<numeroCromosomas-2):
        segundaMejorValoracion = listaOrdenada[x]
        x = x + 1
    listaOrdenada.reverse()
    peorValoracion = listaOrdenada[0]
    segundaPeorValoracion = listaOrdenada[1]
    print(str(mejorValoracion) + '-> mejorValoracion')
    print(str(segundaMejorValoracion) + '-> 2mejorValoracion')
    print(str(peorValoracion) + '-> PeorValoracion')
    print(str(segundaPeorValoracion) + '-> 2peorValoracion')
    borraPeores = 2
    pmejor = 1
    smejor = 1
    for j in range(numeroCromosomas):
        valoracion = funcionDeValoracion('resultado' + str(j) +'.pgm', imagen)
        if(valoracion == mejorValoracion and pmejor>0):
            mejores.append(j)
            print(str(j) + '1ºmejor')
            pmejor = int(pmejor) - 1
            if(iteracion%porc == 0): 
                shutil.copy('resultado' + str(j) + '.pgm', 'r' + str(iteracion)+ '-'+ str(valoracion) +'.pgm')
        elif(valoracion == peorValoracion and borraPeores>0):
            os.remove('resultado' + str(j) + '.pgm')
            borraPeores = int(borraPeores) - 1
            peores.append(j)
            print(str(j) + 'eliminado')
            for i in range(numeroCuadrados):
                os.remove(str(j)+ '-' + str(i) + '.pgm')
        elif(valoracion == segundaPeorValoracion and borraPeores>0):
            os.remove('resultado' + str(j) + '.pgm')
            borraPeores = int(borraPeores) - 1
            peores.append(j)
            print(str(j) + 'eliminado')
            for i in range(numeroCuadrados):
                os.remove(str(j) + '-' + str(i) + '.pgm')
        elif(valoracion == segundaMejorValoracion and smejor>0):
            mejores.append(j)
            print(str(j)+' ' + 'mejor')
            smejor = int(smejor) - 1
            if (iteracion%porc == 0): 
                shutil.copy('resultado' + str(j) + '.pgm', 'r' +  str(iteracion) + '-' + str(valoracion) +'.pgm')            
    print(mejores)
    print(peores)
    pEletodos = mejores[0]
    sEletodos = mejores[1]
    n = random.randint(1,numeroCuadrados-1)##numero de cuadrados de uno de ellos
    for t in range(2):
        lista = []
        numCuadrados = n
        for a in range(numCuadrados):
            lista.append(str(pEletodos)+ '-' + str (a) + '.pgm')
            shutil.copy(str(pEletodos) + '-' + str(a) + '.pgm', str(peores[t]) + '-' + str(a) + '.pgm')
        while(numCuadrados<numeroCuadrados):
            lista.append(str(sEletodos) + '-' + str(numCuadrados) + '.pgm')
            shutil.copy(str(sEletodos)+ '-' + str(numCuadrados) + '.pgm', str(peores[t]) +'-' + str(numCuadrados) + '.pgm')
            numCuadrados = numCuadrados + 1 
        cuadroFinal = open('resultado' + str(peores[t]) +'.pgm' ,'w')
        cuadroFinal.write('P2\n')
        primero = open(lista[0])
        primeralinea = primero.readline()
        byte1 = int(primero.read(2))
        total = byte1 * byte1
        cuadroFinal.write(str(byte1) + ' ' + str(byte1) + '\n')
        pEletodos, sEletodos = sEletodos, pEletodos #intercambio valores pEletodos y sEletodos
        print(lista)
        print(pEletodos)
        print(sEletodos)
        for j in range (total+1):
            l = []
            for i in range (numeroCuadrados):
                a = open (lista[i])
                a.readline()
                a.readline()
                lineas = a.readlines()
                lineaActual = lineas[j]
                cantidadDeGris = 255 - int(lineaActual)
                l.append(cantidadDeGris)
            suma =0
            for j in l:
                suma = suma + int(j)
                grisFinal = 255 - int(suma)
                if(suma>255):
                    grisFinal = 0
            cuadroFinal.write(str(grisFinal)+'\n')
##AQUI FINALIZA LOS CRUCES.

def mejorImagen():
    imagen = 'negroCentro.pgm'
    numeroCuadrados = 15
    numeroCromosomas = 20
    crearCromosoma(numeroCromosomas,numeroCuadrados)
    numeroIteraciones = 20
    iteracion = 1
    porc = round(numeroIteraciones * 0.1)
    while(numeroIteraciones>0):
        definitiva(iteracion,imagen,numeroCromosomas,numeroCuadrados,porc)
        numeroIteraciones = numeroIteraciones - 1
        iteracion = iteracion + 1
    ultimaGeneracion = []
    for u in range (numeroCromosomas):
        i = funcionDeValoracion('resultado' + str(u) + '.pgm', imagen)
        ultimaGeneracion.append(i)
    ultimaGeneracion.sort()
    print(ultimaGeneracion)
    mejorValoracion = ultimaGeneracion[0]
    print(mejorValoracion)        
    for a in range(numeroCromosomas):
        if(funcionDeValoracion('resultado' + str(a) +'.pgm', imagen) == mejorValoracion):
            shutil.copy('resultado' + str(a) + '.pgm', 'resultadoFinal.pgm')
            break

