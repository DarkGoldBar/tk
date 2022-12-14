#!python3
# -*- coding: utf-8 -*-
import sys
import time
import tkinter as tk
from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog
from threading import Thread
from queue import Queue
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
    fontStyle = ImageFont.truetype(text_font, encoding="utf-8")
    int(height)
    int(fps)

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
            font = fontStyle.font_variant(size=t_size)
            draw.text((t_pos_x, t_pos_y), text, text_color, font=font)

        img2 = img.resize((width, height), Image.Resampling.LANCZOS)

        yield i
        stream = img2.tobytes()
        proc.stdin.write(stream)

    proc.stdin.close()
    proc.wait()


class Application(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.top = LabelFrame(self, text=LABELS['lf1'])
        self.top.pack(padx=4, pady=4)
        self.top_label1 = Label(self.top, text=LABELS['l1'])
        self.top_text1 = Entry(self.top, width=40)
        self.top_btn1 = Button(self.top, text=LABELS['b1'], command=self.onClickInputBtn)
        self.top_label1.grid(row=0, column=0, padx=4, pady=4)
        self.top_text1.grid(row=0, column=1, padx=4, pady=4)
        self.top_btn1.grid(row=0, column=2, padx=4, pady=4)
        self.top_label2 = Label(self.top, text=LABELS['l2'])
        self.top_text2 = Entry(self.top, width=40)
        self.top_btn2 = Button(self.top, text=LABELS['b2'], command=self.onClickOutputBtn)
        self.top_label2.grid(row=1, column=0, padx=4, pady=4)
        self.top_text2.grid(row=1, column=1, padx=4, pady=4)
        self.top_btn2.grid(row=1, column=2, padx=4, pady=4)

        self.mid = LabelFrame(self, text=LABELS['lf2'])
        self.mid.pack(padx=4, pady=4)

        self.mid_op1_label = Label(self.mid, text=LABELS['op1'])  # height
        self.mid_op1_ctrl = Entry(self.mid)
        self.mid_op1_ctrl.insert(0, '1440')
        self.mid_op1_label.grid(row=0, column=0, padx=4, pady=4)
        self.mid_op1_ctrl.grid(row=0, column=1, padx=4, pady=4)
        self.mid_op2_label = Label(self.mid, text=LABELS['op2'])  # fps
        self.mid_op2_ctrl = Entry(self.mid)
        self.mid_op2_ctrl.insert(0, '10')
        self.mid_op2_label.grid(row=1, column=0, padx=4, pady=4)
        self.mid_op2_ctrl.grid(row=1, column=1, padx=4, pady=4)
        # self.mid_op3_label = Label(self.mid, text=LABELS['op3'])  # crf
        # self.mid_op3_ctrl = Entry(self.mid)
        # self.mid_op3_ctrl.insert(0, '18')
        # self.mid_op3_label.grid(row=2, column=0)
        # self.mid_op3_ctrl.grid(row=2, column=1)
        self.mid_op4_label = Label(self.mid, text=LABELS['op4'])  # ffmpeg
        self.mid_op4_ctrl = Entry(self.mid)
        self.mid_op4_ctrl.insert(0, 'ffmpeg')
        self.mid_op4_label.grid(row=3, column=0, padx=4, pady=4)
        self.mid_op4_ctrl.grid(row=3, column=1, padx=4, pady=4)
        self.mid_op5_var = BooleanVar(value=True)
        self.mid_op5 = Checkbutton(self.mid, text=LABELS['op5'], variable=self.mid_op5_var)  # text
        self.mid_op5.grid(row=4, column=0, columnspan=2)
        self.mid_op6_label = Label(self.mid, text=LABELS['op6'])  # text_font
        self.mid_op6_ctrl = Entry(self.mid)
        self.mid_op6_ctrl.insert(0, 'DejaVuSans.ttf')
        self.mid_op6_label.grid(row=5, column=0, padx=4, pady=4)
        self.mid_op6_ctrl.grid(row=5, column=1, padx=4, pady=4)
        self.mid_op7_label = Label(self.mid, text=LABELS['op7'])  # text_size
        self.mid_op7_ctrl = Entry(self.mid)
        self.mid_op7_ctrl.insert(0, '0.03')
        self.mid_op7_label.grid(row=6, column=0, padx=4, pady=4)
        self.mid_op7_ctrl.grid(row=6, column=1, padx=4, pady=4)

        self.run = Button(self, text=LABELS['b3'], command=self.onClickRunBtn)
        self.run.pack(padx=4, pady=4)

        self.progress = Progressbar(self, orient=HORIZONTAL, mode='determinate', length=400)
        self.progress.pack(padx=4, pady=4)

        self.bottom = LabelFrame(self, text=LABELS['lf3'])
        self.bottom.pack(padx=4, pady=4)
        self.bottom_text = Text(self.bottom)
        self.bottom_text.pack(padx=4, pady=4)

        self.mid_op5_var.trace('w', self.onChangeTextSW)

    def log(self, text):
        self.bottom_text.insert(END, text)
        self.bottom_text.see(END)

    def onClickInputBtn(self):
        path = filedialog.askdirectory()
        self.top_text1.delete(0, END)
        self.top_text1.insert(0, path)

    def onClickOutputBtn(self):
        path = filedialog.asksaveasfilename(
            defaultextension='.mp4',
            filetypes=[
                ('H.264', 'mp4'),
                ('Xvid', 'avi')]
        )
        self.top_text2.delete(0, END)
        self.top_text2.insert(0, path)

    def onChangeTextSW(self, *args):
        if not self.mid_op5_var.get():
            self.mid_op6_ctrl["state"] = DISABLED
            self.mid_op7_ctrl["state"] = DISABLED
        else:
            self.mid_op6_ctrl["state"] = NORMAL
            self.mid_op7_ctrl["state"] = NORMAL

    def onClickRunBtn(self):
        localtime = time.asctime(time.localtime(time.time()))
        self.log(localtime + '\n')

        args = {
            'in_dir': self.top_text1.get(),
            'out_file': self.top_text2.get(),
            'height': int(self.mid_op1_ctrl.get()),
            'fps': self.mid_op2_ctrl.get(),
            'cmd': self.mid_op4_ctrl.get(),
            'text_font': self.mid_op6_ctrl.get(),
            'text_color': (255, 0, 0),
            'text_pos': (0.005, 0.005),
            'text_size': float(self.mid_op7_ctrl.get()),
        }

        if not self.mid_op5_var.get():
            args['text_font'] = None

        self.log('\n'.join(f'{k}: {v}' for k, v in args.items()) + '\n')
        self.log('START\n')
        self.master.after(10, lambda: self._thread_start_ffmpeg(args))

    def _thread_start_ffmpeg(self, args):
        q = Queue()
        t = Thread(target=_main, args=[q, args])
        t.setDaemon(True)
        t.start()
        self.master.after(10, lambda: self._thread_update_ffmpeg(q, t))

    def _thread_update_ffmpeg(self, q: Queue, t: Thread):
        k, v = q.get()
        stop = True
        if k == 'maximum':
            self.progress['maximum'] = v
            stop = False
        elif k == 'value':
            self.progress['value'] = v
            if v < self.progress['maximum']:
                stop = False
        else:
            self.log(k + str(v) + '\n')

        if stop:
            t.join()
            self.log('DONE\n')
        else:
            self.master.after(10, lambda: self._thread_update_ffmpeg(q, t))


def _main(q, args):
    itermain = main(**args)
    try:
        max_value = next(itermain)
        q.put(('maximum', max_value))
        for i in itermain:
            q.put(('value', i))
        q.put(('value', max_value))
    except Exception:
        q.put(('error', sys.exc_info()))


LABELS = {
    'lf1': '输入输出设置',
    'lf2': '运行设置',
    'lf3': '日志',
    'l1': '输入文件夹',
    'l2': '输出文件',
    'b1': '选择',
    'b2': '选择',
    'b3': '运行',
    'op1': 'height',
    'op2': 'fps',
    'op3': 'crf',
    'op4': 'ffmpeg',
    'op5': 'text',
    'op6': 'text_font',
    'op7': 'text_size'
}


if __name__ == '__main__':
    root = tk.Tk()
    root.resizable(False, False)
    if sys.platform.startswith('linux'):
        import sv_ttk
        sv_ttk.set_theme("light")
        root.option_add("*font", "Ubuntu")
    app = Application(master=root)
    app.mainloop()
