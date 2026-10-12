"""Video audit: chapter contact-sheet, mobile checks, duration, motion warnings.

Human review is required: neither static frames nor formal equations can certify
that the visual explanations are mechanically correct.
"""
from pathlib import Path
from subprocess import run,check_output
import argparse,json,sys
from PIL import Image,ImageOps,ImageDraw,ImageFont,ImageStat

def probe(path):
    return json.loads(check_output(
        ["ffprobe","-v","error","-show_entries",
         "format=duration,size:stream=codec_type,codec_name,width,height,avg_frame_rate,duration",
         "-of","json",str(path)],text=True))

def snapshot(video,time,out,width=640):
    run(["ffmpeg","-hide_banner","-loglevel","error","-y",
         "-ss",str(time),"-i",str(video),"-frames:v","1",
         "-vf",f"scale={width}:-2",str(out)],check=True)
    return Image.open(out).convert("RGB")

def audit(video,target,expected):
    target.mkdir(parents=True,exist_ok=True)
    info=probe(video)
    duration=float(info["format"]["duration"])
    streams=info["streams"]
    vs=next((s for s in streams if s.get("codec_type")=="video"),None)
    audio=next((s for s in streams if s.get("codec_type")=="audio"),None)
    if not vs: raise AssertionError("Falta pista de video")
    video_seconds=float(vs.get("duration") or duration)
    if abs(video_seconds-expected)>2 or abs(video_seconds-duration)>2:
        raise AssertionError(f"Pista de video truncada: video={video_seconds:.2f}, contenedor={duration:.2f}, esperado={expected:.2f}")
    if audio and abs(float(audio.get("duration") or duration)-expected)>2:
        raise AssertionError("La pista de audio no cubre la duración del capítulo")
    if min(int(vs["width"]),int(vs["height"]))<720:
        raise AssertionError("Resolución inferior a 720p")
    if not abs(duration-expected)<2:
        raise AssertionError(f"Audio/video desincronizado: {duration} vs {expected}")
    if not audio: raise AssertionError("Falta pista de narración")
    from importlib.util import spec_from_file_location,module_from_spec
    # Story imported by caller's cwd without depending on renderer.
    times=[6,31,54,76,99,122,143,160] if expected==169 else [
        (i+.5)*duration/8 for i in range(8)]
    cards=[]
    chapter_quality=[]
    for i,t in enumerate(times):
        frame=target/f"chapter_{i+1:02d}.jpg"
        im=snapshot(video,t,frame)
        small=ImageOps.contain(im,(480,270))
        brightness=ImageStat.Stat(small.convert("L"))
        sd=float(brightness.stddev[0])
        quality={"chapter":i+1,"time":round(t,2),"luminance_sd":round(sd,2),
                 "near_blank":sd<3.0}
        chapter_quality.append(quality)
        canvas=Image.new("RGB",(486,302),"#182635")
        canvas.paste(small,((486-small.width)//2,8))
        d=ImageDraw.Draw(canvas)
        d.text((12,279),f"CAPITULO {i+1:02d}    t = {t:.1f}s",fill="#E8F1FC")
        cards.append(canvas)
    sheet=Image.new("RGB",(486*4,302*2),"#061320")
    for i,im in enumerate(cards):
        sheet.paste(im,((i%4)*486,(i//4)*302))
    sheet.save(target/"contact_sheet.jpg",quality=90)
    # 390-px-wide simulation catches common mobile reading-size problems.
    for index in [0,3,7]:
        im=Image.open(target/f"chapter_{index+1:02d}.jpg")
        mobile=ImageOps.contain(im,(390,220))
        mobile.save(target/f"mobile_{index+1:02d}.jpg",quality=90)
    freezes=run(["ffmpeg","-hide_banner","-loglevel","info","-i",str(video),
                 "-vf","freezedetect=n=-60dB:d=4","-an","-f","null","-"],
                capture_output=True,text=True,check=False)
    hits=[s.strip() for s in freezes.stderr.splitlines() if "freeze_duration:" in s]
    report={"duration":duration,"width":int(vs["width"]),"height":int(vs["height"]),
           "video_codec":vs.get("codec_name"),"audio_codec":audio.get("codec_name"),
           "chapters":chapter_quality,"freeze_warnings":hits,
           "human_review_required":[
             "Legibilidad de símbolos y etiquetas a 390px de ancho",
             "Colisiones entre flechas, diagramas y rótulos",
             "Signo/curvatura coherentes con convenciones del problema",
             "Sincronía semántica de cada frase con su acción visible",
             "Fluidez, volumen y pronunciación de la voz"] }
    (target/"qa_report.json").write_text(json.dumps(report,ensure_ascii=False,indent=2))
    print(json.dumps(report,ensure_ascii=False,indent=2))
    if sum(int(x["near_blank"]) for x in chapter_quality)>1:
        raise AssertionError("Demasiados capítulos con fotogramas casi vacíos")
    return report

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("video")
    p.add_argument("--out",default="build/video_qa")
    p.add_argument("--expected",type=float,default=169)
    a=p.parse_args()
    audit(Path(a.video),Path(a.out),a.expected)
