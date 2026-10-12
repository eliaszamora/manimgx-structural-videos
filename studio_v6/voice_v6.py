"""CPU-only Kokoro Alex natural; exactly positioned Spanish narration."""
from pathlib import Path
import sys, numpy as np, soundfile as sf,json
from kokoro import KPipeline
sys.path.insert(0,str(Path(__file__).resolve().parent))
from story_v6 import BEATS,TOTAL_SECONDS,SECONDS_PER_BEAT
RATE=24000
def main():
    out=Path("build/v6");out.mkdir(parents=True,exist_ok=True)
    pipe=KPipeline(lang_code="e")
    result=np.zeros(TOTAL_SECONDS*RATE,dtype=np.float32)
    report=[]
    for ci,ch in enumerate(BEATS):
        for j,(t,phrase) in enumerate(ch["events"]):
            clips=[np.asarray(a,dtype=np.float32) for _,_,a in pipe(phrase,voice="em_alex",speed=.98)]
            assert clips,f"No sound for {ci}-{j}"
            audio=np.concatenate(clips)
            allowed=(ch["events"][j+1][0] if j+1<len(ch["events"]) else SECONDS_PER_BEAT-.25)-t
            if len(audio)/RATE>allowed:
                raise RuntimeError(f"Phrase {ci+1}-{j+1}: {len(audio)/RATE:.1f}s > {allowed:.1f}s; edit script")
            p=round((ci*SECONDS_PER_BEAT+t)*RATE)
            result[p:p+len(audio)]=audio
            report.append(dict(chapter=ci+1,at=ci*SECONDS_PER_BEAT+t,spoken_seconds=round(len(audio)/RATE,3),words=phrase))
            print(ci+1,j+1,round(len(audio)/RATE,3),flush=True)
    sf.write(out/"alex_natural.wav",result,RATE)
    (out/"cues.json").write_text(json.dumps(report,ensure_ascii=False,indent=2))
    print("Kokoro Alex natural complete",TOTAL_SECONDS)
if __name__=="__main__":main()
