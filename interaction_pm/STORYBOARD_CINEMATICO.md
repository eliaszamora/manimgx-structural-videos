# Storyboard de dirección — clase cinematográfica interacción P–M

**Público:** ingeniero civil estructural junior. **Voz:** Kokoro em_alex a velocidad natural. **Motor:** ManimGX 3D auténtico, cámara activa solo si revela geometría. **Formato:** 16:9, QA móvil a 390 px.

No copiar la estructura de 21 diapositivas. Los 21 bloques se escuchan en audio, pero el espectador ve una película continua, con 5 actos y transiciones de objetos físicos. Una fórmula aparece en el mismo lugar que el fenómeno que describe; no hay tarjetas de capítulo.

| Beat | Evidencia visual específica | Movimiento que enseña | Afirmación ingenieril que se verifica |
|---|---|---|---|
| 01 | Volumen de hormigón, estribos y 8 barras | Revelar primero hormigón, luego refuerzo, después dos resultantes | La combinación P+M gobierna la sección |
| 02 | Eje centroidal y línea de acción | Desplazar P transversalmente una distancia e, aparece el par correspondiente | M = P e, con convención de signos clara |
| 03 | Punto de demanda en dos ejes vacíos | Descomponer P y M sobre sus dos coordenadas | Cada estado es una pareja, no dos resistencias independientes |
| 04 | Corte ortogonal del prisma 3D sin cambiar el lado comprimido | Cámara pasa de volumen a sección 400×400, centros de barras a 50 mm | Armado esquemático 4+4, no detallamiento constructivo suficiente |
| 05 | Perfil triangular de deformaciones sin ecuación inicial | Inclinar una línea manteniendo compatibilidad geométrica | Secciones planas permanecen planas |
| 06 | Eje neutro c medido desde la cara comprimida | Desplazar plano amarillo y mostrar cruce ε=0 | La distancia c **no** es el tamaño del bloque equivalente |
| 07 | Barras superiores e inferiores ligadas a ε(y) | Dos indicadores muestrean una **misma** recta de deformaciones | ε_s(y)=0.003(c−y)/c con tracción negativa |
| 08 | Ley material del acero (tensión vs deformación) | Proyectar ε de una barra al gráfico elastoplástico, detener en ±fy | ε_y=fy/Es=0.0021; no asumir siempre fluencia |
| 09 | Campo de tensiones de hormigón y su rectángulo equivalente | Transformar el área comprimida en bloque a=β1c | Cc=0.85 f'c b a, centrado a/2 |
| 10 | Un cilindro de acero atravesando la frontera del bloque | Mostrar el solape como un segmento circular que se descuenta | Ni área ni primer momento del hormigón desplazado deben duplicarse |
| 11 | Flechas de fuerzas del acero y del hormigón sobre la sección | La longitud/orientación sale de F(c); añadir algebraicamente | ΣF=P_n, compresión positiva |
| 12 | Fuerzas + brazos visibles hasta el centroide de la sección | Extraer r×F de cada capa, con curva incremental de suma | M_n=ΣF_i (h/2-y_i), incluyendo el momento real del segmento desplazado |
| 13 | Triángulo ε y barra extrema traccionada | Animar c hasta que ε_t=ε_y en acero extremo, detener justo allí | c_b=d_tε_cu/(ε_cu+ε_y); no confundir acero con fibra extrema |
| 14 | Desaparecen brazos y quedan dos coordenadas nacidas de la sección | Mover c y trazar **solo lo ya recorrido** de la curva nominal | Una variable c conduce simultáneamente a (M_n,P_n) |
| 15 | Corte de compresión uniforme (estado idealizado), no inventar eje neutro | Llevar resultado al extremo P_o, marcar límite axial de estribos | P_o=.85 f'c (A_g-A_st)+f_y A_st; límite axial de diseño 0.8 φP_o |
| 16 | Compresión y tracción interiores opuestas | Mantener suma de fuerzas nula mientras queda par resistente | En P_n=0 aún existe M_n no nulo |
| 17 | Hormigón fisurado pierde su fuerza de tracción | Barra extrema pasa a tracción y resultante se aproxima a −Ast fy | Extremo nominal Pt de sección con armado simétrico |
| 18 | Dos curvas: nominal y diseño, sin reemplazo brusco | Cada punto nominal se desplaza proporcionalmente al φ(c) de ese estado | φ=0.65–0.90 para columna con estribos y acero grado 420 MPa (ACI 318-19) |
| 19 | Puntos de demanda procedentes de combinaciones, no máximos independientes | Iluminar punto que queda dentro y otro fuera de resistencia de diseño | Evaluar par (Pu,Mu), no P y M por separado |
| 20 | Columna 3D con línea lateral de deformada + dos ejes | Mostrar desplazamiento lateral y biaxialidad como **problemas adicionales**, sin afirmar que los resuelve P–M uniaxial | Esbeltez, segundo orden, confinamiento, conexiones, detallamiento y biaxialidad no quedan verificados por una curva uniaxial |
| 21 | Cadena visual: sección → ε → σ → fuerzas → curva → demanda | Objetos anteriores regresan transformándose, sin cartel de recapitulación | Conexión causal completa de compatibilidad a resistencia |

## Tipos de escena: cinco gramáticas distintas, no 21 variaciones de un layout

- **Materia y estructura 3D** (01–04; retorno breve en 20). Cámara con profundidad real, sin giro continuo decorativo.
- **Sección ortogonal a escala legible** (05–10): triángulos de deformación, perfil material y bloque equivalente.
- **Estática con brazos de palanca** (11–13): flechas y sumas vectoriales precisas, vinculación con equilibrio.
- **Cálculo como trazo geométrico** (14–19): puntos sucesivos y recorrido continuo de la curva, nominal y diseño distinguibles.
- **Síntesis causal** (21): las cinco representaciones se convierten unas en otras.

## Puertas de calidad bloqueantes

### G1 — Fórmulas
- Unidades consistentes: mm, MPa, N; resultados kN, kN·m.
- Fuerzas, momentos y φ contrastados contra integración independiente por fibras.
- Estado balanceado, compresión pura, tracción pura y P_n=0 verificados.
- Descuento de hormigón parcialmente desplazado incluye **área y primer momento exactos**.
- El plano neutro real c y el bloque a=β1c se muestran separados.

### G2 — Semántica visual
- Color tracción no puede indicar compresión y viceversa.
- La misma coordenada c alimenta todos los objetos; no hay curvas inventadas.
- Las barras no se representan fluyendo cuando |ε_s|<ε_y.
- La cámara no hace creer que se altera una sección cuando solo cambia la vista.
- Si un valor se sale de escala, indicar explícitamente recorte o cambiar la escala con transición visible (sin clamp silencioso).

### G3 — Post-render
- Verificar todos los beats, 3–5 frames en puntos críticos y escalado móvil 390 px.
- Sin fórmulas superpuestas, diagramas fuera de pantalla ni elementos que se ocultan por error.
- Probar stream de video y audio completo, sin último fotograma congelado excesivamente.
- Comparar voz con movimiento en cada beat, especialmente cuando se deriva una expresión nueva.
- Cualquier falla exige corregir el código, volver a renderizar y auditar **la versión corregida**.

Nota: este storyboard **no equivale** a un render audiovisual aprobado; obliga a diferenciar ingeniería validada, escena compilada y película inspeccionada.
