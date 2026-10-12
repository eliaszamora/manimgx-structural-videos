"""Simple deterministic QC for a visual-only prototype; no false 'perfect' claim."""
from pathlib import Path
from PIL import Image,ImageOps,ImageDraw,ImageStat
import sys,subprocess,json
def run(cmd):return subprocess.run(cmd,capture_output=True,text=True,check=True)
def probe(path):
  return json.loads(subprocess.check_output(["ffprobe","-v","error","-show_entries",
      "format=duration:stream=codec_type,width,height,duration,nb_frames,avg_frame_rate",
      "-of","json",str(path)],text=True))
def main():
  src=Path(sys.argv[1]);dest=Path(sys.argv[2]);dest.mkdir(parents=True,exist_ok=True)
  before=probe(src)
  v=next(s for s in before["streams"] if s["codec_type"]=="video")
  seconds=float(v.get("duration") or before["format"]["duration"])
  assert seconds>20,f"Render appears unexpectedly short: {seconds}"\n  # ManimGX may encode the final hold as container duration without packets;\n  # add up to seven seconds of end-hold and fade the final two seconds.
  # Keep Manim's presentation clock, pad only if source ends early; do not
  # stretch events by re-indexing all 60fps frames.
  final=dest/"Inflection_Visual_Pilot_V7.mp4"
  run(["ffmpeg","-hide_banner","-loglevel","error","-y","-i",str(src),
       "-vf","fps=30,tpad=stop_mode=clone:stop_duration=7,trim=duration=32,fade=t=out:st=30:d=2,format=yuv420p",
       "-an","-c:v","libx264","-preset","veryfast","-crf","20","-movflags","+faststart",str(final)])
  post=probe(final)
  assert abs(float(post["format"]["duration"])-32)<.15
  frames=[]
  times=[1,3,5,7,9,11.5,14,16.5,18.5,21,23.5,26,29.5,31.5]
  photos=[]
  for j,t in enumerate(times):
    p=dest/f"frame_{j:02d}.jpg"
    run(["ffmpeg","-hide_banner","-loglevel","error","-y","-ss",str(t),"-i",
         str(final),"-frames:v","1","-vf","scale=640:-2",str(p)])
    im=Image.open(p).convert("RGB")
    sd=ImageStat.Stat(im.convert("L")).stddev[0]
    frames.append({"seconds":t,"stdev":round(sd,2),"blank":sd<3})
    tile=Image.new("RGB",(480,294),"#111B27")
    small=ImageOps.contain(im,(474,266))
    tile.paste(small,((480-small.width)//2,0))
    ImageDraw.Draw(tile).text((14,271),f"{t:04.1f}s",fill="#D6E6F2")
    photos.append(tile)
  sheet=Image.new("RGB",(480*4,294*4),"#0B131C")
  for i,p in enumerate(photos):sheet.paste(p,((i%4)*480,(i//4)*294))
  sheet.save(dest/"qa_contact.jpg",quality=90)
  scan=subprocess.run(["ffmpeg","-hide_banner","-loglevel","info","-i",str(final),"-vf",
      "freezedetect=n=-60dB:d=3","-f","null","-"],capture_output=True,text=True)
  freezes=[x.strip() for x in scan.stderr.splitlines() if 'freeze_duration:' in x]
  report={"expected_seconds":32,"input_presentation_seconds":seconds,
     "output_seconds":float(post["format"]["duration"]),
     "resolution":[int(v["width"]),int(v["height"])],
     "frames":frames,"static_segments_over_3s":freezes,
     "human_checks":["Is applied force tail on moving joint?","Does column deform continuously?",
       "Do tangent rotations follow the FEM curve?","Is M=0 co-located with inflection?",
       "Are all titles/labels legible on a phone?"]}
  (dest/"qa_report.json").write_text(json.dumps(report,indent=2,ensure_ascii=False))
  print(json.dumps({"duration":report["output_seconds"],"blank_count":sum(f["blank"] for f in frames),
      "static_warning_count":len(freezes)},indent=2))
  assert not any(f["blank"] for f in frames),"Nearly empty QA frame"
if __name__=="__main__":main()
