"""Checks encoded timelines and samples chapter frames/phone-width panels."""
import argparse,subprocess,json
from pathlib import Path
from PIL import Image,ImageDraw,ImageOps,ImageStat

def ffprobe(path):
    return json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration:stream=codec_type,codec_name,width,height,duration','-of','json',str(path)],text=True))

def main():
    p=argparse.ArgumentParser();p.add_argument('video');p.add_argument('--output',default='build/studio_v3/qa');p.add_argument('--duration',type=float,default=84)
    args=p.parse_args();out=Path(args.output);out.mkdir(parents=True,exist_ok=True)
    d=ffprobe(args.video);f=float(d['format']['duration'])
    vids=[s for s in d['streams'] if s['codec_type']=='video'];audios=[s for s in d['streams'] if s['codec_type']=='audio']
    assert len(vids)==1 and len(audios)==1, 'Missing audio or video'
    assert abs(f-args.duration)<1.1,(f,args.duration)
    assert int(vids[0]['width'])>=1280 and int(vids[0]['height'])>=720
    assert abs(float(vids[0].get('duration',f))-f)<1.1
    shots=[]
    for i,t in enumerate([3,17,31,45,59,73]):
        path=out/f'ch_{i+1:02d}.jpg'
        subprocess.run(['ffmpeg','-loglevel','error','-hide_banner','-y','-ss',str(t),'-i',args.video,'-frames:v','1','-vf','scale=800:-2',str(path)],check=True)
        im=Image.open(path).convert('RGB')
        assert ImageStat.Stat(im.convert('L')).stddev[0]>3, f'Empty frame at {t}s'
        tile=Image.new('RGB',(540,334),'#0B1524');preview=ImageOps.contain(im,(528,298));tile.paste(preview,((540-preview.width)//2,0))
        ImageDraw.Draw(tile).text((10,307),f'CAPÍTULO {i+1}  •  {t}s',fill='#F5F7FA');shots.append(tile)
        ImageOps.contain(im,(390,220)).save(out/f'mobile_{i+1:02d}.jpg',quality=89)
    sheet=Image.new('RGB',(1620,668),'#0B1524')
    for i,im in enumerate(shots):sheet.paste(im,((i%3)*540,(i//3)*334))
    sheet.save(out/'contact_sheet.jpg',quality=90)
    z=subprocess.run(['ffmpeg','-hide_banner','-loglevel','info','-i',args.video,'-vf','freezedetect=n=-60dB:d=6','-an','-f','null','-'],text=True,capture_output=True,check=False)
    stops=[x[-200:] for x in z.stderr.splitlines() if 'freeze_duration:' in x]
    report={'seconds':f,'tracks':[s['codec_type'] for s in d['streams']],'freeze_warnings':stops,'human_review_required':True,'disclaimer':'Automated QA cannot certify correctness of diagram arrows and conventions.'}
    (out/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));print(json.dumps(report,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
