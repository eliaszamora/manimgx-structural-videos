# Auditoría de video V2 y mejoras para V3

Fecha: 2026-10-12. Ejecución válida con QA: https://github.com/eliaszamora/manimgx-structural-videos/actions/runs/38203502111

## Comprobaciones automáticas (resultado)
- Los tres jobs (ManimGX, voz neural Kokoro y exportación+auditoría) finalizaron con éxito.
- MP4 con 169 s, 1920×1080, audio y video.
- Ocho tests de mecánica estructural aprobados en el workflow separado.
- Ocho fotogramas auditados; **ningún capítulo prácticamente vacío**.
- **Siete tramos estáticos >4 s**, con duraciones de 10,65; 10,95; 11,47; 11,48; 12,57; 13,52; 15,9 segundos. Advertencia estética importante: superar 10 s inmóvil degrada ritmo didáctico.

## Revisión visual humana de fotogramas
1. En la pantalla móvil (390 px de ancho) varios textos inferiores y etiquetas técnicas son demasiado pequeños. Deben ganar jerarquía y tamaño, no solo color.
2. En el corte de equilibrio se habla de un momento antihorario, pero NO se ve una flecha de momento curvada inequívoca. Añadirla.
3. Las deformadas se ven suaves, pero falta mostrar cómo varía la **rotación de la tangente** a lo largo del tramo con comparación antes/después.
4. Evitar en la próxima iteración mantener el mismo frame durante más de 4 s sin variación visual que acompañe una explicación; dar pausas útiles de 1–3 s sí es deseable.
5. La consistencia física de signos sigue requiriendo segunda revisión humana, además de la validación algebraica.

## Gates de aceptación propuestos para V3
- Explicación causal visible: al menos una acción física por concepto, en lugar de fórmulas superpuestas.
- Diagramas de signo vinculados a equilibrio explícito y convención dibujada.
- Rótulos técnicos legibles en una vista de 390 px.
- Congelamientos >6 s exigen justificación editorial; >10 s obligan revisión de ritmo.
- Comparativa ciega de voz con mismo guion, escucha de pronunciación de términos técnicos.
- No declarar «sin errores» hasta revisión manual completa de fotogramas y tramo de video, especialmente el equilibrio de momentos.

Este documento es una **auditoría parcial**, no una certificación profesional del diseño estructural.
