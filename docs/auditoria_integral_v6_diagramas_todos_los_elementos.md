# V6: diagramas M, V y N de TODOS los elementos — revisión

## Geometría y convenciones
Pórtico plano con 2 columnas, 1 viga (dividida en 2 elementos de análisis) y 2 bases empotradas. Caso lateral: carga horizontal H=24 kN en nudo superior derecho. **Ejes locales:** columnas de base a coronación, dos tramos de viga de izquierda a derecha. Momento local positivo se representa en normal horaria (derecha para las dos columnas, debajo de la viga); negativo, lado opuesto. Axial N positivo = tracción. No intercambiar signos locales sin transformar los ejes.

| Elemento | M local inicial → final (kN·m) | V local (kN) | N (kN) |
|---|---:|---:|---:|
| C1 | −23,7307 → +17,0457 | +11,9931 | +6,0904 |
| V1 | +17,0457 → −0,0074 | −6,0904 | +11,9931 |
| V2 | −0,0074 → −17,0606 | −6,0904 | +11,9931 |
| C2 | −23,7630 → +17,0606 | +12,0069 | −6,0904 |

Las columnas tienen inflexión aproximadamente a 1,98 m desde sus bases. V1 y V2 son dos segmentos de UNA viga física. El momento del punto central de la viga es ~−0,007 kN·m: no hay una rótula.

## Comprobaciones realizadas
- Tests del modelo de rigidez matricial para las cuatro barras: equilibrio, M'(x)=V, axial constante, continuidad M y V en la viga.
- Segundo solucionador PyNite: validación independiente de 18 componentes de desplazamiento nodal y reacciones horizontales para casos vertical y lateral.
- MP4 final de 112 s con audio Alex natural, ambas pistas H264/AAC de 112 s.
- ManimGX: cero incidencias de distribución en 90 muestras.
- Ocho fotogramas representativos del archivo final revisados visualmente, además de los controles a escala móvil generados automáticamente.
- Cuatro avisos de imagen prácticamente estática superiores a 6 s. **No es una auditoría humana continua de los 112 segundos ni certifica ausencia de errores de diseño en todos los fotogramas**.

## Pendiente para calidad editorial superior
1. Animar una verdadera sección cortada en cada columna y en la viga, con fuerzas internas, momentos y signos de ambas caras; un diagrama con áreas correctas no sustituye la demostración de equilibrio.
2. Aumentar tamaño de cotas y signos para pantallas móviles.
3. Sincronizar la aparición de cada fuerza/reacción con la narración y reducir pausas visuales largas.
4. Preparar una versión comparativa para la carga vertical simétrica con sus propios diagramas completos.

Código: `studio_v6/scene_v6.py`, `engineering_v6.py`, `story_v6.py`, `voice_v6.py`. Workflow: `.github/workflows/studio_v6.yml`.
