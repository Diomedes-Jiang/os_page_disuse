from tkinter import *
import GUI

window=Tk()
window.title('预备状态')
window.geometry('300x100')
label=Label(window,text="请输入页面序列（用逗号分隔）")
label.pack()
arr_input = Entry(window)
arr_input.pack()

arr = []

def getArr():
    input = arr_input.get()
    input_list = input.split(',')
    arr.extend(input_list)


def allCommand():
    getArr()
    window.destroy()
    GUI.main(arr)

submit_button = Button(window, text="提交", command=allCommand)
submit_button.pack()

window.mainloop()

