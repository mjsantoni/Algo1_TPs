#Algoritmos y programación I.
#Cátedra: Essaya.
#Práctica: Grace.
#Nombre: Mauro Javier Santoni.
#Padrón: 102654.
#Corrector: Juan Patricio Marshall.

"""
Conway's Game of Life
---------------------

https://es.wikipedia.org/wiki/Juego_de_la_vida

El "tablero de juego" es una malla formada por cuadrados ("células") que se
extiende por el infinito en todas las direcciones. Cada célula tiene 8 células
vecinas, que son las que están próximas a ella, incluidas las diagonales. Las
células tienen dos estados: están "vivas" o "muertas" (o "encendidas" y
"apagadas"). El estado de la malla evoluciona a lo largo de unidades de tiempo
discretas (se podría decir que por turnos). El estado de todas las células se
tiene en cuenta para calcular el estado de las mismas al turno siguiente.
Todas las células se actualizan simultáneamente.

Las transiciones dependen del número de células vecinas vivas:

* Una célula muerta con exactamente 3 células vecinas vivas "nace" (al turno
  siguiente estará viva).
* Una célula viva con 2 ó 3 células vecinas vivas sigue viva, en otro caso
  muere o permanece muerta (por "soledad" o "superpoblación").
"""

def main():
    """
    Función principal del programa. Crea el estado inicial de Game of LIfe
    y muestra la simulación paso a paso mientras que el usuaio presione
    Enter.
    """
    life = life_crear([
        '..........',
        '..........',
        '..........',
        '.....#....',
        '......#...',
        '....###...',
        '..........',
        '..........',
    ])
    while True:
        for linea in life_mostrar(life):
            print(linea)
        print()
        input("Presione Enter para continuar, CTRL+C para terminar")
        print()
        life = life_siguiente(life)

#-----------------------------------------------------------------------------

def life_crear(mapa):
    """
    Crea el estado inicial de Game of life a partir de una disposición
    representada con los caracteres '.' y '#'.

    `mapa` debe ser una lista de cadenas, donde cada cadena representa una
    fila del tablero, y cada caracter puede ser '.' (vacío) o '#' (célula).
    Todas las filas deben tener la misma cantidad decaracteres.

    Devuelve el estado del juego, que es una lista de listas donde cada
    sublista representa una fila, y cada elemento de la fila es False (vacío)
    o True (célula).
    """
    estado_del_juego = []
    if mapa != []:
        for i in range(len(mapa)):
            sublista_aux = []
            for j in range(len(mapa[0])):
                sublista_aux.append(mapa[i][j] == '#')
            estado_del_juego.append(sublista_aux)
    return estado_del_juego

def pruebas_life_crear():
    """Prueba el correcto funcionamiento de life_crear()."""
    # Para cada prueba se utiliza la instrucción `assert <condición>`, que
    # evalúa que la <condición> sea verdadera, y lanza un error en caso
    # contrario.
    assert life_crear([]) == []
    assert life_crear(['.']) == [[False]]
    assert life_crear(['#']) == [[True]]
    assert life_crear(['#.', '.#']) == [[True, False], [False, True]]

#-----------------------------------------------------------------------------

def life_mostrar(life):
    """
    Crea una representación del estado del juego para mostrar en pantalla.

    Recibe el estado del juego (inicialmente creado con life_crear()) y
    devuelve una lista de cadenas con la representación del tablero para
    mostrar en la pantalla. Cada una de las cadenas representa una fila
    y cada caracter debe ser '.' (vacío) o '#' (célula).
    """
    representacion_tablero = []
    if not life == []:
        for i in range(len(life)):
            cadena_tablero = ''
            for j in range(len(life[0])):
                if life[i][j]:
                    cadena_tablero += '#'
                else:
                    cadena_tablero += '.'
            representacion_tablero.append(cadena_tablero)
    return representacion_tablero

def pruebas_life_mostrar():
    """Prueba el correcto funcionamiento de life_mostrar()."""
    assert life_mostrar([]) == []
    assert life_mostrar([[False]]) == ['.']
    assert life_mostrar([[True]]) == ['#']
    assert life_mostrar([[True, False], [False, True]]) == ['#.', '.#']

#-----------------------------------------------------------------------------

def cant_adyacentes(life, f, c):
    """
    Calcula la cantidad de células adyacentes a la celda en la fila `f` y la
    columna `c`.

    Importante: El "tablero" se considera "infinito": las celdas del borde
    izquierdo están conectadas a la izquierda con las celdas del borde
    derecho, y viceversa. Las celdas del borde superior están conectadas hacia
    arriba con las celdas del borde inferior, y viceversa.
    """
    cont_adyacentes = 0
    for i in range(-1,2):
        for j in range(-1,2):
            valor = life[(f+i)%len(life)][(c+j)%len(life[0])]
            if valor and not (((f+i)%len(life)) == f and ((c+j)%len(life[0])) == c):
                cont_adyacentes += 1
    return cont_adyacentes

def pruebas_cant_adyacentes():
    """Prueba el correcto funcionamiento de cant_adyacentes()."""
    assert cant_adyacentes(life_crear(['.']), 0, 0) == 0
    assert cant_adyacentes(life_crear(['..', '..']), 0, 0) == 0
    assert cant_adyacentes(life_crear(['..', '..']), 0, 1) == 0
    assert cant_adyacentes(life_crear(['##', '..']), 0, 0) == 2
    assert cant_adyacentes(life_crear(['##', '..']), 0, 1) == 2
    assert cant_adyacentes(life_crear(['#.', '.#']), 0, 0) == 4
    assert cant_adyacentes(life_crear(['##', '##']), 0, 0) == 8
    assert cant_adyacentes(life_crear(['.#.', '#.#', '.#.']), 1, 1) == 4
    assert cant_adyacentes(life_crear(['.#.', '..#', '.#.']), 1, 1) == 3
    assert cant_adyacentes(life_crear(['...', '.#.', '...']), 1, 1) == 0

#-----------------------------------------------------------------------------

def celda_siguiente(life, f, c):
    """
    Calcula el estado siguiente de la celda ubicada en la fila `f` y la
    columna `c`.

    Devuelve True si en la celda (f, c) habrá una célula en la siguiente
    iteración, o False si la celda quedará vacía.
    """
    celda = life[f][c]
    n = cant_adyacentes(life, f, c)
    if celda:
        return n == 2 or n == 3
    return n == 3

def pruebas_celda_siguiente():
    """Prueba el correcto funcionamiento de celda_siguiente()."""
    assert celda_siguiente(life_crear(['.']), 0, 0) == False
    assert celda_siguiente(life_crear(['..', '..']), 0, 0) == False
    assert celda_siguiente(life_crear(['..', '..']), 0, 1) == False
    assert celda_siguiente(life_crear(['##', '..']), 0, 0) == True
    assert celda_siguiente(life_crear(['##', '..']), 0, 1) == True
    assert celda_siguiente(life_crear(['#.', '.#']), 0, 0) == False
    assert celda_siguiente(life_crear(['##', '##']), 0, 0) == False
    assert celda_siguiente(life_crear(['.#.', '#.#', '.#.']), 1, 1) == False
    assert celda_siguiente(life_crear(['.#.', '..#', '.#.']), 1, 1) == True
    assert cant_adyacentes(life_crear(['...', '.#.', '...']), 1, 1) == False

#-----------------------------------------------------------------------------

def life_siguiente(life):
    """
    Calcula el siguiente estado del juego.

    Recibe el estado actual del juego (lista de listas de False/True) y
    devuelve un _nuevo_ estado que representa la siguiente iteración según las
    reglas del juego.

    Importante: El "tablero" se considera "infinito": las celdas del borde
    izquierdo están conectadas a la izquierda con las celdas del borde
    derecho, y viceversa. Las celdas del borde superior están conectadas hacia
    arriba con las celdas del borde inferior, y viceversa.
    """
    siguiente = []
    for f in range(len(life)):
        fila = []
        for c in range(len(life[0])):
            fila.append(celda_siguiente(life, f, c))
        siguiente.append(fila)
    return siguiente

#-----------------------------------------------------------------------------

def pruebas():
    """Ejecuta todas las pruebas"""
    pruebas_life_crear()
    pruebas_life_mostrar()
    pruebas_cant_adyacentes()
    pruebas_celda_siguiente()

pruebas()
main()
