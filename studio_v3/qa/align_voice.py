"""Optional natural Alex word alignment. Uses a free Whisper tiny model (CPU)."""
import argparse
from pathlib import Path

def main():
    p=argparse.ArgumentParser()
    p.add_argument('audio')
    p.add_argument('script')
    p.add_argument('--out',default='aligned_words.json')
    a=p.parse_args()
    import stable_whisper
    model=stable_whisper.load_model('tiny',device='cpu')
    correct_text=Path(a.script).read_text(encoding='utf8')
    result=model.align(a.audio,correct_text,language='es')
    if result is None:raise RuntimeError('Word alignment failed. Keep original cues.')
    result.save_as_json(a.out)
    print('Saved alignment; inspect each technical term manually before using:',a.out)
if __name__=='__main__':main()
