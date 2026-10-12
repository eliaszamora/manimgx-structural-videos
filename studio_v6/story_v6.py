"""V6 narrated explanation: full-frame M,V,N with equilibrium and signs."""
SECONDS_PER_BEAT=14
BEATS=[
 dict(head="PÓRTICO: TRES BARRAS",events=[
 (0.8,"Analicemos el pórtico completo, con sus dos columnas y una viga."),
 (5.1,"Las bases son empotradas. La viga tiene dos tramos de cálculo."),
 (9.4,"Aplicamos una fuerza horizontal de veinticuatro kilonewtons.")]),
 dict(head="DEFORMACIÓN PROGRESIVA",events=[
 (0.8,"Aumentamos gradualmente la carga, desde cero hasta su valor completo."),
 (5.1,"Los nudos se desplazan y las barras se curvan de manera continua."),
 (9.4,"La deformada está amplificada para distinguir su curvatura.")]),
 dict(head="GIROS Y PUNTO DE INFLEXIÓN",events=[
 (0.8,"Las bases impiden el giro y el desplazamiento."),
 (5.1,"Los nudos superiores giran, por compatibilidad con la viga."),
 (9.4,"En cada columna, el momento cambia de signo en un punto de inflexión.")]),
 dict(head="EQUILIBRIO DEL PÓRTICO",events=[
 (0.8,"Para equilibrar la carga, aparecen reacciones horizontales en ambos apoyos."),
 (5.1,"Las reacciones se oponen a los veinticuatro kilonewtons aplicados."),
 (9.4,"El equilibrio global es nuestro primer control de los esfuerzos.")]),
 dict(head="MOMENTOS EN TODAS LAS BARRAS",events=[
 (0.8,"Dibujamos el momento sobre los ejes de ambas columnas y de la viga."),
 (5.1,"El dorado indica momento positivo; el coral, momento negativo."),
 (9.4,"Los puntos violeta señalan dónde el momento cambia de signo.")]),
 dict(head="CORTANTES EN TODAS LAS BARRAS",events=[
 (0.8,"Ahora aparecen los cortantes de todos los elementos del pórtico."),
 (5.1,"En estos tramos, sin carga distribuida, cada cortante es constante."),
 (9.4,"Su signo corresponde al eje local y a la convención declarada.")]),
 dict(head="ESFUERZOS AXIALES",events=[
 (0.8,"También existen esfuerzos axiales, aunque aquí no sean los protagonistas."),
 (5.1,"En cada tramo son constantes: tracción positiva y compresión negativa."),
 (9.4,"Las direcciones locales importan para interpretar cada signo.")]),
 dict(head="TRES DIAGRAMAS, UN EQUILIBRIO",events=[
 (0.8,"Momento, cortante y axial corresponden a la misma estructura."),
 (5.1,"Cada elemento necesita su propio diagrama y su respectivo signo."),
 (9.4,"El resultado debe respetar equilibrio, compatibilidad y ejes locales.")])
]
TOTAL_SECONDS=SECONDS_PER_BEAT*len(BEATS)
assert TOTAL_SECONDS==112
