# ManimGX Structural Videos

Repositorio de experimentos educativos de ingeniería estructural. Contiene escenas verificables, renderizado automatizado en GitHub Actions y voces sintéticas abiertas en español.

## Estado

Proyecto experimental: la compatibilidad real de ManimGX con el runner de Linux y la síntesis de voz deben comprobarse mediante un workflow. Ningún resultado se declara probado hasta ver los archivos de salida y sus registros.

## Convenciones

Para una viga en voladizo empotrada a la izquierda con fuerza P descendente, con x medido desde el empotramiento y v positivo hacia arriba:

- `v(x) = -P*x**2*(3*L-x)/(6*E*I)`
- `M(x) = -P*(L-x)` y `V(x) = +P`.
- Cara izquierda del tramo derecho aislado: cortante positivo hacia arriba y momento positivo horario.
- Convención gráfica: momento positivo bajo el eje; negativo sobre él.

Se utilizará inicialmente Kokoro-82M (voz abierta en español y CPU) por su menor consumo de recursos. ManimGX incluye software Vulkan sobre CPU (lavapipe) en los paquetes Linux; su funcionamiento en Actions sigue siendo una hipótesis por verificar.
