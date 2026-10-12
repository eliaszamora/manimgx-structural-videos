# V8 — Auditoría del piloto avanzado ManimGX

Fecha: 2026-10-12

## Entrega verificada
- Workflow validado: https://github.com/eliaszamora/manimgx-structural-videos/actions/runs/38290030766
- Video: `Inflection_V8_Advanced_ManimGX.mp4`, 24,3 s, 1920×1080, 30 FPS solicitados (cadencia media reportada por contenedor ~27,24 fps; comprobar timestamps al editar).
- Sin audio por diseño: primera prueba didáctica silenciosa.
- Script: `pilot_inflection_v8/scene_v8.py`; mecánica: `geometry_v8.py`; tests: `test_geometry_v8.py`; auditoría: `video_qa_v8.py`.
- Skill adaptada de la oficial (MIT): `.agents/skills/manimgx/SKILL.md`.

## Cambios respecto a V7

| Aspecto | V7 | V8 |
|---|---|---|
| Carga | Transform de figura final | `ValueTracker` con actualización continua de 4 barras, nudos y flecha |
| Acercamiento | Sustitución por otra curva ampliada | `self.camera.frame.animate` sobre el mismo objeto |
| Tangente | saltos entre muestras | derivada exacta del polinomio de desplazamiento FEM |
| Ref. sin deformar | barra y resto del pórtico permanecían compitiendo en zoom | se atenúan y eliminan geometrías ajenas durante el zoom |
| Momento | dos áreas dibujadas por aparición | áreas negativa y positiva crecen progresivamente sobre eje no deformado |
| Tests | FEM y muestras | pruebas FEM + cinemática + corrección de errores visuales detectados con inspect |

## Validación numérica
Cinco tests aprobados: empotramiento exacto, continuidad, fuerza unida al nudo, derivada/rotación de tangente, curvatura e inflexión M=0.
Momento de cambio de signo: ~1,979 m sobre la base de la columna izquierda. No dibujamos una rótula ahí.

## Inspección visual
`manimgx inspect` reportó «layout: no problems in 11 samples» y el render «no problems in 20 samples». La auditoría extrajo 15 fotogramas y verificó movimiento entre 3 y 6 segundos (diferencia media: 1,838; 0,621; 7,499 en escala de imagen).
No se detectaron muestras prácticamente vacías; sí hubo **una pausa estática de ~3,57 s**.
Se revisó además una comparación de cuatro momentos conceptuales V7 vs V8.

## Pendiente
- La inflexión se muestra, pero falta una ilustración comparativa más expresiva del cambio de curvatura; la tangente gira poco porque el resultado FEM real tiene ángulos modestos.
- Añadir dos referencias tangentes/curvaturas en secciones próximas a la inflexión para hacer explícita la relación «cambia concavidad».
- Incorporar signos + y − visibles en ambas regiones del diagrama, además del color.
- Hacer el cierre menos estático y mejorar legibilidad en pantallas de 390 px.
- Solo después de aprobar la pedagogía visual, sintetizar la voz Alex natural y sincronizar por acciones.

**Estado:** piloto técnico V8 aprobado con reservas de dirección y ritmo. No afirmar que la calidad sea equivalente a 3Blue1Brown ni Efficient Engineering; los checks mecánicos y de layout no pueden medir eso.
