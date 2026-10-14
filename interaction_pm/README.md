# Lección 21 — Interacción P–M en columnas de hormigón armado

Este capítulo desarrolla desde compatibilidad y equilibrio el diagrama de interacción uniaxial P–M de una columna con estribos.

**Ejemplo:** sección 400 × 400 mm, ocho barras Ø16 en dos capas simétricas (4+4), centros a 50 mm de cada cara, f'c = 28 MPa, fy = 420 MPa, Es = 200000 MPa.

## Concepto físico
1. Seleccionar profundidad del eje neutro c desde la fibra comprimida.
2. Compatibilidad: ε(y) = 0.003 (c-y)/c.
3. Acero elastoplástico: fs = clamp(Es ε, −fy, +fy), εy = fy/Es.
4. Hormigón: a = β1 c; Cc = 0.85 f'c b a, con 0 ≤ a ≤ h.
5. Descontar el hormigón ficticio ocupado por cada barra dentro del bloque. El módulo local modela el solape geométrico del círculo con el bloque para evitar discontinuidades artificiales.
6. Equilibrio: Pn = Cc + Σ Fsi; Mn = Cc(h/2−a/2) + Σ Fsi(h/2−yi).
7. Repetir para c variables; identificar compresión, estado balanceado, flexión pura, tracción.
8. Construir (φMn, φPn) según ACI 318-19; para estribos usar el límite axial 0.80 φ Po, con φ=0.65 en compresión, transición lineal hasta 0.90 cuando εt ≥ εy+0.003.

**Convención:** compresión axial positiva; momento positivo comprime la cara superior; unidades base MPa, mm, N; resultados kN, kN·m.

**Precaución:** curva de resistencia seccional, no verifica por sí sola esbeltez, P–Δ, flexión biaxial, estribos, confinamiento ni detalles. En Chile debe contrastarse con la normativa vigente para el proyecto.

## Control de calidad
Los tests comprueban geometría, estado balanceado, equilibrio de fuerzas y momentos, extremos de la curva y factor φ. Un render aprobado exige además inspección audiovisual siguiendo AGENTS.md.

Esta rama prepara la nueva lección. El paquete de esta conversación contiene una vista previa MP4 completa con narración en español y el código local reproducible; no es un render validado de ManimGX/Kokoro.

Referencias: ACI 318-19 y ejemplo público de StructurePoint de columnas con estribos. Documentación ManimGX: https://manimgx.academa.ai/.
