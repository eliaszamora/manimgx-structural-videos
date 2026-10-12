---
name: manimgx
description: Plan, render and inspect ManimGX mathematical and engineering animations with real-time state tracking and camera movement.
license: MIT
---

# ManimGX — project integration

Adapted from the official ManimGX skill, copyright Academa Labs (MIT):
https://github.com/academa-labs/manimgx/blob/main/skills/manimgx/SKILL.md

Use Python 3.13+, import \`manimgx as m\`, install with \`pip install manimgx\`.

## Authoring rules
- Use the actual ManimGX API; consult https://manimgx.academa.ai/llms.txt and https://manimgx.academa.ai/reference/ for unfamiliar arguments.
- For changing values create \`m.ValueTracker\`; derive continuous geometry using \`m.always_redraw\` or a reusable updater. An updater reads the current state rather than counting frames.
- For 2D moving cameras animate \`self.camera.frame\` (scale and move). Do not replace the mathematical subject with a separately drawn enlarged illustration when showing a zoom.
- Place structural force arrows on the applied node, and interpolate nodal positions using one load fraction.
- Verify the deformed shape and curvature using independent mechanics before rendering.

## Inspect and deliver
\`\`\`sh
manimgx inspect path/scene.py SceneClass -t 2,4,8,12,16,end
manimgx render path/scene.py SceneClass -r 1920x1080 --fps 30
\`\`\`

Inspect generates a storyboard and sampled layout checks. Render must also be audited as a moving MP4: sampled frames alone cannot confirm frame-by-frame mechanics.
Include the editable Python scene, storyboard, tests and MP4. Do not declare cinematic or pedagogical quality from CI success alone.
