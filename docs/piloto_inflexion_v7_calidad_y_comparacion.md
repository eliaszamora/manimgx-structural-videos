# V7 — Pilot: structural inflection as a visual discovery (2026-10-12)

## Verified deliverables
- 32.0 s H.264 1920×1080, 30 fps, intentionally silent.
- **GitHub Actions pass:** https://github.com/eliaszamora/manimgx-structural-videos/actions/runs/38276012857
- Final download in the run's `PILOT-V7-INFLECTION-MANIMGX` artifact.
- 14 timeline snapshots, 5/5 numerical checks (deformation linear interpolation, joint load anchoring, inflection from FEM M=0, opposite curvatures, diagram based on undeformed axis).
- ManimGX render: `layout: no problems in 39 samples`.
- Inflection `z = 1.9787 m` from base, corresponding to `M(z)=-23.7307+11.9931z` (kN m, kN).
- Support hatching and load at physical right roof joint.

## Visual direction
One concept in ~32 s: load → continuous portal deformation → isolate enlarged left column → move tangent along FEM curve → geometric inflection (continuous member, no hinge) → signed triangular M over the original column axis.

### What improved from V6
- One visual claim, without cluttered panel and all-force data tables.
- Geometric zoom and moving tangent, not a separate graph detached from the structure.
- Actual inflection location derived from local bending moment, never visually guessed.
- Positive M on right of original upward local axis and negative left (documented convention).

### Issues STILL present
- Four plus seconds of final-held diagram and two over-3 s static stretches (including a 6.3 s warning). These are editorial rhythm shortcomings despite layout tests passing.
- Sign diagram lacks a displayed free-body argument; it shows a mathematically correct distribution, not yet a full equilibrium proof.
- No audio: intentionally postponed until the silent visual sequence is judged instructive. The selected future narrator is Kokoro `em_alex` natural.
- Only the LEFT column is spotlighted; this is a one-question pilot, not a complete M/V/N pórtico lesson.
- No actual Motion Canvas video rendered yet, hence no defensible engine quality/performance comparison.

## Alternative engine
Motion Canvas 3.17 source at `motion_canvas_pilot`; identical FEM exported by `export_fem.py`. Vite build passed:
https://github.com/eliaszamora/manimgx-structural-videos/actions/runs/38276512201

Headless MP4 export for Motion Canvas needs automation of the web editor or a proper renderer wrapper; simply compiling the scene is not a render.

## Next acceptance gate
Before lengthening this study or adding narration: compare matched timestamps of ManimGX and Motion Canvas moving geometry, verify typography at 390 px and eliminate static holds above 4 s. Independent structural error checks remain mandatory. Do not describe this pilot as already equivalent to 3Blue1Brown or The Efficient Engineer.
