"""Final audio/video and storyboard sampling QA for the five-act P-M film.

Cannot certify engineering interpretation visually; attaches evidence for manual review.
"""
from pathlib import Path
import argparse,subprocess,json,math
from PIL import Image,ImageOps,ImageDraw,ImageStat
try:
    from .story import BEATS,TOTAL_SECONDS
except ImportError:
    from story import BEATS,TOTAL_SECONDS

def probe(file):
    return json.loads(subprocess.check_output(["ffprobe","-v","error",
         "-show_entries","format=duration,size:stream=codec_type,width,height,duration",
         "-of","json",str(file)],text=True))

def inspect(video,dst):
    video=Path(video);dst=Path(dst);dst.mkdir(parents=True,exist_ok=True)
    m=probe(video)
    secs=float(m["format"]["duration"])
    streams=m["streams"]
    vs=next((s for s in streams if s["codec_type"]=="video"),None)
    aus=next((s for s in streams if s["codec_type"]=="audio"),None)
    assert vs and aus,"Video and narration both required"
    vd=float(vs.get("duration") or secs);ad=float(aus.get("duration") or secs)
    assert abs(secs-TOTAL_SECONDS)<1.5,(secs,TOTAL_SECONDS)
    assert abs(vd-TOTAL_SECONDS)<1.,("truncated video",vd,TOTAL_SECONDS)
    assert abs(ad-TOTAL_SECONDS)<1.,("truncated audio",ad,TOTAL_SECONDS)
    assert vs["width"]>=1280 and vs["height"]>=720
    off=0;tiles=[];frames=[];flags=[]
    for n,beat in enumerate(BEATS,1):
        time=off+.52*beat["duration"]
        path=dst/f"chapter_{n:02d}.jpg"
        subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-y",
                        "-ss",str(time),"-i",str(video),"-frames:v","1",
                        "-vf","scale=640:-2",str(path)],check=True)
        im=Image.open(path).convert("RGB")
        stat=ImageStat.Stat(im.convert("L")).stddev[0]
        flags.append({"chapter":n,"time":round(time,1),"sd_luma":round(stat,1),
                      "blank":stat<3})
        sm=ImageOps.contain(im,(426,240))
        tile=Image.new("RGB",(440,268),"#0A101D")
        tile.paste(sm,((440-sm.width)//2,4))
        ImageDraw.Draw(tile).text((11,247),f"CAP {n:02d}    t={time:.1f}s",fill="#A9B9CC")
        tiles.append(tile)
        frames.append(path)
        off+=beat["duration"]
    assert off==TOTAL_SECONDS
    sheet=Image.new("RGB",(440*4,268*math.ceil(len(tiles)/4)),"#0A101D")
    for i,x in enumerate(tiles):sheet.paste(x,((i%4)*440,(i//4)*268))
    sheet.save(dst/"storyboard_21_chapters.jpg",quality=90)
    for idx in (1,5,10,13,14,18,20,21):
        orig=Image.open(frames[idx-1])
        orig.resize((390,219)).save(dst/f"mobile_{idx:02d}.jpg")
    freezes=subprocess.run(["ffmpeg","-hide_banner","-loglevel","info",
      "-i",str(video),"-vf","freezedetect=n=-60dB:d=8",
      "-an","-f","null","-"],capture_output=True,text=True)
    alarms=[x.strip() for x in freezes.stderr.splitlines() if "freeze_duration:" in x]
    report={"duration":secs,"video_stream":vd,"audio_stream":ad,
            "video_width":vs["width"],"video_height":vs["height"],
            "near_blank_frames":[x for x in flags if x["blank"]],
            "samples":flags,"freeze_over_8s":alarms,
            "manual_checks_required":[
             "Audio matches gestures at all 21 chapter timestamps",
             "3D and 2D use same physical bending plane and compression face",
             "Strain profile continuous, compressive top plus 0.003",
             "Bar steel colors match sign of stress",
             "Force signs and bending arms match model",
             "Whitney a and neutral axis c are distinct",
             "Diagram nominal versus phi-reduced construction is faithful",
             "No text overlaps at 390 pixel simulation",
             "Full video watched, not just sampled frames"]}
    (dst/"audit_report.json").write_text(json.dumps(report,ensure_ascii=False,indent=2))
    assert not report["near_blank_frames"],"One or more chapters are blank"
    print(json.dumps({k:v for k,v in report.items() if k!="samples"},indent=2,ensure_ascii=False))
if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("file")
    p.add_argument("--out",default="build/final/qa")
    args=p.parse_args();inspect(args.file,args.out)
