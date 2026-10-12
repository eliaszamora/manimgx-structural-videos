# Motion Canvas — prueba controlada

Editor 2D vectorial (MIT). Proyecto TypeScript con geometría de columna derivada **del mismo FEM** que ManimGX: `src/structural_data.json` se exporta desde el modelo Python. Hay una escena de 9 s donde se traza deformada y momento. No se asume que una línea bonita valida signos; se importan datos estructurales.

```sh
npm install
npm run dev
# Abrir http://localhost:9000 y pulsar RENDER en Studio
npm run build
```

El video se exporta desde Studio con el exportador FFmpeg de Motion Canvas; **la integración CI prueba compilación y código de escena**, no certifica su exportación MP4 todavía. Solo promoverlo a motor de producción tras una comparación renderizada y validada, sin sustituir ManimGX silenciosamente.
