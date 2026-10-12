"""Screen-safe 16:9 structural diagram design-system."""
from dataclasses import dataclass
@dataclass(frozen=True)
class Style:
    background: str='#0B1524'
    surface: str='#14243A'
    ink: str='#F3F7FC'
    muted: str='#B9C9D9'
    steel: str='#6D879B'
    deformed: str='#3BDCC4'
    load: str='#FF9F75'
    moment_positive: str='#FFDB91'
    moment_negative: str='#FF8C82'
    shear: str='#80BBFF'
    inflection: str='#C9A6FF'
    small_text_min: int=24
    label_text: int=29
    heading_text: int=35
STYLE=Style()
# Manim 16:9 camera coordinates ~14.2 x 8; all technical labels in +/- 6.0, +/- 2.9
SAFE_LEFT=-6.05;SAFE_RIGHT=6.05;SAFE_TOP=3.37;SAFE_BOTTOM=-3.05
