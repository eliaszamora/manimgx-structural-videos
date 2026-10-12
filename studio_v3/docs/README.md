# Structural Studio V3 — laboratorio de videos estructurales

**Objetivo:** elevar calidad sin confundir estética con mecánica correcta. Ningún método externo modifica el video previo V2 ni lo reemplaza sin evaluación.

## Seis mejoras implementadas

1. `structural_viz`: biblioteca genérica `Member`/`Sample` y adaptadores de ManimGX para apoyos, geometría deformada, diagramas locales `M`,`V`, cruces exactos y convenciones. Local +x = inicio→fin; un diagrama positivo va al normal horario, que para una viga de izquierda a derecha queda bajo el eje. La representación de una fuerza **no** equivale al lado de la curva del diagrama.
2. `style.py`: sistema cromático semántico, dos regiones, títulos fuera de área física y etiquetas técnicas con mayor contraste.
3. `demo/story.py`/`voice.py`: Alex natural `em_alex`, sin pitch shift, 18 frases temporizadas (3 por capítulo) en una lección de 84 s. Cada segmento debe caber en su ventana; si no cabe, el render se bloquea y se edita el guion.
4. `motion_canvas`: prototipo comparativo TypeScript con la MISMA geometría numérica; compila en una acción gratuita. Exportación MP4 de Motion Canvas sigue requiriendo prueba separada desde su editor (el CI no afirma lo contrario).
5. `qa/pynite_check.py`: segundo solver PyNite para verificar desplazamientos nodales y reacciones, independiente de `portal_solver.py`. Además `qa/test_diagrams.py` prueba signos de M, V, lado de curvas, compatibilidad y balance global.
6. `remotion`: posproducción **opcional** de una tarjeta final de seis segundos (con workflow de ejecución manual y licencia gratuita elegible). No se agrega indiscriminadamente a los videos antes de revisar su estilo.

## Ejecución gratuita

- [`studio_v3.yml`](../../.github/workflows/studio_v3.yml) (push en `studio_v3/`): cálculo y comparación PyNite son **gate obligatorio**, luego ManimGX real + Kokoro y MP4 final con auditoría de fotogramas.
- [`compare_motion_canvas.yml`](../../.github/workflows/compare_motion_canvas.yml): prueba de compilación de Motion Canvas. No da por válida la imagen con solo compilar.
- [`remotion_endcard.yml`](../../.github/workflows/remotion_endcard.yml): trabajo **manual** y aislado de posproducción.

## No falsificar revisiones

Los tests de modelo, clips de 84 s y contact sheets ayudan a detectar fallos. No prueban corrección de cada flecha ni que cada palabra esté visualmente sincronizada; se necesita abrir fotogramas y mirar las animaciones finales. Cualquier fallo debe tratarse como `REVISE` y corregirse antes de afirmar `PASS`.

### Convención especial del pórtico

La columna izquierda tiene eje local de la base al nudo. Su momento bajo H=24 kN es ≈−23,73 kN·m en la base y ≈+17,05 kN·m arriba. El diagrama local negativo queda a la izquierda y el positivo a la derecha de su propio eje. El cortante **local** positivo ≈11,99 kN se distingue de la reacción **global** horizontal en base, dirigida a la izquierda. El punto interior con M=0 no es una rótula.

## Herramientas y licencias

ManimGX/Motion Canvas, MIT; PyNite, MIT; Tipografía/Cues Kokoro Apache 2.0/modelo con condiciones propias; Remotion bajo [licencia gratuita elegible](https://github.com/remotion-dev/remotion/blob/main/LICENSE.md). No incorporar componentes extraídos literalmente de bibliotecas incompatibles.
