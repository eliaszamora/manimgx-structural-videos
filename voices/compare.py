"""Comparativa gratuita: mismas frases, voces distintas, sin servicios de pago."""
from pathlib import Path
import json
import subprocess
import sys
import wave
import numpy as np
import soundfile as sf
from kokoro import KPipeline

DEST=Path("build/voice_comparison")
DEST.mkdir(parents=True,exist_ok=True)
TEXT=(
    "Imagina una viga empotrada en su extremo izquierdo. "
    "Cuando aplicamos una carga hacia abajo, el extremo libre desciende, "
    "pero el apoyo impide que la viga gire. "
    "Por eso la deformada comienza con tangente horizontal. "
    "Y si analizamos el equilibrio, descubrimos que el momento flector es negativo."
)

def cmd(args):
    subprocess.run(args,check=True)

def mp3(source,dest):
    cmd(["ffmpeg","-y","-hide_banner","-loglevel","error",
         "-i",str(source),"-af","highpass=f=65,loudnorm=I=-18:TP=-2:LRA=9",
         "-codec:a","libmp3lame","-b:a","160k",str(dest)])

def kokoro_samples():
    pipeline=KPipeline(lang_code="e")
    for key,voice,pitch in [
        ("01_alex_natural","em_alex",1.0),
        ("02_santa_natural","em_santa",1.0),
        ("03_santa_grave","em_santa",.955),
        ("04_alex_grave_suave","em_alex",.97),
    ]:
        parts=[np.asarray(a,dtype=np.float32) for _,_,a in pipeline(TEXT,voice=voice,speed=.98)]
        if not parts: raise RuntimeError(f"Voz {voice} no genero muestras")
        wav=DEST/(key+".wav")
        sf.write(wav,np.concatenate(parts),24000)
        if pitch!=1:
            temp=DEST/(key+"_pitch.wav")
            cmd(["ffmpeg","-y","-hide_banner","-loglevel","error","-i",str(wav),
                 "-af",f"asetrate={24000*pitch:.5f},aresample=24000,atempo={1/pitch:.6f}",
                 str(temp)])
            wav.unlink();temp.rename(wav)
        mp3(wav,DEST/(key+".mp3"))
        print("OK",key,flush=True)

def piper_sample():
    # Piper requiere solamente CPU; la voz de México puede tener prosodia diferente.
    model="es_MX-claude-high"
    try:
        cmd([sys.executable,"-m","piper.download_voices","--data-dir",str(DEST),model])
        output=DEST/"05_piper_mexico_claude.wav"
        cmd([sys.executable,"-m","piper","--data-dir",str(DEST),"-m",model,"-f",str(output),"--",TEXT])
        mp3(output,DEST/"05_piper_mexico_claude.mp3")
        print("OK 05_piper_mexico_claude",flush=True)
    except Exception as exc:
        # No bloquea los cuatro ejemplos Kokoro si Hugging Face no deja descargar.
        print("Piper opcional no completado:",repr(exc),flush=True)
        (DEST/"piper_error.txt").write_text(str(exc),encoding="utf8")

def main():
    kokoro_samples()
    piper_sample()
    manifest=[]
    for audio in sorted(DEST.glob("*.mp3")):
        data=json.loads(subprocess.check_output(["ffprobe","-v","error","-show_entries",
                    "format=duration","-of","json",str(audio)],text=True))
        duration=float(data["format"]["duration"])
        if duration<5: raise ValueError(f"Archivo demasiado corto: {audio}")
        manifest.append({"file":audio.name,"seconds":round(duration,2),"text":TEXT})
    (DEST/"manifest.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding="utf8")
    print(json.dumps(manifest,ensure_ascii=False,indent=2),flush=True)
    assert len(manifest)>=4
if __name__=="__main__":main()
