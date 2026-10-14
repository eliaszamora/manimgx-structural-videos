"""Post-render QA for the title-free 3D P-M lecture.
Not a substitute for a human review of signs, meaning, and camera composition.
"""
from pathlib import Path
from subprocess import run, check_output
import argparse,json,io,math
from PIL import Image,ImageDraw,ImageStat
from story import BEATS,TOTAL_SECONDS

def runqa(video:Path,dst:Path):
    dst.mkdir(parents=True,exist_ok=True)
    meta=json.loads(check_output(["ffprobe","-v","error","-show_entries",
          "format=duration:stream=codec_type,width,height,duration",
          "-of","json",str(video)],text=True))
    secs=float(meta["format"]["duration"])
    assert abs(secs-TOTAL_SECONDS)<=2, f"Video container duration {secs} != {TOTAL_SECONDS}"
    streams=meta["streams"]
    a=next((s for s in streams if s.get("codec_type")=="audio"),None)
    v=next((s for s in streams if s.get("codec_type")=="video"),None)
    assert a and v, "Expected video and voice stream"
    assert abs(float(v.get("duration") or secs)-secs)<1.0,"Visual stream truncated"
    assert abs(float(a.get("duration") or secs)-secs)<1.0,"Audio stream truncated"
    times=[];offset=0
    for b in BEATS:
        times.append((b["id"],offset+b["duration"]*.57))
        offset+=b["duration"]
    assert offset==TOTAL_SECONDS
    tiles=[];quality=[]
    for ident,t in times:
        p=dst/f"chapter_{ident}.jpg"
        run(["ffmpeg","-hide_banner","-loglevel","error","-y",
             "-ss",f"{t:.3f}","-i",str(video),"-frames:v","1",
             "-vf","scale=640:-2",str(p)],check=True)
        im=Image.open(p).convert("RGB")
        tile=im.resize((426,240))
        stat=ImageStat.Stat(tile.convert("L"))
        sd=float(stat.stddev[0])
        quality.append({"chapter":ident,"at":round(t,1),"luma_std":round(sd,2),"near_blank":sd<3})
        labelled=Image.new("RGB",(440,266),"#061521")
        labelled.paste(tile,(7,5))
        ImageDraw.Draw(labelled).text((12,246),f"CAP {ident}    t={t:.1f}s",fill="#A9BBCF")
        tiles.append(labelled)
    sheet=Image.new("RGB",(440*4,266*math.ceil(len(tiles)/4)),"#061521")
    for i,p in enumerate(tiles):sheet.paste(p,((i%4)*440,(i//4)*266))
    sheet.save(dst/"contact_sheet_21.jpg",quality=91)
    for i in [0,5,12,17,20]:
        im=Image.open(dst/f"chapter_{i+1:02d}.jpg")
        im.resize((390,219)).save(dst/f"mobile_{i+1:02d}.jpg",quality=92)
    report={
      "container_seconds":secs,
      "expected_seconds":TOTAL_SECONDS,
      "width":v["width"],"height":v["height"],
      "chapters":quality,
      "automatic_pass":sum(int(r["near_blank"]) for r in quality)==0,
      "human_review_mandatory":[
          "3D column never obscures equations or bars",
          "Whitney block extends from compression face, neutral plane at c",
          "steel layer colors and epsilon direction are correct",
          "3D camera orbits reveal geometry, no cuts mistaken for deformations",
          "at 390px equations remain legible, no original heading bands",
          "narration matches what the viewer can see and is not robotic"]
    }
    (dst/"report.json").write_text(json.dumps(report,ensure_ascii=False,indent=2))
    assert report["automatic_pass"],"Found near-empty sample frames"
    print(json.dumps(report,ensure_ascii=False,indent=2))
if __name__=="__main__":
    ap=argparse.ArgumentParser();ap.add_argument("mp4");ap.add_argument("--out",default="build/pm_3d/qa")
    opt=ap.parse_args();runqa(Path(opt.mp4),Path(opt.out))
