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
    mapa_big = []
    if mapa != []:
        for columna_mapa in range(len(mapa)):
            mapa_small = []
            for fila_mapa in range(len(mapa[columna_mapa])):
                if mapa[columna_mapa][fila_mapa] == '.':
                    mapa_small.append(False)
                    continue
                elif mapa[columna_mapa][fila_mapa] == '#':
                    mapa_small.append(True)
                    continue
            mapa_big.append(mapa_small)
    return mapa_big

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
    mapa = []
    if not life == []:
        for columna_mapa in range(len(life)):
            cadena_mapa = ''
            for fila_mapa in range(len(life[columna_mapa])):
                if life[columna_mapa][fila_mapa] == False:
                    cadena_mapa += '.'
                if life[columna_mapa][fila_mapa] == True:
                    cadena_mapa += '#'
            mapa.append(cadena_mapa)
    return mapa

def pruebas_life_mostrar():
    """Prueba el correcto funcionamiento de life_mostrar()."""
    assert life_mostrar([]) == []
    assert life_mostrar([[False]]) == ['.']
    assert life_mostrar([[True]]) == ['#']
    assert life_mostrar([[True, False], [False, True]]) == ['#.', '.#']

#----------------------------------------------------------
def cant_adyacentes(life, f, c):
    """
    Calcula la cantidad de células vivas adyacentes a la celda en la fila `f` y la
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
            if valor:
                if ((f+i)%len(life)) == f and ((c+j)%len(life[0])) == c:
                    continue
                else:
                    cont_adyacentes += 1
#    print(cont_adyacentes)
#    if life[f][c-((len(life[f])-1))]:
#        cont_adyacentes += 1
#    if life[f][c-1]:
#        cont_adyacentes += 1
#    if life[f-((len(life))-1)][c]:
#        cont_adyacentes += 1
#    if life[f-((len(life))-1)][c-((len(life[f]))-1)]:
#        cont_adyacentes += 1
#    if life[f-((len(life))-1)][c-1]:
#        cont_adyacentes += 1
#    if life[f-1][c]:
#        cont_adyacentes += 1
#    if life[f-1][c-((len(life[f]))-1)]:
#        cont_adyacentes += 1
#    if life[f-1][c-1]:
#        cont_adyacentes += 1
    print(cont_adyacentes)
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

def celda_siguiente(life, f, c):
    """
    Calcula el estado siguiente de la celda ubicada en la fila `f` y la
    columna `c`.

    Devuelve True si en la celda (f, c) habrá una célula en la siguiente
    iteración, o False si la celda quedará vacía.
    * Una célula muerta con exactamente 3 células vecinas vivas "nace" (al turno
    siguiente estará viva).
    * Una célula viva con 2 ó 3 células vecinas vivas sigue viva, en otro caso
    muere o permanece muerta (por "soledad" o "superpoblación").
    """
    celda = life[f][c]
    n = cant_adyacentes(life, f, c)
    print(celda)
    if celda:
        if n == 2 or n == 3:
            return True
        return False
    elif not celda:
        if n == 3:
            return True
        return False

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
