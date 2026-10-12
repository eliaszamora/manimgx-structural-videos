"""A two-case 135-second story with timed narration."""
BEATS=[
dict(id='01',seconds=16,heading='UN PÓRTICO, DOS CARGAS',subtitle='Un piso, una crujía, nudos rígidos y bases empotradas',
narration='Estudiaremos un pórtico plano de un piso y una crujía. Las bases están empotradas y las uniones entre vigas y columnas son rígidas. ¿Por qué cambia tanto su deformada cuando cambiamos la dirección de la carga?'),
dict(id='02',seconds=16,heading='CASO A · CARGA VERTICAL',subtitle='35 kN descendentes en el centro de la viga',
narration='Primero aplicamos una fuerza vertical en el centro de la viga. La geometría y la carga son simétricas. Por eso los nudos superiores pueden girar de manera opuesta, pero el conjunto no tiene desplazamiento lateral global.'),
dict(id='03',seconds=17,heading='¿POR QUÉ SE DEFORMA ASÍ?',subtitle='La viga baja en el centro; los nudos mantienen continuidad',
narration='La viga desciende más en su punto medio. Sin embargo, las uniones rígidas obligan a que viga y columnas compartan el giro de cada nudo. Aparecen pequeños desplazamientos horizontales opuestos por simetría, no un movimiento global hacia un lado.'),
dict(id='04',seconds=17,heading='MOMENTOS BAJO CARGA VERTICAL',subtitle='En la viga: negativos en nudos y positivo cerca del centro',
narration='En la viga, el momento cambia de signo. Cerca de las uniones domina el momento negativo, mientras que en el centro aparece momento positivo. Es consecuencia del empotramiento parcial que aportan las columnas y de la continuidad de los giros.'),
dict(id='05',seconds=18,heading='CASO B · FUERZA HORIZONTAL',subtitle='24 kN hacia la derecha, en el nudo superior derecho',
narration='Ahora retiramos la carga vertical y aplicamos una fuerza horizontal hacia la derecha. Esta vez desaparece la simetría de cargas. Ambos nudos superiores se desplazan hacia la derecha: el pórtico presenta desplazamiento lateral, o sway.'),
dict(id='06',seconds=17,heading='COMPATIBILIDAD DE NUDOS',subtitle='La viga une ambos nudos; las columnas se curvan',
narration='La viga obliga a los nudos superiores a moverse casi juntos. Las bases siguen sin desplazarse ni girar. Por eso las columnas deben curvarse entre una base fija y un techo desplazado. Los giros superiores también están conectados con el de la viga.'),
dict(id='07',seconds=18,heading='DOBLE CURVATURA EN COLUMNAS',subtitle='En ambas columnas el momento cambia de signo',
narration='El análisis de rigidez muestra un cambio de signo de momento en cada columna. Allí donde el momento pasa por cero, la curvatura también cambia de signo. Se forma una zona de inflexión, pero no una rótula: la columna sigue siendo continua.'),
dict(id='08',seconds=16,heading='CORTANTE Y CONCLUSIÓN',subtitle='Las dos columnas equilibran los 24 kN horizontales',
narration='La fuerza horizontal se equilibra con cortantes en las columnas, dirigidos hacia la izquierda en las bases. La suma corresponde a veinticuatro kilonewtons. Compara: carga vertical simétrica sin sway global; carga horizontal con sway y doble curvatura.')
]
TOTAL=sum(b['seconds'] for b in BEATS)
assert TOTAL==135
