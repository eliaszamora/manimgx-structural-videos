"""Cue-accurate single-column lesson. The same times drive video and TTS."""
BEATS=[
 dict(id='01',head='UNA CARGA CAMBIA LA GEOMETRÍA',sub='Pórtico rígido: H = 24 kN a la derecha',events=[
  (0.8,'El pórtico tiene bases empotradas y uniones rígidas.'),
  (5.4,'Aplicamos veinticuatro kilonewtons hacia la derecha.'),
  (10.0,'El equilibrio exige cortantes resistentes en ambas bases.')]),
 dict(id='02',head='DEFORMADA CALCULADA',sub='La base queda fija, el nudo superior se traslada',events=[
  (0.8,'La base no puede girar ni desplazarse.'),
  (5.4,'El nudo superior avanza casi tres milímetros.'),
  (10.0,'Exageramos la deformada para poder observarla.')]),
 dict(id='03',head='ROTACIONES COMPATIBLES',sub='No es una barra rígida inclinada',events=[
  (0.8,'La tangente inferior sigue vertical por el empotramiento.'),
  (5.4,'Arriba, el giro resulta de la continuidad con la viga.'),
  (10.0,'Entre ambos extremos aparece una curvatura variable.')]),
 dict(id='04',head='DEL GIRO AL MOMENTO',sub='La curvatura cambia de signo una vez',events=[
  (0.8,'El momento es negativo en la base de esta columna.'),
  (5.4,'Más arriba, pasa por cero y se vuelve positivo.'),
  (10.0,'Ese cero marca inflexión, no una rótula.')]),
 dict(id='05',head='CORTANTE Y EQUILIBRIO',sub='V local = +11,99 kN; reacción global a la izquierda',events=[
  (0.8,'El cortante local permanece constante en la columna.'),
  (5.4,'La reacción horizontal de esta base apunta a la izquierda.'),
  (10.0,'Ambas bases equilibran los veinticuatro kilonewtons.')]),
 dict(id='06',head='LA LÓGICA DEL PÓRTICO',sub='Restricciones → compatibilidad → curvatura → M y V',events=[
  (0.8,'No memorices la deformada ni el signo de los diagramas.'),
  (5.4,'Dedúcelos desde restricciones, compatibilidad y equilibrio.'),
  (10.0,'Ahora puedes razonar otros pórticos con mayor confianza.')]),
]
SECONDS_PER_BEAT=14
TOTAL_SECONDS=84
assert len(BEATS)*SECONDS_PER_BEAT==TOTAL_SECONDS
