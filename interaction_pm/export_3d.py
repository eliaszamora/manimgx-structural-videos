"""Join ManimGX native 3D track to Kokoro voice; enforce complete streams.

Usage:
 python interaction_pm/export_3d.py silent_full.mp4 narracion.wav final.mp4

The exporter does not silently shorten the last narrated segment.
"""
import subprocess,sys,json
from pathlib import Path

def probe(filename):
    raw=subprocess.check_output(["ffprobe","-v","error",
       "-show_entries","format=duration:stream=codec_type,duration",
       "-of","json",str(filename)],text=True)
    return json.loads(raw)
def streamtime(meta,name):
    stream=next((s for s in meta["streams"] if s["codec_type"]==name),None)
    if stream is None:raise ValueError(f"Missing {name} stream")
    return float(stream.get("duration") or meta["format"]["duration"])
def merge(silent,wav,output):
    silent=Path(silent);wav=Path(wav);output=Path(output)
    if not silent.is_file() or not wav.is_file():raise FileNotFoundError("Missing render or voice")
    vid=probe(silent);snd=probe(wav)
    vd=streamtime(vid,"video");ad=streamtime(snd,"audio")
    output.parent.mkdir(parents=True,exist_ok=True)
    args=["ffmpeg","-hide_banner","-loglevel","error","-y",
          "-i",str(silent),"-i",str(wav)]
    if abs(vd-ad)<.35:
        args+=["-map","0:v:0","-map","1:a:0",
                "-c:v","copy","-c:a","aac","-b:a","192k",
                "-t",str(ad),"-movflags","+faststart",str(output)]
    else:
        # Important: time pad must be LONGER than missing end of video,
        # or '-t ad' may leave the visual stream truncated.
        pad=max(35,ad-vd+15)
        args+=["-filter_complex",f"[0:v]tpad=stop_mode=clone:stop_duration={pad:.4f},format=yuv420p[v]",
                "-map","[v]","-map","1:a:0",
                "-c:v","libx264","-preset","ultrafast","-crf","20",
                "-fps_mode:v","vfr","-c:a","aac","-b:a","192k",
                "-t",str(ad),"-movflags","+faststart",str(output)]
    print("Joining",silent,wav,"video",vd,"audio",ad,flush=True)
    subprocess.run(args,check=True)
    final=probe(output)
    after_v=streamtime(final,"video");after_a=streamtime(final,"audio")
    assert abs(after_v-after_a)<.5,(after_v,after_a)
    assert abs(after_a-ad)<.5
    assert abs(float(final["format"]["duration"])-ad)<.5
    print("A/V validated:",after_v,after_a,"seconds","file:",output.stat().st_size)
if __name__=="__main__":
    if len(sys.argv)!=4:raise SystemExit("usage export_3d.py silent.mp4 narracion.wav output.mp4")
    merge(*sys.argv[1:])
