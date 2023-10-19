import os
import random
import sys
from tkinter import *
import tkinter as tk
import time


# for i in range(15):
#     arr.append(random.randint(1, 8))

class ClockPageReplacement:
    def __init__(self, frame_count):
        self.frame_count = frame_count
        self.frames = [None] * frame_count
        self.hand = 0  # 时钟指针位置

    def page_in(self, page):
        temp = 0
        if page in self.frames:
            # 页面已存在于内存中，不执行替换
            temp = None
        else:
            while True:
                # 查找下一个需要替换的页面
                if self.frames[self.hand] is None:
                    # 如果页面为空或者未被引用，替换当前页面
                    self.frames[self.hand] = {'page': page, 'referenced': True}
                    temp = -1
                    break
                elif not self.frames[self.hand]['referenced']:
                    temp = self.frames[self.hand]["page"]
                    self.frames[self.hand] = {'page': page, 'referenced': True}
                    break
                else:
                    # 页面被引用，重置引用位并继续寻找
                    self.frames[self.hand]['referenced'] = False
                self.hand = (self.hand + 1) % self.frame_count
        return temp


def calPos(pos, n):
    return int(pos) + (n - 1) * 0x8000


def run1(inp, txt, arr, pos):
    page = int(inp.get())
    pos_start = int(pos.get(), 16)
    txt.insert(END, "FIFO页面置换过程为:\n")
    result = []
    loss_page = 0
    sum = 0
    for item in arr:
        if len(result) == page:
            for j in range(sum, len(arr)):
                if arr[j] in result:
                    txt.insert(END, "no exchange\n")
                else:
                    temp = int(result[0])
                    del result[0]
                    result.append(arr[j])
                    loss_page += 1
                    txt.insert(END, "\n")
                    txt.insert(END, "弹出页面的物理地址为：%s\n" % bin(calPos(pos_start, temp)).replace('0b', ''))
                    txt.insert(END, "弹出页面的相对页号为：%s\n" % temp)
                    txt.insert(END, "当前工作集内的页面为：")
                    txt.insert(END, result)
            break
        elif item in result:
            txt.insert(END, "no exchange\n")
            txt.insert(END, "当前工作集内的页面为：")
            txt.insert(END, result)
            sum += 1
        else:
            result.append(item)
            loss_page += 1
            sum += 1
            txt.insert(END, "\n")
            txt.insert(END, "当前工作集内的页面为：")
            txt.insert(END, result)
    result_page = float((loss_page + page) / len(arr))
    txt.insert(END, "FIFO缺页率为：%.2f\n" % result_page)
    txt.insert(END, "\n")


def run2(inp, txt, arr, pos):
    page = int(inp.get())
    pos_start = int(pos.get(), 16)
    txt.insert(END, "LRU页面置换过程为:\n")
    result = []
    loss_page = 0
    sum = 0
    for item in arr:
        if len(result) == page:
            for j in range(sum, len(arr)):
                if arr[j] in result:
                    txt.insert(END, "no exchange\n")
                    p = result[result.index(arr[j])]
                    del result[result.index(arr[j])]
                    result.insert(0, p)
                    txt.insert(END, "\n")
                    txt.insert(END, "当前工作集内的页面为：")
                    txt.insert(END, result)
                else:
                    temp = int(result[-1])
                    del result[-1]
                    result.insert(0, arr[j])
                    loss_page += 1
                    txt.insert(END, "\n")
                    txt.insert(END, "弹出页面的物理地址为：%s\n" % bin(calPos(pos_start, temp)).replace('0b', ''))
                    txt.insert(END, "弹出页面的相对页号为：%s\n" % temp)
                    txt.insert(END, "当前工作集内的页面为：")
                    txt.insert(END, result)
            break
        elif item in result:
            txt.insert(END, "no exchange\n")
            p = result[result.index(item)]
            del result[result.index(item)]
            result.insert(0, p)
            txt.insert(END, "\n")
            txt.insert(END, "当前工作集内的页面为：")
            txt.insert(END, result)
            sum += 1
        else:
            result.insert(0, item)
            loss_page += 1
            sum += 1
            txt.insert(END, "\n")
            txt.insert(END, "当前工作集内的页面为：")
            txt.insert(END, result)
    result_page = float((loss_page) / len(arr))
    txt.insert(END, "LRU缺页率为：%.2f" % result_page)
    txt.insert(END, "\n")


def bidui(param, result):
    list_1 = {}
    for item in param:
        list_1[item] = param.index(item)
    for i in result:
        if i not in list_1.keys():
            return i
        else:
            pass
    return list(list_1.keys())[list(list_1.values()).index(max(list_1.values()))]


def run3(inp, txt, arr, pos):
    page = int(inp.get())
    pos_start = int(pos.get(), 16)
    txt.insert(END, "OPT页面置换过程为:\n")
    result = []
    loss_page = 0
    sum = 0
    for item in arr:
        if len(result) == page:
            for j in range(sum, len(arr)):
                if arr[j] in result:
                    txt.insert(END, "no exchange\n")
                    p = result[result.index(arr[j])]
                    del result[result.index(arr[j])]
                    result.insert(0, p)
                    txt.insert(END, "\n")
                    txt.insert(END, "当前工作集内的页面为：")
                    txt.insert(END, result)
                else:
                    result_number = bidui(arr[j:len(arr)], result)
                    for o in result:
                        if result_number == o:
                            result.remove(o)
                            result.append(arr[j])
                            loss_page += 1
                            txt.insert(END, "\n")
                            txt.insert(END,
                                       "弹出页面的物理地址为：%s\n" % bin(calPos(pos_start, int(o))).replace('0b', ''))
                            txt.insert(END, "弹出页面的相对页号为：%s\n" % int(o))
                            txt.insert(END, "当前工作集内的页面为：")
                            txt.insert(END, result)
            break
        elif item in result:
            txt.insert(END, "\n")
            txt.insert(END, "no exchange\n")
            txt.insert(END, "当前工作集内的页面为：")
            txt.insert(END, result)

            sum += 1
        else:
            result.append(item)
            loss_page += 1
            sum += 1
            txt.insert(END, "\n")
            txt.insert(END, "当前工作集内的页面为：")
            txt.insert(END, result)

    result_page = float((loss_page) / len(arr))
    txt.insert(END, "OPT缺页率为：%.2f" % result_page)
    txt.insert(END, "\n")


def run4(inp, txt, arr, pos):
    page = int(inp.get())
    pos_start = int(pos.get(), 16)
    txt.insert(END, "CLOCK页面置换过程为:\n")
    loss_page = 0
    sum = 0
    clock = ClockPageReplacement(page)
    for item in arr:
        status = clock.page_in(item)
        if status == -1:
            loss_page += 1
            sum += 1
            txt.insert(END, "\n")
            ans = []
            for i in clock.frames:
                if i is not None:
                    ans.append(i['page'])
            txt.insert(END, "当前工作集内的页面为：")
            txt.insert(END, ans)
        elif status == None:
            txt.insert(END, "no exchange\n")
            ans = []
            for i in clock.frames:
                if i is not None:
                    ans.append(i['page'])
            txt.insert(END, "当前工作集内的页面为：")
            txt.insert(END, ans)
            sum += 1
        else:
            loss_page += 1
            sum += 1
            txt.insert(END, "\n")
            ans = []
            for i in clock.frames:
                if i is not None:
                    ans.append(i['page'])
            txt.insert(END, "弹出页面的物理地址为：%s\n" % bin(calPos(pos_start, int(status))).replace('0b', ''))
            txt.insert(END, "弹出页面的相对页号为：%s\n" % int(status))
            txt.insert(END, "当前工作集内的页面为：")
            txt.insert(END, ans)
    result_page = float((loss_page + page) / len(arr))
    txt.insert(END, "CLOCK缺页率为：%.2f\n" % result_page)
    txt.insert(END, "\n")


def restart_program():
    python = sys.executable
    os.execl(python, python, 'D:\\PythonCode\\os_test01\\begin.py')


def main(arr=None):
    if arr is None:
        arr = ['1', '2', '3', '4', '5', '6']
    root = Tk()
    root.title('FIFO,OPT,LRU页面置换算法')
    lb = Label(root, text='', fg='blue', font=("黑体", 24))
    lb.pack()
    root.geometry('800x800')
    lb12 = Label(root, text="请输入第一个页框的物理地址（用四位16进制数表示）")
    lb12.place(relx=0.1, rely=0.05, relwidth=0.8, relheight=0.05)
    pos = Entry(root)
    pos.place(relx=0.3, rely=0.12, relwidth=0.4, relheight=0.05)

    label = Label(root, text="待处理页面序列为：")
    label.place(relx=0.1, rely=0.2, relwidth=0.8, relheight=0.016)

    lb1 = Label(root, text='请输入工作集大小：按下面四个按钮之一进行算法验证')
    lb1.place(relx=0.1, rely=0.24, relwidth=0.8, relheight=0.1)
    str_arr = str(arr)
    lb2 = Label(root, text=str_arr)
    lb2.place(relx=0.1, rely=0.22, relwidth=0.8, relheight=0.025)
    inp = Entry(root)
    inp.place(relx=0.3, rely=0.3, relwidth=0.4, relheight=0.1)

    # 方法-直接调用FIFO run1()
    btn1 = Button(root, text='FIFO', command=lambda: run1(inp, txt, arr, pos))
    btn1.place(relx=0.1, rely=0.4, relwidth=0.2, relheight=0.1)

    # 方法二利用 LRU 传参数调用run2()
    btn2 = Button(root, text='LRU', command=lambda: run2(inp, txt, arr, pos))
    btn2.place(relx=0.3, rely=0.4, relwidth=0.2, relheight=0.1)

    # 方法三利用 OPT 传参数调用run3()
    btn3 = Button(root, text='OPT', command=lambda: run3(inp, txt, arr, pos))
    btn3.place(relx=0.5, rely=0.4, relwidth=0.2, relheight=0.1)

    btn3 = Button(root, text='CLOCK', command=lambda: run4(inp, txt, arr, pos))
    btn3.place(relx=0.7, rely=0.4, relwidth=0.2, relheight=0.1)

    lb_txt = Label(root, text='检验结果:')
    lb_txt.place(relx=0.1, rely=0.5, relwidth=0.3, relheight=0.1)
    txt = Text(root)
    txt.place(rely=0.6, relheight=0.4)

    b1 = Button(root, relief='flat', activebackground='orange', bg='lightgreen', overrelief='raised',
                text='重新输入数组',
                command=restart_program)
    b1.place(relx=0.8, rely=0.6, relwidth=0.1, relheight=0.05)

    root.mainloop()


if __name__ == '__main__':
    main()
