"""Genera voz natural en español con Kokoro-82M y CPU."""
from pathlib import Path
import numpy as np
import soundfile as sf
from kokoro import KPipeline
TEXT=[
"¿Por qué una viga empotrada se curva cuando aplicamos una fuerza hacia abajo?",
"El empotramiento impide desplazamientos y rotaciones.",
"La deformada empieza con pendiente cero, pero después desciende progresivamente.",
"La curvatura es negativa. Por eso, el momento es negativo y alcanza su máximo absoluto junto al apoyo.",
"En nuestra convención, el momento negativo se dibuja sobre el eje.",
"Si aislamos la parte derecha de la viga, el cortante interno apunta hacia arriba y vale más P.",
"La clave es comprender las restricciones, la compatibilidad y el equilibrio. No memorizar diagramas."
]
def main():
    pipe=KPipeline(lang_code='e')
    parts=[]
    for sentence in TEXT:
        for _,_,audio in pipe(sentence,voice='ef_dora',speed=1):
            a=np.asarray(audio,dtype=np.float32)
            if a.size: parts.extend([a,np.zeros(4000,dtype=np.float32)])
    if not parts: raise RuntimeError('El sintetizador no produjo audio')
    out=Path('build/narracion.wav');out.parent.mkdir(parents=True,exist_ok=True)
    audio=np.concatenate(parts);sf.write(out,audio,24000)
    print(f'Audio: {len(audio)/24000:.1f}s')
if __name__=='__main__': main()
