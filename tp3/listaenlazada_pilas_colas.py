#------------------------PILAS Y COLAS---------------------------------

class Pila:
	"""Representa una pila con operaciones de apilar, desapilar y
	verificar si está vacía."""
	def __init__(self):
		"""Crea una pila vacía."""
		self.items = []
	#El método esta_vacia simplemente se fija si la lista de Python está vacía:
	def esta_vacia(self):
		"""Devuelve True si la lista está vacía, False si no."""
		return len(self.items) == 0
	#El método apilar agrega el nuevo elemento al final de la lista:
	def apilar(self, x):
		"""Apila el elemento x."""
		self.items.append(x)
	#Para implementar desapilar se usamos el método pop de lista que hace exactamente lo re-
	#querido: elimina el último elemento de la lista y devuelve el valor del elemento eliminado. Si la
	#lista está vacía desapilar lanza una excepción.
	def desapilar(self):
		"""Devuelve el elemento tope y lo elimina de la pila.
		Si la pila está vacía levanta una excepción."""
		if self.esta_vacia():
			raise IndexError("La pila está vacía")
		return self.items.pop()

class Cola:
	def __init__(self):
		"""Crea una cola vacía."""
		self.primero = None
		self.ultimo = None
	def encolar(self, x):
		"""Encola el elemento x."""
		nuevo = _Nodo(x,None)
		if self.ultimo is not None:
			self.ultimo.prox = nuevo
			self.ultimo = nuevo
		else:
			self.primero = nuevo
			self.ultimo = nuevo
	def desencolar(self):
		"""Desencola el primer elemento y devuelve su valor.
		Si la cola está vacía, levanta ValueError."""
		if self.primero is None:
			raise ValueError("La cola está vacía")
		valor = self.primero.dato
		self.primero = self.primero.prox
		if not self.primero:
			self.ultimo = None
		return valor
	def esta_vacia(self):
		"""Devuelve True si la cola esta vacía, False si no."""
		return self.primero is None


#------------------------LISTA ENLAZADA---------------------------------

class _Nodo:
	def __init__(self,dato,prox):
		self.dato = dato
		self.prox = prox
		self.ant = None

class ListaEnlazada:
	'''
	'''
	def __init__(self):
		self.prim = None
		self.len = 0
		self.ult = 0
	def __str__(self):
		nodo = self.prim
		cadena = '['
		sep = ''
		while nodo:
			cadena += sep + repr(nodo.dato)
			sep = ', '
			nodo = nodo.prox
		return (cadena + ']')
	def extend(self,l2):
		nodo = self.prim
		while nodo and nodo.prox:
			nodo = nodo.prox
		n_l2 = l2.prim
		if not nodo and n_l2: #esto es append
			self.prim = _Nodo(n_l2.dato,None)
			n_l2 = n_l2.prox
			nodo = self.prim
		while n_l2:
			nuevo = _Nodo(n_l2.dato,None)
			nodo.prox = nuevo
			nodo = nodo.prox
			n_l2 = n_l2.prox		
	def append(self,dato):
		act = self.prim
		nuevo = _Nodo(dato,None)
		if not act:
			self.prim = nuevo
		else:
			while act.prox:
				act = act.prox
			act.prox = nuevo
		self.len += 1
	def __len__(self):
		return self.len
	def pop(self, i=None):
		'''Elimina el nodo de la posicion i, y devuelve el dato contenido. Si i esta fuera de rango, se levanta la excepcion IndexError. Si no se recibe la posicion, devuelve el ultimo elemento.'''
		if i is None:
			i = self.len -1
		if i < 0 or i >= self.len:
			raise IndexError('Indice fuera de rango')
		if i == 0:
			#Caso particular: saltear la cabecera de la lista
			dato = self.prim.dato
			self.prim = self.prim.prox
		else:
			#Buscar los nodos en las posicionnes (i-1) e (i)
			ant = self.prim
			actual = ant.prox
			for pos in range(1,i):
				ant = ant
				actual = ant.prox
			#Guardar el dato y descartar el nodo
			dato = actual.dato
			ant.prox = actual.prox
		self.len -= 1
		return dato
	def remove(self, x):
		"""Borra la primera aparición del valor x en la lista.
		Si x no está en la lista, levanta ValueError"""
		if self.len == 0:
			raise ValueError("Lista vacía")

		if self.prim.dato == x:
			# Caso particular: saltear la cabecera de la lista
			self.prim = self.prim.prox
		else:
			# Buscar el nodo anterior al que contiene a x (n_ant)
			n_ant = self.prim
			n_act = n_ant.prox
			while n_act is not None and n_act.dato != x:
				n_ant = n_act
				n_act = n_ant.prox
			if n_act == None:
				raise ValueError("El valor no está en la lista.")
			# Descartar el nodo
			n_ant.prox = n_act.prox
		self.len -= 1
	def insert(self, i, x):
		"""Inserta el elemento x en la posición i.
		Si la posición es inválida, levanta IndexError"""
		if i < 0 or i > self.len:
			raise IndexError("Posición inválida")
		nuevo = _Nodo(x,None)
		if i == 0:
			# Caso particular: insertar al principio
			nuevo.prox = self.prim
			self.prim = nuevo
		else:
			# Buscar el nodo anterior a la posición deseada
			n_ant = self.prim
			for pos in range(1, i):
				n_ant = n_ant.prox
			# Intercalar el nuevo nodo
			nuevo.prox = n_ant.prox
			n_ant.prox = nuevo
			self.len += 1
	def remover_todos(self,elem):
		'''Recibe un elemento. Remueve de la lista todas las apariciones del mismo. Devuelve la cantidad de elementos removidos.'''
		nodo = self.prim
		while nodo and nodo.dato == elem:
			self.prim = nodo.prox
			nodo = self.prim
		while nodo and nodo.prox:
			if nodo.prox.dato == elem:
				nodo.prox = nodo.prox.prox
				continue		
			nodo = nodo.prox
	def duplicar(self,elemento):
		'''Duplica las apariciones del elemento pasado por parametro en la lista'''
		nodo = self.prim
		while nodo:
			if nodo.dato == elemento:
				nuevo = _Nodo(elemento,None)
				aux = nodo.prox
				nuevo.prox = aux
				nodo.prox = nuevo
				nodo = aux
				continue
			nodo = nodo.prox
	def __iter__(self):
		return _IteradorLE(self.prim)	

class _IteradorLE:
	def __init__(self,primero):
		self.actual = primero	
	def __next__(self):
		if not self.actual:
			raise StopIteration()
		dato = self.actual.dato
		self.actual = self.actual.prox
		return dato

class ListaCircular:
	def __init__(self):
		self.prim = None
	def append(self,elem):
		nodo_nuevo = _Nodo(elem,None)
		if not self.prim:
			self.prim = nodo_nuevo
			self.prim.prox = self.prim
		else:
			nodo = self.prim
			while nodo.prox != self.prim:
				nodo = nodo.prox
			nodo.prox = nodo_nuevo
			nodo_nuevo.prox = self.prim
