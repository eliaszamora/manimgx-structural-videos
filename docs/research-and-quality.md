# Recursos estudiados para mejorar videos (2026-10)

## Selección priorizada
| Proyecto | Motivo | Estado |
|---|---|---|
| [Manim Video Lab](https://github.com/ApliroAI/manim-video-lab) | Guion visual, foco, preguntas y gates antes del render | Principios adaptados a skill local |
| [animation-frame-qa](https://github.com/paldom/storytelling-animation) | Contact-sheet, legibilidad móvil y flashes | Implementación mínima propia |
| [anaStruct](https://github.com/anastruct/anaStruct) | Contraste independiente de vigas, marcos y diagramas | Evaluado, integración futura para marcos |
| [iart-ai/manim-skills](https://github.com/iart-ai/manim-skills) | Patrones de animaciones científicas | Referencia; APIs CE requieren adaptación |
| [AmitSubhash/3brown1blue](https://github.com/AmitSubhash/3brown1blue) | Layout, márgenes, tamaño de letra, revisión previa | Reglas adaptadas |
| [Piper](https://github.com/OHF-Voice/piper1-gpl) | Voz española/mexicana 100% offline CPU | Voz alternativa en prueba |
| [Kokoro](https://github.com/hexgrad/kokoro) | 2 voces masculinas españolas, ejecución CPU | Ya funcional |
| [Chatterbox](https://github.com/resemble-ai/chatterbox) | Mayor expresividad, modelos hispanoamericanos | Candidato posterior: necesita probar memoria/velocidad CPU |

## Qué estamos comprobando
- Matemáticas: `qa/mechanics.py` y `qa/test_mechanics.py`.
- Técnica visual: `qa/video_audit.py` exporta 8 frames, 3 pruebas a 390 px y advertencias de congelamiento.
- Calidad narrativa: `.agents/skills/structural-video-quality/SKILL.md` + revisión manual.
- Voces: `voices/compare.py` y workflow `voice_lab.yml` generan muestras del MISMO texto.

**Advertencia:** el motor puede renderizar gráficos bellos que sean mecánicamente falsos; las pruebas algebraicas, revisión de diagrama y revisión humana cumplen roles distintos.

Ninguna de estas referencias fue copiada ni ejecutada directamente; se estudiaron sus prácticas y se escribieron pruebas propias.
