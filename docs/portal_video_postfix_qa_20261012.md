# Pórtico de un piso — auditoría después de correcciones (12-10-2026)

Video: 135 s, 1920 × 1080, H.264/AAC, Kokoro em_alex natural.
Último render y QA automáticos exitosos: https://github.com/eliaszamora/manimgx-structural-videos/actions/runs/38208834167

## Qué se corrigió
1. Casos vertical y lateral: diagramas de momento y cortante de los cuatro elementos, evaluados en los ejes locales definidos.
2. Momento de viga: trazado positivo hacia abajo y negativo hacia arriba; momentos de columnas para ejes locales orientados hacia arriba: positivo a la derecha y negativo a la izquierda.
3. El esfuerzo de la carga horizontal se dibuja en el nudo que se desplaza, no en su posición original.
4. Antes de dibujar los diagramas de esfuerzo sobre el caso vertical, la geometría vuelve a su eje no deformado.
5. La deformada indica ampliación ×170, y la explicación distingue acciones internas y reacciones.
6. Narración Alex natural sin pitch artificial, con textos ajustados sin cortar audio.

## QA numérico
- Calculo matricial independiente y anaStruct: PASA (comparación de desplazamientos).
- Equilibrio global y sección: PASA.
- Relación dM/dx=V para los cuatro elementos en ambos casos: PASA.
- Relación de signo EI*curvatura=M en los cuatro elementos: PASA.
- Bajo fuerza vertical: V viga izquierda +17,5, derecha -17,5 kN; salto -35 kN: PASA.
- Bajo fuerza lateral: V columnas +11,993 y +12,007 kN; suma 24 kN: PASA.
- Momentos de columnas caso lateral cambian de negativo en base a positivo en el coronamiento, inflexión ~1,98 m: PASA.

## QA audiovisual de la exportación
- Video y audio **135 s exactos** cada uno: PASA.
- Resolución 1920×1080 y pistas H.264/AAC: PASA.
- Ocho capturas por capítulo y vista previa de 390px: revisadas.
- Advertencias de congelamiento >5 s: **ninguna** en este render.
- Spot-check visual adicional de escenas 51, 54, 56, 58, 60, 62, 65, 75, 83, 93, 106, 114 y 128 s.
- Flechas, soporte, geometría original, signo de M y V: sin errores graves identificados en esas muestras.

## Limitaciones: no declarar perfección
- Los rótulos numéricos continúan pequeños en una vista de 390px de ancho; conviene verlo a pantalla completa horizontal. **Legibilidad móvil no aprobada por completo.**
- El video usa barras de diagrama superpuestas al pórtico y una leyenda numérica; para enseñanza más extensa conviene agregar acercamientos de sección cortada y arcos de momento.
- QA no inspecciona uno a uno los 4050 fotogramas ni escucha manualmente cada palabra de narración.
- La concordancia FEM de desplazamientos y los tests de esfuerzo por código no equivalen a una certificación profesional del cálculo.
