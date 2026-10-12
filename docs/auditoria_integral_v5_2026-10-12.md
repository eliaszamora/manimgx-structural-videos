# Auditoría V5 — 12 de octubre de 2026

**DICTAMEN: NO APROBADO COMO VIDEO DIDÁCTICO FINAL.** La ejecución de Actions exitosa significa que render, voz y tests acaban; NO demuestra que todos los signos, flechas y secuencias enseñen la física correcta.

## Inspección realizada
- MP4 `Portico_V5_Estilo_Limpio_Alex_Natural.mp4`: 84,00 s, H.264 Full HD 30 fps, AAC mono 24 kHz.
- Secuencia completa mediante 84 capturas a intervalos de un segundo, muestras intermedias, inspección a resolución original y 390 px, archivos de cues y silencios, comparación con el modelo de pórtico y las convenciones.
- 18 frases narradas, ~58,05 s de habla y ~25,95 s de pausas.
- No se inspeccionó manualmente cada uno de los 2520 fotogramas ni se realizó escucha subjetiva completa de pronunciación.

## Diagnóstico por escena
| Tiempo | Aprobado | Hallazgo / corrección |
|---|---|---|
| 0–14 s | Pórtico y apoyos empotrados legibles, H aplicada en nudo superior derecho | No aparecen L=5,6m, h=3,4m ni ejes/nudos/condiciones rotacionales. |
| 14–28 s | La interpolación FEM deforma progresivamente barras; referencia no deformada tenue | La escena dice `carga 0→100 %`, pero la flecha y rótulo `H=24kN` permanecen completos: añadir indicador `λH` sincronizado. |
| 28–42 s | Base conserva tangente vertical; extremo superior muestra tangente | Faltan variación de tangentes, giro de nudos, curvatura local e inflexión vinculada a la deformada. |
| 42–56 s | M triangular de columna izquierda con cambio de signo en el eje original | Momento se revela varios segundos después de hablar del signo basal. Definir cara de corte, ejes locales, signos, valor cero, punto de inflexión ~1,98 m; solo hay M de una columna. |
| 56–70 s | V constante sobre eje original columna izquierda | Ausentes corte y fuerza interna para justificar el signo, dos reacciones de base y equilibrio pese a que el narrador las menciona. |
| 70–84 s | Vuelve la deformada interpolada | Falta cierre mostrando relación geométrica `curvatura ↔ M ↔ V` y resumen de signos. |

## Hallazgos bloqueantes
1. **Voz/acción visual:** la primera frase de M se escucha cuando M no está visible; la narración de reacciones se escucha mientras solo figura V.
2. **Equilibrio no demostrado:** falta cuerpo libre con secciones y flechas de `R_Ax`, `R_Bx`, momentos y cortantes internos (con convenciones de ambas caras).
3. **Ambigüedad signo local vs. diagrama:** positivo para M a la derecha del eje de columna izquierda ascendente y negativo a izquierda, en el modelo; hay que explicitar `x_local`, `y_local`, lado de gráfica y cara cortada antes de generalizar.
4. **Rampa inconsistente:** magnitud de la fuerza no cambia visualmente mientras el texto afirma 0→100%.
5. **Cobertura incompleta:** solo muestra M/V de columna izquierda, no el pórtico completo (viga + otra columna).

## Otras mejoras necesarias
- La transición de diagrama de M a V aparece más como cambio de figura que como deducción de equilibrio; introducir la relación diferencial y el cuerpo libre.
- Destacar dónde cambia la concavidad y contrastarla simultáneamente con M=0. El punto violeta sobre M=0 no debe parecer una rótula real.
- Ajustar rótulos para lectura a 390 px. 25–30px a 1920px equivale a texto muy pequeño en móvil.
- Reducir esperas con geometría inmóvil: la mayoría de los 84s no está animando una cantidad estructural; se muestran textos y espera de voz.
- Mantener empotramiento hachurado (mejoró), sin volver a bloques abstractos.
- Añadir cotas geométricas y rotulaciones mínimas de carga/material.

## Valores revisados
Pórtico 1 crujía 5,6m, altura 3,4m; carga lateral 24kN. Del modelo: desplazamiento superior ~2,93mm; columna izquierda M(base) ~−23,7 kN·m, M(top) ~+17 kN·m, V local ~+11,99kN, M=0 aproximadamente a 1,98m sobre la base. Coherentes entre sí y con la deformada global; las convenciones de fuerza en ambos cortes aún requieren validación gráfica independiente. El test FEM/PyNite previo valida algunas magnitudes, no todos los dibujos.

## Criterios de aprobación para V6
- Cada oración causal tiene una acción visible simultánea: carga, rotación, curvatura, M, V, reacciones.
- Todas las flechas se generan desde fuerzas de corte y ejes locales verificados; signos sobre eje original.
- Mostrar ambas bases/reacciones y cuerpo libre antes de decir que el sistema está en equilibrio.
- Visualizar rampa de H aplicada y desplazamiento bajo misma fracción `λ`.
- Auditar capturas 1s + segmentos de movimiento, vistas móviles, ejes locales/ambas caras; aprobar narración tras escucha por capítulos.
- Solo pasar a publicación después del último render y una comprobación independiente de correcciones.

**Importante:** no confundir `layout: no problems` con corrección mecánica ni pedagógica.
