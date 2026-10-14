"""Voz Kokoro em_alex original, segmentos con tiempo compartido por la escena."""
from pathlib import Path
from story import BEATS, TOTAL_SECONDS
import json, subprocess, tempfile
import numpy as np
import soundfile as sf
from kokoro import KPipeline

SR=24000
VOICE="em_alex"
SPEED=.98

def synthesize():
    root=Path("build/interaction_pm");root.mkdir(parents=True,exist_ok=True)
    pipeline=KPipeline(lang_code="e")
    clips=[];report=[]
    for b in BEATS:
        chunks=[]
        for _,_,wav in pipeline(b["narration"],voice=VOICE,speed=SPEED):
            wav=np.asarray(wav,dtype=np.float32)
            if len(wav):
                chunks.append(wav)
                chunks.append(np.zeros(round(.065*SR),dtype=np.float32))
        if not chunks:raise RuntimeError("No spoken audio for "+b["id"])
        spoken=np.concatenate(chunks)
        available=b["duration"]-1.5
        rate=len(spoken)/(available*SR)
        if rate>1.10:raise RuntimeError(f'Beat {b["id"]} too long: {rate:.2f}x; edit the script')
        if rate>1.0:
            with tempfile.TemporaryDirectory() as tmp:
                src=Path(tmp)/"src.wav";dst=Path(tmp)/"speed.wav"
                sf.write(src,spoken,SR)
                subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-y",
                                "-i",str(src),"-af",f"atempo={rate:.7f}",str(dst)],check=True)
                spoken,_=sf.read(dst,dtype="float32")
        slot=np.zeros(round(b["duration"]*SR),dtype=np.float32)
        start=round(.7*SR)
        if len(spoken)>len(slot)-start:raise RuntimeError(f'Voice overflow chapter {b["id"]}')
        slot[start:start+len(spoken)]=spoken
        clips.append(slot)
        report.append(dict(chapter=b["id"],slot=b["duration"],narration=len(spoken)/SR,speed=rate))
        print("Voz capítulo",b["id"],"narración",round(len(spoken)/SR,1),"s")
    audio=np.concatenate(clips)
    assert len(audio)==TOTAL_SECONDS*SR
    sf.write(root/"narracion.wav",audio,SR)
    (root/"voice_report.json").write_text(json.dumps(report,indent=2))
    print("Voice length",len(audio)/SR,"seconds")
if __name__=="__main__":synthesize()
