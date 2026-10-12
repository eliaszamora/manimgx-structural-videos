"""Guion y reloj compartidos entre ManimGX y el narrador. Segundos por capítulo."""
BEATS = [
    {
        "id": "01",
        "duration": 20,
        "heading": "LA PREGUNTA",
        "caption": "Una fuerza descendente sobre una viga en voladizo",
        "narration": "Observa esta viga. Está empotrada a la izquierda y recibe una fuerza vertical hacia abajo en el extremo libre. Antes de dibujar nada, preguntémonos: ¿qué partes pueden moverse, y qué forma tiene que adoptar para cumplir las restricciones?",
    },
    {
        "id": "02",
        "duration": 22,
        "heading": "PRIMERO: LAS RESTRICCIONES",
        "caption": "En el empotramiento: desplazamiento cero y giro cero",
        "narration": "En el empotramiento, la viga no puede desplazarse verticalmente, ni puede girar. Por tanto, la deformada nace exactamente en la posición original y arranca con tangente horizontal. El extremo libre, en cambio, sí puede descender y girar. Esta diferencia explica por qué la viga no baja como un bloque rígido.",
    },
    {
        "id": "03",
        "duration": 23,
        "heading": "LUEGO: LA DEFORMADA",
        "caption": "La pendiente parte de cero y aumenta su magnitud",
        "narration": "La fuerza tira del extremo hacia abajo. Como el empotramiento mantiene fija la inclinación inicial, la viga debe curvarse gradualmente. Cerca del apoyo, la pendiente es pequeña; hacia la punta se vuelve más negativa. La flecha es mayor al final. Esto no implica un quiebre ni una rótula: la curva debe ser suave.",
    },
    {
        "id": "04",
        "duration": 21,
        "heading": "¿POR QUÉ ESTA CURVATURA?",
        "caption": "El momento se relaciona con la curvatura: M = E I · v''",
        "narration": "La concavidad de esta curva es hacia abajo: su segunda derivada es negativa. Para una viga de Euler Bernoulli, el momento flector es E por I multiplicado por esa curvatura. Por eso el momento interno también resulta negativo. La curvatura es más intensa junto al empotramiento y disminuye hacia el extremo libre.",
    },
    {
        "id": "05",
        "duration": 23,
        "heading": "COMPROBARLO CON EQUILIBRIO",
        "caption": "Aísla el tramo derecho: la fuerza P tiene un brazo L − x",
        "narration": "Para entender el signo sin memorizarlo, cortemos la viga en una sección y aislemos la parte derecha. La carga hacia abajo tiende a hacer girar ese tramo en sentido horario alrededor del corte. Entonces el momento interno que la equilibra debe actuar en sentido antihorario. Con nuestra convención, ese momento es negativo, y vale menos P por L menos x.",
    },
    {
        "id": "06",
        "duration": 22,
        "heading": "DIBUJAR EL MOMENTO",
        "caption": "M(x) = −P(L − x)   |   negativo sobre el eje",
        "narration": "En el extremo libre no queda brazo: el momento es cero. Junto al empotramiento, el brazo es L y la magnitud es máxima: P por L. Entre ambos puntos cambia linealmente. El diagrama es, por tanto, triangular. Como hemos acordado representar los momentos positivos bajo la línea, este momento negativo se dibuja sobre ella.",
    },
    {
        "id": "07",
        "duration": 21,
        "heading": "Y AHORA EL CORTANTE",
        "caption": "V(x) = +P   |   positivo y constante",
        "narration": "El cortante sale directamente del equilibrio vertical del tramo derecho. La carga exterior apunta hacia abajo; por tanto, la fuerza interna de corte en la cara izquierda debe apuntar hacia arriba. Eso corresponde a cortante positivo, igual a P. Como no hay cargas distribuidas a lo largo de la viga, se mantiene constante.",
    },
    {
        "id": "08",
        "duration": 17,
        "heading": "UNA LÓGICA, TRES DIBUJOS",
        "caption": "Restricciones → deformada → momento → cortante",
        "narration": "Recapitulemos. Primero, las restricciones fijan el comienzo de la deformada. Después, la carga y la compatibilidad determinan su curvatura. El equilibrio explica el momento triangular negativo y el cortante constante positivo. Si invirtiéramos la carga, se invertirían también la deformada y los signos de ambos diagramas.",
    },
]
TOTAL_SECONDS = sum(x["duration"] for x in BEATS)
assert len(BEATS)==8 and TOTAL_SECONDS == 169
