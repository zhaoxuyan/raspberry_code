# -*- coding: utf-8 -*
import tkinter

from musicList import MusicList
from musicButtonControl import MusicButtonControl

# 实例化一个父窗口
win = tkinter.Tk()
win.title("音乐播放器")
# 宽x高+左边距+上边距
win.geometry("800x500+200+100")


musicList = MusicList(win)
musicButton = MusicButtonControl(win, musicList)

win.mainloop()