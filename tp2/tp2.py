#Algoritmos y programación I.
#Cátedra: Essaya.
#Práctica: Grace.
#Nombre: Mauro Javier Santoni.
#Padrón: 102654.
#Corrector: Juan Patricio Marshall.

'''
Entrada

Se dispone de un archivo palabras.csv con el siguiente formato:

palabra|definicion

A partir de dicho archivo el programa debe seleccionar un conjunto de palabras al azar (uno distinto cada vez que se ejecuta) y generar un crucigrama.
Crucigrama

El crucigrama generado debe cumplir con las siguientes condiciones:

    Debe tener una sola palabra horizontal, de al menos 8 letras.
    No puede haber dos letras consecutivas en la palabra horizontal que se crucen con una vertical.
    No puede haber tres letras consecutivas en la palabra horizontal que no se crucen con ninguna vertical.
    Todas las palabras deben ser diferentes.

Nota: el cruce entre palabras es, por supuesto, en una letra compartida. Por simplicidad, vamos a considerar a todas las letras con tilde, virgulilla o similar como diferentes a las letras simples. Es decir que los caracteres A y Á son diferentes, como así también N y Ñ, U y Ü, etc. Por lo tanto, la palabra ÁTICO no puede cruzarse con BANANA, pero sí con ANANÁ.
Salida

El programa debe imprimir un crucigrama listo para ser jugado, mostrando las celdas del crucigrama vacías, la referencia de coordenadas de las celdas y las definiciones de cada palabra.

Se deja a libre elección el formato en el que se muestra cada elemento, pero se sugiere un ejemplo a continuación.

Si el programa recibe la opción -s (ejemplo: python tp2.py -s), además debe imprimir la solución del crucigrama.
'''

import argparse
import random
import csv

def main():
	''' Funcion principal del programa. Inicializa la opcion -s que puede ingresar el usuario para obtener la solucion. Ejecuta las funciones que imprimen el crucigrama dependiendo de dicha opcion.'''
	parser = argparse.ArgumentParser(description='Generador de crucigramas')
	parser.add_argument('-s', '--solucion', action='store_true', help='imprimir la solución')
	args = parser.parse_args()
	imprimir_solucion = args.solucion # es True si el usuario incluyó la opción -s
	
	inventario_palabritas,horizontal,verticales = generar_palabras_random()
	
	if imprimir_solucion:
		imprimir_cruci(inventario_palabritas,horizontal,verticales)
		imprimir_solu(inventario_palabritas,horizontal,verticales)
	else:
		imprimir_cruci(inventario_palabritas,horizontal,verticales)


def es_par(n):
	'''Devuelve True si el numero ingresado es par, caso contrario devuelve False.'''
	return n%2==0

def inventario_palabras():
	'''Importa todas las palabras del archivo asignado para el TP. Devuelve un diccionario {palabra:definicion} y,
	del inventario de palabras, filtra y devuelve las palabras cuya longitud es mayor o igual a 8 letras.'''
	palabras = {}
	with open('palabras.csv') as todas:
		lector = csv.reader(todas, delimiter = '|')
		horizontales = []
		for palabra,definicion in lector:
			palabras[palabra] = palabras.get(palabra,definicion)
			if len(palabra) >= 8:
				horizontales.append(palabra)
		return palabras,horizontales

		
def inventario_letras(inventario_palabras):
	'''Crea y devuelve un diccionario con clave cada letra del abecedario y valor las palabras que contengan esa letra.'''
	letras_palabras = {}
	letras = 'AÁÄBCDEÉËFGHIÍÏJKLMNÑOÓÖPQRSTUÚÜVWXYZ'
	for letra in letras:
		for palabra in inventario_palabras:
			if letra in palabra:
				letras_palabras[letra] = letras_palabras.get(letra,[])
				letras_palabras[letra].append(palabra)
	return letras_palabras

def elegir_horizontal(horizontales):
	'''Recibe un inventario de palabras. Devuelve una palabra random para ser usada como horizontal.'''
	horizontal = random.choice(horizontales)
	return horizontal

def letras_horizontal(horizontal):
	'''Recibe una palabra random horizontal. Devuelve una lista compuesta de tuplas con las letras que se usaran para las verticales y su posicion en la palabra horizontal.'''
	letra_para_vertical = []
	for posicion in range(0,len(horizontal),2):
		tupla = (horizontal[posicion],posicion)
		letra_para_vertical.append(tupla)
	return letra_para_vertical
	
def elegir_vertical(letra_horizontal,horizontal,inventario_letras):
	'''Recibe el resultado de la funcion letras_horizontal con una palabra horizontal previamente elegida, y la palabra horizontal. Devuelve un diccionario con la palabra vertical a usar como clave y como valor una tupla con la posicion en la palabra horizontal que debe ir y la posicion de coincidencia de la letra de la palabra vertical con la horizontal.'''
	verticales = [] #[palabra,(posicion en la H, posicion de coincidencia de la V)]
	for tupla in letra_horizontal:
		letra = tupla[0]
		posicion_en_la_horizontal = tupla[1]
		vertical = random.choice(inventario_letras[letra])
		#Verificacion que no se repitan las palabras
		contador = 0
		while contador != len(verticales):
			if vertical == verticales[contador][0] or vertical == horizontal:
				vertical = random.choice(inventario_letras[letra])
				contador = 0
			else:
				contador += 1
		#Fin verificacion
		for posicion in range(len(vertical)):
			if letra == vertical[posicion]:
				coincidencia_posicion = posicion
		verticales.append([vertical,(posicion_en_la_horizontal,coincidencia_posicion)])
	return verticales

def generar_palabras_random():
	'''Genera las palabras, letras y todo lo necesario para armar el crucigrama a partir de funciones previas. Devuelve todo lo necesario para armarlo.'''
	inventario_palabritas,horizontales = inventario_palabras()
	inventario_letritas = inventario_letras(inventario_palabritas)
	horizontal = elegir_horizontal(horizontales)
	letra_para_vertical = letras_horizontal(horizontal)
	verticales = elegir_vertical(letra_para_vertical,horizontal,inventario_letritas)
	return inventario_palabritas,horizontal,verticales
	
def generar_crucigrama(horizontal,verticales):
	'''Recibe todo lo necesario para armar un crucigrama que proviene de la funcion generar_palabras_random. Genera un crucigrama. Devuelve el crucigrama armado en forma de lista de listas que luego sera modificado para ser impreso.'''
#--------------
#Creo el crucigrama vacio.
	crucigrama = []
	vertical_mas_larga = ''
	for i in range(len(verticales)):
		if len(verticales[i][0]) > len(vertical_mas_larga):
				vertical_mas_larga = verticales[i][0]
	cant_filas = len(vertical_mas_larga) * 2 #Numero de filas
	for num in range(cant_filas - 1):
		crucigrama.append([])
	
#--------------
#Lleno el crucigrama
	posicion_horizontal = int(len(crucigrama)/2) #numero de fila donde esta la horizontal
	contador_palabra_vertical = 0
	letra_horizontal = 0
	for columna in range(len(horizontal)):
		switch = False #cambia a True cuando la palabra vertical comienza y asi saber a partir de que fila insertar los caracteres de la palabra vertical.
		letra = 0
		if contador_palabra_vertical < len(verticales):
			tupla_1 = verticales[contador_palabra_vertical][1][1]
			palabra_vertical = verticales[contador_palabra_vertical][0]
		for fila in range(len(crucigrama)):
			if columna == 0:
				if int(fila + tupla_1) == posicion_horizontal:
					switch = True	
				if switch and letra < len(palabra_vertical):
					crucigrama[fila] += verticales[contador_palabra_vertical][0][letra]
					letra += 1
				else:
					crucigrama[fila] += ' '
			if es_par(columna) and columna != 0:
				if int(fila + tupla_1) == posicion_horizontal:
					switch = True
				if switch and letra < len(palabra_vertical):
					crucigrama[fila][0] += verticales[contador_palabra_vertical][0][letra]
					letra += 1
				else:
					crucigrama[fila][0] += ' '
			if not es_par(columna):
				if fila == posicion_horizontal:
					crucigrama[fila][0] += horizontal[letra_horizontal]
				else:
					crucigrama[fila][0] += ' '	
		if es_par(columna):
			contador_palabra_vertical += 1			
		letra_horizontal += 1			
	
#---------------------------
#Le saco las lineas vacias al crucigrama, las que 'sobran'.
	cont_linea = 0
	while cont_linea != len(crucigrama):
		if crucigrama[cont_linea][0].isspace():
			crucigrama.pop(cont_linea)
			continue
		else:
			cont_linea += 1
	return crucigrama

def letras_por_puntos(crucigrama):
	'''Recibe un crucigrama llenado con letras. Devuelve el mismo crucigrama con las letras reemplazadas por puntos.'''
	for linea in range(len(crucigrama)):
		for letra in crucigrama[linea][0]:
			if letra.isalpha():
				crucigrama[linea] = [crucigrama[linea][0].replace(letra,'•')]
	return crucigrama

def agregar_indicadores(crucigrama):
	'''Recibe un crucigrama llenado. Agrega los numeros de referencia y la referencia a la horizontal.'''
	for fila in range(len(crucigrama)):
		for columna in range(len(crucigrama[0])):
			if ' ' not in crucigrama[fila][columna]:
				pos_horizontal = fila #Establezco donde insertar la 'H'.
	for fila in range(len(crucigrama)): #Inserto la 'H'.
		if fila == pos_horizontal:
			crucigrama[fila].insert(0,'H  ')
		else:
			crucigrama[fila].insert(0,'   ')

	#Inserto los numeros de referencia
	cadena = ''
	cont = 1
	for i in range(len(crucigrama[1][1])):		
		if es_par(i):
			cadena += str(cont)
			cont += 1
		else:
			cadena += ' '
			
	cadena_espacios = [' ' * len(crucigrama[0])]
	crucigrama.insert(0,[cadena])
	crucigrama[0].insert(0,'   ')
	crucigrama.insert(1,cadena_espacios)
	crucigrama[1].insert(0,'   ')
	
	for fila in range(len(crucigrama)): #Uno todos los espacios y 'H' agregados.
 		crucigrama[fila] = [''.join(crucigrama[fila])]
 		
	return crucigrama

#--------------
#Imprimir el crucigrama 
def imprimir_sin_soluciones(crucigrama,verticales,horizontal,inventario_palabras):
	'''Imprime el crucigrama con las palabras reempladas por puntos y sus definiciones.'''
	print('CRUCIGRAMA')
	print()

	for fila in range(len(crucigrama)):
		print(crucigrama[fila][0])
	print()
	print('DEFINICIONES')
	print()
	print('H. {}'.format(inventario_palabras[horizontal]))
	for lista in range(len(verticales)):
		print('{}. {}'.format(lista+1,inventario_palabras[verticales[lista][0]]))

def imprimir_solucion(crucigrama):
	'''Imprime la solución del crucigrama previamente creado.'''
	print()
	print('SOLUCION')
	print()
	for fila in range(len(crucigrama)):
		print(crucigrama[fila][0])
	print()	

#-----------------
#Generación del crucigrama.

	
def imprimir_cruci(inventario_palabritas,horizontal,verticales):
	'''Recibe lo necesario para la creacion del crucigrama. Devuelve dicho crucigrama impreso sin soluciones.'''
	crucigrama = generar_crucigrama(horizontal,verticales)
	crucigrama_con_puntos = letras_por_puntos(crucigrama)
	crucigrama_con_indicadores = agregar_indicadores(crucigrama_con_puntos)
	imprimir_sin_soluciones(crucigrama_con_indicadores,verticales,horizontal,inventario_palabritas)

def imprimir_solu(inventario_palabritas,horizontal,verticales):
	'''Recibe lo necesario para la creacion del crucigrama. Devuelve las soluciones de dicho crucigrama.'''
	crucigrama = generar_crucigrama(horizontal,verticales)
	cruci_con_indicadores = agregar_indicadores(crucigrama)
	imprimir_solucion(cruci_con_indicadores)
		

		
main()

