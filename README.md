# ManimGX Structural Videos

Proyecto gratuito de videos didácticos de análisis estructural, usando **ManimGX**, **Kokoro-82M** y **GitHub Actions** sobre CPU (sin GPU contratada, APIs pagadas ni tokens de Work).

## Lección 02: voladizo (169 segundos)

Incluye 8 capítulos sincronizados por duraciones compartidas:

1. Pregunta estructural.
2. Restricciones del empotramiento.
3. Deformada y pendientes.
4. Relación entre curvatura y momento.
5. Sección aislada: equilibrio de fuerzas y momentos.
6. Diagrama de momento (triangular negativo).
7. Diagrama de cortante (rectangular positivo).
8. Recapitulación.

Archivos:
- `lesson_v2/story.py`: guion, subtítulos por capítulo y reloj único.
- `lesson_v2/scene.py`: animación editable en ManimGX.
- `lesson_v2/voice.py`: voz **masculina grave** `em_alex` (pitch reducido ~4,5 %, sin API de pago).
- `.github/workflows/lesson_v2.yml`: renderiza, sintetiza voz, comprueba tiempos, une pistas y publica un MP4 descargable.

### Ejecutar sin instalar nada localmente

1. Abrir **Actions** → **Leccion v2 ManimGX + voz masculina grave (gratis)**.
2. Hacer clic en **Run workflow** → **Run workflow**.
3. Esperar los trabajos `video`, `speech`, `export`.
4. Al finalizar, abrir la ejecución y descargar el artefacto **leccion-v2-masculino-grave-FINAL**.

El workflow también se ejecuta automáticamente al modificar archivos en `lesson_v2/`.

### Control de calidad
- ManimGX: 169 segundos 1920×1080, revisión visual y 0 problemas de diseño en 45 muestras tras corregir 4 superposiciones.
- Narración: 8 segmentos con duración definida por el mismo guion; cada fragmento se comprueba para evitar cortes.
- El multiplexado rellena con el último fotograma los intervalos estáticos de ManimGX (algunos quedan optimizados en el MP4 de origen), para no recortar los últimos segundos del audio con `-shortest`.
- La compatibilidad de los cambios futuros se valida en las ejecuciones de Actions.

### Convención estructural

Viga empotrada a la izquierda, `x` desde el empotramiento, `v` positivo hacia arriba, carga `P` descendente en `x=L`:

- `v(x) = -P*x**2*(3*L-x)/(6*E*I)` (Euler-Bernoulli, pequeña deformación).
- `M(x) = -P*(L-x)`.
- `V(x) = +P` sobre la **cara izquierda del tramo derecho** cortado, con signo positivo hacia arriba.
- Cortante positivo horizontal constante por ausencia de carga distribuida.
- Momento **positivo bajo** el eje y **negativo sobre** el eje.
- En la cara izquierda del tramo derecho, momento positivo es horario; el momento resistente aquí es antihorario y, por tanto, negativo.

## Primera prueba (histórica)

Los archivos `src/escena.py`, `src/voz.py` y `.github/workflows/render.yml` conservan el prototipo inicial de 31 segundos. Son independientes de la segunda lección.

## Repositorios de origen
- https://github.com/academa-labs/manimgx
- https://github.com/hexgrad/kokoro
