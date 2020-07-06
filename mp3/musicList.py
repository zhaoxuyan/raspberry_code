# -*- coding: utf-8 -*
import tkinter
import os
import pygame

class MusicList(tkinter.Frame):
    def __init__(self, master):
        # Frame 是屏幕上的一块矩形区域 用来作为容器布局窗口
        self.frame = tkinter.Frame(master)
        self.frame.pack(side=tkinter.LEFT, fill=tkinter.Y)

        self.lv = tkinter.StringVar()
        # 创建一个listbox
        self.listBox = tkinter.Listbox(self.frame, selectmode=tkinter.BROWSE, width=30,
                                       height=30, bg="#FFFACD",listvariable=self.lv)
        self.listBox.pack()

        # 添加音乐曲目
        self.initMusicList()

        # 事件绑定 参数1：事件的字符串模式, 参数2：事件监听的处理函数
        self.listBox.bind("<Double-Button-1>", self.playMusic)

    def playMusic(self, event):
        pygame.mixer.init()
        pygame.mixer.music.load(self.getCurrentMusicPath())
        pygame.mixer.music.play()

    def getCurrentMusicPath(self):
        path = "/home/pi/code/mp3/music"
        # self.listBox.select_set(0)
        for item in range(self.listBox.size()):
            musicAbsPath = path + "/" + self.listBox.get(item)
            if self.listBox.selection_includes(item):
                path = musicAbsPath
                # print("-----", path)
        return path

    # 初始化音乐曲目
    def initMusicList(self):
        path = "/home/pi/code/mp3/music"
        musicNameList = os.listdir(path)
        for musicName in musicNameList:
            path1 = os.path.join(path, musicName)
            path1list = os.path.splitext(path1)
            if path1list[-1] == ".mp3":
                self.listBox.insert(tkinter.END, musicName)
    
    # 添加音乐曲目
    def addMusicList(self, music_path):
        music_name = music_path.split("/")[-1]
        print(music_name)
        self.listBox.insert(tkinter.END, music_name)