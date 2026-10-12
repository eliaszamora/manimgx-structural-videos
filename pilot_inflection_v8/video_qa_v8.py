"""V8 quality gate: distinguish actual motion from a successful encoding."""
import json,sys,subprocess
from pathlib import Path
import numpy as np
from PIL import Image,ImageOps,ImageDraw,ImageStat,ImageChops
def cmd(args):
    return subprocess.run(args,check=True,capture_output=True,text=True)
def probe(p):
    return json.loads(cmd(["ffprobe","-v","error","-show_entries",
    "format=duration:stream=codec_type,width,height,duration,nb_frames,avg_frame_rate",
    "-of","json",str(p)]).stdout)
def extract(video,t,path):
    cmd(["ffmpeg","-hide_banner","-loglevel","error","-y","-ss",str(t),
         "-i",str(video),"-frames:v","1","-vf","scale=640:-2", "-c:v","png", str(path)])
    return Image.open(path).convert("RGB")
def main():
    video=Path(sys.argv[1]);out=Path(sys.argv[2]);out.mkdir(parents=True,exist_ok=True)
    raw=probe(video)
    track=next(s for s in raw["streams"] if s["codec_type"]=="video")
    duration=float(track.get("duration") or raw["format"]["duration"])
    # Source has no sound by pedagogical design.
    assert 19<duration<35,("Unexpected actual picture duration",duration)
    assert int(track["width"])>=1280 and int(track["height"])>=720
    times=[.7,2.2,3.6,4.7,5.6,7.2,8.4,10.0,12.0,13.8,15.7,17.8,19.1,21.3,22.8]
    times=[t for t in times if t<duration-.2]
    imgs=[];stats=[];tiles=[]
    for i,t in enumerate(times):
        path=out/f"frame_{i:02d}.png"
        img=extract(video,t,path)
        std=ImageStat.Stat(img.convert("L")).stddev[0]
        stats.append({"time":t,"contrast_sd":round(std,2)})
        imgs.append(img)
        tile=Image.new("RGB",(482,300),"#0B192C")
        small=ImageOps.contain(img,(476,268))
        tile.paste(small,((482-small.width)//2,0))
        ImageDraw.Draw(tile).text((15,275),f"t={t:.1f}s",fill="#EDF3FA")
        tiles.append(tile)
    cols=4;rows=(len(tiles)+cols-1)//cols
    sheet=Image.new("RGB",(cols*482,rows*300),"#0B192C")
    for i,im in enumerate(tiles):sheet.paste(im,((i%cols)*482,(i//cols)*300))
    sheet.save(out/"contact_sheet_v8.jpg",quality=91)
    # Per-pixel difference over the λ-ramp. Detect a static stand-in
    # or a camera substitution masquerading as deformation.
    movement=[]
    for i in range(2,5):
        a,b=imgs[i],imgs[i+1]
        diff=ImageChops.difference(a,b)
        mean=sum(ImageStat.Stat(diff).mean)/3
        movement.append(round(mean,3))
    assert min(movement)>.12,("Insufficient visible load movement",movement)
    assert min(s["contrast_sd"] for s in stats)>5,"Near-blank transitional frame: redesign the crossfade"
    fr=subprocess.run(["ffmpeg","-hide_banner","-loglevel","info","-i",str(video),
             "-vf","freezedetect=n=-60dB:d=3","-f","null","-"],capture_output=True,text=True)
    frozen=[line.strip() for line in fr.stderr.splitlines() if "freeze_duration:" in line]
    result={"duration":duration,"resolution":[int(track["width"]),int(track["height"])],
            "fps":track["avg_frame_rate"],"motion_3_to_6_seconds":movement,
            "static_warnings":frozen,"samples":stats,
            "limitations":"Sampled QA does not certify aesthetics or frame-by-frame correct physical signs."}
    (out/"qa_v8.json").write_text(json.dumps(result,ensure_ascii=False,indent=2))
    print(json.dumps({k:result[k] for k in ["duration","resolution","motion_3_to_6_seconds","static_warnings"]},ensure_ascii=False,indent=2))
if __name__=="__main__":main()
