# Vector formulas and optional audio/video QA
- Typst formulas: `typst compile --format svg momento_curvatura.typ momento_curvatura.svg`.
- Optional word alignment: `pip install stable-ts` and `python studio_v3/qa/align_voice.py alex_natural.wav script.txt`.
- Optional scene changes: `pip install scenedetect opencv-python-headless` then `python studio_v3/qa/scene_detect.py VIDEO.mp4`.
- These are auxiliary tools. They do not replace FEM validation, ManimGX scenes, or human visual review.
