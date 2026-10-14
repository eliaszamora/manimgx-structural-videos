# Rediseño visual de la clase P–M (no es la versión final)

## Diagnóstico del render 3D anterior
La captura real de capítulos muestra una columna pequeña repetida en el mismo plano junto a una sección 2D y un gráfico de ε. En la mayor parte de los 1113 segundos se mueve la cámara en círculos, pero la mecánica no cambia de representación. Por eso se ve como una presentación con un objeto 3D. La desaparición de títulos no corrigió el problema.

## Norma de dirección
- Ningún encabezado, número de capítulo, pantalla de transición o fórmula como título.
- Una sola idea dinámica por plano. Encuadres amplios solo para dar contexto; se debe llenar la pantalla al explicar un mecanismo.
- El hormigón es turquesa translúcido; el acero es amarillo; compresión coral; tracción azul; eje neutro amarillo claro.
- Colores asociados a estados mecánicos, no a decoración.
- Las posiciones geométricas provienen de una única profundidad c: bloque a=β₁c, deformaciones ε(y), fuerzas y punto (M,P) sincronizados; no inventar deformación de la columna para mejorar la animación.
- Cámara fija cuando se comparan magnitudes. Girarla solamente cuando se revela volumen, seccionamiento o disposición del acero.
- Fórmulas emergen después del fenómeno. Nunca sustituir una fuerza por un texto aislado.
- Validar signos: compresión positiva y momento positivo comprimiendo cara superior; ε superior +0.003; tracción negativa.
- No mostrar una superficie biaxial como si proviniese del cálculo uniaxial. El caso tridimensional de Mx/My se presenta por separado.

## Arquitectura cinematográfica de ~18m

### Acto I · ¿Por qué P y M juntos? (capítulos 01–04)
Primer plano de una columna tridimensional a escala visual útil. Revelar 8 barras y estribos. Flecha axial por el centro, luego trasladar **en el plano de flexión** para crear e y M=Pe. Cortar físicamente la sección: después del corte cambiar a vista ortogonal sin salto de convención. Evitar diagramas generales antes de plantear el problema.

### Acto II · El mecanismo interno (05–10)
Mantener una sola sección grande: primero triángulo de deformaciones enlazado con c; el espectador debe ver semejanza de triángulos. Barras cambian el estado de tracción/compresión por profundidad. Derivar εs e introducir fy y Es con un gráfico material, no una lista de números. El bloque de Whitney se desarrolla sobre esa sección. Descontar hormigón desplazado por acero dentro del bloque y dibujar diferencias de área sin una lámina de texto.

### Acto III · El punto surge de las fuerzas (11–13)
Hacer visible Cc en el centroide a/2. Fuerzas de barras con flechas cuya orientación y magnitud derivan de Fsi(c). Mover resultantes a los ejes de suma en fuerzas y momentos; mostrar que salen dos coordenadas del mismo estado. Balanceado: animar el mismo c hasta εt = εy, sin asumir que la fibra exterior coincide con la capa extrema de barras.

### Acto IV · Nacimiento de la interacción (14–18)
Los ejes aparecen al lado de sección grande. Arrastrar c continuamente de compresión al balanceado, flexión pura y tracción; cada paso ilumina y deja un punto (Mn,Pn), formando una curva. Nominal vs φ: duplicar la curva mediante una transformación, nunca reemplazarla por otra sin correspondencia visual. Cap axial de columna con estribos 0.80 φPo se identifica aparte.

### Acto V · Diseño y limitaciones (19–21)
Agregar puntos de demanda con una convención visible. Resaltar puntos interiores/exteriores y evitar confundir carga y resistencia. Regresar a una columna 3D para distinguir efectos P–Δ y biaxiales que la curva uniaxial **no** incluye; dejar claro que requieren análisis y verificaciones adicionales.

## QA obligatorio
1. Engineering unit tests: deformaciones, estado balanceado, fuerzas, momentos, φ, capacidad máxima. Usar test independientes del dibujo.
2. Render de **piloto de 49 segundos** con voz de primer beat antes de lanzar los 18 minutos.
3. Extraer 8 fotogramas del piloto, ver además a escala móvil 390 px; verificar tamaño del objeto, barras y colores.
4. Revisar momentos exactos de transición, especialmente eje neutro→bloque→diagrama.
5. Comparar la primera narración de Kokoro con la acción visual, sin cortes ni silencios añadidos artificialmente.
6. Solo entonces extender secuencias y renderizar las 21; revisar contact sheet real y audio del último artefacto. No decir «final» por CI verde.
