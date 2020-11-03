import random
#########################################################################################################################################################
##########       #####  ######  ###########         #####        #####        #####        ##############################################################
##########  ###  #####  ######  ###########  #####  ########  ########  ####  #####  ####################################################################
##########       #####  ######  ###########  #####  ########  ########  ####  #####        ##########                                     ###############
##########  ##########  ######  ###########  #####  ########  ########  ####  ###########  #############################################  ###############
##########  ##########  ######        #####         ########  ########        #####        #########################################  ##  ##  ###########
######################################################################################################################################      #############
																																		##

class Piloto():
	def __init__(self):
		"""Crea un piloto y no recibe ningun parámetro"""
		self.gunpla = None
		self.objetos = []
		self.esqueleto = None
		self.armas = []
		self.nombre = ""
		self.equipo = 0

	def set_gunpla(self,gunpla):
		"""Asigna un Gunpla a un piloto"""
		self.gunpla = gunpla

	def get_gunpla(self):
		"""Devuelve el Gunpla asociado al piloto"""
		return self.gunpla

	def elegir_esqueleto(self,lista_esqueletos):
		""""Dada una lista con esqueletos, devuelve el índice del esqueleto a utilizar"""
		valores = [x for x in range(0,len(lista_esqueletos))]
		indice = random.choice(valores)
		self.esqueleto = lista_esqueletos[indice]
		return indice
	
	def get_esqueleto(self):
		""" Devuelve el esqueleto asocidado a un gunpla """
		return self.esqueleto

	def elegir_parte(self,partes_disponibles):
		"""Dado un diccionario: {tipo_parte:parte}, devuelve el tipo de parte que quiere elegir.
			Este metodo se utiliza para ir eligiendo de a una las partes que se van a reservar para cada piloto, de entre las cuales va a poder elegir para armar su modelo.
			Elige con mayor prioridad las partes Rango y Chest."""
		tipos = [x for x in partes_disponibles]
		disponibles_mayor_prioridad = []
		disponibles_menor_prioridad = []
		for tipo in tipos:
			if tipo == "RANGO" or tipo == "CHEST":
				disponibles_mayor_prioridad.append(tipo)
			else:
				disponibles_menor_prioridad.append(tipo)
		if len(disponibles_mayor_prioridad) > 0:
			return random.choice(disponibles_mayor_prioridad)
		return random.choice(disponibles_menor_prioridad)

	def elegir_combinacion(self,partes_reservadas):
		"""Dada una lista con partes previamente reservadas, devuelve una lista con las partes a utilizar para construir el Gunpla. 
			Este metodo se utiliza para elegir las partes que se van a utilizar en el modelo de entre las que se reservaron previamente para cada piloto."""
		espacio_libre = self.esqueleto.get_cantidad_slots()
		contador = 0
		partes_elegidas = []
		tipos_elegidos = []
		for elem in partes_reservadas:
			if espacio_libre > contador and elem.get_tipo() == "ARMA":
				partes_elegidas.append(elem)
				contador += 1
			else:
				if not elem.get_tipo() in tipos_elegidos:
					partes_elegidas.append(elem)
					tipos_elegidos.append(elem.get_tipo())
		self.objetos = partes_elegidas			
		return self.objetos

	def elegir_oponente(self,oponentes,piloto):
		"""Devuelve el índice del Gunpla al cual se decide atacar de la lista de oponentes pasada"""
		for oponente in oponentes:
			if oponente.equipo == piloto.equipo:
				oponentes.remove(oponente)
		if len(oponentes) == 0:
			return False
		minimo_escudo = [1000000,None]
		for oponente in oponentes:
			if oponente.get_gunpla().get_escudo() < minimo_escudo[0]:
				minimo_escudo = [oponente.get_gunpla().get_escudo(),oponente]
		return minimo_escudo[1]
	
	def elegir_arma(self,oponente):
		"""Devuelve el arma con la cual se decide atacar al oponente"""
		armas = self.armas
		maximo = [0,None]
		for arma in armas:
			daño = arma.daño
			if daño > maximo[0]:
				maximo = [daño,arma]
		return maximo[1]

	def get_partes(self):
		"""Devuelve la lista de partes previamente seleccionadas"""
		return self.objetos

	def armas_y_partes(self):
		"""Devuelve una lista de las armas elegidas por el piloto para su gunpla, y una lista de partes elegida
			por el piloto para su gunpla"""
		armas = []
		partes = []
		for elem in self.objetos:
			if elem.get_tipo() == "MELEE" or elem.get_tipo() == "RANGO":
				armas.append(elem)
			else:
				partes.append(elem)
		self.armas = armas
		return armas,partes

																																		##
######################################################################################################################################      #############
##########       #####  ######  ###########         #####        #####        #####        #########################################  ##  ##  ###########
##########  ###  #####  ######  ###########  #####  ########  ########  ####  #####  ###################################################  ###############
##########       #####  ######  ###########  #####  ########  ########  ####  #####        ##########                                     ###############
##########  ##########  ######  ###########  #####  ########  ########  ####  ###########  ##############################################################
##########  ##########  ######        #####         ########  ########        #####        ##############################################################
#########################################################################################################################################################

