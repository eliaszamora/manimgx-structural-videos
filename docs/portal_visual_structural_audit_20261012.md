# Auditoría estructural y visual — Pórtico de un piso, una crujía (2026-10-12)

**DICTAMEN: REQUIERE CORRECCIONES (NO PUBLICAR COMO VERSIÓN FINAL).**

Alcance: revisión directa del MP4 de 135 s, 16 fotogramas representativos en t=3, 10, 16, 22, 31, 37, 45, 53, 61, 70, 80, 90, 102, 112, 121 y 131 s; lectura de las fuentes `portal_onebay/{mechanics,scene,story,verify_anastruct}.py`; comprobaciones numéricas del modelo por rigidez; informe FFmpeg de pistas, fotogramas y congelamientos. No equivale a revisar manualmente cada uno de los 4050 fotogramas ni a validar palabra por palabra toda la voz.

## Resultados estructurales (modelo de referencia)

Geometría: luz 5,60 m; altura 3,40 m; dos bases empotradas, uniones rígidas. `EI_viga=28 000`, `EI_columnas=20 000`, unidades compatibles con kN y m.

| Comprobación | Resultado | Estado |
|---|---|---|
| Carga vertical 35 kN al centro | Desplazamiento en medio de viga ≈ −2,171 mm | Coherente |
| Carga vertical simétrica | Reacciones verticales 17,5 kN por base; desplazamientos horizontales superiores opuestos de ≈ ±0,0015 mm | Coherente |
| Momento en viga bajo carga vertical | Extremos ≈ −17,188 kN m; centro ≈ +31,812 kN m | Coherente en las fórmulas y signo general del trazado |
| Fuerza horizontal 24 kN a la derecha | `ux` en nudos de coronación ≈ 2,930 y 2,935 mm hacia derecha | Coherente |
| Reacciones horizontales | Bases ≈ −11,993 y −12,007 kN; suma −24 kN | Coherente |
| Cambios de signo de momento en columnas | De ≈ −23,7 kN m en base a ≈ +17,0 kN m en coronación; inflexión ≈ 1,98 m desde base | Coherente matemáticamente |

anaStruct se usó para contrastar desplazamientos nodales de ambos casos en GitHub Actions; la comparación independiente NO certifica todas las flechas de momentos/cortantes renderizadas ni sus convenciones gráficas.

## Defectos confirmados o no resueltos

| Prioridad | Tiempo / capítulo | Evidencia y problema | Corrección exigida |
|---|---|---|---|
| ALTA | 80–131 s; fuerza horizontal | La flecha azul de 24 kN queda referida a la posición original del nudo derecho después de que este se traslada en la deformada exagerada. Se visualiza pasando por la viga, pero no nace exactamente del nudo desplazado. | Atar gráficamente la carga a las coordenadas interpoladas del nudo o mostrar la fuerza en geometría no deformada y desvanecerla al pasar a deformada. |
| ALTA | 119–135 s; cortante | Se muestran únicamente dos flechas de dirección horizontal, no diagramas completos de cortante para viga/columnas y los dos casos de carga. La ubicación de esas flechas sobre los fustes no deja claro si son reacciones en bases o fuerzas internas de un corte. | Añadir diagramas `V` por elemento con ejes locales, valores, signos y cuerpos libres de sección. Separar reacciones de cortante interno. |
| ALTA | 102–119 s; columnas | Curvas doradas del momento sin ejes, unidades ni signos; el código desplaza el trazado de ambos elementos hacia la derecha para `M>0`, sin una leyenda por cara/localización. No queda demostrada la compatibilidad con la convención que el usuario adoptó al mirar el interior del pórtico. | Definir ejes locales, caras de sección, lado positivo/negativo de cada columna y verificar la orientación de ambos trazados, incluido el pórtico original/deformado. |
| MEDIA | 53–66 s; momento de viga | El signo general de `M` concuerda con cálculo y convención positivo-bajo; falta marcar cruces de signo, extremos y valores. El gráfico ocupa el espacio inferior cerca del subtítulo. | Eje de cero dedicado, rótulos −/+ encima/debajo, valores y zonas separadas para fórmula y subtítulo. |
| MEDIA | 31–49 y 84–119 s; deformadas | Curvas proceden de funciones de forma FEM y representan el movimiento previsto, pero la amplificación visual `GAIN=170` no se advierte en pantalla. La doble curvatura se percibe poco a escala móvil. | Rotular “deformada exagerada ×170” (comprobar factor del dibujo) y ampliar localmente curvatura, tangentes/rotaciones/inflexión con referencia sin deformar. |
| MEDIA | Varias escenas, especialmente 45, 112, 131 s | Anotaciones bajas de pequeño tamaño y contraste débil sobre el fondo; difícil lectura en móvil. | Aumentar tipografía/contraste, mover etiquetas desde zonas superpuestas, revisar vistas de 390 px. |
| MEDIA | Ritmo | FFmpeg informó cinco pausas visuales prácticamente inmóviles de entre ≈5,0 y 5,8 s. | Mantener pausas razonadas, animar dependencia real durante explicaciones largas, eliminar congelamientos innecesarios. |
| PENDIENTE | Narración y signos finales | El archivo sí tiene video y audio completos de 135 s, pero no consta auditoría humana palabra por palabra ni comprobación independiente de **todos** los diagramas ya dibujados. | Revisar audio por capítulo y verificar cada trazado con solución de referencia y convenciones. |

## Dictamen por dimensión

- **Modelo geométrico/apoyos:** APROBADO en el alcance revisado.
- **Deformada vertical simétrica y sway lateral:** APROBADO para forma cualitativa y dirección general; falta explicitar amplificación.
- **Momentos de viga, carga vertical:** COHERENTES, presentación necesita mejoras.
- **Momentos de columnas con carga lateral:** resultado numérico coherente; representación gráfica PENDIENTE por signos/lados.
- **Cortante y reacciones:** equilibrio numérico coherente, representación visual INCOMPLETA.
- **Calidad de voz, sincronía pedagógica y legibilidad móvil:** auditoría completa PENDIENTE; legibilidad visual insuficiente.
- **Publicación didáctica final:** NO APROBADO.

## Criterios para V2 corregida

1. Mostrar correctamente todos los casos de carga en configuración original y deformada; cargas y apoyos sujetos a objetos.
2. Incluir diagrama `M` y `V` de viga y columnas bajo cada caso con convención visual explícita y cuerpos libres.
3. Animar el origen y la dirección de los momentos y cortantes con equilibrio; no colocar flechas ambiguas.
4. Rotular factor de exageración de deformada.
5. Agrandar textos técnicos y hacer auditoría móvil a 390 px.
6. Rerenderizar y revisar fotogramas y pista de voz; aprobar solo después de corregir los problemas específicos.

Esta revisión se documenta para impedir que una ejecución verde de GitHub Actions se confunda con verificación profesional exhaustiva de la animación.
