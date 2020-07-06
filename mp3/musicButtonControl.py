# -*- coding: utf-8 -*
import tkinter
import pygame
import os
from tkinter import filedialog
from shutil import copyfile

class MusicButtonControl(tkinter.Frame):
    def __init__(self, master, otherMusicList):
        # 音乐目录
        self.path = "/home/pi/code/mp3/music"
        # Frame 是屏幕上的一块矩形区域 用来作为容器布局窗口
        self.frame = tkinter.Frame(master)
        self.frame.pack(side=tkinter.TOP, fill=tkinter.Y)

        # 加载音乐列表
        self.otherMusicList = otherMusicList
        self.loadMusic()
        print("======音乐加载完成")
        # command：指定Button控件绑定的事件处理函数
        self.buttonPlay = tkinter.Button(self.frame, text="播放",
                                         command=self.playMusic,
                                         width=8, height=2,bg='#FFEC8B')
        # 绑定控件后，需要使用pack()函数将其在父窗口显示出来
        self.buttonPlay.pack(side=tkinter.LEFT, fill=tkinter.X)

        self.buttonPause = tkinter.Button(self.frame, text="暂停",
                                          command=self.pauseMusic,
                                         width=8, height=2,bg='#FFEC8B')
        self.buttonPause.pack(side=tkinter.LEFT, fill=tkinter.X)

        self.buttonStop = tkinter.Button(self.frame, text="停止",
                                         command=self.stopMusic,
                                         width=8, height=2,bg='#FFEC8B')
        self.buttonStop.pack(side=tkinter.LEFT, fill=tkinter.X)

        self.buttonPrevious = tkinter.Button(self.frame, text="上一曲",
                                             command=self.previousMusic,
                                         width=8, height=2,bg='#FFEC8B')
        self.buttonPrevious.pack(side=tkinter.LEFT, fill=tkinter.X)

        self.buttonNext = tkinter.Button(self.frame, text="下一曲",
                                         command=self.nextMusic,
                                         width=8, height=2,bg='#FFEC8B')
        self.buttonNext.pack(side=tkinter.LEFT, fill=tkinter.X)

        self.buttonAdd = tkinter.Button(self.frame, text="添加音乐",
                                         command=self.addMusic,
                                         width=8, height=2,bg='#FFEC8B')
        self.buttonAdd.pack(side=tkinter.LEFT, fill=tkinter.X)

    def loadMusic(self):
        pygame.mixer.init()

    def playMusic(self):
        pygame.mixer.music.load(self.otherMusicList.getCurrentMusicPath())
        pygame.mixer.music.play()
        print(self.otherMusicList.getCurrentMusicPath())

    def pauseMusic(self):
        pygame.mixer.music.pause()

    def stopMusic(self):
        pygame.mixer.music.stop()

    def previousMusic(self):
        path = "/home/pi/code/mp3/music"
        currentMusicPath = self.otherMusicList.getCurrentMusicPath()

        for musicpathIndex in range(self.otherMusicList.listBox.size()):
            ismusic = 0
            musicAbs1Path = path + "/" + self.otherMusicList.listBox.get(musicpathIndex)
            if currentMusicPath == musicAbs1Path:
                ismusic = musicpathIndex
                ismusic -= 1
                # 通过索引，获取listBox中的内容
                musicAbsPath = path + "/" + self.otherMusicList.listBox.get(ismusic)
                if ismusic < 0:
                    pygame.mixer.music.load(path + "/" + self.otherMusicList.listBox.get(0))
                    pygame.mixer.music.play()
                    break
                pygame.mixer.music.load(musicAbsPath)
                # 显示正在播放的歌曲，并取消上一首歌曲的选中
                self.otherMusicList.listBox.select_clear(musicpathIndex)
                self.otherMusicList.listBox.select_set(ismusic)
                pygame.mixer.music.play()
                break

    def nextMusic(self):
        path = "/home/pi/code/mp3/music"
        currentMusicPath = self.otherMusicList.getCurrentMusicPath()

        for musicpathIndex in range(self.otherMusicList.listBox.size()):
            ismusic = 0
            musicAbs1Path = path + "/" + self.otherMusicList.listBox.get(musicpathIndex)
            if currentMusicPath == musicAbs1Path:
                ismusic = musicpathIndex
                ismusic += 1
                if ismusic >= self.otherMusicList.listBox.size():
                    pygame.mixer.music.load(path + "/" + self.otherMusicList.listBox.get(self.otherMusicList.listBox.size()-1))
                    pygame.mixer.music.play()
                    break
                musicAbsPath = path + "/" + self.otherMusicList.listBox.get(ismusic)
                pygame.mixer.music.load(musicAbsPath)
                # 显示正在播放的歌曲，并取消上一首歌曲的选中
                self.otherMusicList.listBox.select_clear(musicpathIndex)
                self.otherMusicList.listBox.select_set(ismusic)
                pygame.mixer.music.play()
                break

    def addMusic(self):
        file_path = filedialog.askopenfilename()
        music_name = file_path.split("/")[-1]
        copyfile(file_path, os.path.join(self.path, music_name))
        self.otherMusicList.addMusicList(file_path)
        