"""Video post-render gates: streams and duration, one chapter frame, mobile samples and freeze warnings."""
import argparse,json,subprocess
from pathlib import Path
from PIL import Image,ImageOps,ImageStat,ImageDraw
from story import BEATS,TOTAL
def check(args):
    x=subprocess.run(args,capture_output=True,text=True)
    if x.returncode:raise RuntimeError(str(args)+'\n'+x.stderr[-1100:])
    return x.stdout
def main():
    p=argparse.ArgumentParser();p.add_argument('video');p.add_argument('--output',default='build/portal/qa');a=p.parse_args()
    path=Path(a.video);dest=Path(a.output);dest.mkdir(parents=True,exist_ok=True)
    meta=json.loads(check(['ffprobe','-v','error','-show_entries','format=duration,size:stream=codec_type,codec_name,width,height,duration','-of','json',str(path)]))
    streams=meta['streams'];v=next(x for x in streams if x.get('codec_type')=='video')
    audio=next(x for x in streams if x.get('codec_type')=='audio')
    d=float(meta['format']['duration']);vd=float(v.get('duration') or d);ad=float(audio.get('duration') or d)
    assert all(abs(x-TOTAL)<1.3 for x in (d,vd,ad)),(TOTAL,d,vd,ad)
    assert v['width']>=1280 and v['height']>=720
    frames=[];quality=[];elapsed=0
    for b in BEATS:
        time=elapsed+int(b['seconds']*.64)
        out=dest/f"chapter_{b['id']}.jpg"
        check(['ffmpeg','-hide_banner','-loglevel','error','-y','-ss',str(time),'-i',str(path),'-frames:v','1','-vf','scale=780:-2',str(out)])
        im=Image.open(out).convert('RGB')
        sd=float(ImageStat.Stat(im.convert('L')).stddev[0]);assert sd>2,'Blank chapter '+b['id']
        tile=Image.new('RGB',(600,365),'#071523')
        th=ImageOps.contain(im,(590,330));tile.paste(th,((600-th.width)//2,0))
        ImageDraw.Draw(tile).text((12,338),'CHAPTER '+b['id']+' AT '+str(time)+'s',fill='white')
        frames.append(tile)
        ImageOps.contain(im,(390,220)).save(dest/f"mobile_{b['id']}.jpg")
        quality.append({'chapter':b['id'],'seconds':time,'luma_sd':round(sd,2)})
        elapsed+=b['seconds']
    sheet=Image.new('RGB',(2400,730),'#071523')
    for i,im in enumerate(frames):sheet.paste(im,((i%4)*600,(i//4)*365))
    sheet.save(dest/'contact_sheet.jpg',quality=88)
    r=subprocess.run(['ffmpeg','-hide_banner','-loglevel','info','-i',str(path),'-vf','freezedetect=n=-60dB:d=5','-an','-f','null','-'],capture_output=True,text=True)
    freeze=[line[-220:] for line in r.stderr.splitlines() if 'freeze_duration:' in line]
    report={'duration':d,'video_duration':vd,'audio_duration':ad,'size':[v['width'],v['height']],
            'chapters':quality,'freeze_warnings':freeze,
            'manual_review_needed':['Signs of beam and column diagrams','Moment inflections against curvature',
            'Load arrows vs internal actions','Audio matched to each animated event','Mobile-readable labels']}
    (dest/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
    print(json.dumps(report,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
