"""Exact cue positioning with natural male Kokoro; no pitch shift or speed tricks."""
from pathlib import Path
import json,sys
import numpy as np
import soundfile as sf
from kokoro import KPipeline
sys.path.insert(0,str(Path(__file__).resolve().parent))
from story import BEATS,SECONDS_PER_BEAT,TOTAL_SECONDS
RATE=24000

def main():
    out=Path('build/studio_v3');out.mkdir(parents=True,exist_ok=True)
    pipeline=KPipeline(lang_code='e')
    master=np.zeros(TOTAL_SECONDS*RATE,dtype=np.float32)
    report=[]
    for bidx,beat in enumerate(BEATS):
        for eidx,(at,script) in enumerate(beat['events']):
            narr=[np.asarray(w,dtype=np.float32) for _,_,w in pipeline(script,voice='em_alex',speed=.98)]
            if not narr:raise RuntimeError('Kokoro produced empty speech')
            voice=np.concatenate(narr)
            until=(beat['events'][eidx+1][0] if eidx+1<len(beat['events']) else SECONDS_PER_BEAT-.35)
            allowance=until-at
            dur=len(voice)/RATE
            if dur>allowance:
                raise RuntimeError(f"Sentence {beat['id']}-{eidx} exceeds cue by {dur-allowance:.2f}s. Edit text; never clip speech.")
            start=round((bidx*SECONDS_PER_BEAT+at)*RATE)
            master[start:start+len(voice)]=voice
            report.append({'chapter':beat['id'],'cue':eidx+1,'absolute_start':bidx*SECONDS_PER_BEAT+at,'seconds':round(dur,3),'speech':script,'headroom':round(allowance-dur,3)})
            print('Cue',beat['id'],eidx,'duration',dur,flush=True)
    sf.write(out/'alex_natural.wav',master,RATE)
    (out/'cues.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
    assert len(master)/RATE==TOTAL_SECONDS
    print('Ready:',TOTAL_SECONDS,'seconds of natural Alex, 0 pitch adjustment')
if __name__=='__main__':main()
