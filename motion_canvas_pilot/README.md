# Motion Canvas comparison — work in progress

Same 2D structural FEM model as ManimGX pilot in ../pilot_inflection.
It uses open-source Motion Canvas 3.17 to animate the pórtico and identify
the inflection point, with the same first-pass palette.

```sh
python -m pip install numpy
python export_fem.py
npm install
npm run build
npm run dev
```

Video export requires the Motion Canvas browser editor / FFmpeg exporter, or
a Playwright-controlled renderer. The free GitHub workflow currently verifies
the project build only. **Do not report quality/speed comparison from source
code alone.** See https://github.com/motion-canvas/motion-canvas/issues/1218
for current headless-rendering limitations.
