"""Generate identical FEM source data for the Motion Canvas engine comparison."""
import sys,json
from pathlib import Path
root=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(root/"studio_v3"/"demo"))
from portal_solver import solve,H
r=solve("lateral")
sections=[]
for e in r["elements"]:
    sections.append(dict(original=[s["xy"] for s in e["samples"]],
                        displacement=[s["uxy"] for s in e["samples"]],
                        m0=e["samples"][0]["M"],m1=e["samples"][-1]["M"]))
left=sections[0]
fraction=-left["m0"]/(left["m1"]-left["m0"])
data=dict(segments=sections,inflection_t=fraction,inflection_height=fraction*H,
          height=H,load_kN=24.0,motion_amplification=155)
path=root/"motion_canvas_pilot"/"src"/"data.json"
path.parent.mkdir(parents=True,exist_ok=True)
path.write_text(json.dumps(data,separators=(',',':')),encoding="utf8")
print("Identical model exported",len(sections),"segments; z0",data["inflection_height"])
