"""V6 narrated explanation: full-frame M,V,N with equilibrium and signs."""
SECONDS_PER_BEAT=14
BEATS=[
 dict(head="PÓRTICO: TRES BARRAS",events=[
 (0.8,"Este pórtico tiene dos columnas y una viga."),
 (5.1,"Bases empotradas. Dividimos la viga en dos tramos."),
 (9.4,"Aplicamos veinticuatro kilonewtons hacia la derecha.")]),
 dict(head="DEFORMACIÓN PROGRESIVA",events=[
 (0.8,"Aumentamos la carga progresivamente, desde cero."),
 (5.1,"Los nudos avanzan y las barras se curvan."),
 (9.4,"Ampliamos la deformada para distinguir su curvatura.")]),
 dict(head="GIROS Y PUNTO DE INFLEXIÓN",events=[
 (0.8,"Las bases impiden giros y desplazamientos."),
 (5.1,"Los nudos superiores giran junto con la viga."),
 (9.4,"Cada columna tiene un punto de inflexión.")]),
 dict(head="EQUILIBRIO DEL PÓRTICO",events=[
 (0.8,"Aparecen reacciones horizontales en las dos bases."),
 (5.1,"Las reacciones se oponen a la carga."),
 (9.4,"Verificamos primero el equilibrio de fuerzas.")]),
 dict(head="MOMENTOS EN TODAS LAS BARRAS",events=[
 (0.8,"Dibujamos los momentos sobre cada barra original."),
 (5.1,"Dorado significa positivo; coral, negativo."),
 (9.4,"Los puntos violetas marcan momentos nulos.")]),
 dict(head="CORTANTES EN TODAS LAS BARRAS",events=[
 (0.8,"Mostramos ahora todos los cortantes."),
 (5.1,"Sin carga distribuida, los cortantes son constantes."),
 (9.4,"Cada signo depende del eje local.")]),
 dict(head="ESFUERZOS AXIALES",events=[
 (0.8,"También tenemos fuerzas axiales en cada tramo."),
 (5.1,"Tracción positiva; compresión negativa."),
 (9.4,"Los ejes locales determinan los signos.")]),
 dict(head="TRES DIAGRAMAS, UN EQUILIBRIO",events=[
 (0.8,"Los tres esfuerzos pertenecen al mismo pórtico."),
 (5.1,"Cada barra tiene sus diagramas y signos."),
 (9.4,"Todo debe cumplir equilibrio y compatibilidad.")])
]
TOTAL_SECONDS=SECONDS_PER_BEAT*len(BEATS)
assert TOTAL_SECONDS==112
