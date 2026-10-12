# ManimGX Structural Videos

Proyecto gratuito de videos explicativos de **ingeniería estructural**, con renderizado auténtico en ManimGX (Rust / lavapipe CPU), voz neural en español y validaciones independientes.

## Estado verificado (12 de octubre de 2026)
- ✅ Renderizado ManimGX en GitHub Actions `ubuntu-latest`, sin GPU dedicada.
- ✅ Síntesis de Kokoro-82M en CPU, exportación de MP4 con FFmpeg.
- ✅ Laboratorio de comparación de cinco muestras, incluidas dos voces españolas masculinas de Kokoro y una variante mexicana de Piper.
- ✅ Ocho tests de mecánica estructural: condiciones de borde, curvatura, momento, cortante y equilibrio de sección.
- 🔎 Auditoría visual automática en integración: fotogramas por capítulo, muestra a 390 px, congelamientos, duración de pistas.

**No confundir ejecución de tests con garantía de ausencia de errores**. La inspección audiovisual y la verificación ingenieril de cada dibujo son obligatorias.

## Flujos
- [Video completo V2](.github/workflows/lesson_v2.yml): anima y narra 169 s de ejemplo voladizo.
- [Comparación de voces](.github/workflows/voice_lab.yml): cinco MP3 del mismo texto. Resultados en **Actions → Run → Artifacts**.
- [Tests de mecánica](.github/workflows/engineering_qa.yml): pruebas sin render que se ejecutan automáticamente al modificar código relevante.

## Archivos principales
- `lesson_v2/scene.py`, `story.py`, `voice.py`: animación y narración con reloj compartido.
- `voices/compare.py`: cinco variantes comparables Kokoro/Piper.
- `qa/mechanics.py`, `qa/test_mechanics.py`: expresiones físicas y tests.
- `qa/video_audit.py`: contact-sheet y revisión técnica del MP4.
- `AGENTS.md` y `.agents/skills/structural-video-quality/SKILL.md`: contrato de calidad para Codex y otros agentes.
- `docs/research-and-quality.md`: repositorios y skills externos evaluados.

## Convención de signos: voladizo
Eje `x` desde el empotramiento al extremo libre, desplazamientos `v` positivos hacia arriba, fuerza externa `P` hacia abajo:

```text
v(x) = -P*x**2*(3*L-x)/(6*E*I)
M(x) = -P*(L-x)
V(x) = +P
```

- El empotramiento impide el desplazamiento y el giro: `v(0)=v'(0)=0`.
- Se dibuja el momento **positivo bajo** el eje del elemento y **negativo sobre** él.
- Para el cuerpo libre DERECHO de una sección, `+V` se dirige hacia arriba y el momento negativo es antihorario.
- En este caso `M=EI*v''` y `V=dM/dx` bajo la convención especificada.

## Fuente independiente
La primera referencia es analítica. Para marcos con múltiples elementos se estudiará contraste por elementos finitos con [anaStruct](https://github.com/anastruct/anaStruct), respetando cuidadosamente sus convenciones.

Revisa las licencias de código y modelos de voz antes de redistribuir archivos distintos a nuestros propios videos.
