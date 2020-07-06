# -*- coding: utf-8 -*
import Tkinter
import tkFont

# 计算
def calculate():
    try:
        # eval()是python的内置函数, 用来执行一个字符串表达式，并返回表达式的值。
        # display_str.get()获取此时display_str内容
        result = eval(display_str.get())
        # 拼接
        display_str.set(display_str.get() + "=\n" + str(result))
    except:
        display_str.set("ERROR")


# 将数字显示在文本框中
def show(buttonString):
    content = display_str.get()
    # 判断，如果内容为0的话相当于没计算，所以空字符串拼接，还是0
    # 如果内容为10的话，content就为10，再拼接我们所按的数字
    if content == "0":
        content = ""
    if "\n" in content: #未清零，进行连续运算
        content = content.split('\n')[1] 
    display_str.set(content + buttonString)


# 清除，置为0
def clear():
    display_str.set("0")


# 退位
def backSpace():
    # 删除前一个字符
    display_str.set(str(display_str.get()[:-1]))
    

# 主程序
root = Tkinter.Tk()
# 设置程序标题
root.title("简易计算器")
# 设在背景颜色
root.configure(bg='black')
# 框体可拖拽，0,0表示不能拖拽
root.resizable(0, 0)
# display_str 是存放显示区的数字
display_str = Tkinter.StringVar()
# 默认为0
display_str.set("0")

# 设置字体大小
font_ = tkFont.Font(family="Arial", size=20)


# 设置文本框
label = Tkinter.Label(root, width=30, height=3, fg='white', bg='black', relief="raised", anchor=Tkinter.SE, textvariable=display_str, font=font_)
label.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

# 第一行
# 清除显示区按钮AC
# text  按钮上的文字
# fg 前景色彩
# bg 背景色彩
buttonClear = Tkinter.Button(root, text="AC", width=5, height=3, fg='black', bg="#C0C0C0", command=clear, font=font_)
buttonClear.grid(row=1, column=0, pady=10)

# 退位键按钮
buttonBack = Tkinter.Button(root, text="退格", width=5, height=3, fg='black', bg="#C0C0C0", command=backSpace, font=font_)
buttonBack.grid(row=1, column=1, pady=10)

# 余按钮
# lambda函数  传参的话需要运用这个lambda
buttonYu = Tkinter.Button(root, text="%", width=5, height=3, fg='black', bg="#C0C0C0", command=lambda: show("%"), font=font_)
buttonYu.grid(row=1, column=2, pady=10)

# 除按钮
buttonDivision = Tkinter.Button(root, text="/", width=5, height=3, fg='white', bg="orange", command=lambda: show("/"), font=font_)
buttonDivision.grid(row=1, column=3, pady=10)

# 第二行
# 数字7
button7 = Tkinter.Button(root, text="7", width=5, height=3, fg='white', bg="#696969", command=lambda: show("7"), font=font_)
button7.grid(row=2, column=0, pady=10)

# 数字8
button8 = Tkinter.Button(root, text="8", width=5, height=3, fg='white', bg="#696969", command=lambda: show("8"), font=font_)
button8.grid(row=2, column=1, pady=10)

# 数字9
button9 = Tkinter.Button(root, text="9", width=5, height=3, fg='white', bg="#696969", command=lambda: show("9"), font=font_)
button9.grid(row=2, column=2, pady=10)

# 乘法按钮
buttonMultiplication = Tkinter.Button(root, text="*", width=5, height=3, fg='white', bg="orange", command=lambda: show("*"), font=font_)
buttonMultiplication.grid(row=2, column=3, pady=10)

# 第三行
# 数字4
button4 = Tkinter.Button(root, text="4", width=5, height=3, fg='white', bg="#696969", command=lambda: show("4"), font=font_)
button4.grid(row=3, column=0, pady=10)

# 数字5
button5 = Tkinter.Button(root, text="5", width=5, height=3, fg='white', bg="#696969", command=lambda: show("5"), font=font_)
button5.grid(row=3, column=1, pady=10)

# 数字6
button6 = Tkinter.Button(root, text="6", width=5, height=3, fg='white', bg="#696969", command=lambda: show("6"), font=font_)
button6.grid(row=3, column=2, pady=10)

# 减法按钮
buttonSubtraction = Tkinter.Button(root, text="-", width=5, height=3, fg='white', bg="orange", command=lambda: show("-"), font=font_)
buttonSubtraction.grid(row=3, column=3, pady=10)

# 第四行
# 数字1
button1 = Tkinter.Button(root, text="1", width=5, height=3, fg='white', bg="#696969", command=lambda: show("1"), font=font_)
button1.grid(row=4, column=0, pady=10)

# 数字2
button2 = Tkinter.Button(root, text="2", width=5, height=3, fg='white', bg="#696969", command=lambda: show("2"), font=font_)
button2.grid(row=4, column=1, pady=10)

# 数字3
button3 = Tkinter.Button(root, text="3", width=5, height=3, fg='white', bg="#696969", command=lambda: show("3"), font=font_)
button3.grid(row=4, column=2, pady=10)

# 加法按钮
buttonAdd = Tkinter.Button(root, text="+", width=5, height=3, fg='white', bg="orange", command=lambda: show("+"), font=font_)
buttonAdd.grid(row=4, column=3, pady=10)

# 第五行
# 小数点按钮
buttonPoint = Tkinter.Button(root, text=".", width=5, height=3, fg='white', bg="#696969", command=lambda: show("."), font=font_)
buttonPoint.grid(row=5, column=0, pady=10)

# 数字0
button0 = Tkinter.Button(root, text="0", width=5, height=3, fg='white', bg="#696969", command=lambda: show("0"), font=font_)
button0.grid(row=5, column=1, pady=10)

# 等于号
buttonEqual = Tkinter.Button(root, text="=", width=13, height=3, fg='white', bg="orange", command=calculate, font=font_)
buttonEqual.grid(row=5, column=2, columnspan=2, pady=10)

# 程序循环进行
root.mainloop()