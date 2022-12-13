#!python3
# -*- coding: utf-8 -*-
import tkinter as tk
import tkinter.font as tkFont
from tkinter import ttk


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        # root window
        self.title('Theme Demo')
        self.geometry('400x300')
        self.style = ttk.Style(self)

        # label
        label = ttk.Label(self, text='Name:')
        label.grid(column=0, row=0, padx=10, pady=10,  sticky='w')
        # entry
        textbox = ttk.Entry(self)
        textbox.grid(column=1, row=0, padx=10, pady=10,  sticky='w')
        # button
        btn = ttk.Button(self, text='Show')
        btn.grid(column=2, row=0, padx=10, pady=10,  sticky='w')

        # radio button
        self.selected_theme = tk.StringVar()
        theme_frame = ttk.LabelFrame(self, text='Themes')
        theme_frame.grid(column=0, row=1, padx=10, pady=10, ipadx=20, ipady=20, sticky='w')

        for theme_name in self.style.theme_names():
            rb = ttk.Radiobutton(
                theme_frame,
                text=theme_name,
                value=theme_name,
                variable=self.selected_theme,
                command=self.change_theme)
            rb.pack(expand=True, fill='both')

        # font
        font_frame = ttk.LabelFrame(self, text='Fonts')
        font_frame.grid(column=1, row=1, rowspan=2, padx=10, pady=10, ipadx=20, ipady=20, sticky='w')
        options = list(tkFont.families())
        self.selected_font = tk.StringVar()
        self.selected_font.set(options[0])
        self.font_drop = tk.OptionMenu(font_frame, self.selected_font, *options)
        self.font_drop.pack()
        self.font_text = tk.Label(font_frame, text='ABCabc123汉字')
        self.font_text.pack()

        self.selected_font.trace("w", self.change_font)

    def change_theme(self):
        self.style.theme_use(self.selected_theme.get())

    def change_font(self, *args):
        new_font = tkFont.Font(family=self.selected_font.get())
        self.font_text['font'] = new_font

if __name__ == "__main__":
    app = App()
    app.mainloop()
