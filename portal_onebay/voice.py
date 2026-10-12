"""Kokoro Alex natural, same chosen profile as voice sample 01; no pitch shifting."""
from pathlib import Path
import json
import numpy as np
import soundfile as sf
from kokoro import KPipeline
from story import BEATS,TOTAL
VOICE='em_alex';SAMPLE_RATE=24000;SPEED=.98;LEAD=.55;TAIL=.50
def main():
    out=Path('build/portal');out.mkdir(parents=True,exist_ok=True)
    pipe=KPipeline(lang_code='e');parts=[];audit=[]
    for beat in BEATS:
        speech=[]
        for _,_,audio in pipe(beat['narration'],voice=VOICE,speed=SPEED):
            a=np.asarray(audio,dtype=np.float32)
            if len(a):speech.extend((a,np.zeros(int(.09*SAMPLE_RATE),dtype=np.float32)))
        if not speech:raise RuntimeError('Silent chapter '+beat['id'])
        audio=np.concatenate(speech);capacity=beat['seconds']-LEAD-TAIL
        if len(audio)/SAMPLE_RATE>capacity:
            raise RuntimeError(f"Natural voice too long for beat {beat['id']}: {len(audio)/SAMPLE_RATE:.2f}s > {capacity}. Shorten narration; never truncate it.")
        slot=np.zeros(beat['seconds']*SAMPLE_RATE,dtype=np.float32)
        start=int(LEAD*SAMPLE_RATE);slot[start:start+len(audio)]=audio
        parts.append(slot)
        audit.append({'chapter':beat['id'],'slot_s':beat['seconds'],'natural_spoken_s':round(len(audio)/SAMPLE_RATE,3),'voice':VOICE,'pitch_shift':0})
        print('Chapter',beat['id'],'spoken',len(audio)/SAMPLE_RATE,'slot',beat['seconds'],flush=True)
    output=np.concatenate(parts)
    assert len(output)==TOTAL*SAMPLE_RATE
    sf.write(out/'alex_natural.wav',output,SAMPLE_RATE)
    (out/'voice_report.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2))
    print('COMPLETE:',VOICE,'duration',len(output)/SAMPLE_RATE)
if __name__=='__main__':main()
