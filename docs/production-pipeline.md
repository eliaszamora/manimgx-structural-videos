# Cómo se incorporan las herramientas de producción

No se hace una instalación masiva. Nuestra arquitectura tiene **un único motor de animación (ManimGX)** y herramientas separadas de verificación y diseño.

| Herramienta | Rol concreto | Implementación actual |
|---|---|---|
| [Manim Video Lab](https://github.com/ApliroAI/manim-video-lab) | Director packet: cada escena debe comunicar una causa y una evidencia | Checklist en `AGENTS.md`, `.agents/skills/structural-video-quality/SKILL.md` y `production/brief_template.json` |
| [motion-skills](https://github.com/iart-ai/motion-skills) y [manim-skills](https://github.com/iart-ai/manim-skills) | Estilo, claridad, foco, ritmo, pruebas de fotograma | Guías adaptadas, NO motor adicional ni snippets Manim CE sin migración |
| [3brown1blue](https://github.com/AmitSubhash/3brown1blue) | Tipografía, espacio seguro, transiciones y objeto focal | Guía adaptada en skill local |
| [anaStruct](https://github.com/anastruct/anaStruct) | Solucionador FEM independiente para detectar deformadas/direcciones erróneas | `qa/anastruct_crosscheck.py` instalado y ejecutado en QA GitHub; requiere ampliación por cada modelo |
| [animation-frame-qa](https://github.com/Paldom/storytelling-animation) | Imágenes por beat, vista 390 px, pausas, recortes | `qa/video_audit.py` + revisión con timestamps; NO ejecución de todo el script tercero |
| [Kokoro](https://github.com/hexgrad/kokoro) | Narración gratuita y natural en español | `lesson_v2/voice.py` voz `em_alex`, sin pitch shift, velocidad .98 |

## Flujo operativo reproducible

```text
Nueva estructura / problema físico
    → ficha de director (plan, apoyos, convención, por qué)
    → solución analítica + solver FEM independiente
    → pruebas automáticas de equilibrio y deformada
    → escenas ManimGX y narración Alex natural por capítulos
    → render GitHub Actions + MP4
    → inspección visual a 390 px / contact sheet / congelamientos
    → revisión ingenieril y pedagógica (manual)
    → CORREGIR y rerender si es necesario
    → entrega de vídeo y reporte de QA
```

### Criterios de rechazo

- **Física**: un signo/rotación o reacción incorrectos bloquean la entrega.
- **Didáctica**: narrar un giro sin mostrarlo o utilizar una fórmula antes de evidenciar el mecanismo exige revisión.
- **Composición**: texto fuera de banda segura, flecha que parece una fuerza y es un desplazamiento, o signos ilegibles exige revisión.
- **Audio**: el texto se corta o requiere aceleración excesiva; ajustar el guion, no deformar la voz.
- **Ritmo**: pausas estáticas largas >5 s sin intención didáctica quedan marcadas para corrección.
- **Validación**: un CI verde NO significa «sin errores». Exigir inspección de la última versión renderizada.

### Sobre la integración efectiva

- Las skills ya residen en el repositorio y se mencionan desde `AGENTS.md`, que permite instruir a agentes de desarrollo compatibles. No son instalaciones de plugins mágicos.
- Nuestro `anaStruct` compara la respuesta numérica en el voladizo con un modelo analítico independiente; todavía NO valida automáticamente cada flecha dibujada, ni sirve para marcos sin ampliar el caso de prueba.
- `qa/video_audit.py` prepara evidencia de pantalla/movimiento pero no interpreta por sí solo las convenciones de signos.
- Para próximos marcos se debe crear en `qa/` un caso FEM independiente por estructura, con su mapping local/global explícito antes de la escena.
