#!python3
# -*- coding: utf-8 -*-
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import ffmpeg


def main(in_dir, out_file, height=1440, fps=10, cmd='ffmpeg',
         text_font='DejaVuSans.ttf',
         text_color=(255, 0, 0),
         text_pos=(0.005, 0.005),
         text_size=0.03):

    img_dir = Path(in_dir)
    img_paths = sorted(img_dir.glob('*'))
    img0 = Image.open(img_paths[0])
    W, H = img0.size
    width = int(height * W / H)

    if out_file.endswith('avi'):
        proc = (
            ffmpeg
            .input('pipe:', format='rawvideo', pix_fmt='rgb24', s='{}x{}'.format(width, height), r=str(fps))
            .output(out_file, r=str(fps), vcodec='mpeg4', vtag='xvid', qscale='1')
            .overwrite_output()
            .run_async(pipe_stdin=True)
        )
    else:
        proc = (
            ffmpeg
            .input('pipe:', format='rawvideo', pix_fmt='rgb24', s='{}x{}'.format(width, height), r=str(fps))
            .output(out_file, r=str(fps), crf='18')
            .overwrite_output()
            .run_async(pipe_stdin=True)
        )

    yield len(img_paths)

    for i, img_path in enumerate(img_paths):
        img = Image.open(img_path)
        W, H = img.size

        if text_font:
            t_pos_x, t_pos_y = text_pos
            t_pos_x = int(t_pos_x * W) if t_pos_x < 1 else t_pos_x
            t_pos_y = int(t_pos_y * H) if t_pos_y < 1 else t_pos_y
            t_size = int(text_size * H) if text_size < 1 else text_size
            text = img_path.name
            draw = ImageDraw.Draw(img)
            fontStyle = ImageFont.truetype(text_font, t_size, encoding="utf-8")
            draw.text((t_pos_x, t_pos_y), text, text_color, font=fontStyle)

        img2 = img.resize((width, height), Image.Resampling.LANCZOS)

        yield i
        stream = img2.tobytes()
        proc.stdin.write(stream)

    proc.stdin.close()
    proc.wait()
