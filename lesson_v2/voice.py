"""Voz masculina española Kokoro em_alex, capítulos sincronizados a ManimGX."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent))
from story import BEATS, TOTAL_SECONDS
import json, subprocess, tempfile
import numpy as np
import soundfile as sf
from kokoro import KPipeline

SAMPLE_RATE = 24000
VOICE = "em_alex"
START_PAUSE = .65
END_PAUSE = .65
PITCH = .955  # Baja ~0.8 semitonos, manteniendo aproximadamente la duración.

def filtered(data, tmp):
    before=tmp/"original.wav"
    after=tmp/"grave.wav"
    sf.write(before,data,SAMPLE_RATE)
    # Pitch discretamente menor, manteniendo velocidad y aplicando compresión leve.
    filt=f"asetrate={SAMPLE_RATE*PITCH:.3f},aresample={SAMPLE_RATE},atempo={1/PITCH:.6f},highpass=f=65,acompressor=threshold=-23dB:ratio=1.8:attack=20:release=160"
    subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-y","-i",str(before),
                    "-af",filt,"-ar",str(SAMPLE_RATE),str(after)],check=True)
    arr,sr=sf.read(after,dtype="float32")
    assert sr == SAMPLE_RATE
    return arr

def fit(data,capacity,tmp):
    maximum=int(capacity*SAMPLE_RATE)
    if len(data)<=maximum:
        return data,1.0
    # Ajuste solo si una narración supera la ventana; mantener el tono.
    factor = len(data)/maximum
    if factor>1.22: raise ValueError(f"Narración demasiado larga ({factor:.2f}x); ajustar guion, no recortar")
    src=tmp/"long.wav"
    dst=tmp/"fitted.wav"
    sf.write(src,data,SAMPLE_RATE)
    subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-y","-i",str(src),
                    "-af",f"atempo={factor:.7f}","-ar",str(SAMPLE_RATE),str(dst)],check=True)
    arr,_=sf.read(dst,dtype="float32")
    if len(arr)>maximum: arr=arr[:maximum]
    return arr,round(factor,3)

def main():
    Path("build").mkdir(exist_ok=True)
    pipe=KPipeline(lang_code="e")
    segments=[]
    report=[]
    for i,b in enumerate(BEATS):
        with tempfile.TemporaryDirectory() as d:
            tmp=Path(d)
            parts=[]
            for _,_,audio in pipe(b["narration"],voice=VOICE,speed=.98):
                audio=np.asarray(audio,dtype=np.float32)
                if len(audio): parts.extend([audio,np.zeros(int(.085*SAMPLE_RATE),dtype=np.float32)])
            if not parts: raise ValueError(f"Capítulo {i+1}: sin audio")
            spoken=filtered(np.concatenate(parts),tmp)
            room=b["duration"]-START_PAUSE-END_PAUSE
            spoken,factor=fit(spoken,room,tmp)
        slot=np.zeros(round(b["duration"]*SAMPLE_RATE),dtype=np.float32)
        start=round(START_PAUSE*SAMPLE_RATE)
        slot[start:start+len(spoken)]=spoken
        segments.append(slot)
        report.append({"chapter":b["id"],"slot_seconds":b["duration"],
                       "spoken_seconds":round(len(spoken)/SAMPLE_RATE,2),
                       "tempo_factor":factor,"voice":VOICE})
        sf.write(f"build/segment_{b['id']}.wav",slot,SAMPLE_RATE)
        print(f"Beat {b['id']} {len(spoken)/SAMPLE_RATE:.2f}s / {b['duration']}s; factor {factor}",flush=True)
    out=np.concatenate(segments)
    assert len(out)==TOTAL_SECONDS*SAMPLE_RATE
    sf.write("build/narracion.wav",out,SAMPLE_RATE)
    Path("build/report_voz.json").write_text(json.dumps(report,ensure_ascii=False,indent=2))
    print(f"HECHO {len(out)/SAMPLE_RATE:.2f}s, masculina {VOICE}, tono {PITCH}",flush=True)
if __name__=="__main__":
    main()
