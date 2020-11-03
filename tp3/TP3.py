import random
from pilotos import Piloto
from listaenlazada_pilas_colas import Pila,Cola,ListaEnlazada

PORCENTAJE_COMBINACION_MELEE = 40
PORCENTAJE_COMBINACION_RANGO = 25
#####################################################################################################################################
class Gunpla: 
	"""Representa un Gunpla. Un Gunpla esta compuesto de un Esqueleto, un conjunto de partes y un conjunto de armas."""
	def __init__(self,esqueleto,partes,armas):
		self.esqueleto = esqueleto
		self.partes = partes
		self.armas = armas
		self.energia = self.get_energia()
		self.energia_restante = self.energia
	
	def get_peso(self):
		"""Devuelve el peso total del Gunpla. Un Gunpla pesa lo que pesa la sumatoria de sus partes y armas"""
		peso_total = 0
		for arma in self.armas:
			peso_total += arma.get_peso()
		for parte in self.partes:
			peso_total += parte.get_peso()
		return peso_total
		
	def get_armadura(self):
		"""Devuelve la armadura total del Gunpla. Un Gunpla tiene tanta armadura como la sumatoria de la armadura de sus partes y armas"""
		armadura_total = 0
		for arma in self.armas:
			armadura_total += arma.get_armadura()
		for parte in self.partes:
			armadura_total += parte.get_armadura()
		return armadura_total

	def get_escudo(self):
		"""Devuelve el escudo total del Gunpla. Un Gunpla tiene tanto escudo como la sumatoria del escudo de sus partes y armas"""
		escudo_total = 0
		for arma in self.armas:
			escudo_total += arma.get_escudo()
		for parte in self.partes:
			escudo_total += parte.get_escudo()
		return escudo_total

	def get_velocidad(self):
		"""Devuelve la velocidad total del Gunpla. Un Gunpla tiene tanta velocidad como la sumatoria de las velocidades de sus partes y esqueleto"""
		velocidad_total = self.esqueleto.get_velocidad()
		for parte in self.partes:
			velocidad_total += parte.get_velocidad()
		return velocidad_total

	def	get_energia(self):
		"""Devuelve la energía total del Gunpla. Un Gunpla tiene tanta energía como la sumatoria de la energía de sus partes, armas y esqueleto"""
		energia_total = self.esqueleto.get_energia()
		for arma in self.armas:
			energia_total += arma.get_energia()
		for parte in self.partes:
			energia_total += parte.get_energia()
		self.energia = energia_total
		return energia_total

	def get_energia_restante(self):
		"""Devuelve la energía que le resta al Gunpla"""
		return self.energia_restante

	def	get_movilidad(self):
		"""Devuelve la movilidad de un Gunpla. Se calcula según la fórmula descripta en la seccion de fórmulas"""
		base = self.esqueleto.get_movilidad()
		peso = self.get_peso()
		velocidad = self.get_velocidad()
		movilidad = (base-peso/2 + velocidad*3)/base
		return movilidad

	def	get_armamento(self):
		"""Devuelve una lista con todas las armas adosadas al Gunpla (Se incluyen las armas disponibles en las partes)"""
		full_armas = self.armas[:]
		for parte in self.partes:
			if parte.get_armamento():
				full_armas += parte.get_armamento()
		return full_armas
	
	def modificar_energia(self,numero):
		""" Modifica la energia del Gunpla """
		if self.energia_restante - numero > self.energia:
			self.energia_restante = self.energia
		else:
			self.energia_restante -= numero


#####################################################################################################################################
class Esqueleto: 
	"""Representa el esqueleto interno del Gunpla."""
	def __init__(self,velocidad,energia,movilidad,slots):
		self.velocidad = velocidad
		self.energia = energia
		self.movilidad = movilidad
		self.slots = slots

	def	get_velocidad(self):
		"""Devuelve la velocidad del esqueleto. Es un valor fijo"""
		return self.velocidad

	def	get_energia(self):
		"""Devuelve la energía del esqueleto. Es un valor fijo"""
		return self.energia

	def	get_movilidad(self):
		"""Devuelve la movilidad del esqueleto. Es un valor fijo"""
		return self.movilidad

	def	get_cantidad_slots(self):
		"""Devuelve la cantidad de slots (ranuras) para armas que tiene el esqueleto. Es un valor fijo"""
		return self.slots


#####################################################################################################################################
class Parte: 
	"""Representa una parte de un Gunpla."""
	def __init__(self,peso,armadura,escudo,velocidad,energia,armamento,tipo):
		""" Crea una instancia de una Parte, recibe el peso, la armadura, escudo,velocidad,energia,armamento (lista que contiene 
			instancias de armas si es que la parte posee) y tipo"""
		self.peso = peso
		self.armadura = armadura
		self.escudo = escudo
		self.velocidad = velocidad
		self.energia = energia
		self.armamento = armamento
		self.tipo = tipo

	def	get_peso(self):	
		"""Devuelve el peso total de la parte. Una parte pesa lo que pesa la sumatoria de sus armas más el peso base de la parte"""
		peso = self.peso
		if self.armamento:
			for arma in self.armamento:
				peso += arma.get_peso()
			return peso
		return peso

	def	get_armadura(self):
		"""Devuelve la armadura total de la parte. Una parte tiene tanta armadura como la sumatoria de la armadura de sus armas más la armadura base de la parte"""
		armadura = self.armadura
		if self.armamento:
			for arma in self.armamento:
				armadura += arma.get_armadura()
			return armadura
		return armadura

	def	get_escudo(self):
		"""Devuelve el escudo total de la parte. Una parte tiene tanto escudo como la sumatoria del escudo de sus armas más el escudo base de la parte"""
		escudo = self.escudo
		if self.armamento:
			for arma in self.armamento:
				escudo += arma.get_escudo()
			return escudo
		return escudo

	def	get_velocidad(self):
		"""Devuelve la velocidad de la parte. Es un valor fijo"""
		return self.velocidad

	def	get_energia(self):
		"""Devuelve la energía total de la parte. La parte tiene tanta energía como la sumatoria de la energía de sus armas más la energía base de la parte"""
		energia = self.energia
		if not self.armamento:
			return energia
		for arma in self.armamento:
			energia += arma.get_energia()
		return energia

	def	get_armamento(self):
		"""Devuelve una lista con todas las armas adosadas a la parte"""
		return self.armamento

	def	get_tipo(self):
		"""Devuelve una cadena que representa el tipo de parte. Ej: "Backpack" """
		return str(self.tipo)


#####################################################################################################################################
class Arma: 
	"""Representa un arma."""
	def __init__(self,peso,armadura,escudo,velocidad,energia,municion,tipo,clase,daño,hits,precision,turnos_recarga):
		self.peso = peso
		self.armadura = armadura
		self.escudo = escudo
		self.velocidad = velocidad
		self.energia = energia
		self.municion = municion
		self.tipo = tipo
		self.clase = clase
		self.daño = daño
		self.hits = hits
		self.precision = precision
		self.turnos_recarga = turnos_recarga
		self.turno_usada = 0
		
		
	def	get_peso(self):
		"""Devuelve el peso del arma. Es un valor fijo"""
		return self.peso

	def	get_armadura(self):
		"""Devuelve la armadura del arma. Es un valor fijo"""
		return self.armadura

	def	get_escudo(self):
		"""Devuelve el escudo del arma. Es un valor fijo"""
		return self.escudo

	def	get_velocidad(self):
		"""Devuelve la velocidad del arma. Es un valor fijo"""
		return self.velocidad

	def	get_energia(self):
		"""Devuelve la energía del arma. Es un valor fijo"""
		return self.energia

	def get_tipo_municion(self):
		"""Devuelve el tipo de munición del arma: "FISICA"|"LASER"|"HADRON" """
		return self.municion

	def get_tipo(self):
		"""Devuelve el tipo del arma: "MELEE"|"RANGO" """
		return self.tipo

	def get_clase(self):	
		"""Devuelve la clase del arma, la cual es un string. Ejemplo "GN Blade" """
		return str(self.clase)

	def	get_daño(self):	
		"""Devuelve el daño de un ataque del arma. Es un valor fijo"""
		return self.daño

	def	get_hits(self):
		"""Devuelve la cantidad de veces que puede atacar un arma en un turno. Es un valor fijo"""
		return self.hits

	def	get_precision(self):
		"""Devuelve la precisión del arma"""
		return self.precision

	def	get_tiempo_recarga(self):
		"""Devuelve la cantidad de turnos que tarda un arma en estar lista"""
		return self.turnos_recarga

	def	esta_lista(self,turno_actual):
		"""Devuelve si el arma es capaz de ser utilizada en este turno o no"""
		if turno_actual - self.turnos_recarga >= self.turno_usada or self.turno_usada == 0:
			self.turno_usada = turno_actual
			return True
		return False

	def get_tipo_parte(self):
		"""Devuelve el tipo de parte de un arma. Siempre es "Arma" """
		return "Arma"

#####################################################################################################################################
#####################################################################################################################################
#####################################################################################################################################

def generador_esqueletos(n):
	"""
	Genera N instancias de la clase Esqueleto.
	Devuelve una lista con los esqueletos generados.
	"""
	lista_esqueletos = []
	for x in range (n):
		velocidad = random.randint(0, 100)
		energia = random.randint(750, 2500)
		movilidad = random.randint(100, 1000)
		slots = random.randint(1, 10)
		esqueleto = Esqueleto(velocidad,energia,movilidad,slots)
		lista_esqueletos.append(esqueleto)
	return lista_esqueletos

def generador_armas(n):
	"""
	Genera N instancias de la clase Arma.
	Devuelve una lista con las armas generadas.
	"""
	lista_armas = []
	for x in range (n):
		peso = random.randint(1,100)
		armadura = random.randint(-100,100)
		escudo = random.randint(-100,100)
		velocidad = random.randint(-100,100)
		energia = random.randint(-10,100)
		municion = random.choice(["FISICA","LASER","HADRON"])
		tipo = random.choice(["MELEE","RANGO"])
		clase = random.choice(["Arma1","Arma2","Arma3","Arma4","Arma5","Arma6","Arma7","Arma8","Arma9","Arma10"])
		daño = random.randint(1,600)
		hits = random.randint(1,10)
		precision = random.randint(1,10)
		turnos_recarga = random.randint(1,5)
		arma = Arma(peso,armadura,escudo,velocidad,energia,municion,tipo,clase,daño,hits,precision,turnos_recarga)
		lista_armas.append(arma)
	return lista_armas

def generador_partes(n):
	"""
	Genera N cantidad de instancias de Partes.
	Devuelve una lista con las partes generadas.
	"""
	lista_partes = []
	for x in range (n):
		peso = random.randint(1,100)
		armadura = random.randint(-100,100)
		escudo = random.randint(-100,100)
		velocidad = random.randint(-100,100)
		energia = random.randint(-10,100)
		armamento = random.choice([True,False])
		tipo = random.choice(["BACKPACK","ARM","CHEST","LEGS","FEET","HEAD"])
		if armamento:
			cantidad = random.randint(1,4)
			parte = Parte(peso,armadura,escudo,velocidad,energia,generador_armas(cantidad),tipo)
			lista_partes.append(parte)
			continue
		parte = Parte(peso,armadura,escudo,velocidad,energia,None,tipo)
		lista_partes.append(parte)
	return lista_partes

def separador(lista):
	"""
	Recibe una lista que es la suma de lista_armas y lista_partes y los separa por tipo. Devuelve un diccionario {tipo:Pila con una instancia de clase Parte}.
	"""
	inventario = {}
	for elem in lista:
		tipo = elem.get_tipo()
		inventario[tipo] = inventario.get(tipo,Pila())
		inventario[tipo].apilar(elem)
	return inventario

def generador_pilotos(n):
	"""
	Genera N cantidad de instancias de Piloto.
	Devuelve una lista con los pilotos generados.
	"""
	pilotos = []
	for x in range(n):
		piloto = Piloto()
		piloto.nombre = "Piloto" + str(x)
		pilotos.append(piloto)
	return pilotos

def asignar_esqueletos(pilotos,lista_esqueletos):
	"""
	Recibe todos los pilotos y la lista de esqueletos. Le asigna a cada piloto un esqueleto.
	"""
	for piloto in pilotos:
		piloto.elegir_esqueleto(lista_esqueletos)

def elegir(pilotos,inventario):
	"""
	Recibe la lista de todos los pilotos y el inventario (diccionario) de partes.
	Asigna a cada lista de partes de un piloto una parte elegida.
	"""
	random.shuffle(pilotos)
	while inventario:
		for piloto in pilotos:
			while inventario: #Sirve para garantizar la proxima linea
				tipo = piloto.elegir_parte(inventario)
				if not inventario[tipo].esta_vacia():
					objeto = inventario[tipo].desapilar()
					piloto.objetos.append(objeto)
					break
				else:
					inventario.pop(tipo)

def piloto_a_gunpla(pilotos):
	"""
	Asigna a cada Piloto una instancia de Gunpla, creada con las partes que el piloto eligió previamente.
	Devuelve la lista, ya en orden, de los pilotos para comenzar los turnos.
	"""
	for piloto in pilotos:
		armas,partes = piloto.armas_y_partes()
		piloto.set_gunpla(Gunpla(piloto.get_esqueleto(),partes,armas))
	pilotos_ordenados = quicksort(pilotos)
	return pilotos_ordenados[::-1]

def quicksort(lista):
	"""
	Recibe una lista de pilotos.
	Devuelve una lista con los pilotos ordenados por la velocidad de sus Gunplas
	"""
	if len(lista) < 2:
		return lista
	piloto_pivote = lista[0]
	pivote = piloto_pivote.get_gunpla().get_velocidad()
	menores = []
	mayores = []
	for i in range(1, len(lista)):
		elemento = lista[i].get_gunpla().get_velocidad()
		if elemento <= pivote:
			menores.append(lista[i])
		else:
			mayores.append(lista[i])

	return quicksort(menores) + [piloto_pivote] + quicksort(mayores)

#####################################################################################################################################

###################################### FÓRMULAS ######################################

def calculo_daño(arma):
	"""
	Recibe una instancia de arma y calcula el daño a realizar según la fórmula.
	Devuelve el valor que causa de daño el arma.
	"""
	daño_total = 0
	precision = arma.get_precision()
	usos = arma.get_hits()
	daño = arma.get_daño()
	probabilidad_de_extra = (25*precision)//10
	probabilidad_de_daño = precision*10
	for hits in range(usos):
		daño_si_no = generador_de_porcentajes(probabilidad_de_daño)
		extra = generador_de_porcentajes(probabilidad_de_extra)
		if daño_si_no:
			if extra:
				daño_total += (daño + int(daño*1.5))
			else:
				daño_total += daño
	return daño_total
		
def generador_de_porcentajes(numero):
	"""
	Recibe un porcentaje (número) y devuelve un booleano con la probabilidad del porcentaje recibido.
	"""
	"""
	#Manera flashera
	eleccion = int(numero)
	lista = [False]*(100-eleccion) + [True]*eleccion
	return random.choice(lista)
	"""
	eleccion = random.randint(0,100)
	return eleccion < int(numero)


def reduccion_daño_fisico(daño_recibido, gunpla):
	"""
	Recibe un daño recibido y un gunpla. Devuelve el daño luego de pasar por la reducción.
	'Reducción de daño físico:
	El daño reducido tiene un límite inferior de 0.'
	"""
	armadura = gunpla.get_armadura()
	daño = daño_recibido
	daño_reducido = daño - armadura
	if daño_reducido < 0:
		return 0
	return daño_reducido

def reduccion_daño_laser(daño_recibido, gunpla):
	"""
	Recibe un daño recibido y un gunpla. Devuelve el daño luego de pasar por la reducción.
	'Reducción de daño láser.
	El daño reducido no tiene límite. Si es negativo, implica que aumenta la energía del Gunpla.'
	"""
	daño = daño_recibido
	escudo = gunpla.get_escudo()
	daño_reducido = daño - ((daño*escudo)//10) #Modificado de la fórmula original porque sino los ataques se vuelven super exagerados (el dividido 10)
	return daño_reducido

###################################### FIN FÓRMULAS ######################################

def combinacion(arma_atacante):
	"""
	Recibe una instancia de arma. Devuelve si se puede volver a combinar o no.
	"""
	tipo = arma_atacante.get_tipo()
	if tipo == "MELEE":
		return generador_de_porcentajes(PORCENTAJE_COMBINACION_MELEE)
	else:
		return generador_de_porcentajes(PORCENTAJE_COMBINACION_RANGO)

def asginar_equipo(pilotos):
	"""
	Recibe una lista de pilotos y le asigna a cada uno un equipo.
	Solo existen 2 equipos posibles.
	"""
	maximo_de_miembros = len(pilotos)//2
	miembros = 0
	for piloto in pilotos:
		if miembros < maximo_de_miembros:
			piloto.equipo = 1
			miembros += 1
		else:
			piloto.equipo = 2

def validador_arma_combinada(arma_principal,arma_a_combinar,turno):
	"""
	Recibe un arma y verifica si es apta o no para ser combinada con el arma principal.
	"""
	return arma_principal.get_tipo()==arma_a_combinar.get_tipo() and arma_principal.get_clase()==arma_a_combinar.get_clase() and arma_principal.get_clase()==arma_a_combinar.get_clase() and arma_principal.get_tipo_municion() == arma_a_combinar.get_tipo_municion() and arma_a_combinar.esta_lista(turno)
	
def ataque(piloto,arma,turno,oponente):
	'''
	Recibe piloto, oponente y arma atacante y genera un ataque siguiendo las reglas. Devuelve el daño a aplicar en la ejecución del ataque.
	'''
	armas_extras = piloto.armas
	cantidad_armas = len(armas_extras)
	contador = 1
	armas_no_validas = []
	arma_inicial = arma
	daño = calculo_daño(arma_inicial)
	combina = combinacion(arma_inicial)
	while combina and contador < cantidad_armas:
		arma = piloto.elegir_arma(oponente)
		while arma_inicial != arma and arma not in armas_no_validas:
			if validador_arma_combinada(arma_inicial,arma,turno):
				print("VA A COMBINAR!!!")
				daño += calculo_daño(arma)
				combina = combinacion(arma)
				armas_no_validas.append(arma)
				break #Lo manda al primer while y repite todo hasta que se quede sin armas combinables
			else:
				armas_no_validas.append(arma)
				contador += 1
		combina = combinacion(arma_inicial)
	return daño
		
def ejecucion_de_ataque(arma_atacante,daño_a_efectuar,oponente,ColaTurnos):
	'''
	Recibe arma atacante, daño a efectuar, oponente y la cola de turnos. Aplica el daño proporcionado por la función 'ataque'.
	'''
	evade,daño = obtener_valores_ataque(arma_atacante,oponente,daño_a_efectuar)
	if evade:
		print("EVADIÓ!!!")
		ColaTurnos.encolar(oponente)
		return
	else:
		if daño == 0:
			ColaTurnos.encolar(oponente)
		else:
			if not arma_atacante.get_tipo_municion() == 'HADRON':
				print("Despues de la reducción, el oponente -{}- recibe {} daño.".format(oponente.nombre,daño))
				oponente.get_gunpla().modificar_energia(daño)

def ejecutar_turnos(pilotos_ordenados):
	"""
	Ejecuta el juego por turnos. Recibe una lista de pilotos ordenados por velocidad de sus gunpla. Devuelve la misma lista pero sólamente con el ganador.
	"""
	ColaTurnos = creacion_cola_turnos(pilotos_ordenados)
	turno_actual = 1
	while not ColaTurnos.esta_vacia() and len(pilotos_ordenados) > 1:
		piloto = proximo_turno_piloto(turno_actual,ColaTurnos)
		if piloto.get_gunpla().get_energia_restante() <= 0:
			print("No puede atacar porque ya está muerto ―(x_x)→")
		if piloto.get_gunpla().get_energia_restante() > 0: #Verifica si puede jugar, si es mayor a 0, juega!
			copia = pilotos_ordenados[::]
			print_pilotos_restantes(copia)
			copia.remove(piloto)
			if not copia:
				break
			oponente = piloto.elegir_oponente(copia,piloto)
			arma_disponible,arma_atacante = armita_disponible(piloto,oponente,turno_actual)
			if not oponente:
				break
			if arma_disponible:
				ataque_completo(piloto,arma_atacante,turno_actual,oponente,ColaTurnos,pilotos_ordenados)
		else:
			if piloto not in pilotos_ordenados:
				continue
			else:
				print("Este piloto se murió: -{}-".format(piloto.nombre))
				pilotos_ordenados.remove(piloto)
				continue
		
		if oponente.get_gunpla().get_energia_restante() <= 0:
				print("Este piloto se murió: -{}-".format(oponente.nombre))
				pilotos_ordenados.remove(oponente)
		else:
			ColaTurnos.encolar(piloto)
			copia.append(piloto)
		print("Finalizó el turno N°{}".format(turno_actual))
		print("--------------------------------------------")
		turno_actual += 1
	print_pilotos_restantes_final(pilotos_ordenados)
	return pilotos_ordenados

#######################################Funciones que se usan en Turnos#############################################

def creacion_cola_turnos(pilotos_ordenados):
	ColaTurnos = Cola()
	for piloto in pilotos_ordenados:
		ColaTurnos.encolar(piloto)
	return ColaTurnos

def ataque_completo(piloto,arma_atacante,turno_actual,oponente,ColaTurnos,pilotos_ordenados):
	daño_a_efectuar = ataque(piloto,arma_atacante,turno_actual,oponente)
	print("El atacante -{}- del equipo -{}- le hará {} daño a -{}- del equipo -{}- ლ(ಠ_ಠლ) Usando Arma tipo {} con munición {}.".format(piloto.nombre,piloto.equipo,daño_a_efectuar,oponente.nombre,oponente.equipo,arma_atacante.tipo,arma_atacante.municion))
	ejecucion_de_ataque(arma_atacante,daño_a_efectuar,oponente,ColaTurnos)
	if oponente.get_gunpla().get_energia_restante() < 0 and abs(oponente.get_gunpla().get_energia_restante() * 20) >= oponente.gunpla.get_energia():
		print("OVERKILL!!!")
		ColaTurnos.encolar(piloto)
	if arma_atacante.get_tipo() == 'MELEE':
		if oponente.get_gunpla().get_energia_restante() < 0:
			print("El oponente -{}- contraatacaría pero no tiene energía.".format(oponente.nombre))
		else:
			print("El oponente -{}- va a contraatacar al atacante -{}-.".format(oponente.nombre,piloto.nombre))
			contraataque(piloto,oponente,daño_a_efectuar,turno_actual,pilotos_ordenados)

def print_pilotos_restantes(copia):
	copia_para_printear = []
	for x in range(len(copia)):
		copia_para_printear.append(copia[x].nombre)
	print("Pilotos restantes vivos: {}".format(copia_para_printear))

def armita_disponible(piloto,oponente,turno_actual):
	contador1 = 0
	arma_disponible = False
	while contador1 < len(piloto.armas):
		arma_atacante = piloto.elegir_arma(oponente)
		if arma_atacante.esta_lista(turno_actual):
			arma_disponible = True
			return arma_disponible,arma_atacante
		else:
			contador1 += 1
	return arma_disponible,arma_atacante

def print_pilotos_restantes_final(pilotos_ordenados):
	copia_para_printear_final = []
	for x in range(len(pilotos_ordenados)):
		copia_para_printear_final.append(pilotos_ordenados[x].nombre)
	print("And the winner team is: Equipo -{}-, con {} como sobreviviente/s!".format(pilotos_ordenados[0].equipo,copia_para_printear_final))


def proximo_turno_piloto(turno_actual,ColaTurnos):
	print("Turno N°{}".format(turno_actual))
	piloto = ColaTurnos.desencolar()	
	print("Es el turno de -{}- del equipo -{}- y tiene {} energía para atacar de su total {}.".format(piloto.nombre,piloto.equipo,piloto.gunpla.get_energia_restante(),piloto.gunpla.energia))
	return piloto

#######################################FIN Funciones que se usan en Turnos#############################################

def contraataque(piloto,oponente,daño_a_efectuar,turno,pilotos_ordenados):
	"""
	Recibe piloto, oponente, daño a efectuar, turno actual y lista de pilotos_ordenados actual. Evalúa si el oponente puede contraatacar, de ser así
	aplica el daño de la misma manera que en la ejecución de ataque, teniendo en cuenta las reglas que aplican al contraataque.
	"""
	usadas = []
	armas = oponente.armas
	armas_contraataque = len(armas)
	contador2 = 0
	contraataca = False
	if oponente.get_gunpla().get_energia_restante() > 0:
		while contador2 < armas_contraataque:
			arma_atacante_oponente = oponente.elegir_arma(piloto)
			if arma_atacante_oponente.esta_lista(turno) and arma_atacante_oponente not in usadas:
				contraataca = True #Tiene arma para contraatacar!
				break
			else:
				usadas.append(arma_atacante_oponente)
				contador2 += 1
		ejecucion_contraataque(piloto,oponente,daño_a_efectuar,pilotos_ordenados,contraataca,arma_atacante_oponente)



def ejecucion_contraataque(piloto,oponente,daño_a_efectuar,pilotos_ordenados,contraataca,arma_atacante_oponente):
	"""
	Verifica si es posible realizar un contraataque, en caso de True, ejecuta el ataque.
	"""
	if contraataca: #Si consiguio arma disponible entra, sino no tenia con que
		evade,daño = obtener_valores_ataque(arma_atacante_oponente,piloto,daño_a_efectuar)
		if evade:
			print("EVADIÓ!!!")
			piloto.get_gunpla().modificar_energia(0)
		else:
			print("El oponente -{}- contraataca por {} daño".format(oponente.nombre,daño))
			piloto.get_gunpla().modificar_energia(daño)
			if piloto.get_gunpla().energia_restante < 0:
				print("Este piloto se murió: -{}-".format(piloto.nombre))
				pilotos_ordenados.remove(piloto)

def obtener_valores_ataque(arma_que_ataca,piloto_u_oponente,daño_a_efectuar):
	if arma_que_ataca.get_tipo_municion() == 'FISICA':
		daño = reduccion_daño_fisico(daño_a_efectuar,piloto_u_oponente.get_gunpla())
	elif arma_que_ataca.get_tipo_municion() == 'LASER':
		daño = reduccion_daño_laser(daño_a_efectuar,piloto_u_oponente.get_gunpla())
	else:
		daño = daño_a_efectuar
	movilidad = piloto_u_oponente.get_gunpla().get_movilidad()
	evade = generador_de_porcentajes((80*movilidad)//10)
	return evade,daño


def main(n,m,o,p):
	"""
	Simulador de batallas de gunplas!
	"""
	pilotos = generador_pilotos(n)
	asginar_equipo(pilotos)
	armas = generador_armas(m)
	partes = generador_partes(o)
	esqueletos = generador_esqueletos(p)
	armas_y_partes = separador(armas+partes)
	asignar_esqueletos(pilotos,esqueletos)
	elegir(pilotos,armas_y_partes)
	pilotos_ordenados = piloto_a_gunpla(pilotos)
	ejecutar_turnos(pilotos_ordenados)


main(10,50,50,50) #Pilotos, armas, partes, esqueletos
	
