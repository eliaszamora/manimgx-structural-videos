"""Optional scene-cut analysis; it does not validate physics."""
import argparse,json
from pathlib import Path
def main():
    p=argparse.ArgumentParser()
    p.add_argument('video')
    p.add_argument('--out',default='scene_cuts.json')
    a=p.parse_args()
    from scenedetect import detect,ContentDetector
    cuts=detect(a.video,ContentDetector(threshold=30.0))
    report={'cuts':[{'start_s':round(x.get_seconds(),3),'end_s':round(y.get_seconds(),3)} for x,y in cuts],
            'note':'Cut detection is a warning, not proof of visual or mechanical errors.'}
    Path(a.out).write_text(json.dumps(report,indent=2))
    print('Detected',len(cuts),'scene ranges, inspect manually')
if __name__=='__main__':main()
