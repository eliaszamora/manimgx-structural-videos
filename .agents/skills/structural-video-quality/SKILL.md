---
name: structural-video-quality
description: Validar videos educativos de ingeniería estructural con ManimGX: equilibrio, compatibilidad, deformadas, M/V, convenciones de signos, narración, frames y revisión humana.
---

# Skill: Structural Video Quality (ManimGX)

## Propósito
Generar videos que **enseñen por qué** una estructura se deforma así. No dar por correcta una animación porque ManimGX la haya renderizado.

## Reglas no negociables (ingeniería)
1. Escribir en el brief: apoyos, grados de libertad, cargas, ejes locales/globales, y convenciones completas de signos en las dos caras del corte.
2. Resolver el ejemplo mediante un modelo de referencia INDEPENDIENTE del código de dibujo (analítico si es simple; anaStruct/PyNite si es marco).
3. Probar equilibrio global, equilibrio de partes cortadas, compatibilidad, condiciones de borde y relaciones dM/dx = V y EI*v'' = M para la convención elegida (tener cuidado con ejes y lado de corte).
4. Separar la convención matemática del trazado gráfico. En este proyecto: momento positivo **bajo** la línea, momento negativo **sobre** la línea; verificar explícitamente los signos en cada elemento.
5. Antes de pasar a otra geometría, conseguir que un segundo método concuerde con los signos y órdenes de magnitud, no solo con el valor absoluto.

## Director packet (antes del código)
Para cada capítulo: pregunta que responde, concepto causal, objeto físico principal, movimiento o comparación que lo demuestra, fórmula que se muestra **después**, segundos de narración, criterio de aprobado y representación visual que debe conservarse.

Prohibido: frases como «se dobla a la derecha» sin justificar por cargas, equilibrio y compatibilidad; flechas de tamaño arbitrario que confunden reacciones con desplazamientos; nuevos rótulos sobre antiguos; ecuaciones sin correspondencia visible.

## Layout profesional y legibilidad
- Reservar banda exclusiva para título, área técnica para geometría, banda de subtítulos sin solapamientos.
- Colores consistentes: geometría turquesa, fuerza naranja, momento naranja, corte azul, razonamiento amarillo. No reutilizar un color con significado contradictorio.
- Tamaño mínimo legible a 390 px de ancho; limitar rótulos largos. No ocultar signos negativos ni unidades.
- Primera escena: mostrar el objeto y la pregunta en 3 segundos. Cada movimiento debe revelar una dependencia.
- Mantener curvas suaves, escala exagerada indicada, fuerzas y desplazamientos visualmente distinguibles.

## Pipeline obligatorio
1. **PRE-BRIEF**: sign convention + guion + comprobación matemática.
2. **PRE-RENDER**: ejecutar `python -m unittest discover -s qa -p 'test_*.py'`, compilación Python y revisar storyboard.
3. **RENDER**: ManimGX auténtico; inspección de layout cuando esté disponible.
4. **AUDIO**: voz generada por capítulos; prohibido cortar frases para ajustar longitud; pronunciación técnica revisada.
5. **POST-RENDER**: `python qa/video_audit.py VIDEO.mp4 --out QA_DIR --expected SEGUNDOS`.
6. **HUMANO**: abrir contact sheet + frames de móvil, escuchar al menos una frase por capítulo, verificar convenciones contra los dibujos, y grabar las observaciones con timestamps.
7. **PUBLICAR** solo tras rerender final si hubo correcciones. No afirmar «sin errores» solo por tests.

## Inspira este protocolo (no ejecutar repositorios de terceros automáticamente)
- https://github.com/ApliroAI/manim-video-lab — director packet, preflight gates, bounded review (MIT).
- https://github.com/paldom/storytelling-animation — animation-frame-qa y legibilidad móvil (MIT).
- https://github.com/AmitSubhash/3brown1blue — reglas de legibilidad y composición (revisar licencia).
- https://github.com/anastruct/anaStruct — verificación independiente de vigas/marcos.
- https://github.com/iart-ai/manim-skills — estilos y flujo de revisar un frame antes de renders completos.

### Limitación
Las reglas de Manim CE/ManimGL no son intercambiables al 100% con ManimGX. Adaptar ideas, no copiar APIs sin contrastarlas. Los tests y fotogramas detectan muchas fallas, pero el juicio ingenieril y la revisión audiovisual siguen siendo imprescindibles.
