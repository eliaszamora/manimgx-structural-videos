# Instrucciones para agentes (Codex, Claude Code y asistentes compatibles)

Este repositorio es exclusivamente para videos didácticos de ingeniería estructural.

- **Leer** [la skill de QA estructural](.agents/skills/structural-video-quality/SKILL.md) antes de editar escenas, guiones o narración.
- No modificar la convención de signos sin documentarla y actualizar simultáneamente fórmulas, dibujos y tests.
- No copiar scripts de GitHub ajenos ni ejecutar `curl | bash` sin revisión.
- Antes de un render largo: pasar tests de equilibrio/compatibilidad y prueba sintáctica.
- Antes de entregar: verificar duración de video y audio, contact-sheet, fotogramas a escala móvil, errores de signos y reproducción real.
- Para las voces: preferir alternativas gratuitas en CPU; usar la misma frase al comparar voces y no representar un acento como chileno sin escucharlo.
- **No afirmar** que un problema visual está corregido sin un fotograma posterior que lo demuestre.

## Flujo operativo para cada video nuevo

1. **Plan**: abrir una ficha del director en `production/brief_template.json`: apoyos, cargas, convención de ambas caras, concepto erróneo a corregir, ocho u otros bloques con evidencia física y narración.
2. **Engineering gate**: ejecutar el modelo analítico y contrastarlo con anaStruct en `python -m qa.anastruct_crosscheck`; si la estructura es distinta, escribir casos FEM propios y comparar signos con la convención declarada.
3. **Story gate**: aplicar principios de Manim Video Lab, motion-skills y 3brown1blue: evidencia física antes de fórmulas, una sola focalización, zonas protegidas, tipografía legible, ritmo con pausas justificadas.
4. **Render**: ManimGX sigue siendo el motor; NUNCA sustituir por Manim CE silenciosamente. Consultar la API de ManimGX antes de adaptar ejemplos de otras librerías.
5. **Audio**: voz predeterminada **Kokoro `em_alex` natural, speed=.98 y sin desplazamiento artificial de tono**; el guion debe caber sin recortar frases ni acelerar más del 10%.
6. **Video QA**: `qa/video_audit.py` y revisión manual de cada capítulo: fotogramas a 390 px, deformada, signos, flechas de corte, curvatura y momento, partes estáticas y pronunciación.
7. **Entrega**: solo declarar `PASS` audiovisual si el último render corregido fue revisado. Los tests automáticos no sustituyen una inspección ingenieril.

Las skills son guías para el agente: no son plugins de renderizado. Integrar sus criterios y scripts solo si se auditan dependencias y licencias.
